from django.conf.urls import include, url
from graphene_django.views import GraphQLView

urlpatterns = [
    #GrapQL
    url(r'^$', GraphQLView.as_view(graphiql=True)),
]
