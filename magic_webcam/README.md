The `magic_webcam.py` can be used for presenting a paper on your desk or a close-enough whiteboard. Beside the packages mentioned in the following, you also need to have **OpenCV** installed. You can use the following [guide](https://www.learnopencv.com/install-opencv3-on-ubuntu/).

Run the code using:
```
python magic_cam.py
```
As long as you have OpenCV installed, the python version doesn't matter.

After running the script, if everything goes well, you will see a "calibration" window. On this window you must specify 3 points using your left mouse button. These points will be used for an affine transform. The selected cordinates will become **Top Left**, **Top Right**, and **Bottom Left** respectively.

As you see the output of this code can be viewed as an OpenCV window. Unfortunately, that's not always the case! You may also want to share the output in an online platform such as Skype(or any other application which uses your webcam). Of course you can always use the "screen sharing" feature provided by the platform itself, however,  it would take too much unnecessary bandwidth and also, make your computer's performance lower during the presentation. In the following I will provide you a fairly simple way to stream this output(transformed images) as a fake webcam.
These instructions will work on Linux. Of course you can still use the basic feature(affine transform resulting in a window) on any operating system having `python` and `OpenCV` installed. 

# Step 1

First of all, we need a video device. Almost all of the applications using your webcam, will automatically search your computer's video devices and provide you a list of cameras to use. So we will create a new one to let it be useable in  such applications.

To do so, we will use [v4l2loopback](https://github.com/umlaeute/v4l2loopback). There's a great detailed guide on their README to help you install their module. I also took hints from the first answer on this [question](https://unix.stackexchange.com/questions/528400/how-can-i-stream-my-desktop-screen-to-dev-video1-as-a-fake-webcam-on-linux?answertab=active#tab-top)
Here are the commands I used: 
```
git clone https://github.com/umlaeute/v4l2loopback/
cd v4l2loopback
sudo make
sudo make install
sudo depmod -a
sudo modprobe videodev
sudo insmod ./v4l2loopback.ko devices=1 video_nr=1 exclusive_caps=1
ls -al /dev/video* (check whether the device is created. You can also use "v4l2-ctl --list-devices" without the " ")
```
Now we have our device, you may already be able to see it in the list of available webcams in different applications. But the problem is that it's not currently streaming any data. So let's fix it. instead of showing each processed frame using `imshow()`, we will pipe the data to a **ffmpeg** command. The command will stream the frames into the new created video device.

To install ffmpeg:
```
sudo apt install ffmpeg
```

Now that we got everything set, the only thing left is to pipe the output to the right ffmpeg command. To enable piping on `magic_cam.py` we will use the `--pipe on` option.

So the command will be:
```
python3 magic_webcam.py --pipe on| ffmpeg -f rawvideo -pixel_format rgb24 -video_size 1280x720 -framerate 30 -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 -vf 'scale=1280:720' -pixel_format rgb24 /dev/video1


```



THIS README IS NOT COMPLETED YET, IF YOU ARE SEEING THIS U R REALLY UNLUCKY, JUST WAIT TILL TONIGHT AND I WILL COMPLETE IT.



the `fastcam.py` is the same script which you can find outside of this directory. It's been used for better fps and lower delay.



Don't forget to smile in the first window; you might not get the chance on the second one.

cheers.
