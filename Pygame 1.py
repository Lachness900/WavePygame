import pygame
import random
import math

# Variables
running = True
ScreenHeight = 500
ScreenWidth = 400
enemySpawnSpeed = 250
enemySpeed = 1
clockOn = True
finalTime = 0
buffs =3
kills = 0
health = 10
maxHealth = 10
MagicOpen = False
playerLastLookDirection = (1,0)
currentSpellX = 0
currentSpellY = 0
cursorMoveX = 0
cursorMoveY = 0
clock = pygame.time.Clock()
win = False
lose = False


#Start game
pygame.init()
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    K_SPACE,
    K_LSHIFT,
    QUIT,
)

#Surfaces
screen = pygame.display.set_mode([ScreenWidth, ScreenHeight])
pygame.font.init()
Text = pygame.font.SysFont('Arial',30)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center = (ScreenWidth/2+10,ScreenHeight/2+10))
    def update(self, pressed_keys):
        if MagicOpen == False:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -4)
                
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 4)
                
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-4, 0)
                
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(4, 0)
            

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ScreenWidth:
            self.rect.right = ScreenWidth
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= ScreenHeight:
            self.rect.bottom = ScreenHeight

player = Player()

class Fireball1(pygame.sprite.Sprite):
    def __init__(self,facing,buffs):
        super(Fireball1, self).__init__()
        self.surf = pygame.Surface((80+buffs/3,80+buffs/3))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center=(player.rect.left+10,player.rect.top+10))
        self.facing = facing
        self.buffs = buffs
        

    def update(self):
        self.rect.move_ip(10*self.facing[0],10*self.facing[1])

        self.surf.fill((0,255,0))
        if self.rect.left > ScreenWidth+50 or self.rect.top> ScreenHeight + 50:
            self.kill()
    
class Earth1(pygame.sprite.Sprite):
    def __init__(self, buffs):
        super(Earth1,self).__init__()
        self.surf = pygame.Surface((ScreenWidth,ScreenHeight))
        self.surf.set_alpha(100)
        self.surf.fill((255,255,255))
        self.size = 0
        self.rect = pygame.draw.circle(self.surf,(255,255,0,100),(player.rect.x-ScreenWidth/2+10,player.rect.y-ScreenHeight/2+10),self.size)
        self.buffs = buffs
    def update(self):
        pygame.draw.circle(self.surf,(255,255,0), (ScreenWidth/2,ScreenHeight/2), self.size,3)
        print(player.rect.clamp(self.rect).center)
        self.size += 4
        newRing = EarthRing(self.size,pygame.time.get_ticks())
        earthrings.add(newRing)
        if self.size>80+self.buffs/6:
            earthrings.empty()
            self.kill()

class EarthRing(pygame.sprite.Sprite):
    def __init__(self,size,time):
        super(EarthRing,self).__init__()
        self.size = int(round(math.sqrt(2*size*size)))
        self.surf = pygame.Surface((self.size,self.size))
        self.surf.set_alpha(100)
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect(center=(player.rect.left+10,player.rect.top+10))
        self.starttime = time

    




class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        self.surf = pygame.Surface((12,12),pygame.SRCALPHA)
        self.surf.fill((0,0,0))
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect(center=(50,ScreenHeight-50))

    def start(self):
        self.surf.set_alpha(150)
    
    def moveUp(self):
        self.rect.move_ip(0,-10)

    def moveDown(self):
        self.rect.move_ip(0,10)

    def moveLeft(self):
        self.rect.move_ip(-10,0)

    def moveRight(self):
        self.rect.move_ip(10,0)

    def stop(self,MoveX,MoveY):
        self.surf.set_alpha(0)
        self.rect.move_ip(-MoveX,-MoveY)

cursor = Cursor()

class CastMagic(pygame.sprite.Sprite):
    def __init__(self,center,color,spellNumber):
        super(CastMagic,self).__init__()
        self.surf = pygame.Surface((10,10))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect(center = center)
        self.spell = spellNumber

