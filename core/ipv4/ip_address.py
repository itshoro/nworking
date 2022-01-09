from __future__ import annotations
from typing import List, Tuple, Union, TYPE_CHECKING, overload
import helpers


class IPv4:
    def __init__(self, octets: Union[List[int], str]):
        self.verify(octets)
        self.octets = octets

    def __init__(self, *octets):
        octets_list = None

        if len(octets) > 1:
            # octets is a tuple
            octets_list = list(octets)
        elif isinstance(octets[0], list):
            octets_list = octets[0]
        elif isinstance(octets[0], str):
            octets_list = [int(octet) for octet in octets[0].split(".")]

        self.verify(octets_list)
        self.octets = octets_list

    """
    Returns true if the ip address is a network adress for a network given its CIDR notation
    """

    @overload
    def is_network_address(self, cidr: int) -> bool:
        pass

    """
    Returns true if the ip address is a network adress for a network given its subnet mask
    """

    @overload
    def is_network_address(self, subnet_mask: IPv4) -> bool:
        pass

    def is_network_address(self, subnet_argument) -> bool:
        subnet_mask = (
            subnet_argument
            if isinstance(subnet_argument, IPv4)
            else helpers.cidr_to_subnet_mask(subnet_argument)
        )
        bit_string = subnet_mask.bit_repr()

        number_of_ones = bit_string.count("1")
        number_of_zeroes = 32 - number_of_ones

        # Starting at the first 0 in the subnet, check that the number of 0 bits in the network address
        # is the same as the number of 0 bits in the subnet mask
        return self.bit_repr()[number_of_ones:].count("0") == number_of_zeroes

    """
    Returns the network address for an ip address, given a CIDR notation
    """

    @overload
    def network_address(self, cidr: int) -> IPv4:
        pass

    @overload
    def network_address(self, subnet_mask: IPv4) -> IPv4:
        pass

    def network_address(self, subnet_argument) -> IPv4:
        subnet_mask = (
            subnet_argument
            if isinstance(subnet_argument, IPv4)
            else helpers.cidr_to_subnet_mask(subnet_argument)
        )

        bit_string = subnet_mask.bit_repr()

        number_of_ones = bit_string.count("1")
        number_of_zeroes = 32 - number_of_ones

        network_address_binary = (
            self.bit_repr()[:number_of_ones] + "0" * number_of_zeroes
        )

        octets = [
            int(octet, 2) for octet in list(helpers.chunk(network_address_binary, 8))
        ]

        return IPv4(octets)

    def bit_repr(self) -> str:
        ip_address_number = 0
        for i, octet in enumerate(self.octets):
            ip_address_number += octet << ((3 - i) * 8)

        bin_repr = bin(ip_address_number)[2:]
        if len(bin_repr) < 32:
            # Pad with leading zeroes
            bin_repr = "0" * (32 - len(bin_repr)) + bin_repr
        return bin_repr

    def __eq__(self, other: object) -> bool:
        if type(other) is str:
            try:
                parts = [int(x) for x in other.split(".")]
                self.verify(parts)
            except Exception:
                # This can either fail if the string had non-number characters or due to the verification
                return False
            return parts == self
        elif type(other) is IPv4:
            return self.octets == other.octets
        return False

    def __str__(self) -> str:
        return ".".join([str(x) for x in self.octets])

    def verify(self, octets: Union[List[int], Tuple[int]]) -> None:
        if len(octets) != 4:
            raise ValueError(
                "An IPv4 address can only have 4 octets, received " + str(len(octets))
            )

        for octet in octets:
            if octet < 0 or octet > 255:
                raise ValueError(
                    "Each octet has to be a value between 0 and 255, received "
                    + str(octet)
                )
