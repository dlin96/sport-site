TEAM_NAMES = \
    ('texans', 'titans', 'colts', 'jaguars',              # AFC South
     'ravens', 'browns', 'bengals', 'steelers',           # AFC North
     'raiders', 'chiefs', 'chargers', 'broncos',          # AFC West
     'patriots', 'dolphins', 'bills', 'jets',             # AFC East
     'cowboys', 'eagles', 'redskins', 'giants',           # NFC East
     'bears', 'lions', 'packers', 'vikings',              # NFC North
     'falcons', 'saints', 'panthers', 'buccaneers',       # NFC South
     'seahawks', 'niners', 'rams', 'cardinals')           # NFC West

EXCEPTION_DICT = {
    "texans": "houstontexans",
    "titans": "titansonline",
    "ravens": "baltimoreravens",
    "browns": "clevelandbrowns",
    "broncos": "denverbroncos",
    "dolphins": "miamidolphins",
    "bills": "buffalobills",
    "jets": "newyorkjets",
    "cowboys": "dallascowboys",
    "eagles": "philadelphiaeagles",
    "bears": "chicagobears",
    "lions": "detroitlions",
    "falcons": "atlantafalcons",
    "saints": "neworleanssaints",
    "niners": "49ers",
    "rams": "therams",
    "cardinals": "azcardinals"
}

POSITIONS = ('WR', 'LWR', 'RWR', 'WR1', 'WR2', 'LT', 'LG', 'C', 'RG', 'RT', 'TE',
             'QB', 'RB', 'SE', 'FL', 'FB', 'RB2')


def create_url(team_name, ending):
    if team_name in EXCEPTION_DICT:
        team_name = EXCEPTION_DICT[team_name]
    url = "https://www.{}.com/" + ending + "/"
    return url.format(team_name)
