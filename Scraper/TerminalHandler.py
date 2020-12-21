#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 20:03:31 2020

@author: nico
"""
import curses as cr

class TerminalHandler:
    def __init__(self, logger):
        
        self.logger = logger
        self.log("Terminal initialized")
        
        self.current_index = 0
        self.colors = list()
        self.newtext = list()
        
        cr.curs_set(0)
        cr.init_pair(1, cr.COLOR_BLACK, cr.COLOR_WHITE)
        cr.init_pair(2, cr.COLOR_BLACK, cr.COLOR_RED)
        cr.init_pair(3, cr.COLOR_WHITE, cr.COLOR_RED)
        
        for _ in range(0,100):
            self.colors.append(1)
            self.newtext.append("")
    
    # ************************************************************************
    # High level curses ******************************************************
    
    def reset_colors(self):
        self.colors = list()
        self.newtext = list()
        
        for _ in range(0,100):
            self.colors.append(1)
            self.newtext.append("")
        
    def clear(self, screen):
        screen.clear()
    
    def show_menu(self, titles, screen, secondary, individual_func=False, should_update_index=False, *handlers):
                
        should_run = True
        selection = None
        self.current_index = 0        
        if secondary:
            titles.append("BACK")
        
        while should_run:
            _ = self.update_dims(screen)
            # Print menu
            screen.clear()
            for inx, row in enumerate(titles):
                x = self.w//2 - len(max(titles, key=len))//2
                y = self.h//2 - len(titles)//2 + inx
                
                if self.colors[inx] == 2:
                    text = self.newtext[inx]
                    if text == "":
                        text = row
                    if inx == self.current_index:
                        screen.attron(cr.color_pair(3))
                            
                        screen.addstr(y, x, " " + text + " ")
                        screen.attroff(cr.color_pair(3))
                    else:
                        screen.attron(cr.color_pair(2))
                        screen.addstr(y, x, text)
                        screen.attroff(cr.color_pair(2))
                else:
                    if inx == self.current_index:
                        screen.attron(cr.color_pair(1))
                        screen.addstr(y, x, " " + row + " ")
                        screen.attroff(cr.color_pair(1))
                    else:
                        screen.addstr(y, x, row)
            screen.refresh()
            # Menu printed
            
            # Wait for input
            selection = self.wait_for_input(screen, len(titles))
            
            if selection != None:
                if not individual_func:
                    if secondary:
                        if selection == len(titles) - 1:
                            self.current_index = 0
                            break
                        else:
                            if should_update_index:
                                try:
                                    handlers[selection](screen, selection)
                                except:
                                    handlers[selection](screen)
                            else:
                                handlers[selection](screen)
                    else:
                        handlers[selection](screen)
                else:
                    if selection == len(titles) - 1:
                            self.current_index = 0
                            # self.reset_colors()
                            break
                    else:
                        if should_update_index:
                            try:
                                handlers[0](screen, selection)
                            except:
                                handlers[0](screen)
                        else:
                            handlers[0](screen)
    
    def get_input(self, screen, message):
        
        answer = self.raw_input(screen, message)        
        
        if answer != None:
            screen.clear()
            screen.addstr(0, 0, f"You entered: {answer}. Press any key to continue")
            self.wait_any_key(screen)
            return answer
    
    def change_color_row(self, row, newtext=""):
        if self.colors[row] == 1:
            self.colors[row] = 2
            if newtext != "":
                self.newtext[row] = newtext
        else:
            self.colors[row] = 1
    
    def get_int_input(self, screen, message):
        answer = self.raw_input(screen, message)
        
        if answer != None:
            try:
                screen.clear()
                screen.addstr(0, 0, f"You entered: {answer}. Press any key to continue.")
                self.wait_any_key(screen)
                return int(answer)
            except:
                screen.clear()
                screen.addstr(0, 0, "You didn't enter a number. Press any key to continue.")
                self.wait_any_key(screen)
                return None
    
    def show_message(self, screen, message):
        screen.clear()
        screen.addstr(0, 0, f"{message} Press any key to continue.")
        self.wait_any_key(screen)
    
    # ************************************************************************
    # Low level curses *******************************************************
    
    def wait_any_key(self, screen):
        screen.getch()
        
    def raw_input(self, screen, message):
        screen.clear()
        cr.echo()
        h, w = self.update_dims(screen)
        
        screen.addstr(0, 0, message)
        screen.addstr(h-1, 0, "Enter without typing anything or enter U or u to undo.")
        answer = screen.getstr(2+len(message)//w, 0, 2000).decode()
        
        if answer == "U" or answer == "" or answer == "u":
            self.log("Raw input was interrupted by user")
            return None
        
        self.log(f"Raw input message: {answer}")
        return answer
    
    def update_dims(self, screen):
        h, w = screen.getmaxyx()
        self.h, self.w = h, w
        return (h, w)
        
    def wait_for_input(self, screen, menu_len):
        key = screen.getch()
        screen.clear()
        
        if key == cr.KEY_UP: # and self.current_index > 0:
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = menu_len - 1
            return None
        elif key == cr.KEY_DOWN: # and self.current_index < len(self.current_menu) - 1:
            self.current_index += 1
            if self.current_index > menu_len - 1:
                self.current_index = 0
            return None
                
        elif key == cr.KEY_ENTER or key in [10, 13]:
            return self.current_index
    
    # ************************************************************************
    # LOGGER *****************************************************************
    
    def log(self, message):
        self.logger.info(f"[TerminalHandler] {message}")
    
    def error(self, message):
        self.logger.error(f"[TerminalHandler] {message}")
    