MagicSystem = CastMagic(center =(50,ScreenHeight-50), spellNumber=0, color = (200,200,200))
FirstSpell = CastMagic(center =(60,ScreenHeight-50),spellNumber =1, color = (0,255,0))
SecondSpell = CastMagic(center=(40,ScreenHeight-50),spellNumber=2,color =(255,255,0))
ThridSpell = CastMagic(center =(50,ScreenHeight-40),spellNumber=2,color =(0,255,255))
FourthSpell =CastMagic(center = (50,ScreenHeight-60),spellNumber=2,color =(255,0,255))

Spells =            [[ThridSpell],
        [SecondSpell,MagicSystem,FirstSpell],
                    [FourthSpell]]



class Enemy(pygame.sprite.Sprite):
    def __init__(self,speed):
        # Randomize position
        TempEnemyPosX=random.randint(0, ScreenWidth)
        TempEnemyPosY=random.randint(0, ScreenWidth)
        if(TempEnemyPosX>player.rect.left):
            TempEnemyPosX = TempEnemyPosX + 100
        else:
            TempEnemyPosX = TempEnemyPosX - 100
        
        if(TempEnemyPosY>player.rect.left):
            TempEnemyPosY = TempEnemyPosY + 100
        else:
            TempEnemyPosY = TempEnemyPosY - 100

        # Constructor Stuff
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (TempEnemyPosX,TempEnemyPosY))
        self.speed = 1 + round(math.log10(speed))
    def update(self):
        #triangulate player
        try:
            direction = math.atan((player.rect.top-self.rect.top)/(player.rect.left-self.rect.left))
            if (player.rect.left-self.rect.left > 0):
                self.rect.move_ip(self.speed*2*math.cos(direction),self.speed*2*math.sin(direction))
            else:
                self.rect.move_ip(self.speed*-2*math.cos(direction),self.speed*-2*math.sin(direction))
        except:
            try:
                direction = (player.rect.top-self.rect.top)/(player.rect.top-self.rect.top)
                self.rect.move_ip(direction,0)
            except:
                self.kill()

#add user events        
        
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, enemySpawnSpeed)

# Instantiate everything

magicSlots = pygame.sprite.Group()
spells = pygame.sprite.Group()
enemies = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
earths = pygame.sprite.Group()
earthrings = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
magicSlots.add(MagicSystem)
magicSlots.add(FirstSpell)
magicSlots.add(SecondSpell)
magicSlots.add(ThridSpell)
magicSlots.add(FourthSpell)

