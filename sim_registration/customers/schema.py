import graphene
from graphene_django import DjangoObjectType
from .models import Customer, SimType, IDType
#from .mutation import Mutation
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import authenticate, get_user_model
import datetime
import regex as re


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
    customers = graphene.List(CustomerType, first=graphene.Int(), after=graphene.Int(), when=graphene.String())
    customers_today = graphene.List(CustomerType, first=graphene.Int(), after=graphene.Int())
    sim_types = graphene.List(SimTypeType)
    id_types = graphene.List(IDTypeType)

    total_sims = graphene.Int()
    total_esims = graphene.Int()
    total_standard_sims = graphene.Int()

    @login_required
    def resolve_total_sims(self, info, *args, **kwargs):
        user = info.context.user
        return Customer.objects.filter(agent=user).count()
    
    @login_required
    def resolve_total_esims(self, info, *args, **kwargs):
        user = info.context.user
        sim_type = SimType.objects.get(name="Embedded Sim (eSim)")
        return Customer.objects.filter(agent=user, sim_type_id=sim_type.id).count()
    
    @login_required
    def resolve_total_standard_sims(self, info, *args, **kwargs):
        user = info.context.user
        sim_type = SimType.objects.get(name="Standard Sim")
        return Customer.objects.filter(agent=user, sim_type_id=sim_type.id).count()

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
    def resolve_customers(self, info, first, after, when, *args, **kwargs):
        user = info.context.user
        query = Customer.objects.filter(agent=user)
        if when:
            # set query if when is today
            if when in ['1dayago', '1daysago', 'today', 'Today']:
                query = Customer.objects.filter(agent=user, date_created__date=datetime.date.today())
            
            elif when in ['yesterday', 'Yesterday']:
                query = Customer.objects.filter(agent=user, date_created__date=datetime.date.today() - datetime.timedelta(days=1))

            else:
                when_splitted = when.split("daysago") if "daysago" in when else when.split("DaysAgo")
                serialize_when = int(when_splitted[0])
            
                query = Customer.objects.filter(
                    agent=user, date_created__date=datetime.date.today() - datetime.timedelta(days=(serialize_when - 1))
                )
            # if when == 1:
                # query = Customer.objects.filter(date_created__date=datetime.date.today())
            # elif when == 2:
                # query = Customer.objects.filter(date_created__date=datetime.date.today() + datetime.timedelta(days=1))
            # elif when == 3:
                # query = Customer.objects.filter(date_created__date=datetime.date.today() - datetime.timedelta(days=3))

        if first and after:
            query = query[after:after + first]

        else:
            if first:
                query = query[:first]

            if after:
                query = query[after:]

        return query
    
    @login_required
    def resolve_customers_today(self, info, first, after, *args, **kwargs):
        user = info.context.user
        query = Customer.objects.filter(agent=user,date_created__date=datetime.date.today())

        if first and after:
            query = query[after:after + first]

        else:
            if first:
                query = query[:first]

            if after:
                query = query[after:]

        return query

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
