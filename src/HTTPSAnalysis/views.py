from django.shortcuts import render

# Create your views here.
def HTTPSHome_page(request, *args, **kwargs):
	return render(request,"HTTPSAnalysis/https.html",{})