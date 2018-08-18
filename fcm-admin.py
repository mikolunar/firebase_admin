import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import auth
import datetime
import requests
import json




def initializeFireBaseSDK(certificate):
    
    
    cred=credentials.Certificate(certificate)
    default_app=firebase_admin.initialize_app(cred)
    return default_app

def getAccessToken(certificate):
    cred=credentials.Certificate(certificate)
    return cred.get_access_token()

def sendPushToDevice(device_token):
    if device_token:
        message = messaging.Message(
                android=messaging.AndroidConfig(
                    ttl=datetime.timedelta(seconds=3600),
                    priority='normal',
                    notification=messaging.AndroidNotification(
                        title='Tuatara TEST Push Notification - FMS API v1.0',
                        body='Push Notification to device Token: '+device_token,
                        icon='stock_ticker_update',
                        color='#f45342'
                    ),
                ),
                token=device_token,
            )
        return messaging.send(message)

def sendPushToTopic(topic):
    if topic:
        message = messaging.Message(
                android=messaging.AndroidConfig(
                    ttl=datetime.timedelta(seconds=3600),
                    priority='normal',
                    notification=messaging.AndroidNotification(
                        title='Mint TEST using new FMS API v1.0',
                        body='Notification from Backend',
                        icon='stock_ticker_update',
                        color='#f45342'
                    ),
                ),
                topic=topic,
            )
        return messaging.send(message)
    else:
        return 'ERROR sending notification: Empty topic'
        

def callAPI(url_string):
    response=''
    data=''
    response = requests.get(url_string)
    return response.json()

def subscribeDevices(topic):
    return True

def unsubscribeDevices(topic):
    return True

def checkRegisteredDevices():
    return 0

def listRegisteredDevices():
    #writes the registered devices to csv file
    #returns number of registered devices
    return 0

def getDeviceByMSISDN(MSIDN):
    reg_token=''
    return reg_token


# Helper functions


# ---------------------------------------------------------------------


print("Tuatara - Mint Push Notification Admin")

mfp8_server_url='https://ttr-mint-por01d.tuatara.pl/mfpadmin/management-apis/2.0/runtimes/mfp/'
print('Using MF server :', mfp8_server_url)
#default_certificate=input('User default certificate location (current directory) [Y/n]: ')
default_certificate='Y'

if default_certificate=='Y':
    user_certificate='d:\\django\\firebase_samples\\mint-da46f-firebase-adminsdk-mca5p-e8665eddfe.json'
elif default_certificate=='N':
    user_certificate=input('Provide absolut path to json certificate location: ')

# Initializing SDK
if user_certificate:
    print('Initializaing FireBase Admin SDK. Using default certificate :'+user_certificate)
    print(initializeFireBaseSDK(user_certificate))
else:
    print('ERROR - Missing certifcate location')
    exit()

print("1 - get authorization token\n2 - check registered devices \n3 - subscribe device(s) to topic \n4 - unsubscribe device(s)\n5 - Firebase push notification to topic\n6 - Firebase push notification to device \n7 - registered devices \n8 - List installed Adapters ")
selection=input("Selec option:")
if selection=='1':
    print('OAuth2.0 TOKEN: ', getAccessToken(user_certificate))
elif selection =='2':
        print('2')
elif selection=='3':
    print('3')
elif selection=='4':
    print('4')
elif selection=='5':
    user_topic=input('Type topic string:')    
    message_id=sendPushToTopic(user_topic)
    print('Sent OK. Message ID:', message_id)
elif selection=='6':
    device_token="d9IUYwBGWvo:APA91bFlWyaBZqBGn1AMCReRo64rRs-VMdLCPwhQAFrceV6q5D-QxCzR117qUuVlnJNxF20CRYDYwp4H4Th1IRlzlx291TSPW621Y22EhM0CScHof-s-s-_-X_t8_7AZnQ5dbNqd3Uy_EM4ZDiD--TFYHJeO1ybksQ"
    print('Using hardcoded device token:',device_token)
    print('Validating token.. :')
    #decoded_token = auth.verify_id_token(device_token)
    #user_id = decoded_token['uid']
    #print("Token User ID:", user_id)
    print('OK')
    print('Sending message..')
    print('Result :',sendPushToDevice(device_token))
elif selection=='7':
    
    print('Checking default server..')
    response=requests.get(mfp8_server_url+'devices', auth=requests.auth.HTTPBasicAuth('mfadmin', 'mfadmin'))
    
    
    print('OK! Response status:',response.status_code)
    print('Response header:',response.headers)
    json_data=json.loads(response.text)
    print('Registered device:', json.dumps(json_data, indent=4, sort_keys=True))

    print('\n Number of registered devices: ', len(json_data['items']))
    for item in json_data['items']:
        print(' \n Application ID : '+ str(item['id']) + '\n')
elif selection=='8':
    print('Listing adapters for current server')
    response=requests.get(mfp8_server_url+'adapters', auth=requests.auth.HTTPBasicAuth('mfadmin', 'mfadmin'))
    print('OK! Response status:',response.status_code)
    print('Response header:',response.headers)
    json_data=json.loads(response.text)
    print('Adapters:', json.dumps(json_data, indent=4, sort_keys=True))

    

#user = auth.create_user(
#    email='marcin.roszczyk@tuatara.pl',
#    email_verified=False,
#    phone_number='+48537699001',
#    password='Passw0rd',
#    display_name='Marcinos',
#    photo_url='http://www.tuatara.pl',
#    disabled=False)

#print('User created: {0}'.format(user.uid))




# print('Response:'+sendPush(reg_token, topic))

#result=callAPI('https://reqres.in/api/users')
#print(result)


