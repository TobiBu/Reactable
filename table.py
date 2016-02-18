import tuio
import numpy as np
from pyo import *
import time

#class Oscillator:
#  '''simple oscillator class for different periodical functions'''
#  def __init__(self, freq=1000, phase=0, mul=1, add=0, typ='Sine'):
#    self._freq = freq
#    self._phase = phase
#    self._mul = mul
#    self._add = add
#    self._typ = typ
#    if typ == 'Sine':
#      self._object = Sine(freq, phase, mul).out
#    else:
#      self._object = Sine(freq, phase, mul)#

#  def set_Freq(self,freq):
#    self._freq = freq
#  def set_Phase(self,phase):
#    self._phase = phase
#  def set_type(self,typ):
#    self._typ = typ
#    if typ == 'Sine':
#      self._object = Sine(freq, phase, mul)
#    else:
#      self._object = Sine(freq, phase, mul)
#  def output(self):
#    return self._object.out()#

class Controller(LFO):
  """simple LFO controller class for different periodical functions

    Band-limited Low Frequency Oscillator with different wave shapes.

    :Parent: :py:class:`PyoObject`

    :Args:

        freq : float or PyoObject, optional
            Oscillator frequency in cycles per second. Defaults to 100.
        sharp : float or PyoObject, optional
            Sharpness factor between 0 and 1. Sharper waveform results
            in more harmonics in the spectrum. Defaults to 0.5.
        type : int, optional
            Waveform type. eight possible values :
                0. Saw up (default)
                1. Saw down
                2. Square
                3. Triangle
                4. Pulse
                5. Bipolar pulse
                6. Sample and hold
                7. Modulated Sine

    >>> s = Server().boot()
    >>> s.start()
    >>> lf = Sine([.31,.34], mul=15, add=20)
    >>> lf2 = LFO([.43,.41], sharp=.7, type=2, mul=.4, add=.4)
    >>> a = LFO(freq=lf, sharp=lf2, type=7, mul=100, add=300)
    >>> b = SineLoop(freq=a, feedback=0.12, mul=.2).out()

    """
  def __init__(self, tuio_obj, freq=440, sharp=0.5, typ='Sine', mul=1, add=0, n=0):
    self.tuio_obj = tuio_obj
    self._n = n
    self._orientation = tuio_obj.angle
    #function to get the rotation angle relative to initial position, also for the number of rotations saved in n
    #function or equation to get frequency from rotation angle
    if typ == 'Sine':
      self._type = 7
    elif typ == 'Sawtooth':
      self._type = 0
    else:
      self._type = 1
    super(self.__class__, self).__init__(self, freq=freq, sharp=sharp, type=self._type, mul=mul, add=add)
    #
  def set_Freq(self,freq):
    """
        Replace the `freq` attribute.

        :Args:

            x : float or PyoObject
                New `freq` attribute, in cycles per seconds.

        """
    super(self.__class__, self).setFreq(self, freq)

  def setSharp(self,sharp):
    """
        Replace the `sharp` attribute.

        :Args:

            x : float or PyoObject
                New `sharp` attribute, in the range 0 -> 1.

        """
    super(self.__class__, self).setSharp(self, sharp)

  def set_type(self,typ):
    """
        Replace the `type` attribute.

        :Args:

            x : string
                New `type` attribute. Choices are :
                    0. Saw up
                    1. Saw down
                    2. Square
                    3. Triangle
                    4. Pulse
                    5. Bipolar pulse
                    6. Sample and hold
                    7. Modulated Sine


        """
    self._typ = typ
    if typ == 'Sine':
      self._type = 7
    elif typ == 'Sawtooth up':
      self._type = 0
    elif typ == 'Sawtooth down':
      self._type = 1
    elif typ == 'Square':
      self._type = 2
    elif typ == 'Triangle':
      self._type = 3
    elif typ == 'Pulse':
      self._type = 4
    elif typ == 'Bipolar pulse':
      self._type = 5
    elif typ == 'Sample and hold':
      self._type = 6
    else:
      print "Unrecognized type keyword!"
      print "Please use only the following keywords:"
      print "Choices are :"
      print "   0. Saw up"
      print "   1. Saw down"
      print "   2. Square"
      print "   3. Triangle"
      print "   4. Pulse"
      print "   5. Bipolar pulse"
      print "   6. Sample and hold"
      print "   7. Modulated Sine"
      self._type = 7
    super(self.__class__, self).setType(self, self._type):
  def reset(self):
    """
    Resets current phase to 0.

    """
    super(self.__class__, self).reset(self)
  def ctrl(self, map_list=None, title=None, wxnoserver=False):
    super(self.__class__, self).ctrl(self, map_list=None, title=None, wxnoserver=False)     
  #def output(self):
  #  return self._object.out()

def output(obj):
  return obj.out()

def get_id(obj):
  return obj.id

def update():
  #function to update the all parameters like frequency etc. from the tuio position

def map_object(obj):
  if get_id(obj) < 4:
    a = Controller(tuio_obj=obj)#LFO(freq=100)
    return a
  if 4 <= get_id(obj) < 10:
    b = Sine(freq=440)
    return b
  else:
    pass

def get_new_obj(new,old):
  return new[np.logical_not(np.in1d(new, old))]

def get_alive_obj(new,old):
  return new[np.in1d(new, old)]

def get_dead_obj(new,old):
  return old[np.logical_not(np.in1d(old, new))]

tracking = tuio.Tracking()
print "loaded profiles:", tracking.profiles.keys()
print "list functions to access tracked objects:", tracking.get_helpers()

s = Server().boot()
s.start()
objects_old = np.empty((0))
objects_new = np.empty((0))
objects_new_id = np.empty((0))
sound_objects = np.asarray([])
tuio_objects = np.asarray([])
print sound_objects
print tuio_objects
try:
    while 1:
        tracking.update()
        #print tracking.objects()
        objects_new = np.asarray([obj for obj in tracking.objects()])
        #print objects_new
        #objects_new_id = map(get_id,objects_new)
        #print objects_new_id

        if not np.array_equal(objects_new,objects_old):
          new = get_new_obj(objects_new,objects_old)
          alive = get_alive_obj(objects_new,objects_old)
          dead = get_dead_obj(objects_new,objects_old)
          print 'new: ' +str(new)
          print 'alive: ' +str(alive)
          print 'dead: ' +str(dead)
          #time.sleep(2)
          
          mask = np.in1d(tuio_objects,dead,invert=True)
          sound_objects = sound_objects[mask]
          tuio_objects = tuio_objects[mask]
          tuio_objects = np.append(tuio_objects,new)
          sound_objects = np.append(sound_objects,map(output,map(map_object,new)))
          #print sound_objects
          #print tuio_objects
          #for tuObj, soObj in zip(tuio_objects, sound_objects):
          #  soObj.set_Freq
          
          

        #for obj in objects_new:
        #  if not obj in objects_old:

        objects_old = objects_new
        objects_old_id = objects_new_id
       	    
except KeyboardInterrupt:
    tracking.stop()


