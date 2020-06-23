from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
from test import abusiveCheck as aCheck
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id =db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(3000), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    abuse = db.Column(db.String(30), nullable = False)
    abuse_category = db.Column(db.String(75), nullable = True)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        comment_check = request.form['comment']
        comment_flag, comment_tags = aCheck(comment_check)
        try: 
            new_task = Todo(comment = comment_check, abuse = comment_flag, abuse_category = str(comment_tags))
        except:
            new_task = Todo(comment = comment_check, abuse = comment_flag, abuse_category = 'null')
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except :
            return "Error Adding ur Comment"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/del/<int:id>')
def delete_task(id):
    comment_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(comment_to_delete)
        db.session.commit()

        return redirect("/")
    except :
            return "Error Deleting ur Task"    


@app.route('/mod/<int:id>', methods=['get', 'Post'])
def modify_task(id):
    mod_comment = Todo.query.get_or_404(id)
    if request.method == 'POST':
        mod_comment.comment = request.form["comment"]
        temp_comments_details = aCheck(mod_comment.comment)
        mod_comment.abuse = temp_comments_details[0]
        mod_comment.abuse_category = str(temp_comments_details[1])
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error Updating Comment'
        
    else:
        return render_template('modify.html', task = mod_comment)
        

if __name__ == "__main__":
    db.create_all()
    app.run()