# CMS-API

## Docker Usage (Testing Environment Only)

> **Note:** Docker is currently used **only for testing and development purposes**.
> For **production deployments**, this application is deployed **without Docker** using the standard server setup.

---

## Build Docker Image

Build the Docker image from the project root directory:

```bash
docker build -t cms-api .
```

List available Docker images:

```bash
docker images
```

---

## Run Docker Container

Run the container and expose the Django application on port `8000`:

```bash
docker run -d \
  --name cms-api-container \
  -p 8000:8000 \
  cms-api
```

View container logs:

```bash
docker logs -f cms-api-container
```

Access the application:

```
http://localhost:8000
```

---

## Stop Docker Container

```bash
docker stop cms-api-container
```

---

## Start Existing Container

```bash
docker start cms-api-container
```

---

## Remove Docker Container

```bash
docker rm -f cms-api-container
```

---

## Remove Docker Image

Delete the Docker image:

```bash
docker rmi cms-api
```

If the image is being used by any container, remove the container first:

```bash
docker rm -f cms-api-container
docker rmi cms-api
```

---

## Docker Workflow for Testing

1. Build the Docker image.
2. Run the Docker container.
3. Perform testing and validation.
4. Stop and remove the container after testing.
5. Remove the image if no longer required.

---

## Production Deployment

* **Docker is NOT used in production.**
* Production deployments follow the organization's standard deployment process directly on the server infrastructure.
* Any Docker-related configurations should be considered **testing/development utilities only**.

## PostgreSQL Configuration

This project now uses PostgreSQL by default. Create a `.env` file from `.env.example` and set the following values:

```bash
DB_NAME=cms_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Then run Django normally with the standard `portfolio_backend.settings` module.
