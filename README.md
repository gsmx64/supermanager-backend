
SuperManager - Backend part (Under Development) - v1.0.0

## Overview

![Super Manager Logo](docs/images/logo.png)
SuperManager is an IT management system designed to streamline and optimize your organization's technology operations.

**Super Manager - Backend** is the core API and service layer for managing all aspects of IT infrastructure. It provides robust tools for device inventory, software deployment, script execution, reporting, supply stock control, calendar management, user administration, and notifications.

## Features

- **Device Inventory**: Track and manage all IT assets and devices.
- **Software & Script Deployment**: Remotely deploy software and execute scripts across managed devices.
- **Reporting**: Generate detailed reports on device status, software deployments, and inventory.
- **Stock Control**: Monitor and manage consumable supplies and inventory levels.
- **Calendar System**: Organize and schedule IT-related events, maintenance, and tasks.
- **User Management**: Control access, roles, and permissions for system users.
- **Notifications**: Receive alerts and updates for important events and system activities.


## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/gsmx64/supermanager-backend.git
    ```
2. Install the dependencies (use `--upgrade` to ensure the latest versions are installed):
    ```bash
    pip install -r requirements.txt
    ```
3. Configure the environment variables as needed:
For development environment, copy `.env.development.sample` to `.env.development`, and edit it.
For testing environment, copy `.env.testing.sample` to `.env.testing`, and edit it.
For production or staging environment, gather all required variables from `.env.development.sample`, edit it and inject them into your environment (not using a file, secrets maybe the best choice). Make sure to set secure values for sensitive keys such as database credentials, secret keys, and API tokens.
4. Apply the database migrations:
    ```bash
    python manage.py migrate
    ```
5. (Optional) Create a superuser to access the admin panel:
    ```bash
    python manage.py createsuperuser --email admin@example.com --username admin
    ```
6. Start the development server:
    ```bash
    python manage.py runserver
    ```

## API Documentation (Swagger)

Interactive API documentation is available via **Swagger UI**. Once the development server is running, you can access the Swagger interface at:

Swagger UI: /swagger/
```
http://localhost:8000/swagger/
```

ReDoc: /redoc/
```
http://localhost:8000/redoc/
```

This allows you to explore and test all available API endpoints directly from your browser.

## Frontend Integration

The backend integrates seamlessly with the [Super Manager Frontend](https://github.com/gsmx64/supermanager-frontend.git), which is built using **React 19**. All IT management features are accessible via the API provided by this backend.

## Documentation

For detailed API documentation and usage examples, see the [docs](./docs) folder.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.

