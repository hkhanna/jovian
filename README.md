# jovian

## Check out the <a href="http://jovian.herokuapp.com/api/matches/">Live Demo</a>.

## TODO - Things to describe

- how I did edge case analysis
- admin/ user account
- API endpoint with pagination etc
- Mention auth and how it's out of scope but would make sense here

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

# Deployment

- Hosted on Heroku
- The database is the PostgreSQL Heroku add-on which has automated nightly backups.

## How to Deploy

- Push to `origin/main` and it will automatically trigger a deploy to Heroku.

## Production Environment Variables

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_SECRET_KEY=<random key>`
  - You can generate this random key with something like `openssl rand -base64 64`.
- `DATABASE_URL` is set by Heroku.
