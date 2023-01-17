#!/usr/bin/env python3

import cv2
import mediapipe as mp
import pygame
import sys
import random
import configparser

from pygame.sprite import Group
from mediapipe.python.solutions import pose as mp_pose

import points as pt
import source as sr

# Configuration file
configfile_name = "config.ini" 
config = configparser.ConfigParser()
config.read(configfile_name)

# [paths]
FONT = config.get('paths','font')
pygame.font.init()

HANDS = config.get('paths', 'hands')
STAR = config.get('paths', 'estrella')

# [sizes]
SMALL_LETTER = config.getint('sizes', 'small_letter')
MEDIUM_LETTER = config.getint('sizes', 'medium_letter')
BIG_LETTER = config.getint('sizes', 'big_letter')

BIG_FONT = pygame.font.Font(FONT, BIG_LETTER)
MEDIUM_FONT = pygame.font.Font(FONT, MEDIUM_LETTER)
SMALL_FONTS = pygame.font.Font(FONT, SMALL_LETTER)

# [screen]
SCREEN_WIDTH = config.getint('screen', 'width')
SCREEN_HEIGHT = config.getint('screen', 'height')
MARGIN_SIZE = config.getint('screen', 'margin')

# [music]
PRESS_STAR = str(config.get('music','arro'))
FINAL_CLAPS = str(config.get('music','claps'))

BLACK = (0,0,0)

def get_mid(coord_a, coord_b, coord_c):
	return ((coord_a+coord_b+coord_c)/3)

def get_points(results):
	# For each hand
	left_x = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].x),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x))

	left_y = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].y),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y))
	
	right_x = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x))

	right_y = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y),
				float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y))

	# Coordinates
	return (left_x, left_y), (right_x, right_y)

def time_control(restart):
	if restart:
		return 0

