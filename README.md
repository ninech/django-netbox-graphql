# Install module

## Requirements

#### This module realise on modules:
    pip graphene_django==1.4
    pip install django-filter==1.0.2 # already goes with netbox installation, no need to install
 
#### Install module:

    pip install django-netbox-graphql

#### Configure project

In file  `netbox/settings.py` add new apps inside `INSTALLED_APPS` 

    # graphQL
    'graphene_django',
    'ninech',
    
At the bottom add graphene configuration

    GRAPHENE = {
        'SCHEMA' : 'netbox-graphql.schema.schema', #points to the schema variable in schema.py
        'SCHEMA_INDENT': 2, #defines the indentation space in the output
    }
    
Add graphene url in `netbox/url.py`

    from graphene_django.views import GraphQLView

Add in pattern row below:

    #GrapQL
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),