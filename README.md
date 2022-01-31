# jovian

### Check out the <a href="https://jovian.herokuapp.com/api/matches/">Live Demo</a>.

## `/api/matches/` endpoint

There is only one endpoint. You can reach it at `/api/matches/`. If you access it with a web browser, it will return an
HTML-rendered representation of the endpoint that you can play around with (a so-called "browsable API" provided by Django Rest Framework).

This can be switched to JSON by passing the `Accept: application/json` header or by passing the [`?format=json` query parameter](https://jovian.herokuapp.com/api/matches/?format=json).
Something like `curl` will, by default, pass the `Accept: application/json` header, so this detail isn't generally something we'd need to worry about. The HTML-rendered return type does provide an easy way for us to explore the API together.

### Pagination

Pagination is provided in "limit offset" style. The browsable API should make it easy to explore this, but you can also manually pass a limit and offset as query params. E.g., [`/api/matches/?offset=100&limit=2`](https://jovian.herokuapp.com/api/matches/?offset=100&limit=2) to get users 101 and 102.

### Search Filter

A case-insensitive search filter is also available by passing the [`search` query parameter](https://jovian.herokuapp.com/api/matches/?search=research). This searches on a user's interests, and will only return users and roles that contain this search string. It is case-insensitive.

### Explanation of Overall Approach

I used Django & Django Rest Framework since I'm very familiar with those tools and I'd be able to work quickly.

The models are [defined here](https://github.com/hkhanna/jovian/blob/main/opps/models.py), but most of the application logic [can be found in the view](https://github.com/hkhanna/jovian/blob/main/opps/views.py).

### Ingestion of data

The [seed data management command](https://github.com/hkhanna/jovian/blob/main/opps/management/commands/seed_data.py) handles ingestion of data from JSON files stored in the repo. A [data migration](https://github.com/hkhanna/jovian/blob/main/opps/migrations/0002_auto_20220129_0117.py) makes sure this command is run once during setup of the database.

### Edge Cases

Before jumping too quickly into a solution, I thought it prudent to do some quick-and-dirty exploration of the data to get a handle on what the edge cases might look like.

I did this by writing a [management command](https://github.com/hkhanna/jovian/blob/main/opps/management/commands/edge_analysis.py) to print out any interest that was not met by a role and any role that was not met by an interest. The results:

```
{
    "Developer I",
    "Engineer I",
    "Safety Technician I",
    "Programmer I",
    "Accountant IV",
    "Geologist I",
    "Budget/Accounting Analyst II",
}
```

This helped guide the edge cases I prioritized.

### Possible Improvements

There are many possible edge cases that it would make sense to handle. The core challenge is that words that are close in meaning do not lend themselves well to string-based matching.

With time, I would experiment with common NLP techniques such as vectorizing all the words in the roles and interests using common and publicly available word embeddings. Then, calculate the cosine similarity or L2 normalized distance between the words and use that as a basis for (or as a factor in) comparing the roles and interests.

## Local Development

### Prerequisites

- Docker (for postgres).
- Python 3.8+

### Local Installation

- Clone the repo: `git clone git@github.com:hkhanna/jovian.git`
- Copy `.env.example` to `.env` and make any changes. Defaults have been picked to avoid interfering with other services you might have running.
- From within the repo directory, run `make all`

### Running Locally

- `make run` will load the application at `localhost:WEB_PORT`, where `WEB_PORT` is set in your `.env` file.

### Testing

- I avoid writing substantial code without at least _some_ tests. In this case, I only wrote [one](https://github.com/hkhanna/jovian/blob/main/opps/tests.py) just as a proof of concept, but if this were actually going to be used, I'd write more.
- `make check` will run all tests. You can also directly run `py.test` if you have the virtualenv activated.

# Runbook for Production Deployment

- Push to `origin/main` and it will automatically trigger a deploy to Heroku.

## Production Environment Variables

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_SECRET_KEY=<random key>`
  - You can generate this random key with something like `openssl rand -base64 64`.
- `DATABASE_URL` is set by Heroku.
