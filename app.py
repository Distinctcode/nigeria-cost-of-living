
# ============================================================
# NIGERIA SELECTED FOOD PRICES DASHBOARD
# ============================================================
# This application explores selected food prices across
# Nigeria's six geopolitical zones.
#
# Tools:
# - Streamlit: dashboard and interactive controls
# - Pandas: data processing
# - Plotly: interactive charts
#
# IMPORTANT:
# This project analyses selected food prices. It does not
# measure every component of Nigeria's cost of living.
# ============================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Nigeria Food Prices Dashboard",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# 2. PROJECT PATHS
# ------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

DATA_DIR = PROJECT_DIR / "data" / "processed"


# ------------------------------------------------------------
# 3. LOAD THE CLEANED DATA
# ------------------------------------------------------------

@st.cache_data
def load_data():
    """Load the three prepared CSV datasets."""

    food_file = DATA_DIR / "food_prices_cleaned.csv"
    regional_file = DATA_DIR / "regional_prices_cleaned.csv"
    variability_file = DATA_DIR / "regional_variability.csv"

    required_files = [
        food_file,
        regional_file,
        variability_file,
    ]

    missing_files = [
        file.name
        for file in required_files
        if not file.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing required data files: "
            + ", ".join(missing_files)
        )

    food = pd.read_csv(food_file)
    regional = pd.read_csv(regional_file)
    variability = pd.read_csv(variability_file)

    return food, regional, variability


try:
    food_data, regional_data, variability_data = load_data()

except (FileNotFoundError, pd.errors.ParserError, OSError) as error:
    st.error("The dashboard could not load its data.")
    st.code(str(error))
    st.info(
        "Check that all three CSV files are saved in "
        "data/processed."
    )
    st.stop()


# ------------------------------------------------------------
# 4. DEFINE THE REGIONAL COLUMNS
# ------------------------------------------------------------

REGIONAL_COLUMNS = [
    "NORTH CENTRAL",
    "NORTH EAST",
    "NORTH WEST",
    "SOUTH EAST",
    "SOUTH SOUTH",
    "SOUTH WEST",
]


# ------------------------------------------------------------
# 5. CHECK REQUIRED COLUMNS
# ------------------------------------------------------------

required_food_columns = [
    "Item Label",
    "Average of May-25",
    "Average of April-26",
    "Average of May-26",
    "MoM",
    "YoY",
]

required_regional_columns = [
    "Item Label",
    *REGIONAL_COLUMNS,
]

missing_food_columns = [
    column
    for column in required_food_columns
    if column not in food_data.columns
]

missing_regional_columns = [
    column
    for column in required_regional_columns
    if column not in regional_data.columns
]

if missing_food_columns or missing_regional_columns:
    st.error("Some required dataset columns are missing.")

    if missing_food_columns:
        st.write("Missing food-price columns:", missing_food_columns)

    if missing_regional_columns:
        st.write(
            "Missing regional columns:",
            missing_regional_columns,
        )

    st.stop()


# ------------------------------------------------------------
# 6. PREPARE NUMERIC COLUMNS
# ------------------------------------------------------------

food_data = food_data.copy()
regional_data = regional_data.copy()
variability_data = variability_data.copy()

food_numeric_columns = [
    "Average of May-25",
    "Average of April-26",
    "Average of May-26",
    "MoM",
    "YoY",
]

for column in food_numeric_columns:
    food_data[column] = pd.to_numeric(
        food_data[column],
        errors="coerce",
    )

for column in REGIONAL_COLUMNS:
    regional_data[column] = pd.to_numeric(
        regional_data[column],
        errors="coerce",
    )

for column in [
    "Average Regional Price",
    "Regional Price Std Dev",
    "Regional Price Range",
    "Price CV (%)",
]:
    if column in variability_data.columns:
        variability_data[column] = pd.to_numeric(
            variability_data[column],
            errors="coerce",
        )


# ------------------------------------------------------------
# 7. DASHBOARD HEADER
# ------------------------------------------------------------

st.title("🇳🇬 Nigeria Selected Food Prices Dashboard")

st.markdown(
    """
    Explore selected food prices, changes across reporting periods,
    and differences among Nigeria's six geopolitical zones.
    """
)

st.caption(
    "Reporting periods: May 2025, April 2026, and May 2026."
)

st.info(
    "Scope: This dashboard analyses selected food items only. "
    "It is not a complete measure of Nigeria's cost of living. "
    "Confirm the source, currency, measurement units, and pack "
    "sizes before making direct price comparisons."
)


# ------------------------------------------------------------
# 8. SIDEBAR NAVIGATION
# ------------------------------------------------------------

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "Overview",
        "Food Price Analysis",
        "Regional Comparison",
        "Regional Variability",
        "Data Explorer",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    "Project: Nigeria Selected Food Prices Analysis"
)


# ------------------------------------------------------------
# 9. OVERVIEW PAGE
# ------------------------------------------------------------

