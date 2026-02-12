from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
from users import views as user_views
from exams import views as exam_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/login', user_views.login_view),
    path('api/me', user_views.me_view),
    path('api/logout', user_views.logout_view),
    
    path('api/admin/questions', exam_views.admin_questions),
    path('api/admin/questions/<int:pk>', exam_views.admin_delete_question),
    
    path('api/admin/tests', exam_views.admin_tests),
    path('api/admin/tests/<int:pk>', exam_views.admin_delete_test),
    path('api/admin/tests/<int:pk>/toggle', exam_views.admin_toggle_test),
    path('api/admin/tests/<int:pk>/update', exam_views.admin_update_test),
    
    path('api/tests', exam_views.get_tests),
    path('api/tests/<int:test_id>/questions', exam_views.get_test_questions),
    path('api/submit', exam_views.submit_answer),
    path('api/tests/<int:test_id>/stats', exam_views.get_test_stats),
    path('api/tests/<int:test_id>/certificate', exam_views.download_certificate),
    path('api/user/analytics', exam_views.get_user_analytics),
    
    # Frontend Pages
    path('', TemplateView.as_view(template_name='index.html')),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html')),
    path('quiz.html', TemplateView.as_view(template_name='quiz.html')),
    path('solution.html', TemplateView.as_view(template_name='solution.html')),
    path('admin.html', TemplateView.as_view(template_name='admin.html')),
    
    # Static files (Dev only)
    re_path(r'^css/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'public/css'}),
    re_path(r'^js/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'public/js'}),
]
