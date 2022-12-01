"""
    Handler for sending a ping message used for latency testing
"""
import tornado.web
import logging

logger = logging.getLogger(__name__)

class HelloHandler(tornado.web.RequestHandler):
    """Simple ping handler for testing latency"""


    async def get(self):
        logger.info("This is an info message")
        self.write("Hello from Tornado")


