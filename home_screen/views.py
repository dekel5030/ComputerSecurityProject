from django.shortcuts import render
from .forms import CustomerForm

def home(request):
    customer = None
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            form = CustomerForm()

    else:
        form = CustomerForm()
    return render(request, 'home.html', {'form': form, 'customer': customer})


##def home(request):
    #print(f"Request method: {request.method}")
    #if request.method == 'POST' and request.POST.get('action') == 'ADD_CUSTOMER':
        # Get the submitted form data
        #name = request.POST.get('name')
        #Email = request.POST.get('email')
        #print(name)
        #print(Email)
        #print("asfgffffff")

    #return render(request,"home.html");