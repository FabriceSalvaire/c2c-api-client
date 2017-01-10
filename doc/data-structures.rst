Geometry Data Structures
========================

Coordinates are in Mercator **espg:3857** projection.

Point Geometry
~~~~~~~~~~~~~~

.. code-block::

    geom : or null
        coordinates : [x, y]
        type : 'Point'
    version : int

Route Geometry
~~~~~~~~~~~~~~

.. code-block::

    geom : {POINT_GEOMETRY}
    geom_detail :
         coordinates : [[x, y], ...]
	 type : 'LineString'
    version : int

Locale Data Structures
======================

Title Locale
~~~~~~~~~~~~

* **lang** : string code language e.g. 'fr'
* **title** : string
* **version** : int

Outing Locale
~~~~~~~~~~~~

* **lang** : 'fr'
* **summary** : string or null
* **title** : 'string
* **version** : 1

Route Locale Short
~~~~~~~~~~~~~~~~~~

* **lang** : string code language e.g. 'fr'
* **summary** : string
* **title_prefix** : string
* **title** : string
* **version** : int

Route Locale
~~~~~~~~~~~~

* **description** : string
* **external_resources** : string
* **gear** : null
* **lang** : string code language e.g. 'fr'
* **remarks** : string
* **route_history** : string
* **summary** : null
* **title** : string
* **title_prefix** : string
* **topic_id** : int
* **version** : int

Waypoint Locale
~~~~~~~~~~~~~~~

* **lang** : string code language e.g. 'fr'
* **summary** : string
* **title** : string
* **version** : int

Other Data Structures
======================

Author
~~~~~~

* **name** : e.g. 'John Doe'
* **user_id** : int

Typed Data Structures
=====================

Area
~~~~

* **area_type** : string e.g. 'country', 'range', 'admin_limits'
* **available_langs** : null
* **document_id** : int
* **locales** : [{TITLE_LOCAL}]
* **protected** : bool
* **type** : 'a'
* **version** : int

Image
~~~~~

* **areas** : []
* **author** : null
* **available_langs** : ['fr']
* **document_id** : int
* **filename** : string filename e.g. 'foo.jpg'
* **geometry** : {POINT_GEOMETRY}
* **locales** : [{TITLE_LOCAL}]
* **protected** : bool
* **type** : 'i'
* **version** : int

Map
~~~

* **available_langs** : null
* **code** : '3145ET'
* **document_id** : int
* **editor** : 'IGN'
* **locales** : [{TITLE_LOCALE}]
* **protected** : bool
* **type** : 'm'
* **version** : int

Outing
~~~~~~

* **activities** : ['rock_climbing']
* **areas** : [{AREA}]
* **author** : {Author}
* **available_langs** : ['fr']
* **date_end** : string date e.g. '2016-12-31'
* **date_start** : string date e.g. '2016-12-31'
* **document_id** : int
* **elevation_max** : null
* **geometry** : {POINT_GEOMETRY}
* **height_diff_up** : null
* **locales** : [{OUTING_LOCALE}]
* **protected** : bool
* **quality** : 'fine'
* **type** : 'o'
* **version** : int

Route Short
~~~~~~~~~~~

* **activities** : list of string e.g. ['rock_climbing']
* **aid_rating** :
* **areas** : [{AREA}]
* **available_langs** : list of code languages e.g. ['it', 'es', 'fr']
* **document_id** : int
* **elevation_max** : int
* **engagement_rating** : string e.g. 'I'
* **equipment_rating** : string e.g. 'P1'
* **exposition_rock_rating** :
* **geometry** : {POINT_GEOMETRY}
* **global_rating** : string e.g. 'AD+'
* **height_diff_difficulties** : int
* **height_diff_up** : int
* **locales** : [{ROUTE_LOCALE_SHORT}]
* **orientations** : list of string e.g. ['SW']
* **protected** : bool
* **quality** : string
* **risk_rating** : null
* **rock_free_rating** : string e.g. '5a'
* **rock_required_rating** : string e.g. '4c'
* **type** : 'r'
* **version** : int

Route
~~~~~

* **activities** : ['rock_climbing']
* **aid_rating** : null
* **areas** : [{AREA}]
* **available_langs** : list of code languages e.g. ['fr', 'es']
* **climbing_outdoor_type** : 'multi'
* **configuration** : ['pillar']
* **difficulties_height** : null
* **document_id** : int
* **durations** : ['1']
* **elevation_max** : int
* **elevation_min** : int
* **engagement_rating** : string e.g. 'II'
* **equipment_rating** : string e.g. 'P1'
* **exposition_rock_rating** : string e.g. 'E1'
* **geometry** : {ROUTE_GEOMETRY}
* **glacier_gear** : string e.g. 'no'
* **global_rating** : string e.g. 'TD-'
* **height_diff_access** : null
* **height_diff_difficulties** : int
* **height_diff_down** : null
* **height_diff_up** : int
* **lift_access** : null
* **locales** : [{ROUTE_LOCALE}]
* **main_waypoint_id** : int
* **maps** : [{MAP}]
* **orientations** : ['W']
* **protected** : bool
* **quality** : 'medium'
* **risk_rating** : null
* **rock_free_rating** : string e.g. '6a+'
* **rock_required_rating** : string e.g. '6a'
* **rock_types** : ['calcaire']
* **route_types** : ['traverse']
* **type** : 'r'
* **version** : int

.. code-block::

    associations :
        articles : []
        books : []
        images : [{IMAGE}]
        recent_outings :
            total : int
            documents : [{OUTING}]
        routes : []
        waypoints : [{WAYPOINT}]
        xreports : []

Waypoint
~~~~~~~~

* **document_id** : int
* **areas** : [{AREA}]
* **available_langs** : ['fr']
* **version** : int
* **waypoint_type** : e.g. 'climbing_outdoor', 'summit'
* **quality** : 'medium'
* **geometry** : {POINT_GEOMETRY}
* **locales** : [{WAYPOINT_LOCALE}]
* **type** : 'w'
* **elevation** : int
* **protected** : bool

Error JSON Response
===================

* **errors** : [{ERROR}]
* **status** : 'error'

Error
~~~~~

* **description** : string e.g. 'Login failed'
* **location** : string e.g. 'body'
* **name** : string e.g. 'user'

Login JSON Response
===================

JSON Response to a successfully login:

* **expire** : unix timestamp
* **forum_username** : string e.g. 'John_Doe'
* **id** : int
* **lang** : string code language e.g. 'fr'
* **name** : string e.g. 'John Doe'
* **redirect_internal** : url e.g. 'https://forum.camptocamp.org/session/sso_login?sig=32...'
* **roles** : []
* **token** : string
* **username** : string e.g. 'johndoe'

Search JSON Response
====================

.. code-block::

    routes
        total : number of items
        documents : [{ROUTE_SHORT}]
