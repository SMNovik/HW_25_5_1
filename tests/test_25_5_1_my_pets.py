import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_my_pets(auth_pets):
    """ Проверяем, все ли питомцы присутствуют"""

    driver = auth_pets

    # считаем сколько строк tr есть в div, где находятся питомцы(в каждом tr - один питомец)
    all_my_pets = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))

    ## без ожидания
    # all_my_pets = testing.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    print('\nКоличество питомцев : ', len(all_my_pets))

    # Вытаскиваем методом get_attribute('innerText') весь текст из блока div
    # our_text = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').get_attribute('innerText')

    our_text = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]'))).get_attribute('innerText')

    # Находим текст от включая 'Питомцев' до 'Друзей'
    all_pets_text = our_text[our_text.find('Питомцев'):our_text.find('Друзей')]
    print('Наш найденный текст :', all_pets_text)

    # Вытаскиваем все цифры из найденного текста в список
    num_text = re.findall(r'\d+', all_pets_text)

    # # Вытаскиваем все цифры из текста 2м способом(сразу цифрой)
    #
    # num_text = int("".join(filter(str.isdigit, all_pets_text)))
    # print('Вытащенные из текста цифры', num_text)

    # Переводим нужный нам элемент списка вытащенных цифр в int
    all_pets_num = int(num_text[0])

    print('Количество наших питомцем : ', all_pets_num)

    # проверяем, что количество питомцев в строках , совпадает с данными из статистики
    assert len(all_my_pets) == all_pets_num


def test_count_photo(auth_pets):
    """  Проверяем, что хотя бы у половины питомцев есть фото"""

    driver = auth_pets

    driver.implicitly_wait(10)

    # находим все img в блоке, где находятся наши питомцы
    images = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets img')

    # Считаем сколько питомцев с фотографиями

    count_img = 0

    for i in range(len(images)):
        # print('Посмотрим images!!!', images[i].get_attribute('src'))
        # атрибут src  пустой , если нет фотки, проверяем это
        if images[i].get_attribute('src') != '':
            # считаем количество img src c НЕ пустой фотографией
            count_img += 1

    # проверяем, что хотя бы у половины питомцев есть фото
    assert len(images) / 2 <= count_img


def test_pets_properties(auth_pets):
    """  Проверяем, что у всех питомцев есть имя, возраст и порода"""

    driver = auth_pets

    driver.implicitly_wait(10)

    # считаем сколько блоков tr есть в div , где находятся питомцы(в каждом tr - один питомец)
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    # создадим список только c данными наших питомцев (без лишних данных)
    pets_info = [pet.text.split('\n')[0] for pet in all_my_pets]
    # print('\nСписок питомцев : ', pets_info)

    # создадим список списков с характеристиками питомцев
    pets_properties = [property.split(' ') for property in pets_info]
    # print('\nДанные питомцев : ', pets_properties)

    # 2й способ получить список со списком характеристик каждого отдельного питомца
    # pets_properties = []
    #
    # # соберем свойства в списки
    # for i in range(1, len(all_my_pets) + 1):
    #     pet = []
    #     for j in range(1, 4):
    #         my_pets = driver.find_element(By.XPATH, f'//div[@id ="all_my_pets"]//tbody/tr[{i}]/td[{j}]').text
    #         # print('\nХарактеристики питомца', my_pets)
    #
    #         # получаем список характеристик каждого отдельного питомца
    #         pet.append(my_pets)
    #
    #     # собираем в список списки всех моих питомцев с характеристиками (свойствами)
    #     pets_properties.append(pet)
    # print('\nСписок списков  с характеристиками питомцев', pets_properties)

    # проверяем, что у всех питомцев есть имя, возраст и порода
    for i in range(len(pets_properties)):
        for j in range(0, 3):
         assert pets_properties[i][j] != ''


def test_pets_name(auth_pets):
    """  Проверяем, что у всех питомцев разные имена"""

    driver = auth_pets

    driver.implicitly_wait(10)

    # находим все tr в div, где находятся питомцы(в каждом tr - один питомец)
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    pet_name = [pet.text.split(' ')[0] for pet in all_my_pets]
    print('\nСписок имен : ', pet_name)

    #######################################################################
    # # 2й способ сделать список имен
    # # pet_name - список имен питомцев
    # pet_name = []
    #
    # # соберем свойства в списки
    # for i in range(1, len(all_my_pets) + 1):
    #     for j in range(1, 4):
    #         my_pets = driver.find_element(By.XPATH, f'//div[@id ="all_my_pets"]//tbody/tr[{i}]/td[{j}]').text
    #         # print('Данные питомцев в списке', my_pets)
    #
    # # начиная с 1го через каждые 3 будет имя, собираем их в список
    #         if j % 3 == 1:
    #            pet_name.append(my_pets)
    #
    # print('\nСписок имен питомцев', pet_name)
    #####################################################
    # # 3й способ создать список имен
    # pet_names = []
    # for pet in all_my_pets:
    #     pet_names.append(pet.find_element(By.TAG_NAME, 'td').text)
    # print('\nсмотрим по тегу', pet_names)

    assert len(set(pet_name)) == len(pet_name)


def test_no_duplicate_pets(auth_pets):
    """ Проверяем, что в списке нет повторяющихся питомцев"""

    driver = auth_pets

    driver.implicitly_wait(10)

    # all_my_pets - наши питомцы(количество элементов , говорит о количестве питомцев)
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    # создадим список c данными наших питомцев
    pets_info = [pet.text for pet in all_my_pets]
    print('\nДанные питомцев : ', pets_info)

    # #чтобы получить список задвоенных питомцев - методом count подсчитываем сколько раз питомец встречается в списке
    # и генерируем список из тех , которые встречаются больше 1го раза, т.к. будут подсчитваться все элементы списка,
    # то убираем задвоенные при помощи set
    #
    # dublicate_pets = set([pet.text for pet in all_my_pets if pets_info.count(pet.text) > 1])
    # print('Повторяющиеся питомцы', dublicate_pets)

    assert len(all_my_pets) == len(set(pets_info))
