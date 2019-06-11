#Deep-frier

import wave as w, os, numpy as np, struct, time, winsound as wn, math, tkinter as tk, colorsys
from turtle import Screen, Turtle

toot = tk.Tk()
toot.withdraw()

print("Please choose a WAV file")

c = True
while c == True:
    file_path = tk.filedialog.askopenfilename()
    print(file_path[len(file_path) - 3:])
    if file_path[len(file_path) - 3:] == "wav":
        c = False
    else:
        print("Please choose a valid WAV file")



#fp = "\\".join(file_path.split("/"))

print(file_path)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


benchmarkTime = 0
curTime = time.time()
gFinal = 0
t = Turtle('square', visible=False)
t.pu()
x = -1

s = Screen()
s.tracer(False)
off = 0
H = 1
debounce = True

#Number of seconds you want each audio file to be
NUM_SEC = 0.5

WRITE_TIMER = math.floor((1000 * NUM_SEC)) - 20

SONG_TITLE = file_path

AMPLIFIER = 100
pastAMPLIFIER = AMPLIFIER

def Volume():
    global H, AMPLIFIER
    if H - 0.01 >= 0:
        H -= 0.01
    else:
        H = 1
    
    t.clear()
    t.color(colorsys.hsv_to_rgb(H, 1, 1))
    t.write("Volume:\n\t" + str(AMPLIFIER) + "%\n\n\n\nHold 'A' to deepfry", False, align='center', font=("Arial", 30, 'normal'))
    s.ontimer(Volume, 30)

def Up():
    global AMPLIFIER
    #print('put on')
    AMPLIFIER += 1

def Down():
    global AMPLIFIER
    #print('put off')
    if AMPLIFIER > 0:
        AMPLIFIER -= 1

def Timer():
    global curTime, benchmarkTime
    if curTime - benchmarkTime >= 1:
        benchmarkTime = time.time()
        
def Write():
    global gFinal, off, x, WRITE_TIMER, NUM_SEC, SONG_TITLE, AMPLIFIER
    
    x += 1
    
    source = w.open(SONG_TITLE, 'rb')
    
    params = source.getparams()
    
    source.close()
    
    if x != params[3] // 44100:
        source = w.open(SONG_TITLE, 'rb')

        params = source.getparams()
        
        frames = params[3]
        
        final = source.readframes(frames)

        final = final[math.floor(params[2] * (NUM_SEC) * params[1] * params[0] * x) : math.floor(params[2] * (NUM_SEC) * params[0] * params[1] * (x + 1))]
    
        nuFinal = np.fromstring(final, np.int16) // 100 * AMPLIFIER

        nuFinal = struct.pack('h'*len(nuFinal), *nuFinal)
        
        source.close()
        
        output = w.open('temp', 'wb')
        
        output.setparams(params)
        
        output.writeframes(nuFinal)
        
        output.close()
        
        wn.PlaySound('temp', wn.SND_ASYNC)
        
        s.ontimer(Write, WRITE_TIMER)

def DEEPFRY():
    global AMPLIFIER, pastAMPLIFIER, debounce
    if debounce:
        pastAMPLIFIER = AMPLIFIER
        debounce = False
    AMPLIFIER = 500
    
def antiDEEPFRY():
    global AMPLIFIER, pastAMPLIFIER, debounce
    AMPLIFIER = pastAMPLIFIER
    debounce = True
    

s.listen()
s.onkeypress(Up, 'Up')
s.onkeypress(Down, 'Down')

s.onkeypress(DEEPFRY, 'a')
s.onkeyrelease(antiDEEPFRY, 'a')

s.ontimer(Write, WRITE_TIMER)
s.ontimer(Volume, 30)
