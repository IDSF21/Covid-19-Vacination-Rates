import sys

sys.path.append("..")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import streamlit as st

import utils
import plots
import text

covid_data = utils.get_covid_data()
dataset = utils.preprocess_covid_data(covid_data)

countries_data, continents_data = utils.country_continental_split(dataset)

top_10_vaccinations_by_countries = utils.sort_and_return_top_k(countries_data)

chart = plots.plot_bars(
    top_10_vaccinations_by_countries,
    "Total Vaccinations:Q",
    "Location:O",
    plot_type=plots.PLOT_TYPES.FULLY_VACCINATED,
)


st.title(text.Title)

st.write(text.Paragraph_1)
st.write("Charts are missing a Title")

st.write(chart)

st.header("Questions")
st.markdown(text.Questions)


st.header("Conclusion")
st.write(text.Conclusion)