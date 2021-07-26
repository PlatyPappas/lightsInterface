from rpi_ws281x import Color
import threading
import zmq
from library import lightController

#Will assume that commands are validated before receiving them
#One thread will listen to zmq publisher socket (main thread) and will 

if __name__ == '__main__':
  context = zmq.Context()
  socket = context.socket(zmq.SUB)
  socket.bind("tcp://10.0.0.73:%s" % "2555")
  lightControllerInstance = lightController.lightController()
  lightControllerInstance.colorWipe(Color(148, 0, 211))
  threading.Thread(target=lightControllerInstance.pulseBrightness, args=()).start()
  while True:
    command = socket.recv_string()
    args = command.split()
    parsedCommand = Color(int(args[0]), int(args[1]), int(args[2]))
    threading.Thread(target=lightControllerInstance.colorWipe, args=(parsedCommand,)).start()
