from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def rescan_page(request):
	logout(request)
	return render_to_response('main/logout.html')

def main_page(request):
	try:
		request.session['session_code'] = request.GET['code']
		return render_to_response('main/index.html')
	except:
		return render_to_response('main/no_code.html')