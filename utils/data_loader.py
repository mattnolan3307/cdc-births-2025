from pathlib import Path
import pandas as pd
import streamlit as st

# Standard U.S. State and District of Columbia Postal Abbreviation Mapping
STATE_TO_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
    "Wyoming": "WY"
}

# Month names sorted chronologically by Month Code (1..12)
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Loads provisional 2025 CDC natality data from Excel, performs data quality checks,
    and maps state abbreviations for geospatial rendering.
    
    Returns:
        pd.DataFrame: Cleaned and validated dataset with categorical month ordering and state codes.
    """
    # Build path relative to repository root to support both local execution and Streamlit Cloud
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "Provisional_Natality_2025_CDC.xlsx"
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at path: {data_path}")

    # Read dataset from Excel
    df = pd.read_excel(data_path)

    # --- Data Integrity & Audit Checks ---
    assert len(df) == 1224, f"Expected 1,224 observations, got {len(df)}"
    assert df["State of Residence"].nunique() == 51, f"Expected 51 geographies, got {df['State of Residence'].nunique()}"
    assert df["Month Code"].nunique() == 12, f"Expected 12 months, got {df['Month Code'].nunique()}"
    assert df["Sex of Infant"].nunique() == 2, f"Expected 2 sex categories, got {df['Sex of Infant'].nunique()}"
    assert df.isnull().sum().sum() == 0, "Found unexpected missing values in dataset"
    assert df["Births"].sum() == 3604640, f"Expected 3,604,640 total births, got {df['Births'].sum()}"

    # Map two-letter state abbreviations for Plotly choropleth mapping
    df["State Code"] = df["State of Residence"].map(STATE_TO_ABBR)
    
    # Ensure categorical month ordering strictly follows calendar sequence (Month Code 1..12)
    df["Month"] = pd.Categorical(df["Month"], categories=MONTH_ORDER, ordered=True)

    return df


def filter_data(
    df: pd.DataFrame,
    selected_states: list[str],
    selected_months: list[str],
    selected_sex: str
) -> pd.DataFrame:
    """
    Filters the dataset based on user selections in the Streamlit sidebar.

    Args:
        df (pd.DataFrame): Full validated dataset.
        selected_states (list[str]): List of state names selected by the user.
        selected_months (list[str]): List of month names selected by the user.
        selected_sex (str): Infant sex filter ('All', 'Female', or 'Male').

    Returns:
        pd.DataFrame: Filtered subset of observations.
    """
    filtered_df = df.copy()

    if selected_states is not None:
        filtered_df = filtered_df[filtered_df["State of Residence"].isin(selected_states)]

    if selected_months is not None:
        filtered_df = filtered_df[filtered_df["Month"].isin(selected_months)]

    if selected_sex and selected_sex != "All":
        filtered_df = filtered_df[filtered_df["Sex of Infant"] == selected_sex]

    return filtered_df

