"""
This script allows a user to add a new user to the user database using the NFC app.
"""

from django.contrib.auth.models import User
from django.http.response import HttpResponse

def add_user(request):
    
    #Retrieve the user's info from the URL request sent by the app
    user = User.objects.create_user(
              username = request.GET['username'],
              email = request.GET['email'],
              password = request.GET['password'])
    
    #Save the new user, if he does nnot exist
    try:
        user.save()
        
    except:
        return HttpResponse("That username is already in use. Please try a different name.")    
    
    return HttpResponse("User saved")