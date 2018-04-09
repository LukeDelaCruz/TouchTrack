import pyautogui


sensitivity_factor = 4.5  # recommended to be in the range [3,5] for comfort
leap_bound = 20  # assertion that the cursor can't be moved more than 25 pixels
pyautogui.PAUSE = 0.01  # remove delay! can't be zero from hardware limitations
pyautogui.FAILSAFE = False  # allow for the corners to be reached by the cursor


def oneTouchTracker(message, received_coords):
    """
    Process one finger mouse tracking network requests.
    """
    if message == "C":
        pyautogui.click()
        received_coords[0][1] = False
    elif message == "RC":
        pyautogui.click(button='right')
        received_coords[0][1] = False
    else:
        coords = message.split(",")
        new_x = int(coords[0].strip())
        new_y = int(coords[1].strip())

        if not received_coords[0][1]:
            received_coords[0][0][0] = new_x
            received_coords[0][0][1] = new_y
            received_coords[0][1] = True
        elif not received_coords[1]:
            curr_x, curr_y = pyautogui.position()
            trans_x = (new_x - received_coords[0][0][0])
            trans_y = (new_y - received_coords[0][0][1])
            if abs(trans_x) > leap_bound or abs(trans_y) > leap_bound:
                received_coords[0][1] = False
                return received_coords
            trans_x *= sensitivity_factor
            trans_y *= sensitivity_factor
            pyautogui.moveTo(curr_x + trans_x , curr_y + trans_y)
            received_coords[0][1] = False

    return received_coords
