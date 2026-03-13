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
    os.chdir(os.getcwd())
    for length in secret_Message:
        ascii_value = ord(length)
        with open(f"{os.getcwd()}/.binaryMessage.txt", 'a') as file:
            file.write(format(ascii_value, '08b'))
    
    audioStegoProcess()
    

def decode():
    start_sequence = "(!%&#"
    end_sequence = "(*&()"
    startseq_bin = ''.join(format(ord(c), '08b') for c in start_sequence)
    endseq_bin = ''.join(format(ord(c), '08b') for c in end_sequence)
    audioFile = "stego.wav"
    fileObj = wave.open(audioFile, mode='rb')
    frames = fileObj.readframes(fileObj.getnframes())
    sample = struct.unpack("<"+"h"*(len(frames)//2), frames)
    samples = list(sample)
    
    bits = []
    for i in range(len(sample)):
        lsb = bin(sample[i])
        bits.append(lsb[-1])
    
    binary_message = ''.join(bits)
    start_idx = binary_message.find(startseq_bin)
    end_idx = binary_message.find(endseq_bin, start_idx + len(startseq_bin))
    if start_idx == -1 or end_idx == -1:
        print("No hidden message found.")
        return
    secret_bin = binary_message[start_idx + len(startseq_bin):end_idx]
    decoded_message = ""
    for i in range(0, len(secret_bin), 8):
        byte = secret_bin[i:i+8]
        if len(byte) == 8:
            decoded_message += chr(int(byte, 2))
    
    print("Secret Message:", decoded_message)

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