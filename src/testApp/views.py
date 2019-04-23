from django.shortcuts import render

# Create your views here.
def testHttpsApp(request, *args, **kwargs):
	return render(request,"testApp/httpstest.html")

def testHSTSApp(request, *args, **kwargs):
	return render(request,"testApp/hststest.html")

def testTLSApp(request, *args, **kwargs):
	return render(request,"testApp/tlstest.html")