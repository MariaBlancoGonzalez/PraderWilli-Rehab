#!/usr/bin/env python3

import cv2
import mediapipe as mp
import pygame
import sys
import random

from pygame.sprite import Group
from mediapipe.python.solutions import pose as mp_pose

from settings import * 
from aux import *
from sticker import Sticker
from source import Source
from animation import Animation


class Game:
	def __init__(self, options):
		self.screen = options.display

	'''def events(self, events):
		raise NotImplementedError("events must be defined")

	def update(self, dt):
		raise NotImplementedError("update must be defined")

	def draw(self, display):
		raise NotImplementedError("draw must be defined")'''

class Game_calibration(Game):
	def __init__(self, options):
		super().__init__(options)
		self.body = Sticker(self.screen, BODY, WIDTH/2, HEIGHT/2, 1000, 760)
		self.screen = options.display

		pygame.font.init()
		self.font_count = pygame.font.Font(FONT, EXTRA_BIG)
		self.font_message = pygame.font.Font(FONT, MEDIUM_FONT)
		self.instructions = self.font_message.render("Para probar la calibracion haz visibles los siguientes puntos en la pantalla", True, BLACK)

		# Puntos de la cabeza
		self.verde_cabeza = Sticker(self.screen, VERDE, 640, 80, 60,60)
		self.rojo_cabeza =  Sticker(self.screen, ROJO, 640, 80, 60,60)

		# Puntos de las manos
		self.verde_izq_mano = Sticker(self.screen, VERDE, 870, 400, 60,60)
		self.rojo_izq_mano=  Sticker(self.screen, ROJO, 870, 400, 60,60)

		self.verde_drch_mano = Sticker(self.screen, VERDE, 410, 400, 60,60)
		self.rojo_drch_mano =  Sticker(self.screen, ROJO, 410, 400, 60,60)

		# Puntos de los pies
		self.verde_drch_pie = Sticker(self.screen, VERDE, 600, 700, 60,60)
		self.rojo_drch_pie =  Sticker(self.screen, ROJO, 600, 700, 60,60)

		self.verde_izq_pie = Sticker(self.screen, VERDE, 680, 700, 60,60)
		self.rojo_izq_pie  =  Sticker(self.screen, ROJO, 680, 700, 60,60)

	def count(self, start_ticks):
		seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
		seconds_txt = self.font_count.render('{0}'.format(int(seconds)), True, BLACK)
		self.screen.blit(seconds_txt, (WIDTH/2, HEIGHT/2))
		pygame.display.flip()
		if seconds>=3.2:
			return True

	def calibrate(self):
		checker = [False, False, False, True, True]
		finish = False
		clock_frames = pygame.time.Clock()
		start_ticks=pygame.time.get_ticks() #starter tick
		cap = cv2.VideoCapture(0)
		with mp_pose.Pose(
			model_complexity=1,
			smooth_landmarks=True,
			min_detection_confidence=0.7,
			min_tracking_confidence=0.7) as pose:

			while cap.isOpened():
				# Make sure game doesn't run at more than 60 frames per second.
				clock_frames.tick(FPS)

				# Check for any Pygame events.
				for event in pygame.event.get():
					# Exit game if user hits the quit button.
					## print(event)
					if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
						sys.exit()

				success, image = cap.read()
				resized = cv2.resize(image, (WIDTH, HEIGHT)) 
				if not success:
					print("Ignoring empty camera frame.")
					# If loading a video, use 'break' instead of 'continue'.
					continue

				# Para "pegar" las ventanas
				image = cv2.cvtColor(cv2.flip(resized, 2), cv2.COLOR_BGR2RGB)
				results = pose.process(image)

				if not results.pose_landmarks:
					continue
				
				pygame.surfarray.blit_array(self.screen, image.swapaxes(0, 1))		
				
				# Cabeza
				if results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility > 0.8:
					if not all(item is True for item in checker):
						self.verde_cabeza.draw(self.screen)
					checker[0] = True
				else:
					self.rojo_cabeza.draw(self.screen)
					checker[0] = False

				# Manos
				if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.8:
					if not all(item is True for item in checker):
						self.verde_drch_mano.draw(self.screen)
					checker[1] = True
				else:
					self.rojo_drch_mano.draw(self.screen)
					checker[1] = False

				if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.8:
					if not all(item is True for item in checker):
						self.verde_izq_mano.draw(self.screen)
					checker[2] = True
				else:
					self.rojo_izq_mano.draw(self.screen)
					checker[2] = False

				# Pies
				'''if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].visibility > 0.8:
					if not all(item is True for item in checker):
						self.verde_drch_pie.draw(self.screen)
					checker[3] = True
				else:
					self.rojo_drch_pie.draw(self.screen)
					checker[3] = False

				if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].visibility > 0.8:
					if not all(item is True for item in checker):
						self.verde_izq_pie.draw(self.screen)
					checker[4] = True
				else:
					self.rojo_izq_pie.draw(self.screen)
					checker[4] = False
				'''
				if all(item is True for item in checker):
					finish = self.count(start_ticks)

				else:
					start_ticks = pygame.time.get_ticks()
					self.body.draw(self.screen)
					self.screen.blit(self.instructions, self.instructions.get_rect(
							center=(WIDTH/2, 750)))
					pygame.display.flip()

				if finish:
					cap.release()
					continue

