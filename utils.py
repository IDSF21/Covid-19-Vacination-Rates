import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from IPython.display import HTML, display


def get_country_list():
    return pd.read_csv("locations.csv")["location"].to_list()


def get_covid_data():
    vaccination_columns = [
        "date",
        "location",
        "population",
        "total_vaccinations",
        "people_vaccinated",
        "people_fully_vaccinated",
    ]
    column_names = {
        "date": "Collection Date",
        "location": "Location",
        "population": "Population",
        "total_vaccinations": "Total Vaccinations",
        "people_vaccinated": "People Vaccinated",
        "people_fully_vaccinated": "People Fully Vaccinated",
    }
    return pd.read_csv(
        "owid-covid-data.csv",
        usecols=vaccination_columns,
    ).rename(columns=column_names)


def get_financial_data():
    financial_columns = [
        "location",
        "human_development_index",
        "extreme_poverty",
        "gdp_per_capita",
        "population",
        "population_density",
    ]
    column_names = {
        "location": "Location",
        "human_development_index": "HDI",
        "extreme_poverty": "Extreme Poverty",
        "gdp_per_capita": "GDP per capita",
        "population": "Population",
        "population_density": "Polulation Density",
    }
    return pd.read_csv("owid-covid-data.csv", usecols=financial_columns).rename(
        columns=column_names
    )


def print_complete_dataframe(dataframe):
    return display(HTML(dataframe.to_html()))


def preprocess_covid_data(dataframe):
    dataframe = dataframe.dropna(
        subset=[
            "Total Vaccinations",
            "People Vaccinated",
            "People Fully Vaccinated",
            "Population",
        ]
    ).drop_duplicates(subset=["Location"], keep="last")
    dataframe["Percentage Fully Vaccinated"] = (
        dataframe["People Fully Vaccinated"] / dataframe["Population"] * 100
    )
    return dataframe


def country_continental_split(dataframe):
    countries = get_country_list()
    countries_data = dataframe[dataframe["Location"].isin(countries)]
    continents_data = dataframe[~dataframe["Location"].isin([*countries, "World"])]
    return countries_data, continents_data


def sort_and_return_top_k(dataframe, k=10, sort_by=["Total Vaccinations"]):
    return dataframe.sort_values(by=[*sort_by], ascending=False).iloc[:k]
