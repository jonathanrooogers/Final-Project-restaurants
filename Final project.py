from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#API request
@app.route('/restaurants/<int:restaurant_id>/JSON')
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(item.serialize)

#show all restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurantlist = session.query(Restaurant).all()
    return render_template('allrestaurants.html', restaurants = restaurantlist)

#create new restaurant
@app.route('/restaurants/new',methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newrestaurant =Restaurant(name = request.form['name'])
        session.add(newrestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    
    else:
        return render_template('newrestaurant.html')
    

#edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit',methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id =restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant = editedRestaurant)

#delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedrestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedrestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant = deletedrestaurant )

#show menu for restaurant
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()

    return render_template('menu.html', restaurant =restaurant, items = items )

#add item to menu
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def addItemMenu(restaurant_id):
    if request.method == 'POST':
        newitem = MenuItem(name = request.form['name'], restaurant_id =restaurant_id)
        session.add(newitem)
        session.commit()
        
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('additemmenu.html', restaurant_id = restaurant_id )
    

#edit item in menu
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editItemMenu(restaurant_id, menu_id):
    item= session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        session.add(item)
        session.commit()
        
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('edititemmenu.html', restaurant_id = restaurant_id, menu_id= menu_id, item = item )

    

#delete a item in menu
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteItemMenu(restaurant_id, menu_id):
    item= session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id = restaurant_id))
    else:
        return render_template('deleteitemmenu.html',restaurant_id = restaurant_id, item = item)

    


if __name__ == '__main__':
    #app.secret_key= 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)