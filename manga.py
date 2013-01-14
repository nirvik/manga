!/usr/bin/python

from BeautifulSoup import BeautifulSoup as bs
import urllib
import re
import sys
import os
import smtplib
import getpass
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
def main():

	comic=sys.argv[1]
	
	direc=raw_input('enter directory:')
	if not os.path.exists(direc):
		os.makedirs(direc)
	else:
		print 'path exists'
		sys.exit(0)
	#manga=urllib.urlopen('http://www.mangareader.net')
	#if ' ' in comic:
	#	comic=comic.replace(' ','-')
	a=int(raw_input('enter starting chapter:'))
	b=int(raw_input('destination chapter:'))
	for i in range(a,b):
		manga='http://www.mangareader.net/%s/%d'%(comic,i)
		manga=urllib.urlopen(manga)
		manga_read=manga.read()
		soup=bs(manga_read)
		imgfiles=soup.find('div',attrs={'id':'imgholder'})
		x=imgfiles.prettify()
		url=re.search(r'(?<=src=)(\S+)',x)
		imgurl=url.group()
		img=imgurl.replace('"','')
		localname='img%d'%i
		print 'Retrieving...%s'%img
		urllib.urlretrieve(img,os.path.join(direc,localname))
	ids=[]
	usr=raw_input('\nenter you gmail id:')
	sendingid=raw_input('\n sending email id:')
	ids.append(sendingid)
	passwd=getpass.getpass()
	data=smtplib.SMTP('smtp.gmail.com')
	tls=data.starttls()
	print 'TLS status:',tls[1]
	try:
		auth=data.login(usr,passwd)
	except smtplib.SMTPAuthenticationError:
		print 'incorrect username/password'
		sys.exit(1)
	print 'Aunthenticated!'
	msg=MIMEMultipart()
	sub=raw_input('\n enter subject:')
	msg['Subject']=sub
	msg['From']=usr
	msg['To']=sendingid
	directory='/home/nirvik/delta/projects/%s'%direc
	jpeg=os.listdir('/home/nirvik/delta/projects/%s'%direc)
	for files in jpeg:
		x=os.path.join(directory,files)
		fp=open(x,'rb')
		img=MIMEImage(fp.read())
		fp.close()
		msg.attach(img)
	a=data.sendmail(usr,ids,msg.as_string())
	if a=={}:
		print 'Message sent'
	else:
		print 'not sent'
	print 'LOGGING OUT.....'
	data.quit()

		
		
if __name__=='__main__':
	main()
