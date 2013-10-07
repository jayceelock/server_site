from Crypto.PublicKey import RSA
from display_qrcode.models import ProductData
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import base64
import random
import os

def getData(request):
    request.session.set_expiry(1)
    
    encrypted_username = request.GET['user']
    encrypted_password = request.GET['password']
    encrypted_product = request.GET['product']
    
    password = decrypt(encrypted_password)
    username = decrypt(encrypted_username)
    product = decrypt(encrypted_product)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            try:
                product = ProductData.objects.get(product_code = product)
            except:
                HttpResponse("Invalid product code")
            approved = check_balance(request, product)
            if approved == 1:
                random_confirm_string = str(('%004x' % random.randrange(16**4) + product.product_code + '%008x' % random.randrange(16**8)).upper())
                encrypted_confirm_string = encrypt(random_confirm_string)
                
                return HttpResponse(encrypted_confirm_string)
            else:
                return HttpResponse("Nah bru, no cash.")
        else:
            return HttpResponse("Your account has been disabled.")
        
    else:
        return HttpResponse("Account name and password are incorrect.")
             
    
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
    
    path = os.getcwd()
    
    f = open(path + "/private_key.pem", 'r')
    priv_key = RSA.importKey(f)
    
    encrypted_text = base64.urlsafe_b64decode(encoded_text.encode())
    
    plain_text = priv_key.decrypt(encrypted_text)

    return plain_text

def encrypt(original_text):
    
    path = os.getcwd()
    
    f = open(path + "/private_key.pem", 'r')
    priv_key = RSA.importKey(f)
    #pub_key = priv_key.publickey()
    
    encrypted_text = priv_key.encrypt(original_text, 32)
    encoded_text = base64.b64encode(encrypted_text[0])
    
    return encoded_text
