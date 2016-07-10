from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import re
import random

jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                    """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
         }

# Create your views here.
class OnBoardingBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2318934571':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    print(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])   
        return HttpResponse()

def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    start_text = ''
    for token in tokens:
        if token in jokes:
            start_text = random.choice(jokes[token])
            break
    if not start_text:
        start_text = "Hey, congrats on getting the job! Im Sarah and I can help you get settled into your new role! We can get started right now with the HR procedure or you can see other options:"
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAHePhy0EvMBAKdbSfQnZAG5QuZBrAZCZA0lGZBVmJrWtg2yxxoQNfvHZAAZAidNdIi2FEJjfiLeO3TZAZC8pvVKykhDwDHP14zQ1cW384kKGR3578fzn8Firby89ZBit6ITmZBOwu0VSjWpZBzDfZBItJ4P4fsUy6PCuybrNHoXcymzHbgZDZD' 
    response_msg = json.dumps({
        "recipient":{"id":fbid},
        "message": {
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"button",
                "text":start_text,
                "buttons":[
                  {
                    "type":"postback",
                    "title":"Get Started",
                    "payload":";klf;kkkl;"
                  },
                  {
                    "type":"postback",
                    "title":"Options",
                    "payload":"USER_DEFINED_PAYLOAD"
                  }
                ]
              }
            } 
          }
        })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(status.json())