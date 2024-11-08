import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from .models import Customer, SimType, IDType
from .mutation import Mutation
from graphql_jwt.decorators import login_required, token_auth
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import authenticate, get_user_model, login, logout

class CustomerType(DjangoObjectType):
    """
        Represent a GraphQL Customer Type for querying it
    """
    class Meta:
        model = Customer
        fields = "__all__"

class SimTypeType(DjangoObjectType):
    """
        Represent a GraphQL Sim Type for querying it
    """
    class Meta:
        model = SimType
        fields = "__all__"

class IDTypeType(DjangoObjectType):
    """
        Represent a GraphQL IDType Type for querying it
    """
    class Meta:
        model = IDType
        fields = "__all__"

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class Query(graphene.ObjectType):
    """
        Represent the root class that
        specifies the set of operation for quering
    """
    customer = graphene.Field(CustomerType, id=graphene.String())
    id_type = graphene.Field(IDTypeType, id=graphene.String())
    sim_type = graphene.Field(SimTypeType, id=graphene.String())
    customers = graphene.List(CustomerType)
    sim_types = graphene.List(SimTypeType)
    id_types = graphene.List(IDTypeType)

    @login_required
    def resolve_customer(self, info, *args, **kwargs):
        id = kwargs.get('id')
        return Customer.objects.get(id=id)

    @login_required
    def resolve_id_type(self, info, *args, **kwargs):
        id = kwargs.get('id')
        return IDType.objects.get(id=id)

    @login_required
    def resolve_sim_type(self, info, *args, **kwargs):
        id = kwargs.get('id')    
        return SimType.objects.get(id=id)

    @login_required
    def resolve_customers(self, info, *args, **kwargs):
        return Customer.objects.all()

    @login_required
    def resolve_sim_types(self, info, *args, **kwargs):
        return SimType.objects.all()

    @login_required
    def resolve_id_types(self, info, *args, **kwargs):
        return IDType.objects.all()

class Login(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise Exception('Invalid username or password')

        token = get_token(user)
        return Login(token=token, user=user)

schema = graphene.Schema(query=Query, mutation=Mutation)
