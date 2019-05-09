#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:42:14 2019

@author: julesdelemotte
"""

import math
import random
import time
import cmath as cm
from tkinter import *


"""Classe définissant le robot"""

# Choix des cartes et procédure pour l'utilisateur

choixProcedure=-1
choixCarte=-1        

def interaction ():
    global choixCarte, choixProcedure
    print("Bonjour, quelle carte voulez-vous tester pour la modélisation (entier de 1 à 8) ? Si besoin, reportez vous aux déscription des 8 cartes de test du rapport partie 3.")
    choixCarte=int(input())
    print("Bonjour, quelle procédure voulez-vous tester pour la modélisation ? Procédure de fonction du robot à l'aveugle (1) ou non (2). ")
    choixProcedure=int(input())
    print("La procédure est lancée !")
    print("Petit rappel des déplacements : les flèches haute et basse servent à avancer, les flèches droite et gauche servent aux rotations.")

interaction()

class Robot:
    
    def centre(self):
        return 1 / 3 * (self.x0 + self.x1 + self.x2), 1 / 3 * (self.y0 + self.y1 + self.y2)
    
    def __init__(self, canvas, x, y, width, height, turnspeed, speed):
        self._d = {'Up':-1, 'Down':1, 'Left':1, 'Right':-1}
        
        
        
        self.canvas=canvas
        self.width=width
        self.height=height
        self.turnspeed=turnspeed
        self.speed=speed
        self.length=5            # nombre de répétition de la boucle une fois déconnecté 
        self.x0=x
        self.y0=y
        self.last_lamp=-1

        
        self.vectdirecteur= -math.pi/2
        
        self.x1=self.x0 + self.width/2
        self.y1=self.y0 - self.height
        
        self.x2=self.x0 - self.width/2
        self.y2=self.y0-self.height
        
        self.x, self.y = self.centre()
        
        self.robot=self.canvas.create_polygon((self.x0, self.y0, self.x1, self.y1, self.x2, self.y2))
        
    def changeCoords(self) : 
        self.canvas.coords(self.robot,self.x0, self.y0, self.x1, self.y1, self.x2, self.y2)
    

    def _rot(self,x, y,t):
                x-=self.x
                y-=self.y
                _x = x * math.cos(t) + y * math.sin(t)
                _y = -x * math.sin(t) + y * math.cos(t)
                return _x + self.x, _y + self.y

    def testConnection(self,canvas,Lampdaires):
        x0=self.x
        y0=self.y
        for i in range(len(Lampdaires)):
            x1=(canvas.coords(Lampdaires[i])[0]+canvas.coords(Lampdaires[i])[2])/2
            y1=(canvas.coords(Lampdaires[i])[1]+canvas.coords(Lampdaires[i])[3])/2
            if distEuclidian(x0,y0,x1,y1)<rLampadaire/2:
                a=canvas.create_rectangle(x0-5, y0-5, x0+5, y0+5,fill="yellow") 
                self.last_lamp=i
                return True;
        self.chemin(self.canvas)
        return False;
    
    def chemin (self,canvas):
        global Distance
        x0=self.x
        y0=self.y
        a=canvas.create_rectangle(x0-2, y0-2, x0+2, y0+2,fill="red")
        Distance+=self.speed 
    
    
    def rotate(self, event=None):
        if self.testConnection(self.canvas,Lampadaires):
            t = self._d[event.keysym] * self.turnspeed * math.pi / 180 
            self.vectdirecteur -= t
        
            self.x0, self.y0 = self._rot(self.x0, self.y0,t)
            self.x1, self.y1 = self._rot(self.x1,self.y1,t)
            self.x2, self.y2 = self._rot(self.x2, self.y2,t)
        
            self.x, self.y = self.centre()
        
            self.changeCoords()
        
    
    
    def left_turn_90(self):
        t=10*math.pi/180
        for i in range (9):
            self.vectdirecteur -=t
            self.x0, self.y0 = self._rot(self.x0, self.y0,t)
            self.x1, self.y1 = self._rot(self.x1,self.y1,t)
            self.x2, self.y2 = self._rot(self.x2, self.y2,t)
        
            self.x, self.y = self.centre()
        
            self.changeCoords()
            
    
        
    def right_turn_90(self):
        t=-10*math.pi/180
        for i in range (9):
            self.vectdirecteur -=t
            self.x0, self.y0 = self._rot(self.x0, self.y0,t)
            self.x1, self.y1 = self._rot(self.x1,self.y1,t)
            self.x2, self.y2 = self._rot(self.x2, self.y2,t)
        
            self.x, self.y = self.centre()
        
            self.changeCoords()
    
    def disconnect_move_straight(self,j):
        for i in range(self.length+j):
            if testColision(self,self.canvas):
                if not self.testConnection(self.canvas,Lampadaires):
                    
                    s=-(self.speed)
                    self.x0 += s * math.cos(self.vectdirecteur)
                    self.x1 += s * math.cos(self.vectdirecteur)
                    self.x2 += s * math.cos(self.vectdirecteur)
        
                    self.y0 += s * math.sin(self.vectdirecteur)
                    self.y1 += s * math.sin(self.vectdirecteur)
                    self.y2 += s * math.sin(self.vectdirecteur)
            
                    self.x, self.y = self.centre()
            
            
                    self.changeCoords()
                
    
                
    
        
    def move(self, event=None):
        if testColision(self,self.canvas):
            if self.testConnection(self.canvas,Lampadaires):
            
                s = self.speed * self._d[event.keysym]
            
                self.x0 += s * math.cos(self.vectdirecteur)
                self.x1 += s * math.cos(self.vectdirecteur)
                self.x2 += s * math.cos(self.vectdirecteur)
        
                self.y0 += s * math.sin(self.vectdirecteur)
                self.y1 += s * math.sin(self.vectdirecteur)
                self.y2 += s * math.sin(self.vectdirecteur)
            
                self.x, self.y = self.centre()
            
            
                self.changeCoords()
                
            else :
                self.procedure(choixProcedure)
                
                
                
     # Fonction outils d'interface avec l'utilisateur pour choisir le mode du robot    
    
    def procedure(self,i):
        switcher = {
            1: self.automatique,
            2: self.procédure_automatique_2,
            
        }
        func = switcher.get(i, lambda: "Invalid syntaxe")
        func()
    
    # Procédure 1 : aveugle
    
    def automatique(self):
        i=0
        while(not self.testConnection(self.canvas,Lampadaires)) : 
            #for i in range (20): 
            self.disconnect_move_straight(i)
            self.left_turn_90()
            i+=1
        
    
    # Procédure 2 : connaissant la carte 

    def procédure_automatique_2(self):

        coord_robot=[self.x,self.y]


        closest=self.closest(Centre,coord_robot,self.last_lamp)
        self.last_lamp=closest
        
        theta=10
        while theta*180/math.pi>=2 or theta*180/math.pi<=-2 :
            theta=self.calcule_angle(Centre[closest],coord_robot,self.vectdirecteur)
            self.rotate_given_angle(1)


        while(not self.testConnection(self.canvas,Lampadaires)) :
        
            self.disconnect_move_straight(0)


    # Distance 
    
    def dist(self, c1, c2):
        return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)


    #Fonction qui donne l'indice du point le plus proche dans une liste de coordonnées, 
    #mais sans donner l'indice du lampadaire qu'il vient de quitter
        

    def closest(self,liste_coords,coord_robot,last_lamp):
        m=MAX 
        indice=-1
        n = len(liste_coords)
        if n==1:
            return 0


        for i in range (n):
            if self.dist(coord_robot, liste_coords[i])<m and i!=last_lamp:
                m=self.dist(coord_robot, liste_coords[i])
                indice=i
        
        return indice

     #Fonction qui calcule l'angle avec formé avec le centre du lampadaire le plus proche

    def calcule_angle(self,coord_luminaire, coord_robot,vecteur_directeur):
        t=complex(math.cos(vecteur_directeur),math.sin(vecteur_directeur))
        #z=math.exp(t)
        vecteur_algebrique=[-coord_luminaire[0]+coord_robot[0],-coord_luminaire[1]+coord_robot[1]]
        rapport=complex(vecteur_algebrique[0],vecteur_algebrique[1])#/z
        return cm.phase(rapport)-cm.phase(t)

    #theta est l'angle dont on doit "rotationner" le robot

    def rotate_given_angle(self,theta):
        t=theta*math.pi/180
        self.vectdirecteur -=t
        self.x0, self.y0 = self._rot(self.x0, self.y0,t)
        self.x1, self.y1 = self._rot(self.x1,self.y1,t)
        self.x2, self.y2 = self._rot(self.x2, self.y2,t)
        
        self.x, self.y = self.centre()
        
        self.changeCoords()


      
"""Classe définissant la MAP"""
MAX=10000000000
Distance=0 #Permet de mesurer la distance par l'algorithme 

class Plan:
    def __init__(self, gameWidth, gameHeight):
        self.root = Tk()
        self.root.title("Simulation TurtleBot")
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.gameWindow()
        
        
        self.robot = Robot(self.canvas, x= random.randint(0,self.gameWidth),y= random.randint(0,self.gameHeight), width=15, height=50, turnspeed=10, speed=10)
        #self.robot = Robot(self.canvas, x= self.gameWidth/2 ,y= self.gameHeight/2 , width=15, height=50, turnspeed=10, speed=10)
        self.root.bind('<Left>', self.robot.rotate)
        self.root.bind('<Right>', self.robot.rotate)
        self.root.bind('<Up>', self.robot.move)
        self.root.bind('<Down>', self.robot.move)

        self.root.mainloop()

    def gameWindow(self):
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=YES)

        self.canvas = Canvas(self.frame,width=self.gameWidth, height=self.gameHeight, bg="white", takefocus=1)
        
        
        self.canvas.pack(fill=BOTH, expand=YES) 
        
        
        """Fonctions générant différentes cartes"""
        self.cartes(choixCarte)
        #creat(self.canvas,dObstacle, rLampadaire,O,L)
        #gener(4,self.canvas,Lampadaires,rLampadaire,"blue","oval")
        #gener(4,self.canvas,Obstacles,dObstacle,"black","rectangle") 
        
        
        """Regarder comment associer la création d'obstacles et lampadaires """
        #self.canvas.bind("<Button-1>", self.creatLampadaire)
        #self.canvas.pack(padx =5, pady =5)
        #self.canvas.bind("<space>", self.creatObstacle)
        #self.canvas.pack(padx =5, pady =5)
        
        """Implémentation des centres"""
        self.centre(Lampadaires,self.canvas)
        
        """Création des bordures"""
        self.bordures()
        
        
        
