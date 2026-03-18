import os
import random

board = []
players = []

def roll():
    num1, num2 = random.randint(1, 6), random.randint(1, 6)
    print(f"\n#####  #####\n# {num1} #  # {num2} #\n#####  #####")
    print(f"You rolled a total of {num1 + num2}!")
    return num1, num2

###############################################################################################################################################
#    Free   ##  Kentucky ##   Chance  ##  Indiana  ##  Illinois ##    B&O    ##  Atlantic ##  Ventnor  ##Water Works##   Marvin  ## Go to Jail#
#  Parking  ##   Avenue  ##           ##   Avenue  ##   Avenue  ##  Railroad ##   Avenue  ##   Avenue  ##           ##  Gardens  ##           #
#           ##           ##           ##           ##           ##           ##           ##           ##           ##           ##           #
#           ##    $220   ##           ##    $220   ##    $240   ##    $200   ##    $260   ##    $260   ##    $150   ##    $280   ##           #
###############################################################################################################################################
#  New York #                                                                                                                     #  Pacific  #
#   Avenue  #                                                                                                                     #   Avenue  #
#           #                                                                                                                     #           #
#    $200   #                                                                                                                     #    $300   #
#############                                                                                                                     #############
# Tennessee #                                                                                                                     #   North   #
#   Avenue  #                                                                                                                     #  Carolina #
#           #                                                                                                                     #   Avenue  #
#    $180   #               #######################################################################################               #    $300   #
#############               #   #       #    ######    #      ##    ######    ######    ######    ##   ##     ##  #               #############
# Community #               #   ##     ##  ###    ###  ####   ##  ###    ###  ##   ## ###    ###  ##    ##   ##   #               # Community #
#   Chest   #               #   #### #### ###      ### ## ### ## ###      ### ###### ###      ### ##      ####    #               #   Chest   #
#           #               #  ##  ###  ## ###    ###  ##   ####  ###    ###  ##      ###    ###  ##       ##     #               #           #
#           #               #  ##   #   ##   ######    ##      #    ######    ##        ######    ######  ##      #               #           #
#############               #######################################################################################               #############
# St. James #                                                                                                                     #Pennsylvani#
#   Place   #                                                                                                                     #  a Avenue #
#           #                                                                                                                     #           #
#    $180   #                                                                                                                     #    $320   #
#############                                                                                                                     #############
#Pennsylvani#                                                                                                                     # Short Line#
# a Railroad#                                                                                                                     #           #
#           #                                                                                                                     #           #
#    $200   #                                                                                                                     #    $200   #
#############                                                                                                                     #############
#  Virginia #                                                                                                                     #   Chance  #
#   Avenue  #                                                                                                                     #           #
#           #                                                                                                                     #           #
#    $160   #                                                                                                                     #           #
#############                                                                                                                     #############
#   States  #                                                                                                                     # Park Place#
#   Avenue  #                                                                                                                     #           #
#           #                                                                                                                     #           #
#    $140   #                                                                                                                     #    $350   #
#############                                                                                                                     #############
#  Electric #                                                                                                                     # Luxury Tax#
#  Company  #                                                                                                                     #           #
#           #                                                                                                                     #           #
#    $150   #                                                                                                                     #           #
#############                                                                                                                     #############
# St.Charles#                                                                                                                     # Boardwalk #
#   Place   #                                                                                                                     #           #
#           #                                                                                                                     #           #
#    $140   #                                                                                                                     #    $400   #
###############################################################################################################################################
# Jail/Just ##Connecticut##  Vermont  ##   Chance  ##  Oriental ##  Reading  ## Income Tax##   Baltic  ## Community ##Mediterrane##     Go    #
#  Visiting ##   Avenue  ##   Avenue  ##           ##   Avenue  ##  Railroad ##           ##   Avenue  ##   Chest   ## an Avenue ##           #
#           ##           ##           ##           ##           ##           ##           ##           ##           ##           ##           #
#           ##    $100   ##    $100   ##           ##    $100   ##    $200   ##           ##    $60    ##           ##    $60    ##           #
###############################################################################################################################################

# I handmade the monopoly logo based on the original logo

def build_board():
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("#" * 143)
    for i in range(4):
        print("".join(f"#{board[j + 20].tile()[i]}#" for j in range(11)))
    print("#" * 143)
    
    scoreboard = ["--- SCOREBOARD ---"]
    for p in players:
        if getattr(p, 'bankrupt', False):
            scoreboard.append(f"Player {p.name} [BANKRUPT]")
            scoreboard.append("")
        else:
            houses = sum(getattr(item, 'houses', 0) for item in p.inventory if not isinstance(item, str))
            scoreboard.append(f"Player {p.name}: ${p.money}")
            
            loc_name = board[p.position].name if hasattr(board[p.position], 'name') else type(board[p.position]).__name__
            status_str = f"Jail: {p.injail} turn(s)" if p.injail > 0 else f"On: {loc_name}"
            scoreboard.append(f"{status_str} | Properties: {len([item for item in p.inventory if not isinstance(item, str)])} | Houses: {houses}")
            scoreboard.append("")

    sb_idx = 0
    
    for j in range(9):
        inbetween = " " * 117
        for i in range(4):
            if j == 1 and i == 3:
                inbetween = ("#" * 87).center(117)
            elif j == 2:
                match i:
                    case 0:
                        inbetween = ("#   ##     ##  ###    ###  ####   ##  ###    ###  ##   ## ###    ###  ##    ##   ##   #").center(117)
                    case 1:
                        inbetween = ("#   #### #### ###      ### ## ### ## ###      ### ###### ###      ### ##      ####    #").center(117)
                    case 2:
                        inbetween = ("#  ##  ###  ## ###    ###  ##   ####  ###    ###  ##      ###    ###  ##       ##     #").center(117)
                    case 3:
                        inbetween = ("#  ##   #   ##   ######    ##      #    ######    ##        ######    ######  ##      #").center(117)
            elif 4 <= j <= 7:
                if sb_idx < len(scoreboard):
                    inbetween = scoreboard[sb_idx].center(117)
                    sb_idx += 1
                else:
                    inbetween = " " * 117
            print(f"#{board[19 - j].tile()[i]}#" + inbetween + f"#{board[31 + j].tile()[i]}#")
        match j:
            case 1:
                inbetween = ("#   #       #    ######    #      ##    ######    ######    ######    ##   ##     ##  #").center(117)
            case 2:
                inbetween = ("#" * 87).center(117)
            case 8:
                inbetween = "#" * 117
            case _:
                if 4 <= j <= 7 and sb_idx < len(scoreboard):
                    inbetween = scoreboard[sb_idx].center(117)
                    sb_idx += 1
                else:
                    inbetween = " " * 117
        print("#" * 13 + inbetween + "#" * 13)
        
    for i in range(4):
        print("".join(f"#{board[j].tile()[i]}#" for j in range(10, -1, -1)))
    print("#" * 143)