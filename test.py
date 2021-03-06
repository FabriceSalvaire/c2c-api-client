####################################################################################################

import logging

# FORMAT = '%(asctime)s - %(name)s - %(module)s.%(levelname)s - %(message)s'
FORMAT = '\033[1;32m%(asctime)s\033[0m - \033[1;34m%(name)s.%(funcName)s\033[0m - \033[1;31m%(levelname)s\033[0m - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

####################################################################################################

from C2cApiClient import Client, ClientLogin, SearchSettings

####################################################################################################

from mylogin import *

from C2cApiClient import Client, ClientLogin
client_login = ClientLogin(username=username, password=password)
client = Client(client_login=client_login)

####################################################################################################

# print(client.user_profile())

# json = client.search('sonia calanque', SearchSettings(route=True))
# documents = json['routes']['documents']
# for document in documents:
#     print('-'*100)
#     print(document['locales'][0]['title'], document['document_id'])

# document = client.route(570170)
# print(document)

####################################################################################################

# https://www.camptocamp.org/waypoints/838941/fr/mont-pourri-fs7
# https://www.camptocamp.org/waypoints/838934/fr/test-c2c-api-fs-waypoint-17
waypoint = client.waypoint(838941)
print('document_id', waypoint['document_id'])
print(waypoint)

version = waypoint['locales'][0]['version']
waypoint['locales'][0]['summary'] = 'update v{}'.format(version + 1)
print(waypoint)

client.update(message='update test', document=waypoint)
