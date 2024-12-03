import unittest
from app import app

class VowelCountTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_vowel_count(self):
        response = self.app.get('/?text=hello world')
        data = response.get_json()
        self.assertEqual(data['answer'], 3)

    def test_empty_string(self):
        response = self.app.get('/?text=')
        data = response.get_json()
        self.assertEqual(data['answer'], 0)

    def test_no_vowels(self):
        response = self.app.get('/?text=bcdfg')
        data = response.get_json()
        self.assertEqual(data['answer'], 0)

if __name__ == '__main__':
    unittest.main()
