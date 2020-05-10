from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render

from collections import deque,defaultdict
from datetime import datetime,timedelta

class TicketQueue:
    queue=defaultdict(deque)
    index=0
    time={"change_oil":2 , "inflate_tires":5,"diagnostic":30}



    def updateQueue(self,operation):
        current_time=datetime.now()
        queue=self.queue[operation]
        delta=timedelta(minutes=self.time[operation])
        if len(queue)>0:
            while current_time - queue[0] > delta :
                queue.popleft()

    def update(self):
        for operation in self.time.keys():
            self.updateQueue(operation)



    def get_waiting(self,operation):
        waiting = lambda operation : len(self.queue[operation]) * self.time[operation]

        if operation=="change_oil":
            return waiting(operation)
        elif operation=="inflate_tires":
            return waiting("change_oil")  + waiting(operation)
        else:
            return waiting("change_oil") + waiting("inflate_tires")  + waiting(operation)

    def add(self,operation):
        self.update()
        self.index+=1
        time_wait=self.get_waiting(operation)
        self.queue[operation].append(datetime.now())
        return (time_wait,self.index)






class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        response="<h2>Welcome to the Hypercar Service!</h2>"
        return HttpResponse(response)


def menuView(request):
    return render(request,"tickets/menu.html")


class TicketView(View):
    ticketqueue=TicketQueue()
    def get(self,request,*args,**kwargs):
        time,index = self.ticketqueue.add(kwargs["operation"])

        return render(request,"tickets/tickets.html",context={"index":index,"time":time})


