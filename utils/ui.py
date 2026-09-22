import streamlit as st
import pandas as pd


def inject_custom_css():
    """
    Injects custom CSS styling for high-contrast typography, styled metric cards,
    and responsive layout paddings.
    """
    st.markdown("""
        <style>
        /* Main Container Styling */
        .main .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
            max-width: 96%;
        }

        /* Metric Card Container Styling */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-left: 5px solid #1E88E5;
            padding: 0.9rem 1.1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            color: #555555 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: #1A237E !important;
        }

        /* Custom Banner & Alert Styles */
        .badge-provisional {
            background-color: #FFF3E0;
            color: #E65100;
            border: 1px solid #FFE0B2;
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 0.5rem;
        }

        .pedagogical-callout {
            background-color: #E3F2FD;
            border-left: 5px solid #1E88E5;
            padding: 0.9rem 1.2rem;
            border-radius: 6px;
            margin-top: 0.5rem;
            margin-bottom: 1.2rem;
            color: #0D47A1;
        }

        .pedagogical-callout h4 {
            margin: 0 0 0.4rem 0;
            font-size: 1rem;
            font-weight: 700;
            color: #0D47A1;
        }

        .pedagogical-callout p {
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #F0F4F8;
            border-right: 1px solid #E0E6ED;
        }

        .filter-summary-box {
            background-color: #FFFFFF;
            border: 1px solid #D0D7DE;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 0.85rem;
            line-height: 1.5;
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    """
    Renders the app title, metadata badges, CDC attribution, provisional status warning,
    and pedagogical alert clarifying birth counts vs. birth rates.
    """
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
            <div>
                <h1 style="margin: 0; font-size: 2.2rem; color: #1A237E; font-weight: 800;">
                    👶 Provisional 2025 CDC U.S. Birth Counts Dashboard
                </h1>
                <p style="margin: 0.4rem 0 0.8rem 0; font-size: 1.05rem; color: #424242;">
                    An interactive exploratory analytics dashboard for analyzing geographic, seasonal, and demographic birth count patterns across the United States.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("""
            <div class="badge-provisional">
                ⚠️ NOTICE: Provisional Data | 2025 CDC Natality Records
            </div>
            <div style="font-size: 0.85rem; color: #616161; margin-bottom: 0.5rem;">
                <b>Source Attribution:</b> CDC National Center for Health Statistics (NCHS) – National Vital Statistics System (NVSS).
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
            <div class="pedagogical-callout">
                <h4>📊 Analytical Note for Students</h4>
                <p>
                    All metrics presented are <b>raw live birth counts</b>, not birth rates per capita. 
                    This dataset contains no population denominators, so population-based rate calculations cannot be derived.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")


def render_kpi_cards(filtered_df: pd.DataFrame, full_df: pd.DataFrame):
    """
    Renders 5 formatted KPI summary cards based on the active selection.
    """
    if filtered_df.empty:
        st.warning("⚠️ No observations match the current filter selection.")
        return

    total_births = int(filtered_df["Births"].sum())
    num_states = filtered_df["State of Residence"].nunique()
    num_months = filtered_df["Month"].nunique()

    # Calculate average births per selected month
    monthly_totals = filtered_df.groupby("Month", observed=False)["Births"].sum()
    avg_monthly_births = float(monthly_totals.mean()) if not monthly_totals.empty else 0.0

    # Identify top geography
    state_totals = filtered_df.groupby("State of Residence", as_index=False)["Births"].sum()
    if not state_totals.empty:
        top_state_row = state_totals.sort_values(by="Births", ascending=False).iloc[0]
        top_state_name = top_state_row["State of Residence"]
        top_state_count = int(top_state_row["Births"])
    else:
        top_state_name, top_state_count = "N/A", 0

    # Identify top month
    month_totals = filtered_df.groupby("Month", as_index=False, observed=False)["Births"].sum()
    if not month_totals.empty:
        top_month_row = month_totals.sort_values(by="Births", ascending=False).iloc[0]
        top_month_name = str(top_month_row["Month"])
        top_month_count = int(top_month_row["Births"])
    else:
        top_month_name, top_month_count = "N/A", 0

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Births",
            value=f"{total_births:,}",
            help="Total sum of provisional live birth counts in current selection."
        )

    with col2:
        st.metric(
            label="Selected Geographies",
            value=f"{num_states} / 51",
            help="Number of U.S. states / DC included in active filter."
        )

    with col3:
        st.metric(
            label="Avg Monthly Births",
            value=f"{avg_monthly_births:,.0f}",
            help="Average birth count per active selected month."
        )

    with col4:
        st.metric(
            label="Top Geography",
            value=top_state_name,
            delta=f"{top_state_count:,} births",
            delta_color="off",
            help="State with the highest birth count in active selection."
        )

    with col5:
        st.metric(
            label="Peak Month",
            value=top_month_name,
            delta=f"{top_month_count:,} births",
            delta_color="off",
            help="Month with highest birth count in active selection."
        )

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)


