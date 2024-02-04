from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    pass



class Task(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tasks")
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Add related_name to avoid clashes


