import tkinter as tk
import subprocess
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import os
import speech_recognition as sr
import wave
import moviepy.editor as mp
from translator.translator import translate_from_file

# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#instructions
instructions = tk.Label(root, text="Select a PDF file on your computer to extract all its text", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)

r = sr.Recognizer()

# importing libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len=500,
        # adjust this per requirement
        silence_thresh=sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

def convert(path):
    # clip = mp.VideoFileClip(r'{}'.format(path))
    # audio_path = r'{}mp3'.format(path[:-3])
    # print(audio_path)
    # clip.audio.write_audiofile(audio_path)
    # path = "/Users/shakil/PycharmProjects/PDFextract_text/starterFiles/test_video.mp4"
    # command = f"ffmpeg -i {path} -ab 160k -ac 2 -ar 44100 -vn audio.wav"

    # subprocess.call(command, shell=True)
    file_name = "/Users/shakil/PycharmProjects/PDFextract_text/finishedProject/audio.wav"
    print("\nFull text:", get_large_audio_transcription(file_name))
    # with sr.AudioFile(file_name) as source:
    #     # listen for the data (load audio to memory)
    #     audio_data = r.record(source)
    #     # recognize (convert from speech to text)
    #     text = r.recognize_google(audio_data)
    #     print(text)
    # with wave.open(file_name, "rb") as wave_file:
    #     frame_rate = wave_file.getframerate()
    #     translate_from_file(file_name, frame_rate)


def open_file():
    browse_text.set("loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("mp4 file", "*.mp4")])
    print(file.name)
    if file:
        convert(file.name)
        # read_pdf = PyPDF2.PdfFileReader(file)
        # page = read_pdf.getPage(0)
        # page_content = page.extractText()
        #
        # #text box
        # text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
        # text_box.insert(1.0, page_content)
        # text_box.tag_configure("center", justify="center")
        # text_box.tag_add("center", 1.0, "end")
        # text_box.grid(column=1, row=3)

        browse_text.set("Browse")

#browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root,
                       textvariable=browse_text,
                       command=lambda:open_file(),
                       font="Raleway",
                       bg="#20bebe",
                       fg="white",
                       height=2,
                       width=15)
browse_text.set("Browse")
browse_btn.grid(column=1, row=2)

canvas = tk.Canvas(root, width=600, height=250)
canvas.grid(columnspan=3)

root.mainloop()
