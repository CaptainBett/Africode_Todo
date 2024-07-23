import secrets
from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
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
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='todos')#back_populates='todos'
    

    def __repr__(self):
        return f'{self.id} {self.description}'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # todos = db.relationship('Todo', back_populates='category', lazy='dynamic')
    

    def __repr__(self):
        return f'[{self.name}]'
    

class TodoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()])
    submit = SubmitField('+')
 


    def __init__(self,*args,**kwargs):
        super(TodoForm, self).__init__(*args,**kwargs)
        self.category.choices = [(category.id,category.name) for category in Category.query.order_by(Category.name).all()]
        
    
app.app_context().push()
db.create_all()



@app.route('/',methods=['GET', 'POST'])
@app.route("/category/<int:category_id>", methods=['GET'])
def index(category_id=None):
    form = TodoForm()
    if form.validate_on_submit():
        try:    
            todo = Todo(description=form.description.data,category_id=form.category.data)
            db.session.add(todo)
            db.session.commit()
            flash(f'Todo has been added to the list successfully!','success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Failed to add todo item:{str(e)}','danger')
        return redirect(url_for('index')) 
    if category_id:
        todos = Todo.query.filter_by(category_id=category_id).all()
        current_category = Category.query.get_or_404(category_id)
    else:
        todos=Todo.query.order_by(Todo.id.desc())
        current_category = None
    categories = Category.query.all()
    return render_template('index.html',todos=todos,form=form,current_category=current_category,categories=categories)
   
    
    
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

 