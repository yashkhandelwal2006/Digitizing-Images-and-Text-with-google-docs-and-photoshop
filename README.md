# Digitizing-Images-and-Text-with-google-docs-and-photoshop
In this project I have tried to do an Instance Segmentation of objects kept near you and paste it inside google docs without a single touch. Also one can extract the text from the images directly paste it inside google docs with minimal touches.

In order to run the project one needs to clone the U-2-net project from https://github.com/NathanUA/U-2-Net and put the script "segmentation.py" inside it's root directory. Also you need to put your own google drive api key and filestack api key. Just a demo project, have added all relevant files. Also If you want to play around with it, and just by using your phone and pointing towards your laptop screen you can simply get the coordinates and paste it at that particular location on the scree. NOTE: This only works with photoshop right now using photoshop connection library. Anyways, for getting the coordinates SIFT is being used for keypoint matching and calculating exact coordinates. This code can be found in "coordinates.py". You need to integrate that with "main.py" in order to use that.

Finally for using it with google docs you need to download the IP webcam app from playstore or apple store and run the "connectionIpwebcam.py" script by replacing the ip with the ip you get from the ip webcam app. Hope this helps whosoever wants to extend this idea.

Go to the following link if you want to see a quick demonstration of how this works with google docs.
https://www.linkedin.com/posts/yash-khandelwal-3a7abb144_python-machinelearning-datascience-activity-6670740489811173376-HpAN
