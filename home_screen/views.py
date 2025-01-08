from django.shortcuts import render, redirect
from django.template.defaultfilters import first

from accounts.models import Customer
def home(request):
    if request.method == 'POST':
        form_type = request.POST['action']  # Get the form type
        print("in " + form_type)

        if form_type == 'add-customer':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            id_number = request.POST['id_number']
            phone = request.POST['phone']
            city = request.POST['city']
            email = request.POST['email']
            internet_package = request.POST['internet_package']
            Customer.add(first_name, last_name, id_number, phone, city, email, internet_package)
            print("add customer submitted")
            customers = Customer.objects.all()
            return render(request, 'home.html', {'customers': customers})

        elif form_type == 'remove-customer':
            # Handle remove customer logic
            # Add your logic for handling the 'remove customer' form
            print("remove customer submitted")

        elif form_type == 'edit-customer':
            # Handle edit customer logic
            # Add your logic for handling the 'edit customer' form
            print("edit customer submitted")

        elif form_type == 'search-customer':
            # Handle search customer logic
            # Add your logic for handling the 'search customer' form
            print("search customer submitted")
    else:
        is_logged_in = request.session.get('isLoggedIn', False)
        print(is_logged_in)
        if is_logged_in == True:
            customers = Customer.objects.all()
        else:
            return redirect("login")

        return render(request, 'home.html', {'customers': customers})

