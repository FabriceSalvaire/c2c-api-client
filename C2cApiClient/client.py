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

from pathlib import Path
import datetime
import json
import logging
import math

import requests

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ClientLogin:

    ##############################################

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

####################################################################################################

class LoginData:

    ##############################################

    def __init__(self, json: dict) -> None:
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
        return datetime.datetime.now() >= self._expire

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

class SearchSettings:

    ##############################################

    def __init__(self,
                 language='fr',
                 limit=7,
                 area=False,
                 article=False,
                 book=False,
                 image=False,
                 map_=False,
                 outing=False,
                 route=False,
                 userprofile=False,
                 waypoint=False,
                 xreport=False,
    ):

        self._limit = limit
        self._language = language

        self._area = area
        self._article = article
        self._book = book
        self._image = image
        self._map = map_
        self._outing = outing
        self._route = route
        self._userprofile = userprofile
        self._waypoint = waypoint
        self._xreport = xreport

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
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        self._area = value


    @property
    def article(self):
        return self._article

    @article.setter
    def article(self, value):
        self._article = value


    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, value):
        self._book = value


    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value


    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        self._map = value


    @property
    def outing(self):
        return self._outing

    @outing.setter
    def outing(self, value):
        self._outing = value


    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, value):
        self._route = value


    @property
    def userprofile(self):
        return self._userprofile

    @userprofile.setter
    def userprofile(self, value):
        self._userprofile = value


    @property
    def waypoint(self):
        return self._waypoint

    @waypoint.setter
    def waypoint(self, value):
        self._waypoint = value


    @property
    def xreport(self):
        return self._xreport

    @xreport.setter
    def xreport(self, value):
        self._xreport = value

    ##############################################

    @property
    def type_letters(self):
        letters = []
        if self._area:
            letters.append('a')
        if self._article:
            letters.append('c')
        if self._book:
            letters.append('b')
        if self._image:
            letters.append('i')
        if self._map:
            letters.append('m')
        if self._outing:
            letters.append('o')
        if self._route:
            letters.append('r')
        if self._userprofile:
            letters.append('u')
        if self._xreport:
            letters.append('x')
        if self._waypoint:
            letters.append('w')
        return ','.join(letters)

####################################################################################################

class VersionedObject:

    ##############################################

    def __init__(self, json):
        self._version = json['version']

    ##############################################

    @property
    def version(self):
        return self._version

####################################################################################################

class TypedObject(VersionedObject):

    ##############################################

    def __init__(self, json):
        VersionedObject.__init__(self, json)
        self._type = json['type']

    ##############################################

    @property
    def type(self):
        return self._type

####################################################################################################

