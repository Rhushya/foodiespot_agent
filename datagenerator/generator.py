import json
import os
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Output file
output_file = "restaurants_data.json"
with open(output_file, "w") as f:
    f.write("[]")  # Initialize the file with an empty list

# Predefined options
cuisines = [
    "South Indian", "North Indian", "Continental", "Multi-Cuisine",
    "Microbrewery", "Coastal Indian", "Vietnamese", "Burmese"
]

special_notes = [
    "Iconic for crispy dosas and filter coffee.",
    "Authentic seafood from coastal India.",
    "Famous for steaks and burgers.",
    "Craft beers and wood-fired pizzas.",
    "India’s largest brewpub with rooftop seating.",
    "Known for royal Mughlai dishes and luxurious ambiance.",
    "Offers traditional village-style meals, especially during festivals.",
    "Vegetarian Burmese cuisine with a modern twist.",
    "Luxury hotel offering diverse dining options in a serene setting.",
    "India’s first Vietnamese restaurant with an elegant outdoor setting.",
    "Retro-themed restaurant with a rock-and-roll vibe.",
    "Panoramic city views and a relaxed rooftop ambiance."
]

working_hours = [
    "06:00-15:00", "07:00-23:00", "11:00-23:00",
    "12:00-15:00, 19:00-23:00", "12:00-00:00",
    "24 Hours", "10:30-23:30"
]

restaurant_types = ["Tiffin Room", "Bistro", "Cafe", "Lounge", "Kitchen", "House", "Place", "Grill"]

def generate_restaurant(index):
    return {
        "id": f"BLR{str(index + 1).zfill(3)}",
        "name": f"{fake.last_name()} {random.choice(restaurant_types)}",
        "location": fake.street_name(),
        "cuisine": random.choice(cuisines),
        "seating_capacity": random.randint(50, 200),
        "hours": random.choice(working_hours),
        "contact": f"+91 {random.randint(6, 9)}{random.randint(100000000, 999999999)}",
        "special_notes": random.choice(special_notes)
    }

# Generate and save data to a single JSON file
with open(output_file, "r+") as f:
    data = json.load(f)
    for i in range(100):
        data.append(generate_restaurant(i))
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()

print("✅ Generated data and stored it in 'restaurants_data.json' file.")
