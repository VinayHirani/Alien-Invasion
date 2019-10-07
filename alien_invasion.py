""" Creating a alien invasion game using pygame """




import pygame

from settings import Settings 
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from pygame.sprite import Group
import game_functions as gf


""" Initializing the screen first """
def run_game():
	""" Initializing the pygame """
	pygame.init()
	
	""" Screen """
	ai_settings = Settings()                 # from class settings
	screen = pygame.display.set_mode(
	    (ai_settings.screen_width , ai_settings.screen_height))
	        
	pygame.display.set_caption("Alien Invasion")
	
	""" Play Button """
	play_button = Button(ai_settings , screen , "Play")
	
	""" Create instance of gamestats and create scoreboard """
	stats = GameStats(ai_settings)
	sb = ScoreBoard(ai_settings , screen , stats)
	
	""" Make a ship , a group of bullets , a group of aliens """
	ship = Ship(ai_settings , screen)
	bullets = Group()
	aliens = Group()
	
	# Create a fleet of aliens 
	gf.create_fleet(ai_settings , screen , ship , aliens)
	
	# Starting the main loop of the game 
	while True:
		
		#Watch for mouse and keyboard events 
		gf.check_events(ai_settings , screen ,stats , sb , play_button ,
		    ship , aliens , bullets)
		    
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings  , screen ,stats , sb , ship ,aliens , bullets)
			gf.update_aliens(ai_settings , screen , stats ,sb ,ship , aliens , bullets)
			
		""" Upgrading the screen """
		gf.upgrade_screen(ai_settings , screen , stats , sb , ship , aliens , bullets,
		    play_button)
		    

run_game()

