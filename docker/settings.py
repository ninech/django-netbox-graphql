# netbox_graphql configuration
# source file docker/setting.py

INSTALLED_APPS += (
    'graphene_django',
    'netbox_graphql',
)

GRAPHIQL_ENABLED = True  # optional, by default True, set False to disable it
GRAPHENE = {
    # points to the netbox_graphql schema variable in schema.py
    'SCHEMA': 'netbox_graphql.schema.schema',
    'SCHEMA_INDENT': 2,  # defines the indentation space in the output
}
