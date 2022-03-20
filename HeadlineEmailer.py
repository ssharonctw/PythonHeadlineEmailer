#handling http requests
import requests
#for webscraping
from bs4 import BeautifulSoup
#send the mail
import smtplib
#handling email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#for getting system date and time
import datetime

#getting the system time to include in email subject
now = datetime.datetime.now()

url = 'https://news.ycombinator.com/'

#email content placeholder
content = ''

#extracting News story, parse it into email body with index and title row by row
def extract_news(url= 'https://news.ycombinator.com/'):
    print('Extracing News Stories...')

    cnt=''#temporary text holder to update the content
    cnt+=('<b>Top Stories:</b>\n'+'<br>'+'-'*50+'<br>') #adding the header of email
    response = requests.get(url) #a response object with its code, 200 means successful
    webcontent = response.content #accessing the repsponse object's actual body/text
    soup = BeautifulSoup(webcontent, 'html.parser') #the content will then be converted to a parsetree and stores in soup
    #iterate all elements with class ="title" and valign =""
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})):
        #remark: there's a more at the page end that matches the above condition, hence we filter that out using below is-else
        if(tag.text!='More'):
            cnt += (str(i+1)+' :: '+ tag.text +"\n" +'<br>')#python is 0-indexed so we use i+1 in the email body
        else:
            cnt +=""
    return cnt

content += extract_news('https://news.ycombinator.com/')
content += '<br>------<br>'
content += '<br><br>End of Message'

fromInput = input("Enter sender gmail:")
pwInput = input("Enter sender gmail password:")
toInput = input("Enter receiver gmail:")

#below is the configuration to send emails (https://kinsta.com/blog/gmail-smtp-server/)
SERVER = 'smtp.gmail.com' #smtp server
PORT = 587 #port number for gmail

FROM = fromInput #the from email id
TO = toInput #the to email ids
PASS = pwInput # email id's password

print('Preparing email object...')
#create a msg body using MIMEMultipart Object
msg = MIMEMultipart()

#to avoid having same email subject everytime, we make the subject dynamic with current dd-mm-yyyy
msg['Subject'] = '[Automated Email] Top News Stories '+str(now.day)+"-"+str(now.month)+'-'+str(now.year)
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')
server = smtplib.SMTP(SERVER, PORT) #initializing the server
server.set_debuglevel(0) #if server have error, we want to see error msg
server.ehlo() #initializing connection
server.starttls() #establish secure connection
server.login(FROM, PASS) #login to sender account
server.sendmail(FROM, TO, msg.as_string()) #send the email

print('Email Sent...')

server.quit()
