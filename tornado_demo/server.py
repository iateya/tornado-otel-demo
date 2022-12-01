import tornado
import tornado.options
import tornado.ioloop
import uvloop
import logging
import logging.config
import os

import yaml
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.tornado import TornadoInstrumentor

from tornado_demo.hello import HelloHandler


def setup_logging(default_path='log.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
   """
   | **@author:** Prathyush SP
   | Logging Setup
   """
   path = default_path
   value = os.getenv(env_key, None)
   if value:
       path = value
   if os.path.exists(path):
       with open(path, 'rt') as f:
           try:
               config = yaml.safe_load(f.read())
               logging.config.dictConfig(config)

           except Exception as e:
               print(e)
               print('Error in Logging Configuration. Using default configs')
               logging.basicConfig(level=default_level)

   else:
       logging.basicConfig(level=default_level)
       print('Failed to load configuration file. Using default configs')


def init_otel():
    resource = Resource(attributes={"service.name": "tornado-demo"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    LoggingInstrumentor().instrument()
    TornadoInstrumentor().instrument()

def main():

    setup_logging()
    init_otel()

    tornado.options.parse_command_line()
    uvloop.install()

    handlers = [

        (r"/hello", HelloHandler),

    ]


    app = tornado.web.Application(
        handlers,

    )
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
