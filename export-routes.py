####################################################################################################

from pathlib import Path
import json
import logging
import math
import pprint
 
####################################################################################################

# FORMAT = '%(asctime)s - %(name)s - %(module)s.%(levelname)s - %(message)s'
FORMAT = '\033[1;32m%(asctime)s\033[0m - \033[1;34m%(name)s.%(funcName)s\033[0m - \033[1;31m%(levelname)s\033[0m - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

####################################################################################################

from C2cApiClient.client import Client, ClientLogin, SearchSettings, RouteDocument
from C2cApiClient.XlsxDocument import XlsxDocument
from C2cApiClient.projection import GeoCoordinate

####################################################################################################

client = Client()

####################################################################################################

arolla_coordinate = GeoCoordinate(latitude=46.02789, longitude=7.48600)

cache_directory = Path('cache')
cache_directory.mkdir(exist_ok=True)
json_cache = cache_directory.joinpath('cache.json')

if json_cache.exists():
    documents = client.read_json(json_cache)
else:
    bbox = arolla_coordinate.bbox(50)
    print('Bounding box:', bbox)
    documents = client.search_route(bbox=bbox)
    client.write_json(documents, json_cache)

print('Number of documents:', len(documents))
# pprint.pprint(documents)

if False:
    activities = set()
    for document in documents:
        activities |= set(document['activities'])
    print(activities)

excluded_activities = set((
    'ice_climbing',
    'mountain_biking',
    'skitouring',
    'snowshoeing',
    'via_ferrata',
))

columns_titles = (
    'D@Arolla [km]',
    'Id',
    'Titre',
    'Activités',

    '#Sorties', # Dernières
    '#Images',
    '#XR',

    'Orientation',

    'Cotations',
    'Engagement',
    'Risque',

    # 'Altitude Min",
    "Dénivelé de l'approche",
    'Altitude Max',
    'Dénivelé positif',
    'Dénivelé négatif',
    'Altitude du début des difficultés',
    'Dénivelé des difficultés',

    'hiking_mtb_exposition',
    'hiking_rating',

    "Type d'itinéraire",
    'Durée',
    'Type de rocher',
    'Type de voie',
    'Configuration',

    'Cotation libre',
    'Cotation obligatoire',
    'Cotation Artif.',

    'Équipement',
    'Exposition',
    
    'Matériel glacier',
)

xlsx_document = XlsxDocument(columns_titles)

# sheet.column_dimensions['A'].width = 30

sorted_documents = sorted(
    documents,
    key=lambda _: arolla_coordinate.distance(RouteDocument(_).coordinate),
)

for short_document in sorted_documents:
    short_document = RouteDocument(short_document)
    if set(short_document.activities).isdisjoint(excluded_activities):
        id_ = short_document.document_id
        json_cache = cache_directory.joinpath(f'{id_}.json')
        if json_cache.exists():
            print(f'Read {id_}')
            document = client.read_json(json_cache)
        else:
            print(f'Write {id_}')
            document = client.route(short_document.document_id)
            client.write_json(document, json_cache)
        document = RouteDocument(document)
        print('='*100)
        # pprint.pprint(document)
        print(document.activities)
        print(document.title)
        def join_list(a_list):
            if isinstance(a_list, list):
                return ', '.join(a_list)
            else:
                return a_list
        values = (
            arolla_coordinate.distance(document.coordinate),
            str(document.document_id),
            document.title,
            ', '.join(sorted(document.activities)),

            document.number_of_outings,
            document.number_of_images,
            document.number_of_accidents,

            join_list(document.orientations),

            document.global_rating,
            document.engagement_rating,
            document.risk_rating,

            document.elevation_min,
            document.elevation_max,
            document.height_diff_up,
            document.height_diff_down,
            document.difficulties_height,
            document.height_diff_difficulties,

            document.hiking_mtb_exposition,
            document.hiking_rating,

            join_list(document.route_types),
            join_list(document.durations),
            join_list(document.rock_types),
            document.climbing_outdoor_type,
            join_list(document.configuration),

            document.rock_free_rating,
            document.rock_required_rating,
            document.aid_rating,
            document.equipment_rating,
            document.exposition_rock_rating,

            document.gear,
        )
        xlsx_document.add_row(values)
        xlsx_document.cell_for_title('Titre').hyperlink = document.document_www_url
        xlsx_document.cell_for_title('Id').hyperlink = document.document_url

xlsx_filename = 'routes.xlsx'
xlsx_document.save(xlsx_filename)
