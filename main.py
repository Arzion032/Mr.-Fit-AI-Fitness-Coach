import streamlit as st
from user_profiles import  create_profile, get_profile, get_notes
from submit import update_user_profile, add_note, delete_note
from mr_fit import advice_mr_fit, big_boi_macro

st.set_page_config(
        page_title="Mr. Fit",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="auto"
    )

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
        
        genders = ("Male", "Female", "Other")
        gender = st.selectbox(
            "Gender:", 
            genders, 
            index=genders.index(
                user["general"].get("gender", "Moderately Oter")
                )
            )
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
        
        submit_profile = st.form_submit_button("Save Profile Info")
        
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

        goals_submit = st.form_submit_button('Update Goals')
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
    
    if nutrition.button("Mr. Fit's Macro Suggestion⚡"):
        result = big_boi_macro(user.get("general"), user.get("goals"))
        user["nutrition"] = result
        nutrition.success("AI has generated the results.")
        
    with nutrition.form("nutrition_form", border=False): 
        
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        with col1:
            calories = st.number_input(
                "Calories:", 
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("calories", 0),
                )
            
        with col2:
            protein = st.number_input(
                "Proteins:", 
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("protein", 0),
                )
        with col3:
            fat = st.number_input(
                "Fats:", 
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("fat", 0),
                )
        with col4:       
            carbs = st.number_input(
                "Carbohydrates:",  
                min_value=0, 
                step=1, 
                value=user["nutrition"].get("carbs", 0),
                )
        
        if st.form_submit_button("Save Macros"):
            with st.spinner("Let Mr. Fit Cook🔥"): 
                st.session_state.profile = update_user_profile(
                    user, 
                    "nutrition", 
                    calories=calories,
                    protein=protein, 
                    fat=fat,
                    carbs=carbs,
                    )
                st.success("Information Updated")
        
@st.fragment()
def notes():
    note_section = st.container(border=True)
    note_section.subheader("Notes:")

    # Iterate through saved notes
    for i, note in enumerate(st.session_state.notes):
        with note_section.container(border=True):  # Ensure each note is in its own box
            cols = st.columns([19,1])  # Layout for text and delete button
            
            with cols[0]:
                st.text(note.get("text"))
            
            with cols[1]:
                if st.button("Delete", key=f"delete_{i}"):  # Unique keys prevent button conflicts
                    delete_note(note.get("_id"))
                    st.session_state.notes.pop(i)
                    st.rerun()
    
    new_note = note_section.text_input("Add a new note: ")
    if note_section.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()
            
@st.fragment()
def ask_mr_fit():
    
    st.subheader("Let’s crush your goals!🚀")
    user_question = st.text_input("How can I help?", placeholder="Ask anyting...")
    
    user = st.session_state.profile
    name = user["general"]["name"]
    
    if st.button("Ask Mr. Fit"):
        with st.spinner("Mr. Fit Working..."):
            advice = advice_mr_fit(user_question, user, name)

            st.markdown("""
            <style>
            .bordered-container {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 15px;
                margin: 10px 0px;
            }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown(f'<div class="bordered-container">{advice}</div>', unsafe_allow_html=True)
                

# Initialize the state or create one
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
    st.markdown("""
    <h1 style='text-align: center;'>Mr. Fit: AI-Powered Fitness Coach💪🔥</h1>
    <style>
        div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
        }
        div[data-testid="stTabs"] button {
            flex-grow: 1;
            text-align: center;
        }
        button[data-baseweb="tab"] {
        font-size: 32px !important;
        font-weight: bold !important;
}
      
    </style>
""", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Ask Mr. Fit", "Profile"])
    forms()
    with tab1:
        ask_mr_fit()
    with tab2:
        prof,macro = st.columns([2,1])
        with prof:
            profile()
        with macro:
            macros()
            st.write("")
            st.write("")
            goals_form()
        notes()