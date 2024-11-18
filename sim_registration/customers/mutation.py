import graphene
import graphql_jwt
from .models import Customer, SimType, IDType
from .file_upload import UploadMutation
from .schema import CustomerType, Login
from django.conf import settings
from django.contrib.auth.models import User
import regex as re


class CreateCustomer(graphene.Mutation):
    class Arguments:
        sim_type_id = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        mssisdn = graphene.String(required=True)
        profession = graphene.String(required=True)
        id_number = graphene.String(required=True)
        id_type_id = graphene.String(required=True)
        id_picture = graphene.String(required=True)
        address = graphene.String(required=True)
        nationality = graphene.String(required=True)
        date_created = graphene.DateTime()

    ok = graphene.Boolean()
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, sim_type_id, first_name, last_name, mssisdn, profession, id_number, id_type_id, id_picture, address, nationality):
        """
            performs the mutation using django ORM
        """
        sim_type = SimType.objects.get(id=sim_type_id)
        id_type = IDType.objects.get(id=id_type_id)
        agent_id = info.context.user.id

        if not agent_id:
            return CreateCustomer(ok=False, message="You must be logged in to create a customer. Login by sending a valid JWT Token to the server.")

        # ensure that the number is 8 characters and starts with 31, 32 or 34
        # pre check
        for prefix in settings.ALLOWED_PHONE_PREFIXES:
            if mssisdn.startswith(prefix):
                if len(mssisdn) == 8 or len(mssisdn) == 7 or len(mssisdn) == 9:
                    is_match = True
                    break
            else:
                is_match = False

        # final check ensure that the number is actually number
        is_match = re.match(settings.PHONE_NUMBER_MATCHING_REGEX, mssisdn)
        if not is_match:
            return CreateCustomer(ok=False, message="Invalid phone number")

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
            nationality=nationality,
            agent = User.objects.get(id=agent_id)
        )

        # save
        customer.save()
        return CreateCustomer(ok=True, customer=customer)

class deleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        customer = Customer.objects.get(id=id)
        customer.delete()
        return deleteCustomer(ok=True)

class SearchCustomer(graphene.Mutation):
    class Arguments:
        sim_type_id = graphene.String(required=True)
        number = graphene.String(required=True)

    ok = graphene.Boolean()
    customers = graphene.List(CustomerType)
    sim_type = graphene.String()

    def mutate(self, info, sim_type_id, number):
        sim_type = SimType.objects.get(id=sim_type_id)
        customers = Customer.objects.filter(mssisdn__contains=number, sim_type=sim_type)

        
        ok = True if customers else False
        # return Customer.objects.filter(mssisdn__contains=number)
        return SearchCustomer(ok=ok, customers=customers, sim_type=sim_type.name)


class Mutation( graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    delete_customer = deleteCustomer.Field()
    login = Login.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    file = UploadMutation.Field()
    search_number = SearchCustomer.Field()

