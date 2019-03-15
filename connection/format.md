# Plan for controller

## Software running on RPI
- Live Kernel for speed
- Wireless network
- Websocket server
- Quadcopter control

## Software running on computer
- Websocket client
- Remote control software
  - Some form of dashboard
  - Video feed?
- Video processing maybe?

## Websocket Communication format
- JSON data transfer
- Heartbeat protocol with auto-land when heartbeat is broken