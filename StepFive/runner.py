import pygame, sys, random

class Game:
    def __init__(self):
        pygame.init() #start pygame
        
        self.screen = pygame.display.set_mode((500, 250))
        self.clock = pygame.Clock()
        
        self.ground = pygame.Surface((500, 50))
        self.ground.fill((200, 200, 200))
        
        self.player = Player()
        self.spawner = Spawner()
        
        self.jumpCoolDown = 60
        self.jumpCounter = 0
        
        self.spawningInterval = 120
        self.spawningCounter = 0
        
        self.exitInterval = 60
        self.exitCounter = 0
        self.exiting = False
        
        self.spawningPos = [500, 175]
        
    def run(self): #the tutorial will be on implementing game logic which will all be done here
        while True:
            self.screen.fill((0,0,0))
            
            self.screen.blit(self.ground, (0, 200))
            
            self.player.update()
            if not self.exiting:
                self.spawner.update()
            self.player.render(self.screen)
            self.spawner.render(self.screen)
            
            #insert spawning logic here
            self.spawningCounter += 1
            if self.spawningCounter > self.spawningInterval + random.choice((-30, 30)):
                self.spawner.add(self.spawningPos.copy())
                self.spawningCounter = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.exiting:
                        self.player.jump()
        
            pygame.display.update()
            self.clock.tick(60)

class Spawner:
    def __init__(self):
        self.pos = []
        self.img = pygame.Surface((24, 25))
        pygame.draw.polygon(self.img, 'red', [(0, 25), (12, 0), (24, 25)])
        self.img.set_colorkey((0,0,0))
        
        self.speed = 2
    
    def get_rect(self, pos):
        return pygame.Rect(pos[0], pos[1], 24, 25)
    
    def add(self, pos):
        self.pos.append(pos)
    
    def update(self):
        remove_pos = []
        for i in range(len(self.pos)):
            self.pos[i][0] -= self.speed
            if self.pos[i][0] < -32:
                remove_pos.append(i)
        
        for i in remove_pos:
            self.pos.pop(i)
    
    def render(self, surf):
         for i in range(len(self.pos)):
             surf.blit(self.img, self.pos[i])

class Player:
    def __init__(self):
        self.img = pygame.Surface((32, 32))
        self.img.fill((250, 250, 250))
        self.pos = [50, 200 - 32]
        self.velocity = 0
    
    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 32, 32)
        
    def jump(self):
        if self.jumps == 1:
            self.velocity = -8
            self.jumps-=1
    
    def update(self):
        self.pos[1] += self.velocity
        
        if self.pos[1] >= (200 - 32):
            self.pos[1] = (200 - 32)
            self.jumps = 1
        
        self.velocity = min(self.velocity + 0.3, 4)
    
    def render(self, surf):
        surf.blit(self.img, self.pos)
        
Game().run()