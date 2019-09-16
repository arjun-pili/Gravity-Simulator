gme = 1
import pygame,sys
import random
import pygame.mixer
import time
import math
from math import atan
from collections import defaultdict
def bound(n,mymin,mymax):#defining this fuction to bound the values to be appropriate to be displayed
    if n<mymin:return mymin
    elif n>mymax:return mymax
    return n
pygame.init()
coll_sound = pygame.mixer.Sound('collide.wav')#sound when planets collide
def size(mass):
    if 0<mass<100:return  5,(0,255,0)
    if 100<=mass<1000:return  10,(0,0,255)
    if 1000<=mass<10000:return  15,(255,0,0)
    if 10000<=mass:return  20,(255,255,255)

class vector:#defining a class vector
    def __init__(self,(x1,y1),(x2,y2)):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x =self.x2 - self.x1
        self.y =self.y2 - self.y1
    @property
    def dir(self):
        if self.x2 == self.x1:
            return math.pi/2
        return atan(float(self.y1-self.y2)/(self.x2-self.x1))
    @property
    def mag(self):
        return math.sqrt((self.x2-self.x1)**2+(self.y2-self.y1)**2)
    def normalize(self):
        return [[self.x1/float(self.mag),self.y1/float(self.mag)],[self.x2/float(self.mag),self.y2/float(self.mag)]]
    def components(self):
        return [self.x,self.y]
    def multiply(self,n):
        return vector((n*self.x1,n*self.y1),(n*self.x2,n*self.y2))
    def unit(self):#return unit vector in same direction
        return vector(self.normalize()[0],self.normalize()[1])
class body:#defining a class body
    def __init__(self,index,mass,vel,state,netforce=[]):
        self.state = state#position of the body
        self.index = index#planet Number
        self.mass = mass#mass of the body
        self.vel = vel# net velocity of th body
        self.path = []#path of the planet
        self.netforce = netforce#net force on the body
        if 0<self.mass<100:
            self.radius= 5
            self.color = (0,255,0)#green
        if 100<=mass<1000:
            self.radius= 10
            self.color = (0,0,255)#blue
        if 1000<=mass<10000:
            self.radius= 15
            self.color = (255,0,0)#red
        if 10000<=self.mass:
            self.radius= 20
            self.color = (255,255,255)#white
def mousedrag(ipos):#to give velocity to th planet
        return (vector(ipos,list(pygame.mouse.get_pos())).components()[0]/40,vector(ipos,list(pygame.mouse.get_pos())).components()[1]/40)
def buttonpress() :
        if( event.type == pygame.MOUSEBUTTONDOWN ):
            x,y = event.pos
            if( x>0 and x<55 and y>game_height/8 + (7*game_height/160) and y<game_height/8 + (7*game_height/160)+7*game_height/40 ):
                return(10,5,(0,255,0))
            if( x>0 and x<55 and y>game_height/8 + 2*(7*game_height/160)+7*game_height/40 and y<game_height/8 + 2*(7*game_height/160)+7*game_height/40+7*game_height/40 ):
                return(100,10,(0,0,255))
            if( x>0 and x<55 and y>game_height/8 + 3*(7*game_height/160)+2*7*game_height/40 and y<game_height/8 + 3*(7*game_height/160)+2*7*game_height/40+7*game_height/40 ):
                return(1000,15,(255,0,0))
            if( x>0 and x<55 and y>game_height/8 + 4*(7*game_height/160)+3*7*game_height/40 and y<game_height/8 + 4*(7*game_height/160)+3*7*game_height/40+7*game_height/40 ):
                return(10000,20,(255,255,255))
            return 0
        return 0

