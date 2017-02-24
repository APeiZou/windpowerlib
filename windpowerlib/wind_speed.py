"""
The ``wind_speed`` module contains methods to calculate the wind_speed at
hub height of a wind turbine.

"""

__copyright__ = "Copyright oemof developer group"
__license__ = "GPLv3"

import numpy as np


def logarithmic_wind_profile(v_wind, v_wind_height, hub_height, z_0,
                             obstacle_height=0):
    r"""
    Calculates the wind speed at hub height with the logarithmic wind profile.

    The logarithmic height equation is used. There is the possibility of
    including the height of the surrounding obstacles in the calculation. This
    fuction is carried out when the parameter `wind_model` of an object of the
    class WindTurbine is 'logarithimc' or 'logarithimc_closest'.

    Parameters
    ----------
    v_wind : pandas.Series or array
        Wind speed time series.
    v_wind_height : float
        Height for which the parameter `v_wind` applies.
    hub_height : float
        Hub height of wind turbine.
    z_0 : pandas.Series or array or float
        Roughness length.
    obstacle_height : float, optional
        Height of obstacles in the surroundings of the wind turbine. Put
        obstacle_height to zero for wide spread obstacles. Default: 0

    Returns
    -------
    pandas.Series or array
        Wind speed at hub height as time series.

    Notes
    -----
    The following equation is used for the logarithmic wind profile [27]_:

    .. math:: v_{wind,hub}=v_{wind,data}\cdot
        \frac{\ln\left(\frac{h_{hub}-d}{z_{0}}\right)}{\ln\left(
        \frac{h_{data}-d}{z_{0}}\right)}

    with:
        v: wind speed, h: height, :math:`z_{0}`: roughness length
        d: includes obstacle height (d = 0.7 * obstacle_height)

    For  d = 0 it results in the following equation [20]_, [25]_:

    .. math:: v_{wind,hub}=v_{wind,data}\cdot\frac{\ln\left(\frac{h_{hub}}
        {z_{0}}\right)}{\ln\left(\frac{h_{data}}{z_{0}}\right)}

    :math:`h_{data}` is the height in which the wind speed
    :math:`v_{wind,data}` is measured.

    `v_wind_height`, `z_0`, `hub_height` and `obstacle_height` have to be of
    the same unit.

    References
    ----------
    .. [20] Gasch R., Twele J.: "Windkraftanlagen". 6. Auflage, Wiesbaden,
            Vieweg + Teubner, 2010, p. 129
    .. [25] Hau, E.: "Windkraftanlagen - Grundlagen, Technik, Einsatz,
            Wirtschaftlichkeit". 4. Auflage, Springer-Verlag, 2008, p. 515
    .. [27] Quaschning V.: "Regenerative Energiesysteme". München, Hanser
            Verlag, 2011, p. 278

    """
    if 0.7 * obstacle_height > v_wind_height:
        raise ValueError('To take an obstacle height of ' +
                         str(obstacle_height) + ' m into consideration wind ' +
                         'speed data of a higher height is needed.')
    return (v_wind * np.log((hub_height - 0.7 * obstacle_height) / z_0) /
            np.log((v_wind_height - 0.7 * obstacle_height) / z_0))


def v_wind_hellman(v_wind, v_wind_height, hub_height, hellman_exp=None,
                   z_0=None):
    r"""
    Calculates the wind speed at hub height with the hellman equation.

    It is assumed that the wind profile follows a power law. This fuction is
    carried out when the parameter `wind_model` of an object of the class
    WindTurbine is 'hellman'.

    Parameters
    ----------
    v_wind : pandas.Series or array
        Wind speed time series.
    v_wind_height : float
        Height for which the parameter `v_wind` applies.
    hub_height : float
        Hub height of wind turbine.
    hellman_exp : float, optional
        The Hellman exponent, which combines the increase in wind speed due to
        stability of atmospheric conditions and surface roughness into one
        constant. Default: hellman_exp = 1 / ln(h_hub/z_0). If no roughness
        length is given hellman_exp = 1/7.
    z_0 : float, optional
        Roughness length. Default: None

    Returns
    -------
    pandas.Series or array
        Wind speed at hub height as time series.

    Notes
    -----
    The following equation is used for the logarithmic wind profile [31]_,
    [32]_, [33]_:

    .. math:: v_{wind,hub}=v_{wind,data}\cdot \left(\frac{h_{hub}}{h_{data}}
        \right)^\alpha

    with:
        v: wind speed, h: height, :math:`\alpha`: Hellman exponent

    :math:`h_{data}` is the height in which the wind speed
    :math:`v_{wind,data}` is measured and :math:`h_{hub}` is the hub height of
    the wind turbine.

    For the Hellman exponent :math:`\alpha` many studies use a value of 1/7 for
    onshore and a value of 1/9 for for offshore. The Hellman exponent can also
    be calulated by the following equation [32]_, [33]_:

    .. math:: \alpha = \frac{1}{ln\left(\frac{h_{hub}}{z_0} \right)}

    with:
        :math:`z_{0}`: roughness length

    References
    ----------
    .. [31] Sharp, E.: "Spatiotemporal disaggregation of GB scenarios depicting
            increased wind capacity and electrified heat demand in dwellings".
            UCL, Energy Institute, 2015, p. 83
    .. [32] Hau, E.: "Windkraftanlagen - Grundlagen, Technik, Einsatz,
            Wirtschaftlichkeit". 4. Auflage, Springer-Verlag, 2008, p. 517
    .. [33] Quaschning V.: "Regenerative Energiesysteme". München, Hanser
            Verlag, 2011, p. 279

    """
    if hellman_exp is None:
        try:
            hellman_exp = 1 / np.log(hub_height / z_0)
        except:
            hellman_exp = 1/7
    return v_wind * (hub_height / v_wind_height) ** hellman_exp
