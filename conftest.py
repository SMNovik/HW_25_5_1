from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def auth_pets():
    pytest_driver = webdriver.Chrome()

    pytest_driver.implicitly_wait(10)

    # Переходим на страницу авторизации
    pytest_driver.get('http://petfriends.skillfactory.ru/login')

    pytest_driver.maximize_window()

    # Вводим email
    WebDriverWait(pytest_driver, 5).until(
        EC.presence_of_element_located((By.ID, 'email'))).send_keys('forsf2022@mail.ru')

    # Вводим пароль
    WebDriverWait(pytest_driver, 5).until(
        EC.presence_of_element_located((By.ID, 'pass'))).send_keys('TAPXojuiu34*')

    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest_driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

    # Нажимаем на кнопку "Мои питомцы" для перехода на страницу с моими питомцами
    WebDriverWait(pytest_driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Мои питомцы")]'))).click()
    sleep(2)

    yield pytest_driver

    pytest_driver.quit()
