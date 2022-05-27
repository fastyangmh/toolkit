#import
import win32com.client

if __name__ == '__main__':
    #parameters
    recipient = 'xxxxxxxx'
    subject = 'xxxxxxxx'
    body = 'xxxxxxxx'
    attachments = 'xxxxxxxx'

    #create outlook object
    outlook = win32com.client.Dispatch('outlook.application')

    #create mail
    mail = outlook.CreateItem(0)

    #write mail
    mail.To = recipient
    mail.Subject = subject
    mail.Body = body
    mail.Attachments.Add(attachments)

    #send mail
    mail.Send()
