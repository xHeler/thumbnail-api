from django.test import TestCase

from src.images.test.factories import SizeFactory


class SizeTestCase(TestCase):
    def test_str(self):
        size = SizeFactory(height=0)
        self.assertEqual(str(size), "Size Image original size")

    def test_save(self):
        size = SizeFactory.create(height=100)
        self.assertEqual(size.name, "Image sizes 100x100")
        self.assertEqual(size.codename, "custom_image_size_100x100")

        size = SizeFactory.create(height=0)
        self.assertEqual(size.name, "Image original size")
        self.assertEqual(size.codename, "custom_image_size_original")
