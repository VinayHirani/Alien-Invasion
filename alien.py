import pygame 
from pygame.sprite import Sprite 

class Alien(Sprite):
	""" A class to represent all the aliens """
	
	def __init__(self, ai_settings , screen):
		super(Alien , self).__init__()
		self.ai_settings = ai_settings 
		self.screen = screen 
		
		# Load the alien from the rect attributes 
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		""" Start each new alien from the top of the screen """
		self.rect.x = self.rect.width 
		self.rect.y = self.rect.height 
		
		""" Store the aliens exact position """
		self.x  = float(self.rect.x)
		
	def check_edges(self):
		""" Return true if alien is at edge of screen """
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <=0:
			return True
			
	def update(self):
		""" Move the alien right """
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x
			
	
		
	""" Draw the alien to the screen """
	def blitme(self):
		self.screen.blit(self.image , self.rect)
		
		
