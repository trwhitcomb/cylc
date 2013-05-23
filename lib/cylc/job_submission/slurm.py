#!/usr/bin/env python

#C: THIS FILE IS PART OF THE CYLC SUITE ENGINE.
#C: Copyright (C) 2008-2013 Hilary Oliver, NIWA
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

import re
from job_submit import job_submit

class slurm( job_submit ):
    """
SLURM job submission.
    """

    COMMAND_TEMPLATE = "sbatch %s"

    def set_directives( self ):
        self.jobconfig['directive prefix'] = "#SBATCH"
        self.jobconfig['directive final']  = None
        self.jobconfig['directive connector'] = "="

        defaults = {}
        defaults[ '--job-name' ] = self.task_id
        # Replace literal '$HOME' in stdout and stderr file paths with '' 
        # because environment variables are not interpreted in directives.
        # (For remote tasks the local home directory path is replaced
        # with '$HOME' in config.py).
        defaults[ '--output' ] = re.sub( '\$HOME/', '', self.stdout_file )
        defaults[ '--error' ]  = re.sub( '\$HOME/', '', self.stderr_file )

        # In case the user wants to override the above defaults:
        for d,val in self.jobconfig['directives'].items():
            defaults[ d ] = val
        self.jobconfig['directives'] = defaults

    def construct_jobfile_submission_command( self ):
        command_template = self.job_submit_command_template
        if not command_template:
            command_template = self.__class__.COMMAND_TEMPLATE
        self.command = command_template % ( self.jobfile_path )


    def get_id( self, out, err ):
        """
        Extract the job submit ID from job submission command
        output. For SLURM jobs the submission command returns
        the process ID to stdout.
        """
        return out.strip()

    def get_job_poll_command( self, jid ):
        """
        Given the job submit ID, return a command string that uses
        'cylc get-task-status' (on the task host) to determine current
        job status:
           cylc get-job-status <QUEUED> <RUNNING>
        where:
            QUEUED  = true if job is waiting or running, else false
            RUNNING = true if job is running, else false

        WARNING: 'cylc get-task-status' prints a task status message -
        the final result - to stdout, so any stdout from scripting prior
        to the call must be dumped to /dev/null.

        There are many held job states, but we really only care about
          * 'PD' (queueing) = waiting in the SLURM queue
          * 'R' (running) = running
        """
        job_data = {
            'job_id': jid,
            'jobfile': jobfile_path,
        }

        # Calling squeue with "-h" disables the header, so we only get
        # back one line with our job information.
        cmd_template = r"""
            RUNNING=false
            QUEUED=false
            # Look for a running job
            squeue -h -j %(job_id) | awk '{print $5}' | egrep "^R$" > /dev/null
            if [[ $? == 0 ]]; then
                # Found a running job
                RUNNING=true
                QUEUED=true
            fi
            if [[ QUEUED != true ]]; then
                # Not running - see if it's queued
                squeue -h -j %(job_id) | awk '{print $5}' | egrep "^PD$" > /dev/null
                if [[ $? == 0 ]]; then
                    QUEUED=true
                fi
            fi

            cylc get-task-status %(jobfile).status $QUEUED $RUNNING
        """
        cmd = cmd_template % job_data

        return cmd

    def get_job_kill_command( self, jid ):
        """
        Given the job submit ID, return a command to kill the job.
        """
        cmd = "scancel " + jid
        return cmd

