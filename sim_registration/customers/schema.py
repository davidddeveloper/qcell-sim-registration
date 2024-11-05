import graphene
from graphene_django import DjangoObjectType
from .models import Customer, SimType, IDType

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

class Query(graphene.ObjectType):
    """
        Represent the root class that
        specifies the set of operation for quering
    """
    customers = graphene.List(CustomerType)
    sim_types = graphene.List(SimTypeType)
    id_types = graphene.List(IDTypeType)

    def resolve_customers(self, info, *args, **kwargs):
        return Customer.objects.all()

    def resolve_sim_types(self, info, *args, **kwargs):
        return SimType.objects.all()

    def resolve_id_types(self, info, *args, **kwargs):
        return IDType.objects.all()

schema = graphene.Schema(query=Query)