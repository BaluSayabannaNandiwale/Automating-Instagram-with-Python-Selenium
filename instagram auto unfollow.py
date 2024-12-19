from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Replace with your Instagram username and password
username = "your_username"
password = "your_password"

# Set up the webdriver
driver = webdriver.Firefox()

# Log in to Instagram
driver.get("https://www.instagram.com/accounts/login/")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

# Get the list of users you follow
driver.get("https://www.instagram.com/" + username + "/")
followers = []
following = []
next_max_id = True
while next_max_id:
    if next_max_id is True:
        next_max_id = ''
    _ = driver.find_element_by_xpath("//a[@href='/{}-/']").get_attribute("href")
    followers.extend([_['pk'] for _ in followers])
    next_max_id = driver.find_element_by_xpath("//a[@href='/{}-/']").get_attribute("href")

# Get the list of users who follow you
followers = set([_['pk'] for _ in followers])
following = set([_['pk'] for _ in following])

# Unfollow users who don't follow you back
unreciprocated = following - followers
for _ in list(unreciprocated)[:50]:  # Unfollow up to 50 users
    driver.get("https://www.instagram.com/" + _ + "/")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqdOP  L3NKy   y3zKF     ']"))).click()
    time.sleep(random.uniform(1, 5))  # Wait a random amount of time between 1 and 5 seconds

# Close the webdriver
driver.quit()