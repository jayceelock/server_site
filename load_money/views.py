"""
This script allows a customer to load more money onto his account
"""

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from decimal import Decimal

#Force a login
@login_required
def load(request):
    
    #Get the user's profile from the database
    profile = request.user.get_profile()
    
    rem_balance = profile.balance / 100
    
    #Extract the requested amount from the POST request
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        
        #Add the new amount to the old balance and save to the database
        profile.balance = profile.balance + (100 * amount)
        profile.save()
        
        return HttpResponseRedirect('/user_admin/')
    else:  
        return render_to_response('load_money/load_money.html',
                                  {"user_name" : profile.user,
                                   "current_balance": str("%.2f" % rem_balance)}, 
                                  RequestContext(request))