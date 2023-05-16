#!/usr/bin/python

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

from utils import Monitor,loginit,now,mkdir
from sbutils import pause
from collections import namedtuple

flog=loginit('/mnt/ram/log/monitor-iotop.log','w')
def log(msg) :
    print(msg,file=flog,flush=True)
    print(msg)

interests = ['brave', 'chrome', 'chromium','firefox','vivaldi']
writes={'brave':0, 'chrome':0, 'chromium':0,'firefox':0,'vivaldi':0}
Event=namedtuple("Event", "cmd,bytes")

ixwrite=5
ixcmd=11

def addwrite(process,amount) :
    print(f'adding {process} {amount}')
    if process not in writes :
        writes[process] = 0
    writes[process] += float(amount)
    print(f'added {process} {amount}')

def parse(event):
    record=event.split()
    return Event(record[ixcmd], float(record[ixwrite]))

log(f'starting read')    
monitor = Monitor('sudo iotop -b') 
while event := monitor.read() :
    #
    #iotop prints 'unavailable' to replace two columns if
    # https://www.suse.com/support/kb/doc/?id=000020888
    # and we're going to split the line expecting two fields
    #
    event=event.replace('unavailable','unavail able')
    if any(interest in event.lower() for interest in interests):
      try:  
        record=parse(event)
        if record.bytes > 0.00 :
            log(f'{now(":")} {record.cmd} wrote {record.bytes}')
            addwrite(record.cmd, record.bytes)
            log(f'total {record.cmd} : {writes[record.bytes]}')
            log('')
      except Exception as e :
          log(f'EXCEPTION{e} on {event.split()}')
log('done')    

