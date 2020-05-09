from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        response="<h2>Welcome to the Hypercar Service!</h2>"
        return HttpResponse(response)


def menuView(request):
    return render(request,"tickets/menu.html")
