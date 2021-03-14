import requests
import json
from requests.models import Response


def get_query(repos_per_request: int, cursor: str = None):
    ###
    # build api query
    # ###
    return """
    query example {
    search(type: REPOSITORY, first: %(repos)i, query: "stars:>100 language:java", after: %(after)s) {
      edges {
        cursor
        node {
          ... on Repository {
              nameWithOwner
              url
              stargazerCount
              createdAt
              releases {
                  totalCount
              }
            }
          }
        }
      }
    }
    """ % {'repos': repos_per_request, "after": ('"{}"'.format(cursor) or 'null')}


def get_repos_data(url: str, query: str, token: str):
    response: Response = requests.post(url, json={'query': query}, headers={
        'Authorization': token
    })

    if response.status_code != 200 or 'errors' in response.text:
        print(response.text)
        raise Exception(
            'There was an error while trying to make the request')

    json_data: dict = json.loads(response.text)

    return json_data['data']['search']['edges']
