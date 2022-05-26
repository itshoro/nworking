from __future__ import annotations
from typing import List, Tuple, Union, overload
import nworking.helpers


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
        elif isinstance(octets[0], int):
            if octets[0] > 2 ** 32 - 1:
                raise AddressOutOfRangeError(octets)
            octets_list = []

            remaining_number = octets[0]
            # An octet always represents 1 byte (8 bit / 0xFF), to convert it into an octet we use the bitwise and operator
            # to selectively append the last byte.
            # Afterwards we shift the remaining number by 8 to remove the byte we just converted.
            for _ in range(4):
                octets_list.append(remaining_number & 0xFF)
                remaining_number >>= 8

            # As we append octets to the list the LSB (byte - not bit in this context) of the address is the first list element
            octets_list.reverse()

        self.verify(octets_list)
        self.octets = octets_list

    @overload
    def is_network_address(self, cidr: int) -> bool:
        """
        Returns true if the ip address is a network adress for a network given its CIDR notation
        """
        pass

    @overload
    def is_network_address(self, subnet_mask: IPv4) -> bool:
        """
        Returns true if the ip address is a network adress for a network given its subnet mask
        """
        pass

    def is_network_address(self, subnet_argument) -> bool:
        subnet_mask = (
            subnet_argument
            if isinstance(subnet_argument, IPv4)
            else nworking.helpers.cidr_to_subnet_mask(subnet_argument)
        )
        bit_string = subnet_mask.bit_repr()

        number_of_ones = bit_string.count("1")
        number_of_zeroes = 32 - number_of_ones

        # Starting at the first 0 in the subnet, check that the number of 0 bits in the network address
        # is the same as the number of 0 bits in the subnet mask
        return self.bit_repr()[number_of_ones:].count("0") == number_of_zeroes

    @overload
    def network_address(self, cidr: int) -> IPv4:
        """
        Returns the network address for an ip address, given a CIDR notation
        """
        pass

    @overload
    def network_address(self, subnet_mask: IPv4) -> IPv4:
        """
        Returns the network address for an ip address, given a subnet mask
        """
        pass

    def network_address(self, subnet_argument) -> IPv4:
        subnet_mask = (
            subnet_argument
            if isinstance(subnet_argument, IPv4)
            else nworking.helpers.cidr_to_subnet_mask(subnet_argument)
        )

        bit_string = subnet_mask.bit_repr()

        number_of_ones = bit_string.count("1")
        number_of_zeroes = 32 - number_of_ones

        network_address_binary = (
            self.bit_repr()[:number_of_ones] + "0" * number_of_zeroes
        )

        octets = [
            int(octet, 2)
            for octet in list(nworking.helpers.chunk(network_address_binary, 8))
        ]

        return IPv4(octets)

    def __repr__(self) -> str:
        return f"core.ipv4.IPv4({repr(self.octets)})"

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
            return parts == self.octets
        elif type(other) is IPv4:
            return self.octets == other.octets
        return False

    def __add__(self, other: object) -> IPv4:
        number_repr = 0
        if isinstance(other, IPv4):
            number_repr = int(other)
        elif isinstance(other, int):
            number_repr = other
        else:
            raise TypeError(f'Type "{str(type(other))}" cannot be added to IPv4')

        try:

            return IPv4(int(self) + number_repr)
        except ValueError as e:
            raise AddressOutOfRangeError(e.args[1]) from e

    def __sub__(self, other: object) -> IPv4:
        number_repr = 0
        if isinstance(other, IPv4):
            number_repr = int(other)
        elif isinstance(other, int):
            number_repr = other
        else:
            raise TypeError(f'Type "{str(type(other))}" cannot be subtracted from IPv4')

        try:
            return IPv4(int(self) - number_repr)
        except ValueError as e:
            raise AddressOutOfRangeError(e.args[1]) from e

    def __str__(self) -> str:
        return ".".join([str(x) for x in self.octets])

    def __int__(self) -> int:
        result = 0

        # Accumulate the octets to a coherent number.
        # An octet always represents 1 byte (8 bit), therefore we shift any given octet result its index times 8
        for octet_index in range(len(self.octets)):
            shift_factor = (3 - octet_index) * 8
            result += self.octets[octet_index] << shift_factor

        return result

    def verify(self, octets: Union[List[int], Tuple[int]]) -> None:
        if len(octets) != 4:
            raise ValueError(
                "An IPv4 address can only have 4 octets, received " + str(len(octets)),
                octets,
            )

        for octet in octets:
            if octet < 0 or octet > 255:
                raise AddressOutOfRangeError(octets)


class AddressOutOfRangeError(BaseException):
    def __init__(self, *address):
        address_repr = "Invalid Type"
        if isinstance(address[0], IPv4):
            address_repr = str(address[0])
        elif isinstance(address[0], str):
            address_repr = address[0]
        elif isinstance(address[0], list):
            address_repr = ".".join([str(arg) for arg in address[0]])

        super().__init__(
            "Addresses can only range from 0.0.0.0 to 255.255.255.255, received "
            + address_repr
        )


class Subnet:
    def __init__(self, network_address: IPv4, cidr: int) -> None:
        if network_address is None:
            network_address = IPv4(0, 0, 0, 0)
        self.verify(network_address, cidr)

        self.cidr = cidr
        self.network_address = network_address
        self.address_count = 2 ** (32 - cidr)
        self.host_address_count = self.address_count - 2
        self.subnet_mask = nworking.helpers.cidr_to_subnet_mask(cidr)
        self.broadcast_address = network_address + (self.address_count - 1)

    def __repr__(self) -> str:
        return f"core.ipv4.subnet({repr(self.network_address)}, {repr(self.cidr)})"

    def __str__(self) -> str:
        return f"Network Address: {self.network_address}, Broadcast Address: {self.broadcast_address}, # of Addresses: {self.address_count}, # of Hosts: {self.host_address_count})"

    def verify(self, network_address: IPv4, cidr: int):

        if cidr > 32 or cidr < 0:
            raise ValueError(
                "The CIDR notation only uses values between 0 and 32, received "
                + str(cidr)
            )

        if not network_address.is_network_address(cidr):
            raise ValueError(
                "The given address can't be a network address for this subnet."
            )
