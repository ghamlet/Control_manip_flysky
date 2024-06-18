import threading

def loop():
    while True:
        print('something')

threading.Thread(target=loop, daemon=True).start()
input('Press <Enter> to exit.')