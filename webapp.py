import flask, pprint
from pkg_resources import resource_filename
from datetime import timedelta

from moviememes.caption import caption
from moviememes.config import read_config_file
from moviememes.context import Context
from moviememes.logging import build_logger
from moviememes.timestamp import pick_timestamp, get_timestamp_by_params
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
    # Specify allowed parameters for this request
    ALLOWED_PARAMS = [
        'hour',
        'minute',
        'second',
        'id',
        'tag'
    ]
    context = Context(config, logger)
    context.logger.info(f"Processing request using workdir f{context.workdir}")

    # get hour, minute, and seconds from the url if it's present
    hour = flask.request.args.get('hour')
    minute = flask.request.args.get('minute')
    second = flask.request.args.get('second')
    id = flask.request.args.get('id')
    tag = flask.request.args.get('tag')

    for arg in flask.request.args:
        if arg not in ALLOWED_PARAMS:
            response = flask.jsonify({
                "message": "'{}' is not an allowed path parameter".format(arg)
            })
            response.status_code = 400
            return response

    # Disallow the caller to specify a tag and an ID.
    if id is not None and tag is not None:
        response = flask.jsonify({
            "message": "You must specify an ID or tag, but not both"
        })
        response.status_code = 404
        return response

    # Calculate the timestamp if any elements were included
    if (hour != None or minute != None or second != None):
        hour = int(hour) if hour is not None else 0
        minute = int(minute) if minute is not None else 0
        second = int(second) if second is not None else 0
        time = timedelta(hours=hour, minutes=minute, seconds=second)
    else:
        time = None

    # Get the Timestamp object given the params specified by the user.
    # If no params were passed, it gets a random timestamp.
    timestamp = get_timestamp_by_params(context, timestamp=time, id=id, tag=tag)

    if timestamp is not None:
        screencap_file = get_screencap(context, timestamp)
        caption(context, screencap_file, timestamp.get_text())

        return flask.send_file(screencap_file)
    else:
        response = flask.jsonify({
            "message": "Could not find source or timestamp."
        })
        response.status_code = 404
        return response

if __name__ == "__main__":
    app.run(debug=True)