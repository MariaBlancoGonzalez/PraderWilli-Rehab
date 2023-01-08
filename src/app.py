import cv2
import mediapipe as mp
import pygame
from pygame.sprite import Group
from mediapipe.python.solutions import pose as mp_pose
import points as pt
import sys
import random
import configparser
import circle as cl

# Configuration file
configfile_name = "config.ini" 
config = configparser.ConfigParser()
config.read(configfile_name)

# [paths]
FONT = config.get('paths','font')
pygame.font.init()

HANDS = config.get('paths', 'hands')
BALLS = config.get('paths', 'balls')

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

BLACK = (0,0,0)

def game():
  # Create the screen object
  # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  right_circle = cl.Circle(screen, HANDS)
  left_circle = cl.Circle(screen, HANDS)
  hands = Group([right_circle, left_circle])

  points_left = Group()
  points_right = Group()

  # Initialise clock.
  clock = pygame.time.Clock()
  mp_pose = mp.solutions.pose

  bolas_restantes, errores = 10, 0
  bolas_r, bolas_l = bolas_restantes/2, bolas_restantes/2
  # For webcam input:
  cap = cv2.VideoCapture(0)
  with mp_pose.Pose(
      model_complexity=1,
      smooth_landmarks=True,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
      # Make sure game doesn't run at more than 60 frames per second.
      clock.tick(60)

      # Check for any Pygame events.
      for event in pygame.event.get():
        # Exit game if user hits the quit button.
        ## print(event)
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
          sys.exit()

      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
      
      # Para "pegar" las ventanas
      image = cv2.cvtColor(cv2.flip(image, 2), cv2.COLOR_BGR2RGB)
      results = pose.process(image)

      if not results.pose_landmarks:
        continue

      id_1, id_2 = False, False
      for id, lm in enumerate(results.pose_landmarks.landmark):
        if (id == 12 and lm.visibility > 0.989):
          id_1 = True
        if (id == 11 and lm.visibility > 0.989):
          id_2 = True

      if id_1 and id_2:
        # Creates balls random with some bounds
        # For left hand right bc is inverted
        # In pixel
        if len(points_left) == 0 and bolas_l != 0:
          left_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * SCREEN_WIDTH)
          left_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * SCREEN_HEIGHT)

          left_x = random.randint(MARGIN_SIZE, left_x_bound)
          left_y = random.randint(MARGIN_SIZE, left_y_bound)
        
          points_left.add(pt.Point(screen, BALLS, left_x, left_y))
          bolas_l -= 1
        
        if len(points_right) == 0 and bolas_r != 0:
          right_x_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * SCREEN_WIDTH)
          right_y_bound = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * SCREEN_HEIGHT)

          right_x = random.randint(right_x_bound, SCREEN_WIDTH-MARGIN_SIZE)
          right_y = random.randint(MARGIN_SIZE, right_y_bound)
          # In pixels
          points_right.add(pt.Point(screen, BALLS, right_x, right_y))
          bolas_r -= 1

      left_circle.rect.centerx = float(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x) * SCREEN_WIDTH
      left_circle.rect.centery = float(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y) * SCREEN_HEIGHT
      right_circle.rect.centerx = float(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x) * SCREEN_WIDTH
      right_circle.rect.centery = float(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y) * SCREEN_HEIGHT

      pygame.surfarray.blit_array(screen, image.swapaxes(0, 1))

      hit_list_left = pygame.sprite.groupcollide(hands, points_left, False, True)
      hit_list_right = pygame.sprite.groupcollide(hands, points_right, False, True)

      # Check the list of colliding sprites, and add one to the score for each one.
      for _ in hit_list_right:
        bolas_restantes -= 1

      for _ in hit_list_left:
        bolas_restantes -= 1

      if bolas_restantes <= 0:
        game_over_text = BIG_FONT.render(
            "Fin", True, BLACK)
        screen.blit(game_over_text, game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.flip()

        # No further processing is required.
        continue

      score_txt = SMALL_FONTS.render(
        "Bolas Restantes: {0}".format(bolas_restantes), True, BLACK)
      screen.blit(score_txt, (15, 15))

      mistakes_txt = SMALL_FONTS.render(
        "Errores: {0}".format(errores), True, BLACK)
      screen.blit(mistakes_txt, (480, 15))

      # Draw point on the screen
      hands.draw(screen)
      points_left.draw(screen)
      points_right.draw(screen)
      pygame.display.flip()

  cap.release()

def setup():
  """ This is for show all points before start, it is not done"""
  '''checker = False
      for id, lm in enumerate(results.pose_landmarks.landmark):
        if lm.visibility < 0.99:
          # Instruction msg
          checker = True
          break'''

  '''if checker:
        instructions = ALL_FONTS.render(
            "Situase donde se vea todo", True, (0, 0, 0))
        screen.blit(instructions, instructions.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.flip()
      else:
        instructions = ALL_FONTS.render(
            "XXXX", True, (0, 0, 0))
        screen.blit(instructions, instructions.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.flip()'''

def main():
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('De hombros hacia arriba')
    game()

if __name__ == '__main__':
    main()