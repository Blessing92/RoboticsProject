# README #

## Urban maze robot ##

### How to run ###
python3 main_improved.py

### Requirements ###
python v3.
opencv v2.

### Overview ###
The project consists of a  constructed cardboard maze with all the signs placed on 
different walls by using the gopigo2 mounted with a camera to navigate around a maze of boxes. 
Signs will be made out of coloured paper and will be glued/taped to walls. For telling the speed, 
MNIST dataset might be used to differentiate numbers. For classifying numbers, signs will be located
where there is a colorful circle, box or background and therefore the location of the number on the camera 
image will be inputed into the MNIST classifier using machine learning algorithm to extract the needed 
information. Some other sensors maybe added for measuring the travel distance done by the robot.

Problems to solve:

* Detect the coloured paper
* Moving forward the Robot by avoiding going to the walls
* Reading the signs while driving the Robot
* Reaction time of the Robot while acquiring new information (Should decrease speed or should stop?)
* Switching between Red and Green light while navigating
* Communication between the camera and sensors to make a decision

Solutions:

* For avoiding the walls, the GoPiGo2 will be mounted with three ultrasonic sensors, 
  one in front and the two on the left and right side forming an angle of 120 degree 
  (between the left and right sensors). Furthermore, the front ultrasonic sensor will 
  provide the ability to the GoPiGo2 to detect obstacles in front while the USB Camera 
  to detect the signs.

* Signs to be used to guide the GoPiGo2 are: Turn Left, Turn Right, Straight Forward, 
  Speed, Stop and Distance. For the traffic lights, Red and Green light will be mostly used.
 
Tasks subdivision:

* Subtask A (Nihat Aliyev & Markus Erik Sügis)
	- Sign detection
	- Detection of traffic lights
* Subtask B (Perseverance Ngoy & Uku Ilves)
	- Driving logic
	- Avoiding driving to walls
* Collective subtask:
	- figure out the format for the communication between the two modules
	- implement the hardware solution and combine software

### Schedule ###

* Week 10
	- Project plan (8h, 2h long group meeting)
* Week 11
	- Constructing the maze (12h)
	- Making signs and traffic lights (12h)
	- Mounting the sensors to the robot (1h)
	- Traffic light/sign detection (10h)
	- Driving the robot in the maze(10h)
* Week 12
	- Driving avoiding walls (20h)
	- Driving the robot in the maze(10h)


* Week 13 (45h)
	- Combining the two modules
	- Figure out the communication
	- Debugging
	- Making the demo video
* Week 14 (40h)
	- Improving the solution
	- Improving the maze
	- Making the poster 
	- Preparing for the presentation
* Week 15 (10h)
	- Finishing up everything 
	- Try to add creative solution

* Week 16 - Presentation day (20h)
	- Minor fixing
	- Rehearsing the presentation

### Component list ###

| Item       | We will provide | Need from insturctors | Total |
| :----------------- |:-----------------: | :-----------------: | :-----------------: |
| GoPiGo2       | No      |   Yes    |    1     |
| HD WebCam     |    No      |   Yes   |     1   |
| Ultrasonic sensor |    Yes (1)    |   Yes(2)    |     3    |
| Battery        |   No       |    Yes      |   1 (per week)  |
| Glue and tape  |     No     |     Yes      |      2        |
| Cardboard boxes |     No       |    Yes     |      20       |
| Color papers  |   No        |     Yes     | Red, Green and Orange |


### Challenges and solutions ###

* Perseverance Munga Ngoy

	- improve the robot's turning 

	- improve data processing speed

	  Tried solutions: increase delay, increase speed for each wheel

	  Solutions: implement multithreading for different functionality

* Uku Ilves

	- implementing detections to the driving logic

	- add more turning conditions

	  Tried solutions: increase delay, increase speed

	  Solutions: using ultrasonic sensors for turning conditions

* Nihat Aliyev

	- implement another image detection function for detecting the traffic lights

	- create state machine for traffic light detection

	  Tried solutions: blob detector implementing

	  Solutions: OpenCV hough circle function

* Markus Erik Sügis

	- improve image processing speed

	- add additional signs with different functions

	  Tried solutions: decrease image resolution, defining RoI, trying out different sign designs

	  Solutions: implement multithreading for image processing


### Group members ###

* Perseverance Munga Ngoy

* Uku Ilves

* Nihat Aliyev

* Markus Erik Sügis


