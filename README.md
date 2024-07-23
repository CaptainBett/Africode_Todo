# Flask Todo App with Categories

This is a simple Flask web application that allows users to create, update, and delete tasks with categories. The application uses Flask-SQLAlchemy for database operations and Flask-WTF for form validation.

## Table of Contents

- [Getting Started](#getting-started)
- [Cloning the Project](#cloning-the-project)
- [Installing Dependencies](#installing-dependencies)
- [Setting Up the Database](#setting-up-the-database)
- [Running the Application](#running-the-application)
- [Contributing to the Project](#contributing-to-the-project)
- [About Africode Academy](#about-africode-academy)

## Getting Started

To use this application, you need to have Python 3.6 or higher installed on your system.

## Cloning the Project

You can clone this project by running the following command in your terminal:

```bash
git clone https://github.com/your-username/flask-todo-app-with-categories.git
```

Replace `your-username` with your GitHub username.

## Installing Dependencies

Navigate to the project directory and create a virtual environment:

```bash
cd flask-todo-app-with-categories
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Setting Up the Database

Make sure you have PostgreSQL installed on your system. Create a new database named `todoapp` and update the database URI in the `app.config` section of the `app.py` file:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/todoapp'
```

Replace `username` and `password` with your PostgreSQL username and password.

Initialize the database:

```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

Start the Flask development server:

```bash
flask run --host=127.0.0.1 --port=8001
```

The application will be available at http://127.0.0.1:8001/.

## Contributing to the Project

To contribute to this project, follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your changes.
3. Make your changes and commit them to your branch.
4. Push your branch to your fork on GitHub.
5. Create a pull request from your branch to the main repository.

## About Africode Academy

[Africode Academy](https://africodeacademy.com/) is a coding school that focuses on teaching web development and programming skills to students from Africa. It offers a variety of courses and workshops, including Python, JavaScript, and web design. Africode Academy is committed to fostering a diverse and inclusive coding community in Africa.

If you have any questions or need further assistance, feel free to reach out to us at [admissions@africodeacademy.com](mailto:admissions@africodeacademy.com).
