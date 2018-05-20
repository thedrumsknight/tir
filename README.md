# apollo project

### Setting up for Development

#### 1. Pre-requisites

> The app uses the following packages - python v3.6, pip, pipenv.
>
> Please make sure you have a python development environment setup and these packages installed.

Clone the repo

```bash
git clone https://github.com/thedrumsknight/tir.git
cd tir
```

Setup a `virtualenv` and install the dependencies from `Pipfile.lock`

```bash
# Setup python3.6 virtualenv
pipenv --three

# Install dependencies
pipenv install

# Run this to verify your installation
pipenv check
```

**NOTE:** You need to copy the pre-trained model (~1.3GB, download [here](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/view?usp=sharing)) to the `apollo/w2v` directory before running the app

#### 2. Setting up the DB

The app uses Redis (django channels depend on it) as its DB

Install [Redis](https://redis.io/download) depending on your OS. For Windows, you might want to checkout [these releases](https://github.com/MicrosoftArchive/redis/releases).

#### 3. Running the app

Assuming you have added the Redis installation to your `PATH` variable, you need to start the redis server before starting the app

```bash
# Move into project directory and start Redis (in a separate terminal window/tab)
cd tir
redis-server

# Run migrations (ONLY NEEDS TO BE RUN ON SETUP or when you change django models)
pipenv run python manage.py migrate

# Run the app
pipenv run python manage.py runserver
```

You should be able to see the app running at [http://localhost:8000/](http://localhost:8000/)

> Note: Since this project uses [pipenv](https://docs.pipenv.org/), all python commands can be used normally by prepending `pipenv run` to them.
>
> This runs the command in the virtual env where the dependencies of the project exist.