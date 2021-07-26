# A simple website to extract Invoice data

## Components/Environment

+ UI
    + Angular
+ API
    + FastAPI
+ PostgreSQL DB
+ E2E
    + docker-compose

## Usage

Passwords/Secrets are not included in the code base, you'll need to configure them in your own `.env` file. The following veriables are required:

```yaml
# .env file

DB_PASSWORD=your_appuser_password
AI_CLIENT_ID=sypht_client_id
AI_CLIENT_SECRET=sypht_client_secret
POSTGRES_PASSWORD=postgresql_db_root_password
```

Build all the components (in the project root directory):

```shell
docker-compose build
```

Run all the components (in the same directory):

```shell
docker-compose up
```

Now you can access the website from: http://localhost:4200.

## Tests

Only provided unittests for the API components. No unittests for UI.

Unittests can be running in the docker container (`test.Dockerfile`). The following commands will run the unittests:

```shell
docker build -t test_easydoc_api -f test.Dockerfile .

docker run -it test_easydoc_api
```


## Troubleshooting

As there are three services running in docker, and three ports will be exposed to host, please ensure 4200, 8087, and 5432 are not occupied.

You should be able to see errors (if any) when running the services from the terminal.
