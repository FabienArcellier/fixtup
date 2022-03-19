# Fixtup

Fixtup facilite l'écriture de tests automatiques en python
qui s'appuie sur des ressources externes. Une ressource externe
peut etre aussi simple qu'un dossier de travail ou être une base de donnée
postgresql, un broker de message rabbitmq, ou un service cloud comme AWS S3 ...

Sans Fixtup, vous aurez à écrire du boilerplate dans vos tests
qui s'appuie sur des ressources externes. Encore plus si vos tests induisent des effets de bord.
Si un test crée un fichier, modifier un fichier existant, ajoute un enregistrement
dans une base de donnée, le code que avez à écrire dans le teardown de votre test composera la
majorité de votre test.

Avec Fixtup, vous spécifiez les ressources à créer. Fixtup les instancie avec le niveau d'isolation
que vous avez spécifié au moment où votre test en a besoin. Les ressources vivent le temps du test.

## Getting started with Fixtup

```
pip install fixtup
```

```python
def test_thumbnail_should_generate_thumbnail(self):
    with fixtup.up('thumbnail_context') as f:
        # Given
        wd = os.getcwd()
        original_file = os.directory.join(wd, 'file.png')
        expected_thumbnail_file = os.directory.join(wd, 'file_t.png')

        # Then
        thumbnail(original_file, expected_thumbnail_file)

        # Then
        self.assertTrue(os.directory.isfile(expected_thumbnail_file)
```

La documentation offre plus d'exemples :

* mutualiser les fixtures dans le setup et teardown
* utiliser fixtup avec le plugin pytest
* instancier une base de donnée redis avec fixtup
* spécifier des variables d'environnement à utiliser avec fixtup
* ...

##

## Des effets de bords difficile à maitriser

Par exemple, votre code génère une miniature à partir d'une image uploadée par l'utilisateur.
Pour tester votre code, vous écrivez le code suivant :

```python
def test_thumbnail_should_generate_thumbnail(self):
    thumbnail('file.jpeg', 'file_t.jpeg')
    self.assertTrue(os.directory.isfile('file_t.jpeg'))
```

Ce test présente un défaut. Une fois le test joué une fois, le fichier `file_t.jpeg` est conservé.
Vous devez penser à l'effacer. Vous avez aussi une chance de vous retrouver à un moment avec
le fichier `file_t.jpeg` dans votre repository de code.

## Contributing

[More information into CONTRIBUTING.md](./CONTRIBUTING.md)
