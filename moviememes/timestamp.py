import srt
import random
from datetime import timedelta

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
