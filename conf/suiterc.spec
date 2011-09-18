#C: THIS FILE IS PART OF THE CYLC FORECAST SUITE METASCHEDULER.
#C: Copyright (C) 2008-2011 Hilary Oliver, NIWA
#C: 
#C: This program is free software: you can redistribute it and/or modify
#C: it under the terms of the GNU General Public License as published by
#C: the Free Software Foundation, either version 3 of the License, or
#C: (at your option) any later version.
#C:
#C: This program is distributed in the hope that it will be useful,
#C: but WITHOUT ANY WARRANTY; without even the implied warranty of
#C: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#C: GNU General Public License for more details.
#C:
#C: You should have received a copy of the GNU General Public License
#C: along with this program.  If not, see <http://www.gnu.org/licenses/>.

#_______________________________________________________________________
#            THIS IS THE CYLC SUITE.RC SPECIFICATION FILE
#-----------------------------------------------------------------------
# Entries are documented in suite.rc reference in the Cylc User Guide. 

# _________________________________________________________MAIN SECTIONS
# [cylc]          - how cylc itself behaves when running this suite.
# [scheduling]    - items affecting when a task is deemed ready to run.
# [runtime]       - what to execute (and how) when a task is ready.
# [visualization] - for suite graphing and the graph-based control GUI.

#_______________________________________________________________________
# WARNING: a CONFIGOBJ or VALIDATE bug? list constructor fails if final
# element is followed by a space (or does it just need a trailing comma?):
#   GOOD: foo = string_list( default=list('foo','bar'))
#   BAD:  bar = string_list( default=list('foo','bar' ))

#___________________________________________________________________HEAD
title = string( default="No title supplied" )
description = string( default="No description supplied" )
#___________________________________________________________________CYLC
[cylc]
    UTC mode = boolean( default=False )
    simulation mode only = boolean( default=False )
    use secure passphrase = boolean( default=False )
    [[logging]]
        directory = string( default = string( default='$HOME/cylc-run/$CYLC_SUITE_REG_NAME/log/suite' )
        roll over at start-up = boolean( default=True )
    [[state dumps]]
        directory = string( default = string( default='$HOME/cylc-run/$CYLC_SUITE_REG_NAME/state' )
        number of backups = integer( min=1, default=10 )
    [[lockserver]]
        enable = boolean( default=False )
        allow multiple simultaneous suite instances = boolean( default=False )
    [[environment]]
        __many__ = string
    [[simulation mode]]
        clock offset from initial cycle time in hours = integer( default=24 )
        clock rate in seconds per simulation hour = integer( default=10 )
        command scripting = force_list( default=list( "echo SIMULATION MODE $TASK_ID; sleep 10; echo BYE",))
        job submission method = option( at_now, background, loadleveler, ll_ecox, ll_raw, ll_raw_ecox, default=background )
#_____________________________________________________________SCHEDULING
[scheduling]
    initial cycle time = integer( default=None )
    final cycle time = integer( default=None )
    runahead limit in hours = integer( min=0, default=24 )
    [[special tasks]]
        clock-triggered = force_list( default=list())
        start-up = force_list( default=list())
        cold-start = force_list( default=list())
        sequential = force_list( default=list())
        one-off = force_list( default=list())
        explicit restart outputs = force_list( default=list())
        exclude at start-up = force_list( default=list())
        include at start-up = force_list( default=list())
    [[dependencies]]
        graph = string( default=None )
        [[[__many__]]]
            graph = string( default=None )
            daemon = string( default=None )
#________________________________________________________________RUNTIME
[runtime]
    [[root]]
        inherit = string( default=None )
        description = string( default="No description supplied" )
        command scripting = force_list( default=list( "echo THIS is the root DUMMY command for $TASK_ID; sleep 10",))
        pre-command scripting = string( default=None )
        post-command scripting = string( default=None )
        manual task completion messaging = boolean( default=False )
        hours = force_list( default=list())
        extra log files = force_list( default=list())
        [[[job submission]]]
            method = option( at_now, background, loadleveler, ll_ecox, ll_raw, ll_raw_ecox, default=background )
            command template = string( default=None )
            job script shell = option( /bin/bash, /usr/bin/bash, /bin/ksh, /usr/bin/ksh, default=/bin/bash )
            log directory = string( default='$HOME/cylc-run/$CYLC_SUITE_REG_NAME/log/job' )
        [[[remote]]]
            host = string( default=None )
            owner = string( default=None )
            cylc directory = string( default=None )
            suite definition directory = string( default=None )
            remote shell template = string( default='ssh -oBatchMode=yes %s' )
            log directory = string( default=None )
        [[[task event hook scripts]]]
            submitted = string( default=None )
            submission failed = string( default=None )
            started = string( default=None )
            succeeded = string( default=None )
            failed = string( default=None )
            warning = string( default=None )
            timeout = string( default=None )
            submission timeout in minutes = float( default=None )
            execution timeout in minutes = float( default=None )
            reset execution timeout on incoming messages = boolean( default=False )
        [[[environment]]]
            __many__ = string
        [[[directives]]]
            __many__ = string
        [[[outputs]]]
            __many__ = string

    [[__many__]]
        inherit = string( default=root )
        description = string( default=None )
        command scripting = force_list( default=None )
        pre-command scripting = string( default=None )
        post-command scripting = string( default=None )
        manual task completion messaging = boolean( default=None )
        hours = force_list( default=list())
        extra log files = force_list( default=list())
        [[[job submission]]]
            method = option( at_now, background, loadleveler, ll_ecox, ll_raw, ll_raw_ecox, default=None )
            command template = string( default=None )
            job script shell = option( /bin/bash, /usr/bin/bash, /bin/ksh, /usr/bin/ksh, default=None )
            log directory = string( default=None )
        [[[remote]]]
            host = string( default=None )
            owner = string( default=None )
            cylc directory = string( default=None )
            suite definition directory = string( default=None )
            remote shell template = string( default=None )
            log directory = string( default=None )
        [[[task event hook scripts]]]
            submitted = string( default=None )
            submission failed = string( default=None )
            started = string( default=None )
            succeeded = string( default=None )
            failed = string( default=None )
            warning = string( default=None )
            timeout = string( default=None )
            submission timeout in minutes = float( default=None )
            execution timeout in minutes = float( default=None )
            reset task execution timeout on incoming messages = boolean( default=None )
        [[[environment]]]
            __many__ = string
        [[[directives]]]
            __many__ = string
        [[[outputs]]]
            __many__ = string
#__________________________________________________________VISUALIZATION
[visualization]
    initial cycle time = integer( default=2999010100 )
    final cycle time = integer( default=2999010123 )
    collapsed families = force_list( default=list() )
    use node color for edges = boolean( default=True )
    default node attributes = force_list( default=list('style=unfilled', 'color=black', 'shape=box'))
    default edge attributes = force_list( default=list('color=black'))
    [[node groups]]
        __many__ = force_list( default=list())
    [[node attributes]]
        __many__ = force_list( default=list())
    [[run time graph]]
        enable = boolean( default=False )
        cutoff in hours = integer( default=24 )
        directory = string( default='$CYLC_SUITE_DEF_PATH/graphing')
#____________________________________________________________DEVELOPMENT
[development]
    use quick task elimination = boolean( default=True )
    live graph movie = boolean( default=False )

