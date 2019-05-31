import json
import urllib.request as req
import urllib.parse as par

from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

from classInfo.models import Teacher
from .models import Users, Student


# Create your views here.


class API:
    @api_view(['GET', 'POST'])
    def login_check(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            username = data["username"]
            sessionid = data["sessionid"]
            token = data["token"]
            role = data["role"]
            class_no = data["class_no"]
            no_user = False
            try:
                response = Users.objects.get(username=username)

            except Exception as e:
                no_user = True

            if no_user is False:
                if response.token != "" and response.token == token:
                    return Response({
                        "code": 1
                    })
            data = {
                "username": username,
                "sessionid": sessionid,
                "token": token
            }
            url = settings.LOGIN_CHECK_URL

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
            }
            try:
                data = par.urlencode(data).encode("utf-8")
                res = req.Request(url, data=data, headers=headers)
                res = req.urlopen(res).read().decode('unicode_escape')
                res_data = json.loads(res)

            except Exception as e:
                return Response({
                    "code": -2,
                    "message": "请求错误",
                })

            if True:
                if no_user is True:
                    db_operate = Users(
                        username=username,
                        token=token
                    )
                    db_operate.save()
                else:
                    Users.objects.filter(username=username).update(
                        token=token
                    )

                if role == "teacher":
                    try:
                        response = Teacher.objects.get(teacher_name=username)

                    except Exception as e:
                        db_operate = Teacher(
                            teacher_name=username,
                            class_no=class_no
                        )
                        db_operate.save()
                else:
                    try:
                        response = Student.objects.get(student_name=username)

                    except Exception as e:
                        db_operate = Student(
                            student_name=username,
                            class_no=class_no
                        )
                        db_operate.save()

                return Response({
                    "code": 1,
                    "message": "成功",
                })

            else:
                return Response({
                    "code": -1,
                    "message": "失败",
                })
