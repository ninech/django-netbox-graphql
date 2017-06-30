=====
django-netbox-graphql
=====

Netbox-Graphql is a simple Django app which provides a GraphQL API for Netbox.

Build package (optional)
------------------------

|    git clone https://github.com/ninech/django-netbox-graphql
|    cd django-netbox-graphql
|    python setup.py sdist

This module relies on modules
-----------------------------
|    graphene-django>=1.0
|    django-filter>=1.0.2

Quick start
-----------

1. Install module::

    pip install django-netbox-graphql #from external storage, not yet deployed
    or
    pip install dist/django-netbox-graphql-0.0.x.tar.gz

2. Add below modules to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
    ...
    'graphene_django',
    'netbox-graphql',
    ]

3. Add graphene settings to netbox/setting.py::

    GRAPHIQL_ENABLED = True # optional, by default True, set False to disable it
    GRAPHENE = {
        'SCHEMA' : 'netbox-graphql.schema.schema', #points to the netbox-graphql schema variable in schema.py
        'SCHEMA_INDENT': 2, #defines the indentation space in the output
    }

4. Include the polls URLconf in your project netbox/urls.py like this::

    url(r'^graphql', include('netbox-graphql.urls')),

5. Visit http://127.0.0.1:8000/graphql to fetch records with graphql::

    curl -H "Authorization: Token <netbox_token>" http://localhost:8000/graphql?query=query%7B%20types%20%7B%20edges%20%7B%20node%20%7B%20name%20%7D%20%7D%20%7D%20%7D

Visit http://localhost:8000/user/api-tokens/ to generate token

Graphql editor for writing queries
----------------------------------

1. You should have installed `graphene_django`::

    INSTALLED_APPS = [
    ...
    'graphene_django',
    ]

2. Create url for graphql client with adding new link in `urls.py` ::

    url(r'^graphql/client', GraphQLView.as_view(graphiql=True)),

3. Visit http://127.0.0.1:8000/graphql/client ::

.. image:: https://s11.postimg.org/5vi9lmn1f/django-netbox-graphql.png


PYPI Distribution
-----------------

Can be found at https://pypi.python.org/pypi?:action=display&name=django-netbox-graphql&version=0.0.2

About
-----
This module is currently maintained and funded by `nine.ch <https://nine.ch>`_

.. image:: https://blog.nine.ch/assets/logo.png
 :target: https://nine.ch