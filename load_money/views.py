from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def load(request):
    profile = request.user.get_profile()
    rem_balance = profile.balance / 100
    
    return render_to_response('load_money/load_money.html',
                              {"user_name" : profile.user,
                               "current_balance": str("%.2f" % rem_balance)})