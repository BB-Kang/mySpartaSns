from django.contrib import admin
from .models import MyTopping, MyPizza



# Register your models here.

# 어드민 화면에 우리가 만든 모델을 적용하기
admin.site.register(MyPizza)
admin.site.register(MyTopping)


