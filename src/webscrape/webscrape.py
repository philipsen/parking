'''
Created on Mar 6, 2015

@author: wim
'''

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time
import logging
from selenium.common.exceptions import NoSuchElementException

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

    @staticmethod
    def login(browser, krtnum, pin):
        '''
        login
        '''
        elem = browser.find_element_by_xpath("//input[@placeholder='Nummer']")
        elem.send_keys(krtnum)
        elem = browser.find_element_by_xpath("//input[@placeholder='Pincode']")
        elem.send_keys(pin)
        elem = browser.find_element_by_xpath("//div[@ng-click='vm.login()']")
        elem.click()
        return elem

    @staticmethod
    def show_history(browser):
        '''
        open history on site
        '''
        time.sleep(5)
        browser.save_screenshot('screen_afterLogin.png')
        elem = browser.find_element_by_xpath("//span[@class='pull-right ng-binding']")
        remaing_hours = elem.text
        elem = browser.find_element_by_xpath("//div[@ng-click='vm.toggleMenu()']")
        elem.click()
        time.sleep(1)
        elem = browser.find_element_by_class_name("glyphicon-stats")
        elem2 = elem.find_element_by_xpath("..")
        elem2.click()
        time.sleep(1)
        elem = browser.find_element_by_xpath("//div[@ng-click='vm.toggleReservations()']")
        elem.click()
        time.sleep(2)
        return remaing_hours

    @staticmethod
    def get_history_elements(browser):
        '''
        get all lines in the table
        '''
        elems = browser.find_elements_by_xpath("//div[@ng-repeat='res in vm.reservations']")
        res = []
        for elem in elems:
            res.append(elem.text)
        return res

    def get_history(self, krtnum, pin):
        '''
        get history from site and process
        '''
        browser = self.open_parkeren_delft()
        time.sleep(2)
        self.login(browser, krtnum, pin)
        remaing_hours = self.show_history(browser)
        res = self.get_history_elements(browser)
        browser.close()
        return (remaing_hours, res)

    @staticmethod
    def proc_item(result, krtnum):
        ''' process item '''
        split = result.split('\n')
        #print len(split)
        if len(split) < 4:
            return None

        key = split[0] + ';' + split[2]
        item = {'key':key, 'nr': krtnum, 'start': split[0],
                'end': split[1], 'kenteken': split[2]}

        if "*" in item['kenteken']:
            return None
        return item

    def open_rdw(self):
        '''
        point browser to rdw site
        '''
        logging.info("open_rdw")
        browser = self.prep_browser()
        logging.info("goto link")
        browser.get("https://www.rdw.nl/particulier/Paginas/default.aspx") # Load page
        time.sleep(1)
        browser.save_screenshot('screen_openPage.png')
        return browser

    @staticmethod
    def enter_kenteken(browser, kenteken):
        '''
        enter the license code on the site
        '''
        elem = browser.find_element_by_id("ctl00_PlaceHolderMain_ctl05_PlateTextBox")
        elem.send_keys(kenteken)
        browser.save_screenshot('screen_enterKenteken.png')
        elem2 = browser.find_element_by_xpath("//input[@value='Gegevens opvragen']")
        elem2.click()
        time.sleep(1)
        browser.save_screenshot('screen_enterKenteken2.png')

    @staticmethod
    def get_info(browser, kenteken):
        '''
        retrieve info from page
        '''

        logging.warn('get_info %s', kenteken)
        info = {}
        info['kenteken'] = kenteken
        info['merk'] = 'onbekend'
        info['naam'] = 'onbekend'
        info['kleur'] = 'onbekend'
        info['InrichtingCodeOmschrijving'] = 'onbekend'

        ## if the license is "****", dont bother
        if '*' in kenteken:
            return info

        try:
            elem = browser.find_element_by_id("Kleur")
            info['kleur'] = elem.text
        except NoSuchElementException:
            info['kleur'] = 'onbekend'

        print 'info 2 = {}'.format(info)

        try:
            elem = browser.find_element_by_id("Merk")
            info['merk'] = elem.text
        except NoSuchElementException:
            pass

        try:
            elem = browser.find_element_by_id("Handelsbenaming")
            info['naam'] = elem.text
        except NoSuchElementException:
            pass

        try:
            elem = browser.find_element_by_id("InrichtingCodeOmschrijving")
            info['InrichtingCodeOmschrijving'] = elem.text
        except NoSuchElementException:
            elem = browser.find_element_by_id("CorrosserieOmschrijving")
            info['InrichtingCodeOmschrijving'] = elem.text
            
        print 'info2 = {}'.format(info)
        browser.save_screenshot('screen.png')
        return info

    def get_rdw_info(self, kenteken):
        ''' return license info retieve from site '''
        logging.warn("get_rdw_info\n\topen browser for: %s", kenteken)

        ## if the license is "****", dont bother
        if '*' in kenteken:
            info = {}
            info['kenteken'] = kenteken
            info['merk'] = 'onbekend'
            info['naam'] = 'onbekend'
            info['kleur'] = 'onbekend'
            info['InrichtingCodeOmschrijving'] = 'onbekend'
            return info
        else:
            browser = self.open_rdw()
            self.enter_kenteken(browser, kenteken)
            info = self.get_info(browser, kenteken)
            browser.close()
            return info
