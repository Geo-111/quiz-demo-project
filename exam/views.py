from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Exam


def exam_list(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='exam/exam-list.html',
        context={'all_exams': Exam.objects.all()}
    )
