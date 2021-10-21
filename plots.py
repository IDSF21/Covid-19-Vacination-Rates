import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from IPython.display import HTML, display


class PLOT_TYPES:
    TOTAL_VACCINATIONS = 1
    FULLY_VACCINATED = 2
    PEOPLE_VACCINATED = 3
    SCATTER_VAX_GNI = 4
    SCATTER_POPULATION = 5


def get_tooltips(plot_type=PLOT_TYPES.TOTAL_VACCINATIONS):
    default_tooltips = ["Collection Date", "Population", "Location"]

    dict = {
        PLOT_TYPES.TOTAL_VACCINATIONS: ["Total Vaccinations"],
        PLOT_TYPES.FULLY_VACCINATED: [
            "People Fully Vaccinated",
            "Percentage Fully Vaccinated",
        ],
        PLOT_TYPES.PEOPLE_VACCINATED: ["People Vaccinated"],
        PLOT_TYPES.SCATTER_VAX_GNI: [
            'Location',
            'GNI',
            'Income Class',
            'Total Vaccinations',
            'Percentage Fully Vaccinated',
        ],
        PLOT_TYPES.SCATTER_POPULATION: [
            'Location',
            'GNI',
            'Income Class',
            'Percentage Fully Vaccinated',
            'Population'
        ],
    }

    return [*default_tooltips, *dict.get(plot_type, [])]


def plot_bars(data, x_label, y_label, plot_type=PLOT_TYPES.TOTAL_VACCINATIONS):

    tooltip_list = get_tooltips(plot_type)
    bars = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            alt.X(x_label, sort=None),
            alt.Y(y_label, sort=None),
            tooltip=tooltip_list,
            color=y_label,
        )
    )
    plot_title = f"Plot of {y_label.split(':')[0]} against {x_label.split(':')[0]}"
    return bars.properties(title=plot_title)

def plot_scatter(data, x_label, y_label, plot_type=PLOT_TYPES.SCATTER_VAX_GNI):
    tooltip_list = get_tooltips(plot_type)
    bars = (
        alt.Chart(data)
        .mark_circle()
        .encode(
            alt.X(x_label, scale=alt.Scale(zero=False)),
            alt.Y(y_label, scale=alt.Scale(zero=False, padding=1)),
            alt.Color('Income Class', sort=['High Income', 'Upper-Middle Income', 'Lower-Middle Income']),
            size='Human Development Index',
            tooltip=tooltip_list,
        ).interactive()
    )
    plot_title = f"A Plot of {y_label.split(':')[0]} vs {x_label.split(':')[0]} grouped by Income Classes"
    return bars.properties(title=plot_title, width=700, height=500)