class Game_diagonals(Game):
	def __init__(self, options):
		super().__init__(options)

		self.screen = options.display
		self.press_star = pygame.mixer.Sound(CLICKS)
		self.claps = pygame.mixer.Sound(CLAPS)
		self.explosion = pygame.mixer.Sound(EXPLOSION_SOUND)

		self.right_source = Source(self.screen, ROCKET)
		self.left_source = Source(self.screen, ROCKET)
		self.hands = Group([self.right_source, self.left_source])

		self.points_left = Group()
		self.points_right = Group()
		self.explosiones = Group()
		self.fireworks = Group()
		# Game settings
		self.trampas = PORCENTAJE_TRAMPAS
		self.velocidad_bolas = VELOCIDAD_ENTRE_BOLAS
		self.tiempo_juego = TIEMPO_JUEGO

		# Fonts
		pygame.font.init()
		self.font_message = pygame.font.Font(FONT, MEDIUM_FONT)
		self.font_bigger = pygame.font.Font(FONT, EXTRA_BIG)

		self.aciertos = 0
		self.errores = 0

		self.puntuacion = 0

	def information(self):
		time = pygame.time.get_ticks()
		while 1:
			# clear background
			self.screen.fill(GRIS)

			information_1 = self.font_message.render(
					"Con las manos, alcanza las estrellas que apareceran por encima de tus hombros.", True, WHITE)
			self.screen.blit(information_1, information_1.get_rect(
					center=(WIDTH/2, HEIGHT/2)))

			information_2 = self.font_message.render("Ten en cuenta que las estrellas se difuminan a los 3 segundos de aparecer", True, WHITE)
			self.screen.blit(information_2, information_2.get_rect(
					center=(WIDTH/2, HEIGHT/2+50)))
			pygame.display.flip()

			if ((pygame.time.get_ticks()-time)/1000)>=3.0:
				break

	def game(self):
		# Initialise clock.
		clock_frames = pygame.time.Clock()
		time = pygame.time.get_ticks()

		min = int(self.tiempo_juego/60)
		sec = int(self.tiempo_juego%60)
		computed_time = 999
		end = False

		cap = cv2.VideoCapture(0)
		with mp_pose.Pose(
			model_complexity=1,
			smooth_landmarks=True,
			min_detection_confidence=0.7,
			min_tracking_confidence=0.7) as pose:

			while cap.isOpened():
				
				# Make sure game doesn't run at more than 60 frames per second.
				clock_frames.tick(FPS)

				# Check for any Pygame events.
				for event in pygame.event.get():
					# Exit game if user hits the quit button.
					if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
						sys.exit()

				success, image = cap.read()
				resized = cv2.resize(image, (WIDTH, HEIGHT)) 
				if not success:
					print("Ignoring empty camera frame.")
					# If loading a video, use 'break' instead of 'continue'.
					continue

				# Para "pegar" las ventanas
				image = cv2.cvtColor(cv2.flip(resized, 2), cv2.COLOR_BGR2RGB)
				results = pose.process(image)

				if not results.pose_landmarks:
					continue

				# If not all points are visible stop the game	
				visibility = [i.visibility for i in results.pose_landmarks.landmark]
				#checker = all(i >= 0.3 for i in visibility)
				checker = True
				if checker:
					# For left hand right bc is inverted
					# Creation of stars or tramp
					left_tramp = random.random() < self.trampas
					right_tramp = random.random() < self.trampas
					if len(self.points_left) == 0 and not left_tramp:
						left_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * WIDTH)
						left_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * HEIGHT)

						left_x = random.randint(MARGIN, left_x_bound)
						left_y = random.randint(MARGIN, left_y_bound)
							
						if left_x > WIDTH:
							left_x = WIDTH - MARGIN

						if left_y > HEIGHT:
							left_y = HEIGHT - MARGIN

						left_point = Sticker(self.screen, ESTRELLA, left_x, left_y, 75, 75)
						left_point.time = pygame.time.get_ticks()
						self.points_left.add(left_point)

					elif len(self.points_left) == 0 and left_tramp:
						left_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * WIDTH)
						left_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * HEIGHT)

						left_x = random.randint(MARGIN, left_x_bound)
						left_y = random.randint(MARGIN, left_y_bound)
							
						if left_x > WIDTH:
							left_x = WIDTH - MARGIN

						if left_y > HEIGHT:
							left_y = HEIGHT - MARGIN

						left_point = Sticker(self.screen, BOMBA, left_x, left_y, 75, 75, True)
						left_point.time = pygame.time.get_ticks()
						self.points_left.add(left_point)

					if len(self.points_right) == 0 and not right_tramp:
						right_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * WIDTH)
						right_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * HEIGHT)

						right_x = random.randint(right_x_bound, WIDTH-MARGIN)
						right_y = random.randint(MARGIN, right_y_bound)

						if right_x > WIDTH:
							right_x = WIDTH - MARGIN

						if right_y > HEIGHT:
							right_y = HEIGHT - MARGIN
								
						right_point = Sticker(self.screen, ESTRELLA, right_x, right_y, 75, 75)
						right_point.time = pygame.time.get_ticks()
						self.points_right.add(right_point)

					elif len(self.points_right) == 0 and right_tramp:
						right_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * WIDTH)
						right_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * HEIGHT)

						right_x = random.randint(right_x_bound, WIDTH-MARGIN)
						right_y = random.randint(MARGIN, right_y_bound)

						if right_x > WIDTH:
							right_x = WIDTH - MARGIN

						if right_y > HEIGHT:
							right_y = HEIGHT - MARGIN
								
						right_point = Sticker(self.screen, BOMBA, right_x, right_y, 75, 75, True)
						right_point.time = pygame.time.get_ticks()
						self.points_right.add(right_point)

				# Get the point in the hand
				left_hand, right_hand = get_points(results)

				# For each hand
				self.left_source.rect.centerx =  left_hand[0] * WIDTH
				self.left_source.rect.centery = left_hand[1] * HEIGHT
				self.right_source.rect.centerx = right_hand[0] * WIDTH
				self.right_source.rect.centery = right_hand[1] * HEIGHT

				pygame.surfarray.blit_array(self.screen, image.swapaxes(0, 1))

				hit_list_left = pygame.sprite.groupcollide(self.hands, self.points_left, False, True)
				hit_list_right = pygame.sprite.groupcollide(self.hands, self.points_right, False, True)

				# Check the list of colliding sprites, and add one to the score for each one.
				for _ in hit_list_right:
					if right_point.trampa:
						self.errores += 1
						self.puntuacion -= FALLO
						explosion = Animation(self.screen, right_point.rect.centerx, right_point.rect.centery, EXPLOSION, FPS_EXPLOSION)
						self.explosiones.add(explosion)
						self.explosion.play()
					else:
						self.aciertos += 1
						self.puntuacion += ACIERTO
						firework = Animation(self.screen, right_point.rect.centerx, right_point.rect.centery, FIREWORKS, FPS_FIREWORKS)
						self.fireworks.add(firework)
						self.press_star.play()

				for _ in hit_list_left:
					if left_point.trampa:
						self.errores += 1
						self.puntuacion -= FALLO
						explosion = Animation(self.screen, left_point.rect.centerx, left_point.rect.centery, EXPLOSION, FPS_EXPLOSION)
						self.explosiones.add(explosion)
						self.explosion.play()
					else:
						self.aciertos += 1
						self.puntuacion += ACIERTO
						firework = Animation(self.screen, left_point.rect.centerx, left_point.rect.centery, FIREWORKS, FPS_FIREWORKS)
						self.fireworks.add(firework)
						self.press_star.play()

				if len(self.points_left) > 0:
					self.points_left.update()

				if len(self.points_right) > 0:
					self.points_right.update()

				if computed_time <= 0:
					game_over_text = self.font_bigger.render(
						"Bien hecho", True, BLACK)
					self.screen.blit(game_over_text, game_over_text.get_rect(
						center=(WIDTH // 2, HEIGHT // 2)))

					mistakes_txt = self.font_message.render(
						"Aciertos: {0}".format(self.aciertos), True, BLACK)
					self.screen.blit(mistakes_txt, (15, 15))
 
					if end:
						self.claps.play()
						end = False
					pygame.display.flip()
					cap.release()
					continue

				new_time = (pygame.time.get_ticks() - time)/1000

				computed_time = self.tiempo_juego-int(new_time)
				
				min = int(computed_time/60)
				sec = int(computed_time%60)
				time_txt = self.font_message.render(
					"Tiempo: {0}".format(f'{min}:{sec}' if sec != 0 else f'{min}:00'), True, BLACK)
				self.screen.blit(time_txt, (15, 15))

				puntuacion = self.font_message.render(
					"Puntuacion: ", True, BLACK)
				self.screen.blit(puntuacion, (900, 15))

				puntos = self.font_message.render(
					"{0}".format(self.puntuacion), True, COLOR_ROJO)
				self.screen.blit(puntos, (1050, 15))

				# Draw point on the screen
				self.hands.draw(self.screen)
				self.points_left.draw(self.screen)
				self.points_right.draw(self.screen)
				self.explosiones.draw(self.screen)
				self.explosiones.update()
				self.fireworks.draw(self.screen)
				self.fireworks.update()
				pygame.display.flip()
