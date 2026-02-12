from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice


def index(request):
    """投票首页 - 显示最新问题列表"""
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    """投票详情页 - 显示问题和选项"""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    """投票结果页 - 显示投票结果"""
    question = get_object_or_404(Question, pk=question_id)
    total_votes = sum(choice.votes for choice in question.choice_set.all())
    return render(
        request,
        "polls/results.html",
        {"question": question, "total_votes": total_votes},
    )


def vote(request, question_id):
    """处理投票"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # 没有选择选项，重新显示表单并显示错误信息
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "请选择一个选项。",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 投票成功后重定向到结果页面（防止重复提交）
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
