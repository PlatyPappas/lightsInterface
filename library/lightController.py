import time
from .lightMode import lightChangeMode
from rpi_ws281x import PixelStrip, Color

class lightController:
  def __init__(self):
    self.mode = lightChangeMode.WIPE
    self.pulseOn = False
    self.currentRed = 0
    self.currentBlue = 0
    self.currentGreen = 0
    self.ledCount = 300
    self.ledPin = 18
    self.ledFreq = 800000
    self.ledDma = 10
    self.currentBrightness = 10
    self.desiredBrightness = 10
    self.maxBrightness = 180
    self.minBrightness = 1
    self.invert = False
    self.ledChannel = 0
    self.strip = PixelStrip(self.ledCount, self.ledPin, self.ledFreq, self.ledDma, self.invert, self.currentBrightness, self.ledChannel)
    self.strip.begin()
  
  def changeMode(self, newMode):
    self.mode = newMode
  
  def changePulse(self):
    self.pulseOn = not self.pulseOn
  
  def changeColor(self, red, green, blue):
    if (self.mode == lightChangeMode.WIPE):
      self.colorWipe(red, green, blue)
    elif (self.mode == lightChangeMode.FADE):
      self.colorFade(red, green, blue)
    else:
      self.colorFlow(red, green, blue)
  
  def colorWipe(self, red, green, blue, wait_ms=10):
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, Color(red, green, blue))
      self.strip.show()
      time.sleep(wait_ms / 1000.0)
    self.currentRed = red
    self.currentGreen = green
    self.currentBlue = blue
  
  def colorFade(self, red, green, blue, wait_ms=.1):
    formerBrightness = self.currentBrightness

    for i in range(self.currentBrightness, 0, -1):
      self.currentBrightness = i
      self.strip.setBrightness(i)
      self.strip.show()
      time.sleep(wait_ms / 1000.0)

    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, Color(red, green, blue))
    self.strip.show()
    time.sleep(wait_ms / 1000.0)

    for i in range(0, formerBrightness + 1):
      self.currentBrightness = i
      self.strip.setBrightness(i)
      self.strip.show()
      time.sleep(wait_ms / 1000.0)

    self.currentRed = red
    self.currentGreen = green
    self.currentBlue = blue
  
  def colorFlowFade(self, red, green, blue, wait_ms=1):
    formerRed = self.currentRed
    formerGreen = self.currentGreen
    formerBlue = self.currentBlue

    #Decrement our shit
    for i in range(formerRed, -1, -1):
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(i, self.currentGreen, self.currentBlue))
      self.currentRed = i
      self.strip.show() #show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)
    
    for i in range(formerGreen, -1, -1):
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, i, self.currentBlue))
      self.currentGreen = i
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)
    
    for i in range(formerBlue, -1, -1):
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, i))
      self.currentBlue = i
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)
    
    #Increment our shit
    for i in range(red + 1):
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(i, self.currentGreen, self.currentBlue))
      self.currentRed = i
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)
    
    for i in range(green + 1):
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, i, self.currentBlue))
      self.currentGreen = i
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)
    
    for i in range(blue + 1):
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, i))
      self.currentBlue = i
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)

  def colorFlow(self, red, green, blue, wait_ms=.05):
    while (self.currentRed < red):
      self.currentRed +=1
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, self.currentBlue))
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)
    
    while (self.currentRed > red):
      self.currentRed -= 1
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, self.currentBlue))
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)

    while (self.currentGreen < green):
      self.currentGreen += 1
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, self.currentBlue))
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)

    while (self.currentGreen > green):
      self.currentGreen -= 1
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, self.currentBlue))
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)
    
    while (self.currentBlue < blue):
      self.currentBlue += 1
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, self.currentBlue))
      self.strip.show()  # show after we set all of the pixels
      time.sleep(wait_ms / 1000.0)

    while (self.currentBlue > blue):
      self.currentBlue -= 1
      for j in range(self.strip.numPixels()):
        self.strip.setPixelColor(j, Color(self.currentRed, self.currentGreen, self.currentBlue))
      self.strip.show()  # show after we set all of the pixels
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
    while self.pulseOn:
      for i in range(self.minBrightness, self.maxBrightness):
        self.currentBrightness = i
        self.strip.setBrightness(i)
        self.strip.show()
        time.sleep(wait_ms / 1000.0)
      time.sleep(wait_ms / 1000.0)
      for i in range(self.maxBrightness, self.minBrightness, -1):
        self.currentBrightness = i
        self.strip.setBrightness(i)
        self.strip.show()
        time.sleep(wait_ms / 1000.0)
      time.sleep(wait_ms / 1000.0)
  
  def setBrightness(self, newBrightness, wait_ms=1):
    if not self.pulseOn and newBrightness <= 255 and newBrightness >= 0:
      self.desiredBrightness = newBrightness
      print(self.desiredBrightness)
      if self.desiredBrightness > self.currentBrightness:
        for i in range(self.currentBrightness, self.desiredBrightness + 1):
          self.currentBrightness = i
          self.strip.setBrightness(i)
          self.strip.show()
          time.sleep(wait_ms / 1000.0)
      else:
        for i in range(self.currentBrightness, self.desiredBrightness - 1, -1):
          self.currentBrightness = i
          self.strip.setBrightness(i)
          self.strip.show()
          time.sleep(wait_ms / 1000.0)
