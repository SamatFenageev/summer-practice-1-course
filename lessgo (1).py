import pygame as pg
import sys
import time

import pygame.transform

pg.init()

sc = pg.display.set_mode((900, 700))
sc_rect = sc.get_rect()
pg.display.set_caption("Summer Practice")
components_color = (255,255,255)
font = pg.font.SysFont(None,14)
money_got = False
bottle_got= False
frames = 10


coin_sound = pg.mixer.Sound('звук_монеты.mp3')
bucks_sound = pg.mixer.Sound('звук_купюры.mp3')
water_sound = pg.mixer.Sound('water.mp3')
water_sound.set_volume(0.1)
change_sound = pg.mixer.Sound('получение сдачи.mp3')
change_sound.set_volume(0.3)

#сам аппарат
machine_image = pg.image.load('tmachine.png')

machine_image = pygame.transform.scale(machine_image,(620,700))
machine_rect = machine_image.get_rect()


#строка состояния
status_bar_rect = pg.Rect((345,200,67,27))

#приемник купюр
banknotes = pg.Rect((350,343,49,12))

#приемник монет
coins_hole = pg.Rect((375,294,12,30))

#кнопка выдачи сдачи
give_change_button = pg.Rect((481, 276, 21, 6))


#окно выдачи сдачи
get_change = pg.Rect((353,383,54,28))

#место, куда помещается бутылка
bottle_area = pg.Rect(100, 183, 217, 342)

#кнопка старта
start_button = pg.Rect((482,284,20,10))
start_button_clicked = False

change = pg.sprite.Group()
#10
class Ten(pygame.sprite.Sprite):
    def __init__(self, machine_rect):
        super().__init__()
        self.img = pg.image.load('10.png')
        self.rect = self.img.get_rect()
        self.rect.x = machine_rect.width+50
ten_coin = Ten(machine_rect)
ten_coin_rect = ten_coin.rect
ten_coin_rect.x = machine_rect.width+50



#1
class One(pygame.sprite.Sprite):
    def __init__(self, machine_rect):
        super().__init__()
        self.img = pg.image.load('1.png')
        self.rect = self.img.get_rect()
        self.rect.x = machine_rect.width+50
        self.rect.y = ten_coin_rect.height+10

one_coin = One(machine_rect)
one_coin_rect = one_coin.rect


#2
class Two(pygame.sprite.Sprite):
    def __init__(self, machine_rect):
        super().__init__()
        self.img = pg.image.load('2.png')
        self.rect = self.img.get_rect()
        self.rect.x = machine_rect.width+50
        self.rect.y = one_coin_rect.height+one_coin_rect.y+10

two_coin = Two(machine_rect)
two_coin_rect = two_coin.rect

#5
class Five(pygame.sprite.Sprite):
    def __init__(self, machine_rect):
        super().__init__()
        self.img = pg.image.load('5.png')
        self.rect = self.img.get_rect()
        self.rect.x = machine_rect.width+50
        self.rect.y = two_coin_rect.height+two_coin_rect.y+10

five_coin = Five(machine_rect)
five_coin_rect = five_coin.rect


#50
fifty_bucks = [pg.image.load('fifty.png'), pg.image.load('fifty1.png'),
               pg.image.load('fifty3.png'),pg.image.load('fifty5.png'),pg.image.load('fifty7.png'),pg.image.load('fifty8.png'),
               pg.image.load('fifty9.png')]
fifty_bucks_rect = fifty_bucks[0].get_rect()
fifty_bucks_rect.x = machine_rect.width+50
fifty_bucks_rect.y = five_coin_rect.height+five_coin_rect.y+10
fifty_got = False


#100
hundred_bucks = [pg.image.load('hundred.png'), pg.image.load('hundred1.png'),
                 pg.image.load('hundred3.png'),pg.image.load('hundred5.png'),pg.image.load('hundred7.png'),pg.image.load('hundred8.png'),
                 pg.image.load('hundred9.png')]
hundred_bucks_rect = hundred_bucks[0].get_rect()
hundred_bucks_rect.x = machine_rect.width+50
hundred_bucks_rect.y = fifty_bucks_rect.height+fifty_bucks_rect.y+10
hundred_got = False

#bottle
bottle = [pg.image.load('bulb.png'), pg.image.load('bulb1.png'),pg.image.load('bulb2.png'),
               pg.image.load('bulb3.png'),pg.image.load('bulb4.png'),pg.image.load('bulb5.png'),
               pg.image.load('bulb6.png'),pg.image.load('bulb7.png'),pg.image.load('bulb8.png'),
               pg.image.load('bulb9.png'),pg.image.load('bulb10.png'),pg.image.load('bulb11.png'),
         pg.image.load('bulb12.png'),pg.image.load('bulb13.png'),pg.image.load('bulb14.png')]

