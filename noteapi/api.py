import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja import NinjaAPI, Schema
from ninja.security import django_auth
from ninja.security import HttpBearer

from noteapi.jwt import JwtUtils
from noteapi.models import Note
import hashlib


class UserLoginSchema(Schema):
    username: str
    password: str


class UserRegisterSchema(Schema):
    username: str
    password: str
    email: str


class NoteInSchema(Schema):
    id: str = "V1StGXR8_Z5jdHi6B-myT"
    content: str = "\n\n\n\n"
    lastContentMd5: str = ""
    background: str = "#ffffff"
    color: str = "#333333"
    state: int = 0
    public: bool = False
    top: int = 0
    secret: bool = False
    type: str = "note"
    createAt: str = "2023-01-24 06:13:00"
    updateAt: str = "2023-01-24 06:13:00"


class NoteOutSchema(Schema):
    id: str = "V1StGXR8_Z5jdHi6B-myT"
    content: str = "\n\n\n\n"
    contentMd5: str = ""
    background: str = "#ffffff"
    color: str = "#333333"
    state: int = 0
    secret: bool = False
    public: bool = False
    top: int = 0
    type: str = "note"
    author: str = ""
    createAt: str = "2023-01-24 06:13:00"
    updateAt: str = "2023-01-24 06:13:00"


class Result(Schema):
    code: int = 200
    message: str = "success"
    data: dict = {}


api = NinjaAPI(urls_namespace="note", csrf=False)


class InvalidToken(Exception):
    pass


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(request, {"detail": "用户不存在"}, status=401)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = JwtUtils.get_payload(token)
        username = payload.get('username')
        print(username)
        if username is None:
            raise InvalidToken()
        else:
            # if username == 'admin':
            #    return False
            return True


@api.get("/add", tags=["test"])
def add(request, a: int, b: int):
    return {"result": a + b}


@api.get("/hello", tags=["test"])
def hello(request):
    return "hello"


@api.get("/note", tags=["note"], response=Result, auth=AuthBearer(), summary="获取用户笔记的列表")
def index(request, search: str = "", state: int = 0):
    user_info = get_user_info_from_token(request)
    username = user_info.get('username')
    # user = User.objects.get(username=username)
    search_list = search.split(" ")

    notes = Note.objects.filter(author=username, content__icontains=search_list[0], state=state).\
        order_by('-top', '-createAt')
    for search_content in search_list:
        notes = notes.filter(content__icontains=search_content)

    data = []
    for note in notes:
        note.createAt = note.createAt.strftime("%Y-%m-%d %H:%M:%S")
        note.updateAt = note.updateAt.strftime("%Y-%m-%d %H:%M:%S")
        data.append(NoteOutSchema.from_orm(note))
    result = Result()
    result.data = data
    return result


@api.post("/note", auth=AuthBearer(), response=Result, tags=["note"], summary="添加笔记")
def create(request, note: NoteInSchema):

    user_info = get_user_info_from_token(request)
    id = note.id
    last_content_md5 = note.lastContentMd5
    del note.lastContentMd5
    old_note = Note.objects.filter(id=id).first()

    print(old_note)

    # 计算note.content的md5值

    m = hashlib.md5()
    m.update(note.content.encode("utf-8"))
    md5 = m.hexdigest()

    if old_note:
        # 更新
        if user_info.get('username') != old_note.author:
            return Result(code=401, message="无权限")

        if last_content_md5 != '' and old_note.contentMd5 != '' and last_content_md5 != old_note.contentMd5:
            return Result(code=402, message="内容已被修改，保存时产生了冲突，请复制笔记内容并刷新后再试")

        note = Note(**note.dict(), contentMd5=md5, author=user_info.get("username"))
        note.save()
        return {
            "code": 200,
            "message": "笔记更新成功",
            "data": {
                "note": NoteOutSchema.from_orm(note)
            }
        }
    else:
        # 新增
        note = Note(**note.dict(), contentMd5=md5, author=user_info.get("username"))
        note.save()
        return {
            "code": 200,
            "message": "笔记添加成功",
            "data": {
                "note": NoteOutSchema.from_orm(note)
            }
        }


@api.delete("/note/{id}", auth=AuthBearer(), response=Result, tags=["note"], summary="删除笔记")
def remove(request, id: str):
    user_info = get_user_info_from_token(request)
    username = user_info.get('username')

    if username == 'help':
        return {
            "code": 403,
            "message": "未防止帮助页面误操作，本账号不支持完全删除",
            "data": {}
        }

    # user = User.objects.get(username=username)
    note = Note.objects.get(id=id, author=username)
    if note:
        note.delete()
        return {
            "code": 200,
            "message": "笔记删除成功",
            "data": {}
        }
    else:
        return {
            "code": 500,
            "message": "笔记不存在",
            "data": {}
        }


# @api.get("/auth", auth=django_auth)
# def pets(request):
#     return f"Authenticated user {request.auth}"


def get_user_info_from_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token = token.split(" ")[1]
    user_info = JwtUtils.get_payload(token)
    return user_info


@api.get("/bearer", auth=AuthBearer(), tags=["test"], summary="权限测试")
def bearer(request):
    user_info = get_user_info_from_token(request)
    return {
        'code': 200,
        'message': 'test_auth正常使用',
        'data': {
            'user_info': user_info
        }
    }


@api.post("/login", summary="用户登录", response=Result, tags=["user"])
def login(request, user: UserLoginSchema):
    user = authenticate(username=user.username, password=user.password)
    if user is not None:
        token = JwtUtils.get_token({'username': user.username, 'auth': 'all'}) # 权限可以控制这个token的作用
        return {
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": token,
                "user_info": {'username': user.username, 'auth': 'all'}
            }
        }
    else:
        return {
            "code": 400,
            "message": "登录失败"
        }


@api.post('/register', response=Result, summary="用户注册", tags=["user"])
def register(request, user: UserRegisterSchema):
    if User.objects.filter(username=user.username).exists():
        return {
            "code": 400,
            "message": "用户已存在"
        }

    user = User.objects.create_user(username=user.username, password=user.password, email=user.email)
    token = JwtUtils.get_token({'username': user.username, 'auth': 'all'})  # 权限可以控制这个token的作用
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token
        }
    }