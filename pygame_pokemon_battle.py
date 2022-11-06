# a pokemon battle game with pygame
# the player will be able to move around a map until challenged by a trainer
# once challenged, the player will take part in a pokemon battle with the computer

import pygame, os, random
pygame.init()

# defining constants
WIN_X = 600
WIN_Y = 600
WIN = pygame.display.set_mode((WIN_X,WIN_Y))

# colour palette
WHITE = (255,255,255)
DARK_GREEN = (29,53,29)
RED = (237,28,36)
YELLOW = (253,240,90)
LIGHT_GREEN = (88,186,76)
BLACK = (0,0,0)

pygame.display.set_caption("Pokemon Battle")

class Pokemon:
    # a class to create pokemon for the player and computer
    def __init__(self,name,file_name,player,total_hp,current_hp,element,moves):
        # constructing pokemon with specific properties
        self.name = name
        self.file_name = file_name
        self.player = player
        self.total_hp = total_hp
        self.current_hp = current_hp
        self.element = element
        self.moves = moves
        self.image = pygame.image.load(os.getcwd() + "\\" + self.file_name)
        if self.player == True:  # the player and computer pokemon have different coordinates
            self.x = -(self.image.get_width())
            self.y = WIN_Y/4
        else:
            self.x = WIN_X
            self.y = WIN_Y/15
        self.length = self.image.get_width()
        self.width = self.image.get_height()
    def draw(self):
        # draws the pokemon on the game screen
        WIN.blit(self.image,(int(self.x),int(self.y)))
    def enter(self,new_x,vel=20):
        # animation for entering
        if self.player == True:
            if self.x < new_x:
                self.x += vel     # player enters from the left
        else:
            if self.x > new_x:
                self.x -= vel     # computer enters from the right
    def faint(self,new_size):
        # an animation for fainting
        if self.length >= new_size:
            self.length -= 5      # the image of the pokemon will get smaller until no longer visible
            self.width -= 5
        else:
            self.length = 0
            self.width = 0
        self.image = pygame.transform.scale(self.image,(abs(self.length),abs(self.width)))

class Attack:
    animations = ["diagonal","drop"]  # two movement options
    done = False
    def __init__(self,name,file_name,sound,damage,player,start_x,x,start_y):
        # constructing moves with specific properties
        self.name = name
        self.file_name = file_name
        self.sound = sound
        self.damage = damage
        self.player = player
        # type of movement is random, image & sound effect are specific based on type of move
        self.animation = random.choice(Attack.animations)
        if self.animation == "diagonal":
            self.x = start_x  # starting for diagional animation
            self.y = start_y
        else:
            self.x = x        # starting coordinates for drop animation
            self.y = -200
        self.image = pygame.image.load(os.getcwd()+"\\"+file_name)
        self.sound_effect = pygame.mixer.Sound(os.getcwd()+"\\"+sound)
    def animate(self,end_x,end_y):
        # animating the image for the attack
        Attack.done = False  # keeps track of when the attack animation is done
        if self.animation == "diagonal":  # diagonal animation
            if self.player:
                if self.x < end_x and self.y > end_y:
                    self.x += 16
                    self.y -= 8
                    WIN.blit(self.image,(int(self.x),int(self.y)))
                else:
                    Attack.done = True    # updating the attack "done" boolean
            else:
                if self.x > end_x and self.y < end_y:
                    self.x -= 16
                    self.y += 8
                    WIN.blit(self.image,(int(self.x),int(self.y)))
                else:
                    Attack.done = True
        else:                             # drop animation
            if self.y < end_y:
                self.y += 20
                WIN.blit(self.image,(int(self.x),int(self.y)))
            else:
                Attack.done = True
    def play_sound(self):
        # playing the sound effect for the attack
        self.sound_effect.play()

def text(words,font,x,y,colour):
    # blits text onto the screen
    text = font.render(words,1,colour)
    WIN.blit(text,(x,y))

def switch_music(new_music,volume,path=os.getcwd()+"\\"):
    # switches the music (will be used at different game statuses)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(path+new_music)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

# defining the font styles that will be used throughout the program
main_font = pygame.font.SysFont("ubuntu mono",23)
small_font = pygame.font.SysFont("ubuntu mono",15)

# creating collision boxes for the map
# coordinates and sizes are declared as a fractions of the screen's x/y values
# using int() for each value to make sure coordinates are always integers
coll1_l = int(WIN_X*(9/20))
coll1_w = int(WIN_Y/5)
coll1_y = WIN_Y-coll1_w
coll1 = pygame.Rect(0,coll1_y,coll1_l,coll1_w)

coll2_w = int(WIN_Y/2+22)
coll2_y = int(WIN_Y/7)
coll2 = pygame.Rect(0,coll2_y,coll1_l,coll2_w)

