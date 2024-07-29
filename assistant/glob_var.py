hears    = False
gpt_bool = False
wake_up  = False
voice    = ''
volset   = 0

def set_bool_mic(bools):
    global hears
    hears = bools
    print(hears)

def read_bool_mic():
    global hears
    return hears

def set_bool_gpt(bools):
    global gpt_bool
    gpt_bool = bools
    print(gpt_bool)

def read_bool_gpt():
    global gpt_bool
    return gpt_bool

def set_bool_wake_up(bools):
    global wake_up
    wake_up = bools
    print(wake_up)

def read_bool_wake_up():
    global wake_up
    return wake_up

def set_volset(vol):
    global volset
    volset = vol
    print(vol)

def read_volset():
    global volset
    return volset

def set_voice(voices):
    global voice
    voice = voices
    print(voices)

def read_voice():
    global voice
    return voice