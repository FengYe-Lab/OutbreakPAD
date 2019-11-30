#!/usr/bin/env python3
#
# Copyright (C) 2016  Carlos Henrique Silva <carlosqsilva@outlook.com>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .results import PlotCharts
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib as mpl

import numpy as np
import pandas as pd

plt.style.use('ggplot')
mpl.rcParams['lines.markersize'] = 4


class spc(object):

    _title = 'SPC : Statistical Process Control Charts for Humans'

    def __init__(self, data=None, newdata=None):

#        if isinstance(data, pd.DataFrame):
#            data = data.values
#        if isinstance(newdata, pd.DataFrame):
#            newdata = newdata.values

        try:
            self.size = len(data[0])
        except:
            if not isinstance(data[0], (list, tuple, np.ndarray)):
                self.size = 1

        self.data = data
        self.newdata = newdata
        self.layers = []
        self.points = None
        self.summary = []

    def __repr__(self):
        self.make()
      #  plt.show()
        return "%r" % self.summary

    def __getitem__(self, i):
        return self.summary[i]

    def __iter__(self):
        for x in self.summary:
            yield x

    def get_subplots(self):

        if len(self.layers) > 1:
            return self.subplots[0]
        return self.subplots

    def save(self, filename, **kargs):
        if len(self.summary) == 0:
            self.make()

        self.fig.savefig(filename, **kargs)

    def drop(self, *args):
        self.data = np.delete(self.data, args, axis=0)

    def make(self):

        num_layers = len(self.layers)
        if num_layers == 0:
 #           plt.show()
            return 

        self.fig, *self.subplots = plt.subplots(num_layers)
        self.fig.canvas.set_window_title(self._title)
 #       for layer in self.layers:
        for layer, ax in zip(self.layers, self.get_subplots()):
            summary = {}

            values, center, lcl, ucl, title = layer.plot(self.data, self.size, self.newdata)
            PlotCharts(ax, values, center, lcl, ucl, title)

            summary['name'] = title
            summary['values'] = values
            summary['lcl'] = lcl
            summary['ucl'] = ucl
            summary['center'] = center

            if self.points is not None:
                summary['violation-points'] = self.points.plot_violation_points(ax, values, center, ucl)

            self.summary.append(summary)

        self.fig.tight_layout()
 #       return self.summary