bottle_img = bottle[0]
bottle_rect = bottle_img.get_rect()
bottle_rect.x = hundred_bucks_rect.x-180
bottle_rect.y = hundred_bucks_rect.y+30
bottle_filled = False

bottle_moving, ten_moving, one_moving, two_moving, five_moving, fifty_moving, hundred_moving = False, False, False,False, False,False, False

balance = 0
change_is_given = False
def show_title():
    global balance,frames, change_is_given, status_bar_rect, start_button_clicked
    sc.fill((229,229,229))
    sc.blit(machine_image, machine_rect)
    sc.blit(ten_coin.img, ten_coin_rect)
    sc.blit(one_coin.img, one_coin_rect)
    sc.blit(two_coin.img, two_coin_rect)
    sc.blit(five_coin.img, five_coin_rect)
    sc.blit(fifty_bucks[0], fifty_bucks_rect)
    sc.blit(hundred_bucks[0], hundred_bucks_rect)
    
    sc.blit(bottle_img, bottle_rect)

    if change_is_given:
        status_bar_msg = font.render('Заберите сдачу', True, (0,0,0), None)
        status_bar_msg_rect = status_bar_msg.get_rect()
        status_bar_msg_rect.centerx = status_bar_rect.centerx
        status_bar_msg_rect.centery = status_bar_rect.centery

        sc.blit(status_bar_msg, status_bar_msg_rect)
        
    elif not money_got :
        status_bar_msg_1 = font.render('5 литров', True, (0,0,0), None)
        status_bar_msg_1_rect = status_bar_msg_1.get_rect()
        status_bar_msg_1_rect.center = status_bar_rect.center

        status_bar_msg_2 = font.render('=', True, (0,0,0), None)
        status_bar_msg_2_rect = status_bar_msg_2.get_rect()
        status_bar_msg_2_rect.center = status_bar_rect.center
        status_bar_msg_2_rect.y += 5

        status_bar_msg_3 = font.render('20 рублей', True, (0,0,0), None)
        status_bar_msg_3_rect = status_bar_msg_3.get_rect()
        status_bar_msg_3_rect.center = status_bar_rect.center
        status_bar_msg_3_rect.y += 15
        
        sc.blit(status_bar_msg_1, status_bar_msg_1_rect)
        sc.blit(status_bar_msg_2, status_bar_msg_2_rect)
        sc.blit(status_bar_msg_3, status_bar_msg_3_rect)

    elif money_got:
        if (balance%100)//10!=1 and balance%10==1: ending = "рубль"
        elif (balance%100)//10!=1 and balance%10<=4 and balance%10!=0: ending = " рубля"
        else: ending = " рублей"
        status_bar_msg = font.render(str(balance)+ending, True, (0,0,0), None)
        status_bar_msg_rect = status_bar_msg.get_rect()
        status_bar_msg_rect.centerx = status_bar_rect.centerx
        status_bar_msg_rect.centery = status_bar_rect.centery

        sc.blit(status_bar_msg, status_bar_rect)    
change_step = 10
coins_counter = 0
def prepare_change():
    global coins_counter, balance, change_is_given, change_step
    while balance//10 !=0:
        ten = Ten(machine_rect)
        ten.rect.x = 330
        ten.rect.y = 365
        ten.rect.x += change_step
        change_step += 10
        change.add(ten)
        balance -= 10
        coins_counter += 1
    while balance//5:
        five = Five(machine_rect)
        five.rect.x = 330
        five.rect.y = 365
        five.rect.x += change_step
        change_step += 10
        change.add(five)
        balance -= 5
        coins_counter += 1
    while balance//2:
        two = Two(machine_rect)
        two.rect.x = 330
        two.rect.y = 365
        two.rect.x += change_step
        change_step += 10
        change.add(two)
        balance -= 2
        coins_counter += 1
    while balance:
        one = One(machine_rect)
        one.rect.x = 330
        one.rect.y = 365
        one.rect.x += change_step
        change_step += 10
        change.add(one)
        balance -= 1
        coins_counter += 1
    change_sound.play(coins_counter-1)

def show_change():
    global sc, coin_sound
    for coin in change:
        sc.blit(coin.img, coin.rect)
        

