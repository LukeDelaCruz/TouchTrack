from enum import Enum

class IPState(Enum):  # Python enums as a class
    """
    States for the FSM that is used to verify sent IP addresses.
    The finite states are symbolized as octets.
    The .name member of this class is used to identify the current state of
    the machine as seen in the IPvalidate function.
    """
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
    >>> IPvalidate("") == True
    False
    """
    if not IPstr:
        return False

    currentstate = IPState.Octet1
    segment = ""  # for numbers with more than one digits
    chr = ''  # holder for individual characters
    i = 0  # used to traverse the string
    while i < len(IPstr):
        segment = ""
        chr = IPstr[i]
        if chr == '.':
            i += 1
            segment = '.'
        else: # get the number which could contain more than 1 digit
            while chr >= "0" and chr <= "9":
                i += 1
                segment += chr
                if i == len(IPstr):
                    break
                chr = IPstr[i]

        # similar style of implementation as in Cmput 274
        # note that this finite state machine is fairly linear but the numbers
        # had to be treated delicately
        if currentstate.name == "Octet1" and segment >= "0" and segment <= "255":
            currentstate = IPState.Dot1
        elif currentstate.name == "Dot1" and segment == ".":
            currentstate = IPState.Octet2
        elif currentstate.name == "Octet2" and segment >= "0" and segment <= "255":
            currentstate = IPState.Dot2
        elif currentstate.name == "Dot2" and segment == ".":
            currentstate = IPState.Octet3
        elif currentstate.name == "Octet3" and segment >= "0" and segment <= "255":
            currentstate = IPState.Dot3
        elif currentstate.name == "Dot3" and segment == ".":
            currentstate = IPState.Octet4
        elif currentstate.name == "Octet4" and segment >= "0" and segment <= "255":
            currentstate = IPState.Done
        else:
            currentstate = IPState.Err
             # automatically break when in the error state to avoid an
             # infinite while loop
            break

    return currentstate == IPState.Done  # The done state is considered valid
