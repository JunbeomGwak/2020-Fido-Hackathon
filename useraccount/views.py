# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models     import User
from .models                        import UploadFileModel, User
from django.http import JsonResponse, Http404
from django.http                    import HttpResponse, HttpResponseRedirect
from .models                        import User
from board.models import Board
from django.shortcuts               import render, redirect
from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth            import authenticate
from .serializers                   import FidoSerializer
from rest_framework_jwt.settings    import api_settings
from .forms                         import UploadFileForm, LoginForm
from django.core.files              import File
from os.path                        import basename
from urllib.request                 import urlretrieve, urlcleanup
from urllib.parse                   import urlsplit
from django.db.models.signals       import post_save
from tempfile                       import TemporaryFile
from django.contrib.auth            import get_user_model
from rest_framework.viewsets import ModelViewSet
from django.template                import RequestContext
from django.core.files import File
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
User = get_user_model()

import json, jwt, mimetypes, os, requests, urllib

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_SECRET='FIDO_2020'
serverprivatekey="MIICWwIBAAKBgQDRKOpN7uhayaJc6FEx3Yrp6+wVcBsiayBqpke3Yp9VIfa0dDX4Ni5uyB1w+9eeWS8CHia6jXPf75yb1BKO6TFhTiGbbev9rTQlhPdgo57V1iv3Ew1JUFIsWyZFTmSSCaL7j/bHF7OenBBG0utXI8KersmKRQHqEOfmEpuw5vkmNQIDAQABAoGAGWxdvodRmudzYtOiOutw3SoeEiUER1S6Jfx8LyA/ubtdH2YYwUjkr/aHDZqvBMJWYm2Dy50x/oBDivVmJBTYOYFhaCqbWtblFgZ3jBTIIoA6Lpx7lxK4mGQ8fk9WVPjS7hRPfZZEJ6QVfLZKloaAc8P+p/l0hjOE1jhlRY9BPoECQQDqq2fFZPQ4leAegu3aW8mRr+NwHJd0Ts6SknGXKIHaDLTrGP5PDJNUwoRERd0VZr4QQrL8QLkkZUplEIn/r9QxAkEA5CvqpMAxjdDTEpeWk2Tg747RSQP9sRben901m/ZRIQAKYVQ+N/tfmOT4GpdwYU3bdokG+Kd+LcdCnrZ5OHAFRQJAMjr2P15YmDQcgOttlivHfZO0jy7PjGnB9cW64qwc/1tw7lGvPaRndOEeBq8dn5MaY8ijHzOLbarwvalIoJ42QQJAXoAN25Q6MdkmQlIELCGgw7br2QjNHnYxWBafKGwY58kDg5IHftoems1iMGk+Qx6i4XIZMAz2xnD7l45NoGFM3QJATOZRBBCX0QTbterJp5cvVCdizOETfBLIbc7prMw7F56rXpraAWCjAayfSFDV6Bc+CY+4S24jYAMm38w+rieAWA=="
programpubkey="MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDz/ni+WCbbUUSgNy+wNT9nmgKlOsNxOAxGkUT/M+Hxt+myP2ewMCoapd0lcDIcufNQOZ6rXpg+pT+Am8N3jATyrAhpActh/2+xgj7b05yg/Hmgok9+O/vpgHNasLhla4pAOVbiRBRpsiuAh0urtZcjGNYrEwkn15+1Oncjc5pR5wIDAQAB"
testprivatekey="fidopriavtekey"
@csrf_exempt
def signup(request): #일반유저 회원가입
    if request.method == 'GET':
        return render(request, 'useraccount/signup.html')

    elif request.method == 'POST':
        username = request.POST['name']
        userid = request.POST['id']
        company = request.POST['company']
        code = request.POST['code']

        #db에 저장
        account = User.objects.create_user(
            username=username,
            user_id = userid,
            company = company,
            companycode = code,
        )
        request.session['user'] = userid
        account.save()
        os.mkdir(os.path.join('media/account/', username))
    return render(request, 'useraccount/signup.html')

#web login
@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'useraccount/login.html')

    elif request.method == 'POST':
        id = request.POST.get('id')
        request.session['user'] = id
        return redirect('https://fidochallenge486.tk:8080/login/' + id, id=id)

@csrf_exempt
def program_login(request):
    if request.method == 'GET':
        return render(request, 'useraccount/login.html')

    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data["name"]
        #code = data["code"]
        test = User.objects.get(username=name)

        return JsonResponse({'name':name, 'id':test.user_id, 'company':test.company, 'code':test.companycode})
        #return JsonResponse({'success':'true','token':token}, status=200)

@csrf_exempt
def program_signup(request): #app_signup
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data["name"]
        userid = data["id"]
        company = data["company"]
        code = data["code"]
        payload = {"name":username, "id":userid, "company":company, "code":code}
        token = jwt.encode(payload, JWT_SECRET).decode('utf-8')
        account = User.objects.create_user(
            username=username,
            user_id=userid,
            company=company,
            companycode=code,
        )
        account.save()
        return JsonResponse({'Check': '1'}, status=200)

