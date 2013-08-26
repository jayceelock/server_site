from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login

def user_reg(request):
	
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			new_user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, new_user)
			return HttpResponseRedirect('/user_admin/')		
	else:
		form = UserForm()
	return render(request, 'register/register.html', {'form': form})
