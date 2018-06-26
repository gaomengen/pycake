# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def logout_view(request):
	"""Log the user out."""
	logout(request)
	return HttpResponseRedirect(reverse('pycake_main:index'))

def register(request):
	"""Register a new user."""
	if request.method != 'POST':
		#Display blank registration form.
		form = UserCreationForm()
	else:
		#Process completed form.
		form = UserCreationForm(data=request.POST)
	
		if form.is_valid():
			new_user = form.save()
			#Log the user in and then redirect to home page.
			#BUG!!! If the password disqulified(weak passwd), is_valid() still true.
			authenticated_user = authenticate(username=new_user.username, 
				password=request.POST['password1'])
		login(request, authenticated_user)
		return HttpResponseRedirect(reverse('pycake_main:index'))

	context = {'form': form}
	return render(request, 'users/register.html', context)