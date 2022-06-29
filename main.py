import os
import schedule
import requests
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


api_url = ''
bt = os.environ.get('BEARER_TOKEN')
access_token = {'Authorization': f'Bearer {bt}'}
base64 = os.environ.get('IMAGE_BASE64')
payload = {'image': f'{base64}'}
api_response = requests.post(api_url, headers=access_token, json=payload)
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email('')
to_email = To('')
tp = 'text/plain'


def check_api_response():
    if api_response.status_code == 200:
        print(api_response.json())
    elif api_response.status_code == 401:
        subject = 'HTTP code 401'
        content = Content(tp, 'Could not authenticate. Check your token.')
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        sg.client.mail.send.post(request_body=mail_json)
    elif api_response.status_code == 500:
        subject = 'HTTP code 500'
        content = Content(tp, 'Internal server error')
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        sg.client.mail.send.post(request_body=mail_json)
    elif api_response.status_code == 502:
        subject = 'HTTP code 502'
        content = Content(tp, 'Bad gateway')
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        sg.client.mail.send.post(request_body=mail_json)
    elif api_response.status_code == 522:
        subject = 'HTTP code 522'
        content = Content(tp, 'Connection timed out')
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        sg.client.mail.send.post(request_body=mail_json)


schedule.every(30).minutes.do(check_api_response)


while True:
    schedule.run_pending()
