from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def admin_page(request):
    profile = request.user.get_profile()
    
    rem_balance = profile.balance / 100
    
    return render_to_response('user_admin/balance.html',
                              {"user_name" : profile.user,
                               "current_balance": str("%.2f" % rem_balance)})