from __future__ import annotations
from pandas.core.series import Series
from datetime import datetime, timezone


class Repo:

    cursor: str
    nameWithOwner: str
    url: str
    stargazerCount: str
    age: str
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
            self.age = (datetime.now(
                timezone.utc) - datetime.fromisoformat(node.get('createdAt').replace('Z', '+00:00'))).days

            if releases := node.get('releases'):
                self.releases = releases.get('totalCount')

    def add_ck_data(self, data: dict):
        self.cbo = data.get('cbo')
        self.dit = data.get('dit')
        self.wmc = data.get('wmc')
        self.loc = data.get('loc')

    @staticmethod
    def from_dataframe(data: Series) -> Repo:
        return Repo({
            'cursor': data['cursor'],
            'node': {
                'nameWithOwner': data['nameWithOwner'],
                'url': data['url'],
                'stargazerCount': data['stargazerCount'],
                'createdAt': data['createdAt'],
                'releases': {
                    'totalCount': data['releases']
                },
            }
        })
