import importlib
import logging

from tornado.web import url

handlers = []

handler_names = ["fsj","fsjjson"]

def _gen_handlers(root_module, handler_names):
    for name in handler_names:
        module = importlib.import_module(".%s" % name, root_module)
        module_handlers = getattr(module, "handlers", None)
        if module_handlers:
            _handlers = []
            for handler in module_handlers:
                try:
                    _handlers.append((handler[0], handler[1]))
                except IndexError:
                    logging.warn("wrong web handler %s , please check it." % str(handler))
                    
            handlers.extend(_handlers)

_gen_handlers("atserverwebapp.handlers", handler_names)