'''
Created on Mar 6, 2015

@author: wim
'''

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time
import logging

class WebScrape(object):
    '''
    classdocs
    '''

    def __init__(self, browser="firefox", debug=False):
        '''
        Constructor
        '''
        self.browser = browser
        self.debug = debug

    def prep_browser(self):
        '''
        set up browser
        '''
        if self.browser == 'phantomjs':
            browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        else:
            browser = webdriver.Firefox() # Get local session of firefox
        browser.set_window_size(1280, 2000)
        return browser

    def open_parkeren_delft(self):
        ''' goto site
        '''
        browser = self.prep_browser()
        browser.get("https://parkeren.delft.nl/BezoekersApp") # Load page
        return browser

    def login(self, browser, nr, pin):
        '''
        login
        '''
        elem = browser.find_element_by_xpath("//input[@placeholder='Nummer']")
        elem.send_keys(nr)
        elem = browser.find_element_by_xpath("//input[@placeholder='Pincode']")
        elem.send_keys(pin)
        elem = browser.find_element_by_xpath("//div[@ng-click='vm.login()']")
        elem.click()
        return elem

    def show_history(self, browser):
        '''
        open history on site
        '''
        time.sleep(5)
        browser.save_screenshot('screen_afterLogin.png')
        if self.debug:
            print "get remaining hours"
        elem = browser.find_element_by_xpath("//span[@class='pull-right ng-binding']")
        remaing_hours = elem.text
        if self.debug:
            print remaing_hours

        if self.debug:
            print "click the menu"
        elem = browser.find_element_by_xpath("//div[@ng-click='vm.toggleMenu()']")
        elem.click()
        time.sleep(1)
        print "click the history item"
        elem = browser.find_element_by_class_name("glyphicon-stats")
        elem2 = elem.find_element_by_xpath("..")
        elem2.click()
        time.sleep(1)
        print "open list with reservations"
        elem = browser.find_element_by_xpath("//div[@ng-click='vm.toggleReservations()']")
        elem.click()
        time.sleep(2)
        return remaing_hours

    def get_history_elements(self, browser):
        '''
        get all lines in the table
        '''
        elems = browser.find_elements_by_xpath("//div[@ng-repeat='res in vm.reservations']")
        res = []
        for e in elems:
            res.append(e.text)
        return res

    def get_history(self, nr, pin):
        '''
        get history from site and process
        '''
        browser = self.open_parkeren_delft()
        time.sleep(2)
        self.login(browser, nr, pin)
        remaing_hours = self.show_history(browser)
        res = self.get_history_elements(browser)
        browser.close()
        return (remaing_hours, res)

    def proc_item(self, r, nr):
        s = r.split('\n')
        key = s[0] + ';' + s[2]
        item = {'key':key, 'nr': nr, 'start': s[0], 'end': s[1], 'kenteken': s[2]}
        return item

    def open_rdw(self):
        logging.info("open_rdw")
        browser = self.prep_browser()
        logging.info("goto link")
        browser.get("https://www.rdw.nl/particulier/Paginas/default.aspx") # Load page
        time.sleep(1)
        browser.save_screenshot('screen_openPage.png')
        return browser

    def enter_kenteken(self, browser, kenteken):
        elem = browser.find_element_by_id("ctl00_PlaceHolderMain_ctl05_PlateTextBox")
        elem.send_keys(kenteken)
        browser.save_screenshot('screen_enterKenteken.png')
        elem2 = browser.find_element_by_xpath("//input[@value='Gegevens opvragen']")
        elem2.click()
        time.sleep(1)
        browser.save_screenshot('screen_enterKenteken2.png')

    def get_info(self, browser, kenteken):
        info = {}
        info['kenteken'] = kenteken
        try:
            info['merk'] = browser.find_element_by_id("Merk").text
            info['naam'] = browser.find_element_by_id("Handelsbenaming").text
            try:
                info['kleur'] = browser.find_element_by_id("Kleur").text
            except(KeyError):
                info['kleur'] = 'onbekend'
            iname = "InrichtingCodeOmschrijving"
            info['InrichtingCodeOmschrijving'] = browser.find_element_by_id(iname).text
        except(IOError):
            logging.error("problem retrieving info from site")
            browser.save_screenshot('screen.png')

        return info

    def get_rdw_info(self, kenteken):
        logging.info("get_rdw_info\n\topen browser")
        browser = self.open_rdw()
        self.enter_kenteken(browser, kenteken)
        info = self.get_info(browser, kenteken)
        browser.close()
        return info
