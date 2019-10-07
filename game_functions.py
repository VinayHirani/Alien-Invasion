import pygame 

import sys 

from bullet import Bullet
from alien import Alien
from time import sleep



def check_keydown_events(event , ai_settings , screen , ship , bullets):
	""" Responds to keypresses """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings , screen , ship , bullets)
	elif event.key == pygame.K_q:
		sys.exit()
		

def fire_bullet(ai_settings , screen ,ship , bullets):
	# create new bullet and add it to the bullets group 
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings , screen , ship)
		bullets.add(new_bullet)
		
		

def check_keyup_events(event , ship):
	""" Respond to keyups """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		


def check_events(ai_settings , screen ,stats , sb , play_button , ship ,aliens , bullets):
	""" Respons to key and mouse events """
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event , ai_settings , screen , ship , bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event , ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x , mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings , screen , stats , sb ,
			    play_button , ship , aliens ,bullets ,mouse_x , mouse_y)

def check_play_button(ai_settings , screen ,stats , sb , play_button ,
    ship , aliens , bullets , mouse_x , mouse_y):
		""" Start a new game when player clicks play"""
		button_clicked = play_button.rect.collidepoint(mouse_x , mouse_y)
		if button_clicked and not stats.game_active:
			ai_settings.initialize_dynamic_settings()
			stats.reset_stats()
			stats.game_active = True
			
			#Reset the scoreboard images.
			sb.prep_score()
			sb.prep_high_score()
			sb.prep_level()
			sb.prep_ships()
			
			aliens.empty()
			bullets.empty()
			pygame.mouse.set_visible(False)
			create_fleet(ai_settings , screen , ship , aliens)
			ship.center_ship() 
											
""" Function for update screen """
def upgrade_screen(ai_settings , screen , stats , sb ,ship , aliens , bullets,play_button):
	""" Update images on the screen and flip to new screen """
	screen.fill(ai_settings.bg_color)
	""" Redraw all the bullets behind ship and aliens """
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	""" Draw the ship """	
	ship.blitme()
	aliens.draw(screen)
	
	#Draw the Score info.
	sb.show_score()
	
	#Draw the play button when the game is inactive.
	if not stats.game_active:
		play_button.draw_button()
		
	# flip the most updated screen 
	pygame.display.flip()

def update_bullets(ai_settings , screen ,stats , sb ,ship ,aliens , bullets):
	""" Update the position of the bullets and get rid of the old bullets """
	
	# get rid of the old bullets that have disappeared 
	for bullet in bullets.copy():
		bullets.update()
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
	

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	""" Respond to bullet alien collisions """
	# Remove any bullets or aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets , aliens , True , True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points
			sb.prep_score()
		check_high_score(stats,sb)	
		
	
	if len(aliens) == 0:
		""" Destroy the bullets"""
		bullets.empty()
		""" Speed up the level """
		ai_settings.increase_speed()
		
		#Increase Level.
		stats.level += 1
		sb.prep_level()
		
		""" Create a new fleet """
		create_fleet(ai_settings , screen , ship , aliens)
		
		
	

				
def get_number_aliens_x(ai_settings , alien_width):
	""" Determine the no of aliens that fit in a row """
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x / (2*alien_width))
	return number_aliens_x

def create_alien(ai_settings , screen , aliens , alien_number , row_number):
	# Create an alien and place it in row 
	alien = Alien(ai_settings , screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width*alien_number
	alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
	alien.rect.x = alien.x
	aliens.add(alien)
	
def get_number_rows(ai_settings , ship_height , alien_height):
	""" Determine the no of rows of aliens that can fit in the screen"""
	available_space_y = (ai_settings.screen_height - 
	                        (3*alien_height) - ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows
	
			
def create_fleet(ai_settings , screen , ship , aliens):
	""" Create a full fleet of aliens """
	""" Create an alien and find the number of aliens in a row """
	""" Spacing between each alien is equal to one alien width """
	alien = Alien(ai_settings , screen)
	number_aliens_x = get_number_aliens_x(ai_settings , alien.rect.width)
	number_rows = get_number_rows(ai_settings , ship.rect.height, 
	    alien.rect.height)
	    
	
	""" Creating the first row of aliens """
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings , screen , aliens , alien_number,
			    row_number)

	
def check_fleet_edges(ai_settings , aliens):
	""" Respond appropiately if any aliens have reached the edge """
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings , aliens)
			break

def change_fleet_direction(ai_settings , aliens):
	""" Drop the entire fleet and change directions """
	
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings ,screen, stats , sb, ship , aliens , bullets):
	""" Respond to ship being hit by alien """
	if stats.ships_left > 0:
		stats.ships_left -= 1
		
		#Update ScoreBoard.
		sb.prep_ships()
		
		aliens.empty()
		bullets.empty()
		
		#Create Fleet.
		create_fleet(ai_settings , screen , ship , aliens)
		ship.center_ship()
		
		# Pause.
		sleep(0.5)
	else:
		stats.game_active = False 
		pygame.mouse.set_visible(True)
			
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	""" Check if aliens hit the bottom of the screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			break
		
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
		""" Move the alien right """
		check_fleet_edges(ai_settings , aliens)
		aliens.update()
		
		#Check for aliens ship collisions.
		if pygame.sprite.spritecollideany(ship,aliens):
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			
		check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
			
		
def check_high_score(stats , sb):
	""" Check to see if there is a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