coll3_l = int(WIN_X*(7/20)+15)
coll3_x = int(WIN_X-coll3_l)
coll3 = pygame.Rect(coll3_x,0,coll3_l,WIN_Y)

# defining details for a box (and the text inside it)
bottom_box_l = int(WIN_X*(9/10))
bottom_box_w = int(WIN_Y*(1/5))
bottom_box_x = int(WIN_X/2 - bottom_box_l/2)
bottom_box_y = int(WIN_Y*(3/4))

bottom_text_x = int(WIN_X/10)
bottom_text1_y = int(WIN_Y*(4/5))
bottom_text2_y = int(WIN_Y*(17/20))
small_text_x = int(WIN_X*(11/20)+25)
small_text_y = int(WIN_Y*(9/10)+10)

# loading images for the map
path = os.getcwd() + "\\"
map_background = pygame.image.load(path+"map.png")
exclamation = pygame.image.load(path+"exclamation.png")
pokeball = pygame.image.load(path+"pokeball.png")

# storing specific player images in lists (for walking animation)
player_right = [pygame.image.load(path+"playerright1.png"),pygame.image.load(path+"playerrightstill.png"),
                pygame.image.load(path+"playerright2.png")]
player_left = [pygame.image.load(path+"playerleft1.png"),pygame.image.load(path+"playerleftstill.png"),
               pygame.image.load(path+"playerleft2.png")]
player_up = [pygame.image.load(path+"playerup1.png"),pygame.image.load(path+"playerupstill.png"),
             pygame.image.load(path+"playerup2.png")]
player_down = [pygame.image.load(path+"playerdown1.png"),pygame.image.load(path+"playerdownstill.png"),
               pygame.image.load(path+"playerdown2.png")]

# the trainer only needs to move right
trainer_move = [pygame.image.load(path+"trainerright1.png"),
                pygame.image.load(path+"trainerrightstill.png"),
                pygame.image.load(path+"trainerright2.png")]

# details about the player's sprite
player_vel = 2
player_size = player_right[0].get_width()
player_x = WIN_X/2
player_y = WIN_Y/2
player_direction = "up"
player_img = player_down
p_walk_count = 1

# details about the trainer's sprite
trainer_vel = 1
trainer_x = WIN_X/20
trainer_y = coll2_y+coll2_w+player_vel+3
trainer_walk = False
t_walk_count = 1

# booleans to make certain elements appear/disappear
talk_box = False
talk1 = True
talk2 = False
mouse_down = False
blackout = False
play_trainer_notice = True
play_battle_end = True
game_map = True

# details for the blackout animation
blackout_r = 10
pokeball_x = WIN_X/2-pokeball.get_width()/2
pokeball_y = -pokeball.get_width()

loop_count = 0  # counts each iteration of the loop

# playing the starting music
switch_music("map_music.mp3",0.5)

# -------------------------------------------------------------------------------------------------------#
# PART 1: MAP WITH TRAINER
# -------------------------------------------------------------------------------------------------------#
# the player will be able to move anywhere on the path until they reach the trainer's line of sight
# once they reach the trainer's line of sight, they will be challenged to a battle (and forced to accept)

