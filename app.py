"""
ESA OTC25 Intelligence Panel
==============================
Assessment and Intercomparison of Water Quality Retrieval Methods
Across In-situ, Inline, Drone, Profiling Floats, and Satellite Observations

Authors: Lou Andrès, Mathurin Choblet, Alba Guzmán-Morales,
         Sejal Pramlall, Alejandro Román, Luz Suklje

Date: 2025
"""

# =============================================================================
# IMPORTS
# =============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import pearsonr
import base64

# Load image data
try:
    from image_data import IMAGE_DATA
    from station_data import STATION_DATA, ABBREVIATIONS
except ImportError:
    IMAGE_DATA = {}
    STATION_DATA = {}
    ABBREVIATIONS = {}

# =============================================================================
# COLOR PALETTES
# =============================================================================
# UI colors - https://coolors.co/palette/01161e-124559-598392-aec3b0-eff6e0
UI_COLORS = {
    'darkest': '#01161E',
    'dark': '#124559',
    'medium': '#598392',
    'light': '#AEC3B0',
    'lightest': '#EFF6E0',
    'white': '#FFFFFF'
}

# Chart colors for data points - https://coolors.co/palette/d9ed92-b5e48c-99d98c-76c893-52b69a-34a0a4-168aad-1a759f-1e6091-184e77
CHART_COLORS = [
    '#D9ED92', '#B5E48C', '#99D98C', '#76C893', '#52B69A',
    '#34A0A4', '#168AAD', '#1A759F', '#1E6091', '#184E77'
]

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="ESA OTC25 Intelligence Panel",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
st.markdown(f"""
<style>
    /* Main header styling */
    .main-header {{
        background: linear-gradient(135deg, {UI_COLORS['dark']} 0%, {UI_COLORS['medium']} 100%);
        padding: 2rem;
        border-radius: 10px;
        color: {UI_COLORS['white']};
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}

    /* Section header styling */
    .section-header {{
        background: {UI_COLORS['light']};
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid {UI_COLORS['dark']};
        margin: 1.5rem 0;
    }}

    /* Team member card */
    .team-card {{
        background: {UI_COLORS['lightest']};
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid {UI_COLORS['medium']};
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {UI_COLORS['darkest']};
    }}

    [data-testid="stSidebar"] * {{
        color: {UI_COLORS['lightest']} !important;
    }}

    [data-testid="stSidebar"] input {{
        color: {UI_COLORS['darkest']} !important;
    }}

    /* Button styling */
    .stButton > button {{
        background-color: {UI_COLORS['medium']};
        color: {UI_COLORS['white']};
        border: none;
        border-radius: 5px;
        transition: all 0.3s;
    }}

    .stButton > button:hover {{
        background-color: {UI_COLORS['dark']};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}

    /* Metric styling */
    .metric-card {{
        background: {UI_COLORS['lightest']};
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Category header full width and reduced height */
    .category-header {{
        margin: 2rem 0 1.5rem 0;
    }}

    /* Fix scroll position - ensure page starts at top */
    html {{
        scroll-behavior: auto;
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

@st.cache_data
def load_panel_data():
    """Load main panel data from Excel"""
    try:
        df = pd.read_excel('data/Panel.xlsx')
        return df
    except Exception as e:
        st.error(f"Error loading Panel.xlsx: {e}")
        return pd.DataFrame()

@st.cache_data
def load_argo_data():
    """Load BGC Argo float data"""
    try:
        df1 = pd.read_csv('data/Rrs_5906995.csv')
        df2 = pd.read_csv('data/Rrs_5906995_ut.csv')
        return df1, df2
    except Exception as e:
        st.error(f"Error loading Argo data: {e}")
        return pd.DataFrame(), pd.DataFrame()

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

# Add logos in simple layout
logos_html = '<div style="text-align: center; padding: 0.5rem 0; line-height: 1.2;">'

# Row 1: ESA, NASA, Lemkhul, NERSC
logos_html += '<div style="margin-bottom: 0.6rem;">'
if IMAGE_DATA.get('esa_logo'):
    logos_html += f'<img src="data:image/svg+xml;base64,{IMAGE_DATA["esa_logo"]}" style="width: 45px; height: 45px; margin: 0 4px;" />'
if IMAGE_DATA.get('nasa_logo'):
    logos_html += f'<img src="data:image/png;base64,{IMAGE_DATA["nasa_logo"]}" style="width: 45px; height: 45px; margin: 0 4px;" />'
if IMAGE_DATA.get('lemkhul_logo'):
    logos_html += f'<img src="data:image/png;base64,{IMAGE_DATA["lemkhul_logo"]}" style="width: 45px; height: 45px; margin: 0 4px;" />'
if IMAGE_DATA.get('nersc_logo'):
    logos_html += f'<img src="data:image/png;base64,{IMAGE_DATA["nersc_logo"]}" style="width: 45px; height: 45px; margin: 0 4px;" />'
logos_html += '</div>'

# Row 2: ODL, OneO, TPS
logos_html += '<div>'
if IMAGE_DATA.get('odl_logo'):
    logos_html += f'<img src="data:image/png;base64,{IMAGE_DATA["odl_logo"]}" style="width: 80px; height: 45px; margin: 0 4px;" />'
if IMAGE_DATA.get('oneo_logo'):
    logos_html += f'<img src="data:image/png;base64,{IMAGE_DATA["oneo_logo"]}" style="width: 45px; height: 45px; margin: 0 4px;" />'
if IMAGE_DATA.get('tps_logo'):
    logos_html += f'<img src="data:image/png;base64,{IMAGE_DATA["tps_logo"]}" style="width: 45px; height: 45px; margin: 0 4px;" />'
logos_html += '</div>'

logos_html += '</div>'

st.sidebar.markdown(logos_html, unsafe_allow_html=True)

# Add spacing between logos and navigation
st.sidebar.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

menu_options = [
    "🚢 The Project",
    "🧑‍🤝‍🧑 Team",
    "🔬 Methodologies",
    "📊 Data Analysis",
    "📖 References"
]

if 'selected_section' not in st.session_state:
    st.session_state.selected_section = menu_options[0]

st.sidebar.markdown("<h3 style='text-align: center;'>Navigation</h3>", unsafe_allow_html=True)
for option in menu_options:
    if st.sidebar.button(option, key=option, use_container_width=True):
        st.session_state.selected_section = option

selected_section = st.session_state.selected_section

# Add study title and authors below navigation
st.sidebar.markdown(f"""
<div style="margin-top: 2rem; padding: 0.5rem;">
    <p style="text-align: center; font-size: 0.75em; font-weight: 600; color: {UI_COLORS['dark']};
               margin: 0 0 0.5rem 0; line-height: 1.3;">
        Assessment and Intercomparison of Water Quality Retrieval Methods
    </p>
    <p style="text-align: center; font-size: 0.65em; color: {UI_COLORS['medium']};
               margin: 0; line-height: 1.4;">
        Andrès L., Choblet M., Guzmán-Morales A., Pramlall S., Román A., Suklje L.
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# MAIN CONTENT AREA - SECTION ROUTING
# =============================================================================

# -----------------------------------------------------------------------------
# THE PROJECT PAGE (Merged Home + Work Summary)
# -----------------------------------------------------------------------------
if selected_section == "🚢 The Project":
    # Get background image
    ship_bg = IMAGE_DATA.get('ship', '')
    bg_style = f"background-image: linear-gradient(rgba(18, 69, 89, 0.85), rgba(89, 131, 146, 0.85)), url('data:image/jpeg;base64,{ship_bg}'); background-size: cover; background-position: center;" if ship_bg else f"background: linear-gradient(135deg, {UI_COLORS['dark']} 0%, {UI_COLORS['medium']} 100%);"

    st.markdown(f"""
    <div class="main-header" style="{bg_style}">
        <h1 style="text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🚢 The Project</h1>
        <h3 style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">Assessment and Intercomparison of Water Quality Retrieval Methods</h3>
        <p style="font-size: 1.1em; margin-top: 1rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">
            Across In-situ, Inline, Drone, Profiling Floats, and Satellite Observations
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {CHART_COLORS[0]};">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0;">📍 Stations</h3>
            <h2 style="color: {UI_COLORS['medium']}; margin: 0.5rem 0; font-size: 2.5em;">30</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {CHART_COLORS[3]};">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0;">🌍 Regions</h3>
            <h2 style="color: {UI_COLORS['medium']}; margin: 0.5rem 0; font-size: 2.5em;">3</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {CHART_COLORS[6]};">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0;">📅 Period</h3>
            <h2 style="color: {UI_COLORS['medium']}; margin: 0.5rem 0; font-size: 2.5em;">45 days</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {CHART_COLORS[9]};">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0;">🛰️ Platforms</h3>
            <h2 style="color: {UI_COLORS['medium']}; margin: 0.5rem 0; font-size: 2.5em;">5</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Project overview with modern design
    st.markdown(f"""
    <div class="section-header">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">📖 About the Project</h2>
    </div>
    """, unsafe_allow_html=True)

    # Intro paragraph with gradient background
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {UI_COLORS['lightest']} 0%, {UI_COLORS['light']} 100%);
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border-left: 5px solid {CHART_COLORS[0]};">
        <p style="font-size: 1.1em; color: {UI_COLORS['dark']}; margin: 0; line-height: 1.8;">
            This intelligence panel presents a <strong>comprehensive assessment of water quality retrieval methods</strong>
            collected during the <strong>ESA OTC25 Expedition</strong> aboard the vessel Statsraad Lehmkuhl,
            combining multi-platform observations across three major oceanic regions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # First row: Main Objectives and Observation Platforms
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="team-card" style="border-left: 4px solid {CHART_COLORS[0]}; height: 260px; display: flex; flex-direction: column;">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0 0 1rem 0;">🎯 Main Objectives</h3>
            <ul style="color: {UI_COLORS['medium']}; line-height: 1.8; margin: 0; padding-left: 1.2rem;">
                <li><strong>Multi-platform comparison</strong>: Assessment from lab, inline sensors, BGC-Argo, drones, and satellites</li>
                <li><strong>Algorithm validation</strong>: OC4ME vs Neural Networks</li>
                <li><strong>Temporal synchronization</strong>: ±3h vs ±1 day impact analysis</li>
                <li><strong>Spatial coverage</strong>: 3 major oceanic regions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="team-card" style="border-left: 4px solid {CHART_COLORS[2]}; height: 260px; display: flex; flex-direction: column;">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0 0 1rem 0;">🔬 Observation Platforms</h3>
            <ul style="color: {UI_COLORS['medium']}; line-height: 1.6; margin: 0; padding-left: 1.2rem; font-size: 0.95em;">
                <li><strong>In-situ</strong>: CTD with fluorescence, turbidity, PAR</li>
                <li><strong>Inline</strong>: AC-S spectrophotometer, LISST-200X</li>
                <li><strong>Drones</strong>: DJI Phantom 4 Multispectral (5 bands)</li>
                <li><strong>BGC-Argo</strong>: 2 floats with hyperspectral radiometers</li>
                <li><strong>Satellite</strong>: Sentinel-3 OLCI, MODIS-Aqua, PACE</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Second row: Study Regions and Parameters Measured
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"""
        <div class="team-card" style="border-left: 4px solid {CHART_COLORS[1]}; height: 300px; display: flex; flex-direction: column;">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0 0 1rem 0;">🌊 Study Regions</h3>
            <ul style="color: {UI_COLORS['medium']}; line-height: 1.8; margin: 0; padding-left: 1.2rem;">
                <li><strong>Norwegian Sea</strong><br/>Stations 1-11 (Apr 24 - May 3, 2025)</li>
                <li><strong>North Atlantic</strong><br/>Stations 12-19 (May 10-20, 2025)</li>
                <li><strong>Mediterranean Sea</strong><br/>Stations 20-30 (May 22 - Jun 2, 2025)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="team-card" style="border-left: 4px solid {CHART_COLORS[3]}; height: 300px; display: flex; flex-direction: column;">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0 0 1rem 0;">📊 Parameters Measured</h3>
            <ul style="color: {UI_COLORS['medium']}; line-height: 1.6; margin: 0; padding-left: 1.2rem; font-size: 0.95em;">
                <li><strong>Chlorophyll-a (Chl-a)</strong>: HPLC, fluorometry, optical</li>
                <li><strong>SPM</strong>: Gravimetric analysis</li>
                <li><strong>IOPs</strong>: Inherent Optical Properties</li>
                <li><strong>Rrs</strong>: Remote sensing reflectance</li>
                <li><strong>POC</strong>: Particulate Organic Carbon <em>(in progress)</em></li>
                <li><strong>CDOM</strong>: Colored Dissolved OM <em>(in progress)</em></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # =========================================================================
    # PROJECT STATIONS - Interactive Map
    # =========================================================================
    st.markdown(f"""
    <div class="section-header" style="margin-top: 3rem;">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">🗺️ Project Stations</h2>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns: map on left, station info on right
    col_map, col_info = st.columns([1.2, 1])

    with col_map:
        # Display the map
        if IMAGE_DATA.get('station_map'):
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <img src="data:image/png;base64,{IMAGE_DATA['station_map']}"
                     style="width: 100%; border-radius: 4px;"
                     alt="Station Map"/>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Station map not available")

    with col_info:
        # Station selector
        station_options = ["Select a station..."] + [f"Station {k}" for k in sorted(STATION_DATA.keys(), key=lambda x: (int(x) if x.isdigit() else float('inf'), x))]

        selected_station = st.selectbox(
            "Choose a station to view details:",
            options=station_options,
            key="station_selector"
        )

        if selected_station != "Select a station...":
            # Extract station ID from selection
            station_id = selected_station.replace("Station ", "")

            if station_id in STATION_DATA:
                station = STATION_DATA[station_id]

                # Build measurements list HTML (more compact)
                measurements_html = ""
                for measurement in station['measurements']:
                    measurements_html += f"<li style='margin: 0.15rem 0; font-size: 0.9em;'>{measurement}</li>"

                # Display station information with max height to match map
                st.markdown(f"""
                <div class="team-card" style="border-left: 4px solid {CHART_COLORS[0]}; max-height: 500px; overflow-y: auto;">
                    <h3 style="color: {UI_COLORS['dark']}; margin: 0 0 0.8rem 0; font-size: 1.2em;">{station['name']}</h3>
                    <p style="color: {UI_COLORS['medium']}; margin: 0.3rem 0; font-size: 0.9em;">
                        <strong>📅</strong> {station['date']} &nbsp;|&nbsp; <strong>📍</strong> {station['location']}
                    </p>
                    <p style="color: {UI_COLORS['medium']}; margin: 0.3rem 0; font-size: 0.9em;">
                        <strong>🌐</strong> {station['lat']}°N, {station['lon']}°E
                    </p>
                    <p style="color: {UI_COLORS['medium']}; margin: 0.8rem 0 0.3rem 0; font-size: 0.95em;">
                        <strong>🔬 Measurements:</strong>
                    </p>
                    <ul style="color: {UI_COLORS['medium']}; margin: 0; padding-left: 1.3rem; line-height: 1.5;">
                        {measurements_html}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    # =========================================================================
    # HELP US TO IMPROVE - Feedback Section
    # =========================================================================

    # Initialize session state for comments
    if 'feedback_comments' not in st.session_state:
        st.session_state.feedback_comments = []

    st.markdown(f"""
    <div class="section-header" style="margin-top: 3rem;">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">💬 Help us to improve</h2>
    </div>
    """, unsafe_allow_html=True)

    # Feedback form
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {UI_COLORS['lightest']} 0%, {UI_COLORS['light']} 100%);
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: {UI_COLORS['dark']}; margin: 0 0 1rem 0;">📝 Submit Your Feedback</h3>
        <p style="color: {UI_COLORS['medium']}; margin: 0;">
            We appreciate your input to make this intelligence panel better. Please fill out the form below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            topic = st.selectbox(
                "Topic *",
                ["General Feedback", "Data Visualization", "User Interface", "Content Accuracy", "Feature Request", "Bug Report", "Other"],
                help="Select the topic that best describes your feedback"
            )

            full_name = st.text_input(
                "Full Name *",
                placeholder="Enter your full name",
                help="Your name will be displayed with your comment"
            )

        with col2:
            institution = st.text_input(
                "Institution",
                placeholder="Your institution or organization (optional)",
                help="Optional: Add your affiliation"
            )

        message = st.text_area(
            "Message *",
            placeholder="Share your thoughts, suggestions, or feedback here...",
            height=150,
            help="Please provide detailed feedback"
        )

        submitted = st.form_submit_button("Submit Feedback", use_container_width=True)

        if submitted:
            if not full_name or not message:
                st.error("Please fill in all required fields (marked with *)")
            else:
                # Add feedback to session state
                feedback = {
                    "topic": topic,
                    "full_name": full_name,
                    "institution": institution if institution else "N/A",
                    "message": message,
                    "timestamp": __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.feedback_comments.append(feedback)
                st.success("Thank you for your feedback! Your comment has been submitted successfully.")

    # Display existing comments
    st.markdown(f"""
    <div class="section-header" style="margin-top: 3rem;">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">💭 Community Feedback</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.feedback_comments:
        st.markdown(f"<p style='color: {UI_COLORS['medium']};'>Total comments: <strong>{len(st.session_state.feedback_comments)}</strong></p>", unsafe_allow_html=True)

        for i, comment in enumerate(reversed(st.session_state.feedback_comments)):
            # Different colors for different topics
            topic_colors = {
                "General Feedback": CHART_COLORS[0],
                "Data Visualization": CHART_COLORS[1],
                "User Interface": CHART_COLORS[2],
                "Content Accuracy": CHART_COLORS[3],
                "Feature Request": CHART_COLORS[4],
                "Bug Report": "#FF6B35",
                "Other": CHART_COLORS[5]
            }

            color = topic_colors.get(comment['topic'], CHART_COLORS[0])

            st.markdown(f"""
            <div class="team-card" style="border-left: 4px solid {color}; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <div>
                        <h4 style="color: {UI_COLORS['dark']}; margin: 0; font-size: 1.1em;">{comment['full_name']}</h4>
                        <p style="color: {UI_COLORS['medium']}; margin: 0.2rem 0; font-size: 0.85em;">
                            {comment['institution']} • {comment['timestamp']}
                        </p>
                    </div>
                    <span style="background: {color}; color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.8em; font-weight: bold;">
                        {comment['topic']}
                    </span>
                </div>
                <p style="color: {UI_COLORS['dark']}; margin: 1rem 0 0 0; line-height: 1.6;">
                    {comment['message']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No feedback yet. Be the first to share your thoughts!")

# -----------------------------------------------------------------------------
# WORK SUMMARY (REMOVED - merged into The Project)
# -----------------------------------------------------------------------------
elif selected_section == "📊 Work Summary (OLD)":
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 Work Summary</h1>
        <p>Key findings and conclusions from the ESA OTC25 expedition</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-header">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">🔍 Key Findings</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="team-card">
            <h3 style="color: {UI_COLORS['dark']};">✅ In-Situ Methods</h3>
            <ul style="text-align: left; line-height: 1.8;">
                <li>CTD-fluorescence overestimates Chl-a compared to inline and fluorometric methods</li>
                <li>Correction factor: ~1.4 (inline) and ~2.1 (fluorometric)</li>
                <li>Stronger correlations in log-space (R² = 0.79-0.89)</li>
                <li>Consistent with factor of 2 reported by Roesler et al. (2017)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="team-card">
            <h3 style="color: {UI_COLORS['dark']};">🛰️ Satellite Validation</h3>
            <ul style="text-align: left; line-height: 1.8;">
                <li>±3h window: R² > 0.85, MdAPD < 17%</li>
                <li>±1 day window: R² ~ 0.64, MdAPD up to 36.78%</li>
                <li>OC-CCI best overall performance (slope=0.601, R²=0.840)</li>
                <li>Systematic underestimation at high concentrations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="team-card">
            <h3 style="color: {UI_COLORS['dark']};">🤖 Hyperspectral BGC-Argo</h3>
            <ul style="text-align: left; line-height: 1.8;">
                <li>Excellent correlation with PACE/OCI (R²=0.95, slope=0.96)</li>
                <li>Average error of ~4% with satellite</li>
                <li>Potential as FRM validation platforms</li>
                <li>Better performance in Lofoten Basin vs Mediterranean</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="team-card">
            <h3 style="color: {UI_COLORS['dark']};">🚁 Drone Challenges</h3>
            <ul style="text-align: left; line-height: 1.8;">
                <li>Low current performance (R²=0.43-0.49, MdAPD>400%)</li>
                <li>Issues: sun glint correction, calibration, band alignment</li>
                <li>Requires significant methodological refinement</li>
                <li>Promising potential after technical improvements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-header">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">💡 Key Conclusions</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🎯 Implications for Oceanographic Monitoring

    1. **Multi-Platform Integration**
       - No single solution exists for all observational needs
       - Synergistic combination of platforms is essential
       - Each method provides specific advantages in spatial and temporal scale

    2. **BGC-Argo as Validation Infrastructure**
       - Transformative capacity to expand global validation network
       - ~20 hyperspectral floats provide measurements every 10 days
       - Complement limited fixed mooring infrastructure (MOBY, AMT)
       - Especially valuable in underrepresented high-latitude regions

    3. **Importance of Temporal Synchronization**
       - ±3 hour windows capture true algorithmic performance
       - 24-hour windows reflect natural oceanographic variability
       - Strict coordination critical for robust validations

    4. **Refinement Needs**
       - Drones require rigorous atmospheric correction protocols
       - Complete HPLC analysis for definitive reference standards
       - Extend temporal analysis beyond 45-day campaign
       - Evaluate additional measured parameters (POC, CDOM, SPM)

    ### 🔬 OTC25 Distinctive Features

    This study represents the **first simultaneous deployment of**:
    - Hyperspectral BGC-Argo floats
    - Multispectral drones
    - Inline optical systems
    - Multi-sensor satellite matchups

    In a **coordinated validation effort** in underrepresented high-latitude environments,
    providing unprecedented opportunities for cross-platform uncertainty quantification.
    """)

# -----------------------------------------------------------------------------
# TEAM
# -----------------------------------------------------------------------------
elif selected_section == "🧑‍🤝‍🧑 Team":
    # Get background image
    team_bg = IMAGE_DATA.get('team', '')
    bg_style = f"background-image: linear-gradient(rgba(18, 69, 89, 0.85), rgba(89, 131, 146, 0.85)), url('data:image/jpeg;base64,{team_bg}'); background-size: cover; background-position: center;" if team_bg else f"background: linear-gradient(135deg, {UI_COLORS['dark']} 0%, {UI_COLORS['medium']} 100%);"

    st.markdown(f"""
    <div class="main-header" style="{bg_style}">
        <h1 style="text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🧑‍🤝‍🧑 Research Team</h1>
        <p style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">ESA OTC25 project participants</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-header">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">🔬 Team members</h2>
    </div>
    """, unsafe_allow_html=True)

    # Team members data structure
    team_members = [
        {
            "name": "Lou Andrès",
            "institution": "ACRI-ST & Laboratoire d'Océanographie de Villefranche (LOV)",
            "location": "Villefranche-sur-Mer, France",
            "email": "lou.andres@imev-mer.fr",
            "expertise": "Ocean optics, BGC-Argo floats, hyperspectral radiometry",
            "contributions": "BGC-Argo float deployment and data processing, Rrs derivation",
            "color": CHART_COLORS[0],
            "linkedin": "https://www.linkedin.com/in/lou-andr%C3%A8s-913ba4203/",
            "orcid": "https://orcid.org/0009-0006-4494-6350"
        },
        {
            "name": "Mathurin Choblet",
            "institution": "University of Liège",
            "location": "Liège, Belgium",
            "email": "mchoblet@uliege.be",
            "expertise": "Remote sensing, ocean color algorithms, data analysis",
            "contributions": "Satellite data processing, algorithm validation, statistical analysis",
            "color": CHART_COLORS[2],
            "linkedin": "https://www.linkedin.com/in/mathurin-choblet-93b24a258/",
            "orcid": "https://orcid.org/0000-0002-0416-7110"
        },
        {
            "name": "Alba Guzmán-Morales",
            "institution": "Environmental Mapping Consultants LLC",
            "location": "Aguadilla, Puerto Rico",
            "email": "guzmanmorales.al@gmail.com",
            "expertise": "Coastal oceanography, water quality monitoring, geospatial analysis",
            "contributions": "Remote sensing expert, data quality control",
            "color": CHART_COLORS[4],
            "linkedin": "https://www.linkedin.com/in/alba-gm/",
            "orcid": "https://orcid.org/0000-0003-1349-6554"
        },
        {
            "name": "Sejal Pramlall",
            "institution": "Marine Optics Laboratory, University of Bergen (UiB)",
            "location": "Bergen, Norway",
            "email": "Sejal.Pramlall@uib.no",
            "expertise": "Marine optics, bio-optical modeling, inherent optical properties",
            "contributions": "Inline optical system setup, IOP processing and analysis",
            "color": CHART_COLORS[6],
            "linkedin": "https://www.linkedin.com/in/sejal-pramlall-442313133/",
            "orcid": "https://orcid.org/0000-0003-1786-9178"
        },
        {
            "name": "Alejandro Román",
            "institution": "Institute of Marine Sciences of Andalusia (ICMAN-CSIC)",
            "location": "Puerto Real, Spain",
            "email": "a.roman@csic.es",
            "expertise": "Ocean color remote sensing, satellite validation, data visualization",
            "contributions": "Drone operations, data integration",
            "color": CHART_COLORS[8],
            "linkedin": "https://www.linkedin.com/in/alejandro-rom%C3%A1n-v%C3%A1zquez/",
            "orcid": "https://orcid.org/0000-0002-8868-9302"
        },
        {
            "name": "Luz Suklje",
            "institution": "Centro Austral de Investigaciones Científicas (CADIC-CONICET)",
            "location": "Ushuaia, Argentina",
            "email": "luzsuklje@hotmail.com",
            "expertise": "Antarctic oceanography, biogeochemical cycles, climate variability",
            "contributions": "Field sampling, laboratory analysis, data interpretation",
            "color": CHART_COLORS[9],
            "linkedin": "https://www.linkedin.com/in/luz-suklje/",
            "orcid": "https://orcid.org/0009-0004-9380-3669"
        }
    ]

    # Display team members in rows of 2
    for i in range(0, len(team_members), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(team_members):
                member = team_members[i + j]
                with col:
                    # Get the photo key for this team member
                    photo_key = member['name'].split()[0].lower() + '_photo'
                    photo_html = ''
                    if IMAGE_DATA.get(photo_key):
                        photo_html = f'<img src="data:image/jpeg;base64,{IMAGE_DATA[photo_key]}" style="width: 160px; height: 160px; border-radius: 50%; object-fit: cover; display: block; margin: 0 auto;" />'
                    else:
                        # Fallback to gradient if photo not found
                        photo_html = f'''<div style="width: 160px; height: 160px; background: linear-gradient(135deg, {member['color']} 0%, {UI_COLORS['medium']} 100%);
                                        border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center;
                                        font-size: 3em; color: white; font-weight: bold;">
                                {member['name'][0]}
                            </div>'''

                    # Build social links HTML
                    social_links = ""
                    if member.get('linkedin') or member.get('orcid'):
                        social_links = '<p style="text-align: center; margin: 0.5rem 0;">'
                        if member.get('linkedin'):
                            social_links += f'<a href="{member["linkedin"]}" target="_blank" style="text-decoration: none; margin: 0 0.3rem;" title="LinkedIn"><img src="data:image/png;base64,{IMAGE_DATA["linkedin_logo"]}" style="width: 18px; height: 18px; vertical-align: middle;"/></a>'
                        if member.get('orcid'):
                            social_links += f'<a href="{member["orcid"]}" target="_blank" style="text-decoration: none; margin: 0 0.3rem;" title="ORCID"><img src="data:image/png;base64,{IMAGE_DATA["orcid_logo"]}" style="width: 18px; height: 18px; vertical-align: middle;"/></a>'
                        social_links += '</p>'

                    st.markdown(f"""
                    <div class="team-card" style="border-left: 4px solid {member['color']}; min-height: 350px;">
                        <div style="text-align: center; margin-bottom: 1rem;">
                            {photo_html}
                        </div>
                        <h3 style="color: {UI_COLORS['dark']}; text-align: center; margin: 0.5rem 0;">{member['name']}</h3>
                        <p style="color: {UI_COLORS['medium']}; text-align: center; font-size: 0.9em; margin: 0.5rem 0;">
                            <strong>{member['institution']}</strong><br>
                            {member['location']}
                        </p>
                        <p style="color: {UI_COLORS['dark']}; text-align: center; font-size: 0.85em; margin: 0.5rem 0;">
                            📧 {member['email']}
                        </p>
                        {social_links}
                        <hr style="border: none; border-top: 1px solid {UI_COLORS['light']}; margin: 1rem 0;">
                        <p style="color: {UI_COLORS['dark']}; font-size: 0.9em; margin: 0.5rem 0;">
                            <strong>Expertise:</strong> {member['expertise']}
                        </p>
                        <p style="color: {UI_COLORS['dark']}; font-size: 0.9em; margin: 0.5rem 0;">
                            <strong>Contributions:</strong> {member['contributions']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# METHODOLOGIES
# -----------------------------------------------------------------------------
elif selected_section == "🔬 Methodologies":
    # Get background image
    methodology_bg = IMAGE_DATA.get('methodology', '')
    bg_style = f"background-image: linear-gradient(rgba(18, 69, 89, 0.85), rgba(89, 131, 146, 0.85)), url('data:image/jpeg;base64,{methodology_bg}'); background-size: cover; background-position: center;" if methodology_bg else f"background: linear-gradient(135deg, {UI_COLORS['dark']} 0%, {UI_COLORS['medium']} 100%);"

    st.markdown(f"""
    <div class="main-header" style="{bg_style}">
        <h1 style="text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🔬 Methodologies</h1>
        <p style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">Description of measurement techniques and platforms used in the ESA OTC25 expedition</p>
    </div>
    """, unsafe_allow_html=True)

    # Add custom CSS for instrument cards
    st.markdown(f"""
    <style>
        .instrument-card {{
            background: linear-gradient(135deg, {UI_COLORS['lightest']} 0%, {UI_COLORS['white']} 100%);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 2px solid {UI_COLORS['light']};
            margin-bottom: 1rem;
            min-height: 180px;
        }}

        .instrument-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            border-color: {UI_COLORS['medium']};
        }}

        .instrument-icon {{
            font-size: 3em;
            text-align: center;
            margin-bottom: 0.5rem;
        }}

        .instrument-name {{
            color: {UI_COLORS['dark']};
            font-size: 1.1em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.3rem;
        }}

        .instrument-manufacturer {{
            color: {UI_COLORS['medium']};
            font-size: 0.9em;
            text-align: center;
            margin-bottom: 1rem;
        }}

        .category-header {{
            background: linear-gradient(135deg, {UI_COLORS['dark']} 0%, {UI_COLORS['medium']} 100%);
            padding: 0.6rem 1.5rem;
            border-radius: 10px;
            color: {UI_COLORS['white']};
            text-align: center;
            margin: 2rem 0 1.5rem 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            border-left: 4px solid {UI_COLORS['lightest']};
        }}

        .chatbot-container {{
            background: linear-gradient(135deg, {UI_COLORS['lightest']} 0%, {UI_COLORS['light']} 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-top: 3rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # =========================================================================
    # IN-SITU SAMPLING INSTRUMENTS
    # =========================================================================
    st.markdown(f"""
    <div class="category-header">
        <h2 style="margin: 0;">🌊 In-Situ Sampling</h2>
        <p style="margin-top: 0.5rem; font-size: 0.95em; opacity: 0.9;">
            Direct water measurements from CTD profilers and sensors
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: CTD, Fluorescence, Turbidity
    col1, col2, col3 = st.columns(3)

    with col1:
        # CTD Image
        ctd_img = IMAGE_DATA.get('ctdsbe', '')
        if ctd_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{ctd_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🌡️</div>
                    <div class="instrument-name">CTD SBE-19 Plus</div>
                    <div class="instrument-manufacturer">Seabird Scientific</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🌡️</div>
                <div class="instrument-name">CTD SBE-19 Plus</div>
                <div class="instrument-manufacturer">Seabird Scientific</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Temperature, Salinity, Depth (Pressure)

            **Key Specifications:**
            - Temperature accuracy: ±0.005°C
            - Conductivity accuracy: ±0.0005 S/m
            - Pressure range: 0-1000 dbar

            **Description:**
            The Seabird SBE-19 plus is a high-precision CTD sensor used for vertical profiling of water properties.
            It provides fundamental oceanographic measurements essential for water mass characterization and
            bio-optical model parameterization during the ESA OTC25 expedition.
            """)

    with col2:
        # Fluorescence Sensor Image
        fluor_img = IMAGE_DATA.get('ecoafl', '')
        if fluor_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{fluor_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🧪</div>
                    <div class="instrument-name">Fluorescence Sensor ECO-AFL/FL</div>
                    <div class="instrument-manufacturer">WET Labs</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🧪</div>
                <div class="instrument-name">Fluorescence Sensor ECO-AFL/FL</div>
                <div class="instrument-manufacturer">WET Labs</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Chlorophyll-a fluorescence

            **Key Specifications:**
            - Excitation wavelengths: 470nm and 435nm
            - Emission: ~685nm (Chl-a)
            - Same sensor used in BGC-Argo floats

            **Description:**
            The WET Labs ECO-AFL/FL measures in-vivo chlorophyll-a fluorescence. Identical to sensors deployed
            on BGC-Argo floats, it provides real-time phytoplankton biomass estimates. Post-processing includes
            NPQ correction and validation against laboratory Chl-a measurements.
            """)

    with col3:
        # Turbidity Sensor Image
        turbidity_img = IMAGE_DATA.get('turbidityeco', '')
        if turbidity_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{turbidity_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🌫️</div>
                    <div class="instrument-name">Turbidity Sensor ECO</div>
                    <div class="instrument-manufacturer">WET Labs</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🌫️</div>
                <div class="instrument-name">Turbidity Sensor ECO</div>
                <div class="instrument-manufacturer">WET Labs</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Optical backscatter (turbidity proxy)

            **Key Specifications:**
            - Wavelength: 700nm (red)
            - Scattering angle: 140-150°
            - Particulate matter detection

            **Description:**
            The WET Labs ECO turbidity sensor measures optical backscattering at red wavelengths as a proxy
            for suspended particulate matter (SPM). This data complements gravimetric SPM measurements and
            helps characterize water clarity and particle dynamics.
            """)

    # Row 2: PAR, Oxygen, AC-S
    col1, col2, col3 = st.columns(3)

    with col1:
        # PAR Sensor Image
        par_img = IMAGE_DATA.get('parsensor', '')
        if par_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{par_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🔆</div>
                    <div class="instrument-name">PAR Sensor</div>
                    <div class="instrument-manufacturer">Satlantic</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🔆</div>
                <div class="instrument-name">PAR Sensor</div>
                <div class="instrument-manufacturer">Satlantic</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Photosynthetically Active Radiation (PAR)

            **Key Specifications:**
            - Spectral range: 400-700 nm
            - Quantum sensor type
            - Underwater light availability

            **Description:**
            The Satlantic PAR sensor measures the photosynthetically active radiation available for phytoplankton
            growth. This data is crucial for understanding primary production and light penetration in the water
            column, supporting bio-optical modeling efforts.
            """)

    with col2:
        # Oxygen Sensor Image
        oxygen_img = IMAGE_DATA.get('oxygenSBE', '')
        if oxygen_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{oxygen_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🫧</div>
                    <div class="instrument-name">Oxygen Sensor SBE 43</div>
                    <div class="instrument-manufacturer">Seabird Scientific</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🫧</div>
                <div class="instrument-name">Oxygen Sensor SBE 43</div>
                <div class="instrument-manufacturer">Seabird Scientific</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Dissolved oxygen concentration

            **Key Specifications:**
            - Measurement range: 0-15 mg/L
            - Accuracy: ±2% of saturation
            - Clark-type polarographic sensor

            **Description:**
            The SBE 43 dissolved oxygen sensor measures O2 concentration in the water column. This parameter
            is essential for understanding biogeochemical processes, respiration, and primary production dynamics
            in the studied oceanic regions.
            """)

    with col3:
        # AC-S Spectrophotometer (Inline Optical) - actual image
        inline_img = IMAGE_DATA.get('inline', '')
        if inline_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{inline_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🔬</div>
                    <div class="instrument-name">AC-S Spectrophotometer</div>
                    <div class="instrument-manufacturer">WET Labs</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🔬</div>
                <div class="instrument-name">AC-S Spectrophotometer</div>
                <div class="instrument-manufacturer">WET Labs</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measures:** Spectral absorption and attenuation coefficients (IOPs)

            **Wavelength Range:** 400-730 nm (>80 wavelengths)

            **Description:**
            Flow-through spectrophotometer measuring inherent optical properties continuously.
            Alternates between filtered and unfiltered seawater. Derives Chl-a via line-height
            method at 676 nm.

            **Type:** Inline optical system
            """)

    # =========================================================================
    # REMOTE SENSING - SATELLITE
    # =========================================================================
    st.markdown(f"""
    <div class="category-header">
        <h2 style="margin: 0;">🛰️ Remote Sensing - Satellite</h2>
        <p style="margin-top: 0.5rem; font-size: 0.95em; opacity: 0.9;">
            Spaceborne ocean color sensors for large-scale monitoring
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # Sentinel-3 Image
        sentinel_img = IMAGE_DATA.get('sentinel3', '')
        if sentinel_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{sentinel_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🛰️</div>
                    <div class="instrument-name">Sentinel-3 OLCI</div>
                    <div class="instrument-manufacturer">ESA / EUMETSAT</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🛰️</div>
                <div class="instrument-name">Sentinel-3 OLCI</div>
                <div class="instrument-manufacturer">ESA / EUMETSAT</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Ocean color multispectral imaging

            **Key Specifications:**
            - Spectral bands: 21 bands (400-1020nm)
            - Spatial resolution: 300m (Full Resolution)
            - Swath width: 1270 km
            - Revisit time: <2 days (A+B constellation)

            **Products:** Chl-a, TSM, PAR, Kd490, Rrs, CDOM

            **Algorithms:** OC4ME (empirical), Neural Network (NN)

            **Description:**
            Sentinel-3 OLCI is the primary satellite sensor for ocean color validation in this study. With excellent
            spectral and spatial resolution, it provides high-quality Chl-a retrievals. Used with ±3h and ±1 day
            matchup windows for algorithm performance assessment.
            """)

    with col2:
        # MODIS Image
        modis_img = IMAGE_DATA.get('modis', '')
        if modis_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{modis_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🌊</div>
                    <div class="instrument-name">MODIS-Aqua</div>
                    <div class="instrument-manufacturer">NASA</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🌊</div>
                <div class="instrument-name">MODIS-Aqua</div>
                <div class="instrument-manufacturer">NASA</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Moderate Resolution Imaging Spectroradiometer

            **Key Specifications:**
            - Spectral bands: 36 bands (405-14385nm)
            - Ocean color bands: 8 bands (412-869nm)
            - Spatial resolution: 1km (ocean color)
            - L3 product resolution: 4km

            **Products:** Chl-a (OCI algorithm), Kd490, POC

            **Description:**
            MODIS-Aqua has provided continuous ocean color data since 2002, making it one of the longest-running
            ocean color missions. Level-3 monthly composites at 4km resolution were used for climatological
            comparisons and regional Chl-a algorithm validation.
            """)

    with col3:
        # PACE Image
        pace_img = IMAGE_DATA.get('pace', '')
        if pace_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{pace_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🎨</div>
                    <div class="instrument-name">PACE OCI</div>
                    <div class="instrument-manufacturer">NASA</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🎨</div>
                <div class="instrument-name">PACE OCI</div>
                <div class="instrument-manufacturer">NASA</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** Hyperspectral ocean color imaging

            **Key Specifications:**
            - Spectral resolution: 5nm (hyperspectral)
            - Spectral range: UV to NIR (340-890nm)
            - Spatial resolution: 1km
            - Launch: February 2024

            **Products:** Chl-a, POC, PIC, phytoplankton community composition

            **Description:**
            PACE OCI represents the next generation of ocean color satellites with unprecedented hyperspectral
            capabilities. Launched in 2024, it provides detailed spectral information for advanced phytoplankton
            functional type discrimination. Showed excellent agreement (R²=0.95) with BGC-Argo floats.
            """)

    # =========================================================================
    # OTHER OCEAN COLOUR TOOLS
    # =========================================================================
    st.markdown(f"""
    <div class="category-header">
        <h2 style="margin: 0;">🔬 Other Ocean Colour Tools</h2>
        <p style="margin-top: 0.5rem; font-size: 0.95em; opacity: 0.9;">
            Autonomous profiling floats and unmanned aerial vehicles
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # BGC-Argo Float - actual image
        argo_img = IMAGE_DATA.get('argo', '')
        if argo_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{argo_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🤖</div>
                    <div class="instrument-name">BGC-Argo Float</div>
                    <div class="instrument-manufacturer">PROVOR Jumbo with TriOS RAMSES</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🤖</div>
                <div class="instrument-name">BGC-Argo Float</div>
                <div class="instrument-manufacturer">PROVOR Jumbo with TriOS RAMSES</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measures:** Hyperspectral radiometry (Ed, Lu), CTD, Chl-a fluorescence, backscatter, O₂

            **Wavelength Range:** Hyperspectral (320-950 nm)

            **Description:**
            Autonomous profiling float with hyperspectral radiometers. Measures from 1000m depth
            to surface every 5-10 days. Derives remote sensing reflectance (Rrs) with R²=0.95 vs PACE/OCI.

            **Deployments:** WMO 5906995 (Lofoten), WMO 7901133 (Gibraltar)
            """)

    with col2:
        # Phantom 4 Image
        phantom_img = IMAGE_DATA.get('phantom4', '')
        if phantom_img:
            st.markdown(f"""
            <div class="instrument-card" style="padding: 0; overflow: hidden;">
                <img src="data:image/jpeg;base64,{phantom_img}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div style="padding: 1rem;">
                    <div class="instrument-icon" style="font-size: 2em; margin-bottom: 0.3rem;">🚁</div>
                    <div class="instrument-name">DJI Phantom 4 Multispectral</div>
                    <div class="instrument-manufacturer">DJI</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="instrument-card">
                <div class="instrument-icon">🚁</div>
                <div class="instrument-name">DJI Phantom 4 Multispectral</div>
                <div class="instrument-manufacturer">DJI</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Show details"):
            st.markdown("""
            **Measurements:** 5-band multispectral imaging

            **Key Specifications:**
            - Weight: 1487g
            - Flight duration: 27 minutes
            - Integrated Downwelling Light Sensor (DLS) for irradiance normalization
            - Spectral bands:
              - 450nm (Blue) - 16nm bandwidth
              - 560nm (Green) - 16nm bandwidth
              - 650nm (Red) - 16nm bandwidth
              - 730nm (Red Edge) - 16nm bandwidth
              - 840nm (NIR) - 26nm bandwidth

            **Operations:** 22 flights during ESA OTC25 at 10-120m altitude

            **Description:**
            The DJI P4M provides multispectral ocean color imagery at very high spatial resolution (cm-scale).
            Deployed during CTD operations for simultaneous validation. The integrated DLS measures incoming
            sunlight for accurate Rrs calculation. Currently faces challenges with sun glint correction and
            radiometric calibration (R²=0.43-0.49), but holds promise after methodological refinement.
            """)

    # =========================================================================
    # AI CHATBOT FOR METHODOLOGIES - MOVED TO TOP
    # =========================================================================
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {UI_COLORS['lightest']} 0%, {UI_COLORS['light']} 100%);
                padding: 1.5rem; border-radius: 12px; margin: 2rem 0 2rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h2 style="color: {UI_COLORS['dark']}; text-align: center; margin: 0 0 0.5rem 0;">
            💬 Ask Questions About Methodologies
        </h2>
        <p style="color: {UI_COLORS['medium']}; text-align: center; margin: 0; font-size: 0.9em;">
            Get instant answers about instruments, techniques, and data processing methods
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Create knowledge base from methodology content
    methodology_knowledge = {
        "ctd": "The CTD SBE-19 plus by Seabird Scientific measures temperature, salinity, and depth with high precision (±0.005°C for temperature). It's used for vertical profiling during the expedition.",
        "fluorescence": "The WET Labs ECO-AFL/FL fluorescence sensor measures chlorophyll-a at 470nm and 435nm excitation. It's identical to sensors on BGC-Argo floats and requires NPQ correction.",
        "turbidity": "The WET Labs ECO turbidity sensor measures optical backscatter at 700nm as a proxy for suspended particulate matter.",
        "par": "The Satlantic PAR sensor measures photosynthetically active radiation from 400-700nm, essential for understanding light availability for phytoplankton.",
        "oxygen": "The SBE 43 dissolved oxygen sensor measures O2 concentration (0-15 mg/L) using Clark-type polarographic method.",
        "sentinel": "Sentinel-3 OLCI has 21 spectral bands with 300m resolution. It measures Chl-a, TSM, and Rrs using OC4ME and Neural Network algorithms. Best performance with ±3h matchup windows (R²>0.85).",
        "modis": "MODIS-Aqua has 36 bands with 4km L3 resolution. It provides long-term ocean color data since 2002, used for Chl-a climatology.",
        "pace": "PACE OCI is hyperspectral with 5nm resolution covering UV-NIR (340-890nm). Launched in 2024, it showed excellent agreement with BGC-Argo (R²=0.95, slope=0.96).",
        "drone": "DJI Phantom 4 Multispectral has 5 bands (450, 560, 650, 730, 840nm) with 1487g weight and 27min flight time. Currently faces challenges (R²=0.43-0.49) due to sun glint and calibration issues.",
        "dls": "The DLS (Downwelling Light Sensor) measures incoming sunlight in the same 5 bands as the P4M camera, essential for converting radiance to Rrs.",
        "argo": "BGC-Argo floats (WMO 5906995, 7901133) have hyperspectral radiometers (TriOS RAMSES) measuring Ed and Lu. They profile 0-1000m every 5-10 days with R²=0.95 agreement with PACE.",
        "inline": "The inline system uses AC-S spectrophotometer (80+ wavelengths, 400-730nm) and LISST-200X (particle size). Chl-a derived using line height at 676nm.",
        "chla": "Chlorophyll-a measured via: (1) CTD fluorescence (WET Labs ECO), (2) Inline spectrophotometry (676nm line height), (3) Laboratory fluorometry (Turner Trilogy), (4) HPLC (SAPIGH CNRS). CTD overestimates by factors of 1.4-2.1.",
        "spm": "Suspended Particulate Matter measured gravimetrically using pre-combusted Whatman GF/F filters, dried 24h at 60°C following Strickland & Parsons (1968).",
        "validation": "Satellite validation used ±3h windows (n=7, R²>0.85) for algorithmic performance and ±1 day windows (n=18-19, R²~0.64) showing natural variability. OC-CCI performed best overall.",
        "algorithms": "Main algorithms: OC4ME (empirical 4-band ratio), Neural Networks, Color Index (oligotrophic), OC-CCI (multi-algorithm). All show systematic underestimation at high Chl-a.",
    }

    # Chat interface
    user_question = st.chat_input("Ask a question about the methodologies...")

    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        # Simple RAG: search for relevant keywords
        question_lower = user_question.lower()
        relevant_info = []

        for key, value in methodology_knowledge.items():
            if key in question_lower or any(word in question_lower for word in key.split()):
                relevant_info.append(value)

        # Generate response
        if relevant_info:
            response = "Based on the methodology documentation:\n\n" + "\n\n".join(relevant_info)
        else:
            # Try to match general topics
            if any(word in question_lower for word in ["satellite", "sentinel", "modis", "pace", "space"]):
                response = methodology_knowledge["sentinel"] + "\n\n" + methodology_knowledge["modis"] + "\n\n" + methodology_knowledge["pace"]
            elif any(word in question_lower for word in ["drone", "uav", "aerial", "phantom"]):
                response = methodology_knowledge["drone"] + "\n\n" + methodology_knowledge["dls"]
            elif any(word in question_lower for word in ["argo", "float", "autonomous"]):
                response = methodology_knowledge["argo"]
            elif any(word in question_lower for word in ["ctd", "in-situ", "profile"]):
                response = methodology_knowledge["ctd"] + "\n\n" + methodology_knowledge["fluorescence"]
            elif any(word in question_lower for word in ["chlorophyll", "chl-a", "phytoplankton"]):
                response = methodology_knowledge["chla"]
            else:
                response = "I don't have specific information about that in the methodology section. Please try asking about: CTD sensors, fluorescence, turbidity, PAR, oxygen, Sentinel-3, MODIS, PACE, drones, BGC-Argo floats, inline systems, Chl-a measurements, or validation protocols."

        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# -----------------------------------------------------------------------------
# DATA ANALYSIS (formerly Correlation Analysis)
# -----------------------------------------------------------------------------
elif selected_section == "📊 Data Analysis":
    # Get background image
    data_bg = IMAGE_DATA.get('data', '')
    bg_style = f"background-image: linear-gradient(rgba(18, 69, 89, 0.85), rgba(89, 131, 146, 0.85)), url('data:image/jpeg;base64,{data_bg}'); background-size: cover; background-position: center;" if data_bg else f"background: linear-gradient(135deg, {UI_COLORS['dark']} 0%, {UI_COLORS['medium']} 100%);"

    st.markdown(f"""
    <div class="main-header" style="{bg_style}">
        <h1 style="text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📊 Data Analysis</h1>
        <p style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">Interactive exploration of relationships between variables</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-header">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">📈 Correlation Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    try:
        df = pd.read_excel('data/Panel.xlsx')

        # Get numeric columns for analysis and filter them
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Remove variables with STD, Latitude, Longitude, and those starting with n_ or std_
        # Keep ALEX columns but rename them to UAV
        filtered_cols = []
        col_mapping = {}

        for col in numeric_cols:
            # Skip columns with STD, Latitude, Longitude, or starting with n_, std_, or Std_
            if ('STD' in col or
                col in ['Latitude', 'Longitude'] or
                col.startswith('n_') or
                col.startswith('std_') or
                col.startswith('Std_')):
                continue

            # Keep column and add to mapping (rename ALEX to UAV)
            if 'ALEX' in col:
                new_col = col.replace('ALEX', 'UAV')
                col_mapping[col] = new_col
                filtered_cols.append(new_col)
            else:
                filtered_cols.append(col)

        # Actually rename the columns in the dataframe for display
        df_display = df.rename(columns=col_mapping)

        # Update numeric_cols to use renamed columns
        numeric_cols = filtered_cols

        if len(numeric_cols) > 1:
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.markdown(f"""
                <div class="team-card">
                    <h3 style="color: {UI_COLORS['dark']};">Analysis Configuration</h3>
                </div>
                """, unsafe_allow_html=True)

                var_x = st.selectbox("Variable X", options=numeric_cols, index=0)
                var_y = st.selectbox("Variable Y", options=numeric_cols, index=min(1, len(numeric_cols)-1))

                plot_type = st.radio(
                    "Plot type",
                    options=['Scatter', 'Scatter + Regression', 'Hexbin', 'Contour']
                )

                log_x = st.checkbox("Logarithmic scale X")
                log_y = st.checkbox("Logarithmic scale Y")

            with col2:
                st.markdown(f"""
                <div class="team-card">
                    <h3 style="color: {UI_COLORS['dark']};">Data Filters</h3>
                </div>
                """, unsafe_allow_html=True)

                # Filter by value ranges
                if var_x in numeric_cols:
                    x_min, x_max = float(df_display[var_x].min()), float(df_display[var_x].max())
                    x_range = st.slider(
                        f"Range {var_x}",
                        min_value=x_min,
                        max_value=x_max,
                        value=(x_min, x_max)
                    )

                if var_y in numeric_cols:
                    y_min, y_max = float(df_display[var_y].min()), float(df_display[var_y].max())
                    y_range = st.slider(
                        f"Range {var_y}",
                        min_value=y_min,
                        max_value=y_max,
                        value=(y_min, y_max)
                    )

            with col3:
                st.markdown(f"""
                <div class="team-card">
                    <h3 style="color: {UI_COLORS['dark']};">Statistics</h3>
                </div>
                """, unsafe_allow_html=True)

                # Filter data
                filtered_df = df_display[
                    (df_display[var_x] >= x_range[0]) &
                    (df_display[var_x] <= x_range[1]) &
                    (df_display[var_y] >= y_range[0]) &
                    (df_display[var_y] <= y_range[1])
                ].copy()

                # Remove NaN values
                clean_data = filtered_df[[var_x, var_y]].dropna()

                if len(clean_data) > 2:
                    # Calculate correlation
                    corr, p_value = pearsonr(clean_data[var_x], clean_data[var_y])

                    st.metric("Pearson Correlation (r)", f"{corr:.3f}")
                    st.metric("R²", f"{corr**2:.3f}")
                    st.metric("p-value", f"{p_value:.4f}")
                    st.metric("N observations", len(clean_data))

                    if p_value < 0.001:
                        sig = "*** (p < 0.001)"
                    elif p_value < 0.01:
                        sig = "** (p < 0.01)"
                    elif p_value < 0.05:
                        sig = "* (p < 0.05)"
                    else:
                        sig = "ns (not significant)"

                    st.markdown(f"**Significance:** {sig}")

            # Create plot
            st.markdown("<br>", unsafe_allow_html=True)

            if len(clean_data) > 0:
                fig = go.Figure()

                # Create plot based on type
                if plot_type == 'Scatter':
                    fig.add_trace(go.Scatter(
                        x=clean_data[var_x],
                        y=clean_data[var_y],
                        mode='markers',
                        marker=dict(
                            size=8,
                            color=CHART_COLORS[9],
                            opacity=0.7
                        ),
                        name='Data'
                    ))

                elif plot_type == 'Scatter + Regression':
                    # Scatter
                    fig.add_trace(go.Scatter(
                        x=clean_data[var_x],
                        y=clean_data[var_y],
                        mode='markers',
                        marker=dict(
                            size=8,
                            color=CHART_COLORS[9],
                            opacity=0.6
                        ),
                        name='Data'
                    ))

                    # Regression line
                    z = np.polyfit(clean_data[var_x], clean_data[var_y], 1)
                    p = np.poly1d(z)
                    x_line = np.linspace(clean_data[var_x].min(), clean_data[var_x].max(), 100)
                    y_line = p(x_line)

                    fig.add_trace(go.Scatter(
                        x=x_line,
                        y=y_line,
                        mode='lines',
                        line=dict(color=CHART_COLORS[0], width=2),
                        name=f'y = {z[0]:.3f}x + {z[1]:.3f}'
                    ))

                elif plot_type == 'Hexbin':
                    fig.add_trace(go.Histogram2d(
                        x=clean_data[var_x],
                        y=clean_data[var_y],
                        colorscale='Viridis',
                        showscale=True
                    ))

                elif plot_type == 'Contour':
                    fig.add_trace(go.Histogram2dContour(
                        x=clean_data[var_x],
                        y=clean_data[var_y],
                        colorscale='Viridis',
                        showscale=True
                    ))

                # Update layout
                fig.update_layout(
                    title=f"{var_y} vs {var_x}",
                    xaxis_title=var_x,
                    yaxis_title=var_y,
                    height=600,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        type='log' if log_x else 'linear',
                        gridcolor=UI_COLORS['light']
                    ),
                    yaxis=dict(
                        type='log' if log_y else 'linear',
                        gridcolor=UI_COLORS['light']
                    )
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available to display with the selected filters.")

        else:
            st.warning("Not enough numeric columns in the data to perform correlation analysis.")

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Data file not found. Please check the data/ directory.")

    # =========================================================================
    # BGC ARGO FLOAT ANALYSIS
    # =========================================================================
    st.markdown(f"""
    <div class="section-header" style="margin-top: 3rem;">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">🌊 BGC Argo Float Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
        <h3 style="color: {UI_COLORS['dark']}; margin: 0;">🤖 Hyperspectral BGC-Argo Float Measurements</h3>
        <p style="color: {UI_COLORS['medium']}; font-size: 0.9em; margin-top: 0.3rem;">
            Validation of autonomous hyperspectral radiometry from two BGC-Argo floats equipped with TriOS RAMSES sensors
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Two hyperspectral BGC-Argo floats with TriOS RAMSES radiometers side-by-side
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 2rem 0;">
        <div style="text-align: center;">
            <img src="data:image/png;base64,{IMAGE_DATA['argo1']}"
                 style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        </div>
        <div style="text-align: center;">
            <img src="data:image/svg+xml;base64,{IMAGE_DATA['argo2']}"
                 style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # OCEAN COLOUR MAPS
    # =========================================================================
    st.markdown(f"""
    <div class="section-header">
        <h2 style="color: {UI_COLORS['dark']}; margin: 0;">🗺️ Ocean Colour Maps</h2>
    </div>
    """, unsafe_allow_html=True)

    # Load satellite matchup data
    try:
        import pandas as pd
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots

        df_panel = pd.read_excel('data/Panel.xlsx', sheet_name='1d-5x5')

        # Remove rows with all NaN values
        df_panel = df_panel.dropna(how='all')

        # =====================================================================
        # GRAPH 3: Time Series of Chlorophyll-a
        # =====================================================================
        st.markdown(f"""
        <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0;">📈 Temporal Evolution of Chlorophyll-a</h3>
            <p style="color: {UI_COLORS['medium']}; font-size: 0.9em; margin-top: 0.3rem;">
                Comparison of satellite algorithms (OC4ME and NN) with in-situ measurements throughout the campaign
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Prepare data for time series
        df_ts = df_panel[['Name', 'Date(yyyy-MM-dd)', 'CHL_OC4ME', 'CHL_NN', 'MEAN_CLA_LUZ']].copy()
        df_ts = df_ts.dropna(subset=['Date(yyyy-MM-dd)'])
        df_ts = df_ts.sort_values('Date(yyyy-MM-dd)')
        # Create station labels for X-axis
        df_ts['Station'] = df_ts['Name'].astype(str)

        fig_ts = go.Figure()

        # Add OC4ME satellite data
        fig_ts.add_trace(go.Scatter(
            x=df_ts['Station'],
            y=df_ts['CHL_OC4ME'],
            mode='lines+markers',
            name='Satellite OC4ME',
            line=dict(color=CHART_COLORS[0], width=2),
            marker=dict(size=8, symbol='circle')
        ))

        # Add NN satellite data
        fig_ts.add_trace(go.Scatter(
            x=df_ts['Station'],
            y=df_ts['CHL_NN'],
            mode='lines+markers',
            name='Satellite NN',
            line=dict(color=CHART_COLORS[2], width=2),
            marker=dict(size=8, symbol='square')
        ))

        # Add in-situ data
        fig_ts.add_trace(go.Scatter(
            x=df_ts['Station'],
            y=df_ts['MEAN_CLA_LUZ'],
            mode='markers',
            name='In-situ (HPLC)',
            marker=dict(size=12, color=CHART_COLORS[4], symbol='diamond',
                       line=dict(width=2, color='white'))
        ))

        fig_ts.update_layout(
            xaxis_title='Station',
            yaxis_title='Chlorophyll-a (mg m⁻³)',
            yaxis_type='log',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Arial', size=14),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=60, r=30, t=40, b=60),
            height=450
        )

        fig_ts.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', title_font=dict(family='Arial', size=16, color='black', weight='bold'), title_standoff=10)
        fig_ts.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', title_font=dict(family='Arial', size=16, color='black', weight='bold'), tickfont=dict(size=14))

        st.plotly_chart(fig_ts, use_container_width=True)

        # =====================================================================
        # GRAPH 4: Error Map
        # =====================================================================
        st.markdown(f"""
        <div style="margin-top: 2rem; margin-bottom: 0.5rem;">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0;">🗺️ Geographic Distribution of Satellite-In Situ Differences</h3>
            <p style="color: {UI_COLORS['medium']}; font-size: 0.9em; margin-top: 0.3rem;">
                Spatial patterns of relative errors between satellite retrievals and in-situ measurements
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Prepare data for error map
        df_map = df_panel[['Name', 'Latitude', 'Longitude', 'CHL_OC4ME', 'CHL_NN', 'MEAN_CLA_LUZ']].copy()
        df_map = df_map.dropna(subset=['Latitude', 'Longitude', 'MEAN_CLA_LUZ'])

        # Calculate relative errors (percentage)
        df_map['Error_OC4ME'] = ((df_map['CHL_OC4ME'] - df_map['MEAN_CLA_LUZ']) / df_map['MEAN_CLA_LUZ']) * 100
        df_map['Error_NN'] = ((df_map['CHL_NN'] - df_map['MEAN_CLA_LUZ']) / df_map['MEAN_CLA_LUZ']) * 100

        # Calculate absolute error for marker size
        df_map['Abs_Error_OC4ME'] = abs(df_map['Error_OC4ME'])
        df_map['Abs_Error_NN'] = abs(df_map['Error_NN'])

        # Create subplots for two maps
        fig_map = make_subplots(
            rows=1, cols=2,
            subplot_titles=('OC4ME Algorithm', 'Neural Network Algorithm'),
            specs=[[{'type': 'scattergeo'}, {'type': 'scattergeo'}]],
            horizontal_spacing=0.02
        )

        # OC4ME map
        fig_map.add_trace(
            go.Scattergeo(
                lon=df_map['Longitude'],
                lat=df_map['Latitude'],
                text=df_map['Name'],
                mode='markers',
                marker=dict(
                    size=df_map['Abs_Error_OC4ME'].fillna(0).clip(lower=5, upper=30),
                    color=df_map['Error_OC4ME'],
                    colorscale='RdBu_r',
                    cmin=-100,
                    cmax=100,
                    colorbar=dict(
                        title="Relative<br>Error (%)",
                        x=0.46,
                        len=0.8,
                        thickness=10
                    ),
                    line=dict(width=1, color='white'),
                    sizemode='diameter'
                ),
                hovertemplate='<b>Station %{text}</b><br>' +
                             'Lat: %{lat:.2f}<br>' +
                             'Lon: %{lon:.2f}<br>' +
                             'Error: %{marker.color:.1f}%<br>' +
                             '<extra></extra>'
            ),
            row=1, col=1
        )

        # NN map
        fig_map.add_trace(
            go.Scattergeo(
                lon=df_map['Longitude'],
                lat=df_map['Latitude'],
                text=df_map['Name'],
                mode='markers',
                marker=dict(
                    size=df_map['Abs_Error_NN'].fillna(0).clip(lower=5, upper=30),
                    color=df_map['Error_NN'],
                    colorscale='RdBu_r',
                    cmin=-100,
                    cmax=100,
                    showscale=False,
                    line=dict(width=1, color='white'),
                    sizemode='diameter'
                ),
                hovertemplate='<b>Station %{text}</b><br>' +
                             'Lat: %{lat:.2f}<br>' +
                             'Lon: %{lon:.2f}<br>' +
                             'Error: %{marker.color:.1f}%<br>' +
                             '<extra></extra>'
            ),
            row=1, col=2
        )

        # Update geo layout
        geo_dict = dict(
            scope='europe',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            projection_type='mercator',
            lonaxis=dict(range=[-25, 10]),
            lataxis=dict(range=[35, 72]),
            bgcolor='rgba(0,0,0,0)'
        )

        fig_map.update_geos(geo_dict, row=1, col=1)
        fig_map.update_geos(geo_dict, row=1, col=2)

        fig_map.update_layout(
            height=500,
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Arial', size=14),
            annotations=[
                dict(
                    text='OC4ME Algorithm',
                    font=dict(family='Arial', size=16, color='black', weight='bold'),
                    xref='paper', yref='paper',
                    x=0.23, y=1.0,
                    xanchor='center', yanchor='bottom',
                    showarrow=False
                ),
                dict(
                    text='Neural Network Algorithm',
                    font=dict(family='Arial', size=16, color='black', weight='bold'),
                    xref='paper', yref='paper',
                    x=0.77, y=1.0,
                    xanchor='center', yanchor='bottom',
                    showarrow=False
                )
            ]
        )

        st.plotly_chart(fig_map, use_container_width=True)

        # Add interpretation note
        st.markdown(f"""
        <div class="team-card" style="margin-top: 1rem;">
            <p style="color: {UI_COLORS['medium']}; font-size: 0.85em; margin: 0;">
                <strong>📌 Interpretation:</strong> Red markers indicate overestimation by satellite,
                blue markers indicate underestimation. Marker size is proportional to the absolute error magnitude.
                Errors are calculated as: (Satellite - In-situ) / In-situ × 100%.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # =====================================================================
        # NEW SUBSECTION: Satellite-derived OC maps
        # =====================================================================
        st.markdown(f"""
        <div style="margin-top: 2rem; margin-bottom: 0.5rem;">
            <h3 style="color: {UI_COLORS['dark']}; margin: 0;">🛰️ Satellite-derived OC maps</h3>
            <p style="color: {UI_COLORS['medium']}; font-size: 0.9em; margin-top: 0.3rem;">
                Supplementary Figure 3: Spatial distribution of satellite-derived ocean color products
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Display Supplementary Figure 3
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin: 1rem 0;">
            <img src="data:image/png;base64,{IMAGE_DATA['sup3']}"
                 style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading ocean colour data: {str(e)}")
        st.info("Ocean colour maps data file not found.")

# -----------------------------------------------------------------------------
# REFERENCES
# -----------------------------------------------------------------------------
elif selected_section == "📖 References":
    # Get background image
    references_bg = IMAGE_DATA.get('references', '')
    bg_style = f"background-image: linear-gradient(rgba(18, 69, 89, 0.85), rgba(89, 131, 146, 0.85)), url('data:image/png;base64,{references_bg}'); background-size: cover; background-position: center;" if references_bg else f"background: linear-gradient(135deg, {UI_COLORS['dark']} 0%, {UI_COLORS['medium']} 100%);"

    st.markdown(f"""
    <div class="main-header" style="{bg_style}">
        <h1 style="text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📖 References</h1>
        <p style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">Scientific bibliography of the ESA OTC25 project</p>
    </div>
    """, unsafe_allow_html=True)

    # Reference categories
    references = {
        "All References": [
            {
                "authors": "Bailey, S.W. & Werdell, P. J.",
                "year": "2006",
                "title": "A multi-sensor approach for the on-orbit validation of ocean color satellite data products",
                "journal": "Remote Sens Environ",
                "volume": "102",
                "pages": "12–23"
            },
            {
                "authors": "Baudena, A., Riom, W., Taillandier, V., Mayot, N., Mignot, A. & D'Ortenzio, F.",
                "year": "2025",
                "title": "Comparing satellite and BGC-Argo chlorophyll estimation: A phenological study",
                "journal": "Remote Sens. Environ.",
                "volume": "326",
                "pages": "114743"
            },
            {
                "authors": "Bittig, H.C. et al.",
                "year": "2019",
                "title": "A BGC-Argo Guide: Planning, Deployment, Data Handling and Usage",
                "journal": "Front. Mar. Sci.",
                "volume": "6",
                "pages": ""
            },
            {
                "authors": "Boss, E. et al.",
                "year": "2013",
                "title": "The characteristics of particulate absorption, scattering and attenuation coefficients in the surface ocean; Contribution of the Tara Oceans expedition",
                "journal": "Methods Oceanogr.",
                "volume": "7",
                "pages": "52–62"
            },
            {
                "authors": "Boss, E., Slade, W.H., Behrenfeld, M.J. & Dall'Olmo, G.",
                "year": "2001",
                "title": "Optical techniques for remote assessment of particle size, composition, and abundance in natural waters",
                "journal": "J. Remote Sens.",
                "volume": "22",
                "pages": "325–345"
            },
            {
                "authors": "Boss, E., Slade, W.H. & Hill, P.",
                "year": "2018",
                "title": "LISST processing and distribution validation for particle size and optical properties in oceanic waters",
                "journal": "Methods Oceanogr.",
                "volume": "7",
                "pages": "94–104"
            },
            {
                "authors": "Brewin, R.J.W., Dall'Olmo, G., Pardo, S., van Dongen-Vogels, V. & Boss, E.S.",
                "year": "2016",
                "title": "Underway spectrophotometry along the Atlantic Meridional Transect reveals high performance in satellite chlorophyll retrievals",
                "journal": "Remote Sens. Environ.",
                "volume": "183",
                "pages": "82–97"
            },
            {
                "authors": "Brewin, R.J.W. et al.",
                "year": "2015",
                "title": "The Ocean Colour Climate Change Initiative: III. A round-robin comparison on in-water bio-optical algorithms",
                "journal": "Remote Sens Environ",
                "volume": "162",
                "pages": "271–294"
            },
            {
                "authors": "Cetinic, I., Perry, M.J., D'Asaro, E.A., Briggs, N., Poulton, N. & Sieracki, M.E.",
                "year": "2016",
                "title": "A simple optical technique for continuous measurement of particle size distributions in natural waters",
                "journal": "Limnol. Oceanogr. Methods",
                "volume": "14",
                "pages": "303–317"
            },
            {
                "authors": "Copernicus Marine Service",
                "year": "",
                "title": "Ocean Colour Multi-sensor Global Ocean Colour Product (Level 3/4)",
                "journal": "",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "EUMETSAT",
                "year": "2022",
                "title": "Recommendations for Sentinel-3 OLCI Ocean Colour product validations in comparison with in situ measurements. Matchup Protocols: Vol. EUM/SEN3/DOC/19/1092968 (V8B)",
                "journal": "",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "García-Jiménez, J., Ruescas, A.B., Amorós-López, J. & Sauzède, R.",
                "year": "2025",
                "title": "Combining BioGeoChemical-Argo (BGC-Argo) floats and satellite observations for water column estimations of the particulate backscattering coefficient",
                "journal": "Ocean Sci.",
                "volume": "21",
                "pages": "1677–1694"
            },
            {
                "authors": "Gray, P.C. et al.",
                "year": "2022",
                "title": "Robust ocean color from drones: Viewing geometry, sky reflection removal, uncertainty analysis, and a survey of the Gulf Stream front",
                "journal": "Limnol. Oceanogr. Methods",
                "volume": "20",
                "pages": "656–673"
            },
            {
                "authors": "Hu, C. et al.",
                "year": "2019",
                "title": "Improving Satellite Global Chlorophyll a Data Products Through Algorithm Refinement and Data Recovery",
                "journal": "J Geophys Res Oceans",
                "volume": "124",
                "pages": "1524–1543"
            },
            {
                "authors": "IOCCG",
                "year": "2019",
                "title": "Uncertainties in Ocean Colour Remote Sensing. Mélin F. (ed.), IOCCG Report Series, No. 18, International Ocean Colour Coordinating Group, Dartmouth, Canada",
                "journal": "",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "Jackson, T., Calton, B. & Hockley, K.",
                "year": "2023",
                "title": "C3S Ocean Colour Version 6.0: Product User Guide and Specification. Issue 1.1. E.U. Copernicus Climate Change Service. Document ref. WP2-FDDP-2022-04_C3S2-Lot3_PUGS-of-v6.0-OceanColour-product",
                "journal": "",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "Kratzer, S. et al.",
                "year": "2022",
                "title": "International intercomparison of in situ chlorophyll-a measurements",
                "journal": "Front. Remote Sens.",
                "volume": "3",
                "pages": "866712"
            },
            {
                "authors": "Liu, Y., Cao, H., Li, H., Wang, J. & Ma, Y.",
                "year": "2018",
                "title": "Evaluation of optical estimation algorithms for particle size in natural waters",
                "journal": "Opt. Express",
                "volume": "26",
                "pages": "19395–19413"
            },
            {
                "authors": "Mabit, R., Araújo, C.A.S., Singh, R.K. & Bélanger, S.",
                "year": "2022",
                "title": "Empirical Remote Sensing Algorithms to Retrieve SPM and CDOM in Québec Coastal Waters",
                "journal": "Front. Remote Sens.",
                "volume": "3",
                "pages": ""
            },
            {
                "authors": "Mo, J. et al.",
                "year": "2024",
                "title": "Remote sensing inversion of suspended particulate matter in the estuary of the Pinglu Canal in China based on machine learning algorithms",
                "journal": "Front. Mar. Sci.",
                "volume": "11",
                "pages": ""
            },
            {
                "authors": "Mueller, J.L., Fargion, G.S. & McClain, C.R.",
                "year": "2003",
                "title": "Ocean Optics Protocols for Satellite Ocean Color Sensor Validation, Revision 4, Volume III: Radiometric Measurements and Data Analysis Protocols. NASA Technical Memorandum 2003–211621/Rev4–Vol. III, NASA Goddard Space Flight Center",
                "journal": "",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "O'Reilly, J.E. et al.",
                "year": "1998",
                "title": "Ocean color chlorophyll algorithms for SeaWiFS",
                "journal": "J Geophys Res Oceans",
                "volume": "103",
                "pages": "24937–24953"
            },
            {
                "authors": "O'Reilly, J.E. & Werdell, P.J.",
                "year": "2019",
                "title": "Chlorophyll algorithms for ocean color sensors- OC4, OC5 & OC6",
                "journal": "Remote Sens Environ",
                "volume": "229",
                "pages": "32–47"
            },
            {
                "authors": "Parsons, T.R., Maita, Y. & Lalli, C.M.",
                "year": "1984",
                "title": "A Manual of Chemical and Biological Methods for Seawater Analysis. Pergamon Press, Oxford, 173 pp.",
                "journal": "",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "Pramlall, S., Jackson, J.M., Konik, M. & Costa, M.",
                "year": "2023",
                "title": "Merged multi-sensor ocean colour chlorophyll product evaluation for the British Columbia Coast",
                "journal": "Remote Sens",
                "volume": "15",
                "pages": "687"
            },
            {
                "authors": "Seegers, B.N., Stumpf, R.P., Schaeffer, B.A., Loftin, K.A., Werdell, J.P.",
                "year": "2018",
                "title": "Performance metrics for the assessment of satellite data products: an ocean color case study",
                "journal": "Optics Express",
                "volume": "26(6)",
                "pages": "7404-7422"
            },
            {
                "authors": "Slade, W.H. et al.",
                "year": "2010",
                "title": "Underway and Moored Methods for Improving Accuracy in Measurement of Spectral Particulate Absorption and Attenuation",
                "journal": "J. Atmos. Oceanic Technol.",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "Strickland, J.D.H. & Parsons, T.R.",
                "year": "1968",
                "title": "A Practical Handbook of Seawater Analysis. 1st ed. Bulletin Fisheries Research Board of Canada, Ottawa, Canada",
                "journal": "",
                "volume": "",
                "pages": ""
            },
            {
                "authors": "Volpe, G. et al.",
                "year": "2019",
                "title": "Mediterranean ocean colour Level 3 operational multi-sensor processing",
                "journal": "Ocean Sci",
                "volume": "15",
                "pages": "127–146"
            },
            {
                "authors": "Volpe, G. et al.",
                "year": "2007",
                "title": "The colour of the Mediterranean Sea: Global versus regional bio-optical algorithms evaluation and implication for satellite chlorophyll estimates",
                "journal": "Remote Sens Environ",
                "volume": "107",
                "pages": "625–638"
            },
            {
                "authors": "Wei, J., Wang, M., Jiang, L., Yu, X., Mikelsons, K. & Shen, F.",
                "year": "2021",
                "title": "Global Estimation of Suspended Particulate Matter From Satellite Ocean Color Imagery",
                "journal": "J. Geophys. Res. Oceans",
                "volume": "126",
                "pages": "e2021JC017303"
            },
            {
                "authors": "Werdell, P.J. et al.",
                "year": "2013",
                "title": "The OceanOptics InLineAnalysis package used in AC-S data processing",
                "journal": "Limnol. Oceanogr. Methods",
                "volume": "11",
                "pages": "42–54"
            }
        ]
    }

    # Display references by category
    for category, refs in references.items():
        # Header hidden as per user request
        # st.markdown(f"""
        # <div class="section-header">
        #     <h2 style="color: {UI_COLORS['dark']}; margin: 0;">{category}</h2>
        # </div>
        # """, unsafe_allow_html=True)

        for i, ref in enumerate(refs):
            color = CHART_COLORS[i % len(CHART_COLORS)]

            # DOI removed as per user request - keeping reference structure but not displaying DOI
            doi_link = ""

            volume_pages = ""
            if ref["volume"]:
                volume_pages = f"<strong>{ref['volume']}</strong>"
            if ref["pages"]:
                volume_pages += f", {ref['pages']}" if volume_pages else ref["pages"]

            # Add period after volume_pages only if it's not empty
            volume_pages_with_period = f"{volume_pages}." if volume_pages else ""

            # Build the reference text, only adding DOI if it exists
            reference_text = f"<strong>{ref['authors']}</strong> ({ref['year']}). {ref['title']}. <em>{ref['journal']}</em> {volume_pages_with_period}"
            if doi_link:
                reference_text += f" {doi_link}"

            st.markdown(f"""
            <div class="team-card" style="border-left: 4px solid {color};">
                <p style="color: {UI_COLORS['dark']}; margin: 0; line-height: 1.8;">
                    {reference_text}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # AI CHATBOT FOR REFERENCES
    # =========================================================================
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {UI_COLORS['lightest']} 0%, {UI_COLORS['light']} 100%);
                padding: 1.5rem; border-radius: 12px; margin: 2rem 0 2rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h2 style="color: {UI_COLORS['dark']}; text-align: center; margin: 0 0 0.5rem 0;">
            💬 Ask Questions About the Literature
        </h2>
        <p style="color: {UI_COLORS['medium']}; text-align: center; margin: 0; font-size: 0.9em;">
            Chat with AI to resolve theoretical questions related to the report and scientific articles
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for references chat history
    if 'references_chat_history' not in st.session_state:
        st.session_state.references_chat_history = []

    # Create knowledge base from references and scientific concepts
    # Enhanced with content from PDF references in resources/references/
    references_knowledge = {
        # Core ocean color concepts
        "ocean color": "Ocean color remote sensing uses the spectral distribution of light leaving the ocean to estimate water quality parameters. Different algorithms like OC4ME (empirical 4-band ratio) and Neural Networks are used to retrieve Chl-a from spectral reflectance. [Sentinel-3 OLCI validation] Ocean-colour retrievals of chlorophyll-a require direct comparison with in situ data that are representative of diverse optical water types.",

        # Validation and accuracy
        "validation": "Satellite validation requires strict temporal synchronization. ±3h windows capture true algorithmic performance (R²>0.85, MdAPD<17%), while ±1 day windows show natural oceanographic variability (R²~0.64). [From NASA Ocean Optics Protocols] Validation is critical for establishing measurement uncertainties, assessing scientific utility, and identifying conditions where reliability is suspect. Requires high quality in situ data consistently processed across mission lifetime.",
        "matchup": "Matchup analysis pairs satellite and in-situ measurements within temporal/spatial windows. Criteria: <3h temporal separation, <1km spatial, clear water pixels, quality flags passed. Statistics include MdAPD, RMSE, bias, and R². [From validation protocols] The validation of satellite ocean color requires considerable high quality in situ data spanning the satellite mission lifetime.",
        "uncertainty": "Ocean color uncertainties arise from: atmospheric correction (~5-10%), bio-optical algorithms (~15-30%), temporal variability, spatial scale mismatch, and in-situ reference measurements. [IOCCG Report 18] Comprehensive uncertainty analysis shows SNR (Signal-to-Noise Ratio) impacts on water constituent retrieval and the use of remote-sensing reflectance to constrain biogeochemical models.",

        # Algorithms
        "algorithms": "Common ocean color algorithms include: OC4ME (Sentinel-3 empirical), OC-CCI (multi-algorithm blend), Neural Networks (machine learning), and Color Index (oligotrophic waters). All show systematic underestimation at high Chl-a concentrations. [Ocean color algorithms] A high degree of consistency among chlorophyll algorithms is necessary for merging data from concurrent missions (PACE, OLCI, HawkEye, EnMAP, SABIA-MAR).",
        "neural network": "[Ocean color algorithms] Neural network approaches for chlorophyll retrieval provide machine learning-based alternatives to empirical band ratios. Float deployments serve multiple purposes and careful compromises must be made in optimal sensor and mission choice.",

        # Chlorophyll measurements
        "chlorophyll": "Chlorophyll-a can be measured via: (1) HPLC (gold standard), (2) fluorometry (fast, requires calibration), (3) spectrophotometry (676nm line-height), (4) remote sensing (empirical/ML algorithms). Each method has different uncertainty ranges. [Comparing Argo fluorescence to HPLC] Bioregions are identified using k-means partition with reference time series, though larger noise and uncertainties can affect convergence.",
        "fluorescence": "[Comparing Argo fluorescence to HPLC chlorophyll] Fluorescence measurements from BGC-Argo floats require calibration against HPLC chlorophyll-a. Bioregional partitioning helps account for spatial variability in the fluorescence-to-chlorophyll relationship.",

        # BGC-Argo floats
        "argo": "BGC-Argo floats are autonomous profiling platforms with biogeochemical sensors. Hyperspectral floats with TriOS RAMSES radiometers can derive Rrs with R²=0.95 vs PACE. They expand validation networks beyond fixed moorings (Bittig et al. 2019). [Hyperspectral BGC-Argo floats] Uncertainties in measurements arise from differences in analytical, storage, and extraction methods across laboratories.",
        "bgc-argo": "[BGC-Argo validation with PACE] The ocean regulates the carbon balance through dissolved and particulate organic carbon (POC). BGC-Argo provides critical validation for satellite missions like PACE. POC, despite its smaller share, plays a vital role connecting surface biomass production with carbon export.",
        "hyperspectral": "[Hyperspectral BGC-Argo floats] Hyperspectral radiometers on BGC-Argo floats enable high-resolution spectral measurements. Differences in analytical methods and storage protocols are main causes of measurement uncertainties. [BGC-Argo validation with PACE] Hyperspectral measurements from PACE (5nm resolution) provide unprecedented detail for phytoplankton functional types.",
        "ramses": "[Hyperspectral BGC-Argo floats] TriOS RAMSES radiometers deployed on BGC-Argo floats provide hyperspectral measurements for ocean color validation. Careful attention to analytical methods, storage, and extraction protocols is essential for minimizing uncertainties.",

        # Satellite missions
        "sentinel3": "Sentinel-3 OLCI has 21 spectral bands (400-1020nm) at 300m resolution. Uses OC4ME and Neural Network algorithms. The constellation (A+B) provides <2 day revisit. Best performance in OTC25 with ±3h matchups. [Sentinel-3 OLCI validation] Ocean-colour retrievals require comparison with representative in situ match-ups across diverse optical water types.",
        "sentinel-3": "[Sentinel-3 OLCI validation] Evaluating ocean-colour retrievals of total chlorophyll-a requires direct comparison with concomitant and co-located in situ data. Global comparisons require match-ups representative of the distribution of optical water types.",
        "olci": "[Sentinel-3 OLCI validation] OLCI (Ocean and Land Colour Instrument) performance evaluation requires in situ match-ups that are ideally representative of diverse optical water type distributions for global comparisons.",
        "pace": "PACE OCI is NASA's hyperspectral mission (5nm resolution, 340-890nm) launched Feb 2024. Provides unprecedented spectral information for phytoplankton functional types. Showed R²=0.95 agreement with BGC-Argo in OTC25. [BGC-Argo validation with PACE] PACE monitoring of particulate organic carbon is key to understanding the climate system and carbon cycle processes.",

        # Atmospheric correction
        "atmospheric correction": "Atmospheric correction removes ~90% of satellite-measured radiance from atmospheric scattering. Errors propagate significantly to water-leaving radiance, especially in oligotrophic waters and at shorter wavelengths. [Atmospheric correction algorithms] Consistency among algorithms is necessary for merging multi-sensor ocean color data and extending time series across missions.",

        # Drones/UAV
        "drone": "UAV remote sensing faces challenges: sun glint correction, radiometric calibration, atmospheric effects at low altitude, spatial registration. DJI P4M has integrated DLS for irradiance normalization. [Robust ocean color from drones] Accurate retrieval of ocean color from UAVs enables critical observations of small-scale processes in coastal and marine ecology and biogeochemistry.",
        "uav": "[Robust ocean color from drones] Remote sensing from drones enables observations of aquatic systems from open ocean biological oceanography to coastal biodiversity and water quality. Small-scale processes play important roles in coastal and marine ecology.",
        "glint": "[Robust ocean color from drones] Sun glint correction is a major challenge for UAV-based ocean color remote sensing. Viewing geometry and sky reflection removal are critical for robust retrievals.",
        "viewing geometry": "[Robust ocean color from drones] Proper viewing geometry is essential for accurate ocean color retrieval from drones. Sky reflection removal and glint correction depend on careful attention to sensor orientation and sun angle.",
        "sky reflection": "[Robust ocean color from drones] Sky reflection removal is critical for robust ocean color retrieval from UAV platforms. Combined with viewing geometry optimization, it enables accurate observations of coastal and marine systems.",

        # IOPs and instruments
        "iops": "Inherent Optical Properties (IOPs) include absorption (a) and scattering (b) coefficients. They're 'inherent' because they depend only on the medium, not the light field. AC-S spectrophotometers measure both across 400-730nm. [Inline flow-through systems] The Tara Oceans expedition characterized particulate absorption, scattering and attenuation coefficients in the surface ocean using flow-through systems.",
        "absorption": "[AC-S spectrophotometer for IOPs] Optical sensors have advantages in ocean observatories and autonomous platforms due to high-frequency measurements, low power consumption, and established relationships between optical measurements and biogeochemical variables. Biofouling and instrument stability remain challenges.",
        "scattering": "[AC-S spectrophotometer for IOPs] Scattering coefficients measured by optical sensors provide critical biogeochemical information. Issues of biofouling and long-term instrument stability must be carefully managed in autonomous deployments.",
        "ac-s": "[AC-S spectrophotometer for IOPs] The AC-S instrument measures both absorption and scattering across the visible spectrum. High-frequency measurements and low power consumption make it ideal for autonomous platforms, though biofouling mitigation is essential.",
        "inline": "Flow-through systems measure IOPs continuously. AC-S alternates filtered/unfiltered seawater to separate dissolved vs particulate absorption. Chl-a derived via line-height at 676nm. Requires careful calibration and NPQ correction (Boss et al. 2013). [Inline flow-through systems] Underway measurements from ships like Tara Oceans provide continuous characterization of particulate optical properties.",
        "flow-through": "[Inline flow-through systems] Flow-through systems on research vessels enable continuous measurement of absorption, scattering and attenuation coefficients. The Tara Oceans expedition demonstrated the value of underway optical measurements for ocean biogeochemistry.",
        "underway": "[Inline flow-through systems] Underway flow-through systems provide high-resolution spatial characterization of ocean optical properties. Continuous measurements complement discrete sampling and enable observation of small-scale variability.",

        # Protocols and standards
        "protocol": "[NASA Ocean Optics Protocols] Detailed protocols specify instrument performance characteristics, specifications, and rationale for in situ observations supporting satellite validation. SeaBASS archival requirements ensure data quality and accessibility. [Validation protocols] High quality in situ data must be consistently processed across satellite mission lifetimes.",
        "nasa": "[NASA Ocean Optics Protocols] NASA Ocean Optics Protocols (Volume III) review instrument performance characteristics for validation, detailed specifications with underlying rationale, and protocols for in situ observations. SeaBASS data archival policies ensure standardization.",
        "in-situ": "[Validation and matchup protocols] In situ validation data must be high quality, consistently processed, and span the satellite mission lifetime. Temporal/spatial matching criteria and quality control are essential for reliable satellite product validation.",
    }

    # Chat interface
    user_question_ref = st.chat_input("Ask a question about the literature and scientific concepts...")

    if user_question_ref:
        # Add user message to history
        st.session_state.references_chat_history.append({"role": "user", "content": user_question_ref})

        # Simple RAG: search for relevant keywords
        question_lower = user_question_ref.lower()
        relevant_info = []

        for key, value in references_knowledge.items():
            if key in question_lower or any(word in question_lower for word in key.split()):
                relevant_info.append(value)

        # Generate response
        if relevant_info:
            response = "Based on the scientific literature and report:\n\n" + "\n\n".join(relevant_info)
        else:
            # Try to match general topics
            if any(word in question_lower for word in ["satellite", "sentinel", "modis", "pace", "space", "remote sensing"]):
                response = references_knowledge["sentinel3"] + "\n\n" + references_knowledge["pace"] + "\n\n" + references_knowledge["ocean color"]
            elif any(word in question_lower for word in ["validate", "validation", "matchup", "accuracy"]):
                response = references_knowledge["validation"] + "\n\n" + references_knowledge["matchup"] + "\n\n" + references_knowledge["uncertainty"]
            elif any(word in question_lower for word in ["algorithm", "oc4", "neural", "retrieval"]):
                response = references_knowledge["algorithms"] + "\n\n" + references_knowledge["ocean color"]
            elif any(word in question_lower for word in ["chlorophyll", "chl-a", "phytoplankton"]):
                response = references_knowledge["chlorophyll"]
            elif any(word in question_lower for word in ["argo", "float", "bgc"]):
                response = references_knowledge["argo"]
            elif any(word in question_lower for word in ["iop", "absorption", "scattering", "optical"]):
                response = references_knowledge["iops"] + "\n\n" + references_knowledge["inline"]
            elif any(word in question_lower for word in ["uncertainty", "error", "accuracy"]):
                response = references_knowledge["uncertainty"]
            elif any(word in question_lower for word in ["drone", "uav", "phantom"]):
                response = references_knowledge["drone"]
            elif any(word in question_lower for word in ["atmospheric", "correction"]):
                response = references_knowledge["atmospheric correction"]
            else:
                response = "I don't have specific information about that in the references section. Please try asking about: ocean color algorithms, satellite validation, chlorophyll measurements, BGC-Argo floats, hyperspectral floats, RAMSES radiometers, IOPs (absorption/scattering), AC-S spectrophotometer, uncertainty analysis, matchup protocols, atmospheric correction, Sentinel-3/OLCI, PACE, drones/UAV (glint correction, viewing geometry), inline/flow-through systems, fluorescence, NASA protocols, or in-situ measurements."

        # Add assistant response to history
        st.session_state.references_chat_history.append({"role": "assistant", "content": response})

    # Display chat history
    for message in st.session_state.references_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# =============================================================================
# END OF FILE
# =============================================================================