def render_sidebar_filters(df: pd.DataFrame):
    """
    Renders sidebar multiselects, toggles, reset button, and active filter readout.

    Returns:
        tuple: (selected_states, selected_months, selected_sex)
    """
    st.sidebar.header("🔍 Dashboard Filters")
    st.sidebar.markdown("Filter provisional birth observations across dimensions.")

    all_states = sorted(df["State of Residence"].unique().tolist())
    all_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    sex_options = ["All", "Female", "Male"]

    # Initialize Session State default values
    if "selected_states" not in st.session_state:
        st.session_state.selected_states = all_states.copy()
    if "selected_months" not in st.session_state:
        st.session_state.selected_months = all_months.copy()
    if "selected_sex" not in st.session_state:
        st.session_state.selected_sex = "All"

    # --- Reset Button ---
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state.selected_states = all_states.copy()
        st.session_state.selected_months = all_months.copy()
        st.session_state.selected_sex = "All"
        st.rerun()

    st.sidebar.markdown("---")

    # --- State Filter & Select All ---
    st.sidebar.subheader("1. Geography")
    c_st1, c_st2 = st.sidebar.columns(2)
    if c_st1.button("Select All States", key="btn_all_states", use_container_width=True):
        st.session_state.selected_states = all_states.copy()
        st.rerun()
    if c_st2.button("Clear States", key="btn_clear_states", use_container_width=True):
        st.session_state.selected_states = []
        st.rerun()

    selected_states = st.sidebar.multiselect(
        "Select State(s) / Geography:",
        options=all_states,
        default=st.session_state.selected_states,
        key="ms_states"
    )

    st.sidebar.markdown("---")

    # --- Month Filter & Select All ---
    st.sidebar.subheader("2. Calendar Month")
    c_m1, c_m2 = st.sidebar.columns(2)
    if c_m1.button("Select All Months", key="btn_all_months", use_container_width=True):
        st.session_state.selected_months = all_months.copy()
        st.rerun()
    if c_m2.button("Clear Months", key="btn_clear_months", use_container_width=True):
        st.session_state.selected_months = []
        st.rerun()

    selected_months = st.sidebar.multiselect(
        "Select Month(s):",
        options=all_months,
        default=st.session_state.selected_months,
        key="ms_months"
    )

    st.sidebar.markdown("---")

    # --- Infant Sex Filter ---
    st.sidebar.subheader("3. Infant Sex")
    selected_sex = st.sidebar.radio(
        "Select Infant Sex:",
        options=sex_options,
        index=sex_options.index(st.session_state.selected_sex),
        key="rad_sex",
        horizontal=True
    )

    st.sidebar.markdown("---")

    # --- Active Filter Summary Readout ---
    st.sidebar.subheader("📋 Active Filter Summary")
    num_st_sel = len(selected_states)
    num_mo_sel = len(selected_months)

    summary_html = f"""
    <div class="filter-summary-box">
        <b>Selected Geographies:</b> {num_st_sel} of 51<br>
        <b>Selected Months:</b> {num_mo_sel} of 12<br>
        <b>Infant Sex:</b> {selected_sex}<br>
        <hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #E0E0E0;">
        <span style="color: {'#2E7D32' if (num_st_sel > 0 and num_mo_sel > 0) else '#C62828'}; font-weight: 600;">
            {'✅ Active Data View' if (num_st_sel > 0 and num_mo_sel > 0) else '⚠️ No Selection (0 Rows)'}
        </span>
    </div>
    """
    st.sidebar.markdown(summary_html, unsafe_allow_html=True)

    return selected_states, selected_months, selected_sex


def render_about_section(full_df: pd.DataFrame):
    """
    Renders educational documentation and dataset background for students.
    """
    st.markdown("## 📚 About the Provisional 2025 CDC Natality Dataset")

    st.markdown("""
    ### 1. Pedagogical Overview & Business Analytics Objectives
    This application is designed for **undergraduate business analytics students** exploring public health dataset structures, data auditing workflows, and exploratory data analysis (EDA).
    
    When working with real-world public data, analytics professionals must evaluate dataset boundaries before constructing metrics or drawing business conclusions.
    """)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        #### 📌 Key Concept: Birth Counts vs. Birth Rates
        * **Birth Counts (Numerator)**: The absolute number of live births registered within a specific state, month, and infant sex category.
        * **Birth Rates (Per Capita / Per 1,000 Population)**: A relative statistical rate computed as:
          $$\\text{Birth Rate} = \\left( \\frac{\\text{Total Births}}{\\text{Total Female Population Aged 15--44}} \\right) \\times 1,000$$
        
        > **Critical Audit Rule**: The provisional CDC table provided in this project **does not contain population denominator data**. Therefore, attempting to calculate demographic birth rates without true census denominators is statistically invalid. We analyze birth counts directly.
        """)

    with col_b:
        st.markdown("""
        #### 🔍 Summary of Dataset Audit Verification
        Before visualization, automated verification assertions confirmed dataset integrity:
        * **Total Observations**: 1,224 rows (51 geographies × 12 months × 2 sexes = 1,224 exact grid rows).
        * **Total Provisional Live Births**: **3,604,640 births** nationwide in 2025.
        * **Geographies**: 50 U.S. states + District of Columbia.
        * **Missing Values**: 0 nulls or missing fields.
        * **Duplicate Rows**: 0 duplicate records.
        """)

    st.markdown("---")

    st.markdown("""
    ### 2. Dataset Structure Reference
    Below is the verified schema definition for `data/Provisional_Natality_2025_CDC.xlsx`:
    """)

    schema_data = {
        "Column Name": ["State of Residence", "Month", "Month Code", "Year Code", "Sex of Infant", "Births", "State Code"],
        "Data Type": ["String / Object", "Categorical String", "Integer (1..12)", "Integer (2025)", "String (Female/Male)", "Integer Count", "String Code"],
        "Sample Value": ["California", "January", "1", "2025", "Male", "17627", "CA"],
        "Description": ["State or district of mother's residence", "Calendar month name", "Numeric month index for sorting", "Reporting year code", "Sex of newborn infant", "Provisional count of live births", "2-letter postal code for geospatial map"]
    }
    st.table(pd.DataFrame(schema_data))

    st.markdown("""
    ### 3. Data Source Attribution
    Data provided by the **Centers for Disease Control and Prevention (CDC)**, National Center for Health Statistics (NCHS), National Vital Statistics System (NVSS) Provisional Natality Data for 2025.
    """)
