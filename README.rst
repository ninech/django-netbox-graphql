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

5. Visit http://127.0.0.1:8000/graphql to get graphQL editor.

PYPI Distribution
-----------------

Can be found at https://pypi.python.org/pypi?:action=display&name=django-netbox-graphql&version=0.0.1
