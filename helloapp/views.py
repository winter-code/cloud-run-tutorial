from django.shortcuts import render
import base64
import os
import requests
from django.views.decorators.http import require_http_methods
from concurrent import futures
from google.cloud import pubsub_v1
import argparse
from typing import Callable


@require_http_methods(["GET", "POST"])
def homepage(request):
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')
    
    return render(request, 'homepage.html', context={
        "message": "It's running!",
        "Service": service,
        "Revision": revision,
    })

@require_http_methods(["GET", "POST"])
def aboutpage(request):
    return render(request, 'aboutpage.html', context={"message": "It's running!","pub_sub": ""})

import json
@require_http_methods(["POST"])
def recieve_pubsub_message(request):

    envelope = json.loads(request.body)
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

    print(f"Hello {name}!")
    print(f"Hello {name}!")
    print(f"Subscription recieved the message successfully. \nTriggered the service at endpoint /pub-sub (Which is why the message is logged above!) \nMessage format -- {envelope}")

    return render(request, 'aboutpage.html', context={"message": "It's running!","pub_sub": name})

@require_http_methods(["GET"])
def send_message(request):

    """Publishes multiple messages to a Pub/Sub topic with an error handler."""

    # TODO(developer)
    project_id = "arpanas-project"
    topic_id = "tp-sarva-demo"

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    msg = request.GET.get('msg')
    if msg is not None:
        msg = f"{msg} is live and working fine!"
    else:
        msg = "No message received"
    msg = msg.encode("utf-8")
    future = publisher.publish(topic_path, msg)
    print(future.result())
    print(f"Published message to {topic_path} - Message will be logged.")
    return render(request, 'aboutpage.html', context={"message": "It's running!","pub_sub": msg})