while 1:
    show_title()
    #обрабатываем действия пользователя
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        #click check
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            if bottle_rect.collidepoint(x,y):
                bottle_moving = True
            elif ten_coin_rect.collidepoint(x,y):
                ten_moving = True
            elif one_coin_rect.collidepoint(x,y):
                one_moving = True
            elif two_coin_rect.collidepoint(x,y):
                two_moving = True
            elif five_coin_rect.collidepoint(x,y):
                five_moving = True
            elif fifty_bucks_rect.collidepoint(x,y):
                fifty_moving = True
            elif hundred_bucks_rect.collidepoint(x,y):
                hundred_moving = True

            elif give_change_button.collidepoint(x,y):
                money_got = False#деньги не закинуты
                change_is_given = True#сдача отдана\
                prepare_change()

            elif change_is_given:
                for coin in change:
                    if coin.rect.collidepoint(x,y):
                        change_is_given = False
                        change_sound.play(0, 1000)
                        
                        change.empty()
                        change_step = 10
                        coins_counter = 0
                                                
            if start_button.collidepoint(x,y) and balance >= 20 and bottle_got:
                start_button_clicked = True
                
        elif event.type == pg.MOUSEBUTTONUP:
            bottle_moving, ten_moving, one_moving, two_moving, five_moving, fifty_moving, hundred_moving = False, False, False,False, False,False, False

    if change_is_given:
        show_change()
        

    #передвижение
    if bottle_moving:
        bottle_rect.center = pg.mouse.get_pos()
    elif ten_moving:
        ten_coin_rect.center = pg.mouse.get_pos()
    elif two_moving:
        two_coin_rect.center = pg.mouse.get_pos()
    elif five_moving:
        five_coin_rect.center = pg.mouse.get_pos()
    elif one_moving:
        one_coin_rect.center = pg.mouse.get_pos()
    elif fifty_moving:
        fifty_bucks_rect.center = pg.mouse.get_pos()
    elif hundred_moving:
        hundred_bucks_rect.center = pg.mouse.get_pos()

    #collisions check
    if(bottle_rect.collidepoint(bottle_area.center)):
        bottle_got = True
        bottle_rect.center = bottle_area.center
    else:
        bottle_got = False

    if bottle_got and start_button_clicked and balance>=20:
        water_sound.play(0, 5000)
        if frames == 300:
            frames = 0
            bottle_got = False
            start_button_clicked = False
            bottle_filled = True
            balance -= 20
            if not balance:
                money_got = False
            bottle_img = bottle[14]
        sc.blit(bottle[frames // 20], (bottle_rect.x, bottle_rect.y))
        frames += 1

    if bottle_filled and bottle_rect.collidepoint(664, 530):
                bottle_img = bottle[0]
                bottle_rect.center = (584, 530)
        
    if (fifty_bucks_rect.collidepoint(banknotes.centerx, banknotes.y + banknotes.height)):
        bucks_sound.play(0, 1500)
        fifty_got = True
        money_got = True
        balance += 50
        fifty_bucks_rect.x = machine_rect.width + 50
        fifty_bucks_rect.y = five_coin_rect.height + five_coin_rect.y + 10
        fifty_moving = False

    if fifty_got:
        if frames == 50:
            frames = 0
            fifty_got = False
        sc.blit(fifty_bucks[frames // 10], (banknotes.x + 3, banknotes.y))
        frames += 1

    if (hundred_bucks_rect.collidepoint(banknotes.centerx, banknotes.y+banknotes.height)):
        bucks_sound.play(0, 1500)
        hundred_got = True
        money_got = True
        balance += 100
        hundred_bucks_rect.x = machine_rect.width+50
        hundred_bucks_rect.y = fifty_bucks_rect.height+fifty_bucks_rect.y+10
        hundred_moving = False
    if hundred_got:
        if frames == 50:
            frames = 0
            hundred_got = False
        sc.blit(hundred_bucks[frames//10], (banknotes.x+3, banknotes.y))
        frames += 1

    if one_coin_rect.collidepoint(coins_hole.center):
        coin_sound.play(0, 800)
        money_got = True
        balance += 1
        one_coin_rect.x = machine_rect.width+50
        one_coin_rect.y = ten_coin_rect.height+10
        one_moving = False

    if two_coin_rect.collidepoint(coins_hole.center):
        coin_sound.play(0, 800)
        money_got = True
        balance += 2
        two_coin_rect.x = machine_rect.width+50
        two_coin_rect.y = one_coin_rect.height+one_coin_rect.y+10
        two_moving = False

    if five_coin_rect.collidepoint(coins_hole.center):
        coin_sound.play(0, 800)
        money_got = True
        balance += 5
        five_coin_rect.x = machine_rect.width+50
        five_coin_rect.y = two_coin_rect.height+two_coin_rect.y+10
        five_moving = False

    if ten_coin_rect.collidepoint(coins_hole.center):
        coin_sound.play(0, 800)
        money_got = True
        balance += 10
        ten_coin_rect.x = machine_rect.width+50
        ten_coin_rect.y = 0
        ten_moving = False
    
    pg.display.flip()
