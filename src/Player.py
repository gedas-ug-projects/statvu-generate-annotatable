from .Team import Team

class Player:
    id: int
    fname: str
    lname: str
    jersey: int
    team: Team
    def __init__(self, id, fname, lname, jersey_number, team: Team):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.jersey = jersey_number
        self.team = team

    def __repr__(self):
        return f"[id: {self.id}, fname: {self.fname}, lname: {self.lname}, jersey: {self.jersey}, team: {self.team.id}"