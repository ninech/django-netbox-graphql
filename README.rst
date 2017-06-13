=====
django-netbox-graphql
=====

Netbox-Graphql is a simple Django app which provides a GraphQL API for Netbox.


Quick start
-----------
1. Install module::
   pip install django-netbox-graphql

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

5. Visit http://127.0.0.1:8000/graphql to get graphQL editor .

PYPI Distribution
-----------------

Can be found at https://pypi.python.org/pypi?name=django-netbox-graphql&version=0.0.1&:action=display
