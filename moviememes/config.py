import argparse
import os
import yaml
from typing import NewType, io

from .dictutil import deep_update

MovieMemeConfig = NewType('MovieMemeConfig', dict)

def build_empty_config() -> MovieMemeConfig:
    return MovieMemeConfig({
        'config-file': None,
        'mode': None,
        'log-level': None,
        'sources': {},
        'output': {
            'filename': 'output.jpg',
            'imgur': {
                'enabled': True,
                'client-id': None,
            },
        },
    })

def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Make random memes out of movies/subtitles")
    parser.add_argument('config_file', metavar='CONFIG_FILE', type=argparse.FileType('r'))
    parser.add_argument('-m', '--mode', type=str, choices=['interactive', 'script'],
        help="Mode to run in; overrides value in config file")

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='store_const', const='debug', dest='verbosity')
    verbosity_group.add_argument('-q', '--quiet', action='store_const', const='error', dest='verbosity')

    imgur_toggle_group = parser.add_mutually_exclusive_group()
    imgur_toggle_group.add_argument('--enable-imgur', action='store_true', dest='imgur_enabled', default=None)
    imgur_toggle_group.add_argument('--disable-imgur', action='store_false', dest='imgur_enabled', default=None)

    return parser

def parse_args(args: [str]) -> MovieMemeConfig:
    config = build_empty_config()
    parser = build_argument_parser()
    values = parser.parse_args(args)

    config['config-file'] = values.config_file
    config['mode'] = config.get('mode') or values.mode
    config['log-level'] = values.verbosity or config.get('log-level')
    if values.imgur_enabled is not None:
        config['output']['imgur']['enabled'] = values.imgur_enabled
    
    return config
    
def read_config_file(f: io.TextIO) -> MovieMemeConfig:
    return MovieMemeConfig(yaml.load(f))
    
def consolidate_configs(cli_config: MovieMemeConfig, file_config: MovieMemeConfig) -> MovieMemeConfig:
    config = build_empty_config()

    deep_update(config, file_config)
    deep_update(config, cli_config)
    
    return config

class InvalidMemeConfigException(Exception): pass

def build_config(args):
    cli_config = parse_args(args)
    file_config = read_config_file(cli_config['config-file'])
    full_config = consolidate_configs(cli_config, file_config)
    verify_config(full_config)
    full_config['config-file'].close()
    return full_config

def verify_config(config: MovieMemeConfig):
    if not config.get('mode'):
        raise InvalidMemeConfigException("No execution mode resolved")    
    if not config.get('log-level'):
        raise InvalidMemeConfigException("No log level resolved")
    if not config.get('sources'):
        raise InvalidMemeConfigException("No sources resolved")
    
    for source_id, source_data in config['sources'].items():
        if not source_data.get('video'):
            raise InvalidMemeConfigException(f"Source `{source_id}` has no `video`")
        if not os.path.isfile(source_data['video']):
            raise InvalidMemeConfigException(f"Source `{source_id}` has a `video` that does not exist")
        if not source_data['srt']:
            raise InvalidMemeConfigException(f"Source `{source_id}` has no `srt`")
        if not os.path.isfile(source_data['srt']):
            raise InvalidMemeConfigException(f"Source `{source_id}` has a `srt` that does not exist")
    
    if not config['output']['filename']:
        raise InvalidMemeConfigException("No output filename resolved")
    
    if config['output']['imgur']['enabled']:
        if not config['output']['imgur']['client-id']:
            raise InvalidMemeConfigException("Imgur enabled, but no client-id resolved")