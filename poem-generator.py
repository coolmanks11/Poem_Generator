import json
import urllib3
import boto3
def lambda_handler(event, context):
    
    # Log full event to CloudWatch logs for testing
    print('EVENT:\n%s\n\n' % event)

    # Select based on intent name
    # (could use dictionary function lookup instead)
    intent_name = get_intent_name(event)
    print(intent_name,'--------- intent_name')
    if 'GeneratePoemIntent' == intent_name:
        response = generate_poem(event)
    else:
        response = fallback(event)

    # Print response to CloudWatch logs
    print('RESPONSE:\n%s\n\n' % response)
    
    return response
def generate_poem(event): 
    intent_name = get_intent_name(event)
    # Get the API key from Secrets Manager
    sm = boto3.client("secretsmanager", region_name="eu-west-1")
    secret = sm.get_secret_value(SecretId="APIKeySecret")
    secret_value = json.loads(secret["SecretString"])
    chat_api_key = secret_value["api_key"]
    print(chat_api_key)
    theme = slot_value(event, "Theme")
    lines = slot_value(event, "Lines")
    keyword = slot_value(event, "Keyword")
    chatMsgRequest = "Provide me a poem about " + theme + " with " + lines + " lines and the keyword " + keyword
    response =  requestChatGPT(chatMsgRequest, chat_api_key)
    json_response = json.loads(response.data)
    res_message = json_response['choices'][0]['message']['content']
    print(f"Response body: {response.data}")

    message_content = 'Poem created. Your Poem : '+ res_message
    return fulfilled_response(intent_name, message_content)
    
def requestChatGPT(chatMsgRequest, chat_api_key):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {chat_api_key}'
    }
    
    data = {
        "model": "gpt-3.5-turbo",
         "messages": [{"role": "user", "content": chatMsgRequest}],
         "temperature": 0.7
    }
    
    # Create a connection pool
    http = urllib3.PoolManager()
    
    # Send a POST request
    response = http.request(
        'POST',
        url,
        body=json.dumps(data).encode('utf-8'),
        headers=headers
    )
    return response

def slot_value(event, slot_name):
    return event['sessionState']['intent']['slots'][slot_name]['value']['interpretedValue']
def fallback(event):
    intent_name = get_intent_name(event)
    message_content = 'No idea what you want to do so did nothing!'
    return fulfilled_response(intent_name, message_content)
def get_intent_name(event):
    return event['sessionState']['intent']['name']
    
def fulfilled_response(intent_name, message_content):
    response = {
        'sessionState': {
            'dialogAction': {
                'type': 'Close' # finishes the convo
            },
            "intent": {
                "name": intent_name,
                "state": "Fulfilled" # must be fulfilled or failed
            }
        },
        "messages": [ # optional, Lex will use configured responses if not
            {
                "contentType": "PlainText",
                "content": message_content
            }
        ]
    }    
    return response