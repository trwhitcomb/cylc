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
# Test suite shuts down with error on missing port file
. "$(dirname "$0")/test_header"
set_test_number 3
install_suite "${TEST_NAME_BASE}" "${TEST_NAME_BASE}"

OPT_SET=
if [[ "${TEST_NAME_BASE}" == *-globalcfg ]]; then
    create_test_globalrc "" "
[cylc]
    health check interval = PT10S"
    OPT_SET='-s GLOBALCFG=True'
fi

run_ok "${TEST_NAME_BASE}-validate" cylc validate ${OPT_SET} "${SUITE_NAME}"
# Suite run directory is now a symbolic link, so we can easily delete it.
SYM_SUITE_RUND="${SUITE_RUN_DIR}-sym"
SYM_SUITE_NAME="${SUITE_NAME}-sym"
ln -s "$(basename "${SUITE_NAME}")" "${SYM_SUITE_RUND}"
suite_run_fail "${TEST_NAME_BASE}-run" \
    cylc run --no-detach ${OPT_SET} "${SYM_SUITE_NAME}"
grep_ok "No such file or directory: '${SYM_SUITE_RUND}'" \
    "${SUITE_RUN_DIR}/log/suite/log".*

rm -f "${SYM_SUITE_RUND}"
purge_suite "${SUITE_NAME}"
exit
