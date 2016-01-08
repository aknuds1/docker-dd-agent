#!/usr/bin/env python
from checks import AgentCheck
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import sys
import time


class BrowserTestCheck(AgentCheck):
    def check(self, instance):
        def get_projects_container_elem():
            return driver.find_element_by_css_selector('.projects-container')

        def is_page_loaded(*args):
            elem = get_projects_container_elem()
            return elem is \
                not None

        def send_event(title, text, alert_type):
            self.event({
                'timestamp': int(time.time()),
                'event_type': 'browsertest_check',
                'msg_title': title,
                'msg_text': text,
                'alert_type': alert_type,
            })

        self.log.info('Running browser tests...')

        timeout = 60

        driver = webdriver.PhantomJS(
            service_args=['--ignore-ssl-errors=true', '--ssl-protocol=ANY', ])
        driver.set_window_size(1024, 768)
        driver.set_page_load_timeout(timeout)
        try:
            self.log.debug('Loading page...')
            driver.get('https://staging.muzhack.com')
        except TimeoutException:
            self.log.warn(
                'Could not load page within {} seconds'.format(
                    timeout))
            send_event(
                'Projects Page Timeout',
                'Failed to load MuzHack projects page within {} seconds'
                .format(timeout))
        else:
            wait = WebDriverWait(driver, timeout)
            try:
                self.log.debug('Waiting for projects to have loaded...')
                wait.until(is_page_loaded)
            except TimeoutException:
                self.log.warn(
                    'Could not load projects within {} seconds'.format(
                        timeout))
                send_event(
                    'Projects Timeout',
                    'Failed to load MuzHack projects within {} seconds'.format(
                        timeout
                    ))
            else:
                elem = get_projects_container_elem()

                project_elems = elem.find_elements_by_css_selector(
                    '.project-item')
                if project_elems:
                    self.log.info('Projects were successfully loaded')
                    send_event(
                        'MuzHack Projects Page Functioning',
                        'Projects were successfully displayed on MuzHack',
                        'success')
                else:
                    self.log.warn('Projects were unsuccessfully loaded')
                    send_event(
                        'MuzHack Projects Page Failing',
                        'Projects were not displayed on MuzHack', 'error')
