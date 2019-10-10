from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
paintings = db.paintings
comments = db.comments

# client = MongoClient()
# db = client.Contractor
# paintings = db.paintings

app=Flask(__name__)
# paintings = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#     { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
# ]

@app.route('/')
def listings_index():
    """Show all paintings."""
    return render_template('paintings_index.html', paintings=paintings.find())

@app.route('/paintings', methods=['POST'])
def paintings_submit():
    """Submit a new painting listing."""
    painting = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'created_at': datetime.now()
    }
    print(painting)
    painting_id = paintings.insert_one(painting).inserted_id
    return redirect(url_for('paintings_show', painting_id=painting_id))

@app.route('/paintings/new')
def paintings_new():
    """Create a new painting listing."""
    return render_template('paintings_new.html', painting={}, title='New Painting Listing')

@app.route('/paintings/<painting_id>')
def paintings_show(painting_id):
    """Show a single painting."""
    painting = paintings.find_one({'_id': ObjectId(painting_id)})
    painting_comments = comments.find({'painting_id': ObjectId(painting_id)})
    return render_template('paintings_show.html', painting=painting, comments=painting_comments)

@app.route('/paintings/<painting_id>', methods=['POST'])
def paintings_update(painting_id):
    """Submit an edited painting."""
    updated_painting = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    paintings.update_one(
        {'_id': ObjectId(painting_id)},
        {'$set': updated_painting})
    return redirect(url_for('paintings_show', painting_id=painting_id))

@app.route('/paintings/<painting_id>/edit')
def paintings_edit(painting_id):
    """Show the edit form for a painting."""
    painting = paintings.find_one({'_id': ObjectId(painting_id)})
    return render_template('paintings_edit.html', painting=painting, title='Edit Painting')

@app.route('/paintings/<painting_id>/delete', methods=['POST'])
def paintings_delete(painting_id):
    """Delete one painting."""
    paintings.delete_one({'_id': ObjectId(painting_id)})
    return redirect(url_for('paintings_index'))

@app.route('/paintings/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'painting_id': ObjectId(request.form.get('painting_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('paintings_show', painting_id=request.form.get('painting_id')))

@app.route('/paintings/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('paintings_show', painting_id=comment.get('painting_id')))

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))