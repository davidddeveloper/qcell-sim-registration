from graphene_file_upload.scalars import Upload
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from werkzeug.utils import secure_filename
from .models import Customer
import graphene

#def serialize_file(file):
#    from django.core.files.storage import FileSystemStorage
#    from django.conf import settings
#    fs = FileSystemStorage(location=settings.STATIC_ROOT + '/uploads/')
#    return fs.url(file)

class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)
        customer_id = graphene.String(required=True)

    success = graphene.Boolean()
    uploaded_file_url = graphene.String()

    @login_required
    def mutate(self, info, file, customer_id, **kwargs):
        # do something with your file
        user = info.context.user
        customer = Customer.objects.get(id=customer_id)
        location = settings.MEDIA_ROOT + '/uploads/' + str(user.pk) + '/'
        fs = FileSystemStorage(location=location)
        filename = secure_filename(file.name)
        filename = fs.save(filename, file)
        uploaded_file_url = settings.MEDIA_URL + 'uploads/' + customer_id + '/' + filename
        customer.id_picture = uploaded_file_url
        customer.save()
        return UploadMutation(success=True, uploaded_file_url=uploaded_file_url)