while game_map:
    pygame.time.delay(10)
    WIN.blit(map_background,(0,0))
    keys = pygame.key.get_pressed()

    # collision box for the player
    player_box = pygame.Rect(player_x,player_y,player_size,player_size)

    # PLAYER MOVEMENT (WITH COLLISIONS AND WALKING ANIMATION)
    # ----------------------------------------------------------------------------------------------------
    # detecting keyboard input
    if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        # the player and trainer's walk count variables only increase every 10 frames
        # otherwise, the legs would be moving too fast
        if loop_count < 10:
            loop_count += 1
        else:
            loop_count = 0         # general loop count resets after 10
            if p_walk_count == 2:  # player walk count resets after 2
                p_walk_count = 0
            else:
                p_walk_count += 1  # increasing the walk count to switch between images
        if keys[pygame.K_RIGHT]:   # checking which direction and updating the direction variable
            player_direction = "right"
            player_img = player_right
            # checking for collisions with the pre-defined rectangles
            if coll3.collidepoint(player_x+player_size,player_y) == 0 and trainer_walk == False:
                player_x += player_vel
        elif keys[pygame.K_LEFT]:  # player movement to the left
            player_direction = "left"
            player_img = player_left
            if player_x > 0 and coll1.collidepoint(player_x-player_vel,player_y+player_size) == 0\
                and coll2.collidepoint(player_x-player_vel,player_y) == 0 and trainer_walk == False:
                player_x -= player_vel
        elif keys[pygame.K_UP]:    # player movement upwards
            player_direction = "up"
            player_img = player_up
            if 5 <= player_y and trainer_walk == False\
                and coll2.collidepoint(player_x,player_y-player_vel) == 0:
                player_y -= player_vel
        elif keys[pygame.K_DOWN]:  # player movement downwards
            player_direction = "down"
            player_img = player_down
            if player_y <= WIN_Y-player_size-10 and trainer_walk == False\
                and coll1.collidepoint(player_x,player_y+player_size+player_vel) == 0\
                and coll2.collidepoint(player_x,player_y+player_vel) == 0:
                player_y += player_vel
    else:
        p_walk_count = 1  # player image will be still if they aren't moving

    # ENCOUNTERING THE TRAINER
    # ----------------------------------------------------------------------------------------------------
    WIN.blit(trainer_move[t_walk_count],(int(trainer_x),int(trainer_y)))
    # detecting if the player is in the trainer's line of sight
    if player_y > coll2_y and player_x <= trainer_x + 150:
        trainer_walk = True

    if trainer_walk:
        if play_trainer_notice:  # playing the trainer notice music
            switch_music("trainer_notice.mp3",0.5)
            play_trainer_notice = False
        WIN.blit(player_left[1],(int(player_x),int(player_y)))  # still image of player
        if trainer_x+player_size <= player_x:
            # using the general loop count for the trainer's walk count (same way as player)
            if loop_count < 10:
                loop_count += 1
            else:
                if t_walk_count == 2:
                    t_walk_count = 0
                else:
                    t_walk_count += 1
                loop_count = 0
            trainer_x += trainer_vel
            # speech bubble with exclamation mark
            WIN.blit(exclamation,(int(trainer_x-5),int(trainer_y-player_size-5)))
        else:
            t_walk_count = 1
            talk_box = True
    else:
        WIN.blit(player_img[p_walk_count],(int(player_x),int(player_y)))  # player walking animation

    if talk_box:
        # talk box will use the pre-defined bottom box coordinates
        # will be blitted at the top instead of the bottom because the encounter happens near the bottom
        pygame.draw.rect(WIN,WHITE,(bottom_box_x,int(WIN_Y/20),bottom_box_l,bottom_box_w))
        if talk1:    # first line of dialogue
            text("Hey, I see you have Pokemon!",main_font,bottom_text_x,int(WIN_Y/10),DARK_GREEN)
            text("click anywhere to continue",small_font,small_text_x,int(WIN_Y/5+10),DARK_GREEN)
            if mouse_down:
                talk1 = False
                talk2 = True
        elif talk2:  # second line of dialogue
            text("I challenge you to a Pokemon battle!",main_font,bottom_text_x,int(WIN_Y/10),DARK_GREEN)
            text("click anywhere to continue",small_font,small_text_x,int(WIN_Y/5+10),DARK_GREEN)
            if mouse_down:
                blackout = True

    # ANIMATION TO BLACK OUT THE SCREEN
    # ----------------------------------------------------------------------------------------------------
    if blackout:             # a pokeball will enter the screen from the top
        if pokeball_y <= WIN_X/2-pokeball.get_width()/2:
            pokeball_y += 10
            WIN.blit(pokeball,(int(pokeball_x),int(pokeball_y)))
            # switching to battle music
            switch_music("battle_music.mp3",2.5)
        else:                # a black circle with an expanding radius will be drawn
            pygame.draw.circle(WIN,BLACK,(int(WIN_X/2),int(WIN_Y/2)),int(blackout_r))
            WIN.blit(pokeball,(int(pokeball_x),int(WIN_X/2-pokeball.get_width()/2)))
            blackout_r += 5  # increasing blackout circle's radius
            if blackout_r >= 600:
                blackout = True
                game_map = False

    mouse_down = False       # resetting the mouse down variable
    pygame.display.update()
    for event in pygame.event.get():
        # detecting input from the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        elif event.type == quit:
            pygame.quit()
            sys.exit

# -------------------------------------------------------------------------------------------------------#
# PART 2: POKEMON BATTLE
# -------------------------------------------------------------------------------------------------------#
# the player and the computer each get one fire type pokemon and one water type pokemon
# the player will get the option to fight or switch pokemon (unless they only have one left)
# will include gameplay elements like missing, critical hits, elemental multipliers, computer switching

# variables for where the player & computer pokemon should end up
p_pok_x = int(WIN_X/20)
p_pok_y = int(WIN_Y/4)
c_pok_x = int(WIN_X*(13/20))
c_pok_y = int(WIN_Y/15)

