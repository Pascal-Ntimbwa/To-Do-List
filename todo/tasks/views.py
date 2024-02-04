from django.shortcuts import render, redirect
from .models import Task, User
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError






@login_required
def index(request):
    try:
        tasks = Task.objects.filter(created_by=request.user).order_by('-created_at')

        paginator = Paginator(tasks, 4)
        page_number = request.GET.get("page")
        tasks_per_page = paginator.get_page(page_number)

        return render(request, 'tasks/index.html', {
            'tasks_per_page': tasks_per_page,
        })
    except Task.DoesNotExist:
        return render(request, 'tasks/index.html', {
            'tasks_per_page': None,
        })


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        task = Task.objects.create(title=title, created_by=request.user)
        task.save()
    return redirect('index')


@login_required
def delete_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id, created_by=request.user)
        task.delete()
    except Task.DoesNotExist:
        pass
    return redirect('index')



@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            task_to_edit = Task.objects.get(pk=task_id, created_by=request.user)
            task_to_edit.title = data["content"]
            task_to_edit.save()
            return JsonResponse({"message": "Change Succeeds", "data": data["content"]})
        except Task.DoesNotExist:
            return JsonResponse({"message": "Task not found for the user"}, status=400)



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tasks/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tasks/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tasks/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tasks/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tasks/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


    
