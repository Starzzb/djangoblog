from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="问题")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = "问题"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name="问题"
    )
    choice_text = models.CharField(max_length=200, verbose_name="选项")
    votes = models.IntegerField(default=0, verbose_name="票数")

    class Meta:
        verbose_name = "选项"
        verbose_name_plural = "选项"

    def __str__(self):
        return self.choice_text