# Fonction de choix de position des lampadaires et obstacles à la main 

    def creatLampadaire(self,event):
        global Lampadaires
        X = event.x
        Y = event.y
        r = rLampadaire/2
        a=self.canvas.create_oval(X-r, Y-r, X+r, Y+r, outline="black",fill="blue")
        Lampadaires+=[a]
    
    def creatObstacle(self,event):
        global Obstacles
        X = event.x
        Y = event.y
        r = dObstacle
        a=self.canvas.create_rectangle(X-r, Y-r, X+r, Y+r,fill="black")
        Obstacles+=[a]
        
# Définition des cartes à la main 

    def cartes(self,i):
        switcher = {
            1: self.carte1,
            2: self.carte2,
            3: self.carte3,
            4: self.carte4,
            5: self.carte5,
            6: self.carte6,
            7: self.carte7,
            8: self.carte8
        }
        func = switcher.get(i, lambda: "Invalid month")
        func()

#Carte avec 2 lampadaires 

    def carte1(self):
        global Lampadaires
        a=self.canvas.create_oval(20, 20, 20+rLampadaire, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(100+rLampadaire, 20, 100+2*rLampadaire, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
 
#Carte avec 2 lampadaires et un obstacle entre les 2
       
    def carte2(self):
        global Lampadaires, Obstacles
        a=self.canvas.create_oval(20, 20, 20+rLampadaire, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(20+rLampadaire+4*dObstacle, 20, 20+2*rLampadaire+4*dObstacle, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_rectangle(20+rLampadaire+1*dObstacle, 20+rLampadaire/2-dObstacle,
                                       20+rLampadaire+3*dObstacle, 20+rLampadaire/2+dObstacle,fill="green")
        Obstacles+=[a]
  
#Carte avec 3 lampadaires non équidisatnts
      
    def carte3(self):
        global Lampadaires, Obstacles
        a=self.canvas.create_oval(20, 20, 20+rLampadaire, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(20+rLampadaire+4*dObstacle, 20, 20+2*rLampadaire+4*dObstacle, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(20+rLampadaire+2*dObstacle, 20+rLampadaire+dObstacle, 20+2*rLampadaire+2*dObstacle, 20+2*rLampadaire+dObstacle, outline="black",fill="blue")
        Lampadaires+=[a]
    
#Carte avec 3 lampadaires non équidistants et un obstacle au milieu 
    
    def carte4(self):
        global Lampadaires, Obstacles
        a=self.canvas.create_oval(20, 20, 20+rLampadaire, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(20+rLampadaire+4*dObstacle, 20, 20+2*rLampadaire+4*dObstacle, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(20+rLampadaire+2*dObstacle, 20+rLampadaire+dObstacle, 20+2*rLampadaire+2*dObstacle, 20+2*rLampadaire+dObstacle, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_rectangle(20+rLampadaire, 20+rLampadaire-dObstacle, 20+rLampadaire+2*dObstacle, 20+rLampadaire+dObstacle,fill="green")
        Obstacles+=[a]
   
#Carte avec 3 lampadaires non équidistants et 2 obstacles au milieu de 2 hemins entre lampadaires
     
    def carte5(self):
        global Lampadaires, Obstacles
        a=self.canvas.create_oval(20, 20, 20+rLampadaire, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(20+rLampadaire+4*dObstacle, 20, 20+2*rLampadaire+4*dObstacle, 20+rLampadaire, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_oval(20+rLampadaire+2*dObstacle, 20+rLampadaire+dObstacle, 20+2*rLampadaire+2*dObstacle, 20+2*rLampadaire+dObstacle, outline="black",fill="blue")
        Lampadaires+=[a]
        a=self.canvas.create_rectangle(20+rLampadaire, 20+rLampadaire-dObstacle, 20+rLampadaire+2*dObstacle, 20+rLampadaire+dObstacle,fill="green")
        Obstacles+=[a]
        a=self.canvas.create_rectangle(40+rLampadaire, rLampadaire-4*dObstacle, 40+rLampadaire+2*dObstacle,rLampadaire-2*dObstacle,fill="green")
        Obstacles+=[a]
      
#Carte mod&lisant un maillage de lampdaire de l'espace avec distance entre les lampadaires grandes pour le robot avec recherche de lampaires naivement   
        
    def carte6(self):
        global Lampadaires, Obstacles
        n=int(modelWidth/rLampadaire)
        for i in range (n):
            for j in range (n):
                if i%2==0:
                    a=self.canvas.create_oval(20 +rLampadaire*(i*1.1), 20+rLampadaire*(j*1.1), 20 +rLampadaire*(1+i*1.1), 20+rLampadaire*(1+j*1.1), outline="black",fill="blue")
                    Lampadaires+=[a]
                else :
                    a=self.canvas.create_oval(20 +rLampadaire*(i*1.1), 20+rLampadaire*(j*1.1-0.5), 20 +rLampadaire*(1+i*1.1), 20+rLampadaire*(1+j*1.1-0.5), outline="black",fill="blue")
                    Lampadaires+=[a]
  
#Carte mod&lisant un maillage de lampdaire de l'espace  plus proche que 6 (le robot peut changer de zone facilement)
                  
    def carte7(self):
        global Lampadaires, Obstacles
        n=int(modelWidth/rLampadaire)+1
        for i in range (n):
            for j in range (n):
                if i%2==0:
                    a=self.canvas.create_oval(20 +rLampadaire*(i*0.9), 20+rLampadaire*(j*1.1), 20 +rLampadaire*(1+i*0.9), 20+rLampadaire*(1+j*1.1), outline="black",fill="blue")
                    Lampadaires+=[a]
                else :
                    a=self.canvas.create_oval(20 +rLampadaire*(i*0.9), 20+rLampadaire*(j*1.1-0.55), 20 +rLampadaire*(1+i*0.9), 20+rLampadaire*(1+j*1.1-0.55), outline="black",fill="blue")
                    Lampadaires+=[a]
                    
                    
#Carte mod&lisant un maillage de lampdaire de l'espace  avec obstacles de manières régulièrement disposée                    
                    
    def carte8(self):
        global Lampadaires, Obstacles
        n=int(modelWidth/rLampadaire)+1
        for i in range (n):
            for j in range (n):
                if i%2==0:
                    a=self.canvas.create_oval(20 +rLampadaire*(i*0.9), 20+rLampadaire*(j*1.1), 20 +rLampadaire*(1+i*0.9), 20+rLampadaire*(1+j*1.1), outline="black",fill="blue")
                    Lampadaires+=[a]
                    a=self.canvas.create_rectangle(20 +rLampadaire*(i*0.9), 20+rLampadaire*(j*1.1), 20 +rLampadaire*(i*0.9)+2*dObstacle, 20+rLampadaire*(j*1.1)+2*dObstacle,fill="green")
                    Obstacles+=[a]
                    #a=self.canvas.create_rectangle(20 +rLampadaire*(1+i*0.9)-2*dObstacle, 20+rLampadaire*(1+j*1.1)-2*dObstacle, 20 +rLampadaire*(1+i*0.9), 20+rLampadaire*(1+j*1.1),fill="green")
                    #Obstacles+=[a]
                    
                else :
                    a=self.canvas.create_oval(20 +rLampadaire*(i*0.9), 20+rLampadaire*(j*1.1-0.55), 20 +rLampadaire*(1+i*0.9), 20+rLampadaire*(1+j*1.1-0.55), outline="black",fill="blue")
                    Lampadaires+=[a]
                    a=self.canvas.create_rectangle(20 +rLampadaire*(i*0.9), 20+rLampadaire*(j*1.1-0.55), 20 +rLampadaire*(i*0.9)+2*dObstacle, 20+rLampadaire*(j*1.1-0.55)+2*dObstacle,fill="green")
                    Obstacles+=[a]
                    #a=self.canvas.create_rectangle(20 +rLampadaire*(1+i*0.9)-2*dObstacle, 20+rLampadaire*(1+j*1.1)-2*dObstacle, 20 +rLampadaire*(1+i*0.9), 20+rLampadaire*(1+j*1.1),fill="green")
                    #Obstacles+=[a]
                    
# Création des bordures
    
    def bordures(self):
        a=self.canvas.create_rectangle(0, 0, 5,modelHeight,fill="black")
        a=self.canvas.create_rectangle(0, 0, modelWidth,5,fill="black")
        a=self.canvas.create_rectangle(modelWidth-5,0, modelWidth,modelHeight,fill="black")
        a=self.canvas.create_rectangle(0,modelHeight-5, modelWidth,modelHeight,fill="black")
        
# Fonction qui crée implemente la liste des centre
       
    def centre(self,Lampadaire, canvas):
        global Centre
        n=len(Lampadaire)
        for i in range(n):
                x1=(canvas.coords(Lampadaires[i])[0]+canvas.coords(Lampadaires[i])[2])/2
                y1=(canvas.coords(Lampadaires[i])[1]+canvas.coords(Lampadaires[i])[3])/2       
                Centre+=[[x1,y1]]        
                     
 
# Variable globale du plan 

modelWidth=1000
modelHeight=1000


Lampadaires=[]               #Liste des lampdaires pour faire faicliement les tests : type ovale mais circulaire 
Obstacles=[]                 #Liste des obstacle pour faire faicliement les tests : type rectangulaire
Chemin=[]                    #Liste pour reperer les points rouges de connexion 
Centre=[]                    #Liste des centre des Lampadaires

# Arret du robot si rencontre d'un obstacle : retourne un booleen

def testColision(element, canvas):
    block=0.2
    
    if ((element.y+element.speed>modelHeight-block*5) and (math.sin(element.vectdirecteur)<0)) or ((element.y+element.speed<block*5) and (math.sin(element.vectdirecteur)>0)): 
        return False
        
    if ((element.x+element.speed>modelWidth-block*5) and (math.cos(element.vectdirecteur)<0)) or ((element.x+element.speed<block*5) and (math.cos(element.vectdirecteur)>0)):
        return False
        
        
    x0=element.x
    y0=element.y
    
    for i in range(len(Obstacles)):
        x1=canvas.coords(Obstacles[i])[0]
        y1=canvas.coords(Obstacles[i])[1]
        x2=canvas.coords(Obstacles[i])[2]
        y2=canvas.coords(Obstacles[i])[3]
        h=max(y1,y2)+block*5
        b=min(y1,y2)-block*5
        d=max(x1,x2)+block*5
        g=min(x1,x2)-block*5
        
        
        if (g<=x0 and x0<=d) and ((y0<b and y0+element.speed>=b and (math.sin(element.vectdirecteur)<0))
                                or (y0>h and y0-element.speed<h and math.sin(element.vectdirecteur)>0)):
            return False
        if (b<=y0 and y0<=h) and ((x0<g and x0+element.speed>=g and (math.cos(element.vectdirecteur)<0)) 
                                or (x0>d and x0-element.speed<d and math.cos(element.vectdirecteur)>0)):
            return False  
        
    return True
        
 
  
    
# Outils 
def distEuclidian(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)
    

# Création des obstacles et des lampadaires 

rLampadaire=300
nombreL=2
dObstacle=50
nombreO=2

def gener(nombre, canvas, Liste, dType, couleur, typ):
    for i in range(nombre):
        x=random.randint(0,modelWidth)
        y=random.randint(0,modelHeight)
        if typ=="rectangle":
            a=canvas.create_rectangle(x-dType, y-dType, x+dType, y+dType,fill=couleur)
        else :
            a=canvas.create_oval(x, y, x+dType, y+dType,fill=couleur)
        Liste+=[a]
        

# Fonction de lancement 

planrobot = Plan(modelWidth,modelHeight)










    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    