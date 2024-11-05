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

class CreateCustomer(graphene.Mutation):
    class Arguments:
        sim_type_id = graphene.Int(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        mssisdn = graphene.String(required=True)
        profession = graphene.String(required=True)
        id_number = graphene.String(required=True)
        id_type_id = graphene.Int(required=True)
        id_picture = graphene.String(required=True)
        address = graphene.String(required=True)
        nationality = graphene.String(required=True)
        date_created = graphene.DateTime()


    ok = graphene.Boolean()
    customer = graphene.Field(CustomerType)

    def mutate(self, info, sim_type_id, first_name, last_name, mssisdn, profession, id_number, id_type_id, id_picture, address, nationality):
        """
            performs the mutation using django ORM
        """
        sim_type = SimType.objects.get(id=sim_type_id)
        id_type = IDType.objects.get(id=id_type_id)

        print("This is the sim type", sim_type, id_type)
        customer = Customer.objects.create(
            sim_type=sim_type,
            first_name=first_name,
            last_name=last_name,
            mssisdn=mssisdn,
            profession=profession,
            id_number=id_number,
            id_type=id_type,
            id_picture=id_picture,
            address=address,
            nationality=nationality
        )

        # save
        customer.save()
        return CreateCustomer(customer=customer)

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

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
