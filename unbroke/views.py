from django.shortcuts import render

# Create your views here.

def IndexView(request):
    return render(request, 'unbroke/index.html', {})
    
def RegisterView(request):
    return render(request, 'unbroke/register.html', {})