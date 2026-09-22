import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Color palette definition for accessible, high-contrast visualization
COLOR_FEMALE = "#008080"  # Teal
COLOR_MALE = "#3F51B5"    # Indigo
COLOR_PRIMARY = "#1E88E5" # Accessible Blue
COLOR_SCALE_MAP = "Blues" # Choropleth map color ramp


def build_choropleth_map(df: pd.DataFrame) -> go.Figure:
    """
    Constructs an interactive U.S. state choropleth map showing total birth counts by state.
    """
    if df.empty:
        return go.Figure()

    state_df = (
        df.groupby(["State of Residence", "State Code"], as_index=False)["Births"]
        .sum()
        .sort_values(by="Births", ascending=False)
    )

    fig = px.choropleth(
        state_df,
        locations="State Code",
        locationmode="USA-states",
        color="Births",
        scope="usa",
        color_continuous_scale=COLOR_SCALE_MAP,
        labels={"Births": "Live Births"},
        hover_name="State of Residence",
    )

    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b> (%{location})<br>Total Live Births: <b>%{z:,}</b><extra></extra>"
    )

    fig.update_layout(
        title={
            "text": "<b>U.S. Geographic Distribution of Provisional 2025 Live Birth Counts</b>",
            "x": 0.0,
            "xanchor": "left"
        },
        margin={"r": 10, "t": 40, "l": 10, "b": 10},
        geo=dict(lakecolor="rgb(255, 255, 255)"),
        coloraxis_colorbar=dict(
            title="Birth Count",
            tickformat=","
        ),
        template="plotly_white",
        height=500
    )

    return fig


def build_monthly_trend(df: pd.DataFrame) -> go.Figure:
    """
    Constructs a monthly birth trend line chart ordered chronologically (Month Code 1..12).
    """
    if df.empty:
        return go.Figure()

    monthly_df = (
        df.groupby(["Month Code", "Month"], as_index=False, observed=True)["Births"]
        .sum()
        .sort_values(by="Month Code")
    )


    fig = px.line(
        monthly_df,
        x="Month",
        y="Births",
        markers=True,
        labels={"Month": "Calendar Month", "Births": "Total Live Births"},
    )

    fig.update_traces(
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=8, color=COLOR_PRIMARY),
        hovertemplate="<b>%{x}</b><br>Total Live Births: <b>%{y:,}</b><extra></extra>"
    )

    fig.update_layout(
        title={
            "text": "<b>Monthly Live Birth Count Trend (2025 Provisional)</b>",
            "x": 0.0,
            "xanchor": "left"
        },
        xaxis=dict(title="", showgrid=True),
        yaxis=dict(
            title="Live Birth Count",
            tickformat=",",
            rangemode="tozero",  # Preserves zero baseline to avoid misleading truncated axes
            showgrid=True
        ),
        template="plotly_white",
        height=400
    )

    return fig


