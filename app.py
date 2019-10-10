from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
listing = db.listing
comments = db.comments

# client = MongoClient()
# db = client.Contractor
# listing = db.listing

app=Flask(__name__)

@app.route('/')
def listings_index():
    """Show all listing."""
    return render_template('listing_index.html', listing=listing.find())

@app.route('/listing', methods=['POST'])
def listing_submit():
    """Submit a new painting listing."""
    painting = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'images': request.form.get('images').split(),
        'created_at': datetime.now()
    }
    print(painting)
    painting_id = listing.insert_one(painting).inserted_id
    return redirect(url_for('listing_show', painting_id=painting_id))

@app.route('/listing/new')
def listing_new():
    """Create a new painting listing."""
    return render_template('listing_new.html', painting={}, title='New Painting Listing')

@app.route('/listing/<painting_id>')
def listing_show(painting_id):
    """Show a single painting."""
    painting = listing.find_one({'_id': ObjectId(painting_id)})
    painting_comments = comments.find({'painting_id': ObjectId(painting_id)})
    return render_template('listing_show.html', painting=painting, comments=painting_comments)

@app.route('/listing/<painting_id>', methods=['POST'])
def listing_update(painting_id):
    """Submit an edited painting."""
    updated_painting = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'images': request.form.get('images').split()
    }
    listing.update_one(
        {'_id': ObjectId(painting_id)},
        {'$set': updated_painting})
    return redirect(url_for('listing_show', painting_id=painting_id))

@app.route('/listing/<painting_id>/edit')
def listing_edit(painting_id):
    """Show the edit form for a painting."""
    painting = listing.find_one({'_id': ObjectId(painting_id)})
    return render_template('listing_edit.html', painting=painting, title='Edit Listing')

@app.route('/listing/<painting_id>/delete', methods=['POST'])
def listing_delete(painting_id):
    """Delete one painting."""
    listing.delete_one({'_id': ObjectId(painting_id)})
    return redirect(url_for('listing_index'))

@app.route('/listing/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'painting_id': ObjectId(request.form.get('painting_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('listing_show', painting_id=request.form.get('painting_id')))

@app.route('/listing/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('listing_show', painting_id=comment.get('painting_id')))

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))