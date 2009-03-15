i = 0
def song():
    global i
    i += 1
    print i, "This is a song that never ends"
    song()
song()
