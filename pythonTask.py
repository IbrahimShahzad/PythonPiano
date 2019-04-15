import pygame
from pygame.locals import *

import math
import numpy

# notes C C# D D# E F F# G G# A A# B
#notes=[130,138,146,155,164,174,185,196,207,233,246,
#       261,277,293,311,329,349,369,392,415,440,466,493,
#       523,554,587,622,659,698,739,783,830,880,932,987,
#       1046,1108,1174,1244,1318,1396,1479,1661,1760,1864,1975,2093]

keys=['q','w','e','r','t','y','u','i','o','p','[',']','a',
      's','d','f','g','h','j','k','l',';','\'','z','x','c',
      'v','b','n','m',',','.','/']

def changesound(factor):
    sample_rate = 44100
    duration =2
    n_samples = int(round(duration*sample_rate))

    #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    max_sample = 2**(bits - 1) - 1
    f = math.pow(2,factor/12)*440
    for s in range(n_samples):
        t = float(s)/sample_rate 
        buf[s][0] = int(round(max_sample*math.sin(2*math.pi*f*t)))        # left
        buf[s][1] = int(round(max_sample*math.sin(2*math.pi*f*t)))    # right
#    print (buf) 
    return (buf)


size = (480, 480)
bits = 16
pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

#this sounds totally different coming out of a laptop versus coming out of headphones

tones =range(-11,37)
#print(tones)
print("processing..Please wait")
buff1 = [changesound(n) for n in tones]
print(len(buff1))
s =map(pygame.sndarray.make_sound,buff1)
key_sound = dict(zip(keys, s))
#play once, then loop forever
#sound.play()
print("done")
is_playing = {k: False for k in keys}

_running = True
while _running:
        event = pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
#            print(pygame.KEYDOWN)
            if (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(fade_ms=50)
                print(key_sound.keys()) 
                is_playing[key] = True

            elif event.key == pygame.K_ESCAPE:
                _runnning = False
                pygame.quit()

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            key_sound[key].fadeout(50)
            is_playing[key] = False
pygame.quit()
