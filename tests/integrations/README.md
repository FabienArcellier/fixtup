Integration tests validate invocation of modules that depends of external system .
For example, they may read files from disk like setup.cfg or pyproject.toml.

Those tests are using the Eat Your Own Dog Food approach because some of them depends on fixtup to be executed.
