import wave
import numpy
import struct
import getpass
import os
from threading import Thread


audioFile = "/home/dhyey/Codes/Projects/Steganography with Audio/audio.wav"
fileObj = wave.open(audioFile, mode='rb')

channel = fileObj.getnchannels()
sampleWidth = fileObj.getsampwidth()
sampleRate = fileObj.getframerate()
nFrames = fileObj.getnframes()

def audioStegoProcess():

    frames = fileObj.readframes(fileObj.getnframes())
    sample = struct.unpack("<"+"h"*(len(frames)//2), frames)
    samples = list(sample)

    with open(".binaryMessage.txt", 'r') as file:
        data = str(file.read().strip())

    for i in range(len(data)):
        bit = int(data[i])

        # clear LSB
        samples[i] = samples[i] & ~1

        # set new bit
        samples[i] = samples[i] | bit

    modifyFrames = struct.pack("<" + "h"*len(samples), *samples)
    newFile = wave.open("stego.wav", "wb")

    newFile.setnchannels(channel)
    newFile.setsampwidth(sampleWidth)
    newFile.setframerate(sampleRate)

    newFile.writeframes(modifyFrames)

    newFile.close()

    for i in range(0, len(sample)):
        newSample = str(format(sample[i], '08b'))
        



def encode():
    start_sequence = "(!%&#"
    end_sequence = "(*&()"
    secret_Message = str(getpass.getpass("Message: "))
    secret_Message = start_sequence + f"  {secret_Message}  " + end_sequence
    with open(f"{os.getcwd()}/.binaryMessage.txt", 'w') as file:
        file.write("")
    print(secret_Message)
    os.chdir(os.getcwd())
    for length in secret_Message:
        ascii_value = ord(length)
        with open(f"{os.getcwd()}/.binaryMessage.txt", 'a') as file:
            file.write(format(ascii_value, '08b'))
    
    audioStegoProcess()
    

def decode():
    """THE DECODING LOGIC WILL BE HERE"""


if __name__ == "__main__":
    # audioStegoProcess()
    print("Steganography Tool:")
    print("1. Encode")
    print("2. Decode")
    choice = int(input("Answer: "))
    if choice == 1:
        selected_audio_path = "/home/dhyey/Codes/Projects/Steganography with Audio/audio.wav"
        encode()
    elif choice == 2:
        decode()
    else:
        print("Invalid choice")