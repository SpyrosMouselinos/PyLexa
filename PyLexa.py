import os
import sys
import subprocess
import speech_recognition as sr


command_list = [
    ('banana', '/usr/bin/firefox -new-window https://www.youtube.com/watch?v=sFukyIIM1XI'),
    ('mountain', '/usr/bin/firefox -new-window  https://www.youtube.com/watch?v=iW1jxJ6ISks')
]


def discover_microphones():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for microphone(device_index = {0})".format(index, name))


def word_to_command(captured, hot_words):
    command = None
    for word in captured:
        for keys in hot_words:
            if word.lower() == keys[0].lower():
                command = keys[1]
                break
    return command


def main():
    captured = ""
    r = sr.Recognizer()
    discover_microphones()
    mic = sr.Microphone(device_index=4)
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.8)
        print ("Ready to capture")
        audio = r.listen(source)
    try:
        captured = r.recognize_google(audio)
    except ValueError:
        print('Couldn\'t understand shit mate')


    captured = captured.split(' ')
    command = word_to_command(captured=captured, hot_words=command_list)
    """
        Shell = True is a security risk but here is used for debugging purposes
    """
    if command is not None:
        subprocess.call(command, shell=True)


if __name__ == '__main__':
    main()
