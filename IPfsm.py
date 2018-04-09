# This is the python implementation of checking for valid IP addresses.
# The server didn't use this. It is simply here for development purposes
# and clarity. A pattern compiler was used in the Android app.

from enum import Enum

class IPState(Enum):
    """States for the FSM that is used to verify sent IP addresses."""
    Octet1 = 1
    Dot1 = 2
    Octet2 = 3
    Dot2 = 4
    Octet3 = 5
    Dot3 = 6
    Octet4 = 7
    Done = 8
    Err = 9


def IPvalidate(IPstr):
    """
    Implementation of the FSM that validates proper IP addresses

    >>> IPvalidate("0.0.0.0") == True
    True
    >>> IPvalidate("255.255.255.255") == True
    True
    >>> IPvalidate("256.255.255.255") == True
    False
    >>> IPvalidate("-1.255.255.255") == True
    False
    >>> IPvalidate("255.256.255.255") == True
    False
    >>> IPvalidate("255.-1.255.255") == True
    False
    >>> IPvalidate("255.255.256.255") == True
    False
    >>> IPvalidate("255.255.-1.255") == True
    False
    >>> IPvalidate("255.255.255.256") == True
    False
    >>> IPvalidate("255.255.255.-1") == True
    False
    >>> IPvalidate("127.0.0.1") == True
    True
    >>> IPvalidate("0..0.0.0") == True
    False
    >>> IPvalidate("0.0.!~0.0") == True
    False
    >>> IPvalidate("0.0.0...0") == True
    False
    >>> IPvalidate("1.10.100,100") == True
    False
    >>> IPvalidate("1000.1.1.1") == True
    False
    >>> IPvalidate("") == True
    False
    """
    if not IPstr:
        return False

    currentstate = IPState.Octet1
    segment = ""
    chr = ''
    i = 0
    while i < len(IPstr):
        segment = ""
        chr = IPstr[i]
        if chr == '.':
            # this is the only ascii character we let through the checks
            # so it must be treated delicately
            if currentstate.name == "Octet1":
                return False
            elif currentstate.name == "Octet2":
                return False
            elif currentstate.name == "Octet3":
                return False
            elif currentstate.name == "Octet4":
                return False
            i += 1
            segment = '.'
        elif chr < "0" or chr > "9":  # elimates non-digits and not dots based on ascii values
            return False
        else:
            while chr >= "0" and chr <= "9":
                i += 1
                segment += chr
                if i == len(IPstr):
                    break
                chr = IPstr[i]
            segment = int(segment)

        if currentstate.name == "Octet1" and segment >= 0 and segment <= 255:
            currentstate = IPState.Dot1
        elif currentstate.name == "Dot1" and segment == ".":
            currentstate = IPState.Octet2
        elif currentstate.name == "Octet2" and segment >= 0 and segment <= 255:
            currentstate = IPState.Dot2
        elif currentstate.name == "Dot2" and segment == ".":
            currentstate = IPState.Octet3
        elif currentstate.name == "Octet3" and segment >= 0 and segment <= 255:
            currentstate = IPState.Dot3
        elif currentstate.name == "Dot3" and segment == ".":
            currentstate = IPState.Octet4
        elif currentstate.name == "Octet4" and segment >= 0 and segment <= 255:
            currentstate = IPState.Done
        else:
            currentstate = IPState.Err
            break

    return currentstate == IPState.Done
