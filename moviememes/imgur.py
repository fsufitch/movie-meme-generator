from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from pprint import pformat

from .context import Context

def imgur_upload(context: Context, path: str) -> str:
    try:
        client = ImgurClient(context.config['output']['imgur']['client-id'], '')
        upload = client.upload_from_path(path)
        context.logger.info("Uploaded image; details:" + pformat(upload))
        return upload['link']
    except ImgurClientError as e:
        context.logger.exception("Error uploading image to Imgur")
        return None
