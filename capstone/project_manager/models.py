from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

class TodoList(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

class Todo(models.Model):
    content = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    notify = models.BooleanField(default=True)
    due_on = models.DateField()
    starts_on = models.DateField()
    list_id = models.ForeignKey(TodoList, on_delete=models.CASCADE)

class People(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    personable_type = models.CharField(max_length=5)
    title = models.CharField(max_length=50)
    bio = models.CharField(max_length=200)
    admin = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)
    time_zone = models.CharField(max_length=15)
    avatar_url = models.URLField()

class ProjectPeople(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    people_id = models.ForeignKey(People, on_delete=models.CASCADE)

class Message(models.Model):
    subject = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
