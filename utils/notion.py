from selenium.webdriver.common.action_chains import ActionChains

from utils.selenium import find_element, find_element_and_click, find_element_and_send_keys


def click_blue_new(driver):
    new_button_color = 'background: rgb(46, 170, 220);'
    new_button_xpath = f'//div[contains(@style,"{new_button_color}")][text()[contains(.,"New")]]'
    find_element_and_click(driver, new_button_xpath)


def click_open_as_page(driver):
    find_element_and_click(driver, '//text()[contains(.,"Open as Page")]/ancestor::*[self::a][1]')


def new_page_set_name(driver, new_page_name):
    name_input_xpath = '//div[@class="notion-selectable"]/div[@contenteditable="true"][@placeholder="Untitled"]'
    find_element_and_send_keys(driver, name_input_xpath, new_page_name)


def set_column_value(driver, column_type, column_name, new_value):
    if column_type == 'text':
        find_element_and_click(driver, f'//div[text()="{column_name}"]/ancestor::div[3]/following-sibling::div/'
                                       f'descendant::div[text()="Empty"]')
        xpath = '//div[contains(@class, "notion-overlay-container")]//div[@contenteditable="true"][@data-root="true"]'
        find_element_and_send_keys(driver, xpath, new_value, escape=True)
    elif column_type == 'checkbox':
        checkbox = find_element(driver, f'//div[text()="{column_name}"]/ancestor::div[3]/following-sibling::div/'
                                        f'descendant::*[name()="svg"]')
        is_checked = 'points' in checkbox.get_attribute('innerHTML')
        if is_checked != new_value:
            checkbox.click()
    elif column_type == 'calendar':
        find_element_and_click(driver, f'//div[text()[contains(.,"{column_name}")]]')
        find_element_and_click(driver, '//div[text()[contains(.,"Format Date")]]')
        find_element(driver, '//div[contains(@class,"notion-calendar-picker")]')
        find_element_and_send_keys(driver, '//div/input[@type="text"]', new_value, escape=True)
    elif column_type in ['select', 'multi-select']:
        find_element_and_click(driver, f'//div[text()[contains(.,"{column_name}")]]')
        find_element_and_click(driver, '//div[text()[contains(.,"Configure Options")]]')
        option_xpath = f'//div[contains(@class, "notion-scroller vertical")]//div[text()="{new_value}"]'
        find_element_and_click(driver, option_xpath)
    elif column_type == 'relation':
        find_element_and_click(driver, f'//div[text()="{column_name}"]/ancestor::div[3]/following-sibling::div/'
                                       f'descendant::div[text()="Empty"]')
        input_xpath = '//div[contains(@class, "notion-scroller vertical")]//input[@type="text"]'
        find_element_and_send_keys(driver, input_xpath, new_value)
        matching_page_xpath = f'//div[contains(@class, "notion-scroller horizontal")]//span[text()="{new_value}"]'
        matching_page = find_element(driver, matching_page_xpath)
        action = ActionChains(driver)
        action.move_to_element(matching_page).perform()
        driver.find_element_by_xpath(f'{matching_page_xpath}/ancestor::div[4]').click()
        find_element_and_send_keys(driver, input_xpath, '', escape=True)
    else:
        raise ValueError('Invalid Column Type')


def set_page_as_favorite(driver):
    find_element_and_click(driver, '//div[contains(@class, "notion-topbar")]//div[text()="Favorite"]')
