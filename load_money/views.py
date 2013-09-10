from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

@login_required
def load(request):
    profile = request.user.get_profile()
    rem_balance = profile.balance / 100
    if request.method == 'POST':
        amount = request.POST['amount']
        profile.balance = profile.balance + amount
        profile.save()
        
        return HttpResponseRedirect('/user_admin/')
    else:  
        return render_to_response('load_money/load_money.html',
                                  {"user_name" : profile.user,
                                   "current_balance": str("%.2f" % rem_balance)}, 
                                  RequestContext(request))