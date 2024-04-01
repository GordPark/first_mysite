from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question, Choice
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.utils import timezone

# Create your views here.
# def index(request):   
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("prg_pj/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, world. You're at the polls index.")
## 장고의 단축 / 위와같은내용
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "prg_pj/index.html", context)
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:10]
    context = {"latest_question_list": latest_question_list}
    return render(request, "prg_pj/index.html", context)

# index1을 만들고, index1.html을 만들어서 동작시켜 보기
def ex_index(request):
    testviews_idx = Question.objects.order_by("-pub_date")
    context = {
        "latest_question_list": testviews_idx
        }
    return render(request, "prg_pj/ex.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "prg_pj/detail.html", {"question": question})

def ex_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "prg_pj/ex.html", {"question": question})

# 404에러
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "prg_pj/index.html", {"question": question})

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# 힌트: filter사용
def result_pd():
    today_date = timezone.now().date() 
    # context = {
    #     Question.objects.get.all()
    # }
    response = Question.objects.filter(Question.question_text,pub_date__date=today_date)
    # response = Question객체 ID
    return HttpResponse(f"Question 문자열을 다 합치면 {today_date}입니다.")
    

def return_Hello(request):
    response = "Hello World!"
    return HttpResponse(response)

def results(request, question_id):    
    return HttpResponse("You're looking at the results of question %s." % question_id)

from django.db.models import F
def vote(request, question_id):
    # choice 데이터에서 해당하는 값에 votes를 1 더하기
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "prg_pj/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("prg_pj:results", args=(question.id,)))
    
    # return HttpResponse("You're voting on question %s." % question_id)

def test(request, question_id):
    return HttpResponse("test text %s. " % question_id)

# question_id 말고 다른 이름으로 받아도 될까
# A. 매개변수 설정 바꿔야하고 바꾼다면 urls에서도 해당하는 자료형으로 바꿔야함
# 숫자가 아닌게 들어오면 어떻게 되지?
# A. url패턴에서 int형으로 설정했고 매칭되는 자료형이 맞지 않음
# 404 Using the URLconf defined in config.urls, Django tried these URL patterns, in this order:

# prg_pj/ [name='index']
# prg_pj/ <int:question_id>/ [name='detail']
# prg_pj/ <int:question_id>/results/ [name='results']
# prg_pj/ <int:question_id>/vote/ [name='vote']
# admin/
# The current path, prg_pj/a/, didn’t match any of these.

# You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.

# 2개 다른 경로로 들어오고 question_id가 표시되는 view의 함수를 만들어 봅시다


# 11시 30분까지

