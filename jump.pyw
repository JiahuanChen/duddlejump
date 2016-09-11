import pygame , random
pygame.init()

screen = pygame.display.set_mode((360, 480))

class Box(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("1.png")
        self.image = self.image.convert_alpha()
        self.rect=self.image.get_rect()
        self.rect_x=180
        self.rect_y=360
        self.dy= 0
        self.dx = 0
        self.state1 = 'godown'
        self.state2 = 'boxmove'
      
    def update(self,barlist):
        self.checkKeys()
        if self.state1 == 'godown':
            self.dy += 0.1
            for i in barlist:
                if i.rect.centery+6> self.rect.bottom > i.rect.centery-6 \
                   and self.rect.left < i.rect.right \
                   and self.rect.right > i.rect.left :
                    self.dy = -6
                    self.state1 = 'goup'
                    
        if self.state1 == 'goup':
            if self.state2 == 'boxmove':
                self.dy += 0.1
                if self.dy >= 0.1:
                    self.state1 = 'godown'
                if self.rect_y <= 150 and self.state2 == 'boxmove':
                    self.state2 = 'barmove'
                    for i in barlist:
                        i.dy = -self.dy
                    self.dy = 0
            if self.state2 == 'barmove':
                for i in barlist:
                    i.dy += -0.1
                if i.dy <= 0.1:
                    for i in barlist:
                        i.dy = 0
                    self.state1 = 'godown'
                    self.state2 = 'boxmove'
                               
        self.rect_y += self.dy
        self.rect_x += self.dx
        self.rect.center=(self.rect_x,self.rect_y)

    def checkKeys(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.dx > -4.5:
            self.dx += -0.1
        elif keys[pygame.K_LEFT] and self.dx <= -4.5:
            self.dx = -4.5
        elif keys[pygame.K_RIGHT] and self.dx < 4.5:
            self.dx += 0.1
        elif keys[pygame.K_RIGHT] and self.dx >= 4.5:
            self.dx = 4.5
        elif self.dx > 0.1 :
            self.dx += -0.1
        elif self.dx < -0.1:
            self.dx += 0.1
        elif -0.1<= self.dx <=0.1:
            self.dx = 0
        if self.rect_x > screen.get_width():
            self.rect_x = 0
        if self.rect_x < 0:
            self.rect_x = screen.get_width()
        if self.dx < -0.1:
            self.image=pygame.image.load("1.png")
        elif self.dx > 0.1:
            self.image=pygame.image.load("2.png")
            

class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load("bar.png")
        self.image = self.image.convert_alpha()
        self.rect=self.image.get_rect()
        self.dy = 0
        self.dx = 0
        

    def update(self,score):
        self.rect.centery += self.dy
        self.rect.centerx += self.dx 
        if self.rect.right > screen.get_width() or self.rect.left < 0:
            self.dx = -self.dx
        if self.rect.top > screen.get_height():
            self.reset(score)

                


    def reset(self,score):
        self.rect.top = -20
        self.rect.centerx =  random.randrange(40,320)
        if 100<= score < 200:
            self.dx = random.randrange(0,2)
        elif score >= 200:
            self.dx = random.randrange(0,4)
        if self.dx != 0:
            self.image= pygame.image.load("mbar.png")
            self.image = self.image.convert_alpha()
        else :
            self.image= pygame.image.load("bar.png")
            self.image = self.image.convert_alpha()


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)

    def update(self,bar):
        if bar.dy > 0 :
            self.score += bar.dy /10 
        self.text="%d" % self.score
        self.image = self.font.render(self.text,1,(255,255,0))
        self.rect=self.image.get_rect()

            
def game(n):
    pygame.display.set_caption("jump")
    background=pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    score = Scoreboard()
    
    box=Box()


    barlist = []
    for i in range(6):
        bar=Bar()
        barlist.append(bar)
        bar.rect.centerx = random.randrange(40,320)
        bar.rect.centery = (i+1)*60
    bar=Bar()
    bar.rect.centerx = 180
    bar.rect.centery = 460
    barlist.append(bar)

    scoreSprite=pygame.sprite.Group(score)
    barSprites=pygame.sprite.Group(barlist)
    boxSprites=pygame.sprite.Group(box)

    
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if box.rect.bottom >= 480:
            keepGoing = False
            
        boxSprites.clear(screen,background)
        barSprites.clear(screen,background)
        scoreSprite.clear(screen,background)
        boxSprites.update(barlist)
        barSprites.update(score.score)
        scoreSprite.update(bar)
        barSprites.draw(screen)
        boxSprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()

    scoreSprite.clear(screen,background)

    while n < 80 :
        clock.tick(90)
        barSprites.clear(screen,background)
        boxSprites.clear(screen,background)
        for i in barlist:
            i.rect.centery += -box.dy
        box.rect.centery += -2
        barSprites.draw(screen)
        boxSprites.draw(screen)
        
        pygame.display.flip()
        n=n+1

    box.dy = 0.1

    while n < 160 :
        clock.tick(90)
        boxSprites.clear(screen,background)
        box.rect.centery += box.dy
        box.dy += 0.08
        boxSprites.draw(screen)
        
        pygame.display.flip()
        n=n+1
        if box.rect.top > 480: quit

    infile = open('score.txt','r')
    rec = infile.readline()
    infile.close()
    outfile = open('score.txt','w')
    if score.score > eval(rec):
        outfile.write(str(int(score.score)))
    else:
        outfile.write(rec)    
    outfile.close()
     
    return score.score

def menu2(score):
    pygame.display.set_caption("jump")
    
    infile = open('score.txt','r')
    rec = infile.readline()
        
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    a = (
    "",
    "",
    "",
    "game over!",
    "your score: %d" % score ,
    "hightest record :" ,
    "%s"% rec,
    "",
    "play again",
    ""
    "quit",
    )

    infile.close()

    

    for line in a:
        tempLabel = insFont.render(line, 1, (255, 0, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if 50 < x <225 and 280 < y < 325: 
                    keepGoing = False
                    donePlaying = False
                elif 50 < x < 200 and 330 < y < 375 :
                    exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
    
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 35*i))
        pygame.display.flip()
    return donePlaying
    
        
def main():
    donePlaying = False
    FirstPlaying = True
    score = 0
    while not donePlaying:
        if FirstPlaying:
            n=0
            score = game(n)
            FirstPlaying = False
        donePlaying = menu2(score)
        if not donePlaying:
            n=0
            score = game(n)
    main()


if __name__ == "__main__":
    main()
