from logging import Logger
from tempfile import TemporaryDirectory

from .config import MovieMemeConfig

class Context:
    def __init__(self, config: MovieMemeConfig, logger: Logger):
        self.config = config
        self.logger = logger
        self.workdir = TemporaryDirectory()
        self.cleaned_up = False

    def cleanup(self):
        if self.cleaned_up:
            return
        self.logger.info("Cleaning up runtime context")
        if 'config-file' in self.config:
            self.config['config-file'].close()
        self.workdir.cleanup()
        self.cleaned_up = True

    def get_source_key_by_id(self, key):
        for source_key, source in self.config['sources'].items():
            if 'id' in source and source['id'] == key:
                self.logger.debug(f"Found source {source_key}, reading SRT")
                return source_key

        # If key not found, return None
        return None

    def get_sources_by_tag(self, tag):
        return [
            source_key for source_key, source in self.config['sources'].items()
            if 'tags' in source and tag in source['tags']
        ]
