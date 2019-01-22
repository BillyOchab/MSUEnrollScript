from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import getpass


def main():
    msuid_input = input('Enter msu id: ')                         # User input
    msu_pass = getpass.getpass('Enter password: ')
    course_id_input = input('Enter course id: ')
    section_input = input('Enter section: ')

    driver = webdriver.Chrome()                                   # Open the web page
    driver.get("https://schedule.msu.edu/")

    subject = driver.find_element_by_id("MainContent_ddlSubject") # Search the page for a specfic class
    for option in subject.find_elements_by_tag_name("option"):
        if option.text == "CSE: Computer Science & Engineering":
            option.click()
            break
    course_id = driver.find_element_by_id("MainContent_txtCourseNumber")
    course_id.send_keys(course_id_input + Keys.ENTER)


    attempt = 1                                                   # Count to keep track of attempts
    loop = True
    while loop:                                                   # Refresh page every 4 minutes and check if the class is open to enroll
        try:
            title = "Open Section - LOG IN to add CSE " + course_id_input + " Section " + section_input + " to your planner"
            indicator = driver.find_element_by_xpath('//*[@title="'+title+'"]')
            print("Open section found!")
            indicator.click()
            loop = False

        except:
            print("Open section not found! (Attempt #" + str(attempt) + ")")
            attempt += 1
            time.sleep(60*4)                                      # 60*4 = 4 minutes
            driver.refresh()


    login = driver.find_element_by_id("netid")                    # Once a open section is found, log the user in and enroll in the class
    login.send_keys(msuid_input)
    login = driver.find_element_by_id("pswd")
    login.send_keys(msu_pass + Keys.ENTER)

    title = "Enroll in CSE " + course_id_input + " Section " + section_input 
    indicator = driver.find_elements_by_xpath('//*[@title="'+title+'"]') 
    if len(indicator) == 1:                                       # Different method to click the title. Difference of find_element vs find_element(s)
        indicator[0].click()
        continue_button = driver.find_element_by_id("MainContent_btnContinue")
        continue_button.click()
        print('Enrolled!')

    driver.close()


if __name__ == "__main__":
    main()
