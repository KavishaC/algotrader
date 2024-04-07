from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import User

class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = "Visitor"
        email = ""

        # Ensure password matches confirmation
        password = ""

        # Check if the user is not authenticated
        if not request.user.is_authenticated:
            # Authenticate the default user
            user = authenticate(request, username=username, password=password)
            # If authentication is successful, log the user in
        
            if user is None:

                # Attempt to create new user
                try:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                except IntegrityError:
                    print("ERROR: Visitor Username already taken.")
        
            if user is not None:
                login(request, user)

        # Continue with the processing of the request
        response = self.get_response(request)
        return response