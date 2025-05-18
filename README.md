# FoodieSpot Reservation Agent

A conversational AI solution for FoodieSpot to manage restaurant reservations.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd foodiespot-reservation-agent
    ```

2.  **Create and activate Conda environment:**
    
    **Option A:** Using environment.yml file (recommended):
    ```bash
    conda env create -f environment.yml
    conda activate foodiespot_env
    ```
    
    **Option B:** Creating environment manually:
    ```bash
    # Create a new conda environment with Python 3.9
    conda create -n foodiespot_env python=3.9
    
    # Activate the environment
    conda activate foodiespot_env
    
    # Install required packages
    pip install -r requirements.txt
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

This project leverages sophisticated prompt engineering techniques to create an effective conversational agent:

* **System Prompt Design**: The system prompt is carefully crafted to establish the assistant's identity as the "FoodieSpot Assistant" and define its purpose and capabilities. It includes:
  * Role definition and personality traits (friendly and efficient)
  * Task-specific instructions for restaurant searches and reservations
  * Tool usage guidelines with error handling procedures
  * Current date reference for contextualizing reservation requests
  * Detailed descriptions of available tools with their parameters

* **Tool-Calling Framework**: The agent implements a JSON-based tool-calling mechanism that allows the LLM to:
  * Select appropriate tools based on user intent
  * Format tool arguments correctly
  * Parse tool responses and incorporate them into natural conversation
  * Handle complex workflows (e.g., checking availability before making reservations)

* **Conversation Management**: The implementation maintains conversation history to provide context for future interactions, allowing for multi-turn conversations with context retention.

## Example Conversations

Below are examples of how users can interact with the FoodieSpot Agent:

### Restaurant Search by Cuisine/Location
```
User: I'm looking for Italian restaurants in Downtown
Assistant: I'll help you find Italian restaurants in Downtown. Let me search for you.

I found 2 Italian restaurants in Downtown area:

1. Bella Italia (ID: FS003)
   - Location: Downtown
   - Seating Capacity: 60
   - Hours: 11:00-22:00
   - Average Rating: 4.7/5

2. Pasta Paradise (ID: FS008)
   - Location: Downtown
   - Seating Capacity: 45
   - Hours: 12:00-21:30
   - Average Rating: 4.3/5

Would you like to check availability at either of these restaurants?
```

### Asking for Recommendations
```
User: Can you recommend a good restaurant for a family dinner?
Assistant: I'd be happy to recommend some restaurants for a family dinner! Here are a few options that would be great for families:

1. Family Feast (ID: FS005)
   - Cuisine: American
   - Location: Suburbia
   - Seating Capacity: 80
   - Average Rating: 4.5/5
   - Perfect for large groups and has a children's menu

2. Garden Grill (ID: FS010)
   - Cuisine: Mixed/Fusion
   - Location: Uptown
   - Seating Capacity: 65
   - Average Rating: 4.6/5
   - Offers a relaxed atmosphere with outdoor seating

3. Spice Avenue (ID: FS007)
   - Cuisine: Indian
   - Location: Midtown
   - Seating Capacity: 50
   - Average Rating: 4.4/5
   - Known for accommodating dietary restrictions

Would you like to know more about any of these restaurants or check availability for a specific date and time?
```

### Making a Reservation
```
User: I'd like to book a table at Bella Italia for tomorrow at 7 PM for 4 people
Assistant: I'll help you make a reservation at Bella Italia for tomorrow at 7 PM for 4 people. Let me first check if they have availability.

Good news! Bella Italia (ID: FS003) has availability for 4 people tomorrow at 19:00. Would you like me to proceed with making the reservation?

User: Yes, please. My name is John Smith and my phone number is 555-123-4567.
Assistant: Great! I've made your reservation. Here are the details:

Reservation confirmed for John Smith at Bella Italia on 2025-05-19 at 19:00 for 4 people. Your reservation ID is R5F3D9A2.

Contact information: 555-123-4567

Is there anything else you'd like help with regarding your reservation?
```

