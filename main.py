import plotly.express as px
import pandas as pd
from typing import Final
import numpy as np
import os

if __name__ == "__main__":
    cut_in_ws: Final[float] = 3.5
    rated_ws: Final[float] = 15
    cut_out_ws: Final[float] = 25
    end_ws: Final[float] = 30
    if not cut_in_ws < rated_ws or not rated_ws < cut_out_ws or not cut_out_ws < end_ws:
        raise ValueError("Configured wind speeds are out of order")

    rated_power_kilowatts: Final[int] = 2000
    precision: Final[float] = 0.01

    nan_series_index: Final[pd.Index] = pd.Index(
        data=np.arange(
            start=cut_in_ws + precision, stop=rated_ws - precision, step=precision
        ).round(2)
    )
    nan_series: Final[pd.Series] = pd.Series(index=nan_series_index, dtype=float)

    curve_series = pd.Series(
        index=[cut_in_ws - precision, cut_in_ws, rated_ws, rated_ws + precision],
        data=[0, 0, rated_power_kilowatts, rated_power_kilowatts],
        dtype=float,
    )

    curve_series = pd.concat(objs=[curve_series, nan_series])
    curve_series = curve_series.interpolate(method="quadratic", order=1)

    constant_series: Final[pd.Series] = pd.Series(
        index=[0, cut_out_ws - precision, cut_out_ws, end_ws],
        data=[0, rated_power_kilowatts, 0, 0],
        dtype=float,
    )

    combined_series = pd.concat(objs=[curve_series, constant_series]).sort_index()

    fig = px.line(
        data_frame=combined_series,
        title="Idealised Wind Turbine Power Curve",
        labels={"value": "Power Output [kW]", "index": "Wind Speed [m/s]"},
        color_discrete_sequence=["black"],
    )
    fig.update_layout(
        showlegend=False,
        title={"x": 0.5, "xanchor": "center", "yanchor": "top"},
        plot_bgcolor="#FFF",
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="lightgray",
        showline=True,
        linecolor="black",
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="lightgray",
        zerolinecolor="lightgray",
        showline=True,
        linecolor="black",
    )
    fig.show()

    output_folder = "img/"
    os.makedirs(output_folder, exist_ok=True)
    fig.write_image(
        os.path.join(output_folder, "Idealised Wind Turbine Power Curve.svg")
    )
