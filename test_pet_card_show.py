import pytest
import time
import selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="session")
def testing():
    pytest.driver = webdriver.Chrome('../chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.implicitly_wait(2)

    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.ID, 'email')))

    pytest.driver.find_element(By.ID, 'email').send_keys('meged21921@haboty.com')

    pytest.driver.find_element(By.ID, 'pass').send_keys('1234567890')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    yield

    pytest.driver.quit()


def test_show_my_pets(testing):
    # Проверяем, что мы оказались на главной странице пользователя

    # assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # time.sleep(1)
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='Мои питомцы']"))).click()
    # pytest.driver.find_element(By.XPATH, "//a[text()='Мои питомцы']").click()
    time.sleep(1)

    table_pet = pytest.driver.find_elements(By.XPATH, '//tbody//tr')
    photo = pytest.driver.find_elements(By.XPATH, '//tbody//tr//th//img[@src]')
    names = pytest.driver.find_elements(By.XPATH, '//td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//td[2]')
    age = pytest.driver.find_elements(By.XPATH, '//td[3]')
    print(table_pet)
    my_info = pytest.driver.find_elements(By.XPATH, "//div[contains(@class, 'left')]")
    sum_pet = my_info[0].text.split("\n")
    count_my_pet = sum_pet[1]
    count_my_pet = int(count_my_pet[count_my_pet.find(':') + 1:].replace(" ", ""))
    print(count_my_pet)

    count_age = 0
    for i in range(len(age)):
        if age[i].text != '':
            count_age += 1
    assert count_age == len(table_pet)

    count_breed = 0
    for i in range(len(breed)):
        if breed[i].text != '':
            count_breed += 1
    assert count_breed == len(table_pet)

    count_name = 0
    for i in range(len(names)):
        if names[i].text != '':
            count_name += 1
    assert count_name == len(table_pet)

    count_photo = 0
    for i in range(len(table_pet)):
        if photo[i].get_attribute('src') != '':
            count_photo += 1
    assert count_photo > len(table_pet) / 2  # 2


def test_show_pets(testing):
    pytest.driver.find_element(By.XPATH, "//a[@class='navbar-brand header2']").click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(",")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
