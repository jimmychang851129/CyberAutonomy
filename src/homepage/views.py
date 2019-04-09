from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# args,kwargs pass request information
def home_page(request, *args, **kwargs):
	# return HttpResponse("<h1>Hello</h1>")
	return render(request,"index.html",{})