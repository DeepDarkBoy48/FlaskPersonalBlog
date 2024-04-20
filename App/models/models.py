from ..exts import db

# card table
class CategoryModel(db.Model):
    __tablename__ = 'tb_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    describe = db.Column(db.Text(), default='describe')
