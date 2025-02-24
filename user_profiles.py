from astra_db import user_profile, notes

def get_values(user_id):
        return {
        "_id": user_id, 
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male"
        },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 140,
            "fat": 20,
            "carbs": 100,
            },
    }
  
  # Create Dummy Profile      
def create_profile(user_id):
    profile = get_values(user_id)
    result = user_profile.insert_one(profile)
    return result.inserted_id, result

def get_profile(user_id):
    return user_profile.find_one({"_id": {"$eq": user_id}})

def get_notes(_id): 
        return list(notes.find({"user_id": {"$eq": _id}})) 