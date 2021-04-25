from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import ProjectForm, CreateUserForm, DeveloperForm
# from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	projects = Work_Status.objects.all()
	developer = Developer.objects.all()
	work_status = Work_Status.objects.all()

	total_developer = developer.count()

	total_projects = projects.count()
	delivered = projects.filter(status='Delivered').count()
	pending = projects.filter(status='Pending').count()

	context = {'orders':projects, 'developer':developer,
	'total_projects':total_projects,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['developer'])
def userPage(request):
	work_status = request.user.developer.work_status_set.all()

	total_projects = work_status.count()
	delivered = work_status.filter(status='Delivered').count()
	pending = work_status.filter(status='Pending').count()

	# print('ORDERS:', orders)

	context = {'work_status':work_status, 'total_projects':total_projects,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['developer'])
def accountSettings(request):
	developer = request.user.developer
	form = DeveloperForm(instance=developer)

	if request.method == 'POST':
		form = DeveloperForm(request.POST, request.FILES,instance=developer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def projects(request):
	projects = Project.objects.all()

	return render(request, 'accounts/projects.html', {'projects':projects})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def developer(request, pk_test):
	developer = Developer.objects.get(id=pk_test)

	work_status = developer.work_status_set.all()
	order_count = work_status.count()

	# myFilter = OrderFilter(request.GET, queryset=orders)
	# orders = myFilter.qs 

	context = {'developer':developer, 'work_status':work_status, 'order_count':order_count}
	return render(request, 'accounts/developer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	ProjectFormSet = inlineformset_factory(Developer, Work_Status, fields=('project', 'status','duration'), extra=10 )
	developer = Developer.objects.get(id=pk)
	formset = ProjectFormSet(queryset=Work_Status.objects.none(),instance=developer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = ProjectForm(request.POST)
		formset = ProjectFormSet(request.POST, instance=developer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	work_status = Work_Status.objects.get(id=pk)
	form = ProjectForm(instance=work_status)
	# print('ORDER:', work_status)
	if request.method == 'POST':

		form = ProjectForm(request.POST, instance=work_status)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	work_status = Work_Status.objects.get(id=pk)
	if request.method == "POST":
		work_status.delete()
		return redirect('/')

	context = {'item':work_status}
	return render(request, 'accounts/delete.html', context)