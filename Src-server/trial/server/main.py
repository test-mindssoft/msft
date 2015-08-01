import os
import mimetypes
import tornado.web
from tornado.web import StaticFileHandler
import tornado.ioloop
import jinja2
from trial.server.constants import ROOT_PATH, HTTP_PORT
from user_agents import parse
import json

from trial.model import LocationModel as locationdb
from trial.server import countries as countriesdb 

TEMPLATE_PATHS = [
    ("/", "files/desktop/index/index.html", "files/mobile/index/index.html", {}),
    ("/task/create", "files/desktop/Task-ActivityData/Task-ActivityData.html", None, {}),
    ("/task/list", "files/desktop/Task-ActivityData/Task-ActivityDataList.html", None, {}),
    ("/location", "files/desktop/LocationMaster/LocationMaster.html", 
        None,
        {"states":locationdb.getStates(),"districts":locationdb.getDistricts(),
        "regions":locationdb.getRegions(),"provinces":locationdb.getProvinces(),
        "countries":countriesdb.countries}),
]

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

class TaskListHandler(tornado.web.RequestHandler):
    def get(self):
        rows = _execute('SELECT * FROM taskactivty')
        data_list = []
        for row in rows:
            data_list.append(row)
        self.write(json.dumps(data_list))
       # query = "select activityname, activitytype, duration, repeats, authority, slaprate, penaltyrate  from taskactivty"         
       # print query
       # c= cursor.execute (query)
       # datalist=cursor.fetchall()
       # self.render('Task-ActivityDataList.html', datalist=datalist)  


class TaskCreateHandler(tornado.web.RequestHandler):
    def initialize(self, url, handler):
        self.url = url
        self.handler = handler

    def get(self):
        self.write("Hello, world")

    def post(self):
        json_data = json.loads(self.request.body)
        data = json_data["data"]
        activityname = data["activityname"]
        taskid = data["taskid"]
<<<<<<< HEAD
        #getid=0
      	if(getid == "0"):
        	sql = "INSERT INTO taskactivity(activityname) VALUES ('%s')" % (activityname)
        	cursor.execute(sql)
        	db.commit()
        get = post # <--------------

REQUEST_PATHS = [
    (r"/task/create", TaskCreateHandler)
=======
        sql = "INSERT INTO taskactivity(activityname) VALUES ('%s')" % (activityname)
        cursor.execute(sql)
        db.commit()
        self.set_header('Content-Type', 'application/json')
        json_ = tornado.escape.json_encode(js)
        self.write(json_)

        #json_data = json.loads(self.request.body)
        #data = json_data["data"]
        #activity1 = data["activityname"]
   #     getid = data["taskid"]
    	#getid=0
    #  	if(getid == "0"):
     #   	sql = "INSERT INTO taskactivity(activityname) VALUES ('%s')" % (activityname)
      #  	cursor.execute(sql)
       # 	db.commit()
       # self.set_header('Content-Type', 'application/json')
       # json_ = tornado.escape.json_encode(js)
       # self.write(json_)
       # get = post # <--------------

REQUEST_PATHS = [
    # ("/post/login", LoginHandler),
    ("/post/task/create", TaskCreateHandler),
    ("/task/create/(.*)", TaskCreateHandler),
    (r"/task/list", TaskListHandler),  
>>>>>>> origin/master
] 

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
