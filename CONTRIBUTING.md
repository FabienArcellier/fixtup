# How to contribute

First of all, thanks for your thinking to help to make Fixtup a better tool.

<!--
Les ressources importantes :

* Discord développeur
* Support sur Stackoverflow
-->

<!--
## Support

Vous avez des questions sur comment utiliser Fixtup, posez vos question sur [Stackoverflow](https://stackoverflow.com/questions/tagged/python-fixtup) avec le tag `python-fixtup`. Si des gens ont la meme question que vous, ils la retrouveront plus facilement, avec la réponse qui vous aura débloqué
-->

## Codebase

* code dependencies are managed in `./setup.cfg`
* codebase of fixtup is in ``./src/fixtup``
* QA tests are in ``./tests``
* build engine commands are in ``./alfred``
* continuous integration scripts are in ``./github/workflows``

## Local Development Environment

First, clone `fixtup` codebase

```bash
$ git clone git@github.com:FabienArcellier/fixtup.git
```

Move into the newly created directory, create the venv and install the dependencies. Fixtup manages the development environment with `pipenv`.

```bash
$ cd fixtup
$ pipenv install --dev
```

Activate the newly created virtualenv

```bash
$ pipenv shell
```

It's time to go further. Fixtup use [``alfred-cli``](https://github.com/FabienArcellier/alfred-cli) as a build engine. If you need to perform an operation to build or test artefacts, you should use alfred command.

### Run the continuous integration process

The continuous integration process is the basis of quality assurance.

In this process, several utilities perform checks on the code base to assess the compliance of the code base with different requirements.

This process is played at each commit by ``github actions``. You can, however, play it locally. This is the best way to verify that your environment is up and ready to contribute.

```bash
$ (fixtup) alfred ci
```

Continuous integration will :

* check typing consistency on python codebase : ``alfred lint``
* run the unit tests : ``alfred tests:units``
* run the integration tests to verify check the behaviors of some components (as reading settings in python manifests) : ``alfred tests:integrations``
* run the acceptance tests that check the behavior of fixtup api : ``alfred tests:acceptances``

You can play each step yourself with `alfred`. Before executing a step in the ``alfred ci`` workflow, ``alfred``
displays the current step in the terminal. Pour lancer le linter, vous avez à exécuter `alfred lint`.

```text
$ alfred lint : check type consistency on source code
Success: no issues found in 14 source files
$ alfred tests : workflow to execute all automatic tests
$ alfred tests:units : execute unit tests
$ alfred tests:integrations : execute integrations tests
$ alfred tests:acceptances : execute acceptances tests
```

### Compile and display the documentation

Here is how to build the documentation

```
$ (fixtup) alfred doc:build
```

The built documentation can then be found in `docs/_build/html/`.

You may want to display it

```bash
$ (fixtup) alfred doc:display
```
