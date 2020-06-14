The `magic_webcam.py` can be used for presenting a paper on your desk or a close-enough whiteboard. Besides the packages mentioned in the following, you also need to have **OpenCV** installed. You can use this [guide](https://www.learnopencv.com/install-opencv3-on-ubuntu/).

Run the code using:
```
python magic_cam.py
```
As long as you have OpenCV installed, the python version doesn't matter.

After running the script, if everything goes well, you will see a "calibration" window. On this window, you must specify 4 points using your left mouse button. These points will be used for a perspective transformation. The selected coordinates will become **Top Left**, **Top Right**, and **Bottom Left** respectively.

As you can see, the output of this code can be viewed in an OpenCV window. Unfortunately, that's not always the case! You may also want to share the output in an online platform such as Skype(or any other application which uses your webcam). Of course, you can always use the "screen sharing" feature provided by the platform itself, however,  it would take too much unnecessary bandwidth and also, lower your computer's performance during the presentation. In the following, I will provide you a fairly simple way to stream this output(transformed images) as a fake webcam.
These instructions will work on Linux. Of course, you can still use the basic feature(perspective transformation resulting in a window) on any operating system having `python` and `OpenCV` installed. 

# Step 1

First of all, we need a video device. Almost all of the applications using your webcam, will automatically search your computer's video devices and provide you a list of cameras to use. Therefore, we will create a new one to let it be useable in such applications.

To do so, we will use [v4l2loopback](https://github.com/umlaeute/v4l2loopback). There's a great detailed guide on their README to help you install their module. I also took hints from the first answer on this [question](https://unix.stackexchange.com/questions/528400/how-can-i-stream-my-desktop-screen-to-dev-video1-as-a-fake-webcam-on-linux?answertab=active#tab-top). Make sure you install this module somewhere accessible enough!

Here are the commands I used: 
```
git clone https://github.com/umlaeute/v4l2loopback/
cd v4l2loopback
sudo make
sudo make install
sudo depmod -a
```
# Step 2
Now that the module is set, we must create our new video device. Keep in mind that you should run the following commands every time you reboot your Linux from the installation directory `[Your installation path]/v4l2loopback`
```
sudo modprobe videodev
sudo insmod ./v4l2loopback.ko devices=1 video_nr=1 exclusive_caps=1
```
Now we must check whether the device is created. You can use either of the below commands:
```
ls -al /dev/video*
v4l2-ctl --list-devices
```
# Step 3
Now we have our device, you may already be able to see it in the list of available webcams in different applications. But the problem is that it's not currently streaming any data. So let's fix it. instead of showing each processed frame using `imshow()`, we will pipe the data to an **ffmpeg** command. The command will stream the frames into the newly created video device.

To install ffmpeg:
```
sudo apt install ffmpeg
```

Now that we got everything set, the only thing left is to pipe the output to the right ffmpeg command. To enable piping on `magic_cam.py`, we will use the `--pipe on` option.

So the command will be:
```
python magic_webcam.py --pipe on| ffmpeg -f rawvideo -pixel_format rgb24 -video_size 1280x720 -framerate 30 -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 -vf 'scale=1280:720' -pixel_format rgb24 /dev/video1
```
Don't forget to change the scale configuration based on your situation

The `fastcam.py` is the same script which you can find outside of this directory named `goodcam.py`. It's been used for better fps and lower delay. To be short, it uses a separate thread for reading the frames from the video source.

cheers.
