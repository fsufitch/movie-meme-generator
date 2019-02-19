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
        self.config['config-file'].close()
        self.workdir.cleanup()
        self.cleaned_up = True
