import srt
import random
from datetime import timedelta, datetime
from typing import List,Union
from srt import Subtitle

from .context import Context

class Timestamp:
    def __init__(self, source_id: str, subtitle: srt.Subtitle, time: timedelta = None):
        self.source_id = source_id
        self.subtitle = subtitle
        self.time = time

    def get_text(self):
        return self.subtitle.content

    def get_time_seconds(self):
        # Gets the time of the timestamp in seconds. If the time is not set, it picks a random time from the subtitle.
        if self.time is None:
            return random.uniform(
                self.subtitle.start.total_seconds(),
                self.subtitle.end.total_seconds(),
            )
        else:
            return self.time.total_seconds()

def pick_timestamp(context: Context) -> Timestamp:
    source_id = random.choice(list(context.config['sources'].keys()))
    context.logger.debug(f"Picked source {source_id}, reading SRT")    
    with open(context.config['sources'][source_id]['srt']) as f:
        srt_data = f.read()
    subs = list(srt.parse(srt_data))
    context.logger.debug("SRT parsed successfully")
    subtitle = random.choice(subs)
    return Timestamp(source_id, subtitle)


def get_timestamp_by_params(context: Context, timestamp: timedelta = None, id: str = None, tag: str = None):
    if id is not None:
        source_key = context.get_source_key_by_id(id)
        context.logger.debug(f"Picked source {source_key} by ID, reading SRT")
    elif tag is not None:
        source_keys = context.get_sources_by_tag(tag)
        if (len(source_keys) > 0):
            source_key = random.choice(source_keys)
        else:
            source_key = None
        context.logger.debug(f"Picked source {source_key} by TAG, reading SRT")
    else:
        source_key = random.choice(list(context.config['sources'].keys()))
        context.logger.debug(f"Picked source {source_key} at RANDOM, reading SRT")

    if source_key is None:
        return None

    with open(context.config['sources'][source_key]['srt']) as f:
        srt_data = f.read()
    subs = list(srt.parse(srt_data))
    context.logger.debug("SRT parsed successfully")
    if timestamp is not None:
        sub = get_subtitle_by_timedelta(subs, timestamp)
    else:
        sub = random.choice(subs)

    if sub is not None:
        return Timestamp(source_key, sub, timestamp)
    else:
        return None


def get_subtitle_by_timedelta(subs: List[Subtitle], timestamp: timedelta) -> Union[Subtitle, None]:
    for sub in subs:
        if sub.start <= timestamp <= sub.end:
            return sub

    return None
