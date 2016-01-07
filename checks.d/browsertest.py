#!/usr/bin/env python
# from checks import AgentCheck
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sys


class BrowserTestCheck(AgentCheck):
    def check(self, instance):
        def get_projects_container_elem():
            return driver.find_element_by_css_selector('.projects-container')

        def is_page_loaded(*args):
            elem = get_projects_container_elem()
            return elem is \
                not None

        self.log.info('Running browser tests...')

        timeout = 30

        driver = webdriver.PhantomJS(
            service_args=['--ignore-ssl-errors=true', '--ssl-protocol=ANY', ])
        driver.set_window_size(1024, 768)
        driver.set_page_load_timeout(timeout)
        try:
            self.log.debug('Loading page...')
            driver.get('https://staging.muzhack.com')
        except TimeoutException:
            self.log.error(
                'Could not load page within {} seconds'.format(
                    timeout))
        else:
            wait = WebDriverWait(driver, timeout)
            try:
                self.log.debug('Waiting for projects to have loaded...')
                wait.until(is_page_loaded)
            except TimeoutException:
                self.log.error(
                    'Could not load projects within {} seconds'.format(
                        timeout))
            else:
                elem = get_projects_container_elem()

                project_elems = elem.find_elements_by_css_selector(
                    '.project-item')
                if project_elems:
                    self.log.success(
                        'Projects were successfully loaded within the '
                        'timeout ({} seconds)'.format(timeout))
                else:
                    self.log.error(
                        'Projects were unsuccessfully loaded within the '
                        'timeout ({} seconds)'.format(timeout))
