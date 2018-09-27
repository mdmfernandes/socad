# This file is part of SOCAD
# Copyright (C) 2018 Miguel Fernandes
#
# SOCAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SOCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Helpers to handle data."""

import re
from functools import reduce


def get_vars_from_file(fname):
    """Get circuit variables from file and store in a dictionary.

    Arguments:
        fname {str} -- file path

    Returns:
        variables {dict} -- circuit variables
    """
    variables = {}

    # Dictionary with metric prefixes
    prefix_dict = {
        'f': 'e-15',
        'p': 'e-12',
        'n': 'e-9',
        'u': 'e-6',
        'm': 'e-3',
        'k': 'e3',
        'K': 'e3',  # Kilo can be 'k' or 'K' in Cadence
        'M': 'e6',
        'G': 'e9',
        'T': 'e12'
    }

    pattern = r'desVar\(\s*\"(?P<param>\w+)\"\s*(?P<value>\S+)\s*\)'

    with open(fname, 'r') as f:
        content = f.read()

    for match in re.finditer(pattern, content):
        try:  # try to convert value to float
            value = float(match.group('value'))
        except ValueError:
            # If fails, replace the prefixes by the respective exponents
            value = float(reduce((lambda a, kv: a.replace(*kv)), prefix_dict.items(),
                                 match.group('value')))

        # Save to dict
        variables[match.group('param')] = value

    return variables


def store_vars_in_file(variables, fname):
    """Store circuit variables in a file.

    Arguments:
        var {dict} -- dictionary with the circuit variables
        fname {str} -- file name
    """
    with open(fname, 'w') as f:
        # Iterate over the dictionary and save variables to file
        for key, val in variables.items():
            f.write("desVar(\t \"{0}\" {1}\t)\n".format(key, val))


def get_results_from_file(fname):
    """Get simulation results from file and store in a dictionary.

    Arguments:
        fname {str} -- file path
        n_sims {int} -- number of simulations runing in parallel

    Returns:
        results_list {list} -- simulation results in a list of dictionaries
    """
    results = {}

    pattern = r'\s*(?P<param>\S+)\s+(?P<value>\S+)'

    with open(fname, 'r') as f:
        content = f.read()

    for match in re.finditer(pattern, content):
        # Save to dict
        results[match.group('param')] = float(match.group('value'))

    return results
