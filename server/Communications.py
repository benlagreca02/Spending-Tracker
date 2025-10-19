# handles comms to the silly trinket

# TODO this is a really poorly organized class, I'm just giving myself a "TODAY"
# deadline for a v1 prototype

# This should be a "client" class or something

import socket

CHARS = 16
PIXELS_PER_CHAR = 5
class Communicator:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_percent_lcd(self, percent):
        # 16x2 screen
        formatted = f"{percent:.2f}%".center(CHARS)
        # print(f"'{formatted}'")
        num_filled_pixels = int((percent * CHARS * PIXELS_PER_CHAR) / 100)
        # formatted += chr(0b0001100) * num_filled_chars

        fully_filled_chars = int(num_filled_pixels // PIXELS_PER_CHAR)
        partial_fill_pixels = num_filled_pixels % PIXELS_PER_CHAR

        # TODO make not a magic number
        formatted += chr(5) * fully_filled_chars

        if fully_filled_chars < CHARS:
            lookup = {0: ' ', 1: chr(1), 2: chr(2), 3: chr(3), 4: chr(4)}
            lastChar = lookup[partial_fill_pixels]
            formatted += lastChar
        
        # send logic
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(formatted.encode(), (self.ip, self.port))


