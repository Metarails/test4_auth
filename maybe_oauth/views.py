import base64
import hashlib
import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
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
        code_verifier = "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(random.randint(43, 128))
        )
        code_verifier = base64.urlsafe_b64encode(code_verifier.encode("utf-8"))

        code_challenge = hashlib.sha256(code_verifier).digest()
        code_challenge = (
            base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
        )

        data = {
            "code_verifier": code_verifier,
            "code_challenge": code_challenge,
            "response_type": "code",
            "code_challenge_method": "S256",
            "client_id": settings.CLIENT_ID,
            "redirect_uri": "http://127.0.0.1:8000/noexist/callback",
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
        data = {"request": request.data, "args": args, "kwargs": kwargs}
        return Response(data)