while(gme):
    FORCEMAX = 1000#max force used inside bound function
    MAXVEL = 40#max velocity used inside bound function
    G = 1#GRAVITATIONAL CONSTANT
    END = 0#EXIT condition
    tym = pygame.time.Clock()
    planets = defaultdict()#default dict for storing instances of body class
    netfrc = {}#dictionary to store net force on each planet ehere planet(instance of the body) is the key
    netvel = defaultdict(list)
    index = 0#index to keep count of number of planets
    game_width = 1800
    game_height = 1000
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    red = (255,0,0)
    yellow = (255,255,0)
    peach = (255,218,185)
    black = (0,0,0)
    purple = (178,102,255)
    dark = (127,0,255)
    color = red
    gameDisplay = pygame.display.set_mode((game_width , game_height))
    pygame.display.set_caption("GRAVITY SIMULATOR")
    image=pygame.image.load('help.jpeg')
    #the func below is to display the choices of selecting size of the planets
    def draw_rect( x , y, w,h,msg,angle):
        mouse = pygame.mouse.get_pos()
        if not(( x+w > mouse[0] > x) and (y+h > mouse[1] > y)):
            pygame.draw.rect( gameDisplay , black , (x,y,w,h))
            pygame.draw.rect(gameDisplay , white, (x,y,w,h))
        def text_objects(text, color):
            textSurface = smallText.render(text, True, black)
            return textSurface, textSurface.get_rect()

        smallText = pygame.font.Font("freesansbold.ttf",15)
        textSurf, textRect =text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        textSurf = pygame.transform.rotate(textSurf,angle)
        gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    #the below func is to calculate the net force on ith planet
    def net(ith):
        X = 0
        Y = 0
        for k in forces[ith]:
            X += k.components()[0]
            Y += k.components()[1]
        return bound(10*X/planets[ith].mass,-1*FORCEMAX,FORCEMAX),bound(10*Y/planets[ith].mass,-1*FORCEMAX,FORCEMAX)
    global temp0
    temp0 = []
    #the below are the default values of the planet
    m = 100
    ra = 10
    c = (0,0,255)
    while not END:
        myfont = pygame.font.SysFont("monospace", 16)
        label = myfont.render("F1 -->> help", 1, (255,255,255))
        gameDisplay.blit(label, (game_width-130 , 22))
        draw_rect(0,0,55,game_height/8,"size",90 )
        draw_rect(0,game_height/8 + (7*game_height/160),55,+7*game_height/40,"small",90 )
        draw_rect(0,game_height/8 + 2*(7*game_height/160)+7*game_height/40 ,55,7*game_height/40,"medium",90 )
        draw_rect(0,game_height/8 + 3*(7*game_height/160)+2*7*game_height/40,55,7*game_height/40,"large",90 )
        draw_rect(0,game_height/8 + 4*(7*game_height/160)+3*7*game_height/40,55,7*game_height/40,"huge",90 )
        draw_rect(game_width-200,game_height-80 ,100,40,"clear",0 )

        r = defaultdict(list)# a dict used as a 2-D array whare ijth elemwnt gives position vector pointing from ith planet to jth planet
        forces = defaultdict(list)#similar functionaity as r but stores forces
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END = 1
                gme = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonpress():m,ra,c=buttonpress()#selected size
                x,y = event.pos
                if( x> 55 and x < game_width and y>0 and y< game_height):#mouse any where other than the boxes of choices
                    if pygame.mouse.get_pressed()[0]:

                        temp0 +=[list(pygame.mouse.get_pos())]#list to hold the planets position wrt to index
                        #---->>>FROM ONE SELECTED POS YOU CAN LAUNCH ONLY ONE PLANET<<<----
                        index+=1
                if  index!=0 and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:#right click to relase (create with given magnitude) planet
                        planets[index-1] = body(index-1,m,[bound(mousedrag(temp0[index-1])[0],-1*MAXVEL,MAXVEL),bound(mousedrag(temp0[index-1])[1],-1*MAXVEL,MAXVEL)],list(temp0[index-1]))#vel given is bounded
        if pygame.key.get_pressed()[282]:#if F1 is pressed display help image
            gameDisplay.blit(image,(1920/3,0))
        if len(temp0)>=1:
            pygame.draw.line(gameDisplay,(255,255,0),temp0[index-1],pygame.mouse.get_pos(),1)#display line from planets pos to mouse pos

            pygame.draw.circle(gameDisplay,c,temp0[index-1],ra)
        temp = 0
        for i in planets:
            planets[temp] = planets.pop(i)#recreating dictionary as when planets collide one of the planet is deleted
            temp+=1
        for i in planets:
            for j in planets:
                r[i] += [vector(planets[i].state,planets[j].state)]
                if r[i][j].mag != 0: forces[i] += [r[i][j].unit().multiply(G*planets[i].mass*planets[j].mass/float((r[i][j].mag)**2))]
                else:forces[i]+=[vector((0,0),(0,0))]
        tmp =[]# alist to store the collided PLANETS
        for i in planets:
            for g in planets:
                if 0<=r[i][g].mag <=planets[i].radius+planets[g].radius and g!=i:
                    print "collided"
                    tmp .append(g)
                    pygame.mixer.Sound.play(coll_sound)
                    #INELASTIC COLLISION
                    planets[i].vel = planets[g].vel = [(planets[i].mass*planets[i].vel[0]+planets[g].mass*planets[g].vel[0])/(planets[i].mass+planets[g].mass),(planets[i].mass*planets[i].vel[1]+planets[g].mass*planets[g].vel[1])/(planets[i].mass+planets[g].mass)]
                    planets[i].mass+=planets[g].mass
                    planets[i].radius,planets[i].color = size(planets[i].mass)
        if len(planets) and len(tmp) >=2:
            del planets[tmp[0]]#AS YOU CANNOT DELETE ITEMS FROM A DICT WHILE ITERATING
            continue
        myfont = pygame.font.SysFont("monospace", 16)
        label = myfont.render("Number of planets : " + str(len(planets)) , 1, (255,255,255))#displaying nuber of planets
        gameDisplay.blit(label, (game_width-250 , game_height - 30 ))
        for xyz in planets:
            pygame.draw.circle(gameDisplay,planets[xyz].color,(int(planets[xyz].state[0]),int(planets[xyz].state[1])),planets[xyz].radius)
	    for abc in range(1,len(planets[xyz].path)):
              pygame.draw.aaline(gameDisplay,planets[xyz].color,(int(planets[xyz].path[abc-1][0]),int(planets[xyz].path[abc-1][1])),(int(planets[xyz].path[abc][0]),int(planets[xyz].path[abc][1])))#drawing lines from points to keep track of path
        i = 0
        for i in planets:
            planets[i].netforce = (net(i))
            #incrementing velocity
            planets[i].vel[0] +=bound(planets[i].netforce[0],-100,400) #bounding net force
            planets[i].vel[1] += bound(planets[i].netforce[1],-100,400)
            #incrementing position
            planets[i].state[0] += bound(planets[i].vel[0],-30,30)#bounding net velocity
            planets[i].state[1] += bound(planets[i].vel[1],-30,30)
            planets[i].state[0]= bound(planets[i].state[0],-2000,2000)#bounding position
            planets[i].state[1]= bound(planets[i].state[1],-2000,2000)
	    planets[i].path.append((planets[i].state[0],planets[i].state[1]))#keeping track of path
        pygame.display.update()
        gameDisplay.fill((0,0,0))#filling screen
        a,b = pygame.mouse.get_pos()
        #print pygame.mouse.get_pressed()[0],a,b
        if  pygame.mouse.get_pressed()[0] and game_width-200<a<game_width-100 and game_height-80<b<game_height:
            break
        tym.tick(60)#frame rate
