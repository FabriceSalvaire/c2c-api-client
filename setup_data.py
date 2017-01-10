####################################################################################################
#
# C2cApiClient - A Python client for the camptocamp.org API
# Copyright (C) 2017 Salvaire Fabrice
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

long_description = open('README.rst').read()

setup_dict = dict(
    name='C2cApiClient',
    version='0.1.0',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='A Python client for the camptocamp.org REST API',
    license="AGPLv3",
    keywords="camptocamp.org",
    url='https://github.com/FabriceSalvaire/PySpice',
    packages=['C2cApiClient',
          ],
    long_description=long_description,
    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # "Topic :: ",
        # "Intended Audience :: ",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)", # Affero
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        ],
    requires=[
        'requests',
    ],
)

####################################################################################################
#
# End
#
####################################################################################################
