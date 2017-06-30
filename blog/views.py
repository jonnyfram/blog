from flask import render_template

from . import app
from .database import session, Entry

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>/")
def entries(page=1):
    #zero indexed page
    page_index = page - 1
    
    count = session.query(Entry).count()
    
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count - 1) //PAGINATE_BY +1
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
def add_entry_get():
    return render_template("add_entry.html")
    
from flask import request, redirect, url_for

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
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
def edit_entry_get(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).first()
    
    return render_template("edit.html", title = entry.title, content = entry.content)
    
@app.route("/entry/<int:id>/edit", methods=["POST"])
def edit_entry_post(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).first()
    entry.title=request.form["title"]
    entry.content=request.form["content"]
    
    session.add(entry)
    session.commit()
    
    return redirect(url_for("entries")) # this does not appear to happen- we stay on edit page

@app.route("/entry/<int:id>/delete", methods=["GET"])
def delete_entry_get(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).first()
    return render_template("delete.html", title=entry.title)

@app.route("/entry/<int:id>/delete", methods=["POST"])
def delete_entry_post(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).first()
    
    session.delete(entry)
    session.commit()
    
    return redirect(url_for("entries")) # this does not appear to happen- we stay on edit page

#CURRENTLY NON FUNCTIONAL
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