# initializing specific moves with the Attack class
p_moves = [Attack("SOAK","soak.png","soak.wav",30,True,p_pok_x,c_pok_x,p_pok_y),
           Attack("BUBBLE BEAM","bubble_beam.png","bubble_beam.wav",20,True,p_pok_x,c_pok_x,p_pok_y),
           Attack("INFERNO","inferno.png","inferno.wav",40,True,p_pok_x,c_pok_x,p_pok_y),
           Attack("EMBER","ember.png","ember.wav",20,True,p_pok_x,c_pok_x,p_pok_y)]
c_moves = [Attack("WATER GUN","water_gun.png","water_gun.wav",30,False,c_pok_x,p_pok_x,c_pok_y),
           Attack("VORTEX","hydro_vortex.png","hydro_vortex.wav",30,False,c_pok_x,p_pok_x,c_pok_y),
           Attack("LAVA PLUME","lava_plume.png","flare_blitz.wav",40,False,c_pok_x,p_pok_x,c_pok_y),
           Attack("FLARE BLITZ","flare_blitz.png","flare_blitz.wav",30,False,c_pok_x,p_pok_x,c_pok_y)]

# initializing specific pokemon using the Pokemon class
poks = [Pokemon("WAILORD","wailord.png",True,140,140,"water",p_moves[:2]),
        Pokemon("NINETALES","ninetales.png",True,130,130,"fire",p_moves[2:]),
        Pokemon("KINGLER","kingler.png",False,120,120,"water",c_moves[:2]),
        Pokemon("FLAREON","flareon.png",False,110,110,"fire",c_moves[2:])]
# the computer attacks first each round, so the player was given slightly better hp to even it out

p_poks = []  # list for the player's pokemon
c_poks = []  # list for the computer's pokemon
for i in poks:
    if i.player == True:
        p_poks.append(i)
    else:
        c_poks.append(i)

c_pok = random.choice(c_poks)  # computer randomly selects a starting pokemon
p_pok = random.choice(p_poks)  # player gets a default starting pokemon too
pok_vel = 20

# loading images that will be used for the battle
battle_background = pygame.image.load(path+"battle_background.png")
player = pygame.image.load(path+"player.png")
trainer = pygame.image.load(path+"youngster_joey.png")

# variables for the images of the two trainers
player_x_ = WIN_X
player_y_ = int(WIN_Y*(3/20))
trainer_x_ = int(-(trainer.get_width()))
trainer_y_ = int(WIN_X/20)

# variables for boxes pointing to each pokemon
p_box_l = int(WIN_X*(2/5))
p_box_w = int(WIN_X/5)
p_box_x = int(WIN_X/4 - p_box_l/2)
p_box_y = int(WIN_Y/20)
c_box_x = int(WIN_X*(3/4) - p_box_l/2)
c_box_y = int(WIN_Y*(2/5))
triangle_size = int(WIN_Y/20)

# variables for the hp bar
p_hp_back_l = int(WIN_X*(7/20)-15)
p_hp_back_w = int(WIN_Y/20)
p_hp_bar_l = int(WIN_X*(7/20)-50)
p_hp_bar_w = int(WIN_Y/20-10)
p_hp_colour = LIGHT_GREEN
c_hp_colour = LIGHT_GREEN

# variables for text and buttons that the player will be able to click
button_l = int(WIN_X*(7/20))
button_w = int(WIN_Y/20)
button_x = int(WIN_X*(11/20))
button1_y = int(WIN_X*(4/5)-5)
button2_y = button1_y+button_w+10

button_text_x = button_x+10
button1_text_y = button1_y+2
button2_text_y = button2_y+2

button1 = pygame.Rect(button_x,button1_y,button_l,button_w)
button2 = pygame.Rect(button_x,button2_y,button_l,button_w)

# booleans to track user input
button1_pressed = False
button2_pressed = False
mouse_down = False

# booleans to track which screen should be shown
opening_sequence = False
c_sendout = False
p_sendout = False
options = False
pick_move = False
switch_pok = False
show_c_attack = False
show_p_attack = False
end_screen = False

# other booleans for the game's progress
show_hp_bars = False
p_attack = False
p_pok_enter = False
p_pok_exit = False
c_pok_exit = False
players_enter = True
apply_c_damage = False
c_faint = False

# list of booleans with a 1/10 chance of True (used for random gameplay elements)
true_false = [True,False,False,False,False,False,False,False,False,False]

# variables to make it easier to write text (will be updated throughout the program)
bottom_text1 = ""
bottom_text2 = ""
small_text = ""

