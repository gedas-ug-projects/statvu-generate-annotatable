class Team:
    """A class for keeping info about the teams"""

    color_dict = {
        1610612737: ('#C8102E', 'ATL'),
        1610612738: ('#007A33', 'BOS'),
        1610612751: ('#000000', 'BKN'),
        1610612766: ('#1D1160', 'CHA'),
        1610612741: ('#CE1141', 'CHI'),
        1610612739: ('#860038', 'CLE'),
        1610612742: ('#00538C', 'DAL'),
        1610612743: ('#0E2240', 'DEN'),
        1610612765: ('#C8102E', 'DET'),
        1610612744: ('#FFC72C', 'GSW'),
        1610612745: ('#C4CED4', 'HOU'),
        1610612754: ('#002D62', 'IND'),
        1610612746: ('#BEC0C2', 'LAC'),
        1610612747: ('#552583', 'LAL'),
        1610612763: ('#5D76A9', 'MEM'),
        1610612748: ('#F9A01B', 'MIA'),
        1610612749: ('#00471B', 'MIL'),
        1610612750: ('#0C2340', 'MIN'),
        1610612740: ('#85714D', 'NOP'),
        1610612752: ('#F58426', 'NYK'),
        1610612760: ('#007AC1', 'OKC'),
        1610612753: ('#007DC5', 'ORL'),
        1610612755: ('#ED174C', 'PHI'),
        1610612756: ('#1D1160', 'PHX'),
        1610612757: ('#E03A3E', 'POR'),
        1610612758: ('#5A2D81', 'SAC'),
        1610612759: ('#EF426F', 'SAS'),
        1610612761: ('#B4975A', 'TOR'),
        1610612762: ('#F9A01B', 'UTA'),
        1610612764: ('#002B5C', 'WAS'),
    }

    def __init__(self, id, isVisitor):
        self.id = id
        # self.name = Team.color_dict[id][1]
        self.color = Team.color_dict[id][0]
        if (isVisitor):
            self.color = '#FF0000'
        else:
            self.color = '#0000FF'
