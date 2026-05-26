# send an alert email if the allsky is down

from meteortools.utils import sendAnEmail
import sys
import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

MAXDELAY = 450 # seconds - the status should be updated every 5 minutes

LASTSTATEFILE= 'LOGDIR/radio_laststate.txt'


def checkAndSend(lastupdatedt):
    log = logging.getLogger('sendRadioAlert')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('LOGDIR/sendRadioAlert.log'), maxBytes=512000, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    upddt = datetime.datetime.strptime(lastupdatedt, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    delay = (datetime.datetime.now(tz=datetime.timezone.utc) - upddt).seconds
    laststate = 0
    if os.path.isfile(LASTSTATEFILE):
        laststate = int(open(LASTSTATEFILE, 'r').readlines()[0].strip())
    if delay > MAXDELAY:
        if laststate == 0:
            log.warning('Radiopi has stalled')
            try:
                msg = f'Radiopi Stalled with last update at {lastupdatedt}'
                sendAnEmail('mark.jm.mcintyre@cesmail.net', msg, 'Radiopi Alert', 'noreply@thelinux')
            except Exception as e:
                log.warning('problem connecting to gmail')
                log.warning(e)
            open(LASTSTATEFILE, 'w').write('1')
        else:
            # we already alerted so no need to send an email
            log.warning('still stalled')        
    else: 
        log.info(f'all ok')
        # not delayed - only notify if the previous state was stalled
        if laststate == 1:
            try:
                sendAnEmail('mark.jm.mcintyre@cesmail.net', 'Radiopi error cleared', 'Radiopi ok', 'noreply@thelinux')
            except Exception as e:
                log.warning('problem connecting to gmail')
                log.warning(e)
            open(LASTSTATEFILE, 'w').write('0')
    return 


if __name__ == '__main__':
    checkAndSend(sys.argv[1])
