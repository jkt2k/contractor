#CREDIT to Make School for providing original test file which this was inspired from

from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_painting_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_painting = {
    'name': 'Cat Videos',
    'artist': 'Cats acting weird',
    'images': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://www.youtube.com/embed/CQ85sUNBK7w'
    ]
}
sample_form_data = {
    'name': sample_painting['name'],
    'artist': sample_painting['artist'],
    'images': '\n'.join(sample_painting['images'])
}

class PaintingsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    def test_index(self):
        """Test the listing homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Painting', result.data)
    def test_new(self):
        """Test the new painting listing creation page."""
        result = self.client.get('/listing/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Painting Listing', result.data)
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_painting(self, mock_find):
        """Test showing a single painting."""
        mock_find.return_value = sample_painting

        result = self.client.get(f'/listing/{sample_painting_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_painting(self, mock_find):
        """Test editing a single painting."""
        mock_find.return_value = sample_painting

        result = self.client.get(f'/listing/{sample_painting_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

if __name__ == '__main__':
    unittest_main()