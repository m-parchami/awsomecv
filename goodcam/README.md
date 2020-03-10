On this python script, we simply use multi-threading for reading and displaying images from a VideoCapture stream(e.g. webcam).

The benefit of this approach could be that reading and displaying frames, no longer block each other out. if we simply put them in a sequential order like this:

```
while True:
  ...
  img = cap.read()
  cv2.imshow('whatever',img)
  cv2.waitKey(1)
  ...
```

The problem is that every `imshow()` is waiting for its previous `read()` to complete, also every `read()` invocation is waiting for the previous captured frame to be displayed ( + of course additioinal 1ms delay on `waitKey(1)` and possibly any other delay by processing input frames).

On this approach we try make these tasks separate, so we use the main thread for displaying and create a seperate thread for reading the frames from input. However, in order to keep an eye on frames and not to lose too much data, we buffer the input frames using the Python built-in queue module.

The length of queue can be really effective. Having it set too small(e.g. 1), may result in almost getting back to the above situation. Also having it too high, may result in getting far from being realtime( having a large queue, may take time to make it empty, so it will take too much time to reach the current and latest captured frame).

In my expierience having it set around 5 or 10 was quite good and satisfying.

Oh btw, this was my first publishing code on github. Hope you guys enjoy it :)

Best regards.
