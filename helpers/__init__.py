import core.ipv4.ip_address


def cidr_to_subnet_mask(cidr: int):
    if cidr > 32 or cidr < 0:
        raise ValueError(
            "CIDR notation only supports values between 0 and 32, received " + str(cidr)
        )

    # ~((1 << x) - 1) == (1 << (x-1)) + (1 << (x-2)) + ...
    cidr_to_number_repr = ~((1 << (32 - cidr)) - 1)

    # Store 40 bits, as in the case of cidr=0 we would receive a number where bit 33 would be
    # the first set bit, and to_bytes therefor thinking we wouldn't be able to store the number,
    # even though we only care for bits 0 through 32.
    #
    # We circumvent this by skipping the first byte (8 bit) using array operations.
    network_bytes = cidr_to_number_repr.to_bytes(5, "big", signed=True)[1:]
    network_octets = [
        int.from_bytes([byte], "big", signed=False) for byte in network_bytes
    ]

    return core.ipv4.ip_address.IPv4(network_octets)


def chunk(array: list, chunk_size: int):
    for i in range(0, len(array), chunk_size):
        yield array[i : i + chunk_size]
