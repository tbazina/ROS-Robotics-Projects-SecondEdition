#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from state_machine_examples_flexbe_states.example_transition_state import ExampleTransitionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Aug 16 2021
@author: Tomislav Bazina
'''
class TransitionBehaviorSM(Behavior):
	'''
	In this example, we have four states: A, B, C, and D. This example aims to transition from one state to another on reception of an output.
	'''


	def __init__(self):
		super(TransitionBehaviorSM, self).__init__()
		self.name = 'Transition Behavior'

		# parameters of this behavior
		self.add_parameter('num_transits', 10)
		self.add_parameter('transit_dir', 'cw')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:418, x:130 y:418
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.tot_transit = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:108 y:50
			OperatableStateMachine.add('A',
										ExampleTransitionState(num_transits=self.num_transits, transit_dir=self.transit_dir),
										transitions={'cw': 'B', 'ccw': 'D', 'done': 'finished'},
										autonomy={'cw': Autonomy.Off, 'ccw': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'input': 'tot_transit', 'output': 'tot_transit'})

			# x:462 y:44
			OperatableStateMachine.add('B',
										ExampleTransitionState(num_transits=self.num_transits, transit_dir=self.transit_dir),
										transitions={'cw': 'C', 'ccw': 'A', 'done': 'finished'},
										autonomy={'cw': Autonomy.Off, 'ccw': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'input': 'tot_transit', 'output': 'tot_transit'})

			# x:459 y:227
			OperatableStateMachine.add('C',
										ExampleTransitionState(num_transits=self.num_transits, transit_dir=self.transit_dir),
										transitions={'cw': 'D', 'ccw': 'B', 'done': 'finished'},
										autonomy={'cw': Autonomy.Off, 'ccw': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'input': 'tot_transit', 'output': 'tot_transit'})

			# x:108 y:222
			OperatableStateMachine.add('D',
										ExampleTransitionState(num_transits=self.num_transits, transit_dir=self.transit_dir),
										transitions={'cw': 'A', 'ccw': 'C', 'done': 'finished'},
										autonomy={'cw': Autonomy.Off, 'ccw': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'input': 'tot_transit', 'output': 'tot_transit'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
