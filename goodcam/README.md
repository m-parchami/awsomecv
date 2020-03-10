In this python script, we simply use multi-threading for reading and displaying images from a VideoCapture stream(e.g. webcam).

The benefit of this approach could be that reading and displaying frames, no longer block each otehr out. if we simply put them in a sequential order