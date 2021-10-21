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
        "human_development_index": "Human Development Index",
        "extreme_poverty": "Extreme Poverty",
        "gdp_per_capita": "GDP",
        "population": "Population",
        "population_density": "Population Density",
    }
    return pd.read_csv("owid-covid-data.csv", usecols=financial_columns).rename(
        columns=column_names
    )

def get_gni_data():
    gni_columns = ['Country Name', '2018', '2019', '2020']
    column_map = {
        'Country Name': 'Location',
    }

    gni_df = pd.read_csv('gni_per_capita.csv', skiprows=3, usecols=gni_columns).rename(
        columns=column_map
    )
    
    gni_data = gni_df[['2018', '2019', '2020']]
    gni_location = gni_df[['Location']]

    return gni_data, gni_location

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

def preprocess_gni_data(dataframe, location_df):
    gni_df = dataframe.copy()
    gni_df.dropna(how='all', inplace=True)

    # if 2020 data is missing, fill countries with 
    # its 2019 GNI data, else with its 2018 GNI data
    gni_df['2020'].fillna(gni_df['2019'], inplace=True)
    gni_df['2020'].fillna(gni_df['2018'], inplace=True)

    gni_df = gni_df.join(location_df)

    countries = get_country_list()
    gni_df = gni_df[gni_df['Location'].isin(countries)]

    gni_data = gni_df[['Location', '2020']].rename(columns={'2020': 'GNI'})

    return gni_data

def preprocess_financial_data(dataframe):
    df = dataframe.copy()
    df = df.drop_duplicates(subset=["Location"], keep="last")

    countries = get_country_list()
    countries_financial_df = df[df["Location"].isin(countries)]
    countries_financial_df = countries_financial_df[countries_financial_df.GDP.notna()]

    return countries_financial_df

def get_vaccine_and_finance_data():
    finance_data = get_financial_data()
    countries_data, _= getDataset()
    countries_financial_df = preprocess_financial_data(finance_data)


    countries_with_valid_gdp = countries_financial_df['Location'].to_list()
    access_vaccine_data = countries_data[countries_data['Location'].isin(countries_with_valid_gdp)]

    countries_vaccines_financial_data = pd.merge(access_vaccine_data, countries_financial_df, on='Location', how='outer')
    countries_vaccines_financial_data.drop(columns=['Population_y'], inplace=True)
    countries_vaccines_financial_data.rename(columns={'Population_x': 'Population'}, inplace=True)

    return countries_vaccines_financial_data

def get_vax_and_gni_dataset():
    countries_vaccines_financial_data = get_vaccine_and_finance_data()
    gni_data, gni_location = get_gni_data()

    gni_df = preprocess_gni_data(gni_data, gni_location)

    vax_gni = pd.merge(countries_vaccines_financial_data, gni_df, on='Location', how='inner')
    vax_gni['Income Class'] = vax_gni.apply(add_income_class, axis=1)

    return vax_gni

def add_income_class(row):
    if row['GNI'] < 1036:
        val = 'Low Income'
    elif row['GNI'] > 1036 and row['GNI'] <= 4045:
        val = 'Lower-Middle Income'
    elif row['GNI'] > 4045 and row['GNI'] <= 12535:
        val = 'Upper-Middle Income'
    elif row['GNI'] > 12535:
        val = 'High Income'
    return val

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

def get_scatter_plot(data, x_label, y_label, plot_type):
    chart = plots.plot_scatter(data, x_label, y_label, plot_type)
    return chart
