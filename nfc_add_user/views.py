from django.contrib.auth.models import User
from django.http.response import HttpResponse

def add_user(request):
    
    user = User.objects.create_user(
              username = request.GET['username'],
              email = request.GET['email'],
              password = request.GET['password'])
    
    try:
        user.save()
        
    except:
        return HttpResponse("That username is already in use. Please try a different name.")    
    
    return HttpResponse("User saved")