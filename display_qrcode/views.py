from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from display_qrcode.models import ProductData

from Crypto.PublicKey import ElGamal 
from Crypto.Hash import MD5

import qrcode

import base64
import random

import cPickle as Pickle

@login_required
def image(request):
    try:
        input_product_code = str(request.session['session_code'])    
    except:
        return HttpResponse("Please scan a valid QR code.")
    
    request.session.set_expiry(1)    
    
    server_priv_key = Pickle.load(open("/home/ubuntu/srv/server_site/server_key.priv", 'r'))
    
    vending_pub_key = Pickle.load(open("/home/ubuntu/srv/server_site/vending_key.pub", 'r'))
    
    try:
        input_data = input_product_code.split('[]', 2)
        encoded_string = input_data[0].split('**', 2)
        encoded_signature = input_data[1].split('**', 2)
        
        encrypted_string = (base64.urlsafe_b64decode(encoded_string[0]), base64.urlsafe_b64decode(encoded_string[1]))
        signature = (long(base64.urlsafe_b64decode(encoded_signature[0])), long(base64.urlsafe_b64decode(encoded_signature[1])))
        
        decrypted_data = server_priv_key.decrypt(encrypted_string)
        product_code = decrypted_data[-4:].upper()
           
        challenge = decrypted_data[4:8]
        
        hash_code = MD5.new(product_code).digest()
        verify_test = vending_pub_key.verify(hash_code, signature)
        
    except:
        return HttpResponse('This code has an invalid format. Please rescan the QR Code.')
    
    if verify_test != True:
        return HttpResponse('The origin of this QR Code could not be verified. Please contact your administrator')
    
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponse("Profile does not exist yet")

    try:                            #get details of current user
        product = ProductData.objects.get(product_code = product_code)
    except:
        return HttpResponse("Invalid product code")
    
    user_balance = profile.balance
    price = product.product_price

    if  user_balance > price:
        user_balance = user_balance - price
        profile.balance = user_balance
        profile.save()
        
        rand_hex_block_1 = '%004x' % random.randrange(16**4)
        rand_hex_block_2 = '%008x' % random.randrange(16**8)
        
        confirm_code_string = rand_hex_block_1 + challenge + rand_hex_block_2           #take challenge code as purchase authentication and insert it into char position 4
        
        encrypted_response_code = vending_pub_key.encrypt(confirm_code_string, 32)
        
        hash_code = MD5.new(challenge).digest()
        response_signature = server_priv_key.sign(hash_code, challenge)
        encoded_response_signature = base64.b64encode(str(response_signature[0])) + '**' + base64.b64encode(str(response_signature[1]))
        
        encoded_response_code = base64.b64encode(encrypted_response_code[0]) + '**' + base64.b64encode(encrypted_response_code[1])

        total_response = encoded_response_code + '[]' + encoded_response_signature
        
        qr = qrcode.QRCode(
                           version = None,
                           box_size = 7,
                           )
     
        qr.add_data(total_response)
        qr.make(fit = True)
     
        im = qr.make_image()
         
        response = HttpResponse(mimetype="image/png")
        im.save(response, "PNG")
        return response

    else:
        return HttpResponse("Not enough credits. Please load some more and scan the QR Code again.")
