# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (c) 2025 Tecnalia Research & Innovation

import json
from pathlib import Path
from pv_power_plants import executePVPowerPlantsProcess


TEST_INPUT_PATH = str(Path(__file__).parent / 'input_test.json')


# Test -> First execution test for process
def test_firstExecutionForProcess():
    '''
    Test -> First execution test for process. The area, power and capex are null.
    Input parameters:
        None.
    '''

    exceptionsRaised = 0

    # Load the payload file
    with open(TEST_INPUT_PATH, 'r') as payloadFile:
        # Execute the process
        try:
            payload = json.load(payloadFile)
            payload['area_total_thermal'] = None
            payload['power_thermal'] = None
            payload['capex_thermal'] = None
            payload['area_total_pv'] = None
            payload['power_pv'] = None
            payload['capex_pv'] = None
            executePVPowerPlantsProcess(
                payload, '2019-03-01T13:00:00', '2019-03-02T13:00:00')
        except:
            exceptionsRaised += 1

    assert exceptionsRaised == 0


# Test -> Second execution test for process
def test_secondExecutionForProcess():
    '''
    Test -> Second execution test for process. At least one of the area, power and
            capex values ​​is not null.
    Input parameters:
        None.
    '''

    exceptionsRaised = 0

    # Load the payload file
    with open(TEST_INPUT_PATH, 'r') as payloadFile:
        # Execute the process
        try:
            executePVPowerPlantsProcess(
                json.load(payloadFile), '2019-03-01T13:00:00', '2019-03-02T13:00:00')
        except:
            exceptionsRaised += 1

    assert exceptionsRaised == 0
