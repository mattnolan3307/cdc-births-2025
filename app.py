import streamlit as st
import pandas as pd

from utils.data_loader import load_data, filter_data
from utils.ui import (
    inject_custom_css,
    render_header,
    render_kpi_cards,
    render_sidebar_filters,
    render_about_section
)
from utils.charts import (
    build_choropleth_map,
    build_monthly_trend,
    build_monthly_sex_trend,
    build_sex_comparison_donut,
    build_state_ranking,
    build_state_month_heatmap,
    build_top_bottom_comparison
)

# Set page layout configuration
st.set_page_config(
    page_title="Provisional 2025 CDC U.S. Birth Counts Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    # 1. Inject CSS styling
    inject_custom_css()

    # 2. Load dataset with caching and automated validation assertions
    try:
        df_full = load_data()
    except Exception as e:
        st.error(f"❌ Critical Error loading dataset: {e}")
        st.stop()

    # 3. Render Header
    render_header()

    # 4. Render Sidebar Filters
    selected_states, selected_months, selected_sex = render_sidebar_filters(df_full)

    # 5. Apply Active Filters
    filtered_df = filter_data(df_full, selected_states, selected_months, selected_sex)

    # 6. Render KPI Cards
    render_kpi_cards(filtered_df, df_full)

    # 7. Check Empty Filter Edge Case
    if filtered_df.empty:
        st.warning(
            "⚠️ **No data matches your active filter selection.** "
            "Please adjust the geography or month filters in the sidebar, or click **'Reset All Filters'**."
        )
        st.stop()

    # 8. Render Main Tabs
    tab_overview, tab_geo, tab_monthly, tab_data, tab_about = st.tabs([
        "📊 Overview",
        "🗺️ Geographic Analysis",
        "📈 Monthly & Sex Analysis",
        "📄 Data Table & Download",
        "📚 About the Data"
    ])

    # --- TAB 1: OVERVIEW ---
    with tab_overview:
        st.markdown("### 📌 Executive Summary & High-Level Patterns")
        st.markdown(
            "Explore national monthly trends, infant sex proportions, and extreme volume geographic contrasts."
        )

        col_left, col_right = st.columns([3, 2])
        with col_left:
            fig_trend = build_monthly_trend(filtered_df)
            st.plotly_chart(fig_trend, use_container_width=True)

        with col_right:
            fig_sex = build_sex_comparison_donut(filtered_df)
            st.plotly_chart(fig_sex, use_container_width=True)

        st.markdown("---")
        fig_comp = build_top_bottom_comparison(filtered_df)
        st.plotly_chart(fig_comp, use_container_width=True)

    # --- TAB 2: GEOGRAPHIC ANALYSIS ---
    with tab_geo:
        st.markdown("### 🗺️ U.S. Geographic Distribution & State Rankings")
        st.markdown(
            "Visualize live birth counts across all 50 U.S. states and the District of Columbia. "
            "Click or hover on map regions for detailed counts."
        )

        fig_map = build_choropleth_map(filtered_df)
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("---")
        col_rank1, col_rank2 = st.columns([3, 1])
        with col_rank2:
            top_n_slider = st.slider(
                "Select Top N Geographies to Display:",
                min_value=5,
                max_value=51,
                value=20,
                step=5
            )
            st.info(
                "💡 **Student Tip**: State birth counts reflect total state population sizes. "
                "Larger states like California, Texas, and Florida naturally register higher total birth counts."
            )

        with col_rank1:
            fig_rank = build_state_ranking(filtered_df, top_n=top_n_slider)
            st.plotly_chart(fig_rank, use_container_width=True)

    # --- TAB 3: MONTHLY & SEX ANALYSIS ---
    with tab_monthly:
        st.markdown("### 📈 Monthly Trends & Infant Sex Breakdown")
        st.markdown(
            "Analyze seasonal birth volume fluctuations and inspect infant sex breakdowns month-by-month."
        )

        fig_monthly_sex = build_monthly_sex_trend(filtered_df)
        st.plotly_chart(fig_monthly_sex, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🌡️ Geography-by-Month Birth Density Matrix")
        st.markdown(
            "Heatmap visualization of birth count density across states and calendar months. "
            "Darker shades indicate higher birth volumes."
        )
        fig_heatmap = build_state_month_heatmap(filtered_df)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # --- TAB 4: DATA TABLE & DOWNLOAD ---
    with tab_data:
        st.markdown("### 📄 Filtered Data Table & Export")
        st.markdown(
            "Inspect filtered micro-data rows, search across fields, and export custom subsets to CSV."
        )

        st.markdown(f"**Showing `{len(filtered_df):,}` observations matching active filters:**")

        # Format numeric display for interactive dataframe
        display_df = filtered_df.copy()
        display_df = display_df[[
            "State of Residence", "State Code", "Year Code",
            "Month", "Month Code", "Sex of Infant", "Births"
        ]]

        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "Births": st.column_config.NumberColumn(
                    "Live Birth Count",
                    format="%d"
                ),
                "Month Code": st.column_config.NumberColumn(
                    "Month #",
                    format="%d"
                ),
                "Year Code": st.column_config.NumberColumn(
                    "Year",
                    format="%d"
                )
            },
            hide_index=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        csv_bytes = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_bytes,
            file_name="provisional_2025_cdc_birth_counts_filtered.csv",
            mime="text/csv",
            type="primary"
        )

    # --- TAB 5: ABOUT THE DATA ---
    with tab_about:
        render_about_section(df_full)


if __name__ == "__main__":
    main()
