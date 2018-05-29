#!/usr/bin/env python3

"""SmoothLife -- Conway's GoL in continuous space

Re-written in Python using the speedups of Numpy

Todo:
    Better integration methods
    Fancy UI
    Refactor. OO design always fails because of nested variable access

Explanations and code (in other language) here:
https://0fps.net/2012/11/19/conways-game-of-life-for-curved-surfaces-part-1/
https://arxiv.org/pdf/1111.1567.pdf
https://jsfiddle.net/mikola/aj2vq/
https://www.youtube.com/watch?v=KJe9H6qS82I

Cool Rules:
            [0.0027416340783160686, 0.6373748026737954, 0.7437640616767585, 0.7984013991827422, 0.2438052421875614, 0.6438204125521396]
            [0.1582212461509208, 0.709732439272074, 0.26738279783802943, 0.781360988711159, 0.4044954564226516, 0.3214349039686113]
            [0.5305854486842543, 0.6167403010738612, 0.23649907064310172, 0.8113649659184522, 0.6238395913063111, 0.789539585330646]
            [0.13635397269112381, 0.695819793489881, 0.9465841271808999, 0.2040427232792994, 0.6962220688147399, 0.7048811280771509]
            [0.4137434158369726, 0.4007234242047063, 0.05285580603516038, 0.9517033719767047, 0.32077036940363135, 0.49771531390730817]
            [0.227068593486637, 0.7897684055222489, 0.11586665765688164, 0.8015103053386754, 0.2890897461334061, 0.6711763514499051]
            [0.2651616746301627, 0.18160394908091038, 0.47970348214448477, 0.5262742624979404, 0.1412985040373167, 0.1673625054620962]
            [0.3642724712098512, 0.40233950326429724, 0.04660547960838113, 0.7695233497620191, 0.2192274958064413, 0.6531165731309083]
            [0.4509868720045459, 0.5004244001867932, 0.17372361764237187, 0.36273881900671034, 0.8002984022230082, 0.2010005845781302]
            [0.5533554705476176, 0.5330770670318796, 0.3562917005220898, 0.9562295756514985, 0.3206018317092917, 0.7998314733699114]



"""

import math
import sys
import time
from copy import deepcopy
from random import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from subprocess import call


# # Necessary for writing video
# from skvideo.io import FFmpegWriter
# from matplotlib import cm


#####EXTRA#####
def dice_coefficient(sequence_a, sequence_b):
    '''(str, str) => float
    Return the dice cofficient of two sequences.
    '''
    a = sequence_a
    b = sequence_b
    if not len(a) or not len(b): return 0.0
    # quick case for true duplicates
    if a == b: return 1.0
    # if a != b, and a or b are single chars, then they can't possibly match
    if len(a) == 1 or len(b) == 1: return 0.0
    
    # list comprehension, preferred over list.append() '''
    a_bigram_list = [a[i:i+2] for i in range(len(a)-1)]
    b_bigram_list = [b[i:i+2] for i in range(len(b)-1)]
    
    a_bigram_list.sort()
    b_bigram_list.sort()
    
    # assignments to save function calls
    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)
    # initialize match counters
    matches = i = j = 0
    while (i < lena and j < lenb):
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1
    
    score = float(matches)/float(lena + lenb)
    return score


###Basic#####
class Rules:
    # Birth range
    B1 = random()#0.278
    B2 = random()#0.365
    # Survival range
    D1 = random()#0.267
    D2 = random()#0.445
    # Sigmoid widths
    N = random()#0.028
    M = random()#0.147

    print(f'Rules: {[B1, B2, D1, D2, N, M]}')
    # B1 = 0.257
    # B2 = 0.336
    # D1 = 0.365
    # D2 = 0.549
    # N = 0.028
    # M = 0.147

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # Set variables from constructor

    @staticmethod
    def sigma(x, a, alpha):
        """Logistic function on x

        Transition around a with steepness alpha
        """
        return 1.0 / (1.0 + np.exp(-4.0 / alpha * (x - a)))

    def sigma2(self, x, a, b):
        """Logistic function on x between a and b"""
        return self.sigma(x, a, self.N) * (1.0 - self.sigma(x, b, self.N))

    @staticmethod
    def lerp(a, b, t):
        """Linear intererpolate t:[0,1] from a to b"""
        return (1.0 - t) * a + t * b

    def s(self, n, m):
        """State transition function"""
        alive = self.sigma(m, 0.5, self.M)
        return self.sigma2(n, self.lerp(self.B1, self.D1, alive), self.lerp(self.B2, self.D2, alive))


