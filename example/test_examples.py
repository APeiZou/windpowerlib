import os
import subprocess
import tempfile
import nbformat
import sys
from example import basic_example as be
from example import further_example as fe
from numpy.testing import assert_allclose
import pytest


class TestExamples:

    def test_basic_example_flh(self):
        # tests full load hours
        weather = be.get_weather_data('weather.csv')
        my_turbine, e126 = be.initialise_wind_turbines()
        be.calculate_power_output(weather, my_turbine, e126)

        assert_allclose(1766.6870, (e126.power_output.sum() /
                                    e126.nominal_power), 0.01)
        assert_allclose(1882.7567, (my_turbine.power_output.sum() /
                                    my_turbine.nominal_power), 0.01)

    def test_further_example_flh(self):
        # tests full load hours
        weather = be.get_weather_data('weather.csv')
        my_turbine, e126 = be.initialise_wind_turbines()
        example_farm, example_farm_2 = fe.initialise_wind_farms(my_turbine,
                                                                e126)
        example_cluster = fe.initialise_wind_turbine_cluster(example_farm,
                                                             example_farm_2)
        fe.calculate_power_output(weather, example_farm, example_cluster)
        assert_allclose(1586.23527, (example_farm.power_output.sum() /
                                     example_farm.installed_power), 0.01)
        example_cluster.installed_power = example_cluster.get_installed_power()
        assert_allclose(1813.66122, (example_cluster.power_output.sum() /
                                     example_cluster.installed_power), 0.01)

    def _notebook_run(self, path):
        """
        Execute a notebook via nbconvert and collect output.
        Returns (parsed nb object, execution errors)
        """
        dirname, __ = os.path.split(path)
        os.chdir(dirname)
        with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
            args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                    "--ExecutePreprocessor.timeout=60",
                    "--output", fout.name, path]
            subprocess.check_call(args)

            fout.seek(0)
            nb = nbformat.read(fout, nbformat.current_nbformat)

        errors = [output for cell in nb.cells if "outputs" in cell
                  for output in cell["outputs"]
                  if output.output_type == "error"]

        return nb, errors

    @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
    def test_basic_example_ipynb(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        nb, errors = self._notebook_run(
            os.path.join(dir_path, 'basic_example.ipynb'))
        assert errors == []

    @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
    def test_further_example_ipynb(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        nb, errors = self._notebook_run(
            os.path.join(dir_path, 'further_example.ipynb'))
        assert errors == []
