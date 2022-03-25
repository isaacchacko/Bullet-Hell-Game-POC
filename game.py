# TODO create better detection software, maybe looking at window as surface, finding coords of player rect and checking if nearby pixels are purple? just spitballing
# imports
import pygame
import random
import sys
import math
import time

pygame.font.init()

# VARIABLES
WINDOW_SETTINGS = {
	'WIDTH': 2000,
	'HEIGHT': 500,
	'NAME': 'DODGE',
	'FPS': 120
}

COLORS = {
	'BLACK': pygame.Color(0,0,0),
	'WHITE': pygame.Color(255,255,255),
	'RED': pygame.Color(255,0,0),
	'CHAMBER_YELLOW': pygame.Color(255,191,49),
	'ENEMY_PURPLE': pygame.Color(128,59,255)
}

GAME_SETTINGS = {
	'BT': {
		'CURRENT_SPEED_EFFECT': 1,
		'BT': 0.05,
		'EXIT_BT': 0.01,
		'NORMAL_SPEED_EFFECT': 1
	},
	'FONT': pygame.font.Font('secrcode.ttf', 75)
}

# FUNCTIONS
def getCenterCoordinates():
	return WINDOW_SETTINGS['WIDTH']//2, WINDOW_SETTINGS['HEIGHT']//2

def checkBT(player, projectiles):
	range = 200 # diameter

	# create a detection sprite
	bulletTimeDetection = pygame.sprite.Sprite()
	bulletTimeDetection.image = pygame.Surface((range, range))
	bulletTimeDetection.rect = bulletTimeDetection.image.get_rect()
	bulletTimeDetection.rect.center = player.rect.center

	if len(pygame.sprite.spritecollide(bulletTimeDetection, projectiles, False)) > 0: # if a projectile is in 200 pixels of the player/touching the detection sprite
		GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'] = GAME_SETTINGS['BT']['BT']

	else:
		if GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'] < GAME_SETTINGS['BT']['NORMAL_SPEED_EFFECT']: # already in bt
			GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'] += GAME_SETTINGS['BT']['EXIT_BT']


	# failsafe
	if GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'] > GAME_SETTINGS['BT']['NORMAL_SPEED_EFFECT'] or GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'] <= 0:
		GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'] = GAME_SETTINGS['BT']['NORMAL_SPEED_EFFECT']

# CLASSES
class TimeBasedTimer:
	def __init__(self, name, delay, loop):
		self.name, self.delay, self.loop = name, delay, loop
		self.startTimer()

	def startTimer(self):
		self.start = time.time()

	def checkRinging(self):
		now = time.time()
		if (now - self.start)*1000 >= self.delay and self.loop > 0:
			self.startTimer()
			self.loop -= 1
			return True

		else:
			return False

class TickBasedTimer:
	def __init__(self, name, delay, loop): # delay will be given in miliseconds
		self.name, self.delay, self.loop = name, delay, loop
		self.count = 0

	def tick(self): # assumed to be called every frame
		self.count += ((1/WINDOW_SETTINGS['FPS'])*10000) * GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT']

	def checkRinging(self):
		if self.count >= self.delay:
			self.loop -= 1
			self.count = 0
			return True

		return False

class TimerHandler:
	def __init__(self, timerDict, timerClass):
		self.timers = []
		for key, value in timerDict.items():
			self.timers.append(timerClass(key, value['DELAY'], value['LOOP']))

	def checkRinging(self):
		ringing = []
		for timer in self.timers:
			if timer.checkRinging():
				ringing.append(timer.name)

		return ringing

	def newTimer(self, name, delay, loop):
		self.timers.append(timerClass(name, delay, loop))

	def deleteClosed(self):
		for timer in self.timers:
			if timer.loop <= 0:
				self.timers.remove(timer)
				del timer

class TimeBasedTimerHandler(TimerHandler):
	def __init__(self, timerDict):
		TimerHandler.__init__(self, timerDict, TimeBasedTimer)

class TickBasedTimerHandler(TimerHandler):
	def __init__(self, timerDict):
		TimerHandler.__init__(self, timerDict, TickBasedTimer)

	def tickAll(self):
		for timer in self.timers:
			timer.tick()

