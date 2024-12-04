from datetime import date

from rest_framework.test import APITestCase

from garpix_page.utils.get_file_path import get_file_path

class GetFilePathTest(APITestCase):
    def setUp(self):
        today = date.today()
        self.params = [
            (f"file{i}.txt", f"uploads/{today.year}/{today.month}/file{i}.txt")
            for i in range(5)
        ]

    def test_file_path(self) -> None:
        for i, o in self.params:
            self.assertEqual(get_file_path(None, i), o)
