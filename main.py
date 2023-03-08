import gradio as gr
import openai, config, subprocess
# from gtts import gTTS
# import os
openai.api_key = config.OPENAI_API_KEY

messages=[
        # {"role": "system", "content": "You are a microsoft professional"},
    ]

def transcribe(audio):
    print(audio)
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)
    
    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages
        
        )
    
    print(response)

    language = 'en'

    system_message = response["choices"][0]["message"]["content"]
    # output = gTTS(text=system_message, lang=language, slow=False)
    # output.save("output.mp3")
    # os.system("start output.mp3")
    # subprocess.call("say", system_message)

    messages.append({"role": "assistant", "content": system_message})

    # subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"
    
    
    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()