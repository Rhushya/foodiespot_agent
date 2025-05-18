# Core agent logic, LLM interaction, tool calling will go here

import json
from groq import Groq
from typing import List, Dict, Any, Optional
from datetime import datetime

from .config import GROQ_API_KEY
from .tools import TOOL_REGISTRY, AVAILABLE_TOOLS_SCHEMAS, SearchRestaurantsTool, CheckAvailabilityTool, MakeReservationTool 

# The model we'll use for Groq
LLM_MODEL = "llama3-8b-8192" 

class GroqAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.conversation_history = []
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        prompt = (
            "You are 'FoodieSpot Assistant', a friendly and efficient AI assistant for the FoodieSpot restaurant chain. "
            "Your primary goal is to help users find restaurants, check availability, and make reservations. "
            "You must use the provided tools to answer questions and perform actions. Do not make up information about restaurants, availability, or reservations. "
            "When a user asks to make a reservation, first check availability using the 'CheckAvailabilityTool'. Only if it's available, then proceed to use 'MakeReservationTool'."
            "Always confirm details with the user before making a reservation (e.g., restaurant name, date, time, party size)."
            "If you need to ask for clarification, do so. Be polite and helpful."
            "If a tool is called and provides information, use that information to formulate your response to the user."
            "If a search yields multiple results, list them clearly. If no results are found, inform the user politely."
            "Today's date is " + datetime.today().strftime("%Y-%m-%d") + ". Assume reservations are for today unless specified otherwise."
            "\nAvailable Tools:\n"
        )
        for tool_schema in AVAILABLE_TOOLS_SCHEMAS:
            prompt += f"- Tool Name: {tool_schema['title']}\n"
            prompt += f"  Description: {tool_schema['description']}\n"
            prompt += "  Parameters (JSON Schema):\n"
            prompt += json.dumps(tool_schema['properties'], indent=4) + "\n"
            if 'required' in tool_schema and tool_schema['required']:
                 prompt += f"  Required Parameters: {', '.join(tool_schema['required'])}\n"
            prompt += "\n"
        
        prompt += """When you need to use a tool, respond with a JSON object in the following format AS PART OF YOUR RESPONSE TEXT, and NOTHING ELSE after it if you are calling a tool:
        ```json
        {
          \"tool_calls\": [
            {
              \"name\": \"<tool_name>\",
              \"arguments\": {\"<arg_name>\": \"<arg_value>\", ...}
            }
            // You can call multiple tools if needed by adding more objects to the list
          ]
        }
        ```
        Replace `<tool_name>` with the name of the tool you want to call (e.g., SearchRestaurantsTool) and `<arg_name>` and `<arg_value>` with the appropriate arguments and their values based on the tool's parameters. Ensure arguments are correctly typed (e.g. integers for party_size).
        If you don't need to call a tool, just respond in natural language.
        """
        return prompt

    def _call_llm(self, messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=LLM_MODEL,
                temperature=0.7, 
                # max_tokens=1024, 
                # top_p=1, 
                # stop=None, 
                # stream=False, 
            )
            return chat_completion.choices[0].message
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return None

    def _execute_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if tool_name in TOOL_REGISTRY:
            tool_function = TOOL_REGISTRY[tool_name]
            try:
                return tool_function(**arguments)
            except Exception as e:
                return f"Error executing tool {tool_name}: {str(e)}"
        else:
            return f"Error: Tool '{tool_name}' not found."

    def handle_user_query(self, user_query: str) -> str:
        if not self.conversation_history: 
            self.conversation_history.append({"role": "system", "content": self.system_prompt})
        
        self.conversation_history.append({"role": "user", "content": user_query})

        llm_response = self._call_llm(self.conversation_history)

        if not llm_response or not llm_response.content:
            self.conversation_history.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."}) 
            return "Sorry, I encountered an error. Please try again."

        response_content = llm_response.content.strip()
        
        tool_calls_data = None
        if response_content.startswith("```json"):
            try:
                json_block_match = response_content[len("```json\n"):-len("```")]
                parsed_json = json.loads(json_block_match)
                if "tool_calls" in parsed_json and isinstance(parsed_json["tool_calls"], list):
                    tool_calls_data = parsed_json["tool_calls"]
                    self.conversation_history.append({"role": "assistant", "content": response_content})
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e} in response: {response_content}") 
                pass 
            except Exception as e:
                print(f"Error parsing tool call JSON: {e}")
                pass 
        
        if tool_calls_data:
            tool_results_messages = []
            for tool_call in tool_calls_data:
                tool_name = tool_call.get("name")
                arguments = tool_call.get("arguments")
                if tool_name and isinstance(arguments, dict):
                    print(f"Executing tool: {tool_name} with args: {arguments}") 
                    tool_result = self._execute_tool_call(tool_name, arguments)
                    tool_results_messages.append({
                        "role": "tool", 
                        "content": f"Tool {tool_name} execution result: {json.dumps(tool_result)}" 
                    })
                else:
                    tool_results_messages.append({"role": "assistant", "content": "I tried to use a tool but the call was malformed."})
            
            self.conversation_history.extend(tool_results_messages)
            
            final_llm_response_obj = self._call_llm(self.conversation_history)
            
            if final_llm_response_obj and final_llm_response_obj.content:
                final_response = final_llm_response_obj.content.strip()
                self.conversation_history.append({"role": "assistant", "content": final_response})
                return final_response
            else:
                err_msg = "Sorry, I executed the action but had trouble formulating a response."
                self.conversation_history.append({"role": "assistant", "content": err_msg})
                return err_msg
        else:
            self.conversation_history.append({"role": "assistant", "content": response_content})
            return response_content

# Example usage (for testing, will be used by Streamlit app later)
if __name__ == '__main__':
    agent = GroqAgent()
    
    print("FoodieSpot Assistant. Ask about restaurants or make a reservation.")

    while True:
        user_input = input("\nUSER: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.handle_user_query(user_input)
        print(f"ASSISTANT: {response}")
