from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse  # 화면에 글자 띄울때
from django.contrib.auth import get_user_model  # 사용자가 db 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated

        if user:
            return redirect('/')  # user가 로그인 되어있는 상태라면 > signup 페이지는 볼 수 없다.
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        # POST로 가져온 데이터 중 username이라고 되어있는 데이터를 가져오고 없으면 빈칸처리 후 username이라는 변수에 저장한다
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')




        if password != password2:
            return render(request, 'user/signup.html',{'error': '패스워드를 확인 해 주세요!'})
            # 일치 하지 않는 경우 페이지 다시 페이지 출력해서 재입력 받도록
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html',{'error': '사용자 이름과 비밀번호는 필수 값 입니다!'})

            check_user_duplication = get_user_model().objects.filter(username=username)
            # .filter는 데이터가 없어도 오류가 안생김 > None으로 이해.
            # .get은 데이터가 없는 경우 오류 발생

            if check_user_duplication:
                return render(request, 'user/signup.html', {'error': '사용자가 존재합니다!'})
                # 중복된 username을 사용할 경우 다시 페이지 출력해서 재입력 받도록
            else:
                # new_user = UserModel()
                # new_user.username = username
                # new_user.password = password
                # new_user.bio = bio
                # # 여기 까지 하면 실제로 우리 db에 저장된것은 아님
                # new_user.save()
                # # 이제야 작성한 정보들이 db에 저장됨

                # 위 5줄을 압축시켜서 간결하게 작성
                UserModel.objects.create_user(username=username, password=password, bio=bio)

                # 다 저장되면 로그인 페이지가 출력되었으면 좋겠다 > redirect
                return redirect('/sign-in')

# 화면을 보여줄 때
def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 장고 모듈 .authenticate: 암호화된 비밀번호와 입력한 비밀번호가 일치하는지 확인하는 함수, 아래 * 표시들을 대체함
        me = auth.authenticate(request, username=username, password=password)
        # db에 있는 유저인지 확인하는 과정
        # * me = UserModel.objects.get(username=username)  # UserModel은 이미 db와 연결되어 있는 객체, 거기에서 조건을 걸어서 데이터를 가져온다

        if me is not None:
            auth.login(request, me) # 사용자가 비어있지 않으면 그 사용자를 로그인 시켜준다.
            return redirect('/') # / 라는 기본 url로 이동
        # * if me.password == password:
            # * request.session['user'] = me.username
            # session(사용자 정보를 저장할 수 있는 공간)의 user에 me.username을 넣었다. 로그인 상태로 만들어 줌
        else:
            return render(request, 'user/signin.html', {'error': '유저이름 혹은 패스워드를 확인해주세요!'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required  # 사용자가 로그인이 꼭 되어있어야만 접근 가능한 함수 라는 뜻!
def logout(request):
    auth.logout(request)  # 장고에 내장된 logout 기능
    return redirect('/')  # logout 에 대한 url도 추가해줘야함 > user 앱의 urls.py에다가!


# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 나를 제외한 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    # 내가 클릭한 사람
    click_user = UserModel.objects.get(id=id)
    # 내가 클릭한 사람의 팔로워 목록에 내가 있으면 나를 빼준다(팔로우 취소)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    # 내가 클릭한 사람의 팔로워 목록에 내가 없으면 나를 넣는다(팔로우 신청)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')

