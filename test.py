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
