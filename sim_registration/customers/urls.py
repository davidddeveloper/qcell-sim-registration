from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from .mutation import Mutation
from .schema import Query
import graphene

from .views import *

schema = graphene.Schema(query=Query, mutation=Mutation)

urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("graphql/file_upload", csrf_exempt(FileUploadGraphQLView.as_view(schema=schema))),
]