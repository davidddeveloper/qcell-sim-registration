import graphene
import graphql_jwt
from .models import Customer, SimType, IDType
from .file_upload import UploadMutation
from .schema import CustomerType, Login

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

class deleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        customer = Customer.objects.get(id=id)
        customer.delete()
        return deleteCustomer(ok=True)

class Mutation( graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    delete_customer = deleteCustomer.Field()
    login = Login.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    file = UploadMutation.Field()

