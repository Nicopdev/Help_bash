#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:27:38 2020

@author: nico
"""

import curses as cr
from instaloader import Instaloader, Profile
import logging
from os import makedirs, environ
from os.path import exists
from TerminalHandler import TerminalHandler
from JSONParser import FileManager


WD = "followers_getter_WD"
OPTIONS_DIR = "options.json"
RESULT_DIR = "result.txt"

class Loader:
    
    def __init__(self, screen):
        
        logger = self.init_logger()
        self.parser = FileManager(WD, logger)
        self.terminal = TerminalHandler(logger)
        
        self.options = self.load_options() 
        
        menu = ["START", "CHANGE ACCOUNT", "CHANGE TARGET"]
        self.terminal.show_menu(menu, screen, False, False, False, self.start, self.change_account, self.change_target)
    
    def save_options(self):
        self.parser.encodeJSON(OPTIONS_DIR, self.options)
    
    def load_options(self):
        return self.parser.decodeJSON(OPTIONS_DIR)
        
    def start(self, screen):
        self.terminal.show_message(screen, "The scraper is starting. Please keep in mind that the bot may need some time, especially when scraping data from big profiles.")
        
        try:
            L = Instaloader()
            L.login(self.options["username"], self.options["password"])
            profile = Profile.from_username(L.context, self.options["target"])
            
            users = list()
            for follower in profile.get_followers():
                users.append(follower.username)
                
            # self.logger.info(users)
            self.parser.encode_from_array(RESULT_DIR, users)
            self.terminal.show_message(screen, "DONE!")
            
        except:
            self.terminal.show_message(screen, "Invalid username or password.")

    def change_account(self, screen):        
        new = self.terminal.get_input(screen, "Enter the username and the password separated by a space.\nThey will be save LOCALLY")
        
        if new != None:
            new = new.split(" ")
            if len(new) != 2:
                self.terminal.show_message(screen, "Please enter a username and a password separated by a space.")
                return
            else:
                self.options["username"] = new[0]
                self.options["password"] = new[1]
                self.save_options()

    def change_target(self, screen):
        new = self.terminal.get_input(screen, "Enter the new target profile")
        
        if new != None:
            self.options["target"] = new
            self.save_options()
        
    def init_logger(self):        
        if not exists(WD):
           makedirs(WD)        

        logger = logging.getLogger("followers_getter")
        hdlr = logging.FileHandler(WD + "/followers_getter" + ".log")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)
        
        logger.info("\n\n\nLogger initiated")
        self.logger = logger
        return logger

def main(screen):
    _ = Loader(screen)

if __name__ == '__main__':
    environ['TERMINFO'] = '/bin/bash'
    cr.wrapper(main)
