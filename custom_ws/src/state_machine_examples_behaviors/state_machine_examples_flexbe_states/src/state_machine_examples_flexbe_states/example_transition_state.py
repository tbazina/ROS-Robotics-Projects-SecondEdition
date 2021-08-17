#!/usr/bin/env python
import rospy
from flexbe_core import EventState, Logger


class ExampleTransitionState(EventState):
    '''
    Implements a state that allows transition to another state based on input.
    num_transits number of state transits before finish.
    input from userdata 1 - clockwise, else - counterclockwise.
    output total number of transits finished

    -- num_transits int   Max. number of transits to perform. 
    -- transit_dir  str   cw for clockwise, ccw for counterclockwise.
    ># input        int		Total number of transits finished in previous state.
    #> output       int		Total number of transits finished after this state.
    <= 'cw'					      Transit in clockwise direction.
    <= 'ccw'					    Transit in counterclockwise direction.
    <= done
    '''
    def __init__(self, num_transits, transit_dir):
      super().__init__(
        input_keys=['input'], output_keys=['output'], outcomes=['cw', 'ccw', 'done']
      )
      self._compl_transits = None
      try:
        self._num_transits = int(num_transits)
      except Exception as e:
        Logger.logwarn('Please enter integer as max. number of transits')

      try:
        self._transit_dir = str(transit_dir)
        if self._transit_dir not in ['cw', 'ccw']:
          raise
      except Exception as e:
        Logger.logwarn(
          "Please enter 'cw' for clockwise direction and 'ccw' for"
          "counterclockwise direction: {}".format(e)
          )

    def execute(self, userdata):
      userdata.output = self._compl_transits
      # return transition value
      if self._compl_transits >= self._num_transits:
        return 'done'
      else:
        return self._transit_dir

    def on_enter(self, userdata):
      rospy.sleep(1)
      try:
        self._compl_transits = int(userdata.input) + 1
        Logger.loginfo('Completed transits: {}'.format(self._compl_transits))
      except Exception as e:
        Logger.logwarn('Failed to calculate total transits: {}'.format(e))
