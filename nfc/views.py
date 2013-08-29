from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from display_qrcode.models import ProductData

def getData(request):
    
    request.session.set_expiry(1)
    
    username = request.GET['user']
    encoded_password = request.GET['password']
    product = request.GET['product']
    
    password = affine_decrypt(encoded_password);
    
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
    

def affine_decrypt(encoded_password):
    
    alpha = ('a','b','c','d','e','f','g','h'
                ,'i','j','k','l','m','n','o','p','q'
                ,'r','s','t','u','v','w','x','y','z')
    
    a_char = encoded_password[0]
    b_char = encoded_password[1]
    a_num = alpha.index(a_char)
    b_num = alpha.index(b_char)
    
    encrypted_pass_text = encoded_password[2:]
    
    a_num %= 26;
    
    for x in range(25):
        if (((a_num * x) % 26) == 1):
            a = x
    
    y = []
    cypher_index = []
    decrypted_text = []
            
    for x in range(len(encrypted_pass_text)):
        y.append(alpha.index(encrypted_pass_text[x]))       
            
    for x in range(len(encrypted_pass_text)):
        cypher_index.append((a * (y[x] - b_num)) % 26)
    
    for x in range(len(encrypted_pass_text)):
        decrypted_text.append(alpha[cypher_index[x]])
            
    return decrypted_text           
    
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
