### Install module

#### Build package (optional)
    git clone https://github.com/ninech/django-netbox-graphql
    cd django-netbox-graphql
    python setup.py sdist

#### This module relies on modules:
    graphene-django>=1.0
    django-filter>=1.0.2
 
#### Install module:

    pip install django-netbox-graphql #from external storage, not yet deployed
    or     
    pip install dist/django-netbox-graphql-0.0.x.tar.gz

#### Configure project

In file  `netbox/settings.py` add new apps inside `INSTALLED_APPS` 
    
    'graphene_django',
    'netbox-graphql',
    
At the bottom add graphene configuration

    GRAPHIQL_ENABLED = True # optional, by default True, set False to disable it 
    GRAPHENE = {
        'SCHEMA' : 'netbox-graphql.schema.schema', #points to the netbox-graphql schema variable in schema.py
        'SCHEMA_INDENT': 2, #defines the indentation space in the output
    }
    
Add graphene url in `netbox/url.py`

    url(r'^graphql', include('netbox-graphql.urls')),