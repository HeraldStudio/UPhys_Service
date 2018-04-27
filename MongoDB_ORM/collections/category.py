from MongoDB_ORM.collections.base import CollectionBase


class Category(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'category')

    # GET /categories
    async def get_categories(self, privilege):
        condition = {'privilege': {'$lt': privilege + 1}}
        sort = [('seq', self.ASCENDING)]
        cursor = self.collection.find(condition, sort=sort)
        result = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result

    # GET /category
    async def get_category(self, category_id, privilege):
        result = await self.find_one_by_id(category_id)
        if result['privilege'] <= privilege:
            return result
        return {}

    # POST /category
    async def post_category(self, category):
        category['seq'] = await self.get_current_seq()
        return await self.insert_one(category)

    # PUT /category
    async def put_category(self, category_id, category):
        await self.update_one_by_id(category_id, category)

    # DELETE /category
    async def delete_category(self, category_id):
        await self.delete_one_by_id(category_id)

    async def get_privilege(self, category_id):
        condition = {'_id': self.ObjectId(category_id)}
        category = await self.collection.find_one(condition)
        if category is not None:
            return category['privilege']
        else:
            return -1

    def get_default(self):
        category = {
            'name': '',  # 分类名称
            'desc': '',  # 分类简介
            'icon': '',  # 分类图标url
            'privilege': 0,  # 分类访问权限(所有人=0 用户=1 管理员=2)
            'seq': 0
        }
        return category

    async def sort(self, id_1, id_2):
        seq_1 = await self.find_one_by_id(id_1)
        seq_2 = await self.find_one_by_id(id_2)
        seq_1 = seq_1['seq']
        seq_2 = seq_2['seq']
        await self.update_one_by_id(id_1, {'seq': int(seq_2)})
        await self.update_one_by_id(id_2, {'seq': int(seq_1)})

    async def get_current_seq(self):
        current = await self.find_all()
        seq = 0
        for item in current:
            if seq < int(item['seq']):
                seq = int(item['seq'])
        return seq + 1
