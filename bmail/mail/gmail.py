
import pickle
import os.path
from playsound import playsound
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from datetime import date
import dateutil.parser as parser
import base64
from bs4 import BeautifulSoup
from mail.voice import speak, get_audio
import re
from time import sleep
from gtts import gTTS
from email.mime.text import MIMEText
import email

SCOPES = ["https://mail.google.com/", "https://www.googleapis.com/auth/gmail.readonly","https://www.googleapis.com/auth/gmail.modify","https://www.googleapis.com/auth/gmail.send"]



#authenticates the gmail account based on credentials file
#creates token.pickle to store them
def authenticate_gmail():
	
	creds = None

	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'/Users/aditisharma/Desktop/test/credentials.json', SCOPES)
			creds = flow.run_local_server(port = 0)

		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('gmail', 'v1', credentials=creds)

	return service



#send message to trash
def trash(service, message_id):

		try:
			message = (service.users().messages().trash(userId='me', id=message_id).execute())
			print('Message Id: %s sent to Trash.' % message['id'])
			speak("Message sent to trash")
			return message
		except Exception as error:
			print('An error occurred while sending email: %s' % error)
			return None



#delete a mail using its mail id
def delete_message(service, message_id):
	try:
		service.users().messages().delete(userId='me', id=message_id).execute()
		print('Message with id: %s deleted' % message_id)
		speak("Message deleted permanently")
	except Exception as error:
		print('An error occurred: %s' % error)



