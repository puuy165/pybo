from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from ..models import Question

# Create your views here.
def index(request):
    # 입력인자
    page = request.GET.get('page', 1)
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')
    ca = request.GET.get('ca', '0')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter = Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer = Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    #카테고리
    if ca and ca != '0':
        print("들어옴")
        question_list = question_list.filter(
            Q(category__pk__icontains=ca)
        ).distinct()

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'ca': ca}

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 목록 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    so = request.GET.get('so', 'recent')
    is_view = request.GET.get('is_view', 0)

    if is_view == 0:
        question.views += 1
        question.save()

    if so == 'recommend':
        answer_list = question.answer_set.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    else:
        answer_list = question.answer_set.order_by('-create_date')

    context = {'question': question, 'answer_list': answer_list, 'so': so, 'is_view': 1}
    return render(request, 'pybo/question_detail.html', context)
