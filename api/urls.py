from rest_framework import routers
from django.urls import path

from api.views import PollViewSet, UserPollListView

router = routers.SimpleRouter()
router.register(r'polls', PollViewSet)

urlpatterns = [
    path('user_polls/<int:user_id>', UserPollListView.as_view()),
]
urlpatterns += router.urls
