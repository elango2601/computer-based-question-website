from django.contrib import admin
from .models import Test, Question, Result

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'scheduled_date', 'duration_minutes', 'is_active', 'has_compiler')
    list_filter = ('scheduled_date', 'has_compiler')
    search_fields = ('title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'type', 'difficulty', 'category')
    list_filter = ('test', 'category', 'difficulty', 'type')
    search_fields = ('text',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'question', 'is_correct', 'timestamp')
    list_filter = ('test', 'is_correct', 'user')
