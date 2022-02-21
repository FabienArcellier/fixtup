Command line
############

``fixtup`` offre un outil en ligne de commande. Cet outil permet d'effectuer
des opérations sur vos fixtures ou valider leur fonctionnement.

Configurer son projet python pour activer fixtup
************************************************

.. code-block:: bash

    fixtup init

Afficher les informations relatives à la configuration
******************************************************

La commande `fixtup info` vous permet d'avoir une vue de la configuration active. Elle affiche
une synthèse des paramètres importants comme le fichier qui contient la configuration de fixtup ou
le repository qui contient les templates de fixture.

.. code-block:: bash

    $ fixtup info

    Configuration: /home/far/documents/project/setup.cfg
    Fixtures: /home/far/documents/project/tests/fixtures/fixtup
    Plugins:
        * fixtup.plugins.docker
        * fixtup.plugins.dotenv

