
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Inflation Analytics Dashboard - India",
    layout="wide"
)

# ======================================================
# CUSTOM CSS & THEME
# ======================================================
st.markdown("""
<style>
    /* Global Font & Reset */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* =========================================
       1. Global Typography & Reset
       ========================================= */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        color: #388087 !important;
        background-color: #F6F6F2 !important;
        font-size: 19px !important; /* Increased base size */
        font-weight: 500 !important; /* Added weight */
    }

    h1, h2, h3, h4, h5, h6, p, label, button, input, select, textarea, li {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    /* Input Labels & Markdown Text */
    p, label, li, .stSelectbox label, .stNumberInput label, .stSlider label, .stDateInput label {
        font-size: 19px !important;
        font-weight: 600 !important; /* Heavier for readability */
        color: #388087 !important;
    }
    
    /* =========================================
       2. Headings (Hierarchy)
       ========================================= */
    h1, h2, h3, h4, h5, h6, .css-10trblm {
        color: #388087 !important; 
        font-weight: 800 !important;
        line-height: 1.2 !important;
        margin-bottom: 1rem !important;
    }
    
    h1 { font-size: 3.2rem !important; }
    h2 { font-size: 2.4rem !important; }
    h3 { font-size: 1.9rem !important; }
    
    /* Metric Labels & Small Text */
    div[data-testid="stMetric"] label {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
    }

    /* =========================================
       3. Sidebar Styling
       ========================================= */
    [data-testid="stSidebar"] {
        background-color: #C2EDCE !important;
        border-right: 1px solid #6FB3B8 !important;
    }
    
    /* Sidebar Section Headers */
    [data-testid="stSidebar"] h1 {
        font-size: 2.0rem !important;
        font-weight: 800 !important;
        margin-top: 1rem !important;
        margin-bottom: 2rem !important;
    }
    
    /* Navigation Links */
    div[data-testid="stSidebarUserContent"] .stRadio label {
        padding: 12px 15px !important; /* Increased padding for larger text */
        border-radius: 6px;
        margin-bottom: 6px !important;
        transition: all 0.2s ease;
    }
    
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        font-size: 20px !important; /* Increased Nav Link Size */
        font-weight: 600 !important; /* Increased Nav Link Weight */
        color: #388087 !important;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label:hover {
        background-color: rgba(56, 128, 135, 0.1) !important;
    }
    
    /* Active State (Simulated) */
    div[data-testid="stSidebarUserContent"] .stRadio label:has(input:checked) {
        background-color: #388087 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    div[data-testid="stSidebarUserContent"] .stRadio label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stSidebarUserContent"] .stRadio label {
        border-left: 4px solid transparent !important;
    }
    div[data-testid="stSidebarUserContent"] .stRadio label:hover {
         border-left: 4px solid #388087 !important;
    }
    
    /* Metric Cards - White or Light Blue */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #6FB3B8 !important; /* Medium Teal Border */
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #388087 !important; /* Dark Teal Border on Hover */
        background-color: #BADFE7 !important; /* Light Blue on Hover */
    }
    
    div[data-testid="stMetric"] label {
        color: #388087 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #388087 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #6FB3B8 !important; 
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stMetricDelta"] svg {
        fill: #6FB3B8 !important;
    }
    
    /* Custom Card Styling for st.container(border=True) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(56, 128, 135, 0.15); /* Teal shadow */
        border: 1px solid #BADFE7 !important;
        padding: 1.5rem !important;
        margin-bottom: 20px;
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #6FB3B8 !important;
    }
    
    /* Input Fields Labels */
    .stSelectbox label, .stNumberInput label, .stSlider label, .stDateInput label {
        color: #388087 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* Input Fields Backgrounds */
    input, select {
        color: #388087 !important;
        background-color: #F6F6F2 !important;
        border: 2px solid #BADFE7 !important;
        font-weight: 600 !important;
    }
    
    /* Focused Input */
    input:focus, select:focus {
        border-color: #388087 !important;
        background-color: #FFFFFF !important;
        color: #388087 !important;
    }
    
    /* =========================================
       4. Component Specific Overrides
       ========================================= */

    /* Dropdown/Selectbox Background & Border */
    div[data-baseweb="select"] > div {
        background-color: #F6F6F2 !important;
        border-color: #BADFE7 !important;
        color: #388087 !important;
    }
    
    /* Dropdown Menu Items (The list itself) */
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #F6F6F2 !important;
    }
    
    /* Individual Options */
    li[role="option"] {
        background-color: #F6F6F2 !important;
        color: #388087 !important;
    }
    
    /* Hover/Focus State for Options */
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #BADFE7 !important;
        color: #388087 !important;
    }
    
    /* Selected Value Display */
    div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p {
        color: #388087 !important;
    }

    /* Alert Boxes */
    div[data-testid="stAlert"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        border-left: 5px solid;
    }
    
    div[data-testid="stAlert"][data-test-alert-type="success"] {
        background-color: #C2EDCE !important;
        border-color: #388087 !important; 
        color: #388087 !important;
    }
    div[data-testid="stAlert"][data-test-alert-type="error"] {
        background-color: #F8D7DA !important;
        border-color: #721c24 !important; 
        color: #721c24 !important;
    }
    div[data-testid="stAlert"][data-test-alert-type="info"] {
        background-color: #BADFE7 !important;
        border-color: #388087 !important;
        color: #388087 !important;
    }
    
    /* Expander - Targeting the details/summary element specifically */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 2px solid #BADFE7 !important;
        border-radius: 8px !important;
        color: #388087 !important;
    }

    div[data-testid="stExpander"] details {
        background-color: #FFFFFF !important;
        color: #388087 !important;
    }

    div[data-testid="stExpander"] summary {
        color: #388087 !important;
        background-color: #FFFFFF !important;
    }
    
    div[data-testid="stExpander"] summary:hover {
        color: #388087 !important;
        background-color: #F6F6F2 !important;
    }

    div[data-testid="stExpander"] svg {
        fill: #388087 !important;
    }
    
    /* Force text color inside the summary */
    div[data-testid="stExpander"] summary p {
        color: #388087 !important;
        font-weight: 700 !important;
    }
    
    /* Content inside expander */
    div[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
        background-color: #F6F6F2 !important;
        color: #388087 !important;
    }

    /* DataFrame/Table Text - Targeting cells specifically */
    div[data-testid="stDataFrame"] div, 
    div[data-testid="stDataFrame"] span,
    div[data-testid="stTable"] div,
    div[data-testid="stTable"] span {
        color: #388087 !important;
        background-color: #F6F6F2 !important;
    }
    
    /* Number Input Buttons (+/-) */
    div[data-testid="stNumberInput"] button {
        background-color: #388087 !important; /* Dark Teal Background */
        color: #F6F6F2 !important; /* Light Text */
        border-color: #388087 !important;
    }
    
    div[data-testid="stNumberInput"] button:hover {
        background-color: #2a6066 !important; /* Slightly darker on hover */
        border-color: #2a6066 !important;
    }
    
    div[data-testid="stNumberInput"] button:active {
        background-color: #1c4044 !important;
    }
    
    /* Fix for any SVG icons inside buttons that might be black */
    div[data-testid="stNumberInput"] button svg {
        fill: #F6F6F2 !important;
    }

    /* DataFrame/Table Text */
    div[data-testid="stDataFrame"] div, div[data-testid="stTable"] div {
        color: #388087 !important;
        background-color: #F6F6F2 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #388087; /* Dark Teal */
        color: #FFFFFF; /* White Text */
        border-radius: 8px;
        font-weight: 700;
        border: none;
        padding: 0.5rem 1rem;
        transition: opacity 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #6FB3B8; /* Medium Teal */
        color: #FFFFFF;
        border: none;
    }

    /* Slider Specifics */
    div[role="slider"] {
         background-color: #388087 !important; /* Thumb */
         box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Targeting the track is tricky without stable classes, 
       but we can at least ensure the value text above is correct */
    div[data-baseweb="slider"] div[data-testid="stMarkdownContainer"] p {
        color: #388087 !important;
    }
    
    /* Input Fields spacing */
    .stSelectbox, .stNumberInput, .stSlider {
        margin-bottom: 16px;
    }
    
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================
df = pd.read_csv(
    "data/final_all_india_cpi.csv",
    parse_dates=["Date"],
    index_col="Date"
)

# Load full dataset for food analysis
df_full = pd.read_csv("data/all_india_cpi.csv")
df_full = df_full[df_full["Sector"] == "Rural+Urban"]

df_full["Date"] = pd.to_datetime(
    df_full["Year"].astype(str) + "-" + df_full["Month"],
    format="%Y-%B",
    errors="coerce"
)

df_full.set_index("Date", inplace=True)

# Load SARIMA model
with open("model/sarima_model.pkl", "rb") as f:
    model = pickle.load(f)

# ======================================================
# SIDEBAR NAVIGATION
# ======================================================
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to:",
    [
        "Dashboard",
        "Forecast",
        "Inflation Calculator",
        "Food Analysis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard provides insights into India's CPI inflation trends, "
    "forecasts future values, and analyzes food price changes."
)


# ======================================================
# DASHBOARD SECTION
# ======================================================
if menu == "Dashboard":

    st.title("Inflation Overview")
    st.markdown("Monitor key inflation indicators and trends.")

    # KPI Metrics
    col1, col2, col3 = st.columns(3)

    latest_cpi = df.iloc[-1]["CPI"]
    previous_cpi = df.iloc[-2]["CPI"]
    cpi_12_months_ago = df.iloc[-13]["CPI"]

    monthly_inflation = ((latest_cpi - previous_cpi) / previous_cpi) * 100
    yearly_inflation_value = ((latest_cpi - cpi_12_months_ago) / cpi_12_months_ago) * 100

    col1.metric("Latest CPI", f"{latest_cpi:.2f}")
    
    # Yearly Inflation
    col2.metric(
        "Yearly Inflation", 
        f"{yearly_inflation_value:.2f}%",
        delta=f"{yearly_inflation_value:.2f}%",
        delta_color="inverse"
    )

    # Monthly Inflation
    col3.metric(
        "Monthly Inflation", 
        f"{monthly_inflation:.2f}%",
        delta=f"{monthly_inflation:.2f}%",
        delta_color="inverse"
    )

    # Status Indicator
    st.markdown("---")
    if monthly_inflation > 0.3:
        st.error("Inflation Trend: Rising")
    elif monthly_inflation < -0.3:
        st.success("Inflation Trend: Falling")
    else:
        st.info("Inflation Trend: Stable")

    # Data Information
    
    with st.container(border=True):
        st.subheader("Data Summary")
        colA, colB, colC = st.columns(3)
        
        # Determine date range string
        date_range = f"{df.index.min().strftime('%b %Y')} - {df.index.max().strftime('%b %Y')}"
        
        colA.metric("Data Range", date_range)
        colB.metric("Total Observations", str(len(df)))
        colC.metric("Frequency", "Monthly")

    with st.expander("View Data Source"):
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)


    # ======================================================
    # SEASONAL TREND ANALYSIS
    # ======================================================
    st.markdown("---")
    st.subheader("Seasonal Trend Analysis")

    df_season = df.copy()
    df_season["Month"] = df_season.index.month

    # Average CPI by month
    monthly_avg = df_season.groupby("Month")["CPI"].mean()

    fig_season, ax_season = plt.subplots(figsize=(8, 4))
    
    # Styling
    fig_season.patch.set_facecolor('none')
    ax_season.set_facecolor('none')
    
    ax_season.plot(monthly_avg.index, monthly_avg.values, marker="o", color="#388087", linewidth=2)
    ax_season.set_title("Average CPI by Month", color="#388087", fontweight="bold")
    ax_season.set_xlabel("Month", color="#388087")
    ax_season.set_ylabel("Average CPI", color="#388087")
    ax_season.tick_params(colors="#388087", which='both')
    ax_season.grid(True, linestyle=':', alpha=0.5, color='#6FB3B8')
    
    # Spines
    for spine in ax_season.spines.values():
        spine.set_color('#388087')
    ax_season.spines['top'].set_visible(False)
    ax_season.spines['right'].set_visible(False)

    st.pyplot(fig_season)

    # Seasonal Grouping & Insights
    st.subheader("Seasonal Insights")
    
    # Define seasons
    def assign_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Summer"
        elif month in [6, 7, 8, 9]:
            return "Monsoon"
        else:
            return "Post-Monsoon"

    df_season["Season"] = df_season["Month"].apply(assign_season)
    
    # Order for tabs
    season_order = ["Winter", "Summer", "Monsoon", "Post-Monsoon"]
    tabs = st.tabs(season_order)

    for i, season in enumerate(season_order):
        with tabs[i]:
            # Filter data for this season
            season_data = df_season[df_season["Season"] == season]
            
            if not season_data.empty:
                avg_cpi = season_data["CPI"].mean()
                peak_month_num = season_data.groupby("Month")["CPI"].mean().idxmax()
                peak_month_name = pd.to_datetime(f"2000-{peak_month_num}-01").strftime('%B')
                
                col_s1, col_s2 = st.columns(2)
                
                col_s1.metric("Average CPI", f"{avg_cpi:.2f}")
                col_s2.metric("Peak Inflation Month", peak_month_name)
                
                # Dynamic Insight
                if season == "Winter":
                    st.info("Winter months (Dec-Feb) often see lower food prices due to fresh harvest arrivals.")
                elif season == "Summer":
                    st.info("Summer (Mar-May) prices may rise due to heat-induced supply constraints.")
                elif season == "Monsoon":
                    st.info("Monsoon (Jun-Sep) inflation is critical; rains affect crop sowing and logistics.")
                else: 
                    st.info("Post-Monsoon (Oct-Nov) stabilizes prices as the kharif harvest begins.")
            else:
                st.write("No data available for this season.")




# ======================================================
# FORECAST SECTION
# ======================================================
elif menu == "Forecast":

    st.title("CPI Forecast")
    st.markdown("Projected Consumer Price Index trends based on historical data.")

    # Controls
    with st.expander("Forecast Settings", expanded=True):
        months = st.slider("Select months to forecast", 6, 24, 12)

    forecast = model.get_forecast(steps=months)
    forecast_values = forecast.predicted_mean
    confidence_intervals = forecast.conf_int()

    future_dates = pd.date_range(
        start=df.index[-1] + pd.DateOffset(months=1),
        periods=months,
        freq="MS"
    )

    forecast_values.index = future_dates
    confidence_intervals.index = future_dates

    # Forecast KPI
    st.metric(
        f"Forecasted CPI after {months} months",
        f"{forecast_values.iloc[-1]:.2f}"
    )

    # Plot
    st.subheader("Forecast Visualization")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Professional Plot Styling (Custom Palette)
    fig.patch.set_facecolor('none') # Transparent background
    ax.set_facecolor('none') # Transparent axes background
    
    # Colors from palette
    color_history = "#388087" # Dark Teal for History
    color_forecast = "#6FB3B8" # Medium Teal for Forecast
    color_ci = "#BADFE7" # Light Blue for Conf Interval
    color_text = "#388087" # Dark Teal Text

    ax.plot(df.index, df["CPI"], label="Historical CPI", color=color_history, linewidth=2)
    ax.plot(forecast_values.index, forecast_values, label="Forecast", color=color_forecast, linestyle="--", linewidth=2)

    ax.fill_between(
        forecast_values.index,
        confidence_intervals.iloc[:, 0],
        confidence_intervals.iloc[:, 1],
        color=color_ci,
        alpha=0.5, # Visibility
        label="95% Confidence Interval"
    )

    ax.set_title("CPI Trends & Projections", fontsize=14, fontweight='bold', color=color_text)
    ax.set_xlabel("Date", fontsize=10, color=color_text)
    ax.set_ylabel("CPI Value", fontsize=10, color=color_text)
    ax.tick_params(colors=color_text, which='both', labelsize=9)
    
    # Legend
    legend = ax.legend(frameon=True, framealpha=0.9, facecolor='#FFFFFF', edgecolor='#388087')
    plt.setp(legend.get_texts(), color=color_text)

    ax.grid(True, linestyle=':', alpha=0.5, color='#6FB3B8') 

    st.pyplot(fig)

# ======================================================
# INFLATION CALCULATOR
# ======================================================
elif menu == "Inflation Calculator":

    st.title("Inflation Calculator")
    st.markdown("Calculate how purchasing power has changed over time.")

    # Prepare yearly CPI
    df_calc = df.copy()
    df_calc["Year"] = df_calc.index.year
    yearly_cpi = df_calc.groupby("Year")["CPI"].mean()
    years = yearly_cpi.index.tolist()

    with st.container(border=True):
        st.subheader("Parameters")
        col1, col2, col3 = st.columns(3)

        # Amount input inputs
        amount = col1.number_input(
            "Enter Amount (INR)",
            min_value=1000,
            max_value=10000000,
            value=10000,
            step=1000,
            format="%d"
        )

        start_year = col2.selectbox("Start Year", years)
        end_year = col3.selectbox("End Year", years, index=len(years)-1)

    if start_year < end_year:

        cpi_start = yearly_cpi.loc[start_year]
        cpi_end = yearly_cpi.loc[end_year]

        adjusted_value = amount * (cpi_end / cpi_start)
        inflation_percent = ((cpi_end - cpi_start) / cpi_start) * 100

        st.markdown("---")
        st.subheader("Calculation Result")

        colA, colB, colC = st.columns(3)

        colA.metric(
            label=f"Value in {start_year}",
            value=f"₹ {amount:,.0f}"
        )
        
        colB.metric(
            label=f"Equivalent Value in {end_year}",
            value=f"₹ {adjusted_value:,.0f}"
        )

        colC.metric(
            label="Inflation Change",
            value=f"{inflation_percent:.2f}%",
            delta=f"{inflation_percent:.2f}%" if inflation_percent > 0 else f"{inflation_percent:.2f}%",
            delta_color="inverse"
        )

        st.info(
            f"Prices increased by **{inflation_percent:.2f}%** between {start_year} and {end_year}. "
            f"To maintain the same purchasing power as **₹{amount:,}** in {start_year}, "
            f"you would need **₹{adjusted_value:,.0f}** in {end_year}."
        )

    elif start_year == end_year:
        st.warning("Start and End year are the same. No inflation change.")

    else:
        st.error("End year must be greater than start year.")

# ======================================================
# FOOD ANALYSIS SECTION
# ======================================================
elif menu == "Food Analysis":

    st.title("Essential Food Inflation")
    st.markdown("Compare price changes across different food categories.")

    food_categories = [
        "Cereals and products",
        "Milk and products",
        "Oils and fats",
        "Fruits",
        "Vegetables",
        "Food and beverages"
    ]

    df_food = df_full.copy()
    df_food["Year"] = df_food.index.year
    yearly_food = df_food.groupby("Year")[food_categories].mean()

    years = yearly_food.index.tolist()

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        selected_food = col1.selectbox("Select Category", food_categories)
        start_year_food = col2.selectbox("Start Year", years)
        end_year_food = col3.selectbox("End Year", years, index=len(years)-1)

    if start_year_food < end_year_food:

        start_value = yearly_food.loc[start_year_food, selected_food]
        end_value = yearly_food.loc[end_year_food, selected_food]

        percent_change = ((end_value - start_value) / start_value) * 100

        st.subheader("Analysis Result")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        col_res1.metric(
            f"{selected_food} ({start_year_food})",
            f"{start_value:.2f}"
        )
        
        col_res2.metric(
            f"{selected_food} ({end_year_food})",
            f"{end_value:.2f}"
        )

        col_res3.metric(
            "Percentage Change",
            f"{percent_change:.2f}%",
            delta=f"{percent_change:.2f}%",
            delta_color="inverse"
        )
        
        # Simple bar chart for visual comparison
        fig_food, ax_food = plt.subplots(figsize=(6, 1.5))
        
        # Custom Theme colors
        color_start = "#6FB3B8" # Medium Teal
        color_end = "#388087" # Dark Teal
        
        ax_food.barh(["Start Year", "End Year"], [start_value, end_value], color=[color_start, color_end])
        ax_food.set_xlim(0, max(start_value, end_value) * 1.25)
        
        # Transparent background for seamless integration
        ax_food.set_facecolor('none')
        fig_food.patch.set_facecolor('none')
        
        for i, v in enumerate([start_value, end_value]):
             ax_food.text(v + 1, i, f"{v:.2f}", va='center', color='#388087', fontweight='bold', fontsize=10)
             
        ax_food.spines['top'].set_visible(False)
        ax_food.spines['right'].set_visible(False)
        ax_food.spines['bottom'].set_visible(False)
        ax_food.spines['left'].set_visible(False)
        
        # Configure tick params
        ax_food.tick_params(axis='y', colors='#388087', labelsize=10) # Y-axis labels (Start/End Year)
        ax_food.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) # Hide X-axis
        
        st.pyplot(fig_food)

    elif start_year_food == end_year_food:
        st.warning("Start and End year are the same.")
    else:
        st.error("End year must be greater than start year.")
