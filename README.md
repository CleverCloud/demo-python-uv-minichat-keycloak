# MiniChat

A simple real-time chat application built with Flask and PostgreSQL, designed for Clever Cloud deployment.

## Requirements

- Python 3.12+
- PostgreSQL Clever Cloud add-on
- (optionnal) Keycloak Clever Cloud add-on

## Local Development

1. Install dependencies using uv:
```bash
uv sync
```

2. Set the PostgreSQL connection URI:
```bash
export POSTGRESQL_ADDON_URI="postgresql://user:password@host:port/database"
```

3. Run the application:
```bash
uv run main.py
```

The application will start on `http://0.0.0.0:9000`

## Clever Cloud Deployment
### Environment Configuration

For `uv` projects on Clever Cloud, you must configure the following:

1. **Port**: The application must listen on port **9000**

2. **Run Command**: Set the environment variable:
```
CC_RUN_COMMAND="uv run main.py"
```

### Prerequisites
- Clever Cloud account
- Clever Cloud CLI installed (optional)

### Deployment Steps
0. **Login** (if not already logged in):
```bash
clever login
```

1. **Create a PostgreSQL add-on** on Clever Cloud
```bash
clever addon create postgresql-addon minichat_postgresql
```

2. **Create a Python application**:
```bash
clever create minichat --type python --region par --org [ORGANISATION ID]
```

3. **Link the add-on to your application**:
```bash
clever service link-addon minichat_postgresql
```

4. **Set up environment variable**:
```bash
clever env set CC_PYTHON_VERSION "3.13"
clever env set CC_RUN_COMMAND "uv run main.py"
```
5. **Deploy**:
```bash
clever deploy
```
