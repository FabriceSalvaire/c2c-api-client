####################################################################################################
#
# C2cApiClient - A Python client for the camptocamp.org API
# Copyright (C) 2017 Salvaire Fabrice
# Contact: http://www.fabrice-salvaire.fr
# SPDX-License-Identifier: AGPL-3.0-only
#
####################################################################################################

__all__ = [
    'ClientLogin', 'Client',
    'SearchSettings',
    'RouteDocument',
]

####################################################################################################

from .client import ClientLogin, Client, SearchSettings, RouteDocument
