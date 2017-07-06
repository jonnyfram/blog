from flask import render_template, request, redirect, url_for
from flask import flash
from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user

from werkzeug.security import check_password_hash

from . import app
from .database import session, Entry, User

PAGINATE_BY = 10

@app.route("/entries")
@app.route("/")
@app.route("/page/<int:page>/")
def entries(page=1):
    #zero indexed page
    print(current_user)
    page_index = page - 1
    
    #grabs the submission if submitted at top of page, uses predefined constant if no argument
    paginate_by = int(request.args.get('entries_per', PAGINATE_BY))
    
    count = session.query(Entry).count()
    
    start = page_index * paginate_by
    end = start + paginate_by
    
    total_pages = (count - 1) //paginate_by +1
    has_next = page_index < total_pages -1
    has_prev = page_index > 0
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    
    return render_template("entries.html", 
    entries=entries,
    has_next = has_next,
    has_prev = has_prev,
    page = page,
    total_pages = total_pages)
    
@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")
    
from flask import request, redirect, url_for

@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author = current_user
        )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
 
# Adding view for individual entry   
@app.route("/entry/<int:id>/")
def view_entry(id):

    entry = session.query(Entry).get(id)
    return render_template("entry.html", entry=entry) # test me

# Edit entry
@app.route("/entry/<int:id>/edit", methods=["GET"])
@login_required
def edit_entry_get(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).first()
    
    return render_template("edit.html", title = entry.title, content = entry.content, entryid=entry.id)

@app.route("/entry/<int:id>/edit", methods=["POST"])
@login_required
def edit_entry_post(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).first()
    entry.title=request.form["title"]
    entry.content=request.form["content"]
    
    session.add(entry)
    session.commit()
    
    return redirect(url_for("entries")) # this does not appear to happen- we stay on edit page

@app.route("/entry/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_entry_get(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).first()
    session.delete(entry)
    session.commit()
    
    return render_template("delete.html", title=entry.title, entryid=entry.id)
    
#/?limit=20 and /page/2?limit=20
@app.route("/?limit=<int:LIMIT>")
@app.route("/page/<int:page>?limit=<int:LIMIT>")
def entry_limit(LIMIT=1, page=1):
    
    post_limit = request.args.get(LIMIT)
    ##page = request.args.get(page)
    
    #zero indexed page
    page_index = page - 1
    
    count = session.query(Entry).count()
    
    start = page_index * post_limit
    end = start + post_limit
    
    total_pages = (count - 1) //LIMIT +1
    has_next = page_index < total_pages -1
    has_prev = page_index > 0
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    
    return render_template("entries.html", 
    entries=entries,
    has_next = has_next,
    has_prev = has_prev,
    page = page,
    total_pages = total_pages)

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        print("error logging in in login_post() method. This should have triggered the flash in browser- did you see flashed_messages??")
        return redirect(url_for("login_get"))
        
    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))
    
@app.route("/logout")
def logout():
    logout_user()
    return render_template("logged_out.html")
