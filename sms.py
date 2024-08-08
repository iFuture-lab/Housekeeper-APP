from TaqnyatSms import client


bearer = ''

body = 'message Content'
recipients = ['0549998696']
sender = 'OFAQ'
scheduled='2024-08-07T15:25'



taqnyt = client(bearer)
message = taqnyt.sendMsg(body, recipients, sender,scheduled)

print (message)