from django.utils import translation
import defaults
from signals import user_saved
from django.db.models import ObjectDoesNotExist

class PybbMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                # Here we try to load profile, but can get error
                # if user created during syncdb but profile model
                # under south control. (Like pybb.Profile).
                profile = request.user.get_profile()
            except ObjectDoesNotExist:
				user_saved(request.user, created=True)
				profile = request.user.get_profile()
				
            language = translation.get_language_from_request(request)
            request.session['django_language']
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
           




		   
