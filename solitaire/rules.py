

def check(source, dest, cards):
    if len(cards) == 1:
        return _check_single_card_move(source, dest, cards[0])
    return _check_multiple_card_move(source, dest, cards)
    

def _check_single_card_move(source, dest, card):
    if "foundation" in dest.label:
        if card["suit"] == dest.label[11:]:
            if dest.cards:
                if dest.cards[-1]["power"] + 1 == card["power"]:
                    return True
                return False
            if card["power"] == 1:
                return True
            return False
        return False
    if dest.label == "tableau":
        if not dest.cards:
            if card["power"] == 13:
                return True
            return False
        if dest.cards[-1]["power"] - 1 == card["power"]:
            if dest.cards[-1]["color"] != card["color"]:
                return True
        return False
    return True
        

def _check_multiple_card_move(source, dest, cards):
    if dest.label == "tableau":
        if not dest.cards:
            if cards[0]["power"] == 13:
                return True
            return False
        if dest.cards[-1]["power"] - 1 == cards[0]["power"]:
            if dest.cards[-1]["color"] != cards[0]["color"]:
                return True
        return False
    return True