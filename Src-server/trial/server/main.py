import os
import mimetypes
import tornado.web
from tornado.web import StaticFileHandler
import tornado.ioloop
import jinja2
from trial.server.constants import ROOT_PATH, HTTP_PORT
from user_agents import parse
import json

TEMPLATE_PATHS = [
    ("/", "files/desktop/index/index.html", "files/mobile/index/index.html", {}),
        None, {}),
]

REQUEST_PATHS = [
    # ("/post/login", LoginHandler),
] 


#
# TemplateHandler
#

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)

class TemplateHandler(tornado.web.RequestHandler) :
    def initialize(self, path_desktop, path_mobile, parameters) :
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters

    def get(self) :
        path = self.__path_desktop
        if self.__path_mobile is not None :
            user_agent = parse(self.request.headers["User-Agent"])
            if user_agent.is_mobile :
                path = self.__path_mobile
        mime_type, encoding = mimetypes.guess_type(path)
        self.set_header("Content-Type", mime_type)
        template = template_env.get_template(path)
        output = template.render(**self.__parameters)
        self.write(output)


def run_server() :
    application_urls = []
    for url, path_desktop, path_mobile, parameters in TEMPLATE_PATHS :
        args = {
            "path_desktop": path_desktop,
            "path_mobile": path_mobile,
            "parameters": parameters
        }
        entry = (url, TemplateHandler, args)
        application_urls.append(entry)

    for url, handler in REQUEST_PATHS :
        args = {
            "url": url,
            "handler": handler
        }
        entry = (url, handler, args)
        application_urls.append(entry)

    static_path = os.path.join(ROOT_PATH, "Src-client")
    files_path = os.path.join(static_path, "files")
    desktop_path = os.path.join(files_path, "desktop")
    common_path = os.path.join(desktop_path, "common")
    images_path = os.path.join(common_path, "images")
    css_path = os.path.join(common_path, "css")
    js_path = os.path.join(common_path, "js")

    lower_level_handlers = [
        (r"/images/(.*)", tornado.web.StaticFileHandler, dict(path=images_path)),
		(r"/css/(.*)", tornado.web.StaticFileHandler, dict(path=css_path)),
        (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path=js_path)),
        (r"/(.*)", tornado.web.StaticFileHandler, dict(path=static_path)),
    ]
    application_urls.extend(lower_level_handlers)
    


    print "Listening on port %s" % (HTTP_PORT,)
    application = tornado.web.Application(
        application_urls,
        gzip=True
    )

    application.listen(HTTP_PORT)
    try :
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt :
        print ""
        print "Ctrl-C received. Exiting."
