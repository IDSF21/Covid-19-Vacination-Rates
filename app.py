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
from utils import get_plot, get_scatter_plot
import text

# Get Dataset
countries_data, continents_data = utils.getDataset()
countries_data_ = countries_data.copy()
vax_gni_data = utils.get_vax_and_gni_dataset()

# Use Wide Page Forma
# st.set_page_config(layout="wide")

logo = Image.open("logo.png")
world_bank_screenshot = Image.open("world_bank.png")
st.image(
    logo,
    width=100,
)


st.title(text.Title)

st.write(text.Paragraph_1)
st.image(
    world_bank_screenshot,
)
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
show_vaccination_rates_by_income_level = st.sidebar.checkbox("Country Vaccination Rates by Income Level", True)
show_vaccination_rates_by_population = st.sidebar.checkbox("Percentage Vaccinated by Population", True)


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

    st.subheader(f"Top {k_countries} Fully Vaccinated countries on the Continent")
    continents_ = [
        "Africa",
        "Asia",
        "Europe",
        "North America",
        "Oceania",
        "South America",
    ]
    continent_of_choice = st.selectbox("Choose a Continent", continents_)

    new_countries = utils.get_countries_by_continent(
        countries_data, continent_of_choice
    )
    st.markdown(
        """ 
            The bar chart below allows you view the Top-K 
            countries in one continent based on the percentage of their vaccination rates.
            
            It's interesting to note that some countries with small populations like Pitcairn and Gibraltar have Vaccination rates equal to or higher than 100%
        """
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

if show_vaccination_rates_by_income_level:
    st.subheader(f"Relationship between Vaccination Rate, GNI per capita and Income Level")
    st.altair_chart(
        get_scatter_plot(
            vax_gni_data,
            "GNI",
            "Percentage Fully Vaccinated",
            plot_type=plots.PLOT_TYPES.SCATTER_VAX_GNI,
        ),
        use_container_width=True,
    )

if show_vaccination_rates_by_population:
    st.subheader(f"Relationship between Percentage Vaccinated, Total Country Population and Income Level")
    st.altair_chart(
        get_scatter_plot(
            vax_gni_data,
            "Population",
            "Percentage Fully Vaccinated",
            plot_type=plots.PLOT_TYPES.SCATTER_POPULATION,
        ),
        use_container_width=True,
    )


st.header("Conclusion")
st.write(text.Conclusion)


with st.expander("References"):
    st.markdown(text.References, unsafe_allow_html=True)

st.sidebar.markdown(text.Footer, unsafe_allow_html=True)

# col1, col2 = st.columns([3, 1])

# with col1:
#     st.write("Col 1")

# col2.write("Col 2")
