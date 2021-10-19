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


def get_tooltips(plot_type=PLOT_TYPES.TOTAL_VACCINATIONS):
    default_tooltips = ["Collection Date", "Population", "Location"]

    dict = {
        PLOT_TYPES.TOTAL_VACCINATIONS: ['Total Vaccinations'],
        PLOT_TYPES.FULLY_VACCINATED: ['People Fully Vaccinated', 'Percentage Fully Vaccinated'],
        PLOT_TYPES.PEOPLE_VACCINATED: ['People Vaccinated']
    }

    return [*default_tooltips, *dict.get(plot_type, [])]


def plot_bars(data, x_label, y_label, plot_type=PLOT_TYPES.TOTAL_VACCINATIONS):

    tooltip_list = get_tooltips(plot_type)
    bars = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            alt.Y(y_label, sort=None),
            x=x_label,
            tooltip=tooltip_list,
        )
    )

    return bars
