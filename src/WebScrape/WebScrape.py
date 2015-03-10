'''
Created on Mar 6, 2015

@author: wim
'''

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time

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
        #print ("prep_browser\n\tstart server " + self.browser)
        if self.browser == 'phantomjs':
            browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        else:
            browser = webdriver.Firefox() # Get local session of firefox

        #print ("\tset window")
        browser.set_window_size(1280, 2000)
        #print ("\tdone")
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

    def procItem(self, r, nr):
        #key = ';'.join(r.split('\n'))
        s = r.split('\n')
        #print("r = %s" % r)
        #print(s)
        #print("l = %d" % len(s))
        key = s[0] + ';' + s[2]
        #print("key = %s" % key)
        item = {'key':key, 'nr': nr, 'start': s[0], 'end': s[1], 'kenteken': s[2]}
        #print item['key']
        return item

    def openRdw(self):
        if self.debug:
            print "openRdw"
        browser = self.prep_browser()
        if self.debug:
            print "\tgoto link"
        browser.get("https://www.rdw.nl/particulier/Paginas/default.aspx") # Load page
        if self.debug:
            print "\tsleep"
        time.sleep(1)
        if self.debug:
            print "\tget shot"
        browser.save_screenshot('screen_openPage.png')
        if self.debug:
            print "done"
        return browser

    def enterKenteken(self, browser, kenteken):
        elem = browser.find_element_by_id("ctl00_PlaceHolderMain_ctl05_PlateTextBox")
        #print("found %d" % len(elem))
        #elem = browser.find_element_by_id("ctl00_PlaceHolderMain_ctl05_PlateTextBox")
        elem.send_keys(kenteken)
        browser.save_screenshot('screen_enterKenteken.png')
        #time.sleep(5)
        #elem[0].send_keys(kenteken + Keys.RETURN)
        #time.sleep(5)

        elem2 = browser.find_element_by_xpath("//input[@value='Gegevens opvragen']")
        elem2.click()
        time.sleep(1)
        browser.save_screenshot('screen_enterKenteken2.png')


    def getInfo(self, browser, kenteken):
        info = {}
        info['kenteken'] = kenteken
        try:
            info['merk'] = browser.find_element_by_id("Merk").text
            info['naam'] = browser.find_element_by_id("Handelsbenaming").text
            try:
                info['kleur'] = browser.find_element_by_id("Kleur").text
            except:
                info['kleur'] = 'onbekend'
            iname = "InrichtingCodeOmschrijving"
            info['InrichtingCodeOmschrijving'] = browser.find_element_by_id(iname).text
        except:
            print "problem retrieving info from site"
            browser.save_screenshot('screen.png')

        return info

    def getRdwInfo(self, kenteken):
        if self.debug:
            print "getRdwInfo\n\topen browser"
        browser = self.openRdw()
        self.enterKenteken(browser, kenteken)
        info = self.getInfo(browser, kenteken)
        browser.close()
        return info
