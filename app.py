import tornado.web
from motor.motor_tornado import MotorClient
from tornado.options import options, define
from MongoDB_ORM.ORM import ORM
#import config
import routes
import IPython

define("port", default=7942, help="本地监听端口", type=int)
define("DEBUG", default=True, help="是否开启debug模式", type=bool)
define("TEST", default=True, help="测试服务器，支持跨域访问,推送测试模式", type=bool)
define("db_name", default="tank", help="mongodb数据库名称", type=str)
tornado.options.parse_command_line()

mongodb_client = MotorClient('127.0.0.1:27017')
mongodb_database = mongodb_client[options.db_name]
mongodb_orm = ORM(mongodb_database)

application = tornado.web.Application(
    handlers=routes.handlers,
    db=mongodb_database,
    orm=mongodb_orm,
    TEST=options.TEST,
    debug=options.DEBUG,
    compiled_template_cache=True,
    static_hash_cache=True,
    autoreload=True,
    # primary_number=random.randint(0,10000),
    debug_mode=True,
)


if __name__ == "__main__":
    application.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.start()
    IPython.embed()