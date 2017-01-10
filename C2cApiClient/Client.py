####################################################################################################
#
# C2cApiClient - A Pythin client for the camptocamp.org API
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

import datetime
import requests
import logging

####################################################################################################

class ClientLogin:

    ##############################################

    def __init__(self, username, password):

        self.username = username
        self.password = password

####################################################################################################

class SearchSettings:

    ##############################################

    def __init__(self,
                 language='fr',
                 limit=7,
                 waypoint=False,
                 route=False,
                 book=False,
    ):

        self._limit = limit
        self._language = language
        self._waypoint = waypoint
        self._route = route
        self._book = book
        # area a
        # map m
        # c ?

    ##############################################

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        self._limit = value

    @property
    def waypoint(self):
        return self._waypoint

    @waypoint.setter
    def waypoint(self, value):
        self._waypoint = value

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, value):
        self._route = value

    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, value):
        self._book = value

    @property
    def type_letters(self):
        letters = []
        if self._waypoint:
            letters.append('w')
        if self._route:
            letters.append('r')
        if self._book:
            letters.append('b')
        # 'c'
        return ','.join(letters)

####################################################################################################

class LoginData:

    ##############################################

    def __init__(self, json):

        self._language = json['lang']
        self._expire = datetime.datetime.fromtimestamp(json['expire'])
        self._id = json['id']
        self._token = json['token']
        self._forum_username = json['forum_username']
        self._name = json['name']
        self._roles = json['roles']
        self._redirect_interval = json['redirect_internal']
        self._username = json['username']

    ##############################################

    @property
    def language(self):
        return self._language

    @property
    def expire(self):
        return self._expire

    @property
    def expired(self):
        return self._expire >= datetime.datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def token(self):
        return self._token

    @property
    def forum_username(self):
        return self._forum_username

    @property
    def name(self):
        return self._name

    @property
    def roles(self):
        return self._roles

    @property
    def redirect_internal(self):
        return self._redirect_interval

    @property
    def username(self):
        return self._username

####################################################################################################

class Client:

    API_URL = 'https://api.camptocamp.org'

    _logger = logging.getLogger(__name__ + '.Client')

    ##############################################

    def __init__(self, client_login=None):

        self._login_data = None

        self._client_login = client_login
        if client_login is not None:
            self.login()

    ##############################################

    def _make_url(self, *args):

        return self.API_URL + '/' + '/'.join(args)

    ##############################################

    def _check_json_response(self, response):

        json = response.json()
        self._logger.debug(json)
        if 'status' in json and json['status'] == 'error':
            # {'status': 'error', 'errors': [{'name': 'user', 'location': 'body', 'description': 'Login failed'}]}
            for error in json['errors']:
                self._logger.error(error['description'])
            return None
        else:
            return json

    ##############################################

    def login(self, remember=True, discourse=True):

        self._logger.info('Login to camptocamp.org with user {} ...'.format(self._client_login.username))
        payload = {
            'username': self._client_login.username,
            'password': self._client_login.password,
            'remember': remember,
            'discourse': discourse,
        }
        url = self._make_url('users', 'login')
        r = requests.post(url, json=payload)
        json = self._check_json_response(r)
        if json is not None:
            self._login_data = LoginData(json)
            self._logger.info("Logged successfully, connection will expire at {}".format(self._login_data.expire))
        else:
            self._login_data = None

    ##############################################

    @property
    def logged(self):
        return self._login_data is not None

    ##############################################

    def update_login(self):

        if self.logged and self._login_data.expired:
            self.login()

    ##############################################

    def user_profile(self, user_id=None):

        if user_id is None:
            if self.logged:
                user_id = self._login_data.id
            else:
                return None
        url = self._make_url('profiles', str(user_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def route(self, document_id):

        url = self._make_url('routes', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def search(self, search_string, settings=None):

        if settings is None:
            settings = SearchSettings()
        # https://api.camptocamp.org/search?q=...&pl=fr&limit=7&t=w,r,c,b
        url = self._make_url('search')
        parameters = {'q': search_string, 'pl': settings.language, 'limit': settings.limit, 't': settings.type_letters}
        r = requests.get(url, params=parameters)
        return self._check_json_response(r)
