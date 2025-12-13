import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Greenscape",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply minimal Streamlit-native CSS
st.markdown("""
<style>
/* ========== FRUTIGER AERO USING STREAMLIT CLASSES ONLY ========== */

/* Main app - Frutiger Aero gradient background */
.stApp {
    background: linear-gradient(135deg, #d4f1ff 0%, #b8e8d8 100%) !important;
}

/* Fix ALL text colors - ensure dark text for readability */
h1, h2, h3, h4, h5, h6,
div, p, span, label,
[data-testid="stMarkdownContainer"],
[class*="st-"] {
    color: #0a5c36 !important;
}

/* Fix form text specifically */
[data-baseweb="form"] label,
[data-baseweb="select"] div,
[data-baseweb="input"] label,
[data-baseweb="textarea"] label {
    color: #0a5c36 !important;
    font-weight: 500 !important;
}

/* Fix input fields - white text issue */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    color: #0a5c36 !important;
    background-color: rgba(255, 255, 255, 0.9) !important;
    border-radius: 10px !important;
    border: 2px solid #4caf50 !important;
}

/* Fix select/dropdown - black with white text issue */
[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.9) !important;
    border-radius: 10px !important;
    border: 2px solid #4caf50 !important;
}

[data-baseweb="select"] [role="listbox"] {
    background-color: white !important;
    color: #0a5c36 !important;
}

/* Fix dataframe styling */
[data-testid="stDataFrame"] {
    border: 2px solid #4caf50 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

[data-testid="stDataFrame"] table {
    background-color: rgba(255, 255, 255, 0.9) !important;
}

[data-testid="stDataFrame"] th {
    background: linear-gradient(to bottom, #4caf50, #2e7d32) !important;
    color: white !important;
    border: none !important;
}

[data-testid="stDataFrame"] td {
    color: #0a5c36 !important;
    border-bottom: 1px solid #81c784 !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #e6f7fb, #c5e8ca) !important;
    border-right: 3px solid #4caf50 !important;
}

/* Buttons - Frutiger Aero glossy style */
.stButton > button {
    background: linear-gradient(to bottom, #4dff77, #02ddd1) !important;
    color: white !important;
    border-radius: 15px !important;
    border: 1px solid #81d4fa !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 8px rgba(3, 169, 244, 0.3), 
                inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.2);
}

.stButton > button:hover {
    background: linear-gradient(to bottom, #29b6f6, #0277bd) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(3, 169, 244, 0.4), 
                inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
}

/* Metrics styling */
[data-testid="stMetricValue"] {
    color: #0a5c36 !important;
    font-size: 24px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricLabel"] {
    color: #2e7d32 !important;
    font-weight: 500 !important;
}

/* Progress bars */
[role="progressbar"] > div {
    background-color: #4caf50 !important;
    border-radius: 10px !important;
}

/* Tabs */
[data-baseweb="tab-list"] [role="tab"] {
    background: linear-gradient(to bottom, #e8f5e9, #c8e6c9) !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid #81c784 !important;
    color: #0a5c36 !important;
    font-weight: 500 !important;
}

[data-baseweb="tab-list"] [aria-selected="true"] {
    background: linear-gradient(to bottom, #4caf50, #2e7d32) !important;
    color: white !important;
}

/* Radio buttons and checkboxes */
[data-baseweb="radio"] label,
[data-baseweb="checkbox"] label {
    color: #0a5c36 !important;
}

/* Expandable containers */
[data-testid="stExpander"] {
    border: 1px solid #4caf50 !important;
    border-radius: 10px !important;
}

/* Alert boxes */
[data-testid="stAlert"] {
    border-left: 5px solid #4caf50 !important;
    border-radius: 8px !important;
}

/* Divider */
hr {
    border-bottom: 2px solid #4caf50 !important;
}

/* Main content container */
.main .block-container {
    background-color: rgba(255, 255, 255, 0.9) !important;
    border-radius: 15px !important;
    box-shadow: 0 8px 20px rgba(0, 100, 0, 0.1) !important;
    border: 1px solid rgba(76, 175, 80, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🌿 Greenscape")
st.markdown("### Connect with plant enthusiasts worldwide")

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    page = st.selectbox(
        "Go to:",
        ["Dashboard", "My Plants", "Community", "Identify", "Profile"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("### Filters")
    categories = st.multiselect(
        "Plant categories:",
        ["Succulents", "Tropical", "Flowering", "Ferns", "Cacti", "Herbs"],
        default=["Succulents", "Tropical"]
    )
    
    st.divider()
    
    st.metric("Your Plants", "24")
    st.metric("Followers", "128")
    
    if st.button("🌱 New Post", use_container_width=True):
        st.session_state.show_form = True

# Main content
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Posts", "1,842", "+42 today")
    with col2:
        st.metric("Active Users", "289", "Online now")
    with col3:
        st.metric("Plants Shared", "8,429", "+128 this week")
    
    st.divider()
    
    # Recent posts
    st.subheader("Recent Community Posts")
    
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("https://images.unsplash.com/photo-1598880940080-ff9a29891b85", width=100)
        with col2:
            st.markdown("**Monstera Deliciosa** by @PlantLover")
            st.caption("Just repotted my Monstera! The aerial roots are amazing.")
            if st.button("❤️ 42", key="like1"):
                st.rerun()
    
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("https://images.unsplash.com/photo-1589923186741-b7d59d6b2c4d", width=100)
        with col2:
            st.markdown("**Snake Plant** by @UrbanGardener")
            st.caption("Thriving in low light office conditions.")
            if st.button("❤️ 28", key="like2"):
                st.rerun()

elif page == "My Plants":
    st.subheader("Your Plant Collection")
    
    # Sample plant data
    plant_data = pd.DataFrame({
        'Plant': ['Monstera Deliciosa', 'Snake Plant', 'Peace Lily', 'Spider Plant', 'Pothos'],
        'Type': ['Tropical', 'Succulent', 'Flowering', 'Foliage', 'Vining'],
        'Health': [90, 95, 75, 88, 92],
        'Last Watered': ['2 days ago', '5 days ago', 'Yesterday', '3 days ago', '4 days ago']
    })
    
    # Display styled dataframe
    st.dataframe(plant_data, use_container_width=True)
    
    st.divider()
    
    # Care schedule
    st.subheader("Care Schedule")
    st.progress(0.75, text="Watering: 3 of 4 plants done")
    st.progress(0.50, text="Fertilizing: 2 of 4 plants done")

elif page == "Community":
    st.subheader("Plant Community")
    
    # Community stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Top Members", "1,842")
    with col2:
        st.metric("Posts Today", "42")
    with col3:
        st.metric("Active Now", "289")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🌿 Discussions", "🏆 Challenges", "📊 Leaderboard"])
    
    with tab1:
        st.info("Join the Monstera care discussion!")
        st.success("New variegated plant varieties spotted")
        
    with tab2:
        st.warning("30-Day Plant Care Challenge: 12 days remaining")
        st.button("Join Challenge", key="join_challenge")
        
    with tab3:
        leaderboard_data = pd.DataFrame({
            'Gardener': ['PlantWhisperer', 'GreenThumb99', 'JungleJane', 'SucculentKing'],
            'Plants': [142, 128, 96, 87],
            'Streak': ['156 days', '128 days', '94 days', '87 days']
        })
        st.dataframe(leaderboard_data, use_container_width=True)

elif page == "Identify":
    st.subheader("Plant Identifier")
    
    # Upload section
    uploaded_file = st.file_uploader("Upload a plant photo", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Your plant photo", width=300)
        
        # Analysis form
        with st.form("analysis_form"):
            st.markdown("### Plant Details")
            col1, col2 = st.columns(2)
            with col1:
                plant_type = st.selectbox(
                    "Plant Type",
                    ["Unknown", "Succulent", "Tropical", "Flowering", "Fern", "Cactus"]
                )
            with col2:
                light_conditions = st.selectbox(
                    "Light Conditions",
                    ["Full Sun", "Partial Sun", "Shade", "Indirect Light"]
                )
            
            notes = st.text_area("Additional Notes")
            
            if st.form_submit_button("Analyze Plant"):
                st.success("Analysis complete! Likely match: Monstera Deliciosa (92%)")
                
        # Care tips expander
        with st.expander("View Care Tips"):
            st.markdown("""
            **Monstera Deliciosa Care:**
            - Water when top inch of soil is dry
            - Bright, indirect sunlight
            - Mist leaves regularly
            - Fertilize monthly during growing season
            """)

elif page == "Profile":
    st.subheader("Your Profile")
    
    # Profile form with proper styling
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", "PlantLover42")
            location = st.text_input("Location", "Zone 7b")
        with col2:
            experience = st.select_slider(
                "Experience Level",
                options=["Beginner", "Intermediate", "Advanced"],
                value="Intermediate"
            )
            member_since = st.date_input("Member Since")
        
        bio = st.text_area("Bio", "Plant enthusiast creating an urban jungle!")
        
        plant_types = st.multiselect(
            "Favorite Plant Types",
            ["Succulents", "Tropical", "Flowering", "Ferns", "Cacti", "Herbs", "Trees"],
            default=["Succulents", "Tropical"]
        )
        
        if st.form_submit_button("Update Profile"):
            st.success("Profile updated successfully!")

# New post form (if triggered from sidebar)
if 'show_form' in st.session_state and st.session_state.show_form:
    with st.form("new_post_form"):
        st.subheader("Create New Post")
        
        post_title = st.text_input("Post Title")
        post_content = st.text_area("Post Content", height=150)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            plant_category = st.selectbox("Category", ["Succulent", "Tropical", "Flowering", "Other"])
        with col2:
            difficulty = st.select_slider("Care Difficulty", ["Easy", "Medium", "Hard"])
        with col3:
            privacy = st.radio("Visibility", ["Public", "Followers Only"])
        
        submitted = st.form_submit_button("Post to Community")
        if submitted:
            st.success("Post published successfully!")
            st.session_state.show_form = False

# Footer
st.divider()
st.caption("🌿 Greenscape • Plant social community • © 2023")