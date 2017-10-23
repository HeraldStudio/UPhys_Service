from tornado.web import RequestHandler
from handler.handler_config import *
from handler.exceptions import ArgsError,MissingArgumentError,PermissionDeniedError
import json
import IPython
DEFAULT_TYPE = []

class BaseHandler(RequestHandler):

    # 获取权限
    @property
    async def privilege(self):
        if not await self.user_info:
            return no_privilege
        if self._user_info['isAdmin']:
            return admin_privilege
        return user_privilege

    # 鉴定管理员
    @property
    async def is_admin(self):
        privilege = await self.privilege
        if privilege == admin_privilege:
            return True
        return False

    def finish_success(self, **kwargs):
        rs = {
            'status': 'success',
            'code':'200',
            'result':list(kwargs.values())[0]
        }
        self.finish(json.dumps(rs))

    def finish_err(self, **kwargs):
        rs = {
            'status': 'success',
            'code':'0',
            'result':list(kwargs.values())[0]
        }
        self.finish(json.dumps(rs))

    @property
    def json_body(self):
        if not hasattr(self, '_json_body'):
            if hasattr(self.request, "body"):
                try:
                    if not self.request.body:
                        self._json_body = {}
                    else:
                        self._json_body = json.loads(self.request.body.decode('utf-8'))
                except ValueError:
                    raise ArgsError("参数不是json格式！")
        return self._json_body

    @property
    def token(self):
        return self.get_cookie("token", default='')

    @property
    def db(self):
        return self.settings['orm']

    @property
    async def user_info(self):
        if not hasattr(self, '_user_info'):
            user_token = self.token
            self._user_info = await self.db.user.get_user(user_token)
            return self._user_info
        else:
            return self._user_info

    @property
    async def user_id(self):
        if not await self.user_info:
            raise PermissionDeniedError("未登录")
        else:
            return str(self._user_info['_id'])

    def get_argument(self, name, default=DEFAULT_TYPE, strip=True):
        if name in self.json_body:
            rs = self.json_body[name]
            return rs
        elif default is DEFAULT_TYPE:
            raise MissingArgumentError(name)
        else:
            return default

    @property
    async def answer_allow(self):
        privilege = await self.privilege
        answer_id = self.get_argument("answer_id")
        question_id = await self.db.answer.get_answer_question_id(answer_id)
        category_id = await self.db.question.get_question_category_id(question_id)
        answer_privilege = await self.db.category.get_privilege(category_id)
        if privilege < answer_privilege:
            return False
        return True

    @property
    async def question_allow(self):
        privilege = await self.privilege
        question_id = self.get_argument("question_id")
        category_id = await self.db.question.get_question_category_id(question_id)
        answer_privilege = await self.db.category.get_privilege(category_id)
        if privilege < answer_privilege:
            return False
        return True
