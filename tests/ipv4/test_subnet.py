import unittest
from core import IPv4
from core import Subnet


class TestSubnet(unittest.TestCase):
    def test_generates_proper_subnet_masks_using_cidr(self):
        mask = Subnet(None, 0)
        self.assertEqual(mask.subnet_mask, IPv4(0, 0, 0, 0))
        mask = Subnet(None, 1)
        self.assertEqual(mask.subnet_mask, IPv4(128, 0, 0, 0))
        mask = Subnet(None, 2)
        self.assertEqual(mask.subnet_mask, IPv4(192, 0, 0, 0))
        mask = Subnet(None, 3)
        self.assertEqual(mask.subnet_mask, IPv4(224, 0, 0, 0))
        mask = Subnet(None, 4)
        self.assertEqual(mask.subnet_mask, IPv4(240, 0, 0, 0))
        mask = Subnet(None, 5)
        self.assertEqual(mask.subnet_mask, IPv4(248, 0, 0, 0))
        mask = Subnet(None, 6)
        self.assertEqual(mask.subnet_mask, IPv4(252, 0, 0, 0))
        mask = Subnet(None, 7)
        self.assertEqual(mask.subnet_mask, IPv4(254, 0, 0, 0))
        mask = Subnet(None, 8)
        self.assertEqual(mask.subnet_mask, IPv4(255, 0, 0, 0))
        mask = Subnet(None, 9)
        self.assertEqual(mask.subnet_mask, IPv4(255, 128, 0, 0))
        mask = Subnet(None, 10)
        self.assertEqual(mask.subnet_mask, IPv4(255, 192, 0, 0))
        mask = Subnet(None, 11)
        self.assertEqual(mask.subnet_mask, IPv4(255, 224, 0, 0))
        mask = Subnet(None, 12)
        self.assertEqual(mask.subnet_mask, IPv4(255, 240, 0, 0))
        mask = Subnet(None, 13)
        self.assertEqual(mask.subnet_mask, IPv4(255, 248, 0, 0))
        mask = Subnet(None, 14)
        self.assertEqual(mask.subnet_mask, IPv4(255, 252, 0, 0))
        mask = Subnet(None, 15)
        self.assertEqual(mask.subnet_mask, IPv4(255, 254, 0, 0))
        mask = Subnet(None, 16)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 0, 0))
        mask = Subnet(None, 17)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 128, 0))
        mask = Subnet(None, 18)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 192, 0))
        mask = Subnet(None, 19)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 224, 0))
        mask = Subnet(None, 20)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 240, 0))
        mask = Subnet(None, 21)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 248, 0))
        mask = Subnet(None, 22)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 252, 0))
        mask = Subnet(None, 23)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 254, 0))
        mask = Subnet(None, 24)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 0))
        mask = Subnet(None, 25)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 128))
        mask = Subnet(None, 26)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 192))
        mask = Subnet(None, 27)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 224))
        mask = Subnet(None, 28)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 240))
        mask = Subnet(None, 29)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 248))
        mask = Subnet(None, 30)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 252))
        mask = Subnet(None, 31)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 254))
        mask = Subnet(None, 32)
        self.assertEqual(mask.subnet_mask, IPv4(255, 255, 255, 255))

    def test_raises_an_error_when_exceeding_cidr_bounds(self):
        with self.assertRaises(ValueError):
            Subnet(None, 33)
        with self.assertRaises(ValueError):
            Subnet(None, -1)
