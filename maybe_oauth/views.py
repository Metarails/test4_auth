import base64
import hashlib
import random
import string

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.views.generic import ProtectedResourceMixin, ProtectedResourceView
from rest_framework import generics, status
from rest_framework import views as rest_views
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CoolBeans
from .serializers import AllUsersSerializer, CoolBeansSerializers

User = get_user_model()


# Create your views here.
class AllBeans(generics.ListAPIView):
    """
    First test view
    """

    serializer_class = CoolBeansSerializers
    queryset = CoolBeans.objects.all()


class AllUsers(generics.ListAPIView):
    serializer_class = AllUsersSerializer
    queryset = User.objects.all()


class GettingThingsOut(APIView):
    def get(self, request):
        # code_verifier = "".join(
        #     random.choice(string.ascii_uppercase + string.digits)
        #     for _ in range(random.randint(43, 128))
        # )
        # code_verifier = base64.urlsafe_b64encode(code_verifier.encode("utf-8"))

        # code_challenge = hashlib.sha256(code_verifier).digest()
        # code_challenge = (
        #     base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
        # )

        code_verifier = settings.CODE_VERIFIER
        code_challenge = settings.CODE_CHALLENGE

        # manual_id = "lQA2LVXfu34gnLk1aZJYxXeRNwFozz2Ql7G1UuLv"
        # manual_secret = "pbkdf2_sha256$600000$vyqUsKxziF4piMk2vnsNxo$ItGIKLf73i0S7/E+7+FoD7enFEkhEds3MPmir5ASe6k="

        data = {
            "code_verifier": code_verifier,
            "code_challenge": code_challenge,
            "response_type": "code",
            "code_challenge_method": "S256",
            "client_id": settings.CLIENT_ID,
            # "client_id": "lQA2LVXfu34gnLk1aZJYxXeRNwFozz2Ql7G1UuLv",
            "redirect_uri": "http://127.0.0.1:8000/responsethings/",
            # "redirect_uri": "http://127.0.0.1:8000/responsethings",
        }

        # Example
        # http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge=XRi41b-5yHtTojvCpXFpsLUnmGFz6xR15c3vpPANAvM&code_challenge_method=S256&client_id=vW1RcAl7Mb0d5gyHNQIAcH110lWoOW2BmWJIero8&redirect_uri=http://127.0.0.1:8000/noexist/callback

        visit_url = f"http://127.0.0.1:8000/o/authorize/?response_type={data['response_type']}&code_challenge={code_challenge}&code_challenge_method={data['code_challenge_method']}&client_id={data['client_id']}&redirect_uri={data['redirect_uri']}"
        data["visit_url"] = visit_url

        return Response(data)


class ResponseThingsView(APIView):
    def get(self, request, *args, **kwargs):
        print("request: ", request)
        print("request data: ", request.data)
        print("request data params:", request.query_params)
        print("secret: ", settings.SECRET)

        # manual_id = "lQA2LVXfu34gnLk1aZJYxXeRNwFozz2Ql7G1UuLv"
        # manual_secret = "pbkdf2_sha256$600000$vyqUsKxziF4piMk2vnsNxo$ItGIKLf73i0S7/E+7+FoD7enFEkhEds3MPmir5ASe6k="

        if "code" in request.query_params:
            curl_test_1 = (
                f"curl -X POST "
                f'-H "Cache-Control: no-cache" '
                f'-H "Content-Type: application/x-www-form-urlencoded" '
                f'"http://127.0.0.1:8000/o/token/" '
                f'-d "client_id={settings.CLIENT_ID}" '
                # f'-d "client_id={manual_id}" '
                f'-d "client_secret={settings.SECRET}" '
                # f'-d "client_secret={manual_secret}" '
                f'-d "code={request.query_params["code"]}" '
                f'-d "code_verifier={settings.CODE_VERIFIER}" '
                f'-d "redirect_uri=http://127.0.0.1:8000/responsethings/" '
                f'-d "grant_type=authorization_code"'
            )
        else:
            curl_test_1 = "derp"
        print("curl: ", curl_test_1)
        data = {
            "request": request.data,
            "args": args,
            "kwargs": kwargs,
            "query_params": request.query_params,
            "curl": curl_test_1,
        }

        # post_data = {
        #     "client_id": {settings.CLIENT_ID},
        #     "client_secret": {settings.SECRET},
        #     "code": {request.query_params["code"]},
        #     "code_verifier": {settings.CODE_VERIFIER},
        #     "redirect_uri": "http://127.0.0.1:8000/responsethings/",
        #     "grant_type": "authorization_code",
        # }
        # r = requests.post("http://127.0.0.1:8000/o/token/", timeout=15, data=post_data)
        # r.headers["content_type"] = "application/x-www-form-urlencoded"
        # r.headers["Cache-Control"] = "no-cache"

        # print("post request: ", r)

        return Response(data)


class ApiEndpointTest1_view(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        print("oath basic view, request:", request)
        print("and user: ", request.user)
        return HttpResponse("Hello, Oauth2!")


class ApiEndpointTest2_view(generics.ListAPIView):
    serializer_class = AllUsersSerializer
    queryset = User.objects.all()

    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        # return Response("data")


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse("Secret contents!", status=200)