def game():
	# Create the screen object
	# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	press_star = pygame.mixer.Sound(PRESS_STAR)
	claps = pygame.mixer.Sound(FINAL_CLAPS)

	right_source = sr.Source(screen, HANDS)
	left_source = sr.Source(screen, HANDS)
	hands = Group([right_source, left_source])

	points_left = Group()
	points_right = Group()
	
	# Initialise clock.
	clock_frames = pygame.time.Clock()
	start_ticks=pygame.time.get_ticks() #starter tick
	mp_pose = mp.solutions.pose

	bolas_restantes, aciertos = 10, 0
	bolas_r, bolas_l = bolas_restantes/2, bolas_restantes/2

	start, end = True, True
	# For webcam input:
	cap = cv2.VideoCapture(0)
	with mp_pose.Pose(
		model_complexity=1,
		smooth_landmarks=True,
		min_detection_confidence=0.7,
		min_tracking_confidence=0.7) as pose:

		while cap.isOpened():
			# Make sure game doesn't run at more than 60 frames per second.
			clock_frames.tick(60)

			# Check for any Pygame events.
			for event in pygame.event.get():
				# Exit game if user hits the quit button.
				## print(event)
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
					sys.exit()

			success, image = cap.read()
			resized = cv2.resize(image, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
			if not success:
				print("Ignoring empty camera frame.")
				# If loading a video, use 'break' instead of 'continue'.
				continue
		
			# Para "pegar" las ventanas
			image = cv2.cvtColor(cv2.flip(resized, 2), cv2.COLOR_BGR2RGB)
			results = pose.process(image)

			if not results.pose_landmarks:
				continue

			#visibility = [i.visibility for i in results.pose_landmarks.landmark]
			# 
			#checker = all(i >= 0.989 for i in visibility)
			id_1, id_2 = False, False
			for id, lm in enumerate(results.pose_landmarks.landmark):
				if (id == 12 and lm.visibility > 0.989):
					id_1 = True
				if (id == 11 and lm.visibility > 0.989):
					id_2 = True
			
			if start:
				pygame.surfarray.blit_array(screen, image.swapaxes(0, 1))
				seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
				if id_1 and id_2:
				# if checker:
					score_txt = BIG_FONT.render('{0}'.format(int(seconds)), True, BLACK)
					screen.blit(score_txt, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
					pygame.display.flip()
				else:
					start_ticks = pygame.time.get_ticks()

				if seconds>=3.2 and id_1 == True and id_2 == True: 
					start = False
				
			else:
				if id_1 and id_2:
				#if checker:
					# For left hand right bc is inverted

					# Creation of stars
					if len(points_left) == 0 and bolas_l != 0:
						left_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * SCREEN_WIDTH)
						left_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * SCREEN_HEIGHT)

						left_x = random.randint(MARGIN_SIZE, left_x_bound)
						left_y = random.randint(MARGIN_SIZE, left_y_bound)
							
						left_point = pt.Point(screen, STAR, left_x, left_y)
						left_point.time = pygame.time.get_ticks()
						points_left.add(left_point)

						bolas_l -= 1
						
					if len(points_right) == 0 and bolas_r != 0:
						right_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * SCREEN_WIDTH)
						right_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * SCREEN_HEIGHT)

						right_x = random.randint(right_x_bound, SCREEN_WIDTH-MARGIN_SIZE)
						right_y = random.randint(MARGIN_SIZE, right_y_bound)
							
						right_point = pt.Point(screen, STAR, right_x, right_y)
						right_point.time = pygame.time.get_ticks()
						points_right.add(right_point)
						bolas_r -= 1

				# Get the point in the hand
				left_hand, right_hand = get_points(results)

				# For each hand
				left_source.rect.centerx =  left_hand[0] * SCREEN_WIDTH
				left_source.rect.centery = left_hand[1] * SCREEN_HEIGHT
				right_source.rect.centerx = right_hand[0] * SCREEN_WIDTH
				right_source.rect.centery = right_hand[1] * SCREEN_HEIGHT

				pygame.surfarray.blit_array(screen, image.swapaxes(0, 1))

				hit_list_left = pygame.sprite.groupcollide(hands, points_left, False, True)
				hit_list_right = pygame.sprite.groupcollide(hands, points_right, False, True)

				# Check the list of colliding sprites, and add one to the score for each one.
				for _ in hit_list_right:
					bolas_restantes -= 1
					aciertos += 1
					press_star.play()

				for _ in hit_list_left:
					bolas_restantes -= 1
					aciertos += 1
					press_star.play()

				if len(points_left) > 0:
					points_left.update()

					if len(points_left) == 0:
						bolas_restantes -= 1

				if len(points_right) > 0:
					points_right.update()
					if len(points_right) == 0:
						bolas_restantes -= 1	

				if bolas_restantes <= 0:
					game_over_text = BIG_FONT.render(
						"Bien hecho", True, BLACK)
					screen.blit(game_over_text, game_over_text.get_rect(
						center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

					'''mistakes_txt = SMALL_FONTS.render(
						"Errores: {0}".format(bolas_r+bolas_l-aciertos), True, BLACK)
					screen.blit(mistakes_txt, (15, 50))'''

					mistakes_txt = SMALL_FONTS.render(
						"Aciertos: {0}".format(aciertos), True, BLACK)
					screen.blit(mistakes_txt, (15, 15))

					if end:
						claps.play()
						end = False
					pygame.display.flip()

					# No further processing is required.
					continue

				score_txt = SMALL_FONTS.render(
					"Bolas Restantes: {0}".format(bolas_restantes), True, BLACK)
				screen.blit(score_txt, (350, 15))

				time =  (pygame.time.get_ticks()/1000)
				
				time_txt = SMALL_FONTS.render(
					"Tiempo: {0}".format(int(time)), True, BLACK)
				screen.blit(time_txt, (15, 15))

				# Draw point on the screen
				hands.draw(screen)
				points_left.draw(screen)
				points_right.draw(screen)
				pygame.display.flip()

	cap.release()


def main():
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('De hombros hacia arriba')
    #setup()
    game()

if __name__ == '__main__':
    main()