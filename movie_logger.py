# review_importer.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from movie_importer import ReviewFetcher


class ReviewImporter:
    def __init__(self, targetUsername, targetPassword, sourceUsername,driver_path):
        self.sourceUsername = sourceUsername
        self.username = targetUsername
        self.password = targetPassword
        self.driver_path = driver_path
        self.driver = None

    def login_to_letterboxd(self):
        serviceObj = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=serviceObj)
        self.driver.get("https://letterboxd.com/sign-in/")
        time.sleep(2)
        
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')
        
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(2)

    def navigate_to_diary(self):
        # Wait for the "Diary" link to be clickable and click it
        diary_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Diary'))
        )
        diary_link.click()
        time.sleep(2)

    def set_rating(self, slider_id, rating):
        slider = self.driver.find_element(By.CLASS_NAME, "rateit-range")
        print(slider.size['width'])
        # Assuming the slider range is from 0 to 10
        width = slider.size['width']
        x_offset = -(rating / 10) * width
        webdriver.ActionChains(self.driver).click_and_hold(slider).move_by_offset(x_offset, 0).release().perform()
        time.sleep(2)

    def add_review_to_movies(self, movieName, review,pageNum):
        if pageNum > 1:
            url = f"https://letterboxd.com/{self.sourceUsername}/films/diary/page/{pageNum}/"
        else:
            url = f"https://letterboxd.com/{self.sourceUsername}/films/diary/"
        print(url)

      
        self.driver.get(url)  # Update with the correct URL
        '''
        self.navigate_to_diary()
        time.sleep(0.5)'''
        
        #Find all movie links in the diary
        movie_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT,movieName))
        )
        movie_link.click()
        time.sleep(0.2)

        
        
        try:
            # Wait for the review button and click it
            log_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Review or log"))
            )
            log_link.click()
            time.sleep(2)
            
            # Wait for the review field to be present and input the review
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'review'))
            )
        
           

            review_field = self.driver.find_element(By.NAME, 'review')
            review_field.clear()
            review_field.send_keys(review)
            time.sleep(2)

            self.set_rating('rateit-range-2', 4)
            
            #Wait for save button and then click
            save_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "diary-entry-submit-button"))
            )
            save_link.click()
            time.sleep(2)
        
        except Exception as e:
            print(f"An error occurred while processing movie '{movie_link}': {e}")
            print(self.driver.page_source)  # Print page source for debugging
            self.driver.save_screenshot(f"screenshot_{movieName}.png")  # Save a screenshot for debugging
        
        

    def close(self):
        if self.driver:
            self.driver.quit()


