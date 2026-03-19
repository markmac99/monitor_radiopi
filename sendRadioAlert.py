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
    try:
        if os.path.isfile('laststate.txt'):
            laststate = int(open(LASTSTATEFILE, 'r').readlines()[0].strip())
    except Exception:
        pass
    if laststate == 0 and delay > MAXDELAY:
        try:
            sendAnEmail('mark.jm.mcintyre@cesmail.net', 'Radiopi Stalled', 'Radiopi Alert', 'noreply@thelinux')
            open(LASTSTATEFILE, 'w').write('1')
        except Exception as e:
            log.warning('problem connecting to gmail')
            log.warning(e)
    else:
        log.info(f'all ok at {lastupdatedt}')
        open(LASTSTATEFILE, 'w').write('0')
    return 


if __name__ == '__main__':
    checkAndSend(sys.argv[1])
