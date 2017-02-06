"""The ``power_output`` module contains methods to calculate the power output
of a wind turbine.

"""

__copyright__ = "Copyright oemof developer group"
__license__ = "GPLv3"
__author__ = "author1, author2"

import numpy as np


def tpo_through_cp(v_wind, rho_hub, d_rotor, cp_series):
    r"""
    Calculates the power output of one wind turbine using cp values.

    This fuction is carried out when the parameter `tp_output_model` of an
    object of the class WindTurbine is 'cp_values'.

    Parameters
    ----------
    v_wind : pandas.Series or array
        wind speed time series at hub height in m/s
    rho_hub : pandas.Series or array
        density of air at hub height in kg/m³
    d_rotor : float
        diameter of rotor in m
    cp_series : pandas.Series or array
        cp (power coefficient) values for the wind speed time series
        see also modelchain.cp_series()

    Returns
    -------
    pandas.Series or array
        electrical power output of the wind turbine in W

    Notes
    -----
    The following equation is used for the power output [21],[26]_:
    .. math:: p _{wpp}=\frac{1}{8}\cdot\rho_{hub}\cdot d_{rotor}^{2}
        \cdot\pi\cdot v_{wind}^{3}\cdot cp\left(v_{wind}\right)

    with:
        v: wind speed [m/s], d: diameter [m], :math:`\rho`: density [kg/m³]

    References
    ----------
    .. [21] Gasch R., Twele J.: "Windkraftanlagen". 6. Auflage, Wiesbaden,
            Vieweg + Teubner, 2010, pages 35ff, 208
    .. [26] Hau, E. Windkraftanlagen - Grundlagen, Technik, Einsatz,
            Wirtschaftlichkeit Springer-Verlag, 2008, p. 542
    """
    return (1 / 8 * rho_hub * d_rotor ** 2 * np.pi * np.power(v_wind, 3) *
            cp_series)


def tpo_through_P(p_values, v_wind):
    r"""
    Converts power curve to power output of wind turbine.

    Interpolates the values of the power curve as a function of the wind speed
    between data obtained from the power curve of the specified wind turbine
    type.
    This fuction is carried out when the parameter 'tp_output_model' of an
    object of the class WindTurbine is 'p_values'.

    Parameters
    ----------
    p_values : pandas.DataFrame
        power curve of the wind turbine
        the indices are the corresponding wind speeds of the power curve, the
        power values containing column is called 'P'
    v_wind : pandas.Series or array
        wind speed time series at hub height in m/s

    Returns
    -------
    array
        electrical power of the wind turbine

    Note
    ----
    See also cp_series() in the module modelchain
    """
    v_max = p_values.index.max()
    v_wind[v_wind > v_max] = v_max
    return np.interp(v_wind, p_values.index, p_values.P)


def interpolate_P_curve(v_wind, rho_hub, p_values):
    r"""
    Interpolates density corrected power curve.

    Parameters
    ----------
    v_wind : pandas.Series or array
        wind speed time series at hub height in m/s
    rho_hub : pandas.Series or array
        density of air at hub height in kg/m³
    p_values : pandas.DataFrame
        power curve of the wind turbine
        the indices are the corresponding wind speeds of the power curve, the
        power values containing column is called 'P'

    Returns
    -------
    numpy.array
        electrical power of the wind turbine

    Notes
    -----
    The following equation is used for the wind speed at site
    [28], [29], [30]_:
    .. math:: v_{site}=v_{std}\cdot\left(\frac{\rho_0}
                       {\rho_{site}}\right)^{p(v)}

    with:
        .. math:: p=\begin{cases}
                      \frac{1}{3} & v_{std} \leq 7.5\text{ m/s}\\
                      \frac{1}{15}\cdot v_{std}-\frac{1}{6} & 7.5
                      \text{ m/s}<v_{std}<12.5\text{ m/s}\\
                      \frac{2}{3} & \geq 12.5 \text{ m/s}
                    \end{cases},
        v: wind speed [m/s], :math:`\rho`: density [kg/m³]

    :math:`v_{std}` is the standard wind speed in the power curve
    (:math:`v_{std}`, :math:`P_{std}`)
    :math:`v_{site}` is density corrected wind speed for the power curve
    (:math:`v_{site}`, :math:`P_{std}`)

    References
    ----------
    .. [28] Svenningsen, L.: "Power Curve Air Density Correction And Other
            Power Curve Options in WindPRO". 1st edition, Aalborg,
            EMD International A/S , 2010, p. 4
    .. [29] Svenningsen, L.: "Proposal of an Improved Power Curve Correction".
            EMD International A/S , 2010
    .. [30] Biank, M.: "Methodology, Implementation and Validation of a
            Variable Scale Simulation Model for Windpower based on the
            Georeferenced Installation Register of Germany". Master's Thesis
            at RLI, 2014, p. 13
    """
    return [(np.interp(v_wind[i], p_values.index *
            (1.225 / rho_hub[i])**(np.interp(p_values.index, [7.5, 12.5],
                                             [1/3, 2/3])),
            p_values.P, left=0, right=0)) for i in range(len(v_wind))]
