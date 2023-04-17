from scapy.all import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def capture_packet():
    channel_layer = get_channel_layer()
    packets = sniff(filter="ip", count=10) # capture 10 packets with ip layer
    for packet in packets:
        # Convert packet to JSON format
        json_packet = json.dumps(packet.summary())
        # Send packet to websocket consumer
        async_to_sync(channel_layer.group_send)("rfid", {"type": "rfid.start", "data": {"packet": json_packet}})
