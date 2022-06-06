from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend



class phoneOrEmail(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        
        users = user_model._default_manager.filter(
            Q(**{user_model.USERNAME_FIELD: username}) | Q(phone_number__iexact=username)
        )

        # Test whether any matched user has the provided password:
        for user in users:
            if user.check_password(password):
                return user

        if not users:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (see
            # https://code.djangoproject.com/ticket/20760)
            user_model().set_password(password)

        # try:
        #    # Try to fetch the user by searching the username or email field
        #     user = MyUser.objects.get(Q(email=username)|Q(phone_number=username))
        #     if user.check_password(password):
        #         return user
        # except MyUser.DoesNotExist:
        #     # Run the default password hasher once to reduce the timing
        #     # difference between an existing and a non-existing user (#20760).
        #     MyUser().set_password(password)