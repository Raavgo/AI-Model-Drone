import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("coco-airplane", threshold=0.6)
camera = jetson.utils.videoSource("/dev/video2")      # 1280/720 -> ideal coords 640/360
display = jetson.utils.videoOutput("display://0")

while True:
	img = camera.Capture()
	detections = net.Detect(img)

	for detection in detections:

		if detection.Confidence > 0.85:
			direction = detection.Center[0]-640 #negtive -> steer right; positve steer left
			altitude = detection.Center[1]-360 #negative -> ascend; positive descend
			print ("Detected Object {0} at {1} x/y Steering command({2}/{3})".format(detection.ClassID, detection.Center, direction, altitude))
	
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

	if not camera.IsStreaming() or not display.IsStreaming():
		break
