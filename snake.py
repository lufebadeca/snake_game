#!/usr/bin&env python3
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

class PiSerpiente:
    def __init__(self, screen):
        self.pantalla = screen

        self.serpiente = [[10,10],[10,9],[10,8],[10,7]]     #2D list for snake body
        self.comida = [5,20]                            #first food location
        
        self.puntuacion = 0
        self.cabeza= 'Ö'
        self.cuerpo = 'o'
        self.velocidad = 100
        
        self.direcciones =  ( ord('a'), ord('w'), ord('s'), ord('d') )
        #(KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN)
        self.tecla = ord('d')
        self.cerrar = ( ord('c'), ord('C') )
        
        curses.curs_set(0)              #disables cursor flickering
        self.pintar_ventana()

    def mostrar_puntuacion(self, puntuacion, closed):
        self.pantalla.clear()
        if closed:
            fin = 'Usted cerró el juego. Su puntuación: {s} puntos(s)'.format(s=puntuacion)
        else:
            fin = 'Perdió. Su puntuación: {s} puntos(s)'.format(s=puntuacion)
        self.pantalla.addstr(self.pantalla_altura // 2, self.pantalla_anchura // 2 - len(fin) // 2, fin)
        self.pantalla.refresh()
        self.pantalla.getch()
        
    def pintar_ventana(self):
        self.pantalla_altura, self.pantalla_anchura = self.pantalla.getmaxyx()
        self.ventana_juego_altura = 30
        self.ventana_juego_anchura = 80
        
        self.ventana_serpiente = curses.newwin(self.ventana_juego_altura, self.ventana_juego_anchura, self.pantalla_altura // 2 - self.ventana_juego_altura // 2, self.pantalla_anchura // 2 - self.ventana_juego_anchura // 2  )
        
        self.ventana_serpiente.box()
        self.ventana_serpiente.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.pantalla.refresh()
        
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        
        if curses.has_colors():
            self.ventana_serpiente.attrset(curses.color_pair(1))
        self.ventana_serpiente.addch(self.comida[0], self.comida[1], '✱')
        
        while True:                         #while loop to control the flow of the game
            if curses.has_colors():
                self.ventana_serpiente.attrset(curses.color_pair(3))
            bandera = '[ {t} - Puntuación:{s} ]'.format(t=self.__class__.__name__, s=self.puntuacion)
            self.ventana_serpiente.addstr(0, 2, bandera)
            
            self.ventana_serpiente.timeout(self.velocidad)
            
            teclaActual = self.ventana_serpiente.getch()
            if teclaActual in self.direcciones + self.cerrar:
                if teclaActual == ord('w') and self.tecla!=ord('s'): self.tecla = teclaActual
                if teclaActual == ord('s') and self.tecla!=ord('w'): self.tecla = teclaActual
                if teclaActual == ord('a') and self.tecla!=ord('d'): self.tecla = teclaActual
                if teclaActual == ord('d') and self.tecla!=ord('a'): self.tecla = teclaActual
                if teclaActual in self.cerrar: self.tecla = teclaActual
            
            if self.tecla in self.cerrar:
                curses.endwin()
                self.mostrar_puntuacion(self.puntuacion, True)
                break
            
            serpiente_x = self.serpiente[0][1]      #temporary head coordinate value. first pair, second value (10)
            serpiente_y = self.serpiente[0][0]      #temporary head coordinate value. first pair, first value (1)
            if self.tecla == ord('d'): serpiente_x +=1
            if self.tecla == ord('s'): serpiente_y +=1
            if self.tecla == ord('a'): serpiente_x -=1
            if self.tecla == ord('w'): serpiente_y -=1
            self.serpiente.insert(0, [serpiente_y, serpiente_x])    #head changes direction, updates the snake coordinates
            
            serpiente_x = self.serpiente[0][1]
            serpiente_y = self.serpiente[0][0]
            if serpiente_y == 0: self.serpiente[0][0] = self.ventana_juego_altura - 2
            if serpiente_y == self.ventana_juego_altura - 1: self.serpiente[0][0]= 1
            if serpiente_x == 0: self.serpiente[0][1] = self.ventana_juego_anchura - 2
            if serpiente_x == self.ventana_juego_anchura - 1: self.serpiente[0][1]= 1
            
            if self.serpiente[0] in self.serpiente[1:]: #if the head touches any part of the body
                curses.endwin()
                self.mostrar_puntuacion(self.puntuacion, False)
                break
            
            if self.serpiente[0] == self.comida:    #if the head touches food
                self.puntuacion += 1 
                self.velocidad -= 2

                while True:                 #tries to generate food coordinates
                    self.comida = [ randint(1, self.ventana_juego_altura - 2), randint(1, self.ventana_juego_anchura - 2) ]
                    if self.comida not in self.serpiente: 
                        break               #if food coordinates are OK (don't colide), breaks the loop
                
                if curses.has_colors():  
                    self.ventana_serpiente.attrset(curses.color_pair(1)) 
                self.ventana_serpiente.addch(self.comida[0], self.comida[1], '✱')
                
            else:       #if the head does not touch food
                cola = self.serpiente.pop()         #removes tip and saves the coordinate (2 var list)
                self.ventana_serpiente.addch(cola[0], cola[1], ' ')     #adds blank into the previous coordinates of cola
            
            if curses.has_colors(): 
                self.ventana_serpiente.attrset(curses.color_pair(2)) 
            self.ventana_serpiente.addch(self.serpiente[0][0],self.serpiente[0][1], self.cabeza)
            
            if curses.has_colors(): 
                self.ventana_serpiente.attrset(curses.color_pair(4)) 
            for cuerpo in self.serpiente[1:]:
                self.ventana_serpiente.addch(cuerpo[0], cuerpo[1], self.cuerpo)
                
curses.wrapper(PiSerpiente)
        
        
    
