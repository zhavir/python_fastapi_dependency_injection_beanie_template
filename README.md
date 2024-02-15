<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">ToDo List</h3>
</div>


## Summary
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#docker">Docker</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#structure">Structure</a></li>
    <li><a href="#contributing">Contributing</a></li> 
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project



<p align="right">(<a href="#summary">back to top</a>)</p>



### Built With

* [![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
* [![fastapi](https://img.shields.io/badge/FastApi-3776AB.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
* [![beanie](https://img.shields.io/badge/beanie-1.25.0-blue)](https://beanie-odm.dev/)
* [![dependencyInjector](https://img.shields.io/badge/dependency_injector-4.41.0-blue)](https://python-dependency-injector.ets-labs.org/)


<p align="right">(<a href="#summary">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The project is based on Poetry. [Here](https://python-poetry.org/docs/#installing-with-the-official-installer) you can find how to install and configure your local environment with poetry: 

* poetry
  ```sh
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### Docker
The service is already exported in Dockerfile and can easly be built through docker-compose. It will be setup with all their dependecies

```sh
docker compose up --build
```

for convenience, if you want to run natively the service and their dependencies dockerized you need to update your hosts file with

```sh
127.0.0.1    mongodb 
```
<p align="right">(<a href="#summary">back to top</a>)</p>

## Usage

Swagger page is accessible at http://localhost:8080

<p align="right">(<a href="#summary">back to top</a>)</p>

<!-- Structure -->
## Structure
```bash
src/
├─ core/
├─ models/
│  ├─ domain/
│  ├─ orm/
│  ├─ schemas/
├─ routers/
│  ├─ v1/
├─ services/
├─ utilities/
tests/
├─ unit/
├─ integration/
```

The application is strongly based on Dependency injection. All the dependency are then declared and instantiated inside 
the container.py. It means that dependencies are never instantiated directly, but they are passed into the constructor or the
method signature by the framework

The folder structure follow the following logic:
* **Routers**: definition of all the endpoints of the application, they can also be versioned and stored in different paths. 
  * they can call only services
  * they can return only schema object
  * they do not execute any sort of business logic
  * they only validate input coming though the endpoint and then return the related schema response (after calling the underlying layer)
* **Services**: definition of the business logic of the application 
  * they can call only repositories and utility classes
  * a service cannot reference another service 
  * a service works and returns a domain object
* **Repository**: Abstraction layer for the database framework
  * they can only manipulate orm objects
  * the orm object must be mapped to a domain object before returning anything
  * it is the only layers allowed to manipulate data on database
  * a repository cannot reference another repository

```bash
routers (domain) -> service (domain) -> repository (orm)
routers (schema) <- service (domain) <- repository (domain) 
```

<!-- CONTRIBUTING -->
## Contributing

Project use:
 * [ruff](https://github.com/astral-sh/ruff) as linter 
 * [MyPy](https://github.com/python/mypy) for strict type-checking
 * [Pytest](https://github.com/pytest-dev/pytest) as test runner

You can run formatting though pre-commit before commiting code to the remote

```sh
pre-commit run 
```

run the tests with
```sh
pytest
```

<p align="right">(<a href="#summary">back to top</a>)</p>

<!-- CONTACT -->
## Contact

* Andrea Aramini - zhavir@outlook.com

<p align="right">(<a href="#summary">back to top</a>)</p>
