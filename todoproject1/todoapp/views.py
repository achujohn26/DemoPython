
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from todoapp.forms import Todoform
from todoapp.models import Task
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

class TaskListview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'

class TaskDetailview(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'


class TaskUpdateview(UpdateView):
    model = Task
    template_name = 'edit.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk:self.object.id'})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')

# Create your views here.
def add(request):
    if request.method == "POST":
        name = request.POST.get("task")
        priority = request.POST.get("priority")
        date = request.POST.get("date")
        task = Task(name=name, priority=priority, date=date)
        task.save()
    task1 = Task.objects.all()
    return render(request, 'home.html', {'tasks': task1})


def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == "POST":
        task.delete()
        return redirect("/")
    return render(request, "delete.html")


def update(request, taskid):
    task = Task.objects.get(id=taskid)
    form1 = Todoform(request.POST or None, instance=task)
    if form1.is_valid():
        form1.save()
        return redirect('/')
    return render(request, "edit.html", {'task': task, 'form1': form1})




