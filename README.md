# BHS Aeronautics
Source code for Bell High School Aeronautics projects

Developer: Matthew Haines

## What is inside
### Quadcopter
- This is the source code for a custom made quadcopter. We were kindly provided with a variety of quadcopter parts thanks to our sponsor, Hobbyking. 
- The quadcopter is controlled by a Raspberry Pi Model 3B that is running the software in this repository. 
- Software running on Raspberry Pi:
  - Wireless Network allowing for communication between laptop client and RPi server.
  - WebSocket Server for low-latency Server-Client Communication.
  - Autonomous and Manual Control Software.
### Control Software
- Abstraction of low level motor control and sensor input.
- PID Controller for heading, allowing for stable flight.
- I learned about Euler Angles and Rotation matrices to switch between reference frames.
### Simulation Software
- Made a quadcopter dynamics simulation environment for OpenAI Gym. Physics courtesy of [Andrew Gibianksy's Blog](http://andrew.gibiansky.com/downloads/pdf/Quadcopter%20Dynamics,%20Simulation,%20and%20Control.pdf).
- Allows for preliminary training and comparison of control model performance and experimentation in Control Theory. 
### Clientside
- App based on Electron Framework.
- Simple control interface.
- Fast communication with WebSocket Server on Raspberry Pi.
- Run on laptop connected to wireless network running off of RPi

## Future Plans
- Figure out how to calculate velocity and position somewhat accurately.
- Add a camera
  - Could possibly help with auto-hover because integrating acceleration twice gives **a lot** of error.
  - With a compute stick I could make an implementation of YOLO algorithm for object recognition.
- Add a GPS
  - More intelligent path planning.
