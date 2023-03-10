import openai
import pyttsx3
import speech_recognition as sr
import time

r=sr.Recognizer()
r.energy_threshold=4000

#set the api key
openai.api_key = "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"

# r=sr.Recognizer()
# r.energy_threshold=4000

# Initialize the text to speech engine

engine = pyttsx3.init()
def transcribe_audio_to_text(filename):
    # recognizer = sr.Recognizer()
    with sr.Audiofile(filename) as source:
        audio = r.record(source)
    try:
        return r.recognize(audio)
        
    except:
        print('Skiping unkown error')

def generate_response(prompt):
    response =openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runandWait()

def main():
    while True:
        #wait for user to say "genius"
        print("Say 'Genius' to start recording your question.")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transciption = recognizer.recognize(audio)
                
                if transciption.lower() == "genius":
                    #Record audio
                    filename = "input.wav"
                    print("Say your question")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshhold = 1
                        audio = r.listen(source, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    #Transcrive audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}") 

                        #Generate response using chat GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        #Read response using text-to-speech       
                        speak_text(response)

            except Exception as e:
                print("An error has occurred: {}".format(e))            

if __name__ == "__main__":
    main()                