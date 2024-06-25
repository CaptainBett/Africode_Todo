import secrets
from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate


SECRET_KEY = secrets.token_hex(16)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://captain: @localhost:5432/todoapp'
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False ,nullable=False)
    

    def __repr__(self):
        return f'{self.id} {self.description}'
    

class TodoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('+')
    
app.app_context().push()
db.create_all()
  
@app.route('/',methods=['GET', 'POST'])
def index():
    form = TodoForm()
    todos=Todo.query.order_by(Todo.id.desc())
    return render_template('index.html',todos=todos,form=form)
    


@app.route('/add',methods=['POST'])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        try:
            todo = Todo(description=form.description.data)
            db.session.add(todo)
            db.session.commit()
            flash(f'Todo has been added to the list successfully!','success')
        except SQLAlchemyError as e:
            flash(f'Failed to add todo item:{str(e)}','danger')
        return redirect(url_for('index'))
    
    
@app.route('/update_todo_status/<int:todo_id>',methods=['get','post'])
def update_todo_status(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        todo.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Failed to update todo status:{str(e)}",'danger')
        return redirect(url_for('index'))

@app.route('/delete_todo/<int:todo_id>',methods=['POST'])
def delete_todo(todo_id):
    try:
        # todo = Todo.query.filter_by(id=todo_id).first()
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        flash('Todo item has been deleted successfully!','success')
        return redirect(url_for('index'))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Failed to delete todo item:{str(e)}','danger')
        return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)

 