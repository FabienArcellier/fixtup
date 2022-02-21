Fixtup
######

``Fixtup`` facilite l'écriture de tests automatiques en python qui s'appuie un environnement complexe.

Une ressource externe peut etre aussi simple qu'un dossier de travail ou un service plus complexe comme
une base de donnée postgresql, un broker de message rabbitmq, ou un service cloud comme AWS S3, ...

Sans ``Fixtup``, vous aurez à écrire du boilerplate dans vos tests pour gérer le contenu de ces ressources externes.
Si vos tests produisent des effets de bord, comme la création de fichier, la modification d'un fichier existant,
de l'ajout d'un enregistrement dans une base de donnée ce code peut devenir plus important que le test lui même.

Avec ``Fixtup``, vous spécifiez des ``fixtures`` qui décrivent les ressources à créer.
Fixtup les instancie au moment où votre test en a besoin. A la fin du test, ``Fixtup`` gère la destruction des ressources.


.. toctree::
    :maxdepth: 2
    :caption: Table of content

    getting_started
    installation
    handbook
    limits
    support
    command_line
    api

Indices and tables
==================

* :ref:`search`
