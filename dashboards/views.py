from django.shortcuts import render
from .models import Dashboard
from queues.models import Queue
from django.db.models import Max, Min


# Create your views here.
def index(request):
    obj = Dashboard.objects.latest('created_at')
    context = {
        'obj' : obj
    }
    return render(request, 'dashboard/index.html', context)

def monitor(request):
    queueLists = Queue.objects.all()
    queue_id = queueLists.aggregate(Min('queue_id'))['queue_id__min']
    context = {
        'queueLists': queueLists,
        'queue_id': queue_id,
    }
    return render(request, 'dashboard/monitor.html', context)
