import datetime
import os

from flask import Flask, render_template, redirect, url_for, flash, request
from forms import ItemForm
from models import Items
from database import init_db, db_session


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm(request.form)
    if request.method=="POST" and form.validate():
        item = Items(
        	name=form.name.data, 
        	quantity=form.quantity.data, 
        	description=form.description.data, 
        	date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    items = db_session.query(Items).all()
    return render_template('cart.html',items=items,description="All Items for Sell")

@app.route("/items/<int:id>",methods=('GET', 'POST'))
def edit_item(id):
	item = db_session.query(Items).filter_by(id=id).first()
	if item:
		form = ItemForm(request.form,obj=item)

		if request.method=="POST":
			if request.form['submit']=='Delete':
				db_session.delete(item)
				db_session.commit()
				return redirect(url_for('success'))

			elif request.form['submit']=='Save' and form.validate():
				
				item.name= form.name.data,
				item.quantity= form.quantity.data,
				item.description= form.description.data,
				item.date_added = datetime.datetime.now()
				db_session.commit()
				return redirect(url_for('success'))

		return render_template("item.html",form=form,id=id)
	else:
		return ("Cannot find item ID%d"%(id,))

@app.route("/cart",methods=('GET',))
def show_cart():
	items = db_session.query(Items).all()
	return render_template('cart.html',items=items,description="All Items for Sell")

@app.route("/search",methods=('GET','POST'))
def search():
	form = ItemForm(request.form)
	if request.method=="POST":
		items = db_session.query(Items).filter_by(name=form.name.data).all()
		return render_template('cart.html',items=items,description="Found %d records"%(len(items),))
	return render_template('search.html',form=form)

@app.route("/search/<name>",methods=("GET","POST"))
def url_search(name):
	items = db_session.query(Items).filter_by(name=name).all()
	return render_template('cart.html',items=items,description="Found %d records"%(len(items),))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
