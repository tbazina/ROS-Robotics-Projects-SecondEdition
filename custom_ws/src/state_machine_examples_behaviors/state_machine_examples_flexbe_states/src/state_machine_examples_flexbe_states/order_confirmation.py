#!/usr/bin/env python
import rospy
from flexbe_core import EventState, Logger

class OrderConfirmation(EventState):
  '''
  Implements a state that reads a button state.
  If the button state is high, state is set to succeeded, else aborted.

  -- button_state int   1 - button high
  <= succeeded
  '''
  def __init__(self, button_state):
    super().__init__(self, outcomes=['succeeded', 'aborted'])
    self._button_state = button_state
  
  def execute(self, userdata):
    if self._button_state == 1:
      return 'succeeded'
    else:
      return 'aborted'