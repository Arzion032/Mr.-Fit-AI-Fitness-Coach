import streamlit as st
from user_profiles import  create_profile, get_profile, get_notes
from submit import update_user_profile, add_note, delete_note
from mr_fit import get_macros

st.title("Mr. Fit: AI-Powered Fitness Coach")

@st.fragment()
def profile():
    
    with st.form("user_profile"):
        st.header("Profile")
        
        user = st.session_state.profile 
        
        name = st.text_input(
            "Name", 
            value=user["general"]["name"]
            )
        age = st.number_input(
            "Age", 
            min_value=5, 
            max_value=100, 
            step=1, 
            value=user["general"]["age"]
            )
        weight = st.number_input(
            "Weight (kg)", 
            min_value=20.0, 
            max_value=450.0, 
            step=0.1, 
            value=float(user["general"]["weight"])
            )
        height = st.number_input(
            "Height (cm)", 
            min_value=50.0, 
            max_value=300.0, 
            step=0.1, 
            value=float(user["general"]["height"])
            )
        
        genders = ["Male", "Female", "Other"]
        gender = st.radio("Gender", genders, genders.index(user["general"].get("gender", "Male")))
        
        activities =  (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Super Active"
        )
        activity_level = st.selectbox(
            "Activity Level", 
            activities, 
            index=activities.index(
                user["general"].get("activity_level", "Moderately Active")
                )
            )
        
        submit_profile = st.form_submit_button("Save")
        
        if submit_profile:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    st.session_state.profile = update_user_profile(
                        user,
                        "general", 
                        name=name, 
                        age=age, 
                        weight=weight, 
                        height=height, 
                        gender=gender, 
                        activity_level=activity_level
                        )
                    st.success('Profile Saved')
            else: 
                st.warning("Please fill in all of the data")
                
@st.fragment()
def goals_form():
    user = st.session_state.profile
    with st.form("user_goals"):
        st.header("Goals")
        goals = st.multiselect(
            "What is your goal?", 
            ["Muscle Gain", "Fat Loss", "Stay Active", "Build Strength", "Improve Flexibility"],
            default=user.get('goals',['Stay Active'])
        )

        goals_submit = st.form_submit_button('Save')
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_user_profile(user, "goals", goals=goals)
                    st.success('Goals saved successfully')
            else: 
                st.warning("Please select at least one goal.")
                
@st.fragment()
def macros():
    user = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    
    if nutrition.button("Generate with AI"):
        result = get_macros(user.get("general"), user.get("goals"))
        user["nutrition"] = result
        nutrition.success("AI has generated the results.")
        
    with nutrition.form("nutrition_form", border=False): 
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories = st.number_input(
                "Calories", 
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("calories", 0),
                )
        with col2:
            protein = st.number_input(
                "protein", 
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("protein", 0),
                )
        with col3:
            fat = st.number_input(
                "fat", 
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("fat", 0),
                )
        with col4:
            carbs = st.number_input(
                "carbs", 
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("carbs", 0),
                )
        
        if st.form_submit_button("Save"):
            with st.spinner(): 
                st.session_state.profile = update_user_profile(
                    user, 
                    "nutrition", 
                    protien=protein, 
                    calorie=calories,
                    fat=fat,
                    carbs=carbs,
                    )
                st.success("Information Updated")
        
    
def forms():
    
    if "profile" not in st.session_state:
        user_id = 1
        user = get_profile(user_id)
        
        if not user:
            user_id, user = create_profile(user_id)
            
        st.session_state.profile = user
        st.session_state.profile_id = user_id
        
    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)


if __name__ == "__main__":
    forms()
    profile()
    goals_form()
    macros()