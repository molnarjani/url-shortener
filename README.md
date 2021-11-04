# url-shortener
A url shortener app

Stack:
- Python3
- [PynamoDB - DynamoDB interface](https://pynamodb.readthedocs.io/en/latest/)
- [FastAPI - Webframework](https://fastapi.tiangolo.com/)
- [Pydanic - API data validation](https://pydantic-docs.helpmanual.io/)
- [Poetry - Dependency Manager](https://python-poetry.org/) 

<hr/>
Architecure:
<img src="https://user-images.githubusercontent.com/4608924/140231249-dab0be8b-3ba3-46a3-889a-31ccb2421010.png" width=400px/>

<hr/>

Wiki:
- [Development](https://github.com/molnarjani/url-shortener/wiki/Development)
- [Architecture](https://github.com/molnarjani/url-shortener/wiki/Architecture)
- [Features](https://github.com/molnarjani/url-shortener/wiki/Features)
- [Design decisions](https://github.com/molnarjani/url-shortener/wiki/Design-decisions)
  - [database](https://github.com/molnarjani/url-shortener/wiki/database)
  - [hashing algorithm](https://github.com/molnarjani/url-shortener/wiki/hashing-algorithm)
- [Specification](https://github.com/molnarjani/url-shortener/wiki/Specification)
  - [URL redirect endpoint](https://github.com/molnarjani/url-shortener/wiki/url-redirect-endpoint)
  - [shorten API](https://github.com/molnarjani/url-shortener/wiki/shorten)
  - [statistics API](https://github.com/molnarjani/url-shortener/wiki/statistics)

<hr/>

TODOs and ideas:
- Add tooling:
  - black auto-formatting hooks
  - pyflakes / flake8 check hooks
  - pytest checks
  - pydocstyle checks
  - CI build system
  - Running multiple workers with gunicorn or some other WSGI server
  - maybe make the whole thing serverless (AWS Lambda + API gateway)
  - deployment system (maybe ArgoCD)

- Improve tests:
  - currently the test drob the DB manually this could be solved better with some scripting or tooling
  - tests could be run in docker with a clean container, while devs can keep their localDB

- Add authentication
- Add API throttling

- Make use of pseudo-threads for DB calls using [InPynamoDB]("https://opensourcelibs.com/lib/inpynamodb")