class Text(pygame.sprite.Sprite):
	def __init__(self, x, y, text, color, bg=None):
		pygame.sprite.Sprite.__init__(self)
		self.image = GAME_SETTINGS['FONT'].render(text, True, color, bg)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# convert black to color
		for y in range(self.image.get_height()):
			for x in range(self.image.get_width()):
				pass

# class Button(Text):
# 	def __init__(self, x, y, text, color, bg):
# 		Text.__init__(self, x, y, text, color, bg)

# 	# TODO 
class Score(Text):
	def __init__(self, x, y):
		self.start = time.time()
		self.color = COLORS['CHAMBER_YELLOW']
		Text.__init__(self, x, y, "00:00:00", self.color)
		
	def update(self, projectiles, boundX, boundY):
		# past timer based on bullets dodged
		# left = pygame.sprite.Sprite()
		# left.image = pygame.Surface((1, WINDOW_SETTINGS['HEIGHT']))
		# left.rect = left.image.get_rect()
		# left.topleft = (0,0)

		# right = pygame.sprite.Sprite()
		# right.image = pygame.Surface((1, WINDOW_SETTINGS['HEIGHT']))
		# right.rect = right.image.get_rect()
		# right.topleft = (boundX[1], 0)

		# top = pygame.sprite.Sprite()
		# top.image = pygame.Surface((WINDOW_SETTINGS['WIDTH'], 1))
		# top.rect = top.image.get_rect()
		# top.topleft = (0,0)

		# bottom = pygame.sprite.Sprite()
		# bottom.image = pygame.Surface((1, WINDOW_SETTINGS['HEIGHT']))
		# bottom.rect = bottom.image.get_rect()
		# bottom.topleft = (boundY[1],0)

		# for sprite in [left, right, top, bottom]:
		# 	removed = pygame.sprite.spritecollide(sprite, projectiles, True)
		# 	for i in removed:
		# 		self.score += i.worth
		# 		print(f'score : {str(self.score - i.worth)} + {str(i.worth)} = {str(self.score)}')
		# 		# del i
		now = time.time()
		hours = round((now-self.start)/3600)
		minutes = round((now-self.start)/60)
		seconds = round((now-self.start)%60)
		hours, minutes, seconds = str(hours), str(minutes), str(seconds)
		while len(str(hours)) < 2:
			hours = '0' + hours
		while len(str(minutes)) < 2:
			minutes = '0' + minutes
		while len(str(seconds)) < 2:
			seconds = '0' + seconds

		# print(f'H: {hours}, M: {minutes}, S: {seconds}')
		self.image = GAME_SETTINGS['FONT'].render(str(f'{hours}:{minutes}:{seconds}'), True, self.color)


class Entity(pygame.sprite.Sprite):
	def __init__(self, image, mass):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.image.set_alpha(255)

		self.vX, self.vY = 0, 0
		self.aX, self.aY = 0, 0
		self.mass = mass # treated as point mass

	def newForce(self, magnitude, angle):
		debug = False

		if debug: print(f'{time.ctime(time.time())}Force Registered: {magnitude} N at directed {angle} degrees from the horizontal.')

		# x
		magX = magnitude*math.cos(math.radians(angle))
		if debug: print(f'X Magnitude = {magX}')
		if debug: print(f'aX: {self.aX} ----> {self.aX + magX/self.mass}')
		self.aX += magX/self.mass

		# x
		magY = magnitude*math.sin(math.radians(angle))
		if debug: print(f'Y Magnitude = {magY}')
		if debug: print(f'aY: {self.aY} ----> {self.aY + magY/self.mass}')
		self.aY += magY/self.mass
		

	def setPos(self, x, y):
		self.rect.center = (x, y)

	def decayA(self, amt):
		if self.aX > 0:
			self.aX -= amt
		if self.aY > 0:
			self.aY -= amt

		# failsafe
		if self.aX < 0:
			self.aX = 0

		if self.aY < 0:
			self.aY = 0

	def decayV(self, amt):
		if self.vX > 0:
			self.vX -= amt
		if self.vY > 0:
			self.vY -= amt

		# failsafe
		if self.vX < 0:
			self.vX = 0

		if self.vY < 0:
			self.vY = 0

	def updatePhysical(self):
		self.vX += self.aX
		self.vY += self.aY
		self.rect.x += self.vX*GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT']
		self.rect.y += self.vY*GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT']

