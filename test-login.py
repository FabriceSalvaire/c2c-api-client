####################################################################################################

import logging

import yaml

####################################################################################################

# FORMAT = '%(asctime)s - %(name)s - %(module)s.%(levelname)s - %(message)s'
FORMAT = '\033[1;32m%(asctime)s\033[0m - \033[1;34m%(name)s.%(funcName)s\033[0m - \033[1;31m%(levelname)s\033[0m - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

####################################################################################################

from C2cApiClient import *

####################################################################################################

with open('mylogin.yaml') as fh:
    login_data = yaml.safe_load(fh)
client_login = ClientLogin(**login_data)

print(Client.health())

client = Client(client_login=client_login)
print(client.user_profile())
