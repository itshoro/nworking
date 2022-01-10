from __future__ import annotations
from typing import TYPE_CHECKING
import helpers

if TYPE_CHECKING:
    from . import IPv4


class Subnet:
    def __init__(self, network_address: IPv4, cidr: int) -> None:
        self.verify(network_address, cidr)

        self.cidr = cidr
        self.network_address = network_address
        self.address_count = 2 ** (32 - cidr)
        self.host_address_count = self.address_count - 2
        self.subnet_mask = helpers.cidr_to_subnet_mask(cidr)
        self.broadcast_address = network_address + (self.address_count - 1)

    def __str__(self) -> str:
        return f"Network Address: {self.network_address}, Broadcast Address: {self.broadcast_address}, # of Addresses: {self.address_count}, # of Hosts: {self.host_address_count})"

    def verify(self, network_address: IPv4, cidr: int):
        if network_address is None:
            return

        if cidr > 32 or cidr < 0:
            raise ValueError(
                "The CIDR notation only uses values between 0 and 32, received "
                + str(cidr)
            )

        if not network_address.is_network_address(cidr):
            raise ValueError(
                "The given address can't be a network address for this subnet."
            )
