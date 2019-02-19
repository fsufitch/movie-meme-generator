import os, pprint, shutil

from .caption import caption
from .config import build_config
from .context import Context
from .imgur import imgur_upload
from .logging import build_logger
from .screencap import get_screencap
from .timestamp import pick_timestamp

def main(argv: [str]):
    config = build_config(argv[1:])
    logger = build_logger(config['log-level'])
    context = Context(config, logger)

    logger.info("Configuration and logging initialized")
    logger.debug("Config is: " + pprint.pformat(config))
    logger.debug("Temporary working dir is: " + str(context.workdir))

    if context.config['mode'] == 'interactive':
        run_interactive(context)
    elif context.config['mode'] == 'script':
        run_script(context)
    else:
        logger.error('Runtime mode not yet supported')

    context.cleanup()

def run_interactive(context):
    import webbrowser

    attempt_number = 1

    while True:
        context.logger.info(f"Attempt #{attempt_number}")
        timestamp = pick_timestamp(context)

        context.logger.info(f"Picked source `{timestamp.source_id}` at timestamp {timestamp.get_time_seconds()}")
        context.logger.info(f"Picked text: {timestamp.get_text()}")

        screencap_file = get_screencap(context, timestamp)
        context.logger.info(f"Screencapped: {screencap_file}")
        
        working_file = os.path.join(context.workdir.name, f'caption-{attempt_number}.jpg')
        shutil.copy(screencap_file, working_file)

        caption(context, working_file, timestamp.get_text())
        webbrowser.open_new_tab(working_file)

        context.logger.info("Input 'OK' to accept this result")

        if input('? ').lower() == 'ok':
            break

    shutil.copy(working_file, context.config['output']['filename'])
    context.logger.info(f"Created output file: {context.config['output']['filename']}")

    if context.config['output']['imgur']['enabled']:
        upload_url = imgur_upload(context, screencap_file)

    if upload_url:
        context.logger.info(f"Uploaded to Imgur at: {upload_url}")
    else:
        context.logger.info(f"Failed Imgur upload, aborting")
        return

    if context.config['output']['reddit']['enabled']:
        context.logger.error('Reddit output not yet supported')

def run_script(context):
    timestamp = pick_timestamp(context)

    context.logger.info(f"Picked source `{timestamp.source_id}` at timestamp {timestamp.get_time_seconds()}")
    context.logger.info(f"Picked text: {timestamp.get_text()}")

    screencap_file = get_screencap(context, timestamp)
    context.logger.info(f"Screencapped: {screencap_file}")
    
    caption(context, screencap_file, timestamp.get_text())

    shutil.copy(screencap_file, context.config['output']['filename'])
    context.logger.info(f"Created output file: {context.config['output']['filename']}")

    if context.config['output']['imgur']['enabled']:
        upload_url = imgur_upload(context, screencap_file)

    if upload_url:
        context.logger.info(f"Uploaded to Imgur at: {upload_url}")
    else:
        context.logger.info(f"Failed Imgur upload, aborting")
        return

    if context.config['output']['reddit']['enabled']:
        context.logger.error('Reddit output not yet supported')