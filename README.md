# Hub blog

The goal of this repo is to showcase a simple implementation of the backend of a blog service that allows:

- create articles
- upvote/downvote articles
- add comments to articles
- delete articles
- list articles by tags or keywords (words in title)

## How to run test

1. `cd hub-blog`
2. `python -m venv venv; source venv/bin/activate` (optional step to run in a virtualenv)
3. `pip install -r requirements.txt`
4. `pytest .`

## How to run spin up locally

### Prerequisites

- `docker` and `docker-compose`

This will build and run a docker container exposing port 5000 to your local machine.

1. `docker-compose up`
2. Now you can hit the api running with requests like

   Create article:
   ```shell
   curl localhost:5000/articles -d '{"title": "A new title", "content": "Lots of content.", "tags": ["finance", "tech"], "user_id": "fran"}' -H 'Content-Type: application/json' -X POST
   ```
   Get an article
   ```shell
   curl localhost:5000/articles/{SOME_ID_HERE}  -X GET
   ```
