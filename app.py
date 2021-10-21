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
st.write(text.Paragraph_2)
st.image(
    world_bank_screenshot,
)
st.info(text.Paragraph_3)

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
show_fully_vaccinated = st.sidebar.checkbox("Full Vaccinations", True)
# show_one_vaccination = st.sidebar.checkbox("One Vaccination")
show_vaccination_rates_by_income_level = st.sidebar.checkbox("Country Vaccination Rates by Income Level", True)
show_vaccination_rates_by_population = st.sidebar.checkbox("Percentage Vaccinated by Population", True)


if show_total_vaccinations:
    st.subheader(f"Vaccinations per Continents")
    st.markdown(
        """ 
            We start by answering the top continents with the highest numbers of total vaccine doses. 
            This includes, first dose, second does and booster shots. We find the entire world have administered an overall 
            7+ billion vaccines (actual: 7874965730). Asia, the most populous continent administered the most vaccine doses and 
            Africa the second most continent has administered the second least total vaccine doses. Is there a reason for this disparity? 
            Do economic factors on the continents play a role in the total number of administered doses? We explore further to answer these.

            For now, we know that the decreasing order of continents with total administered vaccine doses are:
            Asia, Europe, North America, European Union, South America, Africa and Oceania 
        """
    )
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
    st.markdown(
        """ 
            We also, explore the data to know which countries have administered the most vaccine doses. 
            We find in decreasing order, China, India, United States, Brazil, Japan, Indonesia, Turkey, Mexico, Germany and France 
            have administered the most vaccine doses.

            Use the slider in the side bar to increase or decrease the number of countries to see the corresponding 
            top or bottom X countries with full vaccination rates.
        """
    )
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
    st.markdown(
        """ 
           We take a look at the bottom country with total administered vaccines and find the following countries/Islands at the bottom 10.
           Anguilla, Nauru, Wallis and Futuna, Tuvalu, Saint Helena, Folkland Islands, Montseratt, Niue, Tokelau and Pitcairn.
        """
    )
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
st.error(
    """
        Is the usage of total administered doses for analysis a true reflection of our bottomline question (Study of Vaccination Access across Countries and Continents)?

        We find that we need to compare the number of administered vaccines to each country/continent population to give a fair analysis.

        Hence, the remainder of our analysis uses fully vaccination rate which is a percentage ration of fully vaccinated population to total population of each countries.
    """
)
if show_vaccinations_rates:
    st.subheader("Full Vaccination Rates per Continents")
    st.markdown(
        """ 
            For a comparison of fully vaccination rates (fully vaccinated population to total population ratio) amongst continents.
            First, we see that only about 35% of the world is fully vaccinated (received double doses).
            We also notice a wide gap amongst the continets. Asia and Africa the first and second most populous continents 
            rank bottom two on the list of fully vaccinated rated, with position 6th and 7th repsectively.

            Perhaps, we can attribute this to the income levels and poverty index of the countries in these continets?
            We explore further analysis is subsequent sections to get a clearer answer to this question.
        """
    )
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
            
            It's interesting to note that some countries/islands with small populations like Pitcairn 
            and Gibraltar have Vaccination rates equal to or higher than 100%. More interesting is that Pitcairn originally 
            ranked bottom on total administered doses but is now ranked top here. 
            The fully vaccinated percentage is therefore a better metrics to analysis and visualize with.

            Select Continent from the dropdown to see countries in selected continent with top fully vaccinated rates.
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
    st.markdown(
        """
        Full vaccination rates are measured as a percentage of the ratio of fully vaccinated population to the total population.
        We find that countries with high number of doses administered do not feature in the graph as their total population size is a lot 
        and compared with their total populations size, they are not doing very well in vaccination rates.
        The top 10 countries (and islands) with the highest vaccination rates are in descending order are:
        Gibraltar, Pitcairn, Portugal, United Arab Emirates, Cayman Islands, Malta, Iceland, Singapore, Spain and Qatar
        
        Conversely, we also visualize the countries with the countries with the countries with the lowest fully vaccination rates.
        The bottom 10 countries are: 
        Tanzania, Cameroon, Guinea-Bissau, South Sudan, Haiti, Chad, Central African Republic, Liberia, Yemen, and Democratic Republic of Congo.

        Use the slider in the side bar to increase or decrease the number of countries to see the corresponding 
        top or bottom X countries with full vaccination rates.
        """
    )
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
    st.markdown(
        """
        Here, we visualize a graph of countries' percentage of fully vaccinated population with respect to their GNI per capita.
        We also, show the income level of each country. This income level calssification is obtained from World Bank (See Reference for source).

        See see from this visualization that countries with higher GNI per capita have higher percentages of fully vaccinated population
        and vice versa. This also shows that countries with higher income levels generally have higher vaccination percentages.

        Note: The chart below is zoomable to allow for more interactive.
        """
    )
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
    st.markdown(
        """
        The graph of Percentage Fully Vaccinated vs Population shown below prvoides insights that
        the percentage of vaccinated population is almost independent of the population size
        but instead more dependent on the country's access to vaccine.
        This is seen from the outliers (China & India) with very close population sizes; 1444216102 and 1393409033 respectively.
        Both countries have a wide gap in their (fully) vaccinated percentages with China at 70.78% and India only fully vaccinated 19.93%.

        Also, we see that Portugal (classified High Income) with the  one-tenth the population of China has a higher vaccination rate
        whilst lower income countries like Sierra Leone with way smaller population size have less than 1% vaccination rate.

        Hence, we conclude that the percentage of fully vaccinated pupulation in countries is independent of countries' population size 
        but rather dependent on their access to the vaccine, which may be measure here by the Countries' overall income level.

        Note: The chart below is zoomable to allow for more interactive.
        """
    )
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
