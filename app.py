import sys

sys.path.append("..")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import streamlit as st
from PIL import Image

import utils
import plots
from utils import get_plot
import text

# Get Dataset
countries_data, continents_data = utils.getDataset()
countries_data_ = countries_data.copy()

# Use Wide Page Forma
# st.set_page_config(layout="wide")

logo = Image.open("logo.png")
st.image(
    logo,
    width=100,
)


st.title(text.Title)

st.write(text.Paragraph_1)
st.info(text.Paragraph_2)

st.header("Questions")
st.subheader(
    "We performed some EDA to gather some insights that can answer some of the questions listed below"
)
st.markdown(text.Questions)
st.success(
    "The Visualizations are organized in a way that present our findings and answers to the questions"
)


k_continents = 8
st.sidebar.subheader("Country Parameters")
COUNTRIES_SELECTED = st.sidebar.multiselect(
    "Filter/Select Countries", utils.extract_location_list(countries_data)
)

if len(COUNTRIES_SELECTED) == 0:
    countries_data = countries_data_.copy()
else:
    countries_data = countries_data_[
        countries_data_["Location"].isin(COUNTRIES_SELECTED)
    ]

k_countries = st.sidebar.slider("Number of Top countries", 5, 20, 10)

st.sidebar.subheader("Render Menu")
show_total_vaccinations = st.sidebar.checkbox("Number of Vaccinations", True)
show_vaccinations_rates = st.sidebar.checkbox("Vaccination Rates", True)
show_fully_vaccinated = st.sidebar.checkbox("Full Vaccinations")
show_one_vaccination = st.sidebar.checkbox("One Vaccination")


if show_total_vaccinations:
    st.subheader(f"Vaccinations per continent")
    st.altair_chart(
        get_plot(
            continents_data,
            "Total Vaccinations:Q",
            "Location:O",
            k_continents,
            sort_by=["Total Vaccinations"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
        ),
        use_container_width=True,
    )

    st.subheader(f"Top {k_countries} Countries where Vaccinations were administered")
    st.altair_chart(
        get_plot(
            countries_data,
            "Total Vaccinations:Q",
            "Location:O",
            k_countries,
            sort_by=["Total Vaccinations"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
        ),
        use_container_width=True,
    )

    st.subheader(f"Bottom {k_countries} Countries where Vaccinations were administered")
    st.altair_chart(
        get_plot(
            countries_data,
            "Total Vaccinations:Q",
            "Location:O",
            k_countries,
            sort_by=["Total Vaccinations"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
            ascending=True,
        ),
        use_container_width=True,
    )

if show_vaccinations_rates:
    st.subheader("Full Vaccination Rates per Continent")
    st.altair_chart(
        get_plot(
            continents_data,
            "Percentage Fully Vaccinated:Q",
            "Location:O",
            k_continents,
            sort_by=["Percentage Fully Vaccinated"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
        ),
        use_container_width=True,
    )

    continents_ = utils.extract_location_list(continents_data)[:-1]
    print(continents_)
    continent_of_choice = st.selectbox("Filter/Select Continent", continents_)
    new_countries = utils.get_countries_by_continent(
        countries_data, continent_of_choice
    )
    st.subheader(
        f"Top {k_countries} Fully Vaccinated countries in {continent_of_choice}"
    )
    st.altair_chart(
        get_plot(
            new_countries,
            "Percentage Fully Vaccinated:Q",
            "Location:O",
            k_countries,
            sort_by=["Percentage Fully Vaccinated"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
        ),
        use_container_width=True,
    )

    st.subheader(f"Full Vaccination Rates per Country - Top {k_countries}")
    st.altair_chart(
        get_plot(
            countries_data,
            "Percentage Fully Vaccinated:Q",
            "Location:O",
            k_countries,
            sort_by=["Percentage Fully Vaccinated"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
        ),
        use_container_width=True,
    )

    st.subheader(f"Full Vaccination Rates per Country - Bottom {k_countries}")
    st.altair_chart(
        get_plot(
            countries_data,
            "Percentage Fully Vaccinated:Q",
            "Location:O",
            k_countries,
            sort_by=["Percentage Fully Vaccinated"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
            ascending=True,
        ),
        use_container_width=True,
    )

if show_fully_vaccinated:
    st.subheader(f"Top {k_countries} Countries based on number of Full Vaccinations")
    st.altair_chart(
        get_plot(
            countries_data,
            "Total Vaccinations:Q",
            "Location:O",
            k_countries,
            sort_by=["Total Vaccinations"],
            plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
        ),
        use_container_width=True,
    )


st.header("Conclusion")
st.write(text.Conclusion)


with st.expander("References"):
    st.write("COVID-19 Logo obtained from https://www.un.org/en/coronavirus")

st.sidebar.markdown(text.footer, unsafe_allow_html=True)

# col1, col2 = st.columns([3, 1])

# with col1:
#     st.write("Col 1")

# col2.write("Col 2")
