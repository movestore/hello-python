import unittest
import os
from tests.config.definitions import ROOT_DIR
from app.app import App
from sdk.moveapps_io import MoveAppsIo
import pandas as pd
import movingpandas as mpd


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['APP_ARTIFACTS_DIR'] = os.path.join(ROOT_DIR, 'tests/resources/output')
        self.sut = App(moveapps_io=MoveAppsIo())

    def test_app_file_consume(self):
        # prepare
        os.environ['LOCAL_APP_FILES_DIR'] = os.path.join(ROOT_DIR, 'tests/resources/app/')

        # execute
        actual = self.sut._consume_app_file()

        # verif
        self.assertEqual(11, actual)

    def test_filter_output(self):
        # prepare
        testdata: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/app/input2.pickle'))
        config = {
            "individualLocalIdentifier": 742
        }
        self.assertEqual(3, len(testdata.trajectories))

        # execute
        actual = self.sut.execute(data=testdata, config=config)

        # verify
        self.assertEqual(1, len(actual.trajectories))
        self.assertEqual(742, actual.trajectories[0].id)

    def test_full_output_missing_key(self):
        # prepare
        testdata: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/app/input2.pickle'))
        config = {}
        self.assertEqual(3, len(testdata.trajectories))

        # execute
        actual = self.sut.execute(data=testdata, config=config)

        # verify
        self.assertEqual(3, len(actual.trajectories))

    def test_full_output_null_key(self):
        # prepare
        testdata: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/app/input2.pickle'))
        config = {
            "individualLocalIdentifier": None
        }
        self.assertEqual(3, len(testdata.trajectories))

        # execute
        actual = self.sut.execute(data=testdata, config=config)

        # verify
        self.assertEqual(3, len(actual.trajectories))

    def test_crash(self):
        # prepare
        testdata: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/app/input2.pickle'))

        config = {
            "forceCrash": True
        }

        # execute
        with self.assertRaises(Exception):
            self.sut.execute(data=testdata, config=config)
