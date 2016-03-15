from django.shortcuts import render

# Create your views here.

class IndexView():
	return render(request, 'polls/index.html', {})