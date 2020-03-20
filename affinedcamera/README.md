The `magic_webcam.py` can be used for presenting a paper on your desk or a close-enough whiteboard. You should run this code using `python3`.

If everything goes well, you will see a "calibration" window. On this window you must specify 3 points so that they will be stretched out to cover the entire image using a simple affine transform. You can use this script to project a paper or a close-enough whiteboard on your webcam(just select the points carefully). The points will be considered as Top Left, Top Right, and Bottom Left respectively. There's also a gif at the end of this REAMDE to help you pick the right spots.

As you see the output of this code can be viewed as an OpenCV window. Unfortunately, that's not always the case! You may also want to share the output in an online platform such as Skype(or any other software which uses your webcam). Of course you can always use the "screen sharing" feature provided by the platform itself, however,  it would take too much unnecessary bandwidth and also, make your computer slower during the presentation. In the following I will provide you a fairly simple way to stream this output(transformed image) as a fake webcam.
These instructions will work on Linux. Of course you can still use the basic feature(affine transform resulting a window) on any operating system having `python` and `OpenCV` installed. 

# Step 1

First of all, we need a video device. Almost all of the applications using your webcam, will automatically search your computer's video devices and provide you a list of cameras to use. So we will create a new one to fool these applications.

To do so, we will use [v4l2loopback](https://github.com/umlaeute/v4l2loopback). There's a great detailed help on their README on how to install their module. I also took hints from the first answer on this [question](https://unix.stackexchange.com/questions/528400/how-can-i-stream-my-desktop-screen-to-dev-video1-as-a-fake-webcam-on-linux?answertab=active#tab-top)
Here are the commands I used: 

1. git clone https://github.com/umlaeute/v4l2loopback/
2. cd v4l2loopback
3. sudo make
4. sudo make install
5. sudo depmod -a
6. sudo modprobe videodev
7. sudo insmod ./v4l2loopback.ko devices=1 video_nr=1 exclusive_caps=1
8. ls -al /dev/video* (check if whether the device is created)

Now we have our device, you may already be able to see it in the list of available webcams in different applications. But the problem is that it's not currently streaming any data. So let's fix it. instead of showing each processed frame using `imshow`, we will pipe the data to a ffmpeg command. the command will stream the frames into the new created video device.


THIS README IS NOT COMPLETED YET, IF YOU ARE SEEING THIS U R REALLY UNLUCKY, JUST WAIT TILL TONIGHT AND I WILL COMPLETE IT.



the `fastcam.py` is the same script which you can find outside of this directory. It's been used for better fps and lower delay.



Don't forget to smile in the first window; you might not get the chance on the second one.

cheers.
