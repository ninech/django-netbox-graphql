# Install module

## Requirements

#### This module realise on modules:
    graphene-django>=1.0
    django-filter>=1.0.2
 
#### Install module:

    pip install django-netbox-graphql

#### Configure project

In file  `netbox/settings.py` add new apps inside `INSTALLED_APPS` 
    
    'graphene_django',
    'netbox-graphql',
    
At the bottom add graphene configuration

    GRAPHENE = {
        'SCHEMA' : 'netbox-graphql.schema.schema', #points to the netbox-graphql schema variable in schema.py
        'SCHEMA_INDENT': 2, #defines the indentation space in the output
    }
    
Add graphene url in `netbox/url.py`

    url(r'^graphql', include('netbox-graphql.urls')),