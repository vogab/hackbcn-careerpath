import os
import requests
import base64
from openai import OpenAI
from .models import Request
from careerpath.settings import API_KEY,PROMPTS_DIR
from .models import Request

possible_tones = [
    (1, 'Formal'),
    (2, 'Casual'),
    (3, 'Playful')
]

client = OpenAI(
    # This is the default and can be omitted
    api_key=API_KEY,
)

def process_request(request_id):
    try:
        request = Request.objects.get(id=request_id)
        
        # Simulate a long-running process or API call
        # Replace this with actual processing logic
        tone = possible_tones[request.tone - 1][1]
        prompt = request.prompt.prompt.replace('[TONE]', tone).replace('[SKILLS]', request.skills).replace('[INTERESTS]', request.interests)
        response_data = some_async_function(encode_image(request.image.path), prompt)
        
        # Update the request with the response data
        request.response = response_data
        request.save()
    except Request.DoesNotExist:
        pass


def some_async_function(base64_image, promp):
    # Simulate an external API call
    print("Calling API")
    return send_image_to_api(base64_image, promp, API_KEY)



def send_image_to_api(base64_image, promp, api_key):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"{promp}"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 500,
    "temperature": 1,
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()["choices"][0]["message"]["content"]


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
