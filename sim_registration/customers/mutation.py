import graphene
import graphql_jwt
from .models import Customer
from .file_upload import UploadMutation
from .schema import CustomerType, Login
from django.conf import settings
import regex as re


class CreateCustomer(graphene.Mutation):
    class Arguments:
        sim_type = graphene.String(required=True)
        first_name = graphene.String(required=True)
        middle_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        gender = graphene.String(required=True)
        mssisdn = graphene.String(required=True)
        profession = graphene.String(required=True)
        id_number = graphene.String(required=True)
        id_type = graphene.String(required=True)
        id_picture = graphene.String(required=True)
        address = graphene.String(required=True)
        nationality = graphene.String(required=True)
        date_created = graphene.DateTime()

    ok = graphene.Boolean()
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, sim_type, first_name, last_name, middle_name, gender, mssisdn, profession, id_number, id_type, id_picture, address, nationality):
        """
            performs the mutation using django ORM
        """
        agent = info.context.user

        voters_id_format = [
            'VI', 'vi', 'voters_id',
            'Voters_id', 'Voters_ID',
            'voters ID', 'Voters ID',
            'voters id', 'VOTERS ID'
            'votersid', 'VOTERSID'
        ]

        national_id_format = [
            'NIN', 'nin', 'national_id',
            'Voters_id', 'National_ID',
            'national ID', 'National ID',
            'national id', 'NATIONAL ID'
            'nationalid', 'NATIONALID'
        ]

        license_id_format = [
            'LICENSE', 'license',
            'lic', 'LIC'
        ]

        passport_id_format = [
            'PASSPORT', 'passport', 'pp', 'PP',
        ]
        
        
        accepted_id_format = national_id_format + voters_id_format + \
            license_id_format + passport_id_format # accepted format for the IDs

        esim_type_format = [
            'esim',
            'Esim',
            'ESIM',
        ]

        standard_sim_type_format = [
            'standard_sim', 'standard sim',
            'Standard Sim', 'STANDARDSIM',
            'standardsim', 'standard_sim',
            'standard', 'Standard', 'STANDARD'
        ]

        accepted_sim_type_format = esim_type_format + standard_sim_type_format

        number = Customer.objects.filter(mssisdn=mssisdn)

        if number:
            return CreateCustomer(ok=False, message="Sim is already registered")

        # ensure that the number is 8 characters and starts with 31, 32 or 34
        # pre check
        for prefix in settings.ALLOWED_PHONE_PREFIXES:
            print(prefix)
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
        
        if gender not in ['m', 'M', 'male', 'Female', 'f', 'F', 'female', 'Female']:
            return CreateCustomer(ok=False, message="Invalid gender")
        
        if id_type not in accepted_id_format:  # checks for correct format
            return CreateCustomer(ok=False, message="Invalid IDType")
        
        if sim_type not in accepted_sim_type_format:
            return CreateCustomer(ok=False, message="Invalid SimType")

        customer = Customer.objects.create(
            sim_type=sim_type,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            gender=gender,
            mssisdn=mssisdn,
            profession=profession,
            id_number=id_number,
            id_type=id_type,
            id_picture=id_picture,
            address=address,
            nationality=nationality,
            agent=agent
        )

        if id_type in voters_id_format:
            print("yep!")
            customer.id_type = 'vi'

        if id_type in license_id_format:
            customer.id_type = 'lic'

        if id_type in national_id_format:
            customer.id_type = 'nin'
        
        if id_type in passport_id_format:
            customer.id_type = 'pp'

        # sim type - correct saving
        if sim_type in esim_type_format:
            customer.sim_type = 'esim'

        if sim_type in standard_sim_type_format:
            customer.sim_type = 'standard'

        # save
        customer.save()
        return CreateCustomer(ok=True, customer=customer, message=f"Sim successfully registered for {first_name}.")

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
        sim_type = graphene.String(required=True)
        number = graphene.String(required=True)

    ok = graphene.Boolean()
    customers = graphene.List(CustomerType)
    sim_type = graphene.String()

    def mutate(self, info, sim_type, number):
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