#check for latest mails in inbox
#uses bs4 and regex to clean the mail body
#reads mail to the user
def check_mails(service):
	today = (date.today())

	today_main = today.strftime('%Y/%m/%d')
	print("Connection established on ", today_main)
	
	
	results = service.users().messages().list(userId = 'me',
											labelIds=["INBOX","UNREAD"],
											q="after:{} and category:Primary".format(today_main)).execute()
	
	
	try:
		mssg_list = results['messages']
		no_of_msg = results['resultSizeEstimate']
		# print(no_of_msg)
		speak("{} new emails found".format(len(mssg_list)))
		print(no_of_msg, " new messages found! ")
		print("List of new mails:: ")
	except:
		results['resultSizeEstimate'] = 0
		no_of_msg = results['resultSizeEstimate']
		mssg_list = []
		print('No messages found.')
		speak('No messages found.')
	final_list = [ ]

	for mssg in mssg_list:
		temp_dict = { }
		m_id = mssg['id'] # get id of individual message
		message = service.users().messages().get(userId="me", id=m_id).execute() # fetch the message using API
		payld = message['payload'] # get payload of the message 
		headr = payld['headers'] # get header of the payload


		for one in headr: # getting the Subject
			if one['name'] == 'Subject':
				msg_subject = one['value']
				temp_dict['Subject'] = msg_subject
			else:
				pass			

		for two in headr: # getting the date
			if two['name'] == 'Date':
				msg_date = two['value']
				date_parse = (parser.parse(msg_date))
				m_date = (date_parse.date())
				temp_dict['Date'] = str(m_date)
			else:
				pass

		for three in headr: # getting the Sender
			if three['name'] == 'From':
				msg_from = three['value']
				
				sender = str(msg_from).split("<")
				
				temp_dict['Sender'] = sender[0]

			else:
				pass

		temp_dict['Snippet'] = message['snippet'] # fetching message snippet
		
		mssg_b = ""
		# Fetching message body
		mssg_parts = payld.get('parts') # fetching the message parts
		try:
			part_one  = mssg_parts[0] # fetching first element of the part 
			part_body = part_one['body'] # fetching body of the message
			part_data = part_body['data'] # fetching data from the body
			clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
			clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
			clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
			soup = BeautifulSoup(clean_two , "lxml" )
			# print(type(soup.body))
			if soup.body is None:
				mssg_b = ""
				pass
			
			else:
				mssg_b = soup.body()
		except:
			pass
	
		mssg_body = "".join(line.strip() for line in str(mssg_b).split("\n"))
		CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
		msg_text = re.sub(CLEANR, '', mssg_body)
		temp_dict['Message_body'] = msg_text
		
		final_list.append(temp_dict) 
		service.users().messages().modify(userId="me", id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute() 
	
	#reading the latest mails
	for i in range(int(no_of_msg)):
		
		print("\nSender:", final_list[i]['Sender'])
		print("Subject:", final_list[i]['Subject'])
		speak("Sender:")
		my_obj = gTTS(text = final_list[i]['Sender'], lang = 'en', slow = "False", tld="com")
		my_obj.save("sender.mp3")
		playsound("sender.mp3")
		if os.path.exists("sender.mp3"):
			os.remove("sender.mp3")
		else:
			print("The file does not exist")
	
		speak("Subject:")		
		my_obj = gTTS(text = final_list[i]['Subject'], lang = 'en', slow = "False")
		my_obj.save("subject.mp3")
		playsound("subject.mp3")
		
		if os.path.exists("subject.mp3"):
			os.remove("subject.mp3")
		else:
			print("The file does not exist")
		
			  
		speak("If you want to listen to this mail, say read. To ignore the mail, say leave")
		sleep(1)
		reply = get_audio()

		if 'read' in reply.lower() or 'red' in reply.lower() :
			if (len(final_list[i]['Message_body']) == 0) and (len(final_list[i]['Snippet']) != 0):
				speak("Message Body")
				my_obj = gTTS(text = final_list[i]['Snippet'], lang = 'en', slow = "False", tld="com")
				my_obj.save("snippet.mp3")
				playsound("snippet.mp3")
				if os.path.exists("snippet.mp3"):
					os.remove("snippet.mp3")
				else:
					print("The file does not exist")
				
				
			else:
				speak("Message Body")
				my_obj = gTTS(text = final_list[i]['Message_body'], lang = 'en', slow = "False", tld="com")
				my_obj.save("Message_body.mp3")
				playsound("Message_body.mp3")
				if os.path.exists("Message_body.mp3"):
					os.remove("Message_body.mp3")
				else:
					print("The file does not exist")
				# speak(final_list[i]['Message_body'])
			
			speak("Message body ended. If you want to send it to trash, say 'trash'.")
			q = get_audio()
			if 'rash' in q.lower():
				trash(service, mssg_list[i]['id'])

		else:
			speak("Mail Skipped")

	if len(mssg_list)>0:
		speak("No more mails found!")
	return final_list



#creates an email and encodes it
def create_message(sender, to, subject, message_text):	
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
	b64_string = b64_bytes.decode('utf-8')
	return {'raw': b64_string}



#send emails from user's account
def send_message(service, user_id, message):
		
	try:
		message = service.users().messages().send(userId=user_id, body=message).execute()
		print('Message Id: %s' % message['id'])
		speak("Message sent successfully")
		return message
	except Exception as e:
		print('An error occurred: %s' % e)
		return None



#helper function to compose and send emails
def send_final_message(service):
	
	speak("Creating a New Email")
	sleep(1)
	sender = "aditisharma100201@gmail.com"
	to = ""
	subject = ""
	message_text = ""
	speak("Enter receiver's email i d")
	sleep(2)
	to1 = get_audio()
	to = "".join(to1.split())
	to = to+'@gmail.com'
	print("to: ", to)
	speak("Enter subject")
	subject = get_audio()
	speak("Enter message text")
	message_text = get_audio()

	message1 =create_message(sender, to.lower(), subject, message_text)
	result = send_message(service, "me", message1)
	return result



#search for a string/user in gmail
#returns a list of message ids with similar substrings
def search_message(service, user_id, search_string):
   
	try:
		list_ids = []

		# get the id of all messages that are in the search string
		search_ids = service.users().messages().list(userId=user_id, q=search_string).execute()
	   
		try:
			ids = search_ids['messages']

		except KeyError:
			print("WARNING: the search queried returned 0 results")
			print("returning an empty string")
			speak("No such messages found.")

		if len(ids)>1:
			for msg_id in ids:
				list_ids.append(msg_id['id'])
			

		else:
			list_ids.append(ids['id'])
			

		# count = len(list_ids)
		# speak("Number of messages found are ")
		# speak(count)
		return list_ids
		
	except:
		print("No mail found")
		speak("No mail found")




#search for a message id in inbox
#cleans the message body and returns it
def get_message(service, user_id, msg_id):
	"""
	Search the inbox for specific message by ID and return it back as a 
	clean string. 
	"""
	try:
		# the message instance
		message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()

		
		msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

		
		mime_msg = email.message_from_bytes(msg_str)

		
		#for multipart content
		content_type = mime_msg.get_content_maintype()
		if content_type == 'multipart':
			
			parts = mime_msg.get_payload()

			
			final_content = parts[0].get_payload()
			final_content = re.sub('<[^>]+>', '', final_content)
			final_content = " ".join(final_content.split())
			print(final_content, "final")
			my_obj = gTTS(text = final_content, lang = 'en', slow = "False", tld="com")
			my_obj.save("sub.mp3")
			playsound("sub.mp3")
			
			if os.path.exists("sub.mp3"):
				os.remove("sub.mp3")
			else:
				print("The file does not exist")
			# speak(final_content)
			

		#for mails having text as content
		elif content_type == 'text':
			my_obj = gTTS(text = mime_msg.get_payload(), lang = 'en', slow = "False", tld="com")
			my_obj.save("sound.mp3")
			playsound("sound.mp3")
			print(mime_msg.get_payload(), "mime")
			if os.path.exists("sound.mp3"):
				os.remove("sound.mp3")
			else:
				print("The file does not exist")
			

		else:
			speak("An unexpected error has occured")
			print("\nMessage is not text or multipart, returned an empty string")
   
   #error handling
	except Exception:
		print("An error occured: ")



#helper function to search a message
def search(service):
	speak("What is the message you want to search?")
	msg = get_audio()
	list_ids = search_message(service, "me", msg)
	
	# print(list_ids)
	speak("Body of the first message is")
	get_message(service, "me", list_ids[0])
	speak("Message ended!")
	return None



def create_draft(service, user_id):
	speak("Creating Draft")
	sleep(1)
	sender = "aditisharma100201@gmail.com"
	to = ""
	subject = ""
	message_text = ""
	speak("Enter receiver's email i d")
	sleep(2)
	to1 = get_audio()
	to = "".join(to1.split())
	to = to+'@gmail.com'
	print("to: ", to)
	speak("Enter subject")
	subject = get_audio()
	speak("Enter message text")
	message_text = get_audio()

	message1 =create_message(sender, to.lower(), subject, message_text)
	
	try:
		message = {'message': message1}
		draft = service.users().drafts().create(userId=user_id, body=message).execute()

		speak("draft created and saved, draft id is")
		speak(draft[id])
	
	except Exception:
		print("Exception")
	




