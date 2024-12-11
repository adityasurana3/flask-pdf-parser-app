# Flask PDF Processing with Celery

## Prerequisites

Before running this project, make sure you have the following installed:

- **Docker**
- **Docker Compose**
- **Redis**

## Project Setup

### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/adityasurana3/flask-pdf-parser-app.git
```

Now move to the directory
```bash
cd flask-pdf-parser
```

To run the server run the docker-compose command
```
docker-compose up --build
```

When the server have started. Go to postman

1. Hit this endpoint in post request
    ```
    http://locahost:5000/upload
    ```

2. Now in the postman there is the body tab click on it
3. select the form-data
3. add key with the name `file` and click the choose file button next to `file` key
