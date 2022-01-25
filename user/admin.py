from django.contrib import admin
from .models import UserModel  # 내 경로에 있는 models.py 중 UserModel을 가져오겠다.

# Register your models here.
admin.site.register(UserModel) # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다