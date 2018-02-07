import json
import os
import urllib

import requests
from api import app
import unittest
import tempfile

import time

base_path = './'
base_url = 'http://localhost:5000/'


def remove_file(path, retries=3, sleep=0.1):
    """ I'm using this to fix an issue where the tests will sometimes fail because one of the CSV files can't be deleted.
    The error it shows is "The process cannot access the file because it is being used by another process"

    Solution from https://stackoverflow.com/a/45447192/4115031
    """
    for i in range(retries):
        try:
            os.remove(path)
        except WindowsError:
            time.sleep(sleep)
        else:
            break


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.tearDownClass()
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        for file_path in []:
            if os.path.isfile(file_path):
                remove_file(file_path)

    def test_create(self):
        result = self.app.post('/create', data=json.dumps({'name': 'new_name',
                                                   'address': 'new_address',
                                                   'latitude': 111111,
                                                   'longitude': 222222}))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data.decode('utf-8'))
        new_id = data['id']

        result = self.app.get('/read/%s' % str(new_id))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(result.status_code, 200)
        self.assertEquals("new_name", data['name'])
        self.assertEquals("new_address", data['address'])
        self.assertEquals(111111, data['latitude'])
        self.assertEquals(222222, data['longitude'])

    def test_read(self):
        result = self.app.get('/read/1')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data.decode('utf-8'))

        self.assertIn('name', data.keys())
        self.assertIn('address', data.keys())
        self.assertIn('latitude', data.keys())
        self.assertIn('longitude', data.keys())

        self.assertEquals(1, data['id'])
        self.assertEquals("Equator Coffees & Teas", data['name'])
        self.assertEquals("986 Market St", data['address'])
        self.assertEquals(37.782394430549445, data['latitude'])
        self.assertEquals(-122.40997343121123, data['longitude'])

    def test_update(self):
        result = self.app.post('/update/3', data=json.dumps({'name': 'new_name',
                                                   'address': 'new_address',
                                                   'latitude': 111111,
                                                   'longitude': 222222}))
        self.assertEqual(result.status_code, 200)

        result = self.app.get('/read/3')
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(result.status_code, 200)
        self.assertEquals(3, data['id'])
        self.assertEquals("new_name", data['name'])
        self.assertEquals("new_address", data['address'])
        self.assertEquals(111111, data['latitude'])
        self.assertEquals(222222, data['longitude'])

    def test_delete(self):
        result = self.app.get('/delete/2')
        self.assertEqual(result.status_code, 200)

        result = self.app.get('/read/2')
        self.assertEqual(result.status_code, 404)

    def test_nearest(self):
        address = "535 Mission St., San Francisco, CA"
        plus_encoded_address = urllib.parse.quote_plus(address)
        result = self.app.get('/nearest/%s' % plus_encoded_address)
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data.decode('utf-8'))

        self.assertEquals(16, data['id'])
        self.assertEquals("Red Door Coffee", data['name'])
        self.assertEquals("111 Minna St", data['address'])
        self.assertEquals(37.78746242830388, data['latitude'])
        self.assertEquals(-122.39933341741562, data['longitude'])

        address = "252 Guerrero St, San Francisco, CA 94103, USA"
        plus_encoded_address = urllib.parse.quote_plus(address)
        result = self.app.get('/nearest/%s' % plus_encoded_address)
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data.decode('utf-8'))

        self.assertEquals("Four Barrel Coffee", data['name'])


if __name__ == '__main__':
    unittest.main()
