import time
import signal
import sys
from rpi_ws281x import PixelStrip, Color

class lightController:
  def __init__(self):
    self.ledCount = 300
    self.ledPin = 18
    self.ledFreq = 800000
    self.ledDma = 10
    self.maxBrightness = 180
    self.minBrightness = 50
    self.invert = False
    self.ledChannel = 0
    self.strip = PixelStrip(self.ledCount, self.ledPin, self.ledFreq, self.ledDma, self.invert, self.minBrightness, self.ledChannel)
    self.strip.begin()
    signal.signal(signal.SIGINT, self.signal_handler)
  
  def colorWipe(self, chosenColor, wait_ms=10):
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, chosenColor)
      self.strip.show()
      time.sleep(wait_ms / 1000.0)

  def theaterChase(self, color, wait_ms=50, iterations=10):
    for j in range(iterations):
      for q in range(3):
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i + q, color)
        self.strip.show()
        time.sleep(wait_ms / 1000.0)
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i + q, 0)

  def wheel(self, pos):
    if pos < 85:
      return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
      pos -= 85
      return Color(255 - pos * 3, 0, pos * 3)
    else:
      pos -= 170
      return Color(0, pos * 3, 255 - pos * 3)

  def rainbow(self, wait_ms=20, iterations=1):
    for j in range(256 * iterations):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel((i + j) & 255))
      self.strip.show()
      time.sleep(wait_ms / 1000.0)

  def rainbowCycle(self, wait_ms=20, iterations=5):
    for j in range(256 * iterations):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
      self.strip.show()
      time.sleep(wait_ms / 1000.0)

  def theaterChaseRainbow(self, wait_ms=50):
    for j in range(256):
      for q in range(3):
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
        self.strip.show()
        time.sleep(wait_ms / 1000.0)
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i + q, 0)

  def pulseBrightness(self, wait_ms=10):
    while True:
      for i in range(self.minBrightness, self.maxBrightness):
        self.strip.setBrightness(i)
        self.strip.show()
        time.sleep(wait_ms / 1000.0)
      time.sleep(wait_ms / 1000.0)
      for i in range(self.maxBrightness, self.minBrightness, -1):
        self.strip.setBrightness(i)
        self.strip.show()
        time.sleep(wait_ms / 1000.0)
      time.sleep(wait_ms / 1000.0)

  def signal_handler(self, sig, frame):
    self.colorWipe(Color(0, 0, 0), 0)
    sys.exit(0)
