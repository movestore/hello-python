import os

from co_pilot.co_pilot_spec import hook_impl
from movingpandas import TrajectoryCollection
import logging


class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        self.__print_input(data)

        # showcase consuming `LOCAL_FILE`
        self._consume_app_file()

        # showcase doing something with the app input
        output = self.__do_something(app_input=data, config=config)

        return output

    @staticmethod
    def __print_input(data: TrajectoryCollection):
        logging.info(data)
        geopandas = data.to_point_gdf()
        logging.info(geopandas.info())
        logging.info(geopandas['individual.local.identifier'].unique())

    def __do_something(self, app_input: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        if 'individualLocalIdentifier' in config and config['individualLocalIdentifier']:
            animal_id_config = config['individualLocalIdentifier']
            if animal_id_config == 'error':
                raise ValueError("testing exceptions")
            animal_traj = app_input.filter('individual.local.identifier', animal_id_config)
            plot = animal_traj.plot(legend=True, figsize=(9, 9), linewidth=4)
            plot.figure.savefig(self.moveapps_io.create_artifacts_file(f'{animal_id_config}.png'))
            logging.info(f'saved plot of individual {animal_id_config}')
            # output of this app will be just the requested individuals
            return animal_traj
        else:
            plot = app_input.plot(legend=True, figsize=(9, 9), linewidth=1)
            plot.figure.savefig(self.moveapps_io.create_artifacts_file('all.png'))
            logging.info(f'saved plot of all individuals')
            # output of this app will be the same as its input
            return app_input

    def _consume_app_file(self):
        app_file_root_dir = self.moveapps_io.get_app_file_path('myFiles')
        if app_file_root_dir:
            expected_file = os.path.join(app_file_root_dir, 'my-machine.txt')
            with open(expected_file) as f:
                content = f.read()
                logging.info(content)
                return content