### Handling a Full Restaurant
```
User: I need a table for 10 people at Sushi Spot tonight at 8 PM
Assistant: I'll help you check availability at Sushi Spot for tonight at 8 PM for 10 people.

I'm sorry, but Sushi Spot (ID: FS004) does not have availability for 10 people tonight at 20:00. They currently have 15 seats already booked, and their total capacity is 20, which isn't enough for your party of 10.

Would you like me to suggest some alternative restaurants that might be able to accommodate your group of 10 people? Or perhaps a different time at Sushi Spot?
```

### Error Handling
```
User: Book me a table at Fantasy Food
Assistant: I'll help you book a table at Fantasy Food. Let me first check if this restaurant is in our system.

I'm sorry, but I couldn't find a restaurant named "Fantasy Food" in our database. Would you like me to suggest some other restaurants, or did you perhaps mean a different restaurant name?

Here are some of our popular restaurants:
1. Family Feast - American cuisine in Suburbia
2. Bella Italia - Italian cuisine in Downtown
3. Sushi Spot - Japanese cuisine in Uptown

Please let me know which restaurant you're interested in, or if you'd like to search by cuisine or location instead.
```

## Business Strategy Summary

FoodieSpot's Conversational AI Reservation System addresses several key business challenges and opportunities:

### Current Challenges
* **High Call Volume:** Manual phone reservations are time-consuming for staff, especially during peak hours
* **Inefficient Resource Allocation:** Staff time is diverted from in-person customer service
* **Limited Accessibility:** Reservations can only be made during operating hours
* **Potential for Human Error:** Manual data entry can lead to mistakes
* **Lack of Centralized Data:** Difficulty aggregating reservation data across locations
* **Inconsistent Customer Experience:** Quality varies based on staff availability and workload

### Business Opportunities
* **Enhanced Efficiency:** 24/7 automated reservation process reduces staff workload
* **Improved Customer Experience:** Instant, consistent, and convenient reservation services
* **Increased Booking Conversion:** Easy-to-use interface with intelligent recommendations
* **Valuable Data Insights:** Better understanding of customer behavior and preferences
* **Scalability:** Handle increasing reservation volume without proportional staffing increases
* **Modernized Brand Image:** Position FoodieSpot as a technologically advanced brand

### Success Metrics
* **Adoption Rate:** Target percentage of reservations handled by the AI agent
* **Operational Efficiency:** Reduction in staff time spent on phone reservations
* **Customer Satisfaction:** CSAT scores and reduction in reservation-related complaints
* **System Performance:** Response time, successful intent recognition, and accurate reservations

## Assumptions, Limitations, and Future Enhancements

### Assumptions
* Restaurant data (locations, capacity, hours) is accurate and available
* Users will interact with the system in English
* The primary interaction mode is text-based chat
* For the MVP phase, "real-time" availability is simulated based on existing reservations in memory
* The Groq API key is valid and has sufficient quota for development and testing

### Limitations
* In-memory data storage (not persistent across application restarts)
* Simplified availability checking that doesn't account for reservation duration
* No user authentication or personalization features
* Limited error recovery for complex conversational flows
* No integration with external calendar systems or notification services

### Future Enhancements
* **Database Integration:** Replace in-memory data with a persistent database solution
* **User Accounts & History:** Allow users to create accounts and view past reservations
* **Cancellation/Modification:** Add tools for users to manage existing bookings
* **Multi-language Support:** Expand beyond English to serve diverse customers
* **Voice Interface:** Add voice input/output capabilities for accessibility
* **Calendar Integration:** Sync reservations with popular calendar applications
* **Analytics Dashboard:** Provide restaurant management with key operational metrics
* **Promotional Offers:** Integrate special offers and events information
* **Waitlist Management:** Handle restaurant capacity overflow with waitlists
* **Advanced Recommendation Engine:** Suggest restaurants based on user preferences and history
