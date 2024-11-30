from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from pathlib import Path
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup as bs



### Add question title if possible
def get_title(driver: webdriver.Chrome, count) -> str:
    result = ''
    try:
        WebDriverWait(driver, 5).until(
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
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="questions-answers-list"] span[data-text="true"]'))
        )

        answer_options = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="questions-answers-list"] span[data-text="true"]')


        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for i in range(len(answer_options)):
            result += f'     {alphabet[i%27]}) {answer_options[i].get_attribute("innerHTML")}\n'

    except:
        print(f"WARNING: No answer options found for question #{count}")
        return "      Unknown type of input (Most likely text input)\n"

    return result



### Go to next question if possible
def go_to_next_question(driver: webdriver.Chrome) -> bool:
    
    try:
        WebDriverWait(driver, 2).until(
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


        path = Path(os.path.join(__file__, f"../images/{count}.png")).resolve()
        path.parent.mkdir(exist_ok=True, parents=True) # creates directory and file, if there isn't one


        if not image.screenshot(str(path)):
            print(f"Failed to save image of question #{count}")



    except:
        pass




def get_table_contents(driver:webdriver.Chrome, count) -> tuple[str, bool]:
    result = ''

    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="student-categorizer-answers-form"]'))
        )

        table_div = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="student-categorizer-answers-form"]')
        table_tag = table_div.find_element(By.CSS_SELECTOR, 'table[role="grid"]')
        

        soup = bs(table_tag.get_attribute("outerHTML"), "html.parser")
        table = soup.find("table")

        # Extract data
        rows = table.find_all("tr")
        data = [[cell.text for cell in row.find_all(["td", "th"])] for row in rows]

        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        

        return (df.to_string(), True)

        


    except:
        return (result, False)
    



def get_additional_info(driver:webdriver.Chrome) -> tuple[str, bool]:

    result = ''

    try:

        style = """outline: none; user-select: text; white-space: pre-wrap; overflow-wrap: break-word;"""
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'div[class="_8ae271eec1188b7ee372cb8b781a3c19"] div[spellcheck="false"][contenteditable="false"][style="{style}"] span[data-text="true"]'))
        )

        data_fields = driver.find_elements(By.CSS_SELECTOR, f'div[class="_8ae271eec1188b7ee372cb8b781a3c19"] div[spellcheck="false"][contenteditable="false"][style="{style}"] span[data-text="true"]')


        #additional_info = additional_info_div.find_element(By.CSS_SELECTOR, 'span[data-text="true"]')
                                        # additionla info is always first
        result += f'  Additional info: {data_fields[0].get_attribute("innerHTML")}\n'
        

    except:
        return ('', False)

    return (result, True)
    
