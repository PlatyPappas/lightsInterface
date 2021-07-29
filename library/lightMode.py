from enum import Enum

class lightChangeMode(Enum):
  WIPE = 1
  FADE = 2
  FLOW = 3

lightChangeDict = {
  "WIPE": lightChangeMode.WIPE,
  "FADE": lightChangeMode.FADE,
  "FLOW": lightChangeMode.FLOW
}