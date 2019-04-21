from django.shortcuts import render

# Create your views here.
def testHttpsApp(request, *args, **kwargs):
	return render(request,"testApp/httpstest.html")
