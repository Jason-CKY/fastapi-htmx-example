# FastAPI htmx server

## Dependencies

* docker (docker-desktop if you are using windows)
* docker-compose (comes with docker-desktop, but can install [here](https://docs.docker.com/compose/install/standalone/) if you are not on windows)
* [Node LTS v18](https://nodejs.org/en/download)

## Features

https://github.com/Jason-CKY/fastapi-htmx-example/assets/27609953/9519a6ea-a5e4-407d-8a29-dcdd76bc2857

* [FastAPI](https://fastapi.tiangolo.com/) web server that serves html on htmx endpoints
* [HTMX](https://htmx.org/) for interactivity, minimal js needed
* Lazy loading with HTMX
* [DaisyUI](daisyui.com/) with [theme-changing library](https://github.com/saadeghi/theme-change) for CSS styling and themes
* [SortableJS](https://github.com/SortableJS/Sortable) for drag and drop of tasks (sorting and updates)
* [Directus](https://directus.io/) for headless CMS and API routes for CRUD operations

## Quickstart (development mode)

You can either start up using `docker-compose`:

```sh
npm ci
make build-dev
# make sure directus is up on http://localhost:8055
make initialize-db
```

## Format on save

Refer to this [link](https://www.digitalocean.com/community/tutorials/how-to-format-code-with-prettier-in-visual-studio-code) on how to install and set prettier to format on save.
