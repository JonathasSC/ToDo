from django.shortcuts import render

from django.http import HttpResponse

def helloWorld(request):
	return HttpResponse('Olá mundo!')
def taskList(request):
	return render(request,'tasks/list.html')
