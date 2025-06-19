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
from building_energy_process import executeBuildingEnergySimulationProcess


TEST_INPUT_PATH = str(Path(__file__).parent / 'input_test.json')


# Test -> Final execution test
def test_finalExecution():
    '''
    Test -> Final execution test.
    Input parameters:
        None.
    '''

    exceptionsRaised = 0

    # Load the payload file
    with open(TEST_INPUT_PATH, 'r') as payloadFile:
        # Execute the process
        try:
            executeBuildingEnergySimulationProcess(json.load(
                payloadFile), '2019-03-01T13:00:00', '2019-03-02T13:00:00', 'Apartment Block')
        except:
            exceptionsRaised += 1

    assert exceptionsRaised == 0
