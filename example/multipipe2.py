# This code continuously checks for incoming images from stdincollection.stdin_deque,
# converts the color space of the images from RGB to BGR, and writes the processed images to the named pipe
# using the write2pipe function.

# The code enters an infinite loop with the statement while True:
#
# Inside the loop, the code checks the value of stdincollection.ran_out_of_input.
# If it is True, the code calls os._exit(1) to exit the program with a status code of 1,
#
# If stdincollection.ran_out_of_input is False, the code proceeds to the next conditional statement.
#
# The code checks if the stdincollection.stdin_deque is empty by evaluating if not stdincollection.stdin_deque.
# If it is empty, the code executes sleep(0.01) to pause the execution for a short period (10 milliseconds)
# before continuing to the next iteration of the loop.
#
# If stdincollection.stdin_deque is not empty, the code pops an item from the deque using
# stdincollection.stdin_deque.pop(). The popped item is then copied to a new variable called poppeddata.
#
# The code converts the color space of the poppeddata image from RGB to BGR using cv2.cvtColor with the
# flag cv2.COLOR_RGB2BGR. The result is stored in a variable called with_changed_color.
#
# Finally, the code calls the write2pipe function, passing with_changed_color as the object to be written to the named
# pipe (back to the original process).
#
# Any exceptions that occur during the execution of the code are caught in a general Exception block,
# and the code continues to the next iteration of the loop.
#

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
        with_changed_color = cv2.cvtColor(poppeddata, cv2.COLOR_RGB2BGR)
        write2pipe(obj=with_changed_color)
    except Exception:
        continue
