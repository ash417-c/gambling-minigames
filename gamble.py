'''
supported games:
black jack

future:
baccarat
hitman?
''' 
import sys
import os
from deck import BlackJack
import pygame    

class AnimatedCard:
    def __init__(self, card_front, x, target_y, auto_flip=True, start_fall=True):
        self.front = card_front
        self.x = x
        self.y = -300
        self.target_y = target_y
        self.flipping = False
        self.falling = start_fall
        self.fall_speed = 15 # pixels per frame
        self.width = 1.0 # 1 -> 0, 0 -> 1
        self.primary_face = 'BACK'
        self.flip_speed = 0.05 # % of width
        self.autoflip = auto_flip
        self.finished = False
        if start_fall == False:
            self.y = self.target_y

    def get_status(self):
        return self.finished

    def force_flip(self):
        self.flipping = True

    def update(self):
        if self.falling and self.y <= self.target_y:
            self.y += self.fall_speed
            if self.y > self.target_y:
                self.y = self.target_y
                self.falling = False
                self.flipping = self.autoflip
        if self.flipping:
            if self.primary_face == 'BACK':
                self.width -= self.flip_speed
                if self.width <= 0:
                    self.width = 0
                    self.primary_face = self.front
            else:
                self.width += self.flip_speed
                if self.width >= 1:
                    self.width = 1
                    self.flipping = False
                    self.finished = True

    def draw(self, surface, cards_path):
        img = pygame.image.load(os.path.join(cards_path, self.primary_face+'.png'))
        new_width = img.get_width() * self.width
        img_scaled = pygame.transform.scale(img, (new_width, img.get_height()))
        surface.blit(img_scaled, (self.x+((img.get_width() - new_width) // 2),self.y))

def pygame_manager(blackjack:BlackJack):
    if hasattr(sys, '_MEIPASS'):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cards_path = os.path.join(BASE_DIR, "cards")
    other_path = os.path.join(BASE_DIR, "assets")

    pygame.init()
    pygame.display.set_caption('BlackJack')
    clock = pygame.time.Clock()
    running = True # pygame running

    display_width = 1200
    display_height = 900
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    def image_loader(img):# to /assets
        return pygame.image.load(os.path.join(other_path, img+'.png'))
    def card_push(img, x,y):
        gameDisplay.blit(pygame.image.load(os.path.join(cards_path, img+'.png')), (x,y))
    def status_push(img, x=display_width/2, y=display_height/2):
        if not img == 'not over':
            image = image_loader(img)
            x -= image.get_width()/2
            y -= image.get_height()/2 +40
            gameDisplay.blit(image, (x,y))
    def player_options(diplay_moves=True):
        if diplay_moves:
            gameDisplay.blit(image_loader('hit'), (850, 300))
            gameDisplay.blit(image_loader('stand'), (0, 300))
        gameDisplay.blit(pygame.transform.scale(image_loader('new hand'), (100,50)), (5, 5))

    #check if points intesect
    def intersect(mousepos, targetpos, spread=350):
        x_valid = targetpos[0]-spread <= mousepos[0] <= targetpos[0]+spread
        y_valid = targetpos[1]-spread <= mousepos[1] <= targetpos[1]+spread
        return x_valid and y_valid
    
    #important points
    STAND_COORDS = (display_width//3, display_height//2)
    HIT_COORDS = (display_width, display_height//2)
    RESET_COORDS = (0,0)

    #coords for player cards
    x =  list(range(int(display_width * 0.4), display_width, 75))
    y = list(range(int(display_height * 0.7), 0, -90))

    #coords for dealer cards
    dealx =  list(range(int(display_width * 0.05), display_width, 200))
    dealy = [int(display_height * 0.05)]*len(dealx)

    stable_cards = []
    animating_cards = []
    hidden_card = AnimatedCard(blackjack.get_dealers_hidden(), dealx[0], dealy[1], start_fall=False)
    stable_cards.append(hidden_card)

    game_on = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:#on click
                pos = pygame.mouse.get_pos()
                if intersect(pos, HIT_COORDS) and game_on:
                    blackjack.hit()
                    new_card_img = blackjack.get_players_hand().get_card(-1)
                    animating_cards.append(AnimatedCard(new_card_img, x[len(blackjack.get_players_hand())-1], y[len(blackjack.get_players_hand())-1]))
                elif intersect(pos, STAND_COORDS):
                    blackjack.stand()
                elif intersect(pos, RESET_COORDS) and not game_on:
                    game_on = True
                    animating_cards = []
                    stable_cards = []
                    blackjack.reset()
                    hidden_card = AnimatedCard(blackjack.get_dealers_hidden(), dealx[0], dealy[1], start_fall=False)
                    stable_cards.append(hidden_card)

        if game_on and blackjack.player_turn_over():
            game_on = False
            animating_cards.append(stable_cards[0])
            blackjack.game_end()
            for card, i in zip(blackjack.get_dealers_hand().cards(), range(len(blackjack.get_dealers_hand()))):
                if i > 1:
                    animating_cards.append(AnimatedCard(card, dealx[i], dealy[i]))


        # fill the screen with a color to wipe away anything from last frame
        gameDisplay.fill("green")

        #players cards
        for card_img, i in zip(blackjack.get_players_hand().cards(), range(2)):
            card_push(card_img, x[i], y[i])
        
        #dealers cards
        for card_img, i in zip(blackjack.get_dealers_hand().cards(hide_first=game_on), range(2)):
            if i != 0:
                card_push(card_img, dealx[i], dealy[i])

        #stable cards
        for card in stable_cards:
            if game_on == False:
                hidden_card.force_flip()
            card.update()
            card.draw(gameDisplay, cards_path)

        #animate cards
        if len(animating_cards) > 0:
            animating_cards[0].update()
            animating_cards[0].draw(gameDisplay, cards_path)
            if animating_cards[0].get_status():
                stable_cards.append(animating_cards.pop(0))

        #player options
        player_options(game_on)

        #game status on top after animations
        if len(animating_cards) == 0:
            status_push(blackjack.get_result())

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
    
def main():
    black_jack = BlackJack()
    pygame_manager(black_jack)

if __name__ == '__main__':
    main()
