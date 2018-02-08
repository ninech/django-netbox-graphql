# netbox_graphql urls
# source docker/urls.py

_patterns += [
    url(r'^graphql', include('netbox_graphql.urls')),  # token required

    # url(r'^graphql/client', GraphQLView.as_view(graphiql=True)), # without token
]
