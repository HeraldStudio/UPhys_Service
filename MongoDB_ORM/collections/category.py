from MongoDB_ORM.collections.base import CollectionBase


class Category(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'category')

    # GET /categories
    async def get_categories(self):
        return self.collection.find()

    # GET /category
    async def get_category(self, category_id):
        return await self.find_one_by_id(category_id)

    # POST /category
    async def post_category(self, category):
        return await self.insert_one(category)

    # PUT /category
    async def put_category(self, category_id, category):
        await self.update_one_by_id(category_id, category)

    # DELETE /category
    async def delete_category(self, category_id):
        await self.delete_one_by_id(category_id)

    def get_default(self):
        category = {
            'name': '',  # 分类名称
            'desc': '',  # 分类简介
            'icon': '',  # 分类图标url
            'privilege': 0  # 分类访问权限(所有人=0 用户=1 管理员=2)
        }
        return category
