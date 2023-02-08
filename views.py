
from django.shortcuts import redirect, render
from flask import Blueprint, flash, render_template, request, session, url_for
from importlib_metadata import re
import sqlite3
from .models import User
from . import db
from flask_login import current_user, login_required


views = Blueprint('views', __name__)


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row # goes through the database
    return connection
    

def update_task(conn, task):
    
    """
    update Bio
    :param conn:
    :param task:
    :return: project id
    """
    
    sql = """ UPDATE Accounts SET Bio = ? WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    # write code here

    bio = request.form.get('bio')

    
    if request.method == 'POST':

        update_task(connection, (bio, current_user.id))
        flash('Bio updated successfully!', category='success')


    return render_template("home.html", accounts=accounts, namesToDisplay=User.query.all(), user=current_user)

@views.route('/filter', methods=['GET', 'POST'])
def filter():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    connection.close()
    

    return render_template("filter.html", accounts=accounts)

@views.route('/profile', methods=['GET', 'POST'])
def profile():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table

    acc = 1
    for account in accounts:
        if current_user.id == account['ID']:
            acc = account

    connection.close()
    

    return render_template("profile.html", accounts=accounts, acc=acc)