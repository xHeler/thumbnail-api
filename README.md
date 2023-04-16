# Thumbnail API
Images API.

# Demo
[LINK TO DEMO](http://52.2.28.62/)
admin - admin

# Techstack
- Django
- Django Rest Framework
- AWS S3
- AWS CloudFront
- PostgreSQL

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development
Create own .env
```bash
cp .env.example .env
```

Start the dev server for local development:
```bash
docker compose up
```

Run a command inside the docker container:

```bash
docker compose run --rm web [command]
```

# List images
List all users images include thumbnails.

`GET` /api/v1/images/

# Upload image
Upload image file.


`POST` /api/v1/images/upload/

**Example response**:
```json
{
    "id": "a21cb51c-555e-4cc3-8548-74845e386ff5",
    "created_at": "2023-03-10T15:12:43+0000",
    "updated_at": "2023-03-10T15:12:43+0000",
    "urls_dict": [
        {
            "200x200": "127.0.0.1/<user_id>/<uui4>.jpg"
        },
        {
            "orginal": "127.0.0.1/<user_id>/<uui4>.jpg"
        }
    ]
}
```

# Generate expiring link
Generate temporary link to uploaded image using url.


`POST` /api/v1/images/generate_expiring_link/

**Example POST**:

**url** - link to thumbnail 

**time** - time in second to expire
```json
{
"url": "http://127.0.0.1:8000/<user_id>/<image_name>",
"time": 300
}
```
