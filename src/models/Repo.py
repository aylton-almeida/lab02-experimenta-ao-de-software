class Repo:

    cursor: str
    nameWithOwner: str
    url: str
    stargazerCount: str
    createdAt: str
    releases: int
    cbo: int
    dit: int
    wmc: int
    loc: int

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')

        if node := data.get('node'):
            self.nameWithOwner = node.get('nameWithOwner')
            self.url = node.get('url')
            self.stargazerCount = node.get('stargazerCount')
            self.createdAt = node.get('createdAt')

            if releases := node.get('releases'):
                self.releases = releases.get('totalCount')

    def add_ck_data(self, data: dict):
        self.cbo = data.get('cbo')
        self.dit = data.get('dit')
        self.wmc = data.get('wmc')
        self.loc = data.get('loc')
