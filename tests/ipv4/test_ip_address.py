import unittest

from core import IPv4


class TestIPv4(unittest.TestCase):
    def test_can_create_from_tuple(self):
        i = IPv4(255, 255, 255, 255)
        self.assertEqual(i.octets, [255, 255, 255, 255])

    def test_can_create_from_str(self):
        i = IPv4("255.255.255.255")
        self.assertEqual(i.octets, [255, 255, 255, 255])

    def test_can_create_from_list(self):
        i = IPv4([255, 255, 255, 255])
        self.assertEqual(i.octets, [255, 255, 255, 255])

    def test_cannot_create_when_too_many_octets(self):
        with self.assertRaises(ValueError):
            i = IPv4(255, 255, 255, 255, 255)
        with self.assertRaises(ValueError):
            i = IPv4([255, 255, 255, 255, 255])
        with self.assertRaises(ValueError):
            i = IPv4("255.255.255.255.255")

    def test_cannot_create_when_too_few_octets(self):
        with self.assertRaises(ValueError):
            i = IPv4(255, 255, 255)
        with self.assertRaises(ValueError):
            i = IPv4([255, 255, 255])
        with self.assertRaises(ValueError):
            i = IPv4("255.255.255")

    def test_octet_cannot_be_out_of_range(self):
        with self.assertRaises(ValueError):
            i = IPv4(256, 255, 255, 255)
        with self.assertRaises(ValueError):
            i = IPv4([-1, 255, 255, 255])
        with self.assertRaises(ValueError):
            i = IPv4("256.255.255.300")
