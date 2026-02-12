from django.db import models
from django.conf import settings

class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    scheduled_date = models.DateField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)
    has_compiler = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    type = models.CharField(max_length=20, default='mcq') # mcq, text
    options = models.JSONField(default=list, blank=True) # Requires db that supports JSON
    correct_answer = models.TextField()
    category = models.CharField(max_length=50, default='General')
    difficulty = models.CharField(max_length=20, default='Medium')
    
    def __str__(self):
        return self.text[:50]

class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
