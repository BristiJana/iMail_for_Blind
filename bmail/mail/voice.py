from time import sleep
import pyttsx3
import speech_recognition as sr
from speech_recognition import Recognizer, Microphone


#converts text to speech
def speak(text):

	engine=pyttsx3.init()
	if engine._inLoop:
		engine.endLoop()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[0].id)
	rate = engine.getProperty('rate')

	engine.setProperty('rate', 178)

	engine.say(text)
	engine.runAndWait()
	sleep(2)


#converts speech to text
def get_audio():
	recog = Recognizer()
	mic = Microphone()

	with mic:
		recog.adjust_for_ambient_noise(mic, duration=1)
		audio = recog.record(mic, duration=4)
		recognized = ""
	try:
		recognized = recog.recognize_google(audio, language='en-in')
		print("you said: ", recognized)
	except:
		print("No")
		# speak("Didn't get that")
	
	return recognized