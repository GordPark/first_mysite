from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question, Choice
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.db.models import Sum, Max
# 원하는 클래스 가져오기
from django.views.generic import UpdateView

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

# Choice - UpdateView
class ChoiceUpdateView(generic.edit.UpdateView):
    model = Choice
    fields = ['choice_text'] # , 'pub_date'
    template_name = 'prg_pj/choice_update_form.html'   # 새로운 템플릿 또는 기존 템플릿 지정

    def get_success_url(self):
        # 선택지가 업데이트된 후, 선택지가 속한 질문의 상세 페이지로 리다이렉션
        choice = self.object
        ## 리다이렉트 문제
        return reverse('prg_pj:detail', kwargs={'question_id': choice.question.pk})

# Question - UpdateView
class QuestionUpdateView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text'] # , 'pub_date'
    template_name = 'prg_pj/question_update_form.html'  # 재사용하거나 적절한 템플릿 지정
    success_url = reverse_lazy('prg_pj:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요


# Question - DeleteView
class QuestionDeleteView(generic.edit.DeleteView):
    model = Question
    template_name = 'prg_pj/question_confirm_delete.html'
    success_url = reverse_lazy('prg_pj:index')  # 삭제 후 리다이렉션될 URL, 실제 프로젝트에 맞게 수정 필요

# ChoiceView
class ChoiceCreateView(generic.edit.CreateView):
    model = Choice
    fields = ['choice_text']    
    template_name = 'prg_pj/choice_form.html'
    def form_valid(self,form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('prg_pj:detail', kwargs={'question_id': self.kwargs['pk']})
    # 정적인 주소
    # success_url = reverse_lazy('prg_pj:index')

# CreateView
class QuestionCreateView(generic.edit.CreateView):
    model = Question
    fields = ['question_text'] # , 'pub_date'
    template_name = 'prg_pj/question_form.html'
    success_url = reverse_lazy('prg_pj:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요


# IndexView
class IndexView(generic.ListView):
    # [app_name]/[model_name]_list.html
    # templates폴더안에 html 이름을 _list로 끝나게 만들면 template_name을 지정안해도 됨
    template_name = "prg_pj/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last fiv publisehd questions."""
        return Question.objects.order_by("-pub_date")[:10]

# DetailView
class DetailView(generic.DetailView):
    model = Question
    template_name = "prg_pj/detail.html"
    def get_object(self):                
        q_id = self.kwargs['q_id']
        question = get_object_or_404(Question, pk=q_id)
        return question




# ResultsView
class ResultsView(generic.DetailView):
    model = Question
    template_name = "prg_pj/results.html"

# 최근 설문조사 질문 목록
class RecentlyView(generic.ListView):
    model = Question
    template_name = "prg_pj/recently.html"
    context_object_name = "latest_question_list"
    # queryset = Question.objects.all()  # 새로운 queryset를 정의함


    def get_queryset(self):
        """Return the last fiv publisehd questions."""
        return Question.objects.order_by("-pub_date")[:3]
    
# 가장 많은 투표를 받은 질문
# 전체 퀘스쳔 가져오기
# 각 퀘스쳔 별로 votes를 어떻게 구하지
# 총합을 구하기
# 정렬은 어떻게 할까
# 하나 question -> q.choice_set.all() : choice들 -> sum[] 리스트컴프리헨션

class MostVotedView(generic.DetailView):
    model = Choice
    template_name = "prg_pj/mostvoted.html"    
    most_voted = Choice.objects.aggregate(most_voted=Max('votes'))


    def get_queryset(self):
        """Return the last fiv publisehd questions."""
        return Choice.objects.order_by('votes')[:5]


# 아직 투표가 없는 질문 목록
class UnVotedView(generic.DetailView):
    model = Choice
    template_name = "prg_pj/unvoted.html"

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:10]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "prg_pj/index.html", context)

# index1을 만들고, index1.html을 만들어서 동작시켜 보기
def ex_index(request):
    testviews_idx = Question.objects.order_by("-pub_date")
    context = {
        "latest_question_list": testviews_idx
        }
    return render(request, "prg_pj/ex.html", context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "prg_pj/detail.html", {"question": question})

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

# def results(request, question_id):    
#     question = get_object_or_404(Question, pk=question_id)
    
#     return render(request, "prg_pj/results.html",  {"question":question})
    # return HttpResponse("You're looking at the results of question %s." % question_id)

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
        # 모든 선택지의 투표수 1증가
        Choice.objects.filter(question_id=question_id).update(votes=F('votes')+1)
        # 특정 선택지의 투표 수 감소
        Choice.objects.filter(question_id=question_id).update(votes=F('votes')-1)
        
        
        # 모든 선택지의 튜표 두배로 늘리기
        Choice.objects.filter(question_id=question_id).update(votes=F('votes')*2)

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

