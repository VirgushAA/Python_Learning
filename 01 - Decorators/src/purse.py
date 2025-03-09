from decorators import squeak


@squeak
def add_ingot(purse: dict[str, int]) -> dict[str, int]:
    if "gold_ingots" in purse: tmp: dict[str,int] = {"gold_ingots": purse["gold_ingots"] + 1}
    else: tmp: dict[str,int] = {"gold_ingots" : 1}
    return tmp


@squeak
def get_ingot(purse: dict[str, int]) -> dict[str, int]:
    if "gold_ingots" in purse and purse["gold_ingots"] > 0:
        tmp: dict[str,int] = {"gold_ingots": purse["gold_ingots"] - 1}
    else:
        tmp: dict[str,int] = {}
    return tmp


@squeak
def empty(purse: dict[str, int]) -> dict[str, int]:
    tmp: dict[str,int] = {}
    return tmp


def split_booty(*purses: dict[str,int]) -> dict[str,int]:
    booty: int = 0
    for purse in purses:
        if "gold_ingots" in purse and purse["gold_ingots"] >= 0:
            booty += purse["gold_ingots"]
    one: int = 0
    two: int = 0
    three: int = 0
    while booty > 0:
        if two > three:
            three += 1
        else:
            if one > two:
                two += 1
            else:
                one += 1
        booty -= 1
    purse_one: dict[str,int] = {"gold_ingots": one}
    purse_two: dict[str,int] = {"gold_ingots": two}
    purse_tree: dict[str,int] = {"gold_ingots": three}
    return purse_one, purse_two, purse_tree