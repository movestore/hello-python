from co_pilot.co_pilot_spec import hook_impl
from movingpandas import TrajectoryCollection
import logging


class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        self.print_input(data)

        animal_id_config = config['individualLocalIdentifier']

        if animal_id_config:
            animal_traj = data.filter('individual.local.identifier', animal_id_config)
            plot = animal_traj.plot(legend=True, figsize=(9, 9), linewidth=4)
            plot.figure.savefig(self.moveapps_io.create_artifacts_file(f'{animal_id_config}.png'))
            logging.info(f'saved plot of individual {animal_id_config}')
        else:
            plot = data.plot(legend=True, figsize=(9, 9), linewidth=1)
            plot.figure.savefig(self.moveapps_io.create_artifacts_file('all.png'))
            logging.info(f'saved plot of all individuals')

        return data

    @staticmethod
    def print_input(data: TrajectoryCollection):
        logging.info(data)
        geopandas = data.to_point_gdf()
        logging.info(geopandas.info())
        logging.info(geopandas['individual.local.identifier'].unique())
