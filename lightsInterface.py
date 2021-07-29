import threading
import signal
import sys
import time
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

    self.colorThread = threading.Thread(target=self.colorThreadOperation, args=())
    self.modeThread = threading.Thread(target=self.modeThreadOperation, args=())
    self.pulseThread = threading.Thread(target=self.pulseThreadOperation, args=())
    self.brightnessThread = threading.Thread(target=self.brightnessThreadOperation, args=())

    self.colorContext = zmq.Context()
    self.colorSocket = self.colorContext.socket(zmq.SUB)

    self.modeContext = zmq.Context()
    self.modeSocket = self.modeContext.socket(zmq.SUB)

    self.pulseContext = zmq.Context()
    self.pulseSocket = self.pulseContext.socket(zmq.SUB)

    self.brightnessContext = zmq.Context()
    self.brightnessSocket = self.brightnessContext.socket(zmq.SUB)

    self.lightControllerShare = lightController.lightController()
  
  def startThreads(self):
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
    colorSocket = colorContext.socket(zmq.PUB)
    colorSocket.connect("tcp://127.0.0.1:%s" % "2555")
    colorSocket.send_string("0 0 0")

    modeContext = zmq.Context()
    modeSocket = modeContext.socket(zmq.PUB)
    modeSocket.connect("tcp://127.0.0.1:%s" % "2556")
    modeSocket.send_string("WIPE")

    pulseContext = zmq.Context()
    pulseSocket = pulseContext.socket(zmq.PUB)
    pulseSocket.connect("tcp://127.0.0.1:%s" % "2557")
    pulseSocket.send_string("FOO")

    brightnessContext = zmq.Context()
    brightnessSocket = brightnessContext.socket(zmq.PUB)
    brightnessSocket.connect("tcp://127.0.0.1:%s" % "2558")
    brightnessSocket.send_string("0")

    self.colorThread.join
    self.modeThread.join
    self.pulseThread.join
    self.brightnessThread.join
    sys.exit(0)

  def colorThreadOperation(self):
    self.colorSocket.bind("tcp://*:%s" % "2555")
    while self.colorThreadToggle:
      command = self.colorSocket.recv_string()
      args = command.split()
      threading.Thread(target=self.lightControllerShare.changeColor,args=(int(args[0]), int(args[1]), int(args[2]))).start()

  def modeThreadOperation(self):
    self.modeSocket.bind("tcp://*:%s" % "2556")
    while self.modeThreadToggle:
      command = self.modeSocket.recv_string()
      args = lightMode.lightChangeDict[command]
      self.lightControllerShare.changeMode(args)
  
  def pulseThreadOperation(self):
    self.pulseSocket.bind("tcp://*:%s" % "2557")
    while self.pulseThreadToggle:
      self.pulseSocket.recv_string()
      self.lightControllerShare.changePulse
      threading.Thread(target=self.lightControllerShare.pulseBrightness, args=()).start()
  
  def brightnessThreadOperation(self):
    self.brightnessSocket.bind("tcp://*:%s" % "2558")
    while self.brightnessThreadToggle:
      command = self.brightnessSocket.recv_string()
      threading.Thread(target=self.lightControllerShare.setBrightness, args=(int(command))).start()

if __name__ == '__main__':
  threadController = SupportThreadController()
  signal.signal(signal.SIGINT, threadController.signal_handler)
  threadController.startThreads
  while True:
    time.sleep(1000)
