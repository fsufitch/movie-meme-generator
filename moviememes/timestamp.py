import srt
import random
from datetime import timedelta, datetime
from typing import List,Union
from srt import Subtitle

from .context import Context

class Timestamp:
    def __init__(self, source_id: str, subtitle: srt.Subtitle):
        self.source_id = source_id
        self.subtitle = subtitle

    def get_text(self):
        return self.subtitle.content

    def get_time_seconds(self):
        return random.uniform(
            self.subtitle.start.total_seconds(),
            self.subtitle.end.total_seconds(),
        )

def pick_timestamp(context: Context) -> Timestamp:
    source_id = random.choice(list(context.config['sources'].keys()))
    context.logger.debug(f"Picked source {source_id}, reading SRT")    
    with open(context.config['sources'][source_id]['srt']) as f:
        srt_data = f.read()
    subs = list(srt.parse(srt_data))
    context.logger.debug("SRT parsed successfully")
    subtitle = random.choice(subs)
    return Timestamp(source_id, subtitle)


def get_timestamp_by_timedelta(context: Context, timestamp: timedelta):
    source_id = random.choice(list(context.config['sources'].keys()))
    context.logger.debug(f"Picked source {source_id}, reading SRT")
    with open(context.config['sources'][source_id]['srt']) as f:
        srt_data = f.read()
    subs = list(srt.parse(srt_data))
    context.logger.debug("SRT parsed successfully")
    sub = get_subtitle_by_timedelta(subs, timestamp)
    if sub is not None:
        return Timestamp(source_id, sub)
    else:
        return None


def get_subtitle_by_timedelta(subs: List[Subtitle], timestamp: timedelta) -> Union[Subtitle, None]:
    for sub in subs:
        if sub.start <= timestamp <= sub.end:
            return sub

    return None
