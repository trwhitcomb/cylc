#!/bin/bash
# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2019 NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
# Test poll intervals is used from both flow.rc and suite.rc
. "$(dirname "${0}")/test_header"
#-------------------------------------------------------------------------------
set_test_number 6
install_suite "${TEST_NAME_BASE}" "${TEST_NAME_BASE}"
#-------------------------------------------------------------------------------
run_ok "${TEST_NAME_BASE}-validate" cylc validate "${SUITE_NAME}"
create_test_globalrc '
[hosts]
   [[localhost]]
        task communication method = poll
        execution polling intervals = 10*PT6S
        submission polling intervals = 10*PT6S'

suite_run_ok "${TEST_NAME_BASE}-run" \
    cylc run --reference-test --debug --no-detach "${SUITE_NAME}"
#-------------------------------------------------------------------------------
TEST_NAME="${TEST_NAME_BASE}"
LOG_FILE="${SUITE_RUN_DIR}/log/suite/log"

PRE_MSG='-health check settings:'
POST_MSG='.*, polling intervals=10\*PT6S...'
for INDEX in 1 2; do
    for STAGE in 'submission' 'execution'; do
        grep_ok "\[t${INDEX}\.1\] ${PRE_MSG} ${STAGE}${POST_MSG}" "${LOG_FILE}"
    done
done
#-------------------------------------------------------------------------------
purge_suite "${SUITE_NAME}"
exit
