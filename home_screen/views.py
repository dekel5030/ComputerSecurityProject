from django.shortcuts import render

# Create your views here.
def home(request):
    print(f"Request method: {request.method}")
    if request.method == 'POST' and request.POST.get('action') == 'ADD_CUSTOMER':
        # Get the submitted form data
        name = request.POST.get('name')
        print(name)
        print("asfgffffff")

    return render(request,"home.html");