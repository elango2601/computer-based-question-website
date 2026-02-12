from django.contrib import admin
from .models import Test, Question, Result
from .forms import QuestionAdminForm

class QuestionInline(admin.TabularInline):
    model = Question
    form = QuestionAdminForm
    extra = 1
    # Use fields from form (which excludes 'options', includes 'options_csv')
    # Or just let form handle it.
    # TabularInline with custom form works better if fields are explicit or automatic.
    # Since form has options_csv, it will show up.
    
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'scheduled_date', 'duration_minutes', 'is_active', 'has_compiler')
    list_filter = ('scheduled_date', 'has_compiler')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('text', 'test', 'type', 'difficulty', 'category')
    list_filter = ('test', 'category', 'difficulty', 'type')
    search_fields = ('text',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'question', 'is_correct', 'timestamp')
    list_filter = ('test', 'is_correct', 'user')
