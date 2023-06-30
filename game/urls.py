from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'rates', views.RateViewSet)
router.register(r'games', views.GameViewSet)

app_name = "game"
urlpatterns = [
    path('', include(router.urls)),
    path("<int:game_id>/gacha/", views.Gacha.as_view(), name="gacha"),
    path("<int:game_id>/", views.GameView.as_view(), name="game"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

