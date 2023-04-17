from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe
import json
##import channels
from asgiref.sync import async_to_sync
from app.models import Status, Alert
from django.core.paginator import Paginator
from channels import layers

from django.shortcuts import render
from django.http import HttpResponse
#from . import start_capture, stop_capture
from app.forms import RFIDForm
from app.models import RFID
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from scapy.all import *

def index(request):
    return render(request, 'index.html')

def capture_packet():
    channel_layer = get_channel_layer()
    packets = sniff(iface='80-91-33-F2-26-49',  count=25, timeout=15)
    for packet in packets:
        # Convert packet to JSON format
        json_packet = json.dumps(packet.summary())
        # Send packet to websocket consumer
        async_to_sync(channel_layer.group_send)("rfid", {"type": "rfid_start", "data": {"packet": json_packet}})

def start_capture_view(request):
    if request.method == 'POST':
        form = RFIDForm(request.POST)
        if form.is_valid():
            ip_address = form.cleaned_data['ip_address']
            RFID.objects.create(ip_address=ip_address)
            # Call packet capturing function
            capture_packet()
            return HttpResponse("Capture Started")
    else:
        form = RFIDForm()
    return render(request, 'start_capture.html', {'form': form})

def stop_capture_view(request):
    stop_capture()
    return HttpResponse("Capture Stopped")


def index(request):
    return render(
        request,
        "app/index.html",
        context={})


def log(request):
    if request.method == "POST":
        alert_list = Alert.objects.all()
        draw = request.POST.get('draw')
        # /*Jumlah baris yang akan ditampilkan pada setiap page*/
        length = request.POST.get('length')
        # /*Offset yang akan digunakan untuk memberitahu database
		# dari baris mana data yang harus ditampilkan untuk masing masing page
		# */
        start = request.POST.get('start')
        # /*Keyword yang diketikan oleh user pada field pencarian*/
        search = request.POST.get('search')
        paginator = Paginator(alert_list, length)
        alerts = paginator.get_page(draw)
        data = [[alert.created_at.strftime('%Y-%m-%d %H:%M:%S'),alert.ip_source,alert.ip_destination,alert.port,alert.agent,alert.datasource] for alert in alerts.object_list]
        output = {
            "draw": draw,
            "recordsTotal": alert_list.count(),
            "recordsFiltered": alert_list.count(),
            "data" : data
        }
        return JsonResponse(output)
    return render(
        request,
        "app/log.html",
        context={})



def service(request):
    # if Status.objects.all().count() == 0:
    #     status = False
    # else:
    #     status = Status.objects.all()[0].status
    _return = {"status": False}
    _return_status = 403

    if request.method == "POST":
        command = ""
        channel_layer = layers.get_channel_layer()
        if 'command_start' in request.POST:
            command = request.POST.get("command_start", "start")
            async_to_sync(channel_layer.send)('alert-generate', {
                'type': 'triggerWorker',
                'command': command
            })
            _return = {"status":True}
            _return_status = 200
        elif 'command_stop' in request.POST:
            command = request.POST.get("command_stop", "stop")
            async_to_sync(channel_layer.send)('alert-generate', {
                'type': 'triggerWorker',
                'command': command
            })
            _return = {"status":True}            
            _return_status = 200
    return JsonResponse(_return, status=_return_status)
