from drf_firebase.authentication import BaseFirebaseAuthentication
from firebase_admin import credentials, initialize_app
from django.contrib.auth import get_user_model

creds = credentials.Certificate('firebase.json')
app = initialize_app(creds, name='RideGroup')


class FirebaseAuthentication(BaseFirebaseAuthentication):
    keyword = 'RideGroupFirebaseToken'

    def get_firebase_app(self):
        return app

    def get_django_user(self, firebase_user_record):
        try:
            return get_user_model().objects.get(firebase_uid=firebase_user_record.uid)
        except get_user_model().DoesNotExist:
            return get_user_model().objects.create(firebase_uid=firebase_user_record.uid,
                                                   username=firebase_user_record.display_name,
                                                   email=firebase_user_record.email,
                                                   phone=firebase_user_record.phone_number,
                                                   email_verified=firebase_user_record.email_verified,
                                                   photo_url=firebase_user_record.photo_url
                                                   )
            # return get_user_model().objects.create(firebase_uid=firebase_user_record.uid)
