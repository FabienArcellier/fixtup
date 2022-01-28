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

* code dependencies are managed in `setup.cfg`

## Local Development Environment

Fixtup gère l'environnement de développement avec `pipenv`.

First, clone `fixtup` codebase

```bash
$ git clone ...
```

Move into the newly created directory, create the venv and install the dependencies

```bash
$ cd fixtup
$ pipenv install --dev
```

Activate the newly created virtualenv

```bash
$ pipenv shell
```

It's time to go further. Fixtup use alfred-cli as a build engine. If you need to perform an operation to build or test artefacts, you should use alfred command.

### Run the continuous integration process

Le process d'integration continue est la base de l'assurance qualité.

Dans ce process, plusieurs utilitaires effectuent des vérifications sur la base de code pour évaluer la conformité de la base de code à différentes exigences.

Ce process est joué à chaque commit par github actions, la plateforme d'intégration continue. Vous pouvez cependant le jouer en local. C'est le meilleur moyen de  vérifier que votre poste développeur est prêt pour contribuer.

```bash
$ (fixtup) alfred ci
```

Ce process va exécuter des vérifications sur :

* le typage du code python
* des tests unitaires
* des tests integrations pour vérifier le fonctionnement bout en bout de certains composants (comme la lecture des settings)
* des tests d'acceptances qui vérifie le bon fonctionnement de fixtup

Vous pouvez jouer chaque étape unitairement. Avant d'exécuter une commande alfred
affiche dans le terminal l'étape en cours. Pour lancer le linter, vous avez à exécuter `alfred lint`.

```text
$ alfred lint : check type consistency on source code
Success: no issues found in 14 source files
$ alfred tests : workflow to execute all automatic tests
$ alfred tests:units : execute unit tests
```

### Compile and display the documentation

You should be able to build the documentation.

Here is how to build the documentation

```
$ (fixtup) alfred doc:build
```

The built documentation can then be found in `docs/_build/html/`.

You may want to display it

```bash
$ (fixtup) alfred doc:display
```
