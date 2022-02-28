class Prompt():

    def new_fixture(self, fixture_repository: str) -> str:
        """
        ask to the user a name of a new fixture he want to generate.
        The name should be unique and it should not match existing names, otherwise, the user
        can't validate it's prompt.

        >>> prompt = lookup_prompt()
        >>> fixture = prompt.new_fixture('test/fixtup/fixtures')

        :param fixture_repository: path of the fixture repository
        :return: the identifier written by the user
        """
        raise NotImplementedError()

    def confirm(self, question: str) -> bool:
        """
        ask the user to confirm a question by using yes or no

        >>> prompt = lookup_prompt()
        >>> is_shared = prompt.confirm('Is this fixture is shared between all the tests ?')

        :param question: the question to confirm
        :return:
        """
        raise NotImplementedError()
