from django.shortcuts import render

# Create your views here.
def HSTSHome_page(request, *args, **kwargs):
	return render(request,"HSTSAnalysis/hsts.html",{})