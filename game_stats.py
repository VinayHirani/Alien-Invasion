""" stores the number of ships allowed """
class GameStats():
	""" Track Stastics for alien invasion """
	
	def __init__(self , ai_settings):
		""" Initialize the stastics """
		self.ai_settings = ai_settings
		self.reset_stats()
		# Start alien invasion in inactive state.
		self.game_active = False
		# High score should never be reset.
		self.high_score = 0
		self.level = 1
			
	def reset_stats(self):
		""" Initialiaze the stastics that change during the game """
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		
		
