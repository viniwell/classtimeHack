from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from pathlib import Path
import sys



### Add question title if possible
def get_title(driver: webdriver.Chrome, count) -> str:
    result = ''
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[data-testid="student-session-question-title"]'))
        )

        ### get question on the current page
        result += f'{count}. {driver.find_element(By.CSS_SELECTOR, 'h2[data-testid="student-session-question-title"]').get_attribute("innerHTML")}\n'

    except:
        print(f"ERROR: Couldn't fetch title of question #{count}")


    return result



### Add answer options to result if possible
def get_options(driver:webdriver.Chrome, count) -> str:

    result = ''

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-text="true"]'))
        )

        answer_options = driver.find_elements(By.CSS_SELECTOR, 'span[data-text="true"]')
        for option in answer_options:
            result += f'        {option.get_attribute("innerHTML")}\n'

    except:
        print(f"WARNING: No answer options found for question #{count}")

    return result



### Go to next question if possible
def go_to_next_question(driver: webdriver.Chrome) -> bool:
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="student-next-question-button"]'))
        )

        next_question_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="student-next-question-button"]')
        next_question_button.click()

    except:
        return False
    
    return True




def fetch_image(driver:webdriver.Chrome, count) -> None:
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="https://images.classtime.com/gopollock/image/upload/"]'))
        )

        image = driver.find_element(By.CSS_SELECTOR, 'img[src*="https://images.classtime.com/gopollock/image/upload/"]')

        print(f'file: {__file__}')
        path = Path(os.path.join(__file__, f"../images/{count}.png")).resolve()
        path.parent.mkdir(exist_ok=True, parents=True) # creates directory and file, if there isn't one
        print(str(path))


        if not image.screenshot(str(path)):
            print(f"Failed to save image of question #{count}")



    except:
        pass



if __name__ == "__main__":
    print(f'file: {__file__}')
    path = Path(os.path.join(__file__, f"../images/{1}.png")).resolve()
    path.parent.mkdir(exist_ok=True, parents=True) # creates directory and file, if there isn't one
    print(str(path))