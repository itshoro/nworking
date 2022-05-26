import unittest

from nworking import IPv4, AddressOutOfRangeError


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
            IPv4(255, 255, 255, 255, 255)
        with self.assertRaises(ValueError):
            IPv4([255, 255, 255, 255, 255])
        with self.assertRaises(ValueError):
            IPv4("255.255.255.255.255")

    def test_cannot_create_when_too_few_octets(self):
        with self.assertRaises(ValueError):
            IPv4(255, 255, 255)
        with self.assertRaises(ValueError):
            IPv4([255, 255, 255])
        with self.assertRaises(ValueError):
            IPv4("255.255.255")

    def test_octet_cannot_be_out_of_range(self):
        with self.assertRaises(AddressOutOfRangeError):
            IPv4(256, 255, 255, 255)
        with self.assertRaises(AddressOutOfRangeError):
            IPv4([-1, 255, 255, 255])
        with self.assertRaises(AddressOutOfRangeError):
            IPv4("256.255.255.300")

    def test_can_increment_an_ip_address_using_an_int(self):
        self.assertEqual(IPv4(255, 255, 255, 254) + 1, IPv4(255, 255, 255, 255))
        self.assertEqual(IPv4(255, 255, 254, 0) + 256, IPv4(255, 255, 255, 0))
        self.assertEqual(IPv4(255, 254, 0, 0) + 256 ** 2, IPv4(255, 255, 0, 0))
        self.assertEqual(IPv4(254, 0, 0, 0) + 256 ** 3, IPv4(255, 0, 0, 0))

        with self.assertRaises(AddressOutOfRangeError):
            IPv4(255, 255, 255, 255) + 1

    def test_can_add_two_ip_addresses(self):
        self.assertEqual(IPv4(0, 0, 0, 0) + IPv4(0, 0, 0, 1), IPv4(0, 0, 0, 1))
        self.assertEqual(IPv4(0, 0, 0, 255) + IPv4(0, 0, 0, 1), IPv4(0, 0, 1, 0))
        with self.assertRaises(AddressOutOfRangeError):
            _ = IPv4(255, 255, 255, 255) + IPv4(0, 0, 0, 1)
