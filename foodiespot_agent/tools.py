# Definitions of tools like find_restaurant, make_reservation will go here
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import datetime
import uuid # For generating unique reservation IDs

# Import restaurant data and reservations list
from .restaurant_data import RESTAURANTS, RESERVATIONS

# --- Tool Pydantic Models ---

class SearchRestaurantsTool(BaseModel):
    """
    Searches for restaurants based on various criteria.
    All parameters are optional. If no parameters are provided, it may return a few general suggestions.
    """
    cuisine: Optional[str] = Field(None, description="The type of cuisine (e.g., Italian, Mexican, Indian).")
    location: Optional[str] = Field(None, description="The desired location or area (e.g., Downtown, Uptown, Suburbia).")
    name: Optional[str] = Field(None, description="The specific name of the restaurant.")
    min_capacity: Optional[int] = Field(None, description="Minimum seating capacity preferred.")

class CheckAvailabilityTool(BaseModel):
    """
    Checks the availability of a specific restaurant for a given date, time, and party size.
    """
    restaurant_id: str = Field(..., description="The unique ID of the restaurant (e.g., FS001).")
    date: str = Field(..., description="The desired date for the reservation (YYYY-MM-DD).")
    time: str = Field(..., description="The desired time for the reservation (HH:MM in 24-hour format).")
    party_size: int = Field(..., description="The number of people in the party.")

class MakeReservationTool(BaseModel):
    """
    Makes a reservation at a specific restaurant for a given date, time, party size, and customer details.
    This tool should only be called after confirming availability.
    """
    restaurant_id: str = Field(..., description="The unique ID of the restaurant (e.g., FS001).")
    date: str = Field(..., description="The date for the reservation (YYYY-MM-DD).")
    time: str = Field(..., description="The time for the reservation (HH:MM in 24-hour format).")
    party_size: int = Field(..., description="The number of people in the party.")
    customer_name: str = Field(..., description="The name of the customer making the reservation.")
    customer_contact: Optional[str] = Field(None, description="The contact information for the customer (phone or email).")

# --- Tool Implementation Functions ---

def search_restaurants(cuisine: Optional[str] = None, location: Optional[str] = None, name: Optional[str] = None, min_capacity: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Implements the logic to search for restaurants from the RESTAURANTS list.
    """
    results = []
    for r in RESTAURANTS:
        match = True
        if cuisine and cuisine.lower() not in r["cuisine"].lower():
            match = False
        if location and location.lower() not in r["location"].lower():
            match = False
        if name and name.lower() not in r["name"].lower():
            match = False
        if min_capacity and r["seating_capacity"] < min_capacity:
            match = False
        
        if match:
            results.append(r)
    
    if not results and not any([cuisine, location, name, min_capacity]): # If no criteria and no results, maybe suggest a few popular ones
        return RESTAURANTS[:3] # Return first 3 as general suggestions
    return results

def check_availability(restaurant_id: str, date: str, time: str, party_size: int) -> Dict[str, Any]:
    """
    Implements the logic to check restaurant availability.
    This is a simplified check: it checks if the restaurant exists and if party_size <= capacity.
    A real system would check against existing reservations for that date/time.
    """
    restaurant = next((r for r in RESTAURANTS if r["id"] == restaurant_id), None)
    if not restaurant:
        return {"available": False, "message": f"Restaurant with ID {restaurant_id} not found."}

    # Simplified check: just ensure party size isn't greater than total capacity
    # A more complex check would sum up party_sizes of existing reservations for the given date/time slot
    # and see if (current_bookings + party_size) <= seating_capacity.
    
    # Let's simulate a basic check for existing reservations for the exact slot
    # This is still very basic, doesn't account for reservation duration etc.
    booked_slots_for_datetime = sum(
        res["party_size"] for res in RESERVATIONS 
        if res["restaurant_id"] == restaurant_id and res["date"] == date and res["time"] == time
    )

    if (booked_slots_for_datetime + party_size) <= restaurant["seating_capacity"]:
        return {"available": True, "message": f"Restaurant {restaurant['name']} has potential availability for {party_size} on {date} at {time}."}
    else:
        return {"available": False, "message": f"Sorry, Restaurant {restaurant['name']} does not have availability for {party_size} on {date} at {time} (currently booked: {booked_slots_for_datetime}, capacity: {restaurant['seating_capacity']})."}


def make_reservation(restaurant_id: str, date: str, time: str, party_size: int, customer_name: str, customer_contact: Optional[str] = None) -> Dict[str, Any]:
    """
    Implements the logic to make a reservation and adds it to the RESERVATIONS list.
    """
    availability_check = check_availability(restaurant_id, date, time, party_size)
    if not availability_check["available"]:
        return {"success": False, "message": f"Cannot make reservation. {availability_check['message']}", "reservation_id": None}

    restaurant = next((r for r in RESTAURANTS if r["id"] == restaurant_id), None)
    if not restaurant: # Should have been caught by check_availability, but good to double check
        return {"success": False, "message": f"Restaurant with ID {restaurant_id} not found.", "reservation_id": None}

    reservation_id = f"R{uuid.uuid4().hex[:7].upper()}" # Generate a unique reservation ID
    
    new_reservation = {
        "reservation_id": reservation_id,
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant["name"], # Store name for easier display
        "date": date,
        "time": time,
        "party_size": party_size,
        "customer_name": customer_name,
        "customer_contact": customer_contact,
        "status": "confirmed" # or "pending" initially
    }
    RESERVATIONS.append(new_reservation)
    
    return {
        "success": True, 
        "message": f"Reservation confirmed for {customer_name} at {restaurant['name']} on {date} at {time} for {party_size} people. Your reservation ID is {reservation_id}.",
        "reservation_id": reservation_id
    }

# --- Tool Mapping ---
# This mapping will be used by the agent to find the actual function to call based on the tool name from LLM
TOOL_REGISTRY = {
    "SearchRestaurantsTool": search_restaurants,
    "CheckAvailabilityTool": check_availability,
    "MakeReservationTool": make_reservation,
}

# For the LLM to know about available tools, we need their schemas.
# We can generate JSON schemas from Pydantic models.
AVAILABLE_TOOLS_SCHEMAS = [
    SearchRestaurantsTool.schema(),
    CheckAvailabilityTool.schema(),
    MakeReservationTool.schema(),
]
