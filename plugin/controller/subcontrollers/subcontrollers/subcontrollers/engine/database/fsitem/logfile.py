################################################################################
### UTC relative local time (timezone-aware datetime)
################################################################################
'''
Log entries are stored by date
'''
import os, datetime

def local_time():
    return datetime.datetime.now().astimezone()
def local_time_as_str():
    return local_time().isoformat(timespec='milliseconds')

################################################################################

from .csvfile import CSVFile

################################################################################
'''
A LOGFile should merely log a user action by date.
The action in a labelSession is: "assign"-ing a label,
and the result of assigning the label, is the label value.

Since we only log labels, we can skip the opcode.
Code is currently in Session using a normal CSVFile.
'''

class LOGFile(CSVFile):

    @classmethod
    def get_date(cls):
        return local_time_as_str()

    @classmethod
    def get_user(cls):
        return os.getlogin().lower()
