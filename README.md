# FoodieSpot Reservation Agent

A conversational AI solution for FoodieSpot to manage restaurant reservations.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd foodiespot-reservation-agent
    ```

2.  **Create and activate Conda environment:**
    ```bash
    conda env create -f environment.yml
    conda activate foodiespot_env
    ```

3.  **Configure API Key:**
    Create a file named `config.py` in the `foodiespot_agent` directory (`foodiespot_agent/config.py`) and add your Groq API key:
    ```python
    GROQ_API_KEY = "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"
    ```
    *(**Note**: For a real-world scenario, it's highly recommended to use environment variables for API keys and add `config.py` to `.gitignore` to avoid committing sensitive information.)*

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

## Prompt Engineering Approach

*(To be documented: Describe the system prompts, user prompts, and any specific strategies used to guide the LLM for intent recognition and tool calling.)*

## Example Conversations

*(To be documented: Provide examples of user interactions, including:
*   Searching for a restaurant based on cuisine/location.
*   Asking for recommendations.
*   Making a reservation.
*   Handling cases where a restaurant is full.
*   Error handling.)*

## Business Strategy Summary

*(To be documented: Summarize key points from the `use_case_document.md`.)*

## Assumptions, Limitations, and Future Enhancements

### Assumptions
*   (List any assumptions made during development)

### Limitations
*   (List any known limitations of the current implementation)

### Future Enhancements
*   (Suggest potential future improvements or features)
