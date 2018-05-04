"""
The ``turbine_cluster_modelchain`` module contains functions and classes of the
windpowerlib. TODO: adapt

"""

__copyright__ = "Copyright oemof developer group"
__license__ = "GPLv3"

from windpowerlib import wake_losses
from windpowerlib.modelchain import ModelChain


class TurbineClusterModelChain(ModelChain):
    r"""
    Model to determine the output of a wind farm or wind turbine cluster.

    Parameters
    ----------
    wind_object : WindFarm or WindTurbineCluster
        A :class:`~.wind_farm.WindFarm` object representing the wind farm or
        a :class:`~.wind_turbine_cluster.WindTurbineCluster` object
        representing the wind turbine cluster.
    wake_losses_method : String
        Defines the method for talking wake losses within the farm into
        consideration. Options: 'power_efficiency_curve',
        'constant_efficiency', 'dena_mean', 'knorr_mean', 'dena_extreme1',
        'dena_extreme2', 'knorr_extreme1', 'knorr_extreme2', 'knorr_extreme3'
        or None. Default: 'dena_mean'.
    smoothing : Boolean
        If True the power curves will be smoothed before the summation.
        Default: True.
    block_width : Float, optional
        Width of the moving block.
        Default in :py:func:`~.power_curves.smooth_power_curve`: 0.5.
    standard_deviation_method : String, optional
        Method for calculating the standard deviation for the gaussian
        distribution. Options: 'turbulence_intensity', 'Norgaard',
        'Staffell_Pfenninger'.
        Default in :py:func:`~.power_curves.smooth_power_curve`:
        'turbulence_intensity'.
    smoothing_order : String
        Defines when the smoothing takes place if `smoothing` is True. Options:
        'turbine_power_curves' (to the single turbine power curves),
        'wind_farm_power_curves'. Default: 'wind_farm_power_curves'.

    Other Parameters
    ----------------
    wind_speed_model : string
        Parameter to define which model to use to calculate the wind speed
        at hub height. Valid options are 'logarithmic', 'hellman' and
        'interpolation_extrapolation'.
    temperature_model : string
        Parameter to define which model to use to calculate the temperature
        of air at hub height. Valid options are 'linear_gradient' and
        'interpolation_extrapolation'.
    density_model : string
        Parameter to define which model to use to calculate the density of
        air at hub height. Valid options are 'barometric', 'ideal_gas' and
        'interpolation_extrapolation'.
    power_output_model : string
        Parameter to define which model to use to calculate the turbine
        power output. Valid options are 'power_curve' and
        'power_coefficient_curve'.
    density_correction : boolean
        If the parameter is True the density corrected power curve is used
        for the calculation of the turbine power output.
    obstacle_height : float
        Height of obstacles in the surrounding area of the wind turbine in
        m. Set `obstacle_height` to zero for wide spread obstacles.
    hellman_exp : float
        The Hellman exponent, which combines the increase in wind speed due
        to stability of atmospheric conditions and surface roughness into
        one constant.

    Attributes
    ----------
    power_plant : WindFarm or WindTurbineCluster
        A :class:`~.wind_farm.WindFarm` object representing the wind farm or
        a :class:`~.wind_turbine_cluster.WindTurbineCluster` object
        representing the wind turbine cluster.
    wake_losses_method : String
        Defines the method for talking wake losses within the farm into
        consideration. Options: 'power_efficiency_curve',
        'constant_efficiency', 'dena_mean', 'knorr_mean', 'dena_extreme1',
        'dena_extreme2', 'knorr_extreme1', 'knorr_extreme2', 'knorr_extreme3'
        or None. Default: 'dena_mean'.
    smoothing : Boolean
        If True the power curves will be smoothed before the summation.
        Default: True.
    block_width : Float, optional
        Width of the moving block.
        Default in :py:func:`~.power_curves.smooth_power_curve`: 0.5.
    standard_deviation_method : String, optional
        Method for calculating the standard deviation for the gaussian
        distribution. Options: 'turbulence_intensity', 'Norgaard',
        'Staffell_Pfenninger'.
        Default in :py:func:`~.power_curves.smooth_power_curve`:
        'turbulence_intensity'.
    power_output : pandas.Series
        Electrical power output of the wind turbine in W.
    smoothing_order : String
        Defines when the smoothing takes place if `smoothing` is True. Options:
        'turbine_power_curves' (to the single turbine power curves),
        'wind_farm_power_curves'. Default: 'wind_farm_power_curves'.
    wind_speed_model : string
        Parameter to define which model to use to calculate the wind speed
        at hub height. Valid options are 'logarithmic', 'hellman' and
        'interpolation_extrapolation'.
    temperature_model : string
        Parameter to define which model to use to calculate the temperature
        of air at hub height. Valid options are 'linear_gradient' and
        'interpolation_extrapolation'.
    density_model : string
        Parameter to define which model to use to calculate the density of
        air at hub height. Valid options are 'barometric', 'ideal_gas' and
        'interpolation_extrapolation'.
    power_output_model : string
        Parameter to define which model to use to calculate the turbine
        power output. Valid options are 'power_curve' and
        'power_coefficient_curve'.
    density_correction : boolean
        If the parameter is True the density corrected power curve is used
        for the calculation of the turbine power output.
    obstacle_height : float
        Height of obstacles in the surrounding area of the wind turbine in
        m. Set `obstacle_height` to zero for wide spread obstacles.
    hellman_exp : float
        The Hellman exponent, which combines the increase in wind speed due
        to stability of atmospheric conditions and surface roughness into
        one constant.

    """
    def __init__(self, power_plant, wake_losses_method='dena_mean',
                 smoothing=True, block_width=0.5,
                 standard_deviation_method='turbulence_intensity',
                 smoothing_order='wind_farm_power_curves', **kwargs):
        super(TurbineClusterModelChain, self).__init__(power_plant, **kwargs)

        self.power_plant = power_plant
        self.wake_losses_method = wake_losses_method
        self.smoothing = smoothing
        self.block_width = block_width
        self.standard_deviation_method = standard_deviation_method
        self.smoothing_order = smoothing_order

        self.power_curve = None
        self.power_output = None

    def run_model(self, weather_df):
        r"""
        Runs the model.

        Parameters
        ----------
        weather_df : pandas.DataFrame
            DataFrame with time series for wind speed `wind_speed` in m/s, and
            roughness length `roughness_length` in m, as well as optionally
            temperature `temperature` in K, pressure `pressure` in Pa,
            density `density` in kg/m³ and turbulence intensity
            `turbulence_intensity` depending on `power_output_model`,
            `density_model` and `standard_deviation_model` chosen.
            The columns of the DataFrame are a MultiIndex where the first level
            contains the variable name (e.g. wind_speed) and the second level
            contains the height at which it applies (e.g. 10, if it was
            measured at a height of 10 m). See below for an example on how to
            create the weather_df DataFrame.

# TODO rename method to model (wake_losses_method)

        Returns
        -------
        self

        Examples
        ---------
        >>> import numpy as np
        >>> import pandas as pd
        >>> weather_df = pd.DataFrame(np.random.rand(2,6),
        ...                           index=pd.date_range('1/1/2012',
        ...                                               periods=2,
        ...                                               freq='H'),
        ...                           columns=[np.array(['wind_speed',
        ...                                              'wind_speed',
        ...                                              'temperature',
        ...                                              'temperature',
        ...                                              'pressure',
        ...                                              'roughness_length']),
        ...                                    np.array([10, 80, 10, 80,
        ...                                             10, 0])])
        >>> weather_df.columns.get_level_values(0)[0]
        'wind_speed'

        """
        # Set turbulence intensity for assigning power curve
        turbulence_intensity = (
            weather_df['turbulence_intensity'].values.mean() if
            'turbulence_intensity' in
            weather_df.columns.get_level_values(0) else None)
        # Assign power curve
        if (self.wake_losses_method == 'power_efficiency_curve' or
                self.wake_losses_method == 'constant_efficiency' or
                self.wake_losses_method is None):
            wake_losses_method_to_power_curve = self.wake_losses_method
        else:
            wake_losses_method_to_power_curve = None
        self.power_plant.assign_power_curve(
            wake_losses_method=wake_losses_method_to_power_curve,
            smoothing=self.smoothing, block_width=self.block_width,
            standard_deviation_method=self.standard_deviation_method,
            smoothing_order=self.smoothing_order,
            roughness_length=weather_df['roughness_length'][0].mean(),
            turbulence_intensity=turbulence_intensity)
        # Assign mean hub height
        self.power_plant.mean_hub_height()

        # Run modelchain
        wind_speed_hub = self.wind_speed_hub(weather_df)
        density_hub = (None if (self.power_output_model == 'power_curve' and
                                self.density_correction is False)
                       else self.density_hub(weather_df))
        if (self.wake_losses_method != 'power_efficiency_curve' and
                self.wake_losses_method != 'constant_efficiency' and
                self.wake_losses_method is not None):
            # Reduce wind speed with wind efficiency curve
            wind_speed_hub = wake_losses.reduce_wind_speed(
                wind_speed_hub,
                wind_efficiency_curve_name=self.wake_losses_method)
        self.power_output = self.turbine_power_output(wind_speed_hub,
                                                      density_hub)
        return self
