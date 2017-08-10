# netbox-graphql configuration
# source file docker/setting.py

INSTALLED_APPS += (
    'graphene_django',
    'netbox-graphql',
)

GRAPHIQL_ENABLED = True # optional, by default True, set False to disable it
GRAPHENE = {
    'SCHEMA' : 'netbox-graphql.schema.schema', #points to the netbox-graphql schema variable in schema.py
    'SCHEMA_INDENT': 2, #defines the indentation space in the output
}
