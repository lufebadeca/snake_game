#!/usr/bin&env python3
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

class PiSerpiente:
    def __init__(self, screen):
        self.pantalla = screen

        self.serpiente = [[1,10],[1,9],[1,8],[1,7]]
        self.comida = [5,20]
        
        self.puntuacion = 0
        self.cabeza= 'Ö'
        self.cuerpo = 'o'
        self.velocidad = 100
        
        self.direcciones = (KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN)
        self.tecla = KEY_RIGHT
        self.cerrar = (ord('c'),ord('C'))
        
        curses.curs_set(0) #disables pointer flickering
        
    def pintar_ventana(self):
        self.pantalla_altura, self.pantalla_anchura = self.pantalla.getmaxyx()
        self.ventana_juego_altura = 30
        self.ventana_juego_anchura = 80
        
        self.ventana_serpiente = curses.newwin(self.ventana_juego_altura, self.ventana_juego_anchura, self.pantalla_altura // 2 - self.ventana_juego_altura // 2, self.pantalla_anchura // 2 - self.ventana_juego_anchura // 2  )
        
        self.ventana_serpiente.box()
        self.ventana_serpiente.border('|', '|', '|', '-', '-', '+', '+', '+', '+')
        self.pantalla.refresh()
        
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        
        if curses.has_colors():
            self.ventana_serpiente.attrset(curses.color_pair(1))
        self.ventana_serpiente.addch(self.comida[0], self.comida[1], '*')
        
        while True:
            if curses.has_colors():
                self.ventana_serpiente.attrset(curses.color_pair(3))
            bandera = '[ {t} - Puntuación:]'.format(t=self.__class__.__name__, s=self.puntuacion)
            self.ventana_serpiente.addstr(0, 2, bandera)
            
            self.ventana_serpiente.timeout(self.velocidad)
            
            tecla = self.ventana_serpiente.getch()
            if tecla in self.direcciones + self.cerrar:
                self.tecla = tecla
            
            if self.tecla in self.cerrar:
                curses.endwin()
                self.mostrar_puntuacion(self.puntuacion)
                break
            
            def mostrar_puntuacion(self, puntuacion):
                self.pantalla.clear()
                fin = 'Su puntuación: {s} puntos(s)'.format(s=puntuacion)
                self.pantalla.addstr(self.pantalla_altura // 2, self.pantalla_anchura // 2 - len(fin) // 2, fin)
                self.pantalla.refresh()
                self.pantalla.getch()
                
                serpiente_x = self.serpiente[0][1]
                serpiente_y = self.serpiente[0][0]
                if self.tecla == KEY_RIGHT: serpiente_x +=1
                if self.tecla == KEY_DOWN: serpiente_y +=1
                if self.tecla == KEY_LEFT: serpiente_x -=1
                if self.tecla == KEY_UP: serpiente_y -=1
                self.serpiente.insert(0, [serpiente_y, serpiente_x])
                
                serpiente_x = self.serpiente[0][1]
                serpiente_y = self.serpiente[0][0]
                if serpiente_y == 0: self.serpiente[0][0] = self.ventana_juego_altura - 2
                if serpiente_y == self.ventana_juego_altura - 1: self.serpiente[0][0]= 1
                if serpiente_x == 0: self.serpiente[0][1] = self.ventana_juego_anchura - 2
                if serpiente_x == self.ventana_juego_anchura - 1: self.serpiente[0][1]= 1
                
                if self.serpiente[0] in self.serpiente[1:]:
                    curses.endwin()
                    self.mostrar_puntuacion(self.puntuacion)
                    break       #103
        
        
    