if page == "Overview":

    st.header("Dashboard Overview")

    number_of_items = food_data["Item Label"].nunique()

    average_may_price = food_data[
        "Average of May-26"
    ].mean()

    average_mom = food_data["MoM"].mean()

    average_yoy = food_data["YoY"].mean()

    # Calculate regional averages from the regional dataset.
    regional_averages = (
        regional_data[REGIONAL_COLUMNS]
        .mean()
        .rename_axis("Geopolitical Zone")
        .reset_index(name="Average Recorded Price")
    )

    regional_averages = regional_averages.sort_values(
        "Average Recorded Price"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Selected Food Items",
        f"{number_of_items:,}",
    )

    col2.metric(
        "Geopolitical Zones",
        "6",
    )

    col3.metric(
        "Average May 2026 Price",
        f"{average_may_price:,.2f}",
    )

    col4.metric(
        "Average Monthly Change",
        f"{average_mom:+.2f}%",
    )

    st.metric(
        "Average Year-on-Year Change",
        f"{average_yoy:+.2f}%",
    )

    st.divider()

    # Top five recorded food prices.
    st.subheader("Five Most Expensive Selected Food Items")

    expensive_items = (
        food_data[["Item Label", "Average of May-26"]]
        .dropna()
        .nlargest(5, "Average of May-26")
        .sort_values("Average of May-26")
    )

    figure = px.bar(
        expensive_items,
        x="Average of May-26",
        y="Item Label",
        orientation="h",
        text="Average of May-26",
        labels={
            "Average of May-26": "Recorded price",
            "Item Label": "Food item",
        },
        template="plotly_white",
    )

    figure.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    st.plotly_chart(figure, use_container_width=True)

    # Average price by region.
    st.subheader("Average Recorded Price by Geopolitical Zone")

    figure = px.bar(
        regional_averages,
        x="Geopolitical Zone",
        y="Average Recorded Price",
        text="Average Recorded Price",
        labels={
            "Geopolitical Zone": "Geopolitical zone",
            "Average Recorded Price": "Average recorded price",
        },
        template="plotly_white",
    )

    figure.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    st.plotly_chart(figure, use_container_width=True)

    highest_zone = regional_averages.iloc[-1]
    lowest_zone = regional_averages.iloc[0]

    st.subheader("Key Finding")

    st.write(
        f"The highest average recorded regional price was in "
        f"{highest_zone['Geopolitical Zone']} "
        f"({highest_zone['Average Recorded Price']:,.2f}), "
        f"while the lowest was in "
        f"{lowest_zone['Geopolitical Zone']} "
        f"({lowest_zone['Average Recorded Price']:,.2f})."
    )


# ------------------------------------------------------------
# 10. FOOD PRICE ANALYSIS PAGE
# ------------------------------------------------------------

