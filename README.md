# MiniChat

A simple real-time chat application built with Flask and PostgreSQL, designed for Clever Cloud deployment.

## Description
In this demo is designed for two kind of deployment:
1) A native chat based on PostgreSQL backend without authentication.
2) Adding a Keycloak based authentication and user management layer.

This is why there is two files `main.py` and `main_with_keycloak.py`, and two indexes `index.html` and `secure_index.html`.

## Requirements

- Python 3.12+
- PostgreSQL Clever Cloud add-on
- (optionnal) Keycloak Clever Cloud add-on

## Clever Cloud Deployment - With Terraform
1. **Add your Organisation ID** in `terraform/clevercloud.tf` file (line 13)
2. **Initialize Terraform**:
```bash
terraform init
terraform apply
```

> to remove the resources created by terraform, run `terraform destroy`

## Clever Cloud Deployment - From local repository
### Environment Configuration

For `uv` projects on Clever Cloud, the application must listens on port `9000` with `0.0.0.0` as host.

- **Run Command**: Set the environment variable:
```
CC_RUN_COMMAND="uv run main.py"
```

### Prerequisites
- Clever Cloud account
- Clever Cloud CLI installed (optional)

### Deployment Steps
#### No security layer
0. **Login** (if not already logged in):
```bash
clever login
```

1. **Create a PostgreSQL add-on** on Clever Cloud
```bash
clever addon create postgresql-addon --org [ORGANISATION ID] minichat_postgresql
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

#### Add a user management with a Keycloak add-on

6. **Create a Keycloak add-on**:
```bash
clever addon create keycloak --org [ORGANISATION ID] minichat_keycloak
```

7. **Link the add-on to your application**:
```bash
clever service link-addon minichat_keycloak
```

8. **Set up environment variable**:
```bash
clever env set CC_PYTHON_VERSION "3.13"
clever env set CC_RUN_COMMAND "uv run main_with_keycloak.py"
```

8. **Set up Keycloak**:
    - 8.1 Set up the Keycloak administration

        - Go to the Keycloak admin console and create a new client.
            - Admin URL: `clever env | grep CC_KEYCLOAK_ADMIN_URL`
            - Initial password: `clever env | grep CC_KEYCLOAK_ADMIN_DEFAULT_PASSWORD`
            - You will have to change it at the first login

        - Manage Realm menu:
            - Top corner left, default **realm name** is `master`, you can create a new one or not.

        - Set up a client:
            > You will need to provide the full URL of your application. (Available in Domain names from the Clever Cloud console or with the CLI `clever domain`)
            - Left panel -> `Clients` -> `Create a client`
                    - Client ID: `minichat`
                    - Client authentication: `On`
                    - Fill Valid Redirect URIs and Web Origins with the URL of your application. Mind the `http://` or `https://` prefix
                        - example `http://APPID.cleverapps.io/`
        
        - Set up the Realm
            - Left panel -> `Realm settings` -> `Login` tab
                - Turn on `User registration` option
            - -> `User profile` tab
                - Manage fields required during the registration


    - 8.2 Update your application environment variable
        - Get the following information from the Keycloak admin: Keakcloak realm name (default `master`), Keycloak client ID (we set; `minichat`), Keycloak client secret (admin Keycloak, Left panel -> `Clients` -> `minichat` tab -> `Credentials` tab)

        - Update your application environment variable
            - `clever env set KEYCLOAK_REALM "master"`
            - `clever env set KEYCLOAK_CLIENT_ID "minichat"`
            - `clever env set KEYCLOAK_CLIENT_SECRET "[THE SECRET YOU GET]"`
 
9. **Deploy or restart your apllication to appply chages**:
```bash
clever deploy
clever restart
```