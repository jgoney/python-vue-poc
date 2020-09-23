# Home programming assignment

## Pre-requisites

This project is built/tested with the following stack:

- [Vue.js 2.0][vue]
- [Python 3.7.4][vue]
- [Node.js v12.18.0][node]
- [npm 6.14.4][npm]

Other versions may work, but at your own risk. Caveat emptor.

## Quickstart

```bash
npm install  # Install JavaScript dependencies
npm run build  # Compile and minify JavaScript for production

python3 -m venv ./env  # Initialize Python virtual environment
. env/bin/activate   # Activate virtualenv in current shell
pip install -r requirements.txt  # Install Python dependencies

python server/server.py  # Run Flask server
```

To view the webapp, visit http://0.0.0.0:8869 in your web browser.

N.B.; if you try to run the Python server without building the JavaScript first, you'll encounter a `jinja2.exceptions.TemplateNotFound` error. Just run `npm run build` and try again.

## Running tests

After setting up your Python and JavaScripts environments as described above, you can run tests as follows:

```bash
# Server tests
. env/bin/activate   # Still in virtualenv, from above instructions
python server/test_server.py  # Run tests
coverage run --omit=env/* server/test_server.py  # Run server tests with Coverage
coverage html  # Generate Coverage report (run above command first)
open htmlcov/index.html  # Open Coverage HTML report on MacOS

# Frontend tests
npm run test:unit  # Run tests
open coverage/lcov-report/index.html  # Open Coverage HTML report on MacOS
```

## Notes / optimizations

1. This setup shouldn't be used in production as-is; ideally it should be run behind a proper web server (such as Gunicorn) and a reverse proxy (such as NGINX).

2. NGINX also would make it possible to enable gzip compression, which hypothetically would speed up response times quite a bit for larger responses.

## npm scripts

```bash
npm install  # Installs JavaScript dependencies

npm run serve  # Compiles and hot-reloads for development

npm run build  # Compiles and minifies for production

npm run lint  # Lints and fixes files
```

[vue]: https://vuejs.org/
[python]: https://www.python.org/
[node]: https://nodejs.org/en/
[npm]: https://www.npmjs.com/
