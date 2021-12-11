from django.contrib.postgres.fields import JSONField
from drf_yasg import openapi
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from core.models import *


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'text',
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'type',
            'answers',
        ]


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
            'questions',
        ]


class UserAnswerSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        fields['answers'].required = False
        return fields

    #You can choose only one answer for single choise question
    def validate_answers(self, answers):
        question_type = Question.objects.filter(id=self.initial_data['question']).values_list('type', flat=True).first()
        if question_type == Question.TYPE_SINGLE_CHOICE and len(answers) > 1:
            raise ValidationError(
                f'You can choose only one answer for question with id {self.initial_data["question"]}'
            )
        return answers

    class Meta:
        model = UserAnswer
        fields = [
            'id',
            'user_poll',
            'question',
            'answers',
            'text',
        ]


class UserPollSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = UserPoll
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "User poll",
            "properties": {
                "user_id": openapi.Schema(
                    title="User id",
                    type=openapi.TYPE_INTEGER,
                ),
                "user_answers": openapi.Schema(
                    title="User answers",
                    type=openapi.TYPE_ARRAY,
                    items= {
                        "type": openapi.TYPE_OBJECT,
                        "title": "User answer",
                        "properties": {
                            "question": openapi.Schema(
                                title="Question id",
                                type=openapi.TYPE_INTEGER,
                            ),
                            "answers": openapi.Schema(
                                title="if question has answer variants",
                                type=openapi.TYPE_ARRAY,
                                items={"type": openapi.TYPE_INTEGER, }
                            ),
                            "text": openapi.Schema(
                                title="if question of text type",
                                type=openapi.TYPE_STRING,
                            ),

                        }
                    }
                ),
            },
            "required": ["user_id", "user_answers"],
         }
        fields = [
            'id',
            'user_id',
            'poll',
            'user_answers',
        ]

# List Serializers


class AnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'text',
        ]


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'type',
        ]


class UserAnswerListSerializer(serializers.ModelSerializer):
    question = QuestionListSerializer(read_only=True)
    answers = AnswerListSerializer(many=True, read_only=True)

    class Meta:
        model = UserAnswer
        fields = [
            'id',
            'question',
            'answers',
            'text',
        ]


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
        ]


class UserPollListSerializer(serializers.ModelSerializer):
    poll = PollListSerializer(read_only=True)
    user_answers = UserAnswerListSerializer(many=True, read_only=True)

    class Meta:
        model = UserPoll
        fields = [
            'id',
            'user_id',
            'poll',
            'user_answers',
        ]
