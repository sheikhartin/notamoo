## Notamoo

![GitHub repo status](https://img.shields.io/badge/status-active-green?style=flat)
![GitHub license](https://img.shields.io/github/license/sheikhartin/notamoo)
![GitHub contributors](https://img.shields.io/github/contributors/sheikhartin/notamoo)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sheikhartin/notamoo)
![GitHub repo size](https://img.shields.io/github/repo-size/sheikhartin/notamoo)

This project provides an API to help you leave important and secret notes for
specific people with an expiration date without authentication...

### How to Use

Install the dependencies:

```
poetry install
```

Test it first:

```
poetry run pytest -rP
```

Run the server:

```
poetry run uvicorn notamoo.main:app --reload
```

Then navigate to http://127.0.0.1:8000/api/docs/swagger.

### License

This project is licensed under the MIT license found in the [LICENSE](LICENSE) file in the root directory of this repository.
