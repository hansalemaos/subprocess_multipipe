import os

import cv2
from time import sleep
from subprocess_multipipe.start_pipethread import stdincollection, write2pipe

while True:
    if stdincollection.ran_out_of_input:
        os._exit(1)
    if not stdincollection.stdin_deque:
        sleep(0.01)
        continue
    try:
        try:
            poppeddata = stdincollection.stdin_deque.pop().copy()
        except Exception:
            continue
        with_changed_color = cv2.cvtColor(poppeddata, cv2.COLOR_BGR2GRAY)
        write2pipe(obj=with_changed_color)
    except Exception:
        continue
