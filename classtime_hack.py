from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd, sys

from actions import *


def parse_args() -> dict:
    result = {
        "path": "",
        "images": False,
    }

    for arg in sys.argv[1:]:
        if arg == "--images": result["images"] = True
        else: result["path"] = arg

    return result
            

ARGS = parse_args()




def get_questions(url):
    driver = webdriver.Chrome()
    driver.get(url)
    

    ### see if inputfield for name is on the page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id*="text-input-"]'))
        )

    except Exception as e:
        print(e)
        input()
        return "ERROR: Ensure link is correct."
    
    ### get inputfield and pass the name
    name_field = driver.find_element(By.CSS_SELECTOR, 'input[id*="text-input-"]')
    name_field.send_keys("error 404") # for less suspicion


    ### see if 'Join' button is on the page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="student-join-button"]'))
        )

    except Exception as e:
        print(e)
        input()
        return "ERROR: Ensure link is correct."
    
    ### get inputfield and click it
    join_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="student-join-button"]')
    join_button.click()
    

    ############################ FETCHING DATA ##############################
    count = 0
    result = ""


    while True:
        count+=1
        
        ### Add question title if possible
        result += get_title(driver, count)
        
        
        
        ### Add answer options to result if possible
        result += get_options(driver, count)

        ### fetch image if user requests
        if ARGS["images"]:
            fetch_image(driver, count)





        ### Go to next question if possible
        if not go_to_next_question(driver): break


    return result


def main():
    url = input("Provide a link to 'Classtime' test: ")
    print(get_questions("https://www.classtime.com/code/MENFTP"))


if __name__ == "__main__":
    #print(ARGS["images"])
    ARGS["images"] = True
    main()