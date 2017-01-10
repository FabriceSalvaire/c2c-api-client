Geometry Data Structures
========================

Coordinates are in Mercator espg:3857 projection.

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

.. code-block::

    lang : string code language e.g. 'fr'
    title : string
    version : int

Route Locale Short
~~~~~~~~~~~~~~~~~~

.. code-block::

    lang : string code language e.g. 'fr'
    summary : string
    title_prefix : string
    title : string
    version : int

Route Locale
~~~~~~~~~~~~

.. code-block::

    description : string
    external_resources : string
    gear : null
    lang : string code language e.g. 'fr'
    remarks : string
    route_history : string
    summary : null
    title : string
    title_prefix : string
    topic_id : int
    version : int

Waypoint Locale
~~~~~~~~~~~~~~~

.. code-block::

    lang : string code language e.g. 'fr'
    summary : string
    title : string
    version : int

Typed Data Structures
=====================

Area
~~~~

.. code-block::

    area_type : string e.g. 'country', 'range'
    available_langs : null
    document_id : int
    locales : [{TITLE_LOCAL}]
    protected : bool
    type : 'a'
    version : int

Image
~~~~~

.. code-block::

    areas : []
    author : null
    available_langs : ['fr']
    document_id : 576750
    filename : string filename e.g. 'foo.jpg'
    geometry : {POINT_GEOMETRY}
    locales : [{TITLE_LOCAL}]
    protected : bool
    type : 'i'
    version : int

Map
~~~

.. code-block::

    available_langs : null
    code : '3145ET'
    document_id : int
    editor : 'IGN'
    locales : [{TITLE_LOCALE}]
    protected : bool
    type : 'm'
    version : int

Route Short
~~~~~~~~~~~

.. code-block::

    activities : list of string e.g. ['rock_climbing']
    aid_rating :
    areas : [{AREA}]
    available_langs : list of code languages e.g. ['it', 'es', 'fr']
    document_id : int
    elevation_max : int
    engagement_rating : string e.g. 'I'
    equipment_rating : string e.g. 'P1'
    exposition_rock_rating :
    geometry : {POINT_GEOMETRY}
    global_rating : string e.g. 'AD+'
    height_diff_difficulties : int
    height_diff_up : int
    locales : [{ROUTE_LOCALE_SHORT}]
    orientations : list of string e.g. ['SW']
    protected : bool
    quality : string
    risk_rating
    rock_free_rating : string e.g. '5a'
    rock_required_rating : string e.g. '4c'
    type : 'r'
    version : int

Route
~~~~~

.. code-block::

    activities : ['rock_climbing']
    aid_rating : null
    areas : [{AREA}]
    available_langs : list of code languages e.g. ['fr', 'es']
    climbing_outdoor_type : 'multi'
    configuration : ['pillar']
    difficulties_height : null
    document_id : int
    durations : ['1']
    elevation_max : int
    elevation_min : int
    engagement_rating : string e.g. 'II'
    equipment_rating : string e.g. 'P1'
    exposition_rock_rating : string e.g. 'E1'
    geometry : {ROUTE_GEOMETRY}
    glacier_gear : string e.g. 'no'
    global_rating : string e.g. 'TD-'
    height_diff_access : null
    height_diff_difficulties : int
    height_diff_down : null
    height_diff_up : int
    lift_access : null
    locales : [{ROUTE_LOCALE}]
    main_waypoint_id : int
    maps : [{MAP}]
    orientations : ['W']
    protected : bool
    quality : 'medium'
    risk_rating : null
    rock_free_rating : string e.g. '6a+'
    rock_required_rating : string e.g. '6a'
    rock_types : ['calcaire']
    route_types : ['traverse']
    type : 'r'
    version : int

    associations :
        articles : []
        books : []
        images : [{IMAGE}]
        recent_outings :
            total : 8
            documents : [{}]
        routes : []
        waypoints : [{WAYPOINT}]
        xreports : []

Waypoint
~~~~~~~~

.. code-block::

    document_id : int
    areas : [{AREA}]
    available_langs : ['fr']
    version : int
    waypoint_type : 'climbing_outdoor'
    quality : 'medium'
    geometry : {POINT_GEOMETRY}
    locales : [{WAYPOINT_LOCALE}]
    type : 'w'
    elevation : int
    protected : bool

Error JSON Response
===================

.. code-block::

    errors : [{ERROR}]
    status : 'error'

Error
~~~~~

.. code-block::

    description : string e.g. 'Login failed'
    location : string e.g. 'body'
    name : string e.g. 'user'

Login JSON Response
===================

JSON Response to a successfully login:

.. code-block::

    expire : unix timestamp
    forum_username : string e.g. 'John_Doe'
    id : int
    lang : string code language e.g. 'fr'
    name : string e.g. 'John Doe'
    redirect_internal : url e.g. 'https://forum.camptocamp.org/session/sso_login?sig=32...'
    roles : []
    token : string
    username : string e.g. 'johndoe'

Search JSON Response
====================

.. code-block::

    routes
        total : number of items
        documents : [{ROUTE_SHORT}]
