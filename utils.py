#!/usr/bin/env python


#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#

import subprocess
import datetime
import os
import time

def now(delim='') :
    fmtstr = "%H?%M?%S".replace("?",delim)
    return datetime.datetime.strftime(datetime.datetime.now(), fmtstr)

def mkdir(dirname) :
    os.makedirs(dirname, exist_ok=True)
    
    
def loginit(logfname,mode='w',directory='.') :
    from pathlib import Path
    mkdir(Path(logfname).parent)
    #
    # if not appending then clear existing
    #
    if mode=='w' :
        open(logfname,'w').close()
        
    return open(logfname,mode)
    
    
class Monitor :
  
    def __init__(self, command, trace=False) :
        self.trace=trace
        if trace :
            self.log(f'init with {command}')
        self.command = command
        self.process = subprocess.Popen(command, \
                        shell=True, \
                        stdout=subprocess.PIPE, \
                        #stderr=subprocess.PIPE\
                        stderr=subprocess.STDOUT\
                        )
        print(f'monitoring {command}')
                        
    def traceon(self, trace=True) :
        self.trace=trace
        
    def log(self, msg) :
        if self.trace :
            print(msg)
        
    def read(self) :
        try :
            return self.process.stdout.readline().decode('UTF-8').strip()
        except Exception as e :
            return f'Exception {e} on monitoring {self.command}'

    def readerr(self) :
        return self.process.stderr.readline().decode('UTF-8').strip()
      


