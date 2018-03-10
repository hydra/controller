#!/usr/bin/env python3
'''
Layers test case for Host-side KLL
'''

# Copyright (C) 2018 by Jacob Alexander
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

### Imports ###

import itertools
import logging
import os

import interface as i
import kiilogger

from common import (
    check,
    fail_tests,
    header,
    pass_tests,
    result,
    EvalBase,
    KLLTest,
    KLLTestUnitResult,
    KLLTestRunner,
    TriggerResultEval,
)



### Classes ###

class LayerRotationEval(EvalBase):
    '''
    Evaluates a Layer Rotation
    '''
    def __init__(self, parent, layers):
        '''
        Constructor

        @param parent:     Parent object
        @param layers:     JSON layer information
        '''
        EvalBase.__init__(self, parent)
        self.layers = layers

        # Prepare info line
        self.info = "0 -> {}".format(len(self.layers))

    def run(self):
        '''
        Evaluate/run layer test

        @return: True if successful, False if not
        '''
        # Rotate right from 0 to max, then to 0
        # Making sure we hit each layer
        # TODO
        print('right')

        # Cleanup
        self.clean()

        # Rotate left from max to 0, starting at 0
        # Making sure we hit each layer
        # TODO
        print('left')

        # Cleanup
        self.clean()
        return True

    def clean(self):
        '''
        Cleanup between tests
        '''
        # Clear layers
        i.control.cmd('clearLayers')()


class LayerActionEval(EvalBase):
    '''
    Takes a given layer action (list of layer actions) does that action.
    Then attempts all the responses for the given action to resolve it.

    For example:
    shift, lock -> shift, lock
    shift, lock -> lock, shift
    '''
    def __init__(self, parent, action):
        '''
        Constructor

        @param parent:     Parent object
        @param action:     List of layer actions
        '''
        EvalBase.__init__(self, parent)
        self.action = action

        # Prepare info line
        self.info = str(self.action)

    def run_action(self, action):
        '''
        Process and monitor action

        @param action: Commands to run
        '''
        # TODO
        pass

    def run(self):
        '''
        Run layer action evaluation.

        Checks:
        1) Action was successful
        2) Response was successful

        @return: True if successful, False otherwise.
        '''
        # Permutate action
        for permuation in itertools.permutations(self.action):
            # Process action
            # TODO handle return
            self.run_action(self.action)

            # TODO handle return
            self.run_action(permuation)

            # Cleanup after test
            self.clean()
        return True

    def clean(self):
        '''
        Cleanup between tests
        '''
        # Clear layers
        i.control.cmd('clearLayers')()


class LayerTest(KLLTest):
    '''
    Layer Test

    Using each of the defined layers, apply a complete permutation of layer activates/deactivates.
    * Shift
    * Latch
    * Lock

    Use combinations of Shift, Latch and Lock using both combinations and sequences.

    A rotation test is also done using all the layers.

    This test is looking for layer functionality correctness.
    '''
    def prepare(self):
        '''
        Prepare to run test

        Does necessary initialization before attempting to run.
        Must be done before run.

        @return: True if ready to run test, False otherwise
        '''
        # Prepare layer action permutations
        layer_actions3 = ['shift', 'latch', 'lock']
        layer_actions2a = ['shift', 'latch']
        layer_actions2b = ['shift', 'lock']
        layer_actions2c = ['shift', 'lock']
        layer_actions1 = [('shift',), ('latch',), ('lock',)]

        layer_permutations = []
        layer_permutations.extend(itertools.permutations(layer_actions3))
        layer_permutations.extend(itertools.permutations(layer_actions2a))
        layer_permutations.extend(itertools.permutations(layer_actions2b))
        layer_permutations.extend(itertools.permutations(layer_actions2c))
        layer_permutations.extend(layer_actions1)

        # Per layer action, add a LayerActionEval
        for action in layer_permutations:
            testresult = KLLTestUnitResult(self, None, LayerActionEval(self, action), 0)
            self.testresults.append(testresult)

        # Layer Rotation Test
        testresult = KLLTestUnitResult(self, None, LayerRotationEval(self, self.klljson['Layers']), 0)
        self.testresults.append(testresult)

        return True



### Setup ###

# Logger (current file and parent directory only)
logger = kiilogger.get_logger(os.path.join(os.path.split(__file__)[0], os.path.basename(__file__)))
logging.root.setLevel(logging.INFO)


# Reference to callback datastructure
data = i.control.data

# Enabled macro debug mode - Enabled USB Output, show debug
i.control.cmd('setMacroDebugMode')( 2 )

# Enabled vote debug mode
i.control.cmd('setVoteDebugMode')( 1 )

# Enable layer debug mode
i.control.cmd('setLayerDebugMode')(1)

# Enable pending trigger debug mode
i.control.cmd('setTriggerPendingDebugMode')(1)

# Enable output module debug mode
i.control.cmd('setOutputDebugMode')(2)



### Test ###

testrunner = KLLTestRunner([
    LayerTest(),
    #LayerTest(tests=1, test=3),
])
testrunner.run()

# Results of test
result()

