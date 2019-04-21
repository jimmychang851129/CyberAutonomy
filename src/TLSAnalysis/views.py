from django.shortcuts import render

# Create your views here.
def TLSHome_page(request, *args, **kwargs):
	return render(request,"TLSAnalysis/tls.html",{})