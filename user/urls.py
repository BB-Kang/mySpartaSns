from django.urls import path
from . import views  # 지금 내가 있는 폴더에서 views 라는 파이선 파일을 가져올거야

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    # 주어진 포트에서 /sign-up 이라고 접근을 하면 view.py의 sign_up_view가 실행될것임임
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>', views.user_follow, name='user-follow'),
]