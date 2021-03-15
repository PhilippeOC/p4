from .menus_controller import HomeMenuController
from .import utils


class ApplicationController:
    def __init__(self):
        self.controller = None

    def start_app(self):
        utils.players_db_list = utils.disp_players_alpha(utils.read_datas_db('players'))
        utils.tournaments_db_list = utils.read_datas_db('tournaments')
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller.run()
        #self.quit_app()

    def quit_app(self):
        utils.write_datas_db('players', utils.players_db_list)
        utils.write_datas_db('tournaments', utils.tournaments_db_list)
