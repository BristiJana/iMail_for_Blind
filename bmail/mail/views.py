from django.http import HttpResponse
from django.shortcuts import render
from .gmail import authenticate_gmail, check_mails, send_final_message, search
from .voice import speak, get_audio
import os.path
from playsound import playsound
from gtts import gTTS


#connecting the frontend
def front(request):
    context = { }
    return render(request, "index.html", context)
	


#main function
def Home(self):
	SERVICE2=authenticate_gmail()

	speak("Welcome to i Mail")
	print("Welcome to i Mail")
	menu = "To check your inbox, say 'inbox'. To send a new mail, say 'create a mail', and to search for a message, say 'search'."
	choice = 'yes'

	my_obj = gTTS(text = menu, lang = 'en', slow = "False", tld="com")
	my_obj.save("menu.mp3")
	playsound("menu.mp3")
	choice = get_audio()
	if os.path.exists("menu.mp3"):
		os.remove("menu.mp3")
	else:
		print("The file does not exist")

	while choice.lower() != 'exit':	
		if 'create' in choice.lower():
			# print("here")
			x = send_final_message(SERVICE2)
		if 'inbox' in choice.lower():
			x = check_mails(SERVICE2)
		if 'search' in choice.lower():
			x = search(SERVICE2)
		if 'exit' in choice.lower():
			choice = 'exit'
			speak("Bye Bye!")
			return HttpResponse('done')

		menu = "Cursor has moved back to the main menu! If you want to exit the application, say 'exit'. To check your inbox, say 'inbox', to send a new mail, say 'create a mail' and to search for a message, say 'search'."
		my_obj = gTTS(text = menu, lang = 'en', slow = "False", tld="com")
		my_obj.save("again.mp3")
		playsound("again.mp3")
		choice = get_audio()
		if os.path.exists("again.mp3"):
			os.remove("again.mp3")
		else:
			print("The file does not exist")
	return HttpResponse('done')	
	
	

