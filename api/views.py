from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import PollSerializer, UserPollSerializer, UserAnswerSerializer, UserPollListSerializer
from core.models import *


class PollViewSet(ReadOnlyModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

    def get_queryset(self):
        now = timezone.localtime()
        return Poll.objects.filter(start_date__lt=now, end_date__gt=now)

    @swagger_auto_schema(operation_summary="List all active polls")
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="See Poll detail by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @swagger_auto_schema(request_body=UserPollSerializer, operation_summary="Take a poll by ID")
    @action(detail=True, methods=['post'])
    def answer(self, request, pk):
        # Валидация poll, если он не существует - вернется ошибка 404
        poll = self.get_object()
        data = request.data

        user_poll_ser = UserPollSerializer(data=dict(poll=poll.id, **data))
        user_poll_ser.is_valid(raise_exception=True)
        user_poll = user_poll_ser.save()

        for answer_data in request.data['user_answers']:
            answer_data['user_poll'] = user_poll.id
            user_answer_ser = UserAnswerSerializer(data=answer_data)
            user_answer_ser.is_valid(raise_exception=True)
            user_answer_ser.save()

        return Response({'status': 'ok'})



class UserPollListView(ListAPIView):
    serializer_class = UserPollListSerializer
    queryset = UserPoll.objects.all()

    def get_queryset(self):
        return UserPoll.objects.filter(user_id=self.kwargs['user_id'])

    @swagger_auto_schema(operation_summary="Polls that user has completed", operation_description="description")
    def get(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)