def build_monthly_sex_trend(df: pd.DataFrame) -> go.Figure:
    """
    Constructs a grouped line chart comparing monthly birth trends by infant sex.
    """
    if df.empty:
        return go.Figure()

    monthly_sex_df = (
        df.groupby(["Month Code", "Month", "Sex of Infant"], as_index=False, observed=True)["Births"]
        .sum()
        .sort_values(by=["Month Code", "Sex of Infant"])
    )

    fig = px.line(
        monthly_sex_df,
        x="Month",
        y="Births",
        color="Sex of Infant",
        markers=True,
        color_discrete_map={"Female": COLOR_FEMALE, "Male": COLOR_MALE},
        labels={"Month": "Calendar Month", "Births": "Live Births", "Sex of Infant": "Infant Sex"}
    )

    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=7),
        hovertemplate="<b>%{x}</b> (%{fullData.name})<br>Live Births: <b>%{y:,}</b><extra></extra>"
    )

    fig.update_layout(
        title={
            "text": "<b>Monthly Live Birth Counts by Infant Sex</b>",
            "x": 0.0,
            "xanchor": "left"
        },
        xaxis=dict(title=""),
        yaxis=dict(
            title="Live Birth Count",
            tickformat=",",
            rangemode="tozero"
        ),
        legend=dict(title="Infant Sex", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=420
    )

    return fig


def build_sex_comparison_donut(df: pd.DataFrame) -> go.Figure:
    """
    Constructs a donut chart showing national or selected female vs. male birth proportions.
    """
    if df.empty:
        return go.Figure()

    sex_df = df.groupby("Sex of Infant", as_index=False)["Births"].sum()

    fig = px.pie(
        sex_df,
        names="Sex of Infant",
        values="Births",
        hole=0.45,
        color="Sex of Infant",
        color_discrete_map={"Female": COLOR_FEMALE, "Male": COLOR_MALE}
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Birth Count: <b>%{value:,}</b><br>Share: <b>%{percent}</b><extra></extra>"
    )

    fig.update_layout(
        title={
            "text": "<b>Infant Sex Distribution (Birth Counts & Shares)</b>",
            "x": 0.0,
            "xanchor": "left"
        },
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        template="plotly_white",
        height=380
    )

    return fig


def build_state_ranking(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """
    Constructs a horizontal bar chart ranking geographies by birth count.
    """
    if df.empty:
        return go.Figure()

    state_df = (
        df.groupby("State of Residence", as_index=False)["Births"]
        .sum()
        .sort_values(by="Births", ascending=True)  # Ascending for horizontal bar rendering top at top
    )

    if len(state_df) > top_n:
        state_df = state_df.tail(top_n)

    fig = px.bar(
        state_df,
        x="Births",
        y="State of Residence",
        orientation="h",
        text_auto=",.0f",
        labels={"Births": "Total Live Births", "State of Residence": "Geography"}
    )

    fig.update_traces(
        marker_color=COLOR_PRIMARY,
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Live Births: <b>%{x:,}</b><extra></extra>"
    )

    fig.update_layout(
        title={
            "text": f"<b>Top {len(state_df)} Geographies by Total Live Birth Count</b>",
            "x": 0.0,
            "xanchor": "left"
        },
        xaxis=dict(
            title="Total Live Birth Count",
            tickformat=",",
            rangemode="tozero"
        ),
        yaxis=dict(title=""),
        template="plotly_white",
        height=max(400, len(state_df) * 24)
    )

    return fig


def build_state_month_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Constructs a state-by-month heatmap matrix of birth count density.
    """
    if df.empty:
        return go.Figure()

    pivot_df = df.pivot_table(
        index="State of Residence",
        columns="Month",
        values="Births",
        aggfunc="sum",
        observed=True
    ).fillna(0)

    fig = px.imshow(
        pivot_df,
        labels=dict(x="Calendar Month", y="Geography", color="Birth Count"),
        color_continuous_scale="YlGnBu",
        aspect="auto"
    )

    fig.update_traces(
        hovertemplate="Geography: <b>%{y}</b><br>Month: <b>%{x}</b><br>Births: <b>%{z:,}</b><extra></extra>"
    )

    fig.update_layout(
        title={
            "text": "<b>Geography-by-Month Birth Count Density Matrix</b>",
            "x": 0.0,
            "xanchor": "left"
        },
        coloraxis_colorbar=dict(title="Birth Count", tickformat=","),
        template="plotly_white",
        height=max(500, len(pivot_df) * 18)
    )

    return fig


def build_top_bottom_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Constructs a comparative visual contrasting the top 5 highest birth geographies
    against the bottom 5 lowest birth geographies to highlight geographic scale variance.
    """
    if df.empty:
        return go.Figure()

    state_totals = (
        df.groupby("State of Residence", as_index=False)["Births"]
        .sum()
        .sort_values(by="Births", ascending=False)
    )

    if len(state_totals) <= 10:
        comp_df = state_totals
    else:
        top_5 = state_totals.head(5).copy()
        top_5["Group"] = "Top 5 (Highest Volume)"
        bottom_5 = state_totals.tail(5).copy()
        bottom_5["Group"] = "Bottom 5 (Lowest Volume)"
        comp_df = pd.concat([top_5, bottom_5])

    fig = px.bar(
        comp_df,
        x="State of Residence",
        y="Births",
        color="Group",
        color_discrete_map={
            "Top 5 (Highest Volume)": COLOR_PRIMARY,
            "Bottom 5 (Lowest Volume)": "#E53935"  # Soft crimson accent
        },
        text_auto=",.0f",
        labels={"State of Residence": "Geography", "Births": "Total Live Births"}
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Total Live Births: <b>%{y:,}</b><extra></extra>"
    )

    fig.update_layout(
        title={
            "text": "<b>Geographic Scale Comparison: Top 5 vs. Bottom 5 Birth Volume Geographies</b>",
            "x": 0.0,
            "xanchor": "left"
        },
        xaxis=dict(title=""),
        yaxis=dict(
            title="Total Live Birth Count",
            tickformat=",",
            rangemode="tozero"
        ),
        legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=450
    )

    return fig
