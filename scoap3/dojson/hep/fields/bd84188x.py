# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""MARC 21 model definition."""

from __future__ import absolute_import, division, print_function

import os

from dojson import utils

from ..model import hep, hep2marc


@hep2marc.over('8564', 'urls')
@utils.for_each_value
@utils.filter_values
def urls2marc(self, key, value):
    """URL to external resource."""
    return {
        'u': value.get('value'),
        'y': value.get('description'),
    }


@hep.over('files', '8564')
@utils.for_each_value
@utils.filter_values
def files(self, key, value):
    if (value.get('x', None)):
        file_extension = value.get('x').lower()
    else:
        tmp, file_extension = os.path.splitext(value.get('u'))
    file_extension = file_extension.lower().strip('.')

    return {
        file_extension: value.get('u')
    }
