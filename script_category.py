from app import db ,Category

def create_initial_categories():
    categories = ['General', 'Personal', 'Work', 'Relationship', 'Other']
    for cat_name in categories:
        category = Category.query.filter_by(name=cat_name).first()
        if not category:
            category = Category(name=cat_name)
            db.session.add(category)
            db.session.commit()
# Call this function after your app is initialized
create_initial_categories()