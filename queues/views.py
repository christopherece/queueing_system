from multiprocessing import Process, Queue as MultiProcessQueue
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Max, Q
import requests
from queues.models import Queue
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa


from django.template.loader import render_to_string
import datetime

from queues.models import Queue




# Create your views here.

@login_required(login_url='login')
def generate_pdf(request):

    startDate = request.GET['startDate']
    start = datetime.datetime.strptime(startDate, "%Y-%m-%d") 
    endDate = request.GET['endDate']
    end = datetime.datetime.strptime(endDate, "%Y-%m-%d") + datetime.timedelta(days=1)


   
    user = request.user.username
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d')
    reports = Queue.objects.filter(created__range=[start, end])
    context = {
        'reports':reports,
        'user':user,
        'current_datetime':current_datetime,
        'startDate':startDate
        
    }
    html = render_to_string('accounts/report.html', context)
    write_to_file = open('media/test_1.pdf', "w+b")
    result = pisa.CreatePDF(html,dest=write_to_file)
    write_to_file.close()
    return HttpResponse(html)

@login_required(login_url='login')
def updateticket(request, id):
    myqueue = Queue.objects.get(id=id)
    usersList = User.objects.all()
    hardwareCount = Queue.objects.filter(type__contains='hardware').count()
    softwareCount = Queue.objects.filter(type__contains='software').count()
    phoneCount = Queue.objects.filter(type__contains='phone').count()
    accountCount = Queue.objects.filter(type__contains='other').count()

    context = {
        'myqueue':myqueue,
        'usersList':usersList,
        'hardwareCount':hardwareCount,
        'softwareCount':softwareCount,
        'phoneCount':phoneCount,
        'accountCount':accountCount,

    }
    return render(request, 'dashboard/updateticket.html', context)

@login_required(login_url='login')
def updatequeue(request, id):
    obj = Queue.objects.get(id = id)
    if request.method == 'POST':
            status = request.POST['status']
            comment = request.POST['comment']
            technician = request.POST['technician']

    obj.status = status
    obj.technician = technician
    obj.comment = comment
    obj.save()
    return redirect('dashboard')

def addqueue(request):
    return render(request, 'dashboard/queue.html')

def submitqueue(request):
    
    queueIdMax = 0

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        type = request.POST['type']
        status = request.POST['status']
        technician = request.POST['technician']


        if Queue.objects.exists():
            queueList = Queue.objects.filter(status='Active').count()
            queueIdMax = Queue.objects.aggregate(Max('queue_id'))['queue_id__max']
            print(queueIdMax)
            addOne = queueIdMax + 1
        else:
            addOne = 1

    
    #api_request_process = Process(target=make_api_request, args=(name,description))
    #incNumber = make_api_request(name, description)

    myqueue = Queue(
        name = name,
        description = description,
        type = type,
        status = status,
        #ritm = incNumber,
        queue_id = addOne,
        technician = technician,
    )

    myqueue.save()

    messages.success(request, addOne)
    return redirect('addqueue')


def make_api_request(name,description):
    # Set the request parameters for the API request
    url = 'https://dev185867.service-now.com/api/now/table/incident'
    #user = 'svc_access_AutomationDev'
    #pwd = 'mcg10?4w:wEzC>l>-93T;M6d=sb(rg$OPNpV7FIN'

    user = 'admin'
    pwd = 'Nokia5130-c'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    #Prepare data for the API request
    data = {
        'caller_id': name,
        'short_description': description,

    }

    # Make the API request
    response = requests.post(url, auth=(user, pwd), headers=headers, json=data)
    response_data = response.json()
    result_data = response_data.get('result', {})
    api_response_number = result_data.get('number')
    
    #print(api_response_number)
    return api_response_number

    