class Projectile(Entity):
	def __init__(self, width, height, mass, color, magnitude, angle, x, y, worth):
		Entity.__init__(self, pygame.Surface((width, height)), mass)
		
		self.aX = magnitude*math.cos(math.radians(angle))
		self.aY = magnitude*math.sin(math.radians(angle))
		self.rect.center = (x, y)

		self.width, self.height, self.mass, self.color, self.magnitude, self.angle, self.x, self.y = width, height, mass, color, magnitude, angle, x, y
	
		self.image.fill(self.color)

		self.worth = worth

	def update(self, player, boundX, boundY, score):
		self.image.fill(self.color)

		decay = 1

		self.updatePhysical()

		# decay
		self.decayA(decay)

		# sprint(self.rect.center)

		# player 
		if self.rect.colliderect(player.rect):
			player.alive = False

	def clone(self, **kwargs):
		width, height, mass, color, magnitude, angle, x, y  = self.width, self.height, self.mass, self.color, self.magnitude, self.angle, self.x, self.y
		for i in kwargs.keys():
			if i == 'width':
				width = kwargs['width']
			if i == 'height':
				height = kwargs['height']
			if i == 'mass':
				mass = kwargs['mass']
			if i == 'color':
				color = kwargs['color']
			if i == 'magnitude':
				magnitude = kwargs['magnitude']
			if i == 'angle':
				angle = kwargs['angle']
			if i == 'x':
				x = kwargs['x']
			if i == 'y':
				y = kwargs['y']

		return Projectile(width, height, mass, color, magnitude, angle, x, y)

class Pulse(Projectile):
	def __init__(self, x, y):
		Projectile.__init__(self, width=10, height=200, mass=None, color=COLORS['ENEMY_PURPLE'], magnitude=10, angle=0, x=x, y=y, worth=10)

class Snowflake(Projectile):
	def __init__(self, x, y):
		Projectile.__init__(self, width=10, height=10, mass=None, color=COLORS['ENEMY_PURPLE'], magnitude=10, angle=0, x=x, y=y, worth=1)

class Deadeye(Projectile):
	def __init__(self, x, y):
		Projectile.__init__(self, width=100, height=10, mass=None, color=COLORS['ENEMY_PURPLE'], magnitude=10, angle=0, x=x, y=y, worth=5)

class Player(Entity):
	def __init__(self, width, height, mass, color):
		Entity.__init__(self, pygame.Surface((width, height)), mass)
		
		self.color = color
		self.image.fill(self.color)
		self.alive = True

	def update(self, keys, boundX, boundY):
		isBT = lambda: GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'] == GAME_SETTINGS['BT']['NORMAL_SPEED_EFFECT']

		self.image.fill(self.color)

		strength = 5
		decay = 1
		bounce = True
		bounce_ratio = 1/4

		if isBT and True in [keys['right'], keys['up'], keys['left'], keys['down']]:
			self.aX, self.aY = 0, 0

		if isBT:
			if keys['right']:
				self.newForce(strength, 0)

			if keys['up']:
				self.newForce(strength, 270)

			if keys['left']:
				self.newForce(strength, 180)

			if keys['down']:
				self.newForce(strength, 90)

		else:
			if keys['right']:
				self.vX += strength

			if keys['up']:
				self.vY += strength

			if keys['left']:
				self.vX -= strength

			if keys['down']:
				self.vY -= strength

		self.updatePhysical()

		# screen boundaries
		if self.rect.left < boundX[0]:
			self.rect.left = boundX[0]
			self.vX = self.vX*-bounce_ratio if bounce else 0

		if self.rect.right > boundX[1]:
			self.rect.right = boundX[1]
			self.vX = self.vX*-bounce_ratio if bounce else 0

		if self.rect.top < boundY[0]:
			self.rect.top = boundY[0]
			self.vY = self.vY*-bounce_ratio if bounce else 0

		if self.rect.bottom > boundY[1]:
			self.rect.bottom = boundY[1]
			self.vY = self.vY*-bounce_ratio if bounce else 0

		# decay
		self.decayA(decay)