def logistic2d(size, radius, roll=True, logres=None):
    """Create a circle with blurred edges

    Set roll=False to have the circle centered in the middle of the
    matrix. Default is to center at the extremes (best for convolution).

    The transition width of the blur scales with the size of the grid.
    I'm not actually sure of the math behind it, but it's what was presented
    in the code from:
    https://0fps.net/2012/11/19/conways-game-of-life-for-curved-surfaces-part-1/
    """
    y, x = size
    # Get coordinate values of each point
    yy, xx = np.mgrid[:y, :x]
    # Distance between each point and the center
    radiuses = np.sqrt((xx - x/2)**2 + (yy - y/2)**2)
    # Scale factor for the transition width
    if logres is None:
        logres = math.log(min(*size), 2)
    with np.errstate(over="ignore"):
        # With big radiuses, the exp overflows,
        # but 1 / (1 + inf) == 0, so it's fine
        logistic = 1 / (1 + np.exp(logres * (radiuses - radius)))
    if roll:
        logistic = np.roll(logistic, y//2, axis=0)
        logistic = np.roll(logistic, x//2, axis=1)
    return logistic


class Multipliers:
    """Kernel convulution for neighbor integral"""

    INNER_RADIUS = 7.0
    OUTER_RADIUS = INNER_RADIUS * 3.0

    def __init__(self, size, inner_radius=INNER_RADIUS, outer_radius=OUTER_RADIUS):
        inner = logistic2d(size, inner_radius)
        outer = logistic2d(size, outer_radius)
        annulus = outer - inner

        # Scale each kernel so the sum is 1
        inner /= np.sum(inner)
        annulus /= np.sum(annulus)

        # Precompute the FFT's
        self.M = np.fft.fft2(inner)
        self.N = np.fft.fft2(annulus)


dice_history = set()
len_history = len(dice_history)
initial_lives = 25
lives = initial_lives #to be lost if the pattern repeat itslef too long
class SmoothLife:
    def __init__(self, height, width):
        self.time_start= time.time()
        self.width = width
        self.height = height

        self.multipliers = Multipliers((height, width))
        self.rules = Rules()

        self.clear()
        self.filedset = set()
        # self.esses = [None] * 3
        # self.esses_count = 0

    def clear(self):
        """Zero out the field"""
        self.field = np.zeros((self.height, self.width))
        # self.esses_count = 0

    def step(self):
        """Do timestep and return field"""

        global dice_history, len_history, initial_lives, lives
        # To sum up neighbors, do kernel convolutions
        # by multiplying in the frequency domain
        # and converting back to spacial domain
        field_ = np.fft.fft2(self.field)
        M_buffer_ = field_ * self.multipliers.M
        N_buffer_ = field_ * self.multipliers.N
        M_buffer = np.real(np.fft.ifft2(M_buffer_))
        N_buffer = np.real(np.fft.ifft2(N_buffer_))

        # Apply transition rules
        s = self.rules.s(N_buffer, M_buffer)
        nextfield = s

        # Trying some things with smooth time stepping....
        # Not yet working well....
        # s0 = s - M_buffer
        # s1, s2, s3 = self.esses

        # if self.esses_count == 0:
        #     delta = s0
        # elif self.esses_count == 1:
        #     delta = (3 * s0 - s1) / 2
        # elif self.esses_count == 2:
        #     delta = (23 * s0 - 16 * s1 + 5 * s2) / 12
        # else:  # self.esses_count == 3:
        #     delta = (55 * s0 - 59 * s1 + 37 * s2 - 9 * s3) / 24

        # self.esses = [s0] + self.esses[:-1]
        # if self.esses_count < 3:
        #     self.esses_count += 1
        # dt = 0.1
        # nextfield = self.field + dt * delta

        # mode = 0  # timestep mode (0 for discrete)
        # dt = 0.9  # timestep
        # # Apply timestep
        # nextfield = self._step(mode, self.field, s, M_buffer, dt)
        
        self.prevfield = deepcopy(self.field)
        self.field = np.clip(nextfield, 0, 1)
        #print('prev:', self.prevfield)
        #print('curr:', self.field)
        dice_cf = dice_coefficient(str(self.prevfield), str(self.field))
        
        # if dice_cf < 0.4:
        #     print(f'{dice_cf}: low')
        #     #sys.exit(0)
        # elif dice_cf > 0.80:
        #     print(f'{dice_cf}: high')
        # else:
        #     print(f'{dice_cf}: good')


        len_history = len(dice_history)
        dice_history.add(round(dice_cf,4))

        if len(dice_history) == len_history:
            lives -= 1
        else:
            lives = initial_lives
        if lives < 1:
            print(f'out of lives :(')
            sys.exit(0)

        #print(dice_history)
            #sys.exit(0)
        #self.fieldset = set([])
        #print(f'starting fieldset: {self.fieldset}')
        #self.prevfield = deepcopy(self.fieldset)
        #print(f'starting prevfield: {self.prevfield}')

        if not np.array_equal(self.prevfield, self.field) and time.time() - self.time_start < 30:
            # #quit if the same pattern is repeated over and over
            # past_len = len(self.fieldset)
            # self.fieldset.add(str(self.prevfield))

            # current_len = len(self.fieldset)

            # print(f'past_len: {past_len}, current_len:{current_len}')
            # if past_len == current_len:
            #     timeout -= 1
            #     print(timeout)

            # else:
            #     if current_len > 25:
            #         print('flushing fieldset')
            #         self.fieldset = set()
            #     timeout = 60

            # if timeout <= 0:
            #     print('got stuck in a loop, terminating.')
            #     self.exit(0)


            return self.field
        else:
            print(f'WARNING: population died after {round(time.time()-self.time_start,2)} seconds')
            sys.exit()



    def _step(self, mode, f, s, m, dt):
        """State transition options

        SmoothLifeAll/SmoothLifeSDL/shaders/snm2D.frag
        """
        if mode == 0:  # Discrete time step
            return s

        # Or use a solution to the differential equation
        elif mode == 1:
            return f + dt*(2*s - 1)
        elif mode == 2:
            return f + dt*(s - f)
        elif mode == 3:
            return m + dt*(2*s - 1)
        elif mode == 4:
            return m + dt*(s - m)

    def add_speckles(self, count=None, intensity=1):
        """Populate field with random living squares

        If count unspecified, do a moderately dense fill

        I suggest using a smaller count when using continuous time
        updating instead of discrete because continuous tends to converge.
        """
        if count is None:
            # count = 200 worked well for a 128x128 grid
            # scale according to area
            count = 200 * (self.width * self.height) / (128 * 128)
            count = int(count)
        for i in range(count):
            radius = int(self.multipliers.INNER_RADIUS)
            r = np.random.randint(0, self.height - radius)
            c = np.random.randint(0, self.width - radius)
            self.field[r:r+radius, c:c+radius] = intensity
        # self.esses_count = 0



def show_animation():
    w = 1 << 9#200*16#
    h = 1 << 9#200*9#
    # w = 1920
    # h = 1080
    sl = SmoothLife(h, w)
    sl.add_speckles()
    sl.step()
    fig = plt.figure()
    # Nice color maps: viridis, plasma, gray, binary, seismic, gnuplot, prism
    im = plt.imshow(sl.field, animated=True,
                    cmap=plt.get_cmap("prism"), aspect="equal")

    respawn = 0

    def animate(*args):
        try:
            im.set_array(sl.step())
            return (im, )
        except KeyboardInterrupt:
            sys.exit(0)

    if not respawn:
        ani = animation.FuncAnimation(fig, animate, interval=60, blit=True)
        plt.show()
    else:
        plt.close('All')
        return False



def save_animation():
    w = 1 << 8
    h = 1 << 8
    # w = 1920
    # h = 1080
    sl = SmoothLife(h, w)
    sl.add_speckles()

    # Matplotlib shoves a horrible border on animation saves.
    # We'll do it manually. Ugh

    from skvideo.io import FFmpegWriter
    from matplotlib import cm

    fps = 24
    frames = 24*10
    w = FFmpegWriter("smoothlife.mp4", inputdict={"-r": str(fps)})
    for i in range(frames):
        frame = cm.viridis(sl.field)
        frame *= 255
        frame = frame.astype("uint8")
        w.writeFrame(frame)
        sl.step()
    w.close()

    # Also, webm output isn't working for me,
    # so I have to manually convert. Ugh
    # ffmpeg -i smoothlife.mp4 -c:v libvpx -b:v 2M smoothlife.webm


if __name__ == '__main__':
    show_animation()



    # save_animation()