#Dr. RNG(or "BLiNX PERSON")'s super simple Detroit: Become Human randomizer
#Be sure to back up your IDX file before using just in case!
#This rewrite aims to use a pre-generated asset list to speed things up significantly:
#What took 30+ minutes in the old script only takes like 5 seconds in the new one
#Extra information will be stored in a comment block at the end of the script.

#Configuration information - 1 = randomize, anything else = don't randomize
anim = 0 #Breaks the game a lot, turn this off if you want a playable experience
move = 1 #Randomizes each playable (and non-playable) character's animation set. Can make the game unplayable.
hmns = 0 #Human characters - can (and probably will) lead to softlocks
ands = 0 #Android characters - can (and probably will) lead to softlocks
voic = 1 #Randomizes voice clips
vide = 1 #Randomizes videos

#Choose your voice language here
lang = "ENG" #(ARA, ENG, JPN, SPA, RUS, FRE, GER, ITA, BRA, MEX, POR, POL)

import struct
import tkinter as tk #Used to kill the extra tkinter window
import os
from tkinter import filedialog
import random

root = tk.Tk() #Create a root window
root.withdraw() #Hide the root window
folder = filedialog.askdirectory() #Prompt the user to open the folder with the idx file
root.destroy() #Kill the root window

BigFile = folder+"/BigFile_PC"

def randomize(TYPE, OFFSETS, LIST, FILE):
    random.shuffle(OFFSETS) #Shuffle the offsets
    with open(FILE+".idx", "r+b") as f:
        print(f"Starting {TYPE}...")
        for i in range(len(LIST)-1):
            offset = OFFSETS[i]
            data_chunk1, data_chunk2 = LIST[i]
            f.seek(offset)
            f.write(data_chunk1)
            f.seek(4, 1)
            f.write(data_chunk2)
        print(f"End of {TYPE} reached! {len(LIST)} assets were randomized.")

#Get everything from the asset list
file = "AssetList.txt" #Get this from the same folder as the script!

#Offsets
animationOffsets = []
movesetOffsets = []
humanOffsets = []
androidOffsets = []
voiceOffsets = []
videoOffsets = []

#Info
animations = [] #Animations used for cutscenes and non-playable characters
movesets = []   #Calling these movesets for simplicity
humans = []     #Human models (listed from deadray)
androids = []   #Android models (listed from deadray)
voices = []     #Voice clips
videos = []     #Videos

with open(file, "r") as f:
    lines = f.readlines()
with open(BigFile+".idx", "r+b") as f:
    for line in lines: #The main "get stuff" loop
        if line.startswith("?") != True:
            offset = int(line.split()[1], 16)
            f.seek(offset)
            info1 = f.read(8)
            f.seek(4, 1)
            info2 = f.read(16)
            if anim == 1 and line.startswith("ANIMDATA") == True:
                data = info1, info2
                animations.append(data)
                animationOffsets.append(offset)
            if move == 1 and line.startswith("GMK_ANIM"):
                data = info1, info2
                movesets.append(data)
                movesetOffsets.append(offset)
            if hmns == 1 and line.startswith("HumanModel"): #The list needs to be fixed!
                data = info1, info2
                humans.append(data)
                humanOffsets.append(offset)
            if ands == 1 and line.startswith("AndroidModel"): #The list needs to be fixed!
                data = info1, info2
                androids.append(data)
                androidOffsets.append(offset)
            if voic == 1 and line.startswith("Voice") == True and "ENG" in line:
                data = info1, info2
                voices.append(data)
                voiceOffsets.append(offset)
            if vide == 1 and line.startswith("VIDEO") == True:
                data = info1, info2
                videos.append(data)
                videoOffsets.append(offset)

    if anim == 1:
        TYPE = "animations"
        randomize(TYPE, animationOffsets, animations, BigFile) #Randomize the animations
        
    if move == 1:
        TYPE = "movesets"
        randomize(TYPE, movesetOffsets, movesets, BigFile) #Randomize the "movesets"

    if hmns == 1:
        TYPE = "human characters"
        randomize(TYPE, humanOffsets, humans, BigFile) #Randomize the human characters

    if ands == 1:
        TYPE = "android characters"
        randomize(TYPE, androidOffsets, androids, BigFile) #Randomize the human characters
    
    if voic == 1:
        TYPE = "voices"
        randomize(TYPE, voiceOffsets, voices, BigFile) #Randomize the voice clips

    if vide == 1:
        TYPE = "videos"
        randomize(TYPE, videoOffsets, videos, BigFile) #Randomize the videos

#Edits/modifications and rewrites are welcome.
#The end goal of this randomizer was to be able to randomize as much stuff as possible without modifying any of the 50+ gigabytes worth of packages.
#This script is supposed to be free.
#If anyone made you buy it in any way/shape/form without any significant modifications, I (Dr. RNG/BLiNX PERSON) am not to blame.
