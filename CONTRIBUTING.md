# How to contribute

First of all, thanks for your thinking to help to make Fixtup a better tool.


  * [Support](#support)
  * [Codebase](#codebase)
  * [Local Development Environment](#local-development-environment)
    + [Run the continuous integration process](#run-the-continuous-integration-process)
    + [Compile and display the documentation](#compile-and-display-the-documentation)
  * [I want to contribute](#i-want-to-contribute)
    + [Implement a new example for your own stack](#implement-a-new-example-for-your-own-stack)

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

## I want to contribute

### Implement a new example for your own stack

An example shows how a developer would use ``fixtup`` on a tech stack. If you are using fixtup in a stack that is not documented, then you can contribute and make another developer's job easier.

Here's how to add an example:

* the example is in fixtup ``./examples/my-awesome-example``
* the example is published in a PR ``doc/my-awesome-example``
* l'exemple has a ``README.md`` a user can follow step by step
* the example is self-contained. It can be copied to another folder without the fixtup code and should still work
* the example is CI validated from ``.github/workflow/validate_examples.yml``.
* the section `Start with other technical stacks` in ``getting_started.rst`` link to the readme of the example

