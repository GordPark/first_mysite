# path 경로 끝에는 /를 기본적으로 붙여줘야 한다
# 보통 웹 애플리케이션의 일관성을 유지하고 URL 경로를 명확하게 구분하기 위함
from django.urls import path
# views에 구현한 기능을 임포트
from . import views

app_name = "prg_pj"
urlpatterns = [
    # 루트 URL "" , views.index에서 호출하고 패턴의 이름은 index
    # path("", views.index, name="index"),
    
    path("", views.IndexView.as_view(), name="index"),
    # path("", views.index1, name="index1"),
    #int형 question_id를 받는 URL에 대한 요청을 처리, views.detail에서 호출하고 패턴 이름은 detail
    # /polls/5/  와 같은형식이고 세부 정보를 세부 정보를 보여줌
    # path("<int:question_id>/", views.detail, name="detail"),
    path("<int:q_id>/", views.DetailView.as_view(), name="detail"),
    # int형 question_id를 받는 URL에 대한 요청을 처리, views.results를 호출하고 
    # /polls/5/results/ 와 같은 형식
    # path("<int:question_id>/results/", views.results, name="results"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/recently/", views.RecentlyView.as_view(), name="recently"),
    path("<int:pk>/mostvoted/", views.MostVotedView.as_view(), name="mostvoted"),
    path("<int:pk>/unvoted/", views.UnVotedView.as_view(), name="unvoted"),
    path("question/new/", views.QuestionCreateView.as_view(), name="question_new"),
    path("question/<int:pk>/choice/new/", views.ChoiceCreateView.as_view(), name="choice_new"),
    path("question/<int:pk>/update/", views.QuestionUpdateView.as_view(), name="question_update"),
    path("choice/<int:pk>/update/", views.ChoiceUpdateView.as_view(), name="choice_update"),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    

    # int형 question_id를 받는 URL에 대한 요청을 처리, views.results를 호출하고 
    # /polls/5/vote/ 와 같은 형식
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/test/", views.test, name="test"),
    path("result_pd/", views.result_pd, name="result_pd"),
    path("return_Hello/", views.return_Hello, name="return_Hello"),

    path("ex/", views.ex_index, name="ex_index"),
    path("ex/<int:question_id>/", views.ex_detail, name="ex_detail"),


]