elif page == "Food Price Analysis":

    st.header("Food Price Analysis")

    st.write(
        "Compare recorded prices and percentage changes "
        "for individual food items."
    )

    available_items = sorted(
        food_data["Item Label"].dropna().unique().tolist()
    )

    selected_items = st.multiselect(
        "Select food items to compare:",
        options=available_items,
        default=available_items[:5],
    )

    period_columns = {
        "May 2025": "Average of May-25",
        "April 2026": "Average of April-26",
        "May 2026": "Average of May-26",
    }

    selected_periods = st.multiselect(
        "Select reporting periods:",
        options=list(period_columns.keys()),
        default=list(period_columns.keys()),
    )

    if selected_items and selected_periods:

        selected_data = food_data[
            food_data["Item Label"].isin(selected_items)
        ][["Item Label"] + [
            period_columns[period]
            for period in selected_periods
        ]]

        long_data = selected_data.melt(
            id_vars="Item Label",
            var_name="Reporting Period",
            value_name="Recorded Price",
        )

        reverse_period_names = {
            value: key
            for key, value in period_columns.items()
        }

        long_data["Reporting Period"] = (
            long_data["Reporting Period"].map(
                reverse_period_names
            )
        )

        figure = px.bar(
            long_data,
            x="Item Label",
            y="Recorded Price",
            color="Reporting Period",
            barmode="group",
            title="Selected Food Prices Across Reporting Periods",
            template="plotly_white",
        )

        figure.update_layout(
            xaxis_title="Food item",
            yaxis_title="Recorded price",
            xaxis_tickangle=-35,
        )

        st.plotly_chart(figure, use_container_width=True)

        st.subheader("Month-on-Month and Year-on-Year Changes")

        change_data = food_data[
            food_data["Item Label"].isin(selected_items)
        ][["Item Label", "MoM", "YoY"]]

        st.dataframe(
            change_data,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.warning(
            "Select at least one food item and one reporting period."
        )

    st.subheader("Largest Monthly Price Increases")

    top_monthly = (
        food_data[["Item Label", "MoM"]]
        .dropna()
        .nlargest(10, "MoM")
    )

    st.dataframe(
        top_monthly,
        use_container_width=True,
        hide_index=True,
    )


# ------------------------------------------------------------
# 11. REGIONAL COMPARISON PAGE
# ------------------------------------------------------------

elif page == "Regional Comparison":

    st.header("Regional Price Comparison")

    st.write(
        "Compare the recorded prices of selected food items "
        "across Nigeria's six geopolitical zones."
    )

    available_items = sorted(
        regional_data["Item Label"].dropna().unique().tolist()
    )

    selected_items = st.multiselect(
        "Select food items:",
        options=available_items,
        default=available_items[:5],
        key="regional_items",
    )

    if selected_items:

        selected_data = regional_data[
            regional_data["Item Label"].isin(selected_items)
        ]

        long_data = selected_data.melt(
            id_vars="Item Label",
            value_vars=REGIONAL_COLUMNS,
            var_name="Geopolitical Zone",
            value_name="Recorded Price",
        )

        figure = px.bar(
            long_data,
            x="Item Label",
            y="Recorded Price",
            color="Geopolitical Zone",
            barmode="group",
            title="Food Prices Across Geopolitical Zones",
            template="plotly_white",
        )

        figure.update_layout(
            xaxis_title="Food item",
            yaxis_title="Recorded price",
            xaxis_tickangle=-35,
        )

        st.plotly_chart(figure, use_container_width=True)

        st.subheader("Regional Price Table")

        st.dataframe(
            selected_data,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.warning("Select at least one food item.")

    st.subheader("Regional Average Rankings")

    zone_summary = (
        regional_data[REGIONAL_COLUMNS]
        .mean()
        .rename_axis("Geopolitical Zone")
        .reset_index(name="Average Recorded Price")
        .sort_values(
            "Average Recorded Price",
            ascending=False,
        )
    )

    st.dataframe(
        zone_summary,
        use_container_width=True,
        hide_index=True,
    )


# ------------------------------------------------------------
# 12. REGIONAL VARIABILITY PAGE
# ------------------------------------------------------------

elif page == "Regional Variability":

    st.header("Regional Price Variability")

    st.write(
        "Explore how much recorded food prices differ "
        "across the six geopolitical zones."
    )

    required_variability_columns = [
        "Item Label",
        "Average Regional Price",
        "Regional Price Range",
        "Price CV (%)",
    ]

    missing_variability_columns = [
        column
        for column in required_variability_columns
        if column not in variability_data.columns
    ]

    if missing_variability_columns:

        st.error(
            "The regional variability dataset is missing "
            "required columns."
        )

        st.write(missing_variability_columns)

    else:

        variability_measure = st.selectbox(
            "Choose a variability measure:",
            [
                "Regional Price Range",
                "Price CV (%)",
            ],
        )

        chart_data = (
            variability_data[
                [
                    "Item Label",
                    "Average Regional Price",
                    "Regional Price Range",
                    "Price CV (%)",
                ]
            ]
            .dropna(subset=[variability_measure])
        )

        largest_variability = chart_data.nlargest(
            10,
            variability_measure,
        ).sort_values(variability_measure)

        figure = px.bar(
            largest_variability,
            x=variability_measure,
            y="Item Label",
            orientation="h",
            text=variability_measure,
            title=f"10 Items with the Largest {variability_measure}",
            template="plotly_white",
        )

        figure.update_traces(
            textposition="outside",
            cliponaxis=False,
        )

        st.plotly_chart(figure, use_container_width=True)

        st.subheader("Items with the Smallest Variability")

        smallest_variability = (
            chart_data.nsmallest(10, variability_measure)
        )

        st.dataframe(
            smallest_variability,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Complete Regional Variability Table")

        st.dataframe(
            chart_data.sort_values(
                variability_measure,
                ascending=False,
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Regional Price Range measures the absolute difference "
            "between the highest and lowest recorded regional prices. "
            "Price CV (%) measures standard deviation relative to "
            "average regional price."
        )


# ------------------------------------------------------------
# 13. DATA EXPLORER PAGE
# ------------------------------------------------------------

elif page == "Data Explorer":

    st.header("Data Explorer")

    st.write(
        "Search the cleaned datasets, inspect records, "
        "and download data for further analysis."
    )

    dataset_choice = st.selectbox(
        "Choose a dataset:",
        [
            "Food Prices",
            "Regional Prices",
            "Regional Variability",
        ],
    )

    if dataset_choice == "Food Prices":
        selected_data = food_data.copy()
        download_name = "food_prices_cleaned.csv"

    elif dataset_choice == "Regional Prices":
        selected_data = regional_data.copy()
        download_name = "regional_prices_cleaned.csv"

    else:
        selected_data = variability_data.copy()
        download_name = "regional_variability.csv"

    # Optional food-item search.
    search_text = st.text_input(
        "Search by food-item name:",
        placeholder="For example, beans or tomatoes",
    )

    if search_text and "Item Label" in selected_data.columns:

        selected_data = selected_data[
            selected_data["Item Label"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False,
            )
        ]

    st.write(
        f"Records displayed: {len(selected_data):,}"
    )

    st.dataframe(
        selected_data,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = selected_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Selected Data as CSV",
        data=csv_data,
        file_name=download_name,
        mime="text/csv",
    )


# ------------------------------------------------------------
# 14. FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Nigeria Selected Food Prices Dashboard | "
    "Python, Pandas, Plotly, and Streamlit"
)
