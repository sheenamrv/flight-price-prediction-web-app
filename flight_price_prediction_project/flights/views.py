from django.shortcuts import render

# Create your views here.

# For landing/home page
def landing_page(request):
    return render(request, "flights/landing_page.html")

# For flights search page
def flights_search_page(request):
    # add code for data then it'll be passed to render function below

    return render(request, "flights/flights_search_page.html")