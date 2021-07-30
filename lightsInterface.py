import threading
import sys
import signal
import zmq
from library import lightController, lightMode

#Will assume that commands are validated before receiving them
#One thread will listen to zmq publisher socket (main thread) and will 

class SupportThreadController:
  def __init__(self):
    self.colorThreadToggle = True
    self.modeThreadToggle = True
    self.pulseThreadToggle = True
    self.brightnessThreadToggle = True

    self.colorThread = threading.Thread(target=self.colorThreadOperation)
    self.modeThread = threading.Thread(target=self.modeThreadOperation)
    self.pulseThread = threading.Thread(target=self.pulseThreadOperation)
    self.brightnessThread = threading.Thread(target=self.brightnessThreadOperation)
    print("Threads assigned")

    self.colorContext = zmq.Context()
    self.colorSocket = self.colorContext.socket(zmq.REP)

    self.modeContext = zmq.Context()
    self.modeSocket = self.modeContext.socket(zmq.REP)

    self.pulseContext = zmq.Context()
    self.pulseSocket = self.pulseContext.socket(zmq.REP)

    self.brightnessContext = zmq.Context()
    self.brightnessSocket = self.brightnessContext.socket(zmq.REP)
    print("Sockets assigned")

    self.lightControllerShare = lightController.lightController()
    print("Lights made")
  
  def startThreads(self):
    print("Starting threads...")
    self.colorThread.start
    self.modeThread.start
    self.pulseThread.start
    self.brightnessThread.start
  
  def signal_handler(self, sig, frame):
    #switch off
    self.colorThreadToggle = False
    self.modeThreadToggle = False
    self.pulseThreadToggle = False
    self.brightnessThreadToggle = False

    colorContext = zmq.Context()
    colorSocket = colorContext.socket(zmq.REQ)
    colorSocket.connect("tcp://127.0.0.1:%s" % "2555")
    colorSocket.send_string("0 0 0")

    modeContext = zmq.Context()
    modeSocket = modeContext.socket(zmq.REQ)
    modeSocket.connect("tcp://127.0.0.1:%s" % "2556")
    modeSocket.send_string("WIPE")

    pulseContext = zmq.Context()
    pulseSocket = pulseContext.socket(zmq.REQ)
    pulseSocket.connect("tcp://127.0.0.1:%s" % "2557")
    pulseSocket.send_string("FOO")

    brightnessContext = zmq.Context()
    brightnessSocket = brightnessContext.socket(zmq.REQ)
    brightnessSocket.connect("tcp://127.0.0.1:%s" % "2558")
    brightnessSocket.send_string("0")

    self.colorThread.join
    self.modeThread.join
    self.pulseThread.join
    self.brightnessThread.join
    sys.exit(0)

  def colorThreadOperation(self):
    print("Color thread started")
    self.colorSocket.bind("tcp://*:%s" % "2555")
    while self.colorThreadToggle:
      command = self.colorSocket.recv_string()
      print(command)
      args = command.split()
      threading.Thread(target=self.lightControllerShare.changeColor,args=(int(args[0]), int(args[1]), int(args[2]))).start()
      self.colorSocket.send_string("Color OK")
    print("Color thread exiting")

  def modeThreadOperation(self):
    print("Mode thread started")
    self.modeSocket.bind("tcp://*:%s" % "2556")
    while self.modeThreadToggle:
      command = self.modeSocket.recv_string()
      args = lightMode.lightChangeDict[command]
      self.lightControllerShare.changeMode(args)
      self.modeSocket.send_string("Mode OK")
    print("Mode thread exiting")
  
  def pulseThreadOperation(self):
    print("Pulse thread started")
    self.pulseSocket.bind("tcp://*:%s" % "2557")
    while self.pulseThreadToggle:
      self.pulseSocket.recv_string()
      self.lightControllerShare.changePulse
      threading.Thread(target=self.lightControllerShare.pulseBrightness, args=()).start()
      self.pulseSocket.send_string("Pulse OK")
    print("Pulse thread exiting")
  
  def brightnessThreadOperation(self):
    print("Brightness thread started")
    self.brightnessSocket.bind("tcp://*:%s" % "2558")
    while self.brightnessThreadToggle:
      command = self.brightnessSocket.recv_string()
      threading.Thread(target=self.lightControllerShare.setBrightness, args=(int(command))).start()
      self.brightnessSocket.send_string("Brightness OK")
    print("Brightness thread exiting")

if __name__ == '__main__':
  threadController = SupportThreadController()
  threadController.startThreads()
  signal.signal(signal.SIGINT, threadController.signal_handler)
  while True:
    pass
