from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators	import login_required
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from django.contrib import messages #pacotes de mensagens para usuario
import datetime

@login_required
@csrf_exempt
def taskList(request):
	search = request.GET.get('search') #Search é o nome do input referente ao buscador
	filter = request.GET.get('filter')
	taskDoneRecently = Task.objects.filter(done='done', update_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
	taskDone = Task.objects.filter(done='done', user=request.user).count()
	taskDoing = Task.objects.filter(done='doing', user=request.user).count()

	if search: 
		tasks = Task.objects.filter(title__icontains=search, user=request.user)

	elif filter: 
		tasks = Task.objects.filter(done=filter, user=request.user)

	else:
		tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user) #Pegando todos os objetos Tasks do banco de dados
		
		paginator = Paginator(tasks_list,7)
		page = request.GET.get('page')
		tasks = paginator.get_page(page)

	return render(request, 'tasks/list.html', {'tasks':tasks, 'tasksrecently':taskDoneRecently, 'tasksdone':taskDone, 'tasksdoing':taskDoing})

@login_required
@csrf_exempt
def taskView(request, id):
	task = get_object_or_404(Task, pk=id)
	return render(request, 'tasks/task.html',{'task': task})

@login_required
@csrf_exempt
def newTask(request):
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.done = 'doing'
			task.user = request.user
			task.save()
			return redirect('/')

	else:
		form = TaskForm()
		return render(request, 'tasks/addtask.html', {'form': form})

@csrf_exempt
@login_required
def editTask(request,id):
	task = get_object_or_404(Task,pk=id)
	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST,instance=task)
		if form.is_valid():
			task.save()
			return redirect('/')
		else:
			return render(request, 'tasks/edittask.html',{'form': form, 'task': task})
	else:
		return render(request, 'tasks/edittask.html',{'form': form, 'task': task})
	
@csrf_exempt
@login_required
def deleteTask(request, id):
	task = get_object_or_404(Task, pk=id)
	task.delete()

	messages.info(request, 'Tarefa deletada com sucesso')

	return redirect('/')

@csrf_exempt
@login_required
def changeStatus(request, id):
	task = get_object_or_404(Task, pk=id)
	
	if task.done == 'doing':
		task.done = 'done'
	else: 
		task.done = 'doing'

	task.save()

	return redirect('/')