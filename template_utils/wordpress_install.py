'''Creates a new wordpress site on the webfaction server

arg1: the subdomain to create
'''

# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains

import os, sys, time, re
import urllib, urlparse, unittest

# if we're running this script independent of the framework
# we need to add the sebo_runner directory to the path
if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.dirname(this_dir)
    sebo_runner_dir = os.path.join(script_dir, 'sebo_runner' )

    sys.path.append(sebo_runner_dir)
    #main()

import vars

webfaction_user = vars.ftp_username
webfaction_passwd = vars.ftp_password
website_name = sys.argv[1].replace(' ', '')
if not re.compile('^[a-zA-Z0-9\.\-]+$').search(website_name) and not website_name.startswith('-') and not website.endswith('-'):
    raise Exception('You\'re getting too fancy with your subdomain. ' \
                    'The subdomain must only contain the characters a-Z and 1-9 and dashes and periods. ' \
                    'The subdomain must also not start or end with a dash.')

class WordpressInstall():
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://my.webfaction.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    def install_wordpress(self):
        try:
            driver = self.driver

            #login to webfaction
            driver.get(self.base_url + "/")
            driver.find_element_by_id("id_username").clear()
            driver.find_element_by_id("id_username").send_keys(webfaction_user)
            driver.find_element_by_id("id_password").clear()
            driver.find_element_by_id("id_password").send_keys(webfaction_passwd)
            driver.find_element_by_css_selector('#loginbox button[type="submit"]').click()

            if True:
                #create the wordpress site
                driver.find_element_by_link_text("DOMAINS / WEBSITES").click()
                driver.find_element_by_link_text("Websites").click()
                driver.find_element_by_link_text("Add new website").click()
                driver.find_element_by_id("id_name").clear()
                driver.find_element_by_id("id_name").send_keys(website_name)
                driver.find_element_by_css_selector("#website_form .subdomains-tokeninput input").click()
                time.sleep(1)
                driver.find_element_by_css_selector("#website_form .subdomains-tokeninput input").clear()
                driver.find_element_by_css_selector("#website_form .subdomains-tokeninput input").send_keys(website_name + ".sebodev.com")
                time.sleep(1)
                driver.find_element_by_id('website_table').click()
                time.sleep(.5)
                driver.find_element_by_id("add-another").click()
                time.sleep(1)
                driver.find_element_by_link_text("Create a new application").click()
                time.sleep(1)

                driver.find_element_by_css_selector('#name_row > td > #id_name').clear()
                driver.find_element_by_css_selector("#name_row > td > #id_name").send_keys(website_name)
                Select(driver.find_element_by_id("id_app_category")).select_by_visible_text("WordPress")

                btn = driver.find_element_by_css_selector("div.modal-footer > div > button.submit-button")
                ActionChains(driver).move_to_element(btn).click().perform()
                print('waiting 20 seconds for the website request to submit')
                time.sleep(20)
                driver.find_element_by_css_selector("#website_form .submit-button").click()
                time.sleep(1)


            #grab the password
            driver.find_element_by_link_text("DOMAINS / WEBSITES").click() #temporary line of code
            driver.find_element_by_link_text("Applications").click()
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.5)

            driver.find_element_by_css_selector(".application .row-item[data-title~='" + website_name  + "']").click()
            wp_initial_passwd = driver.find_element_by_css_selector('#extra_info .read_only_field').text
            print('successfully created %s with the username sebodev and the temporary password %s' % (website_name+".sebodev.com", wp_initial_passwd))

            if True:
                #change some wordpress settings
                print("There is about a 5 minute wait for your site to be created. If you notice your site is created before this time, you may push enter to continue")
                # for i in range(300):
                #     time.sleep(1)
                #     if sys.stdin.read(1):
                #         break;
                for i in range(300):
                  line=sys.stdin.readline()
                  if line:
                    sys.stdout.write('continuing on')
                    break
                  else:
                    sys.stdout.flush()
                    time.sleep(1)

            driver.get('http://' + website_name + ".sebodev.com" + "/wp-admin")
            print('let me take a moment to make a few tweaks to your wordpress installation for you...')
            driver.find_element_by_id("user_login").clear()
            driver.find_element_by_id("user_login").send_keys("sebodev")
            driver.find_element_by_id("user_pass").clear()
            driver.find_element_by_id("user_pass").send_keys(wp_initial_passwd)
            driver.find_element_by_id("wp-submit").click()
            #time.sleep(1)
            driver.get('http://%s.sebodev.com/wp-admin/user-new.php' % website_name)
            driver.find_element_by_id("user_login").clear()
            driver.find_element_by_id("user_login").send_keys("sitekeeper")
            driver.find_element_by_id("email").clear()
            driver.find_element_by_id("email").send_keys("hi@sebodev.com")
            driver.find_element_by_id("first_name").clear()
            driver.find_element_by_id("first_name").send_keys(website_name)
            driver.find_element_by_id("last_name").clear()
            driver.find_element_by_id("last_name").send_keys("Admin")
            driver.find_element_by_id("url").clear()
            driver.find_element_by_id("url").send_keys("http://sebodev.com")
            driver.find_element_by_id("send_user_notification").click()
            Select(driver.find_element_by_id("role")).select_by_visible_text("Administrator")
            driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
            driver.find_element_by_id("createusersub").click()
            driver.find_element_by_link_text("Log Out").click()
            driver.find_element_by_id("user_login").clear()
            driver.find_element_by_id("user_login").send_keys("sitekeeper")
            driver.find_element_by_id("user_pass").clear()

            import string, random
            ascii = string.letters + string.digits + string.punctuation
            passwd_size = 16
            password = ''.join((random.SystemRandom().choice(chars)) for i in range(passwd_size))
            print("the wordpress credential are now username: sitekeeper password: " + password)
            driver.find_element_by_id("user_pass").send_keys(password)
            driver.find_element_by_id("wp-submit").click()
            driver.find_element_by_link_text("All Users").click()
            driver.find_element_by_link_text("Delete").click()
            driver.find_element_by_id("delete_option1").click()
            driver.find_element_by_id("submit").click()
            driver.find_element_by_link_text("Permalinks").click()
            driver.find_element_by_id("permalink_structure").clear()
            driver.find_element_by_id("permalink_structure").send_keys("/%category%/%postname%/")
            driver.find_element_by_id("submit").click()
            driver.find_element_by_link_text("General").click()
            driver.find_element_by_id("blogname").clear()
            driver.find_element_by_id("blogname").send_keys("Social5")
            driver.find_element_by_id("blogdescription").clear()
            driver.find_element_by_id("blogdescription").send_keys("")
            driver.find_element_by_id("submit").click()
            driver.find_element_by_xpath("(//a[contains(text(),'Add New')])[4]").click()
            driver.find_element_by_name("s").clear()
            driver.find_element_by_name("s").send_keys("advanced custom fields")
            driver.find_element_by_id("search-submit").click()
            driver.find_element_by_link_text("Install Now").click()
            driver.find_element_by_link_text("Activate Plugin").click()
            driver.find_element_by_xpath("(//a[contains(text(),'Add New')])[4]").click()
            driver.find_element_by_name("s").clear()
            driver.find_element_by_name("s").send_keys("yoast")
            driver.find_element_by_id("search-submit").click()
            driver.find_element_by_link_text("Install Now").click()
            driver.find_element_by_link_text("Activate Plugin").click()
            driver.find_element_by_xpath("(//a[contains(text(),'Add New')])[4]").click()
            driver.find_element_by_name("s").clear()
            driver.find_element_by_name("s").send_keys("super cache")
            driver.find_element_by_id("search-submit").click()
            driver.find_element_by_link_text("Install Now").click()
            driver.find_element_by_link_text("Activate Plugin").click()
            driver.find_element_by_css_selector("a.current").click()
            driver.find_element_by_name("s").clear()
            driver.find_element_by_name("s").send_keys("ewww")
            driver.find_element_by_id("search-submit").click()
            driver.find_element_by_link_text("Install Now").click()
            driver.find_element_by_link_text("Activate Plugin").click()
            driver.find_element_by_xpath("(//a[contains(text(),'Add New')])[4]").click()
            driver.find_element_by_name("s").clear()
            driver.find_element_by_name("s").send_keys("word fence")
            driver.find_element_by_id("search-submit").click()
            driver.find_element_by_css_selector("button.submit-button").click()

            self.driver.quit()
        except KeyboardInterrupt:
            self.driver.quit()
            time.sleep(3)
            raise

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.main()
    installer = WordpressInstall()
    installer.setUp()
    installer.install_wordpress()
