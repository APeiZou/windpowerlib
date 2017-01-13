#!/usr/bin/python3
# -*- coding: utf-8

import pandas as pd
import logging

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None

from windpowerlib import modelchain

# Feel free to remove or change these lines
# import warnings
# warnings.simplefilter(action="ignore", category=RuntimeWarning)
logging.getLogger().setLevel(logging.INFO)


# Specification of the weather data set CoastDat2 (example data)
coastDat2 = {
    'dhi': 0,
    'dirhi': 0,
    'pressure': 0,
    'temp_air': 2,
    'v_wind': 10,
    'Z0': 0}

# Specification of a second weather data set Exampledata for interpolation
# (example data)
exampledata = {
    'dhi': 0,
    'dirhi': 0,
    'pressure': 0,
    'temp_air': 10,
    'v_wind': 80,
    'Z0': 0}

# Specifications of the wind turbines
enerconE126 = {
    'h_hub': 135,
    'd_rotor': 127,
    'wind_conv_type': 'ENERCON E 126 7500'}

vestasV90 = {
    'h_hub': 105,
    'd_rotor': 90,
    'wind_conv_type': 'VESTAS V 90 3000'}


def ready_example_data(filename, datetime_column='Unnamed: 0'):
    df = pd.read_csv(filename)
    return df.set_index(pd.to_datetime(df[datetime_column])).tz_localize(
        'UTC').tz_convert('Europe/Berlin').drop(datetime_column, 1)


# Loading weather data
weather_df = ready_example_data('weather.csv')
weather_df_2 = ready_example_data('weather_other_height.csv')

e126 = modelchain.SimpleWindTurbine(**enerconE126)
v90 = modelchain.SimpleWindTurbine(**vestasV90)

if plt:
    e126.cp_values.plot(style='*')
    plt.show()
else:
    print("The cp value at a wind speed of 5 m/s: {0}".format(
        e126.cp_values.cp[5.0]))

if plt:
    e126.turbine_power_output(weather=weather_df, data_height=coastDat2).plot(
        legend=True, label='Enercon E126')
    v90.turbine_power_output(weather=weather_df, data_height=coastDat2).plot(
        legend=True, label='Vestas V90')
    e126.turbine_power_output(
        weather=weather_df, weather_2=weather_df_2, data_height=coastDat2,
        data_height_2=exampledata).plot(legend=True, label='Enercon E126')
    v90.turbine_power_output(
        weather=weather_df, weather_2=weather_df_2, data_height=coastDat2,
        data_height_2=exampledata).plot(legend=True, label='Vestas V90')
    plt.show()
else:
    print(v90.turbine_power_output(weather=weather_df, data_height=coastDat2))

logging.info('Done!')
