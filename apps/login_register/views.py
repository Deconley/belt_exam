from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Item
# Create your views here.
def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def currentUser(request):
	id = request.session['user_id']

	return User.objects.get(id=id)

def index(request):

    return render(request, "login_register/index.html")

def success(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        items = Item.objects.all().order_by('-created_at')

        context = {
        'user': user,
        'items': items
        }
        print request.session['user_id']
        return render(request,'login_register/success.html', context)

    return redirect('/')

def register(request):
    if request.method == "POST":
        errors = User.objects.validateRegistration(request.POST)

        if not errors:
            user = User.objects.createUser(request.POST)

            request.session['user_id'] = user.id

            return redirect('/success')
        for error in errors:
            messages.error(request, error)

        flashErrors(request, errors)

    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.validateLogin(request.POST)

        if not errors:
            user = User.objects.filter(email = request.POST['email']).first()
            if user:
                password = str(request.POST['password'])
                user_password = str(user.password)

                hashed_pw = bcrypt.hashpw(password, user_password)

                if hashed_pw == user.password:
                    request.session['user_id'] = user.id

                    return redirect('/success')

            errors.append("Invaid account information")
        flashErrors(request, errors)
    return redirect('/')

def logout(request):
    if 'user_id'in request.session:
        request.session.pop('user_id')
    return redirect('/')

def createItem(request):
    	if 'user_id' in request.session:
		current_user = currentUser(request)
		items = Item.objects.all()

		context = {
			'current_user': current_user,
			'items': items
		}

	return render(request, 'login_register/createItem.html', context)

def addItem(request):
	if request.method == "POST":
		errors = Item.objects.validateItem(request.POST)
		current_user = currentUser(request)

		if not errors:
			item = Item.objects.createItem(request.POST, current_user)

			request.session['item_id'] = item.id

			route = "/item_info/" + str(item.id)
			return redirect(route)

		flashErrors(request, errors)

	return redirect('/success')

def item_info(request, id):
	item = Item.objects.get(id=id)

	context = {
		'item': item
	}
	return render(request, "login_register/success.html", context)
