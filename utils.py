import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from IPython.display import HTML, display

import plots



def extract_location_list(dataframe):
    return dataframe["Location"].to_list()


def get_country_list():
    column_names = {"location": "Location"}
    return extract_location_list(
        pd.read_csv("locations.csv").rename(columns=column_names)
    )


def get_covid_data():
    vaccination_columns = [
        "date",
        "location",
        "continent",
        "population",
        "total_vaccinations",
        "people_vaccinated",
        "people_fully_vaccinated",
    ]
    column_names = {
        "date": "Collection Date",
        "location": "Location",
        "continent": "Continent",
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
    # continents_data = dataframe[~dataframe["Location"].isin([*countries, "World"])]
    continents_data = dataframe[~dataframe["Location"].isin([*countries])]
    return countries_data, continents_data

def get_countries_by_continent(dataframe, continent):
    return dataframe[dataframe['Continent'] == continent]

def sort_and_return_top_k(
    dataframe, k=10, sort_by=["Total Vaccinations"], ascending=False
):
    return dataframe.sort_values(by=[*sort_by], ascending=ascending).iloc[:k]


def getDataset():
    covid_data = get_covid_data()
    dataset = preprocess_covid_data(covid_data)
    countries_data, continents_data = country_continental_split(dataset)
    return countries_data, continents_data


def get_plot(data, x_label, y_label, k, sort_by, plot_type, ascending=False):
    subset = sort_and_return_top_k(data, k, sort_by, ascending)
    chart = plots.plot_bars(subset, x_label, y_label, plot_type)
    return chart
