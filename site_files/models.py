from database import db
import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, note_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.post_id = note_id
        self.user_id = user_id
class Post(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    image = db.Column("image", db.BLOB)
    date = db.Column("date", db.String(50))
    category = db.Column("category", db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pin_status = db.Column("Pin_Status", db.Boolean)
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan", lazy=True) 
    def __init__(self, title, text, image, date, category, user_id, pin_status):
        self.title = title
        self.text = text
        self.image = image
        self.date = date
        self.category = category
        self.user_id = user_id
        self.pin_status = pin_status
class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    posts = db.relationship("Post", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()
