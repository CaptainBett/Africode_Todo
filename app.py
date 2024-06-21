import secrets
from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from sqlalchemy.exc import SQLAlchemyError


SECRET_KEY = secrets.token_hex(16)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://captain: @localhost:5432/todoapp'
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'{self.id} {self.description}'
    

class TodoForm(FlaskForm):
    description = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')
    
app.app_context().push()
db.create_all()
  
@app.route('/',methods=['GET', 'POST'])
def index():
    form = TodoForm()
    if form.validate_on_submit():
        try:
            todo = Todo(description=form.description.data)
            db.session.add(todo)
            db.session.commit()
            flash(f'Todo ({todo.description}) has been added to the list','success')
        except SQLAlchemyError as e:
            flash(f'Failed to add todo item:{str(e)}','danger')
        return redirect(url_for('index'))
    todos=Todo.query.all()
    return render_template('index.html',todos=todos,form=form)
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)

 