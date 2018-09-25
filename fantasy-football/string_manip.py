

# player_list="WR DeAndre Hopkins Vyncint Smith LT Julie'n Davenport Martinas Rankin LG Senio Kelemete C Nick Martin Greg Mancz RG Zach Fulton RT Seantrel Henderson Kendall Lamm TE Ryan Griffin Jordan Akins Jordan Thomas WR Bruce Ellington Keke Coutee WR Will Fuller V Sammie Coates Jr. QB Deshaun Watson Brandon Weeden Joe Webb RB Lamar Miller Alfred Blue Tyler Ervin Buddy Howell"

def make_player_dict(player_list):
    count = 0
    name = ''
    positions = ('WR', 'LT', 'LG', 'C', 'RG', 'RT', 'TE', 'QB', 'RB', 'SE', 'FL', 'FB')
    suffixes = ('Sr.', 'Jr.', 'II', 'III', 'V')
    pos = []
    names = []

    temp_list = []

    for word in player_list.split():
        if word in positions:
            if name:
                temp_list.append(name)
                name = ""
            if temp_list:
                names.append(temp_list)
                temp_list = []
                count = 0
            pos.append(word)
            continue
        if count < 2 or word in suffixes:
            count = count + 1
            if name:
                name = name + " " + word
            else:
                name = name + word
        else:
            if name:
                temp_list.append(name)
            name = word
            count = 1

    temp_list.append(name)
    names.append(temp_list)

    # TODO: add logging.
    # print(pos)
    # print(names)
    player_dict = {}

    for i in range(len(pos)):
        # print(i)
        # print(len(pos))
        # print(len(names))
        position = pos[i]
        if position in player_dict:
            player_dict[position].append(tuple(names[i]))
        else:
            player_dict[position] = [tuple(names[i])]

    return player_dict
