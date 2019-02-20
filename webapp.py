import flask, pprint
from pkg_resources import resource_filename

from moviememes.caption import caption
from moviememes.config import read_config_file
from moviememes.context import Context
from moviememes.logging import build_logger
from moviememes.timestamp import pick_timestamp
from moviememes.screencap import get_screencap

config_file = './movie-meme-config.yaml'
with open(config_file) as f:
    config = read_config_file(f)
print(config_file, config)
logger = build_logger(config['log-level'])
app_context = Context(config, logger)
app_context.logger.info("Application context set up")
app_context.logger.debug("Config is: " + pprint.pformat(config))

app = flask.Flask('moviememes')

@app.route('/')
def hello():
    response = flask.make_response("Hello World! Perhaps you're looking for /sources or /meme?")
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/sources')
def sources():
    response = flask.make_response(pprint.pformat(config['sources']))
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/meme')
def meme():
    context = Context(config, logger)
    context.logger.info(f"Processing request using workdir f{context.workdir}")

    timestamp = pick_timestamp(context)
    screencap_file = get_screencap(context, timestamp)
    caption(context, screencap_file, timestamp.get_text())

    return flask.send_file(screencap_file)