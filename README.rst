=====
django-netbox-graphql
=====

Netbox-Graphql is a simple Django app which provides a GraphQL API for Netbox.
This module is dockerized and **development of it is still in progress**. Netbox's circuit module with all it's models are covered.
For this part of app you can CRUD operations.

Available Models for CRUD
------------------------
* CIRCUITS
    * Provider
    * Circuit
    * CircuitType
    * CircuitTermination
* DCIM
    * Region
    * Site
* TENANCY
    * TenantGroup
    * Tenant
* IPAM
    * Role
    * VlanGroup
    * VLAN

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

    curl  -H 'Content-Type: application/json'\
     -H "Authorization: Token <netbox_token>"\
      -XPOST -d '{"query":"{ circuitTypes { edges { node { id name slug } } } }"}' http://localhost:8000/graphql

Visit http://localhost:8000/user/api-tokens/ to generate token

Graphql CRUD examples
---------------------

Create::

    curl -H 'Content-Type: application/json'\
     -H "Authorization: Token <netbox_token>"\
      -XPOST -d '{"query":"mutation { newCircuitType(input: {name: \"Type1\", slug: \"type1\"}) { circuitType { id name slug } } }"}' http://localhost:8000/graphql

    {"data":{"newCircuitType":{"circuitType":{"id":"Q2lyY3VpdFR5cGVOb2RlOjI1","name":"Type1","slug":"type1"}}}}
Read::

    curl -H 'Content-Type: application/json'\
     -H "Authorization: Token <netbox_token>"\
      -XPOST -d '{"query":"{ circuitTypes(id: \"<circuit-type-id>\") { edges { node { id name slug } } } }"}' http://localhost:8000/graphql

    {"data":{"circuitTypes":{"edges":[{"node":{"id":"Q2lyY3VpdFR5cGVOb2RlOjI0","name":"Type","slug":"type"}}]}}}
Update::

    curl -H 'Content-Type: application/json'\
     -H "Authorization: Token <netbox_token>"\
      -XPOST -d '{"query":"mutation { updateCircuitType(input: {id:\"<circuit-type-id>\", name: \"TypeX\", slug: \"typeX\"}) { circuitType { slug name slug } } }"}' http://localhost:8000/graphql

    {"data":{"updateCircuitType":{"circuitType":{"id":"Q2lyY3VpdFR5cGVOb2RlOjI0","name":"TypeX","slug":"typeX"}}}}

Delete::

    curl -H 'Content-Type: application/json'\
     -H "Authorization: Token <netbox_token>"\
      -XPOST -d '{"query":"mutation { deleteCircuitType(input: {id:\"<circuit-type-id>\"}) { circuitType { name slug } } }"}' http://localhost:8000/graphql

    {"data":{"deleteCircuitType":{"circuitType":{"name":"TypeX","slug":"typeX"}}}}

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

Examples for module Circuit
---------------------------

All examples are available `here <EXAMPLES.md>`_

Packaging and deploying to pypi.python.org
-----------------------------------------------
The simplest way to make package and deploy it is with using `twine`::

    pip install twine # install twine
    python setup.py sdist # build django-netbox-graphql-X.X.X.tar.gz
    twine upload dist/django-netbox-graphql-X.X.X.tar.gz


Tests
-----
Run unit tests::

    docker-compose up -d postgres
    
    # wait until the database started.

    docker-compose run --rm --entrypoint './manage.py' netbox test # runs all tests
    docker-compose run --rm --entrypoint './manage.py' netbox test netbox-graphql/ # runs only netbox-graphql module tests

    # At the end, you can stop any running service and cleanup as follows:
    docker-compose down

PYPI Distribution
-----------------

Can be found at https://pypi.python.org/pypi?:action=display&name=django-netbox-graphql

About
-----
This module is currently maintained and funded by `nine <https://www.nine.ch>`_

.. image:: https://logo.apps.at-nine.ch/Dmqied_eSaoBMQwk3vVgn4UIgDo=/trim/500x0/logo_claim.png
 :target: https://nine.ch
