'''
Created on Mar 6, 2015

@author: wim
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class WebScrape:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def prepBrowser(self):
        print ("prepBrowser\n\tstart server")
        browser = webdriver.Firefox() # Get local session of firefox
        #browser = webdriver.PhantomJS("/usr/bin/phantomjs")
        print ("\tset window")
        browser.set_window_size(1280, 2000)
        print ("\tdone")
        return browser

    def openParkerenDelft(self):
        browser = self.prepBrowser()
        browser.get("https://parkeren.delft.nl/BezoekersApp") # Load page
        return browser

    def login(self, browser, nr, pin):
        elem = browser.find_element_by_xpath("//input[@placeholder='Nummer']")
        elem.send_keys(nr)
        elem = browser.find_element_by_xpath("//input[@placeholder='Pincode']")
        elem.send_keys(pin)
        elem = browser.find_element_by_xpath("//div[@ng-click='vm.login()']")
        elem.click()
        return elem
    
    def showHistory(self, browser):
        time.sleep(5)
        browser.save_screenshot('screen_afterLogin.png')
        print "get remaining hours"
        elem = browser.find_element_by_xpath("//span[@class='pull-right ng-binding']")
        remaing_hours = elem.text
        print(remaing_hours)
        
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
        
    def gethistory(self, browser):
        elems = browser.find_elements_by_xpath("//div[@ng-repeat='res in vm.reservations']")
        res = []
        for e in elems:
            res.append(e.text)
        return res

    def getHistory(self, nr, pin):
        browser = self.openParkerenDelft()
        time.sleep(2)
        self.login(browser, nr, pin)
        remaing_hours = self.showHistory(browser)
        res = self.gethistory(browser)
        browser.close()
        return (remaing_hours, res)   

    def procItem(self, r, nr):
        #key = ';'.join(r.split('\n'))
        s = r.split('\n')
        print("r = %s" % r)
        print(s)
        print("l = %d" % len(s))
        key = s[0] + ';' + s[2]
        print("key = %s" % key)
        item = {'key':key, 'nr': nr, 'start': s[0], 'end': s[1], 'kenteken': s[2]}
        print item['key']
        return item

    def openRdw(self):
        print ("openRdw")
        browser = self.prepBrowser()
        print ("\tgoto link")
        browser.get("https://www.rdw.nl/particulier/Paginas/default.aspx") # Load page
        print ("\tsleep")
        time.sleep(1)
        print ("\tget shot")
        browser.save_screenshot('screen_openPage.png') 
        print("done")
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
            
            info['InrichtingCodeOmschrijving'] = browser.find_element_by_id("InrichtingCodeOmschrijving").text
        except:
            print("problem retrieving info from site")
            browser.save_screenshot('screen.png') 

        return info
    
    def getRdwInfo(self, kenteken, debug = False):        
        self._debug = debug
        if debug: print("getRdwInfo\n\topen browser")
        browser = self.openRdw()
        if debug: print("enter kenteken")
        self.enterKenteken(browser, kenteken)
        if debug: print("get info")
        info = self.getInfo(browser, kenteken)
        browser.close()
        return info
    
    


    
