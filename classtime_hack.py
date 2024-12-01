from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

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




def get_browser_options() -> webdriver.ChromeOptions :
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")

    return options


def get_questions(url):


    driver = webdriver.Chrome(options=get_browser_options())
    driver.get(url)
    

    ### see if inputfield for name is on the page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id*="text-input-"]'))
        )

    except Exception as e:
        print(e)
        return "ERROR: Ensure link is correct."
    
    ### get inputfield and pass the name
    name_field = driver.find_element(By.CSS_SELECTOR, 'input[id*="text-input-"]')
    name_field.send_keys( input("Enter the name, with which you will be taking test(it won't start the test, but teacher will see, that you joined): ") ) # for less suspicion


    ### see if 'Join' button is on the page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="student-join-button"]'))
        )

    except Exception as e:
        print(e)
        return "ERROR: Ensure link is correct."
    
    ### get inputfield and click it
    join_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="student-join-button"]')
    join_button.click()
    

    ############################ FETCHING DATA ##############################
    count = 0
    result = ""


    while True:
        count+=1

        if count==1: result += "\n\n\n------------------------------------------\n\n"
        
        ### Add question title if possible
        result += get_title(driver, count)
        
        
       
        if count == 5: 
            test=True
        
        ## get additional info
        additional_info = get_additional_info(driver)
        if additional_info[1]: result+=additional_info[0]

        ### try to find table; function returns tuple[str, bool] - (result, found_or_not)
        table = get_table_contents(driver, count)
        if table[1]:
            ### add table contents
            result += table[0]
        else:
            ### Add answer options to result if possible
            answer_options = get_options(driver, count)
            result += answer_options
                                                

        ### fetch image if user requests
        if ARGS["images"]:
            fetch_image(driver, count)


        result += "\n\n------------------------------------------\n\n"



        ### Go to next question if possible
        if not go_to_next_question(driver): break


    return result


def main():
    if ARGS["path"] == "":
        ARGS["path"] = input("Provide a link to 'Classtime' test: ")
        
    print(get_questions(ARGS["path"]))


if __name__ == "__main__":
    main()