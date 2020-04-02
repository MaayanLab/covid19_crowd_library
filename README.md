# covid19

An interface to submit, serve, and analyze COVID19 related gene and drug sets.

## Development

The entrypoint of the application is in `covid19/app/app.py`; do not change the name of the file or directory.

### Getting Started
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running in development
```bash
source venv/bin/activate
python run.py
```

And visit <http://localhost:8080/covid19>.

### Installing new dependencies

#### Python dependencies
Ensure you update `requirements.txt` whenever installing a new dependency with `pip`.

#### System dependencies
In the case of extra (debian) system dependencies, add them to `deps.txt`.

## Database

The `.env.example` and `docker-compose.yml` can be used to establish a local database.

- `docker-compose up -d database`: will start the database
- `alembic current`: will show you the current migrations on the active database (defined in .env)
- `alembic upgrade +1`: apply database migrations on the active database (defined in .env)
- `alembic downgrade -1`: revert database migrations on the active database (defined in .env)

## Deployment

### Build for deployment
```bash
docker-compose build app
```

### Deploy
```bash
docker-compose push app
```

### Execute locally
```
docker-compose run app
```