class Client:

    _logger = _module_logger.getChild('Client')

    API_URL = 'https://api.camptocamp.org'
    WWW_URL = 'https://www.camptocamp.org'
    LIMIT_MAX = 100

    TYPE_TO_URL = {
        'a': 'areas',
        'c': 'articles',
        'b': 'books',
        'i': 'images',
        'm': 'maps',
        'o': 'outings',
        'r': 'routes',
        'u': 'userprofiles',
        'x': 'xreports',
        'w': 'waypoints',
    }

    ##############################################

    def __init__(self, client_login=None):
        self._login_data = None
        self._client_login = client_login
        if client_login is not None:
            self.login()

    ##############################################

    @classmethod
    def _url_for(cls, base: str, args: list) -> str:
        # return base + '/' + '/'.join(args)
        return base + ''.join(f'/{_}' for _ in args)

    @classmethod
    def url_for(cls, *args) -> str:
        return cls._url_for(cls.API_URL, args)

    @classmethod
    def www_url_for(cls, *args) -> str:
        return cls._url_for(cls.WWW_URL, args)
    
    ##############################################

    @classmethod
    def _make_url_for_document(cls, document):
        return cls.url_for(self.TYPE_TO_URL[document['type']], str(document['document_id']))

    ##############################################

    def _headers_for_authorization(self) -> dict:
        headers = {}
        if self.logged:
            headers['Authorization'] = 'JWT token="{}"'.format(self._login_data.token)
        return headers

    ##############################################

    def _check_json_response(self, response):
        response.raise_for_status()
        json = response.json()
        # self._logger.debug(json)
        if 'status' in json and json['status'] == 'error':
            # {'status': 'error', 'errors': [{'name': 'user', 'location': 'body', 'description': 'Login failed'}]}
            for error in json['errors']:
                self._logger.error(error['description'])
            return None
        else:
            return json

    ##############################################

    @classmethod
    def _get(cls, url: list | str, verbose: bool=True, **kwargs) -> dict:
        if not isinstance(url, (list, tuple)):
            url = (url,)
        url = cls.API_URL + ''.join(f'/{_}' for _ in url)
        r = requests.get(url, params=kwargs)
        if r.status_code != requests.codes.ok:
            raise NameError(f"API request failed {r.url}")
        if verbose:
            cls._logger.info(f"API request {r.url}")
        return r.json()

    ##############################################

    def _list(self, url: str, **kwargs) -> dict:
        data = self._get(url, **kwargs, limit=0)
        number_of_entries = data['total']
        retrieved_number_of_entries = 0
        number_of_queries = int(math.ceil(number_of_entries / self.LIMIT_MAX))
        print(f'number of queries {number_of_queries}')
        documents = []
        for i in range(0, number_of_queries):
            data = self._get(url, **kwargs, offset=i*self.LIMIT_MAX, limit=self.LIMIT_MAX)
            retrieved_number_of_entries += len(data['documents'])
            print(f'Retrieved {retrieved_number_of_entries}/{number_of_entries} entries')
            documents += data['documents']
        return documents

    ##############################################

    def _post_put(self, url, payload, requests_method):
        if not self.logged:
            return
        self.update_login()
        r = requests_method(url, headers=self._headers_for_authorization(), json=payload)
        r.raise_for_status()

    ##############################################

    def _post(self, url, payload):
        self._post_put(url, payload, requests.post)

    ##############################################

    def _put(self, url, payload):
        self._post_put(url, payload, requests.put)

    ##############################################

    @classmethod
    def health(cls):
        """Query the health of the REST API service"""
        return cls._get('health')

    ##############################################

    def login(self, remember: bool=True, discourse: bool=True) -> None:
        self._logger.info('Login to camptocamp.org with user {} ...'.format(self._client_login.username))
        payload = {
            'username': self._client_login.username,
            'password': self._client_login.password,
            'discourse': discourse,
            #'remember': remember,
        }
        url = self.url_for('users', 'login')
        self._logger.info(f'Post {url} {payload}')
        r = requests.post(url, json=payload)
        json = r.json()
        self._login_data = None
        if json is not None:
            if json.get('status') == 'error':
                self._logger.error(f"Login failed {json}")
            else:
                self._login_data = LoginData(json)
                self._logger.info("Logged successfully, connection will expire at {}".format(self._login_data.expire))

    ##############################################

    @property
    def logged(self):
        return self._login_data is not None

    ##############################################

    def update_login(self):
        if self.logged and self._login_data.expired:
            self._logger.info("Login expired")
            self.login()

    ##############################################

    def area(self, document_id):
        url = self.url_for('areas', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def article(self, document_id):
        url = self.url_for('articles', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def image(self, document_id):
        url = self.url_for('images', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def map(self, document_id):
        url = self.url_for('maps', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def outing(self, document_id):
        url = self.url_for('outings', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def route(self, document_id):
        # https://api.camptocamp.org/routes/168658?cook=fr
        return self._get(('routes', document_id), verbose=True)

    ##############################################

    def user_profile(self, user_id=None):
        if user_id is None:
            if self.logged:
                user_id = self._login_data.id
            else:
                return None
        url = self.url_for('profiles', str(user_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def xreport(self, document_id):
        url = self.url_for('xreports', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def waypoint(self, document_id):
        url = self.url_for('waypoints', str(document_id))
        r = requests.get(url)
        return self._check_json_response(r)

    ##############################################

    def search(self, search_string, settings=None):

        # https://api.camptocamp.org/search?q=sonia&t=w,r,c,b&limit=7

        """Search documents

        cf. https://github.com/c2corg/v6_api/blob/master/c2corg_api/views/search.py

        Request:
            `GET` `/search?q=...[&lang=...][&limit=...][&t=...]`

        Parameters:
            `q=...`
            The search word.

            `lang=...` (optional)
            When set only the given locale will be included (if available).
            Otherwise all locales will be returned.

            `limit=...` (optional)
            How many results should be returned per document type
            (default: 10). The maximum is 50.

            `t=...` (optional)
            Which document types should be included in the search. If not
            given, all document types are returned. Example: `...&t=w,r`
            searches only for waypoints and routes.
        """

        if settings is None:
            settings = SearchSettings()
        url = self.url_for('search')
        parameters = {
            'q': search_string,
            'pl': settings.language, # lang ???
            'limit': settings.limit,
            't': settings.type_letters,
        }
        r = requests.get(url, params=parameters)
        return self._check_json_response(r)

    ##############################################

    def search_route(self, **kwargs):
        # https://www.camptocamp.org/routes?act=mountain_climbing,snow_ice_mixed&bbox=819448,5774967,844631,5801415&limit=100&grat=F,PD%2B&sort=global_rating
        parameters = {}
        if 'bbox' in kwargs:
            parameters['bbox'] = ','.join([str(_) for _ in kwargs['bbox']])
        return self._list('routes', **parameters, verbose=True)
        
    ##############################################

    def post(self, document):
        url = self._make_url_for_document(document)
        self._post(url, document)

    ##############################################

    def update(self, message, document):
        url = self._make_url_for_document(document)
        payload = {'message': message, 'document': document}
        self._put(url, payload)

    ##############################################

    # : dict | list
    @classmethod
    def write_json(cls, data, path: str | Path) -> None:
        with open(path, 'w') as fh:
            json_data = json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )
            fh.write(json_data)

    ##############################################

    @classmethod
    def read_json(cls, path: str | Path):
        with open(path) as fh:
            return json.load(fh)

####################################################################################################

class SeracDocument:

    ##############################################

    def __init__(self, data) -> None:
        self._data = data

    ##############################################

    @property
    def json(self):
        return self._data

    ##############################################

    def xpath(self, *args):
        data = self._data
        for key in args:
            data = data[key]
        return data

    ##############################################

    @property
    def avalanche_level(self) -> str:
        return self.xpath('avalanche_level')

    @property
    def avalanche_slope(self) -> str:
        return self.xpath('avalanche_slope')

    @property
    def date(self) -> str:
        return datetime.strptime(self.xpath('date'), '%Y-%m-%d')

    @property
    def document_id(self) -> int:
        return self.xpath('document_id')

    @property
    def elevation(self) -> int:
        return self.xpath('elevation')

    @property
    def event_activity(self) -> str:
        return self.xpath('event_activity')

    @property
    def event_type(self) -> str:
        return self.xpath('event_type')

    @property
    def nb_impacted(self) -> int:
        return self.xpath('nb_impacted')

    @property
    def nb_participants(self) -> int:
        return self.xpath('nb_participants')

    @property
    def rescue(self) -> bool:
        _ = self.xpath('rescue')
        # Fimxe: ok???
        if _ is None:
            return False
        return _

    @property
    def severity(self) -> str:
        return self.xpath('severity')

    @property
    def coordinate(self) -> str:
        # "{\"type\": \"Point\", \"coordinates\": [713257.9299571944, 5623130.402088347]}"
        json_data = self.xpath('geometry', 'geom')
        if json_data is not None:
            data = json.loads(json_data)
            return data['coordinates']
        return None

####################################################################################################

class RouteDocument:

    ##############################################

    def __init__(self, data) -> None:
        self._data = data

    ##############################################

    @property
    def json(self):
        return self._data

    ##############################################

    def xpath(self, *args):
        data = self._data
        # try:
        for key in args:
            data = data[key]
        return data
        # except KeyError:
        #     return None

    def protected_xpath(self, *args):
        try:
            return self.xpath(*args)
        except KeyError:
            return ''

    ##############################################

    @property
    def document_id(self) -> int:
        return self.xpath('document_id')

    @property
    def document_url(self) -> int:
        return Client.url_for('routes', self.document_id)

    @property
    def document_www_url(self) -> int:
        return Client.www_url_for('routes', self.document_id)

    ##############################################

    @property
    def activities(self) -> list:
        return self.xpath('activities')

    @property
    def aid_rating(self) -> list:
        return self.protected_xpath('aid_rating')

    @property
    def climbing_outdoor_type(self) -> list:
        return self.protected_xpath('climbing_outdoor_type')
 
    @property
    def configuration(self) -> list:
        return self.protected_xpath('configuration')

    @property
    def difficulties_height(self) -> list:
        return self.protected_xpath('difficulties_height')

    @property
    def durations(self) -> list:
        return self.protected_xpath('durations')

    @property
    def equipment_rating(self) -> list:
        return self.protected_xpath('equipment_rating')

    @property
    def exposition_rock_rating(self) -> list:
        return self.protected_xpath('exposition_rock_rating')

    @property
    def elevation_max(self) -> list:
        return self.protected_xpath('elevation_max')

    @property
    def elevation_min(self) -> list:
        return self.protected_xpath('elevation_min')

    @property
    def engagement_rating(self) -> list:
        return self.protected_xpath('engagement_rating')

    @property
    def glacier_gear(self) -> list:
        return self.protected_xpath('glacier_gear')

    @property
    def global_rating(self) -> list:
        return self.protected_xpath('global_rating')

    @property
    def height_diff_difficulties(self) -> list:
        return self.protected_xpath('height_diff_difficulties')

    @property
    def height_diff_down(self) -> list:
        return self.protected_xpath('height_diff_down')

    @property
    def height_diff_up(self) -> list:
        return self.protected_xpath('height_diff_up')

    @property
    def hiking_mtb_exposition(self) -> list:
        return self.protected_xpath('hiking_mtb_exposition')

    @property
    def hiking_rating(self) -> list:
        return self.protected_xpath('hiking_rating')

    @property
    def ice_rating(self) -> list:
        return self.protected_xpath('ice_rating')

    @property
    def lift_acces(self) -> list:
        return self.protected_xpath('lift_acces')

    @property
    def mixed_rating(self) -> list:
        return self.protected_xpath('mixed_rating')

    @property
    def orientations(self) -> list:
        return self.protected_xpath('orientations')

    @property
    def risk_rating(self) -> list:
        return self.protected_xpath('risk_rating')

    @property
    def rock_free_rating(self) -> list:
        return self.protected_xpath('rock_free_rating')

    @property
    def rock_required_rating(self) -> list:
        return self.protected_xpath('rock_required_rating')

    @property
    def rock_types(self) -> list:
        return self.protected_xpath('rock_types')

    @property
    def route_types(self) -> list:
        return self.protected_xpath('route_types')

    @property
    def quality(self) -> list:
        return self.xpath('quality')

    ##############################################

    @property
    def coordinate(self) -> str:
        # "{\"type\": \"Point\", \"coordinates\": [713257.9299571944, 5623130.402088347]}"
        json_data = self.xpath('geometry', 'geom')
        if json_data is not None:
            data = json.loads(json_data)
            return data['coordinates']
        return None

    ##############################################

    @property
    def locale(self) -> dict:
        locales = self.xpath('locales')
        for locale in locales:
            for lang in ('fr', 'it', 'de'):
                if locale['lang'] == lang:
                    return locale
        return None
 
    @property
    def title(self) -> str:
        locale = self.locale
        if locale:
            return locale['title_prefix'] + ' — ' + locale['title']
        return ''

    @property
    def gear(self) -> str:
        locale = self.locale
        if locale:
            return locale['gear']
        return ''

    ##############################################

    @property
    def number_of_outings(self) -> int:
        return self.xpath('associations', 'recent_outings', 'total')

    @property
    def number_of_images(self) -> int:
        return len(self.xpath('associations', 'images'))

    @property
    def number_of_accidents(self) -> int:
        return len(self.xpath('associations', 'xreports'))
