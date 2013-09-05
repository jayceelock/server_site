from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from display_qrcode.models import ProductData

from Crypto.PublicKey import RSA
import base64
import cPickle as pickle

def getData(request):
    
    request.session.set_expiry(1)
    
    username = request.GET['user']
    encrypted_password = request.GET['password']
    product = request.GET['product']
    
    password = decrypt(encrypted_password);
    #password = request.GET['password']
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            approved = check_balance(request, product)
            if approved == 1:
                return HttpResponse("You have enough money!")
            else:
                return HttpResponse("Nah bru, no cash.")
        else:
            return HttpResponse("Your account has been disabled.")
        
    else:
        return HttpResponse("Account name and password are incorrect.")
    
    #return HttpResponse(request.session['username'] + " " + request.session['password'])           
    
def check_balance(request, product):
    
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponse("Profile does not exist yet")
    
    try:                            #get details of current user
        product = ProductData.objects.get(product_code = product)
    except:
        return HttpResponse("Invalid product code")
    
    user_balance = profile.balance
    price = product.product_price
    
    if  user_balance > price:
        user_balance = user_balance - price
        profile.balance = user_balance
        profile.save()
        
        return 1
    
    else:
        return 0
    
    
def decrypt(encoded_text):
#     f = open("app_private_key.pem", 'r')
#     priv_key = RSA.importKey(f.read())
#     f.close()
    f = open("app_key.priv", 'r')
    priv_key = pickle.load(f)
    
    #pub_key = priv_key.publickey()
    
    encrypted_text = base64.b64decode(encoded_text)
    
    plain_text = priv_key.decode(encrypted_text)
    
    return plain_text
