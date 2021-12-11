from django.core.exceptions import ValidationError
from django.db import models

__all__ = [
    'Poll',
    'Question',
    'Answer',
    'UserPoll',
    'UserAnswer',
]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Poll(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'#{self.id} {self.name}'


# вопрос из опроса
class Question(BaseModel):
    TYPE_TEXT, TYPE_SINGLE_CHOICE, TYPE_MULTIPLE_CHOICE = range(1, 4)
    TYPES = (
        (TYPE_TEXT, 'Text'),
        (TYPE_SINGLE_CHOICE, 'Single choice'),
        (TYPE_MULTIPLE_CHOICE, 'Multiple choice'),
    )

    text = models.TextField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    type = models.PositiveSmallIntegerField(choices=TYPES)

    def __str__(self):
        return f'#{self.id} {self.text[:50]}'


# хранит в себе предложенные варианты ответов
class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)

    # если вопрос текстовый(типа TYPE_TEXT), для него нет варианта ответа
    def clean(self):
        if self.question.type == 1:
            raise ValidationError("no answer variant for text question")

    def __str__(self):
        return f'#{self.id} {self.text[:50]}'


class UserPoll(BaseModel):
    user_id = models.PositiveIntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='user_polls')

    class Meta:
        unique_together = ('user_id', 'poll')


# хранит ответы пользователей
class UserAnswer(BaseModel):
    user_poll = models.ForeignKey(UserPoll, on_delete=models.CASCADE, related_name='user_answers')
    # на какой вопрос отвечает юзер
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    # какие ответы выбрал юзер
    answers = models.ManyToManyField(Answer, related_name='user_answers')
    # поля для ответа, если вопрос текстовый
    text = models.TextField(null=True)

    class Meta:
        unique_together = ('user_poll', 'question')

    # ограничение - заполнено либо поле text, либо answers, что-то одно в зависимости от Question.type
    def clean(self):
        if self.answers and self.text:
            raise ValidationError("only text OR question variants can be set")
