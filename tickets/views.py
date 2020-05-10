from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render,redirect

from collections import deque,defaultdict
from datetime import datetime,timedelta

class TicketQueue:
    queue=defaultdict(deque)
    index=0
    time={"change_oil":2 , "inflate_tires":5,"diagnostic":30}


    def get_waiting(self,operation):
        waiting = lambda operation : len(self.queue[operation]) * self.time[operation]

        if operation=="change_oil":
            return waiting(operation)
        elif operation=="inflate_tires":
            return waiting("change_oil")  + waiting(operation)
        else:
            return waiting("change_oil") + waiting("inflate_tires")  + waiting(operation)

    def add(self,operation):

        self.index+=1
        time_wait=self.get_waiting(operation)
        self.queue[operation].append(self.index)

        return (time_wait,self.index)

    @classmethod
    def size(cls):
        return sum([ len(q) for q in cls.queue.values()])

    @classmethod
    def next(cls):
        if cls.size() <  1:
            return 0
        if cls.queue["change_oil"]:
            return cls.queue["change_oil"].popleft()
        elif cls.queue["inflate_tires"]:
            return cls.queue["inflate_tires"].popleft()
        else:
            return cls.queue["diagnostic"].popleft()

    @classmethod
    def get_count(cls):
        return { key : len(cls.queue[key]) for key in cls.time.keys()}





class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        response="<h2>Welcome to the Hypercar Service!</h2>"
        return HttpResponse(response)


def menuView(request):
    return render(request,"tickets/menu.html" )


def nextView(request,index):
    size=TicketQueue.size()
    return render(request,"tickets/next.html",context={"size": size,"index":index})

class TicketView(View):
    ticketqueue=TicketQueue()
    def get(self,request,*args,**kwargs):
        time,index = self.ticketqueue.add(kwargs["operation"])

        return render(request,"tickets/tickets.html",context={"queue":TicketQueue.queue,"index":index,"time":time})

class ProcessingView(View):

    def get(self,request,*args,**kwargs):
        return render(request,"tickets/processing.html",context=TicketQueue.get_count())

    def post(self,request,*args,**kwargs):
        return redirect("/next",index = TicketQueue.next())
