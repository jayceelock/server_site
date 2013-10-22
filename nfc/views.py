"""
This script allows a user to buy a product using the NFC payment option.
"""

from Crypto.PublicKey import RSA
from display_qrcode.models import ProductData
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import base64
import random
import os

def getData(request):
    
    #Automatically log the user out after one second
    request.session.set_expiry(1)
    
    #Extract the data from the URL request from the app
    encrypted_username = request.GET['user']
    encrypted_password = request.GET['password']
    encrypted_product = request.GET['product']
    
    #Decrypt the data
    password = decrypt(encrypted_password)
    username = decrypt(encrypted_username)
    product = decrypt(encrypted_product)
    
    #Perform the logon operation
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            try:
                product = ProductData.objects.get(product_code = product)
            except:
                HttpResponse("Invalid product code")
            
            #Perfomr user balance check    
            approved = check_balance(request, product)
            
            #If the user has enough credits, the server returns an encrypted approval message
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
             

#Function to check the users balance    
def check_balance(request, product):
    
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponse("Profile does not exist yet")
    
    try:                           
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
    

#Function to decrypt the data    
def decrypt(encoded_text):
    
    path = os.getcwd()
    
    f = open(path + "/private_key.pem", 'r')
    priv_key = RSA.importKey(f)
    
    encrypted_text = base64.urlsafe_b64decode(encoded_text.encode())
    
    plain_text = priv_key.decrypt(encrypted_text)

    return plain_text

#Fucntion the encrypt the return data
def encrypt(original_text):
    
    path = os.getcwd()
    
    f = open(path + "/private_key.pem", 'r')
    priv_key = RSA.importKey(f)
    
    encrypted_text = priv_key.encrypt(original_text, 32)
    encoded_text = base64.b64encode(encrypted_text[0])
    
    return encoded_text