# INITALIZATION ---------------------------------------------------------------------------------------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_SETTINGS['WIDTH'], WINDOW_SETTINGS['HEIGHT']))
boundX=[-10, WINDOW_SETTINGS['WIDTH']]
boundY=[-10,WINDOW_SETTINGS['HEIGHT']]
pygame.display.set_caption(WINDOW_SETTINGS['NAME'])
clock = pygame.time.Clock()
player = Player(width=20, height=20, mass=10, color=COLORS["CHAMBER_YELLOW"])
x, y = getCenterCoordinates()
player.setPos(WINDOW_SETTINGS['WIDTH']/4*3, y)

spawn = {
	'DEADEYE': {'DELAY': 1000, 'LOOP': 100}, 
	'SNOWFLAKE': {'DELAY': 1100, 'LOOP': 100},
	'PULSE': {'DELAY': 2000, 'LOOP': 100}
}

bulletSpawnHandler = TickBasedTimerHandler(spawn)
projectiles = pygame.sprite.Group()

allText = pygame.sprite.Group()
score = Score(x, y) # center
allText.add(score)

# GAME LOOP ---------------------------------------------------------------------------------------------------------------------------------------------------------------
running = True
while running:

	# GENERAL AND DEBUG ---------------------------------------------------------------------------------------------------------------------------------------------------------------
	clock.tick(WINDOW_SETTINGS['FPS'])
	bulletSpawnHandler.tickAll()

	# print(GAME_SETTINGS['BT']['CURRENT_SPEED_EFFECT'])

	# INPUT ---------------------------------------------------------------------------------------------------------------------------------------------------------------
	keys = {'left': False,
			'right': False,
			'up': False,
			'down': False, 
		}

	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_w]:
		keys['up'] = True
	   
	if pressed[pygame.K_s]:
		keys['down'] = True

	if pressed[pygame.K_a]:
		keys['left'] = True

	if pressed[pygame.K_d]:
		keys['right'] = True

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# UPDATE ---------------------------------------------------------------------------------------------------------------------------------------------------------------
	if not player.alive:
		running = False

	ringing = bulletSpawnHandler.checkRinging()
	for timer in ringing:
		if timer == 'DEADEYE':
			y = random.randint(boundY[0], boundY[1])
			projectiles.add(Deadeye(0, y))
		if timer == 'SNOWFLAKE':
			y = random.randint(boundY[0], boundY[1])
			projectiles.add(Snowflake(0, y))
		if timer == 'PULSE':
			y = random.randint(boundY[0], boundY[1])
			projectiles.add(Pulse(0, y))
	bulletSpawnHandler.deleteClosed()

	player.update(keys, boundX, boundY)
	projectiles.update(player, boundX, boundY, score)
	checkBT(player, projectiles)
	allText.update(projectiles, boundX, boundY)
	# print(projectiles.sprites())

	# RENDER ---------------------------------------------------------------------------------------------------------------------------------------------------------------
	screen.fill(COLORS['BLACK'])
	screen.blit(player.image, player.rect.center)
	projectiles.draw(screen)
	allText.draw(screen)
	pygame.display.flip()

pygame.time.wait(1000)
animationComplete = pygame.event.custom_type()
pygame.time.set_timer(animationComplete, 5000, 0)
running = True
while running:

	clock.tick(WINDOW_SETTINGS['FPS'])

	for event in pygame.event.get():
		if event.type == pygame.QUIT or event.type == animationComplete:
			running = False

	for sprite in projectiles:
		sprite.image.set_alpha(sprite.image.get_alpha()*(99/100))

	player.image.set_alpha(player.image.get_alpha()*(99/100))

	screen.fill(COLORS['BLACK'])
	screen.blit(player.image, player.rect.center)
	projectiles.draw(screen)
	allText.draw(screen)
	pygame.display.flip()

# TODO insert while loop to wait for input to restart game
pygame.quit()
sys.exit()