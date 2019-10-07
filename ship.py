""" Adding the ship image to the bottom using class """
import pygame 
from pygame.sprite import Sprite
class Ship(Sprite):
	
	def __init__(self , ai_settings , screen):
		super(Ship , self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings 
		
		# Load the screen and ship image 
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		
		
		# Start each new ship at the bottom of the screen 
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		# Store A decimal value for the ships center 
		self.center = float(self.rect.centerx)
		
		
		#Movement flags
		self.moving_right = False
		self.moving_left = False
		
		
	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		 
			
		# update rect object 
		self.rect.centerx = self.center
		
	def center_ship(self):
		""" Center the ship on the screen after being hit by alien"""
		self.center = self.screen_rect.centerx
		
		
		
	def blitme(self):
		""" Draw the ship to its current location """
		self.screen.blit(self.image , self.rect)
	
	
