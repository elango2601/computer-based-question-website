from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Test, Question, Result
from django.shortcuts import get_object_or_404
import random
from django.db.models import Count, Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tests(request):
    tests = Test.objects.all().order_by('scheduled_date')
    data = []
    for t in tests:
        total_q = t.questions.count()
        results = Result.objects.filter(user=request.user, test=t)
        attempted = results.count()
        score = results.filter(is_correct=True).count()
        # Simplified completed logic: if attempted > 0.
        # Ideally check if attempted == total_q or submitted flag.
        is_completed = attempted > 0
        
        data.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "scheduled_date": t.scheduled_date, # DateField serializes to YYYY-MM-DD string automatically by DRF? No, standard Response uses DjangoJSONEncoder? No, DRF uses JSONRenderer.
            # DRF JSONRenderer handles date objects -> ISO string.
            "duration_minutes": t.duration_minutes,
            "total_questions": total_q,
            "is_completed": is_completed,
            "score": score
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_test_questions(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = list(test.questions.all())
    random.shuffle(questions)
    
    q_data = []
    for q in questions:
        q_data.append({
            "id": q.id,
            "text": q.text,
            "type": q.type,
            "options": q.options,
            "category": q.category,
            "difficulty": q.difficulty
        })
        
    return Response({
        "test": {
            "title": test.title,
            "duration": test.duration_minutes,
            "has_compiler": test.has_compiler
        },
        "questions": q_data
    })

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    data = request.data
    q_id = data.get('questionId')
    answer = data.get('answer')
    
    question = get_object_or_404(Question, pk=q_id)
    is_correct = (question.correct_answer == answer)
    
    Result.objects.update_or_create(
        user=request.user,
        question=question,
        defaults={
            'test': question.test,
            'user_answer': answer,
            'is_correct': is_correct
        }
    )
    return Response({'is_correct': is_correct})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_test_stats(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    user = request.user
    
    total = Result.objects.filter(user=user, test=test).count()
    score = Result.objects.filter(user=user, test=test, is_correct=True).count()
    
    questions = test.questions.all().order_by('id')
    history = []
    
    # Efficiently fetch results
    results_map = {r.question_id: r for r in Result.objects.filter(user=user, test=test)}
    
    for q in questions:
        r_dict = {
            "id": q.id,
            "question_text": q.text,
            "correct_answer": q.correct_answer
        }
        res = results_map.get(q.id)
        if res:
            r_dict['user_answer'] = res.user_answer
            r_dict['is_correct'] = res.is_correct
            r_dict['status'] = 'answered'
        else:
            r_dict['user_answer'] = "Not Attempted"
            r_dict['is_correct'] = False
            r_dict['status'] = 'skipped'
        history.append(r_dict)
        
    return Response({
        "total": total,
        "score": score,
        "history": history
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_analytics(request):
    user = request.user
    # Get distinct tests user attempted
    test_ids = Result.objects.filter(user=user).values_list('test_id', flat=True).distinct()
    
    analytics = []
    for tid in test_ids:
        test = Test.objects.filter(pk=tid).first()
        if not test: continue
        
        total_questions = test.questions.count()
        if total_questions == 0: continue
        
        score = Result.objects.filter(user=user, test=test, is_correct=True).count()
        percentage = round((score / total_questions) * 100, 1) if total_questions > 0 else 0
        
        analytics.append({
            "test_id": test.id,
            "test_title": test.title,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "date": test.scheduled_date
        })
        
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.http import HttpResponse
from io import BytesIO
import datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_certificate(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    # Check score
    score = Result.objects.filter(user=request.user, test=test, is_correct=True).count()
    total = test.questions.count() or 1
    percentage = (score / total) * 100
    
    if percentage < 50:
        return Response({'error': 'Score too low for certificate (Need 50%)'}, status=400)
        
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Border
    p.setStrokeColor(colors.blue)
    p.setLineWidth(5)
    p.rect(50, 50, width-100, height-100)
    
    # Content
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(width/2, height-150, "Certificate of Completion")
    
    p.setFont("Helvetica", 20)
    p.drawCentredString(width/2, height-250, "This is to certify that")
    
    p.setFont("Helvetica-Bold", 25)
    p.drawCentredString(width/2, height-300, request.user.username)
    
    p.setFont("Helvetica", 20)
    p.drawCentredString(width/2, height-350, "has successfully completed the exam")
    
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width/2, height-400, test.title)
    
    p.setFont("Helvetica", 18)
    p.drawCentredString(width/2, height-450, f"with a score of {score}/{total} ({percentage:.1f}%)")
    
    p.drawCentredString(width/2, height-550, "Date: " + str(datetime.date.today()))
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{test.id}.pdf"'
    return response
