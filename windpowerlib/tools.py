"""
The ``tools`` module contains a collection of functions used in the
windpowerlib.

"""

__copyright__ = "Copyright oemof developer group"
__license__ = "GPLv3"

import collections


def select_closer_value(value_1, value_2, comp_value, corresp_1, corresp_2):
    r"""
    Selects the value with the smaller difference to a comparative value.

    Additionally returns a corresponding value. This function is for example
    used in :py:func:`~.modelchain.v_wind_hub` of the
    :class:`~.modelchain.ModelChain` to choose the wind speed data that is
    close to the hub height of the examined wind turbine. In this case
    `value_1` and `value_2` are the heights of the corresponding wind speed
    data sets `corresp_1` and `corresp_2`.

    Parameters
    ----------
    value_1 : float
        First value of which the difference to `comp_value` will be
        compared with the difference to `comp_value` of `value_2`.
    value_2 : float
        Second value for comparison.
    comp_value : float
        Comparative value.
    corresp_1 : float
        Corresponding value to `value_1`.
    corresp_2 : float
        Corresponding value to `value_2`.

    Returns
    -------
    Tuple(float, float, string)
        Value closer to comparing value as float, corresponding value as
        float and a string for logging.debug.
    """
    if (value_2 is not None and corresp_2 is not None):
        if value_1 == comp_value:
            closest_value = value_1
            logging_string = '(at hub height).'
        elif value_2 == comp_value:
            closest_value = value_2
            logging_string = '(2) (at hub height).'
        elif abs(value_1 - comp_value) <= abs(value_2 - comp_value):
            closest_value = value_1
            logging_string = None
        else:
            closest_value = value_2
            logging_string = None
    else:
        closest_value = value_1
        if value_1 == comp_value:
            logging_string = '(at hub height).'

    # Select correponding value
    if closest_value == value_1:
        corresp_value = corresp_1
    else:
        corresp_value = corresp_2
    # Store values in a named tuple
    return_tuple = collections.namedtuple('selected_values',
                                          ['closest_value',
                                           'corresp_value', 'logging_string'])
    return return_tuple(closest_value, corresp_value, logging_string)
