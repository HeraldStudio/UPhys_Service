from MongoDB_ORM.collections.base import CollectionBase
import pymongo

class Question(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'question')

    # GET /questions
    async def get_questions(self, category_id, page, pagesize):
        condition = {'category_id': category_id}
        sort = [('post_time', pymongo.DESCENDING)]
        result = await self.find_pages_by_condition(condition, sort, page, pagesize)
        return result

    # GET /question
    async def get_question(self, question_id):
        result = await self.find_one_by_id(question_id)
        result['read_num'] = result['read_num'] + 1
        await self.update_one_by_id(question_id, result)
        return result

    # POST /question
    async def post_question(self, category_id, question, user_id):
        question['category_id'] = category_id
        question['post_time'] = self.timestamp()
        question['user_id'] = user_id
        question['read_num'] = 0
        question['modify_time'] = self.timestamp()
        question['modify_user_id'] = user_id
        question['answer_count'] = 0
        await self.insert_one(question)

    # PUT /question
    async def put_question(self, question_id, question, user_id):
        question['modify_user_id'] = user_id
        question['modify_time'] = self.timestamp()
        await self.update_one_by_id(question_id, question)

    # DELETE /question
    async def delete_question(self, question_id):
        await self.delete_one_by_id(question_id)

    async def get_question_category_id(self, question_id):
        question = await self.find_one_by_id(question_id)
        if question is not None:
            return question['category_id']
        return question

    async def get_user_id(self,question_id):
        question = await self.find_one_by_id(question_id)
        if question is not None:
            return question['user_id']
        return question

    async def get_question_count(self,category_id):
        condition = {"category_id":category_id}
        return await self.get_count_by_condition(condition)

    def get_default(self):
        question = {
            'title': '',  # 问题标题
            'content': '',  # 问题内容
            'images': [],  # 问题所包含图片url列表
            'read_num': 0,  # 问题阅读量
            'user_id': '',  # 问题发布者
            'post_time': 0.0,  # 问题发布时间
            'modify_user_id': '',  # 问题最后修改者
            'modify_time': 0.0,  # 问题最后修改时间
            'category_id': ''  # 问题所在category_id
        }
        return question
