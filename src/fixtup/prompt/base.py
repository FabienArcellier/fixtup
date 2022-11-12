from typing import List, Optional


class Prompt():

    def choice(self, question: str, choices: List[str], default: Optional[str] = None) -> str:
        """
        ask the user to make a choice based on propositions

        The user has to pick a specific choice, he can't valide the input
        if the value does not match the choice exactly

        >>> prompt = lookup_prompt()
        >>> manifest = prompt.choice("Python manifests ?", choices=["setup.cfg", "pyproject.toml"])
        """
        raise NotImplementedError

    def fixture_repository(self) -> str:
        """
        ask the user the path of fixture repository he want to use.

        A user can enter the path of a new folder or select the path of an empty folder.
        It cannot select the path of a folder that already contains files or folders.

        >>> prompt = lookup_prompt()
        >>> fixture_repository = prompt.fixture_repository()
        """
        raise NotImplementedError

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

    def confirm(self, question: str, default: bool = False) -> bool:
        """
        ask the user to confirm a question by using y or n

        >>> prompt = lookup_prompt()
        >>> is_shared = prompt.confirm('Is this fixture is shared between all the tests ?')

        :param question: the question to confirm
        :return:
        """
        raise NotImplementedError()

    def input(self, question: str, default: Optional[str] = None) -> Optional[str]:
        """
        ask a user to write something on one line

        >>> prompt = lookup_prompt()
        >>> database_url = prompt.text('What is the database url ?', default="sqlite://helloworld.db")

        :param question: the question to answer
        :param default: the value to use if the user let it blank
        :return: the input written by the user, if it's blank, return the default value
        """
        raise NotImplementedError()
