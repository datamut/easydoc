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

Build all the components (in the project root directory):

```shell
docker-compose build
```

Run all the components (in the same directory):

```shell
docker-compose up
```

Now you can access the website from: http://localhost:4200.

## Troubleshooting

As there are three services running in docker, and three ports will be exposed to host, please ensure 4200, 8087, and 5432 are not occupied.

You should be able to see errors (if any) when running the services from the terminal.