#Main Loop
while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            enemySpeed += 0.01
            enemySpawnSpeed = enemySpawnSpeed * 0.99
            new_enemy = Enemy(enemySpeed)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
        elif event.type == KEYUP:
            
            if event.key == K_LSHIFT and MagicOpen == False:
                MagicOpen = True
                cursor.start()
                print('shift menu')

            try:
                if event.key == K_LEFT and MagicOpen == True:
                    currentSpellX = currentSpellX - 1
                    cursor.moveLeft()
                    cursorMoveX += -10
                if event.key == K_RIGHT and MagicOpen == True:
                    currentSpellX = currentSpellX + 1
                    cursor.moveRight()
                    cursorMoveX += 10
                if event.key == K_UP and MagicOpen == True:
                    currentSpellY = currentSpellY + 1
                    cursor.moveUp()
                    cursorMoveY += -10
                if event.key == K_DOWN and MagicOpen == True:
                    currentSpellY = currentSpellY - 1
                    cursor.moveDown()
                    cursorMoveY += +10
            except:
                print('out of range'+str(currentSpellX))


    #Update player
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)       
    
    #Update projectiles
    
    
    if MagicOpen == False:
        currentSpellX = 0
        currentSpellY = 0
        if pressed_keys[K_UP]:
                playerLastLookDirection = (0,-1)
                
        if pressed_keys[K_DOWN]:
            playerLastLookDirection = (0,1)
                
        if pressed_keys[K_LEFT]:
            playerLastLookDirection = (-1,0)
                
        if pressed_keys[K_RIGHT]:
            playerLastLookDirection = (1,0)
    
    if MagicOpen == True:   
        if pressed_keys[K_SPACE] and currentSpellX == 1:
            new_projectile = Fireball1(playerLastLookDirection,buffs)
            fireballs.add(new_projectile)
            all_sprites.add(new_projectile)
            MagicOpen = False
            cursor.stop(cursorMoveX,cursorMoveY)
            cursorMoveY = 0
            cursorMoveX = 0
            currentSpellX = 0
        
        if pressed_keys[K_SPACE] and currentSpellX == -1:
            new_projectile = Earth1(buffs)
            earths.add(new_projectile)
            all_sprites.add(new_projectile)
            MagicOpen = False
            cursor.stop(cursorMoveX,cursorMoveY)
            cursorMoveY = 0
            cursorMoveX = 0
            currentSpellX = 0
        
        if pressed_keys[K_SPACE] and currentSpellY == 1:
            health += 10
            if health > maxHealth:
                health = maxHealth
            maxHealth += 2
            MagicOpen = False
            cursor.stop(cursorMoveX,cursorMoveY)
            cursorMoveY = 0
            cursorMoveX = 0
            currentSpellX = 0
        
        if pressed_keys[K_SPACE] and currentSpellY == -1:
            
            buffs += 3
            MagicOpen = False
            cursor.stop(cursorMoveX,cursorMoveY)
            cursorMoveY = 0
            cursorMoveX = 0
            currentSpellX = 0
   
    fireballs.update()
    earths.update()
    earthrings.update()

    # Update enemy position
    enemies.update()
    for entity in enemies:
        if(pygame.Rect.colliderect(player.rect, entity.rect)):
            entity.kill()
            if lose == False:
                health = health - 1
            if health <= 0:
                lose = True
                clockOn = False
        for bullet in fireballs:
            if(pygame.Rect.colliderect(bullet.rect, entity.rect)):
                entity.kill()
                kills = kills + 1
        for bullet in earthrings:
            if pygame.sprite.collide_circle((bullet),(entity)):
                entity.kill()
                kills = kills + 1
        if kills >= 500:
            win = True
            clockOn = False

    screen.fill((255,255,255))
    
    #Spawn everything
    for entity in enemies:
        screen.blit(entity.surf, entity.rect)
    for entity in fireballs:
        screen.blit(entity.surf, entity.rect)
    for entity in earths:
        screen.blit(entity.surf, entity.rect)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    for entity in magicSlots:
        screen.blit(entity.surf, entity.rect)
    screen.blit(cursor.surf,cursor.rect)

    HitsTextSurface = Text.render('Health =' + str(health),False,(0,0,0))
    screen.blit(HitsTextSurface,(ScreenWidth-150,0))
    
    KillsTestSurface = Text.render('Kills ='+ str(kills),False,(0,0,0))
    screen.blit(KillsTestSurface,(ScreenWidth-270,0))

    PowerTextSurface = Text.render('Power =' + str(buffs/3),False,(0,0,0))
    screen.blit(PowerTextSurface,(ScreenWidth/2-30,ScreenHeight/2+200))
    
    if clockOn == True:
        ClockTextSurface = Text.render('Time:'+str(round(pygame.time.get_ticks()/1000)),False,(0,0,0))
        screen.blit(ClockTextSurface,(10,0))
        finalTime = pygame.time.get_ticks()/1000
    if clockOn == False:  
        ClockTextSurface = Text.render('Time:'+str(finalTime),False,(0,0,0))
        screen.blit(ClockTextSurface,(ScreenWidth/2 - 30,ScreenHeight/2+50))

    if win == True:
        WinTextSurface = Text.render('You Win!',False,(0,0,0))
        screen.blit(WinTextSurface,(ScreenWidth/2 - 30,ScreenHeight/2 -30))
    elif lose == True:
        LoseTextSurface = Text.render('You Lose!',False,(0,0,0))
        screen.blit(LoseTextSurface,(ScreenWidth/2 - 30,ScreenHeight/2 -30))
    
    pygame.display.flip()

    #Update clock
    clock.tick(30)
pygame.quit() 

