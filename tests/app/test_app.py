import unittest
import os
from tests.config.definitions import ROOT_DIR
from app.app import App
from co_pilot.moveapps_io import MoveAppsIo


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.sut = App(moveapps_io=MoveAppsIo())

    def test_app_file_consume(self):
        # prepare
        os.environ['LOCAL_APP_FILES_DIR'] = os.path.join(ROOT_DIR, 'tests/resources/app/')

        # execute
        actual = self.sut._consume_app_file()

        # verif
        self.assertEqual("hello world", actual)
