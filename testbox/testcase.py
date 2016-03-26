
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import Select


class SeleniumTestCase(StaticLiveServerTestCase):
    browser_wait = 4

    def setUp(self):
        if hasattr(self, 'firefox_profile'):
            fp = self.firefox_profile
        else:
            fp = webdriver.FirefoxProfile()
        fp.update_preferences()
        self.browser = webdriver.Firefox(firefox_profile=fp)
        self.browser.implicitly_wait(self.browser_wait)
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(SeleniumTestCase, self).tearDown()

    def open_page(self, path):
        self.browser.get(self.live_server_url + path)

    def assertPage(self, path, wait=True, remove_hashtag=True):
        if wait:
            self.wait_for_page_load()
        url = self.browser.current_url
        if remove_hashtag:
            url = self.browser.current_url.split('#')[0]
        self.assertEqual(url, self.live_server_url + path)

    def submit_form(self, form, data, clear=True, submit=True, wait=True):
        for k, v in data.items():
            input_field = form.find_element_by_name(k)
            if input_field.tag_name in ('input', 'textarea'):
                field_type = input_field.get_attribute('type')
                if field_type == 'radio':
                    radio_button = form.find_element_by_css_selector(
                        "input[type=radio][name={}][value='{}']".format(
                            k, v
                        )
                    )
                    radio_button.click()
                elif field_type == 'checkbox':
                    checkbox_button = form.find_element_by_css_selector(
                        'input[type=checkbox][name={}]'.format(k)
                    )
                    if v and not checkbox_button.is_selected():
                        checkbox_button.click()
                    elif not v and checkbox_button.is_selected():
                        checkbox_button.click()
                elif clear and input_field.get_attribute('value'):
                    input_field.clear()
                input_field.send_keys(v)
            elif input_field.tag_name == 'select':
                select_field = Select(input_field)
                select_field.select_by_value(v)
        if submit:
            submit_btn = form.find_element_by_xpath(
                './/button[@type="submit"]')
            submit_btn.click()
        if wait:
            self.wait_for_page_load()

    def login(self, user):
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        self.browser.get(self.live_server_url + "/nonexistent-url/")
        self.browser.add_cookie(
            {
                'name': settings.SESSION_COOKIE_NAME,
                'value': session.session_key,
                'path': '/',
            }
        )

    def wait_for_page_load(self):
        self.browser.find_element_by_tag_name('body')
