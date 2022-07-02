####################################################################################################
#
# C2cApiClient - A Python client for the camptocamp.org API
# Copyright (C) 2017 Salvaire Fabrice
# Contact: http://www.fabrice-salvaire.fr
# SPDX-License-Identifier: AGPL-3.0-only
#
####################################################################################################

__all__ = ['GeoCoordinate']

####################################################################################################

import math

from pyproj import Transformer

####################################################################################################

class GeoCoordinate:

    ##############################################

    def __init__(self, latitude: float, longitude: float) -> None:
        self._latitude = latitude
        self._longitude = longitude

        # axis order in the x,y or lon,lat order
        transformer = Transformer.from_crs('EPSG:4326', 'EPSG:3857', always_xy=True)
        self._x, self._y = transformer.transform(self._longitude, self._latitude)

    ##############################################

    @property
    def wgs84(self) -> list:
        return self._x, self._y

    ##############################################

    def bbox(self, radius) -> list:
        radius = radius * 1000
        return (
            self._x - radius,
            self._y - radius,
            self._x + radius,
            self._y + radius,
        )

    ##############################################

    def distance(self, xy, factor=10):
        x, y = xy
        d =  math.sqrt((self._x - x)**2 + (self._y - y)**2) / 1000
        return math.trunc(d * factor) / factor
