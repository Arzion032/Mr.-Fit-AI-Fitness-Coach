from astra_db import user_profile, notes
from datetime import datetime

def update_user_profile(existing, update_type, **kwargs):
    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
        update_field = {"goals": existing["goals"]}
    else:
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}
        
    user_profile.update_one(
        {"_id": existing["_id"]}, {"$set": update_field}
    )
    
    return existing
    
def add_note(note, user_id):
    new_note = {
        "user_id": user_id, 
        "text": note, 
        "$vectorize": note, 
        "metadata": {"injested": datetime.now()},
        }
    result = notes.insert_one(new_note)
    new_note["_id"] = result.inserted_id
    return new_note

def delete_note(note_id):
    return notes.delete_one({"_id":note_id})