@csrf_exempt
#이름과 회사코드 공개키를 받으면 이름.pub으로 공개키 저장
def keystore(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        req_username = data["name"]
        req_companycode = data["code"]
        publickey = data["pbkey"]
        user = authenticate(username = req_username, companycode = req_companycode)
        if user is not  None:
            link = "useraccount/PublicKey/" + req_username + ".pub"
            f = open(link, "w")
            f.write(publickey)
            f.close()
            return HttpResponse('Success!', status=200)
        else:
            return HttpResponse("False!!", status=400)

@csrf_exempt
#복호화키, 이름, 파일이름을 받으면 synn, 복호화된 파일이름을 리턴
def receivefilekey(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Synkey = data["Synkey"]
        Recvname = data["Name"]
        filename = data["filename"]
        link = "useraccount/encryptedfile/" + str(Recvname) + "-" + str(filename)
        f = open(link, "w")
        f.write(Synkey)
        resultname = filename
        return JsonResponse({'Synkey':Synkey, "encrypt_filename":resultname}, status=200)

@csrf_exempt
#유저이름과 파일이름을 받고, 그 파일안에 있는 복호화 키전송, testfilekey가 아니라 다른이름으로 변경해야할듯
def receivesynkey(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        verify = data["username"]
        filename = data["filename"]
        link = "useraccount/encryptedfile/" + str(verify) + "-" + str(filename)
        if link is None:
            return JsonResponse({"status":"No file name!!"}, status=404)
        else:
            f = open(link, "r")
            print("file found!")
            synnkey = f.read()
            return JsonResponse({"synnkey":synnkey}, status=200)

@csrf_exempt
def encryptsynnkey(request): #synnkey 암호화
    if request.method == 'POST':
        data = json.loads(request.body)
        synkey = data["synkey"]
        name = data["name"]
        filename = data["filename"]
        key = RSA.importKey(testprivatekey)
        encryptor = PKCS1_OAEP.new(key)
        encrypted = encryptor.encrypt(synkey) #여기서 문
        link = "useraccount/encryptedfile/" + str(name)+ "-" + str(filename)
        f = open(link, "w")
        f.write(encrypted)
        f.close()

@csrf_exempt
def app_login(request, id):
    request.session['user'] = id
    return redirect('https://fidochallenge486.tk:8080/login/' + id, user_id=id)

@csrf_exempt
#시그널을 보내는 부분
def receivesignal(request): #시그널 보내는곳
    if request.method == 'POST':
        data = json.loads(request.body)
        Name = data["name"]
        signal= data["check_me"]
        Name = str(Name)
        if User.objects.filter(username=Name):
            return JsonResponse({"signal":"1"}, status=200)
        else:
            return JsonResponse({"signal":"0"}, status=400)

@csrf_exempt
def index(request):
    return render(request, 'useraccount/index.html', {})

@csrf_exempt
def file_list(request):
    return render(request, 'useraccount/list.html', {})

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')

    else:
        form = UploadFileForm()
    return render(request, 'useraccount/upload.html', {'form': form})

@csrf_exempt
def download_to_file(url, field):
    try:
        tempname, _ = urlretrieve(url)
        field.save(basename(urlsplit(url).path), File(open(tempname, 'wb')))
    finally:
        urlcleanup()

@csrf_exempt
def download_file(request, file):
    fl_path = 'useraccount/encryptedfile/'
    filename = str(file)
    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename = %s" % filename
    return response

@csrf_exempt
def test_upload(url, field):
    with TemporaryFile() as tf:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)

            tf.seek(0)
            field.save(basename(urlsplit(url).path, File(tf)))

@csrf_exempt
def return_list(request, name):
    if request.method == 'POST':
        username = name # useraccount/return_list/userename
        #data = json.loads(request.body)

        path = "useraccount/NameFolder/" + str(username) #경로 생성
        file_list = os.listdir(path)
        f = open(path+"/date.txt")
        date_list = [str(value) for value in f.read().split()]
        f.close()

        f = open(path+"/sender.txt")
        sender_list = [str(value) for value in f.read().split()]
        f.close()

        f = open(path+"/receiver.txt")
        receiver_list = [str(value) for value in f.read().split()]
        f.close()

        payload = {
            "file_list" : file_list,
            "sender_list" : sender_list,
            "date_list" : date_list
        }


        return JsonResponse(payload, safe=False, status=200)

# Create your views here.
def logout(request):
    if request.session.get('user'): # user의 세션ID가 존재한다면
        del(request.session['user']) # 현재 세션ID를 지워주고

    return redirect('/') # 홈으로 리다이렉트 해줌
@csrf_exempt
def home(request):
    user_id = request.session.get('user') # 세션으로부터 사용자 ID를 가져옴

    if user_id:
        user = User.objects.get(pk=user_id) # 모델에서 id를 기본키로해서 가져옴
        return HttpResponse(user.username) # 모델의 username을 출력 (로그인이 된경우)

    return HttpResponse("Home!") # 로그인이 되지 않은 경우 Home!출력

def register(request):
    if request.method == 'GET':
        return render(request, 'useraccount/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None) # 템플릿에서 입력한 name필드에 있는 값을 키값으로 받아옴
        password = request.POST.get('password', None) # 받아온 키값에 값이 없는경우 None값으로 기본값으로 지정
        re_password = request.POST.get('re-password', None)
        useremail = request.POST.get('useremail', None)

        res_data = {} # 응답 메세지를 담을 변수(딕셔너리)

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            user = User( # 모델에서 생성한 클래스를 가져와 객체를 생성
                username=username,
                useremail=useremail,
                password=make_password(password) # 비밀번호를 암호화하여 저장
            )

            user.save() # 데이터베이스에 저장

        return render(request, 'user/register.html', res_data) # res_data가 html코드로 전달이 됨

@csrf_exempt
def verity(request):
    if request.method == 'POST':
        dataa = json.loads(request.body)
        data = dataa['token']
        decoded = jwt.decode(data, JWT_SECRET, algorithms='HS256')
        name = decoded['name']
        code = decoded['code']
        user = authenticate(username=name, companycode=code)
        if user is not None:
            return HttpResponse('success!', status=200)

        return HttpResponse('false', status=404)


