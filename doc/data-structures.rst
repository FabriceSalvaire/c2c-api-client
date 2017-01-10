Error Response
==============

.. code-block::

    status : 'error'
    errors : [{
        description : 'Login failed'
        location : 'body'
        name : 'user'
    }]

Login Response
==============

JSON Response to a successfully login:

* *expire* : unix timestamp
* forum_username : string e.g. 'John_Doe'
* *id* : int
* *lang* : string e.g. 'fr'
* *name* : string e.g. 'John Doe'
* *redirect_internal* : url e.g. 'https://forum.camptocamp.org/session/sso_login?sig=32...'
* *roles* : []
* *token* : string
* *username* : string e.g. 'johndoe'

.. code-block::

    expire : unix timestamp
    forum_username : string e.g. 'John_Doe'
    id : int
    lang : string e.g. 'fr'
    name : string e.g. 'John Doe'
    redirect_internal : url e.g. 'https://forum.camptocamp.org/session/sso_login?sig=32...'
    roles : []
    token : string
    username : string e.g. 'johndoe'

Search Response
===============

.. code-block::

    routes
        total : number of items
        documents : [{DOCUMENT}]

Document
--------

.. code-block::

    activities : list of string e.g. ['rock_climbing']
    aid_rating :
    areas : [{AREA}]
    available_langs : list of languages e.g. ['it', 'es', 'fr']
    document_id : int
    elevation_max : int
    engagement_rating : string e.g. 'I'
    equipment_rating : string e.g. 'P1'
    exposition_rock_rating :
    geometry : {GEOMETRY}
    global_rating : string e.g. 'AD+'
    height_diff_difficulties : int
    height_diff_up : int
    locales : [{ROUTE_LOCALE}]
    orientations : list of string e.g. ['SW']
    protected : bool
    quality : string
    risk_rating
    rock_free_rating : string e.g. '5a'
    rock_required_rating : string e.g. '4c'
    type : 'r'
    version : int

Area
----

.. code-block::

    area_type : 'country'
    available_langs : None
    document_id : int
    locales : [{
        lang : 'fr'
        title : string
        version : int
        }]
    protected : bool
    type : 'a'
    version : int

Geometry
--------

.. code-block::

    geom :
        coordinates : [x, y] Mercator espg:3857
        type : 'Point'
    version : int

Route_Locale
------------

.. code-block::

    lang : string e.g. 'fr'
    summary : string
    title_prefix : string
    title : string
    version : int

Route
=====

