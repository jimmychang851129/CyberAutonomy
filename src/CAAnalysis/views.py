from django.shortcuts import render

# Create your views here.
def CAHome_page(request, *args, **kwargs):
	return render(request,"CAAnalysis/ca.html",{})