# jovian

You can either run this locally or check out the <a href="http://jovian.herokuapp.com/">Live Demo</a>.

## Local Development

### Prerequisites

- Docker (for postgres).
- Python 3.8+
- `libtidy-dev` (e.g., `apt install libtidy-dev`)

### Local Installation

- Clone the repo: `git clone git@github.com:hkhanna/jovian.git`
- Copy `.env.example` to `.env` and make any changes. Defaults have been picked to avoid interfering with other services you might have running.
- From within the repo directory, run `make all`

### Running Locally

- `make run` will load the application at `localhost:WEB_PORT`, where `WEB_PORT` is set in your `.env` file.

### Testing

- `make check` will run all tests. You can also directly run `py.test` if you have the virtualenv activated.

# Deployment

- Hosted on Heroku
- The database is the PostgreSQL Heroku add-on which has automated nightly backups.
- Backend logging to Papertrail via Heroku.
  - Papertrail sends a pushover anytime the the logs match `at=ERROR OR at=CRITICAL`. It should send the email a maximum of once a day.
  - You cannot just look for `error` because they will match admin filtering for errors. You cannot look for `error -at=INFO` because something is emitting a log in Heroku with every request that doesn't include the `at=LEVEL`. It could be gunicorn, but after spending half a day on it, I've given up.

## How to Deploy

- Push to `origin/main` and it will automatically trigger a deploy to Heroku (after CI passes).

## Production Environment Variables

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_SECRET_KEY=<random key>`
  - You can generate this random key with something like `openssl rand -base64 64`.
- `LOGLEVEL=INFO`
  - Without this, it will use the default of `DEBUG`.
- `POSTMARK_API_KEY=<postmark key>`
- `DATABASE_URL` is set by Heroku.
