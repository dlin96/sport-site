import urllib
import json
import re, pprint
from pymongo import MongoClient
# from bs4 import BeautifulSoup

# String Values to access fields of JSON object
players = "players"
first_name = "fname"
last_name = "lname"
id = "id"
formations = "formations"
offense = "Offense"
defense = "Defense"
base = "Base"
position_id = "positionID"
url_head = "http://www."
depth_chart_url_tail = "depth-chart"
html_tail = ".html"
depth_chart_path = ".com/team/"
patriots_url_path = ".com/schedule-and-stats/"
file_name_tail = "_DepthChart."
json_extension = "json"
text_extension = "txt"
JSON_path = "JSON_files/"
txt_path = "txt_files/"
space = " "
new_line = '\n'
player_dict = {}
team_dict = {}
exception_dict = {}
dc = {}
without_html_dict = {
    'patriots': 'patriots',
    'chargers': 'chargers',
    'cowboys': 'cowboys',
    'seahawks': 'seahawks'
}
# pattern to get position name from HTML source. Used for regular expressions.
html_position_pattern = (
    '<td class="field_position">'
    '<div class="field field--name-field-position field--type-taxonomy-term-reference field--label-hidden">'
    '<div class="field__items"><div class="field__item even">(\w+)</div>')
# used to get player names from each position.
html_player_pattern = 'class="player">(\w+\s\w+)</a>'

connection = MongoClient('localhost', 27017)
db = connection['fantasy-football-db']

def insert_team_list():
	collection = db['teams']
	collection.insert(team_dict)
	db.collection_names(include_system_collections=False)
	pprint.pprint(collection.find_one())


def insert_dc(team_name):
	collection = db[team_name]
	collection.insert(dc)
	db.collection_names(include_system_collections=False)
	pprint.pprint(collection.find_one())


# This method populates the team dictionary with the team name as the key and the URL version of team name as value
def populate_teams_dict():
    with open("teamnames.txt", 'r') as team_names:
        for team_key in team_names:
            val = team_names.next()
            key = team_key.rstrip(new_line)
            value = val.rstrip(new_line)
            team_dict[key] = value



# populate the dictionaries containing the teams that don't use JSON objects for depth charts
def populate_exception_dict():
    with open("exception_teams.txt", 'r') as without_json:
        for team_key in without_json:
            val = without_json.next()
            key = team_key.rstrip(new_line)
            value = val.rstrip(new_line)
            exception_dict[key] = value


def create_url(team_name):
    url = url_head + team_dict[team_name]
    if team_name == 'patriots':
        url += patriots_url_path + depth_chart_url_tail
    else:
        url += depth_chart_path + depth_chart_url_tail
    if team_name not in without_html_dict:
        url += html_tail
    return url


# create the file name based on the file type. I.e. Files containing JSON objects go into JSON folder.
def create_file_name(team_name, extension):
    if extension == json_extension:
        file_name = JSON_path + team_name + file_name_tail + extension
    else:
        file_name = txt_path + team_name + file_name_tail + extension
    return file_name


# get position list from teams that use HTML to store their depth charts.
def get_html_depth_chart(team_name):
    url = create_url(team_name)
    response = urllib.urlopen(url)
    data = response.read()
    positions = re.findall(html_position_pattern, data)
    player = re.findall(html_player_pattern, data)
    print positions
    print player


# get the depth chart from JSON objects.
def get_depth_chart_json(team_name):
    url = create_url(team_name)
    response = urllib.urlopen(url)
    data = response.read()
    latter_half = re.split("depthChartJson = ", data)
    json_object = re.split("</script>", latter_half[1])
    depth_chart = json_object[0]

    # write JSON object to file
    log_file = open(create_file_name(team_name, json_extension), "w+")
    log_file.write(depth_chart)
    log_file.close()


# set the player dictionary for the team name.
def set_player_dict(team_name):

    with open(create_file_name(team_name, json_extension)) as json_data:	# open team JSON file
        data = json.load(json_data)

    for index in range(len(data[players])):		# go through player list and get name
        player_name = data[players][index][first_name] + space + data[players][index][last_name]

        # store player names under their ID value
        player_id = data[players][index][id]
        player_dict[player_id] = player_name

    return data


# get the starters of the team. 
# TODO: rename this. This function no longer gets the starters
def get_starters(team_name):

	dc.clear()
	data = set_player_dict(team_name)

# get offensive players from JSON. Write depth chart to file. 
	for index in range(len(data[formations][offense][base])):
		# position
		position = data[formations][offense][base][index][position_id]
		player_list = []

		for i in range(len(data[formations][offense][base][index][players])):
			# player names
			player_list.append(player_dict[data[formations][offense][base][index][players][i]].encode('utf-8'))
		if position in dc:
			# append list for now to separate between WR1 and WR2
			dc[position].append(player_list)
		else:
			dc[position] = player_list

	# no support for defense yet
	# for index in range(len(data[formations][defense][base])):
	# 	position = data[formations][defense][base][index][position_id]
	# 	player_list = []

	# 	for i in range(len(data[formations][defense][base][index][players])):
	# 		player_list.append(player_dict[data[formations][defense][base][index][players][i]])
	# 		dc[position] = player_list


def main(team_name):
	if team_name not in team_dict:
		print "Not a valid team name."
		return
	if team_name in without_html_dict:
		get_html_depth_chart(team_name)
	else:
		get_depth_chart_json(team_name)
		set_player_dict(team_name)
		get_starters(team_name)
		insert_dc(team_name)
	connection.close()


def populate():
    populate_teams_dict()
    populate_exception_dict()