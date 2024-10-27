from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests
import json

# We are generating an access_token to be used whenever we want to make a request to FCM
def generate_firebase_auth_key():
    scopes = ['https://www.googleapis.com/auth/firebase.messaging']
    
    
    # Replace the value of credentials_info with what you downloaded from Firebase cloud messaging
    credentials_info = {
        "type": "service_account",
        "project_id": "ofaq-app",
        "private_key_id": "759da86434e64e0dec0fbc159ad224f8ba94638c",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCnyuH1kmHStcxe\nHFxw3JHP0lcVB+Dnh+bkwIH+yPj0n9phf+Wfhrx6lgh+rhl/AcB/dn4k8xQEaYXf\n2UGWrN7Pl6da9Vi9PwtjAdNPr6WWcwqhqSNKh4nouQPmqDoPe27y+RPlXRevkiGD\n92pqyAvxzE4MSRp+Uhx7/q/WfCjKQ1ylTRpY94PIkgH2owsKNs4VkEYCpwpxSBgB\nfBVPunVqNeS/4/pP/mbn5Ng+LW7yNStjH/HKitNgXpPObKPfESU1BakhvItgncoO\nFp2WQx4OWTqBwCo9WH+gQ0SpPD26qyygt5mh0i95Zzfc2xuDJZXQzESM3raQsBYR\nN7J29qUzAgMBAAECggEAHcIOlwXyEXOqnho7jsyfk5MDXLh7+7QPkAxQQcaU2JWt\nHlOXftZfgQIw2X65CNxfrntuXdE6gJnSY2PdjQJ1ta14wdn3dgDDXTjKqDxHiso2\nXXtoxeQJ4ltFxNebDHngsHjaPXhoJfwts4Div7Ng4u5P/T/N0g9v+9Gsj8aPWWeV\nc8y759YBYY65nLiYAdQA4rBOSoLywWbWvZmcM9fYwOBXbnyT/uwNid4CfMoVJEux\nYGYFOGuWHRX5O4u+K0JOdB7ZvRBU+HI3hvC7FUYr9dYAeKeQSDRKZZPnmkLSo9+i\nXOtlfa6iSvU9xJ++9pnVmFOmIG0uZ5jUeQIzgFDC8QKBgQDTqgfZakyuiAqvMXDc\nMIqHuUx9/h9sJbegivivD3sUYlspwsBcPhU5vou47vAFLay1Mb+1uNnNNSKA2qIX\nUSo9oxlXyaaC2or3SuqZAfZH0SHO7qOjDAyyBR9MjCLK+PxnwdL4tJIT3rEWa6tf\n3ELQw3JlOgnHgvv/89VB4xGgaQKBgQDK8FeE48ntjjtEKF8TmH/3XMoGo77OzycB\no9VnaIffhy44toacTAMzPgSPM9PvfzkcnS5VbrsIqjsIJgJpVfgiem/88e5jExjs\nxVMiYSE4vG93wyA1LOwn9Oix9Z7m1ikBE1zVaUtMF0v5iQdNvPAGTz7QuBjoVzf+\njSBDuQulOwKBgAiqTlX1RxxiD2XqtT8ecZ1q1ZnW3Hx18tWMuu+Xx6cm+6pzAaMF\nG6NYjKnOhl7/5rEoTzvmTGxdP4Nc8APaW8tYMQJqC/oRblz/YSlQbj+0bRjmpiZX\nqPFkyko89nOuy86HndZ2tgBAPqm3ULXE86tORRGl1Z6oWx64YcOnwyH5AoGBAJ80\nyhQw9/trt8cSvPQMkWen3b4zu79W+EzrEMIdWWrdDD/lwdjgMSqEHuORT1T2RAHU\ntcLEKer0UXdlCkNE9HNoBm80BUaodsdZTo0MEhoGipQz+hJ9eY8nLV5fSRfjLyvu\n2sd54V6CcFIFVDuCW/M3PBpWMwQjWIRUhtlaVG59AoGAOm6u2XHVuP9jns7x+OKM\nujptGRByKd11VZ1xZmGzZoVPnieSUeZx6+TG4pm/9PImmAb7ycr6tAmFZjZyvWmL\nJJbde0J37yGPjpPWTbh78TXzR87GFV3kvXy2juxxZcDizS9fFJbC55fZ1911Wq10\nx9vwzl95NiXv+uevUvCJEuw=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-vnt7v@ofaq-app.iam.gserviceaccount.com",
        "client_id": "116065377226956876129",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vnt7v%40ofaq-app.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    credentials = service_account.Credentials.from_service_account_info(
            credentials_info, scopes=scopes
    )

    credentials.refresh(Request())

    access_token = credentials.token
    return access_token

def send_push_notification(fcm_token, notification):
    url = "https://fcm.googleapis.com/v1/projects/ofaq-app/messages:send"
    auth_token = generate_firebase_auth_key()
    notification['id'] = str(notification['id'])
    if 'users' in notification:
        notification['users'] = [str(uid) for uid in notification['users']]
    payload = json.dumps({
        "message": {
            "token": f'{fcm_token}',
            "notification": {
            "title": notification['title'],
            "body": notification['message'],
            },
            "data": {
                "message": notification["message"],
                "title": notification["title"],
                "created_at": notification["created_at"],
            }
        }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {auth_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)