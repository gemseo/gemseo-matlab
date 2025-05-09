# Copyright 2021 IRT Saint Exupéry, https://www.irt-saintexupery.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# Copyright (c) 2018 IRT-AESE.
# All rights reserved.
#
# Contributors:
#    INITIAL AUTHORS - API and implementation and/or documentation
#        :author: Arthur Piat
#        :author: François Gallard: initial author of the scilab version
#                                   of MatlabDataProcessorWrapper
#        :author: Nicolas Roussouly: GEMSEO integration
#
#    OTHER AUTHORS   - MACROSCOPIC CHANGES
"""Definition of Matlab data processor.

Overview
--------

The class and functions in this module enables to
manipulate data from and toward the Matlab workspace.
It also enables to read and write Matlab data file (.mat).
"""

from __future__ import annotations

import os
from copy import copy
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version_of
from typing import TYPE_CHECKING
from typing import Final

import matlab
import scipy.io
from gemseo.core.discipline.data_processor import DataProcessor
from numpy import array
from numpy import iscomplexobj
from numpy import ndarray
from packaging import version

if TYPE_CHECKING:
    from collections.abc import Mapping
    from collections.abc import MutableMapping
    from pathlib import Path

try:
    USE_ARRAY2DOUBLE_NUMPY: Final[bool] = version.parse(
        get_version_of("matlabengine")
    ) >= version.parse("9.12")
except PackageNotFoundError:
    if "READTHEDOCS" in os.environ:
        # This is a workaround for building the doc on readthedocs,
        # because sphinx cannot mock the package for importlib.
        pass


class MatlabDataProcessor(DataProcessor):
    """A Matlab data processor.

    Convert GEMSEO format to Matlab format.

    Examples:
        >>> # Build a new instance
        >>> proc = MatlabDataProcessor()
        >>> # initial python data
        >>> d = {"x": array([2]), "y": array([2j], dtype="complex")}
        >>> # process data to matlab format
        >>> res = proc.pre_process_data(d)
        >>> print(res)
        >>>
        >>> # initial data in matlab format
        >>> d = {"y": double([2, 3]), "x": double([2j], is_complex=True)}
        >>> # process to Python format
        >>> res = proc.post_process_data(d)
        >>> print(res)
    """

    def pre_process_data(
        self, data: Mapping[str, ndarray]
    ) -> Mapping[str, matlab.double]:
        """Transform data from GEMSEO to Matlab.

        The function takes a dict of ndarray and return
        a dict of matlab.double.

        Args:
            data: The input data.

        Returns:
            The data with matlab array types.
        """
        processed_data = {}

        for name, values in data.items():
            if isinstance(values, matlab.double):
                processed_data[name] = values
            else:
                processed_data[name] = array2double(values)

        return processed_data

    def post_process_data(
        self, data: Mapping[str, matlab.double]
    ) -> Mapping[str, ndarray]:
        """Transform the output data from Matlab to GEMSEO.

        Args:
            data: The data with matlab arrays.

        Returns:
            The data with numpy arrays.
        """
        processed_data = {}

        for name, values in data.items():
            if isinstance(values, ndarray):
                processed_data[name] = values.copy()
            else:
                processed_data[name] = double2array(values)

        return processed_data


def load_matlab_file(
    file_path: str | Path,
) -> Mapping[str, matlab.double]:
    """Read .mat file and convert it to usable format for Matlab.

    Args:
        file_path: The path to a .mat file.

    Returns:
        The dict of matlab.double.
    """
    row_data = scipy.io.loadmat(str(file_path))
    clean_data = {}
    for parameter in row_data:
        if parameter not in ["__header__", "__globals__", "__version__"]:
            clean_data[parameter] = array2double(row_data[parameter])

    return clean_data


