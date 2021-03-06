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

set -u

usage() {
  cat <<eof
Usage: run-functional-tests.sh [...]

Run the Cylc test battery, in <CYLC_REPO_DIR>/tests.

Options and arguments are appended to "prove -j \$NPROC -s -r \${@:-tests}".
NPROC is the number of concurrent processes to run, which defaults to the
global config "process pool size" setting.

The tests ignore normal site/user global config and instead use the file:
   \$CYLC_REPO_DIR/tests/global-tests.rc
This should specify test job hosts under the [test battery] section, plus any
other critical settings settings, including [hosts] configuration for test job
hosts (and special batchview commands like qcat if available). Additional
global config items can be added on the fly using the create_test_globalrc
shell function defined in the test_header.

Suite run directories are only cleaned up for passing tests on the suite host.

Set "export CYLC_TEST_DEBUG=true" to print failed-test stderr to the terminal.

To change the test file comparision command from "diff -u" do (for example):
   export CYLC_TEST_DIFF_CMD='xxdiff -D'

Some test suites submit jobs to the 'at' so atd must be up on the job hosts.

Commits or Pull Requests to cylc/cylc-flow on GitHub will trigger Travis CI to
run generic (non platform-specific) tests - see .travis.yml.

By default all tests are executed.  To run just a subset of them:
  * list individual tests or test directories to run on the command line
  * list individual tests or test directories to skip in \$CYLC_TEST_SKIP
  * skip all generic tests with CYLC_TEST_RUN_GENERIC=false
  * skip all platform-specific tests with CYLC_TEST_RUN_PLATFORM=false
  List specific tests relative to \$CYLC_REPO_DIR (i.e. starting with "test/").
Some platform-specific tests are automatically skipped, depending on platform.

Platform-specific tests must set "CYLC_TEST_IS_GENERIC=false" before sourcing
the test_header.

Tests requiring the sqlite3 CLI must be skipped if sqlite3 is not installed (it
is not otherwise a Cylc software prerequisite):
| if ! which sqlite3 > /dev/null; then
|     # Skip the remaining 3 tests.
|     skip 3 "sqlite3 not installed?"
|     purge_suite \$SUITE_NAME
|     exit 0
| fi

Options:
  -h, --help       Print this help message and exit.

Examples:

Run the full test suite with the default options.
  run-functional-tests.sh
Run the full test suite with 12 processes
  run-functional-tests.sh -j 12
Run only tests under "tests/cyclers/"
  run-functional-tests.sh tests/cyclers
Run only "tests/cyclers/16-weekly.t" in verbose mode
  run-functional-tests.sh -v tests/cyclers/16-weekly.t
Run only tests under "tests/cyclers/", and skip 00-daily.t
  export CYLC_TEST_SKIP=tests/cyclers/00-daily.t
  run-functional-tests.sh tests/cyclers
Run the first quarter of the test battery
  CHUNK=1/4 run-functional-tests.sh
Re-run failed tests
  run-functional-tests.sh --state=save
  run-functional-tests.sh --state=failed
eof
}
for ARG in "$@"; do
    case "${ARG}" in
        --help|-h)
            usage
            exit 0
            ;;
    esac
done

# (Should be the same as $TRAVIS_BUILD_DIR, on Travis CI)
cd "$(dirname "$0")/../.." || exit 1
export CYLC_REPO_DIR="${PWD}"
# Defaults
export CYLC_TEST_RUN_GENERIC=${CYLC_TEST_RUN_GENERIC:-true}
export CYLC_TEST_RUN_PLATFORM=${CYLC_TEST_RUN_PLATFORM:-true}
export CYLC_TEST_SKIP=${CYLC_TEST_SKIP:-}
export CYLC_TEST_IS_GENERIC=true
CYLC_TEST_TIME_INIT="$(date -u +'%Y%m%dT%H%M%SZ')"
export CYLC_TEST_TIME_INIT
# Normal run
NPROC=$(cylc get-global-config '--item=process pool size')
if [[ -z "${NPROC}" ]]; then
    NPROC=$(python3 -c 'import multiprocessing as mp; print(mp.cpu_count())')
fi
if [[ -n "${CHUNK:-}" ]]; then
    exec env -u 'CHUNK' prove --timer -j "${NPROC}" -s -r "$@" - \
        < <(prove --dry --recurse './tests' | sort | split -n "r/${CHUNK}")
else
    exec prove --timer -j "${NPROC}" -s -r "$@"
fi
