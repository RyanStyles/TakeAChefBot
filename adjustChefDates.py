# TO DO
# Make it work for more than 3 months in advance by clicking arrow
# Docs; how to use / what to change, only works on Edge, need Edge driver, session cookie is optional, if it blows up on a certain line try adding a sleep() before that line because selenium is sometimes too fast for its own good
# Change commented code to debug mode
# Change script name
# Sanity check / boundaries (make sure dates aren't negative, zero, or more than 31)
# Run selenium phantom headless in background
# Check if login worked before proceeding
# Properly comment code

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from getpass import getpass

###############################################

PHPSESSID_cookie = "" # Can use this instead of logging in with creds every time; obtain from your browser after logging in manually

year = 2022 # choose a year
month = 11 # choose a month

# Choose individual days and/or a date range
individualDays = [] # comma separated list of individual dates
dateRange = [27, 30] # start date and end date

freeForLunch = False # we are FREE for lunch
freeForDinner = False # we are NOT FREE for dinner

###############################################

if type(individualDays) is not list:
    print("ERROR: individualDays must be a list!")
    quit()
if type(dateRange) is not list or len(dateRange) != 2:
    print("ERROR: dateRange must be a list containing the start date and end date, e.g. [1, 5]")
    quit()

days = []
for day in individualDays:
    if type(day) is int and day >= 1 and day <= 31:
        days.append(day)
    else:
        print("ERROR: All list elements in individualDays must be type int and values between 1-31!")
        quit()
for day in range(dateRange[0], dateRange[1]+1):
    if type(day) is int and day >= 1 and day <= 31:
        days.append(day)
    else:
        print("ERROR: dateRange must contain exactly two elements that both must be type int and values between 1-31!")
        quit()

options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

if PHPSESSID_cookie == "":
    # Ask for creds
    email = input("\nEnter your Take A Chef email: ", )
    password = getpass("Enter your password: ")
    # Log into site with creds
    driver = webdriver.Edge(options=options)
    driver.get("https://www.takeachef.com/en-us/user/signin")
    driver.find_element(By.ID, "form_users_sign_in_use_email").send_keys(email)
    driver.find_element(By.ID, "form_users_sign_in_use_password").send_keys(password)
    driver.find_element(By.ID, "form_users_sign_in_action").click()
else:
    # Log into site using session cookie
    driver.add_cookie({"name": "PHPSESSID", "value":PHPSESSID_cookie})
    driver = webdriver.Edge(options=options)

driver.get("https://www.takeachef.com/en-us/extranet/chefs/schedule")
driver.maximize_window()

#sleep(1)

# You know that the current month is div[0], next month is div[1], etc
today = datetime.now()
# FUTURE WORK: Make script work with spelling out months
#currentMonthFullName = today.strftime("%b") # January
#currentMonthAbbreviatedName = today.strftime("%b") # Jan
currentMonthNumber = int(today.strftime("%m"))
if month == currentMonthNumber:
    XPATH_Month_Index = 1
else:
    currentMonthNumber += 1
    if currentMonthNumber == 13:
        currentMonthNumber = 1
    if month == currentMonthNumber:
        XPATH_Month_Index = 2
    
    else:
        currentMonthNumber += 1
        if currentMonthNumber == 13:
            currentMonthNumber = 1
        if month == currentMonthNumber:
            XPATH_Month_Index = 3
        else:
            print("FUTURE WORK: Make the script work with months 3+ in advance of current date")
            exit()

# Total offset = 7 + day + 1st day of month day of week offset
firstDayOfMonthDayOfWeek = (datetime.date(datetime(year, month, 1)).weekday()+1)%7
#print("DAY OF WEEK: ", firstDayOfMonthDayOfWeek)
for day in days:
#    print("DAY: {}".format(day))
    XPATH_Day_Index = firstDayOfMonthDayOfWeek + 7 + day

    XPATH_Expression = "/html/body/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div["+str(XPATH_Month_Index)+"]/div[2]/div["+str(XPATH_Day_Index)+"]/span[1]"
    driver.find_element(By.XPATH, XPATH_Expression).click()

    # Before clicking, need to check what current value is
    isLunchSelected = driver.find_element(By.ID, "selected_day_slot_lunch").is_selected()
#    print("IS LUNCH SELECTED: ", isLunchSelected)
    isDinnerSelected = driver.find_element(By.ID, "selected_day_slot_dinner").is_selected()
#    print("IS DINNER SELECTED: ", isDinnerSelected)

    # Check if box should be clicked or not
    while (isLunchSelected and not freeForLunch) or (not isLunchSelected and freeForLunch):
#        print("Clicking lunch button...")
        driver.find_element(By.ID, "selected_day_slot_lunch").click()
        sleep(1)
        driver.find_element(By.XPATH, XPATH_Expression).click()
        isLunchSelected = driver.find_element(By.ID, "selected_day_slot_lunch").is_selected()
#        print("IS LUNCH SELECTED: ", isLunchSelected)
    while (isDinnerSelected and not freeForDinner) or (not isDinnerSelected and freeForDinner):
#        print("Clicking dinner button...")
        driver.find_element(By.ID, "selected_day_slot_dinner").click()
        sleep(1)
        driver.find_element(By.XPATH, XPATH_Expression).click()
        isDinnerSelected = driver.find_element(By.ID, "selected_day_slot_dinner").is_selected()
#        print("IS DINNER SELECTED: ", isDinnerSelected)

#sleep(5)
print("\nAvailability successfully changed for the following dates in {}/{}: {}!\n".format(month, year, ', '.join(map(str, days))))
driver.close()