def save_matlab_file(
    data: MutableMapping[str, ndarray],
    file_path: str | Path = "output_dict",
    **options: bool | str,
) -> None:
    """Save data to a MATLAB-style *.mat* file.

    Args:
        data: The data of the form ``{data_name: data_value}``.
        file_path: The path of the file where to save the data.
        **options: The options of ``scipy.io.savemat``.

    Raises:
        ValueError: If some values in ``data`` are not NumPy arrays.
    """
    data_copy = copy(data)
    for data_name, data_value in data_copy.items():
        if isinstance(data_value, matlab.double):
            data_copy[data_name] = double2array(data_value)
        elif not isinstance(data_value, ndarray):
            msg = "The data must be composed of NumPy arrays only."
            raise TypeError(msg)
    scipy.io.savemat(str(file_path), data_copy, **options)


def array2double(data_array: ndarray) -> matlab.double:
    """Convert a ndarray into a matlab.double.

    May lead to memory leaks for matlabengine < 9.12.

    Args:
        data_array: The numpy array to be converted.

    Returns:
        The matlab.double value.
    """
    if USE_ARRAY2DOUBLE_NUMPY:
        return __array2double_numpy(data_array)
    return __array2double_tolist(data_array)


def __array2double_tolist(data_array: ndarray) -> matlab.double:
    """Convert a ndarray into a matlab.double.

    May lead to memory leaks by using ``.tolist()`` method.

    Args:
        data_array: The numpy array to be converted.

    Returns:
        The matlab.double value.
    """
    is_cmplx = iscomplexobj(data_array)

    if len(data_array.shape) == 1:
        return matlab.double(data_array.tolist(), is_complex=is_cmplx)[0]
    return matlab.double(data_array.tolist(), is_complex=is_cmplx)


def __array2double_numpy(data_array: ndarray) -> matlab.double:
    """Convert a ndarray into a matlab.double.

    Args:
        data_array: The numpy array to be converted.

    Returns:
        The matlab.double value.
    """
    is_cmplx = iscomplexobj(data_array)

    # Data type conversion if
    # the array contains integers
    # or the array has a type like '<f4'.
    #
    # matlab.double must get ndarray of type 'f' (or complex)
    arr = data_array if is_cmplx else data_array.astype(float)

    if len(arr.shape) == 1:
        return matlab.double(arr, is_complex=is_cmplx)[0]
    return matlab.double(arr, is_complex=is_cmplx)


def double2array(
    matlab_double: matlab.double,
) -> ndarray:
    """Turn a matlab double into ndarray.

    Args:
        matlab_double: The matlab.double values.

    Returns:
        The array of values.
    """
    d_type = "complex" if iscomplexobj(matlab_double) else None

    # note here that we can treat string as well
    # -> we put string into an array as float
    #    (otherwise the array has no shape)
    if isinstance(matlab_double, (float, str, complex)):
        output = array([matlab_double], dtype=d_type)
    else:
        output = array(matlab_double, dtype=d_type)

    if output.shape[0] == 1 and len(output.shape) > 1:
        output = output[0]

    return output


def convert_array_from_matlab(
    data: Mapping[str, matlab.double],
) -> Mapping[str, ndarray]:
    """Convert dict of matlab.output to dict of ndarray.

    Args:
        data: The dict of matlab.double.

    Returns:
        The dict of ndarray.
    """
    output_values = {}
    for matlab_key in data:
        current_value = data[matlab_key]
        output_values[matlab_key] = double2array(current_value)
    return output_values


def convert_array_to_matlab(
    data: Mapping[str, ndarray],
) -> Mapping[str, matlab.double]:
    """Convert gems dict of ndarray to dict of matlab.double.

    Args:
        data: The dict of ndarray.

    Returns:
        The dict of matlab.double.
    """
    output = {}
    for keys in data:
        current_data = data[keys]
        if len(current_data) != 1:
            output[keys] = array2double(current_data)
        else:
            if iscomplexobj(current_data):
                output[keys] = complex(current_data)
            else:
                output[keys] = float(current_data)

    return output
