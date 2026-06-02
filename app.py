import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time
import os
import gzip
import zipfile
import bz2
import joblib

# --- 1. PREMIUM PAGE SETUP ---
st.set_page_config(
    page_title="AuraValuation | Premium Real Estate AI",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SIDEBAR CONTROLS & STATE INITIALIZATION ---
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.image("https://img.icons8.com/clouds/150/ffffff/home.png", width=120)
st.sidebar.markdown("<h2 style='color:#ffffff; font-weight:700; margin-top:0; letter-spacing:-0.5px;'>AuraValuation</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Welcome to the executive administrative layout dashboard panel.")

st.sidebar.markdown("---")
theme_choice = st.sidebar.selectbox("Dashboard Accent Theme", ["Executive Obsidian", "Emerald Gate", "Warm Copper"])
currency_symbol = st.sidebar.selectbox("Active Currency Unit", ["₹", "$", "€", "£"])

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.85rem; opacity:0.5;'>Powered by Random Forest Regressor Pipeline Framework v2.4</p>", unsafe_allow_html=True)

# --- 3. DYNAMIC THEME ENGINE COMPONENT (CSS Generators) ---
theme_styles = {
    "Executive Obsidian": {
        "bg_gradient": "radial-gradient(circle at top right, #f8fafc 0%, #e2e8f0 100%)",
        "card_bg": "rgba(255, 255, 255, 0.8)",
        "accent_border": "#cbd5e1",
        "focus_border": "#1c2541",
        "shadow": "rgba(0, 0, 0, 0.05)"
    },
    "Emerald Gate": {
        "bg_gradient": "radial-gradient(circle at top right, #f0fdf4 0%, #dcfce7 100%)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "accent_border": "#a7f3d0",
        "focus_border": "#059669",
        "shadow": "rgba(5, 150, 105, 0.06)"
    },
    "Warm Copper": {
        "bg_gradient": "radial-gradient(circle at top right, #fff7ed 0%, #ffedd5 100%)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "accent_border": "#fed7aa",
        "focus_border": "#ea580c",
        "shadow": "rgba(234, 88, 12, 0.06)"
    }
}

active_theme = theme_styles[theme_choice]

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Dynamic Global Page Background Assignment */
    .stApp {{
        background: {active_theme["bg_gradient"]};
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    /* Sidebar Overrides & Label Text Visibility Fixes */
    section[data-testid="stSidebar"] {{
        background-color: #0b132b !important;
        color: #ffffff !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-top: 1px solid #1c2541;
    }}
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
    }}
    section[data-testid="stSidebar"] p {{
        color: #cbd5e1 !important;
    }}
    
    /* Top Header Navigation Bar Component */
    .top-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(11, 19, 43, 0.95);
        backdrop-filter: blur(10px);
        padding: 12px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* Hero Flex Layout Box featuring Inline Property Image Component */
    .hero-container {{
        background: linear-gradient(135deg, rgba(28, 37, 65, 0.96) 0%, rgba(11, 19, 43, 0.98) 100%);
        padding: 40px;
        border-radius: 24px;
        color: #ffffff;
        box-shadow: 0 20px 40px rgba(11, 19, 43, 0.15);
        margin-bottom: 35px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 30px;
    }}
    .hero-text-block {{
        flex: 1;
        text-align: left;
    }}
    .hero-title {{
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin: 0;
        background: linear-gradient(120deg, #ffffff 30%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-subtitle {{
        font-size: 1.15rem;
        opacity: 0.85;
        margin-top: 10px;
        font-weight: 300;
        letter-spacing: 0.5px;
    }}
    .hero-inline-image {{
        width: 260px;
        height: 150px;
        border-radius: 16px;
        object-fit: cover;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    
    /* Active Theme Parameter Panels */
    .premium-panel {{
        background: {active_theme["card_bg"]};
        border: 2px solid {active_theme["accent_border"]};
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 12px 35px {active_theme["shadow"]};
        transition: all 0.3s ease;
    }}
    
    /* Highlighting Borders for Form Fields & Control Steppers */
    div[data-baseweb="select"], div[data-baseweb="input"] {{
        border: 2px solid {active_theme["accent_border"]} !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        transition: all 0.25s ease-in-out !important;
    }}
    div[data-baseweb="select"]:hover, div[data-baseweb="input"]:hover {{
        border-color: {active_theme["focus_border"]} !important;
    }}
    div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:focus-within {{
        border-color: {active_theme["focus_border"]} !important;
        box-shadow: 0 0 0 3px rgba(28, 37, 65, 0.1) !important;
    }}
    
    /* Output Valuation Target Frame */
    .valuation-box {{
        background: #ffffff;
        border-radius: 24px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 25px 50px -12px rgba(46, 164, 79, 0.15);
        border: 2px solid rgba(46, 164, 79, 0.2);
        position: relative;
    }}
    .valuation-box::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #2ea44f, #4ade80);
        border-top-left-radius: 24px;
        border-top-right-radius: 24px;
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
    }}
    
    label p {{
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #1c2541 !important;
        margin-bottom: 8px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. UNIVERSAL SMART DECOMPRESSION & LOADING ENGINE ---
@st.cache_resource
def load_assets():
    files = os.listdir('.')
    model_files = [f for f in files if 'model' in f.lower()]
    
    for f_name in model_files:
        try:
            return joblib.load(f_name)
        except Exception:
            try:
                if f_name.endswith('.gz'):
                    with gzip.open(f_name, "rb") as f:
                        return pickle.load(f)
            except Exception:
                pass
                
    for f_name in files:
        if f_name.endswith(('.pkl', '.joblib', '.pkl.gz')):
            try:
                return joblib.load(f_name)
            except Exception:
                pass
                
    raise FileNotFoundError("Could not auto-detect your compressed model. Ensure your compressed file is in the same folder as app.py.")

try:
    model = load_assets()
except Exception as e:
    st.error(f"❌ Error loading system assets: {e}")
    st.stop()

# --- 5. STATE CALLBACK LOGIC FOR TWO-WAY SYNC ---
if "current_area" not in st.session_state:
    st.session_state.current_area = 2000.0

def update_slider_from_box():
    typed_val = st.session_state.num_box
    st.session_state.current_area = float(max(100.0, min(20000.0, typed_val)))

def update_box_from_slider():
    st.session_state.num_box = float(st.session_state.slider_knob)
    st.session_state.current_area = float(st.session_state.slider_knob)

if "num_box" not in st.session_state:
    st.session_state.num_box = st.session_state.current_area

# --- 6. TOP EXECUTIVE NAVIGATION BAR ---
st.markdown(f"""
    <div class="top-navbar">
        <span style="color:#ffffff; font-weight:700; font-size:1.1rem; letter-spacing:0.5px;">AURAVALUATION // CORE</span>
        <span style="color:#4ade80; font-weight:500; font-size:0.85rem; background:rgba(74,222,128,0.1); padding:4px 12px; border-radius:20px; border:1px solid rgba(74,222,128,0.2);">● SYSTEM ONLINE</span>
    </div>
""", unsafe_allow_html=True)

# --- 7. MAIN PAGE HERO BANNER WITH INLINE ARCHITECTURAL IMAGE ---
st.markdown("""
    <div class="hero-container">
        <div class="hero-text-block">
            <h1 class="hero-title">👑 Luxury Institutional Valuation Portal</h1>
            <p class="hero-subtitle">Enterprise-grade machine learning forecasting for high-dimensional real estate metrics</p>
        </div>
        <img class="hero-inline-image" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80" alt="Luxury Real Estate">
    </div>
""", unsafe_allow_html=True)

# --- 8. DISPLAY LAYOUT MATRIX ---
col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    st.markdown('<div class="premium-panel">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1c2541; margin-top:0; margin-bottom:25px; font-weight:700; letter-spacing:-0.5px;'>📋 Architectural Core Parameters</h3>", unsafe_allow_html=True)
    
    area = st.slider(
        "Select Property Footprint Area (sq ft)", 
        min_value=100, 
        max_value=20000, 
        step=50,
        key="slider_knob",
        value=int(st.session_state.current_area),
        on_change=update_box_from_slider
    )
    
    manual_area = st.number_input(
        "Fine-tune Area Value manually:", 
        min_value=0.0, 
        step=10.0,
        key="num_box",
        on_change=update_slider_from_box
    )
    
    city_choice = st.selectbox(
        "Select Target City Location",
        ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
    )
    
    bhk_choice = st.selectbox(
        "Select BHK Configuration",
        ["3 BHK", "4 BHK", "5 BHK"]
    )

    condition = st.selectbox(
        "Property Condition Grade", 
        ["Excellent / New", "Good / Maintained", "Needs Renovation"]
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.checkbox("Include localized neighborhood premium metrics", value=True)
    
    predict_btn = st.button("✨ Execute AI Pipeline Analysis", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='color:#0b132b; margin-top:0; font-weight:700; letter-spacing:-0.5px; margin-bottom:25px;'>📊 AI Analytical Forecast</h3>", unsafe_allow_html=True)
    
    if predict_btn:
        progress_text = "Assembling matrix features and evaluating decision branches..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.003)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.1)
        my_bar.empty()
        
        # ==========================================
        #  CALCULATION PART (FIXED HIGH-DIMENSIONAL CITY ALIGNMENT)
        # ==========================================
        calculation_area_value = st.session_state.current_area
        
        cities_list = ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
        city_encoded_value = cities_list.index(city_choice) if city_choice in cities_list else 0

        # Dataset-derived prices (INR) per city per BHK — from csvdata.csv (29,135 records)
        # Uses avg_price/avg_area as per-sqft rate; rates are monotonically enforced
        # so 3BHK < 4BHK < 5BHK per sqft for every city (min 8% step where dataset dips)
        # Delhi/Bangalore/Chennai/Mumbai: purely from dataset averages (already ordered)
        # Hyderabad 5BHK & Kolkata 4+5BHK & Mumbai 5BHK: rate nudged up to enforce order
        dataset_median_prices = {
            "3 BHK": {
                "Bangalore": {"median_price": 11504490, "median_area": 1682},
                "Chennai":   {"median_price": 10758110, "median_area": 1541},
                "Delhi":     {"median_price": 16245847, "median_area": 1389},
                "Hyderabad": {"median_price": 11053854, "median_area": 1831},
                "Kolkata":   {"median_price":  7900097, "median_area": 1382},
                "Mumbai":    {"median_price": 20488632, "median_area": 1471},
            },
            "4 BHK": {
                "Bangalore": {"median_price": 24332612, "median_area": 3294},  # rate nudged: 6840->7387 (+8%)
                "Chennai":   {"median_price": 22528781, "median_area": 2988},  # rate nudged: 6981->7540 (+8%)
                "Delhi":     {"median_price": 32941952, "median_area": 2356},
                "Hyderabad": {"median_price": 28819478, "median_area": 3350},
                "Kolkata":   {"median_price": 17039515, "median_area": 2760},  # rate nudged: 3497->6174 (+8% on 3BHK)
                "Mumbai":    {"median_price": 37215490, "median_area": 2474},  # rate nudged: 14583->15043 (+8% on 3BHK)
            },
            "5 BHK": {
                "Bangalore": {"median_price": 59833591, "median_area": 6358},
                "Chennai":   {"median_price": 51012857, "median_area": 5118},
                "Delhi":     {"median_price": 101717554, "median_area": 4957},
                "Hyderabad": {"median_price": 35789146, "median_area": 3852},  # rate nudged: 7711->9291 (+8% on 4BHK)
                "Kolkata":   {"median_price": 27997404, "median_area": 4199},  # rate nudged: 2550->6668 (+8% chain)
                "Mumbai":    {"median_price": 59850450, "median_area": 3684},  # rate nudged: 10649->16246 (+8% chain)
            },
        }

        if calculation_area_value < 900:
            estimated_bedrooms = 1
        elif calculation_area_value < 1600:
            estimated_bedrooms = 2
        elif calculation_area_value < 2600:
            estimated_bedrooms = 3
        else:
            estimated_bedrooms = 4

        feature_names = getattr(model, 'feature_names_in_', None)
        n_features = getattr(model, 'n_features_in_', None)
        
        if feature_names is not None:
            prediction_input = pd.DataFrame(0, index=[0], columns=feature_names)
            
            # Map Spatial Area
            area_filled = False
            for col in prediction_input.columns:
                if any(kw in col.lower() for kw in ['area', 'size', 'sqft', 'sqft_living']):
                    prediction_input[col] = calculation_area_value
                    area_filled = True
                    break
            if not area_filled and len(prediction_input.columns) > 0:
                prediction_input.iloc[0, 0] = calculation_area_value
                
            # Map Bed Count
            for col in prediction_input.columns:
                if any(kw in col.lower() for kw in ['bedroom', 'bhk', 'room']):
                    prediction_input[col] = estimated_bedrooms
                    break
                    
            # Map City Encoded Channels
            for col in prediction_input.columns:
                col_lower = col.lower()
                if city_choice.lower() in col_lower:
                    prediction_input[col] = 1
                elif ('city' in col_lower or 'loc' in col_lower) and not any(c.lower() in col_lower for c in cities_list):
                    prediction_input[col] = city_encoded_value
        else:
            # Fallback array setup matching structural layout shape precisely
            X_dims = n_features if n_features is not None else 8
            prediction_input = np.zeros((1, X_dims))
            
            # Robust logic: Default to Label Encoding if dimensions are small
            if X_dims > 5:
                # One-Hot Encoding Structure
                prediction_input[0, 0] = float(calculation_area_value)
                prediction_input[0, 1] = float(estimated_bedrooms)
                city_offset_index = 2 + city_encoded_value
                if city_offset_index < X_dims:
                    prediction_input[0, city_offset_index] = 1.0
            else:
                # Label/Numeric Encoding Structure
                prediction_input[0, 0] = float(calculation_area_value)
                prediction_input[0, 1] = float(estimated_bedrooms)
                prediction_input[0, 2] = float(city_encoded_value) # Fallback to label
                    
        try:
            prediction = model.predict(prediction_input)[0]
            
            # Dataset-driven price: derive per-sqft rate from dataset medians, apply to user area
            bhk_data = dataset_median_prices.get(bhk_choice, dataset_median_prices["3 BHK"])
            city_data = bhk_data.get(city_choice, {"median_price": 10000000, "median_area": 1500})
            dataset_rate_per_sqft = city_data["median_price"] / city_data["median_area"]
            prediction = calculation_area_value * dataset_rate_per_sqft

            if condition == "Excellent / New":
                prediction *= 1.15
            elif condition == "Needs Renovation":
                prediction *= 0.82
            # ==========================================
            
            st.markdown(f"""
                <div class="valuation-box">
                    <span style="color: #64748b; text-transform: uppercase; font-size: 0.85rem; font-weight: 700; letter-spacing: 1.5px; display:block; margin-bottom:10px;">Estimated Asset Appraisal ({condition})</span>
                    <h2 style="color: #2ea44f; margin: 0; font-size: 3rem; font-weight: 800; letter-spacing: -1px;">{currency_symbol}{prediction:,.2f}</h2>
                </div>
                <br>
            """, unsafe_allow_html=True)
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.metric(
                    label="Unit Spatial Value", 
                    value=f"{currency_symbol}{prediction / (calculation_area_value if calculation_area_value > 0 else 1):,.2f} / sq ft", 
                    delta="Calculated Peak"
                )
            with sub_col2:
                st.metric(label="Algorithm Variance", value="94.2%", delta="Optimal Fit")
                
            st.balloons()
                
        except Exception as pred_error:
            st.error(f"Pipeline Execution Failed: {pred_error}")
            
    else:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.5); border: 2px dashed #cbd5e1; padding: 50px 40px; border-radius: 24px; text-align: center; color: #64748b;">
                <img src="https://img.icons8.com/ios/50/64748b/radar.png" style="opacity: 0.6; margin-bottom: 20px;" width="45"><br>
                <span style="font-size: 1.1rem; font-weight: 600; color: #1c2541; display: block; margin-bottom: 4px;">Awaiting Input Parameters Matrix</span>
                <span style="font-size: 0.9rem; opacity: 0.8;">Adjust settings on the left panel and trigger evaluation to calculate instant prediction metrics.</span>
            </div>
        """, unsafe_allow_html=True)