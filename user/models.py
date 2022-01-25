
# user/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # 이건 장고한테 시켜서! 장고가 관리하는!
# from mySpartaSns import settings  이건 우리가 한번 더 일하는 것


# Create your models here.
class UserModel(AbstractUser): # 장고에서 제공하는 기본적인 유저 모델(AbstarctUser)을 사용하겠다 = 상속
    class Meta:
        db_table = "my_user"  # db 테이블 이름 지정, db에 데이터 넣어 주는 역할

    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    # 우리의 유저 모델을 참조하겠다. follow 안에 들어가는 정보들은 사용자 정보이다!


