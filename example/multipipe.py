# this example sets up two separate threads to perform parallel image conversions from RGB to BGR (pipe1) and RGB to
# grayscale (pipe2) using inter-process communication through named pipes.
# The converted images are saved in separate output directories.


# The code begins by importing various modules
# These modules provide functionality for handling operating system operations, image processing, multi-threading,
# inter-process communication, and file manipulation.

import os
import cv2
import kthread
from kthread_sleep import sleep
from varpickler import encode_var
import psutil
from subprocess_multipipe.run_multipipe_subproc import start_subprocess, pipresults
from list_all_files_recursively import get_folder_file_complete_path

# Next, the code defines several variables that hold file paths and folder locations.
# These variables include picfolder (the folder where the input images are located),
# pyfile2 and pyfile1 (file paths for two Python scripts),

# pipename2 and pipename1 (the names of the named pipes used for inter-process communication),
# https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipes

# output_folder_rgb2bgr and output_folder_rgb2gray (folders where the output images will be saved), and allfiles.

picfolder = r"C:\testpipe\testimg"
pyfile2 = r"C:\ProgramData\anaconda3\envs\dfdir\multipipe2.py"
pipename2 = r"\\.\pipe\pipe2"
output_folder_rgb2bgr = r"C:\testpipe\resultrgbgray"
pyfile1 = r"C:\ProgramData\anaconda3\envs\dfdir\multipipe1.py"
pipename1 = r"\\.\pipe\pipe1"
output_folder_rgb2gray = r"C:\testpipe\resultrgbbgr"

# The allfiles variable is a list comprehension that reads all the files with a .jpg extension from the picfolder and
# stores the corresponding images using the cv2.imread function.
# Essentially, it creates a list of OpenCV image objects from the JPEG files in the specified folder.

allfiles = [
    cv2.imread(x.path)
    for x in get_folder_file_complete_path(picfolder)
    if x.ext == ".jpg"
]

# After that, the code defines two functions: pipe1_rgb2bgr and pipe2_rgb2gray. These functions perform the image
# conversion tasks using separate processes.


def pipe1_rgb2bgr():
    # The pipe1_rgb2bgr function uses the start_subprocess function from the run_multipipe_subproc module
    # to start a subprocess by executing the pyfile1 script. It passes various arguments to the subprocess,
    # including the size of the encoded image (imgencodedsize), the name of the pipe (pipename1),
    # and other parameters. The function then writes each image from the allfiles list to the pipe using the
    # p.write_function method. It waits until all images are processed by checking the length of the received
    # results (pipresults.pipedict[pipename1]) and the status of the subprocess using psutil.pid_exists.
    # Finally, it saves the converted images to the output_folder_rgb2bgr directory using cv2.imwrite.
    p = start_subprocess(
        pyfile1,
        bytesize=imgencodedsize,
        pipename=pipename1,
        pickle_or_dill="dill",
        deque_size=len(allfiles) * 2,
        other_args=(),
        write_first_twice=True,
        block_or_unblock="block",
        pipe_timeout_ms=50,
        pipe_max_instances=10,
    )
    # sleep(1)
    for ini, im in enumerate(allfiles):
        p.write_function(im)
    while len(pipresults.pipedict[pipename1]) < len(allfiles) and psutil.pid_exists(
        p.sub_process.pid
    ):
        print(len(pipresults.pipedict[pipename1]))

        sleep(0.2)
    p.kill_process()
    for ini, c in enumerate(pipresults.pipedict[pipename1]):
        cv2.imwrite(os.path.join(output_folder_rgb2bgr, f"{ini}.jpg"), c)


def pipe2_rgb2gray():
    # The pipe2_rgb2gray function is similar to pipe1_rgb2bgr but uses the pyfile2
    # script and operates on a different pipe
    # (pipename2). It also saves the converted images to the output_folder_rgb2gray directory.
    p = start_subprocess(
        pyfile2,
        bytesize=imgencodedsize,
        pipename=pipename2,
        pickle_or_dill="dill",
        deque_size=len(allfiles) * 2,
        other_args=(),
        write_first_twice=True,
        block_or_unblock="block",
        pipe_timeout_ms=50,
        pipe_max_instances=10,
    )
    for ini, im in enumerate(allfiles):
        p.write_function(im)
    while len(pipresults.pipedict[pipename2]) < len(allfiles) and psutil.pid_exists(
        p.sub_process.pid
    ):
        print(len(pipresults.pipedict[pipename2]))
        sleep(0.2)
    p.kill_process()
    for ini, c in enumerate(pipresults.pipedict[pipename2]):
        cv2.imwrite(os.path.join(output_folder_rgb2gray, f"{ini}.jpg"), c)


# After defining the conversion functions, the code calculates the size of the encoded image by calling the encode_var
# function from the varpickler module on the last element of the allfiles list. (biggest image (byte size!!) in this case)
imgencodedsize = len(encode_var(allfiles[-1]))

# Then, two KThread objects (t1 and t2) are created, representing the threads for the pipe1_rgb2bgr and pipe2_rgb2gray
# functions, respectively. These threads are started using the start method.

t1 = kthread.KThread(target=pipe1_rgb2bgr, name="1")

t2 = kthread.KThread(target=pipe2_rgb2gray, name="2")
t1.start()
# sleep(1)
t2.start()
