import os
import subprocess
import shlex

from .context import Context
from .timestamp import Timestamp

class FFMPEGFailureError(RuntimeError): pass

def get_screencap(context: Context, timestamp: Timestamp) -> str:
    # ffmpeg -ss 20 -i <infile.mp4> -vframes 1 -q:v 2 <outfile.jpg>
    outfile = os.path.join(context.workdir.name, 'screencap.jpg')
    verbosity = 'error' if context.config['log-level'] != 'debug' else 'info'

    cmd = ['ffmpeg', '-y',
        '-loglevel', verbosity,
        '-ss', str(timestamp.get_time_seconds()), 
        '-i', context.config['sources'][timestamp.source_id]['video'],
        '-vframes', '1', 
        '-q:v', '2',
        outfile]

    joined_command = ' '.join([shlex.quote(x) for x in cmd])
    context.logger.info(f"Executing: {joined_command}")

    retval = subprocess.call(cmd)
    if retval:
        return FFMPEGFailureError(f"FFMPEG returned code {retval}")

    return outfile
