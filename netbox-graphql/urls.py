from django.conf.urls import include, url
from graphene_django.views import GraphQLView
from django.conf import settings

graphiql_enabled = getattr(settings, "GRAPHIQL_ENABLED", True)

urlpatterns = [
    #GrapQL
    url(r'^$', GraphQLView.as_view(graphiql=graphiql_enabled)),
]
