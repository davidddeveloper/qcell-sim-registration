import graphene
from graphene_django import DjangoObjectType
from .models import Customer
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
    customers = graphene.List(CustomerType, first=graphene.Int(), after=graphene.Int(), when=graphene.String())
    customers_today = graphene.List(CustomerType, first=graphene.Int(), after=graphene.Int())

    total_sims = graphene.Int()
    total_esims = graphene.Int()
    total_standard_sims = graphene.Int()

    me = graphene.Field(UserType)

    id_types = graphene.List(graphene.String)
    sim_types = graphene.List(graphene.String)

    def resolve_me(self, info, *args, **kwargs):
        return info.context.user

    @login_required
    def resolve_total_sims(self, info, *args, **kwargs):
        user = info.context.user
        return Customer.objects.filter(agent=user).count()
    
    @login_required
    def resolve_total_esims(self, info, *args, **kwargs):
        user = info.context.user
        return Customer.objects.filter(agent=user, sim_type='esim').count()
    
    @login_required
    def resolve_total_standard_sims(self, info, *args, **kwargs):
        user = info.context.user
        return Customer.objects.filter(agent=user, sim_type='standard').count()

    @login_required
    def resolve_customer(self, info, *args, **kwargs):
        id = kwargs.get('id')
        return Customer.objects.get(id=id)

    @login_required
    def resolve_customers(self, info, first, after, when, *args, **kwargs):
        user = info.context.user
        query = Customer.objects.filter(agent=user)
        if when:
            # set query if when is today
            if when in ['1dayago', '1daysago', 'today', 'Today']:
                query = Customer.objects.filter(agent=user, date_created__date=datetime.date.today())

            # set query if when is yesterday
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
        return [choice[0] for choice in Customer._meta.get_field('sim_type').choices]

    @login_required
    def resolve_id_types(self, info, *args, **kwargs):
        return [choice[0] for choice in Customer._meta.get_field('id_type').choices]

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
