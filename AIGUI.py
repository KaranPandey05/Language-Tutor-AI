import tkinter as tk
from tkinter import ttk
import openai
import boto3
import pydub
from pydub import playback
import speech_recognition as sr
import whisper
from tkinter.filedialog import *


openai.api_key = "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"

recognizer = sr.Recognizer()
WAKE_WORD = "friday"
exit_command = "bye"  # Command to exit the conversation loop

def get_wake_word(phrase):
    if WAKE_WORD in phrase.lower():
        return WAKE_WORD
    else:
        return None

def audio_to_text(filename):
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def aws_speechFr(text, output_filename, voice_id):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural',
    )

    with open(output_filename, 'wb') as f:
        f.write(response['AudioStream'].read())

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

def generate_response(prompt, voice_id, content, response_label, user_input_label):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": content}, 
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        top_p=1,
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\nUser:"],
        temperature=0.5,
    )

    response_text = response['choices'][0]['message']['content']
    response_label.config(text=f"AI Generated Response:\n{response_text}", foreground="black", wraplength=500, justify="left", width=60)  # Adjust width here
    response_label.update()

    user_input_label.config(text=f"User Input: {prompt}", foreground="black")
    user_input_label.update()

    response_audio_file = 'response.mp3'
    aws_speechFr(response_text, response_audio_file, voice_id)
    play_audio(response_audio_file)

def start_conversation(prompt=None):
    global response_label, user_input_label
    response_label.config(text="Listening...")

    model = whisper.load_model("tiny")

    while True:
        if prompt:
            phrase = prompt
        else:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                try:
                    with open("audio.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    result = model.transcribe("audio.wav")
                    phrase = result["text"]
                    print(f"You said: {phrase}")
                    if exit_command in phrase.lower():
                        break  # Exit the conversation loop if exit command is given
                except Exception as e:
                    print("Error:", e)

        generate_response(phrase, 'Isabelle', "You are a French language teacher. You will teach the user French. Since the user is an English speaker, you should talk in English. Only talk in French when translating something.", response_label, user_input_label)
        prompt = None  # Reset prompt for the next iteration

def gui_main():
    global response_label, user_input_label

    def start_conversation_from_entry():
        prompt = user_prompt_entry.get()
        start_conversation(prompt)

    root = tk.Tk()
    root.title("Isabella the French Tutor")  # Modify the title here
    root.geometry("1280x720")
    root.resizable(False, False)  # Make the window non-resizable

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 14, 'bold'), foreground="black", background="#34495E", padding=10)
    style.map('TButton', background=[('active', '#2C3E50')], foreground=[('active', 'white')])

    title_label = tk.Label(root, text="Isabelle the French Tutor", font=('Helvetica', 20, 'bold'), fg='white', bg='#2C3E50')
    title_label.pack(side=tk.TOP, pady=20)

    user_prompt_entry = tk.Entry(root, width=80, font=('Helvetica', 14), bg='#34495E', fg='white', insertbackground='white')
    user_prompt_entry.pack(side=tk.TOP, pady=10)

    submit_button = ttk.Button(root, text="Ask", command=start_conversation_from_entry)
    submit_button.pack(side=tk.TOP, pady=10)

    start_conversation_button = ttk.Button(root, text="Start Conversation", command=start_conversation)
    start_conversation_button.pack(side=tk.TOP, pady=10)

    conversation_frame = tk.Frame(root, bg="#2C3E50")
    conversation_frame.pack(side=tk.TOP, pady=20, fill=tk.X)

    user_input_label = ttk.Label(conversation_frame, text="", padding=20, font=('Helvetica', 14), foreground="white", background="#2C3E50", relief="solid", borderwidth=4, wraplength=500, justify="left")
    user_input_label.pack(side=tk.LEFT, padx=10)

    response_label = ttk.Label(conversation_frame, text="", padding=20, font=('Helvetica', 14), foreground="white", background="#2C3E50", relief="solid", borderwidth=4, wraplength=500, justify="right")
    response_label.pack(side=tk.RIGHT, padx=10)

    root.configure(bg="#2C3E50")  # Set window background color

    root.mainloop()

if __name__ == "__main__":
    gui_main()