while game_map == False:
    pygame.time.delay(5)
    WIN.blit(battle_background,(0,0))

    # drawing the bottom box using the variables
    pygame.draw.rect(WIN,WHITE,(bottom_box_x,bottom_box_y,bottom_box_l,bottom_box_w))
    p_pok.draw()  # drawing the player's pokemon
    c_pok.draw()  # drawing the computer's pokemon

    # DISPLAYING THE HP BARS
    # ----------------------------------------------------------------------------------------------------
    if show_hp_bars:  # using the variables defined outside the loop
        # player's hp bar:
        p_hp_length = int(p_pok.current_hp/p_pok.total_hp*(WIN_X*(7/20)-50))
        p_hp_text = str(int(p_pok.current_hp)) + "/" + str(p_pok.total_hp)
        pygame.draw.rect(WIN,WHITE,(p_box_x,p_box_y,p_box_l,p_box_w))
        pygame.draw.rect(WIN,WHITE,pygame.Rect(p_box_x+50,p_box_y+55,p_hp_bar_l,p_hp_bar_w))
        pygame.draw.rect(WIN,DARK_GREEN,(p_box_x+20,p_box_y+50,p_hp_back_l,p_hp_back_w))
        pygame.draw.rect(WIN,WHITE,pygame.Rect(p_box_x+50,p_box_y+55,p_hp_bar_l,p_hp_bar_w))
        pygame.draw.polygon(WIN,WHITE,((int(WIN_X/4-triangle_size/2),p_box_y+p_box_w),
                                       (int(WIN_X/4+triangle_size/2),p_box_y+p_box_w),
                                       (int(WIN_X/4),p_box_y+p_box_w+triangle_size)))
        text(p_pok.name+" (you)",main_font,p_box_x+20,p_box_y+20,DARK_GREEN)
        text("HP",main_font,p_box_x+24,int(WIN_Y*(3/20)-8),WHITE)
        # making sure the hp doesn't go into the negatives
        if p_pok.current_hp >= 0:
            # changing the hp bar's colour based on how much health is left
            if p_pok.current_hp/p_pok.total_hp > 1/2:
                p_hp_colour = LIGHT_GREEN
            elif 1/2 > p_pok.current_hp/p_pok.total_hp > 1/3:
                p_hp_colour = YELLOW
            elif p_pok.current_hp/p_pok.total_hp < 1/3:
                p_hp_colour = RED
            pygame.draw.rect(WIN,p_hp_colour,(p_box_x+50,p_box_y+55,p_hp_length,int(WIN_Y*(1/20)-10)))
            text(p_hp_text,main_font,int(WIN_X*(5/20)+12),p_box_y+80,DARK_GREEN)
        else:
            text("0/0",main_font,int(WIN_X*(3/10)+7),p_box_y+80,DARK_GREEN)

        # computer's hp bar:
        c_hp_length = int(c_pok.current_hp/c_pok.total_hp*(WIN_X*(7/20)-50))
        pygame.draw.rect(WIN,DARK_GREEN,pygame.Rect(c_box_x,c_box_y,p_box_l,p_box_w))
        pygame.draw.rect(WIN,WHITE,pygame.Rect(c_box_x+20,c_box_y+50,p_hp_back_l,p_hp_back_w))
        pygame.draw.rect(WIN,DARK_GREEN,(c_box_x+50,c_box_y+55,p_hp_bar_l,p_hp_bar_w))
        pygame.draw.polygon(WIN,DARK_GREEN,((int(WIN_X*(3/4)-triangle_size/2),c_box_y),
                                            (int(WIN_X*(3/4)+triangle_size/2),c_box_y),
                                            (int(WIN_X*(3/4)),c_box_y-triangle_size)))
        text(c_pok.name+" (enemy)",main_font,c_box_x+20,c_box_y+20,WHITE)
        text("HP",main_font,c_box_x+24,int(WIN_Y*(1/2)-8),DARK_GREEN)
        if c_pok.current_hp >= 0:  # changing the computer's hp bar colour too
            if c_pok.current_hp/c_pok.total_hp > 1/2:
                c_hp_colour = LIGHT_GREEN
            elif 1/2 > c_pok.current_hp/c_pok.total_hp > 1/3:
                c_hp_colour = YELLOW
            elif c_pok.current_hp/c_pok.total_hp < 1/3:
                c_hp_colour = RED
            pygame.draw.rect(WIN,c_hp_colour,(c_box_x+50,c_box_y+55,c_hp_length,int(WIN_Y*(1/20)-10)))

    # BATTLE OPENING (BLACKOUT ANIMATION AND OPENING SEQUENCE)
    # ----------------------------------------------------------------------------------------------------
    # continuing the blackout animation from the map
    if blackout:
        if blackout_r > 10:
            blackout_r -= 10      # decreasing the radius of the black circle
            pygame.draw.circle(WIN,BLACK,(int(WIN_X/2),int(WIN_Y/2)),blackout_r)
            WIN.blit(pokeball,(pokeball_x,int(WIN_X/2-pokeball.get_width()/2)))
        else:
            if pokeball_y <= WIN_Y:
                pokeball_y += 10  # moving the pokeball back down to exit the screen
                WIN.blit(pokeball,(pokeball_x,pokeball_y))
            else:
                blackout = False  # updating booleans
                opening_sequence = True
    # opening sequence that includes images of the player and computer's trainer
    if opening_sequence:
        if players_enter:
            if player_x_ >= WIN_X*(1/5):
                player_x_ -= 15   # player's character entering
            if trainer_x_ <= WIN_X*(7/10):
                trainer_x_ += 15  # computer's trainer entering
        else:
            player_x_ += 15       # player's trainer leaving
            trainer_x_ -= 15      # computer's trainer leaving
            if trainer_x_ <= -(trainer.get_width()) or player_x_ >= WIN_X:
                c_sendout = True
                opening_sequence = False
        WIN.blit(trainer,(trainer_x_,trainer_y_))
        WIN.blit(player,(player_x_,player_y_))
        bottom_text1 = "YOUNGSTER JOEY wants to fight!"
        small_text = "click anywhere to continue"
        if mouse_down:
            players_enter = False # letting the player exit the opening sequence by clicking

    # SENDING OUT THE POKEMON
    # ----------------------------------------------------------------------------------------------------
    if c_sendout:             # computer's pokemon emerging from the right
        c_pok.enter(c_pok_x)  # using the pokemon class's enter function
        bottom_text1 = "YOUNGSTER JOEY sent out "+c_pok.name
        bottom_text2 = ""
        small_text = "click anywhere to continue"
        if mouse_down:        # letting the player go to the next screen themself
            c_sendout = False
            p_sendout = True
    elif p_sendout:           # player's pokemon emerging from the left
        if c_faint == False:  # when the computer's pokemon faints, only the computer sendout is needed
            p_pok.enter(p_pok_x)
            bottom_text1 = "Go "+p_pok.name+"!"
            bottom_text2 = ""
            small_text = "click anywhere to continue"
            if mouse_down:
                p_sendout = False
                options = True
                show_hp_bars = True
        else:
            p_sendout = False
            options = True

    # PLAYER'S CHOICES
    # ----------------------------------------------------------------------------------------------------
    elif options:  # the player will get to choose between fighting and switching pokemon
        if len(p_poks) > 1:
            # the player only gets a choice if they have more than one pokemon left
            bottom_text1 = "What would "+p_pok.name
            bottom_text2 = "like to do?"
            small_text = ""
            # drawing the buttons and adding text using the pre-defined variables
            pygame.draw.rect(WIN,DARK_GREEN,(button1))
            pygame.draw.rect(WIN,DARK_GREEN,(button2))
            text("FIGHT",main_font,button_text_x,button1_text_y,WHITE)
            text("SWITCH POKEMON",main_font,button_text_x,button2_text_y,WHITE)
            if button1_pressed or button2_pressed:
                # checking if either buttons were pressed
                options = False
                if button1_pressed:
                    pick_move = True
                elif button2_pressed:
                    switch_pok = True
        else:
            options = False
            pick_move = True
    elif pick_move:  # the player will get to pick a move
        bottom_text1 = "Pick a move!"
        bottom_text2 = ""
        small_text = ""
        # drawing the buttons and text
        pygame.draw.rect(WIN,DARK_GREEN,(button1))
        pygame.draw.rect(WIN,DARK_GREEN,(button2))
        text(p_pok.moves[0].name,main_font,button_text_x,button1_text_y,WHITE)
        text(p_pok.moves[1].name,main_font,button_text_x,button2_text_y,WHITE)
        if button1_pressed or button2_pressed:
            # updating booleans
            switch_pok = False
            pick_move = False
            p_attack = True
            show_c_attack = True
            if button1_pressed:
                p_move = p_pok.moves[0]  # updating the player's move
            elif button2_pressed:
                p_move = p_pok.moves[1]
            p_damage = p_move.damage     # assigning damage (from the attack object)
            apply_c_damage = True
    elif switch_pok:  # the player will get to choose a new pokemon
        p_attack = False
        bottom_text1 = "Choose your Pokemon!"
        bottom_text2 = ""
        small_text = ""
        pygame.draw.rect(WIN,DARK_GREEN,(button1))
        pygame.draw.rect(WIN,DARK_GREEN,(button2))
        # using the list of player's pokemon for the button choices
        text(p_poks[0].name,main_font,button_text_x,button1_text_y,WHITE)
        text(p_poks[1].name,main_font,button_text_x,button2_text_y,WHITE)
        if button1_pressed or button2_pressed:
            # checking which button was pressed and which pokemon should be assigned
            if button1_pressed:
                new_p_pok = p_poks[0]
            elif button2_pressed:
                new_p_pok = p_poks[1]
            p_pok_exit = True
        if p_pok_exit:            # the player's old pokemon will exit the screen
            p_pok.x -= pok_vel
            if p_pok.x <= int(-(p_pok.image.get_width())):
                p_pok_exit = False
                p_pok = new_p_pok # reassigning the player pokemon variable
                p_pok_enter = True
        if p_pok_enter:           # the player's new pokemon will enter the screen
            p_pok.enter(p_pok_x)
            if p_pok.x >= p_pok_x:
                switch_pok = False
                p_pok_enter = False
                show_c_attack = True
                apply_c_damage = True

    # ATTACKS
    # ----------------------------------------------------------------------------------------------------
    elif apply_c_damage:  # this block isn't for graphics; it just applies computer damage each round
        # the computer picks a random move each round
        c_move = random.choice(c_pok.moves)
        c_damage = c_move.damage
        if len(c_poks) > 1:  # the computer will randomly switch if it still has two pokemon
            c_switch = random.choice(true_false)
        # using random to apply random critical hits and misses
        c_crit_hit = random.choice(true_false)
        p_crit_hit = random.choice(true_false)
        p_miss = random.choice(true_false)
        c_miss = random.choice(true_false)
        if c_switch == False and c_miss == False:
            # updating the computer's damage based on the conditions above
            if c_crit_hit:
                c_damage = c_damage*2
            elif c_pok.current_hp <= 0:
                c_damage = 0
            # applying elemental multipliers (water strong against fire, fire weak against water)
            elif c_pok.element == "water" and p_pok.element == "fire":
                c_damage = c_damage*1.5
            elif c_pok.element == "fire" and p_pok.element == "water":
                c_damage = c_damage/1.5
            p_pok.current_hp -= c_damage  # updating the player's current hp
            c_move.play_sound()           # playing the computer's attack sound
        elif c_switch:
            c_miss = False                # the computer won't be able to miss if they switched
            c_pok_exit = True             # giving the computer a new pokemon
            new_c_pok = random.choice(c_poks)
            c_damage = 0                  # the computer does no damage if it's switching
            while new_c_pok == c_pok:     # the computer won't be able to switch to its current pokemon
                new_c_pok = random.choice(c_poks)
        # resetting the attack coordinates back to their starting positions
        if p_attack:
            if p_move.animation == "drop":
                p_move.x = c_pok_x
                p_move.y = -200
            else:
                p_move.x = p_pok_x
                p_move.y = p_pok_y
        if c_move.animation == "drop":
            c_move.x = p_pok_x
            c_move.y = -200
        else:
            c_move.x = c_pok_x
            c_move.y = c_pok_y
        # making sure the block of code above only executes for one iteration of the loop each round
        apply_c_damage = False
        
    # graphically displaying the computer's turn:
    elif show_c_attack and switch_pok == False:
        small_text = "click anywhere to continue"
        if mouse_down:
            show_c_attack = False
            show_p_attack = True
            if p_pok.current_hp <= 0:  # checking if the player's pokemon was knocked out
                p_poks.remove(p_pok)
                if len(p_poks) > 0:
                    p_pok = p_poks[0]  # reassigning the player's pokemon if necessary
                p_sendout = True
                c_faint = False
                p_attack = False
            if p_attack and p_pok.current_hp >= 0 and p_miss == False:
                # applying the player's damage; this block is nested under the mouse down condition
                # so that it only executes for one iteration of the loop each round
                if p_crit_hit:               # checking for gameplay elements
                    p_damage = p_damage*2
                elif p_pok.current_hp <= 0:  # the player's pokemon won't do any damage if it fainted
                    p_damage = 0
                elif p_pok.element == "water" and c_pok.element == "fire":
                    p_damage = p_damage*1.5
                elif p_pok.element == "fire" and c_pok.element == "water":
                    p_damage = p_damage/1.5
                c_pok.current_hp -= p_damage # updating computer's hp
                p_move.play_sound()
        if c_pok_exit and c_switch:
            c_pok.x += pok_vel               # making the computer's current pokemon exit if switched
            if c_pok.x > WIN_X:
                c_pok = new_c_pok            # reassigning the computer's pokemon
                c_pok_exit = False
        else:
            c_pok.enter(c_pok_x)             # the computer's new pokemon enters
        # displaying specific text based on what the computer did
        if c_switch:
            bottom_text1 = "YOUNGSTER JOEY switched their Pokemon"
            bottom_text2 = "to " + c_pok.name
        elif c_miss:
            bottom_text1 = c_pok.name + " (enemy) tried to attack with"
            bottom_text2 = c_move.name + " but missed!"
        else:  # if the computer attacked
            bottom_text1 = c_pok.name + " (enemy) attacked with " + c_move.name
            # special text based on certain conditions
            if c_crit_hit:
                bottom_text2 = "Critical hit!"
            elif c_damage >= 40:
                bottom_text2 = "Ouch!"
            elif c_damage < 20:
                bottom_text2 = "Not so effective..."
            else:
                bottom_text2 = ""
            c_move.animate(p_pok_x,p_pok_y)
            if p_pok.current_hp <= 0:
                # informing the player if their pokemon has fainted
                bottom_text2 = p_pok.name + " has fainted!"
                # player's fainting animation will begin when the computer's attack animation is over
                if Attack.done:
                    p_pok.faint(0)
                    
    # graphically displaying the player's turn:
    elif show_p_attack:
        small_text = "click anywhere to continue"
        if p_attack:  # displaying text based on what the player did
            bottom_text1 = p_pok.name + " (you) attacked with " + p_move.name
            if p_miss == False:
                p_move.animate(c_pok_x,c_pok_y)
                # special text that will appear under certain conditions
                if p_crit_hit:
                    bottom_text2 = "Critical hit!"
                elif p_damage >= 40:
                    bottom_text2 = "Great choice!"
                elif p_damage <= 20:
                    bottom_text2 = "Not so effective..."
                else:
                    bottom_text2 = ""
                if c_pok.current_hp <= 0:
                    # informing the player if their opponent died
                    bottom_text2 = c_pok.name + " (enemy) has fainted!"
                    # computer's fainting animation will begin when the player's attack animation is over
                    if Attack.done:
                        c_pok.faint(0)
            else:   # informing the player if their pokemon missed
                bottom_text1 = p_pok.name + " (you) tried to attack with"
                bottom_text2 = p_move.name + " but missed. Yikes!"
        else:       # confirming the player's pokemon switch
            bottom_text1 = "You switched your Pokemon to " + p_pok.name
            bottom_text2 = ""
        if mouse_down:
            show_p_attack = False
            p_attack = False
            p_miss = False
            if c_pok.current_hp <= 0: # checking if the computer fainted
                c_poks.remove(c_pok)
                c_faint = True
                if len(c_poks) > 0:
                    c_pok = c_poks[0] # reassigning the computer's pokemon if necessary
                    c_sendout = True  # going back to the computer's sendout screen to inform the player
            if len(c_poks) > 0 and len(p_poks) > 0:
                options = True        # going back to the options screen for the next round

    # GAME OVER SCREEN
    # ----------------------------------------------------------------------------------------------------
    if len(c_poks) == 0 or len(p_poks) == 0:
        if play_battle_end:
            # switching the background music to the game over music
            switch_music("battle_end.mp3",1)
            play_battle_end = False
        # making sure none of the previous screens appear
        show_hp_bars = False
        p_sendout = False
        c_sendout = False
        pick_move = False
        options = False
        p_pok.x -= 15  # the player's pokemon leaving the screen
        c_pok.x += 15  # the trainer's pokemon leaving the screen
        if (p_pok.x <= -(p_pok.image.get_width()) and len(c_poks) == 0)\
           or (c_pok.x >= WIN_X and len(p_poks) == 0):
            # the player and computer's characters will enter after their pokemon have left
            if player_x_ >= WIN_X*(1/5):
                player_x_ -= 15  # the player's character enters from the right to the left
            if trainer_x_ <= WIN_X*(7/10):
                trainer_x_ += 15 # the trainer enters from the left to the right
            WIN.blit(trainer,(trainer_x_,trainer_y_))
            WIN.blit(player,(player_x_,player_y_))
            small_text = "click anywhere to exit"
            # displaying specific text based on whether the player won or lost
            if len(c_poks) == 0:
                bottom_text1 = "YOUNGSTER JOEY: I have no Pokemon left!"
                bottom_text2 = "Looks like you win. Congratulations!"
            else:
                bottom_text1 = "YOUNGSTER JOEY: You have no more"
                bottom_text2 = "Pokemon left? Yay, I win! Good game."
            # exiting out of the loop to exit the game
            if mouse_down:
                break

    # displaying text based on the text variables (that were updated throughout the program)
    text(bottom_text1,main_font,bottom_text_x,bottom_text1_y,DARK_GREEN)
    text(bottom_text2,main_font,bottom_text_x,bottom_text2_y,DARK_GREEN)
    text(small_text,small_font,small_text_x,small_text_y,DARK_GREEN)

    # changing the booleans for player input back to False
    mouse_down = False
    button1_pressed = False
    button2_pressed = False

    pygame.display.update()
    for event in pygame.event.get():
        # checking if the player clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            # checking if the player clicked on one of the mouse buttons
            if button1.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                button1_pressed = True
            elif button2.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                button2_pressed = True
        elif event.type == quit:
            pygame.quit()
            sys.exit
