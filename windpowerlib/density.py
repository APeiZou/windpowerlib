# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 13:26:19 2017

@author: RL-INSTITUT\sabine.haas
"""

"""
The ``density`` module contains methods
to calculate density (and temperature) at hub height of a wind turbine.
"""


def temperature_gradient(weather, data_height, h_hub):
    r"""
    Calculates the temperature T at hub height assuming a linear temperature
    gradient of -6.5 K/km.

    Parameters
    ----------
    weather : DataFrame or Dictionary
            Containing columns or keys with the timeseries for Temperature
            (temp_air) and pressure (pressure).
    data_height : DataFrame or Dictionary
            Containing columns or keys with the height of the measurement or
            model data for temperature (temp_air) and pressure (pressure).
    Returns
    -------
    pandas.Series
        temperature T in K at hub height

    Notes
    -----
    Assumptions:
        * Temperature gradient of -6.5 K/km

    The following equation is used [22]_:
    .. math:: T_{hub}=T_{air, data}-0.0065\cdot\left(h_{hub}-h_{T,data}\right)

    References
    ----------
    .. [22] ICAO-Standardatmosphäre (ISA).
        http://www.dwd.de/DE/service/lexikon/begriffe/S/Standardatmosphaere
                _pdf.pdf?__blob=publicationFile&v=3

    todo: check parameters and references
    """
    h_temperature_data = data_height['temp_air']
    return weather.temp_air - 0.0065 * (h_hub - h_temperature_data)

#def temperature_hub_interpol:


def rho_barometric(weather, data_height, h_hub, T_hub):
    r"""
    Calculates the density of air in kg/m³ at hub height.
    (temperature in K, height in m, pressure in Pa)

    Parameters
    ----------
    weather : DataFrame or Dictionary
        Containing columns or keys with the timeseries for Temperature
        (temp_air) and pressure (pressure).
    data_height : DataFrame or Dictionary
        Containing columns or keys with the height of the measurement or
        model data for temperature (temp_air) and pressure (pressure).
    h_hub : float
        hub height of wind turbine in m
    T_hub : pandas.Series
        temperature in K at hub height

    Returns
    -------
    pandas.Series
        density of air in kg/m³ at hub height

    Notes
    -----
    Assumptions:
      * Pressure gradient of -1/8 hPa/m

    The following equation is used [23],[24]_:
    .. math:: \rho_{hub}=\left(p_{data}/100-\left(h_{hub}-h_{p,data}\right)
       \cdot\frac{1}{8}\right)\cdot \frac{\rho_0 T_0\cdot 100}{p_0 T_{hub}}

    with T: temperature [K], h: height [m], p: pressure [Pa]

    ToDo: Check the equation and add references.

    References
    ----------
    .. [23] Hau, E. Windkraftanlagen - Grundlagen, Technik, Einsatz,
            Wirtschaftlichkeit Springer-Verlag, 2008, p. 560
    .. [24] Weitere Erläuterungen zur Druckgradientkraft
        http://www.dwd.de/DE/service/lexikon/begriffe/D/Druckgradient_pdf.
            pdf?__blob=publicationFile&v=4
    """
    h_pressure_data = data_height['pressure']
    return (weather.pressure / 100 - (h_hub - h_pressure_data)
            * 1 / 8) * 1.225 * 288.15 * 100 / (1.0133 * 10**5 * T_hub)
