import webbrowser
import codecs
import time
import warnings
from urllib.parse import unquote
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

url = "https://cityquiz.io/quizzes/usa"
txtfile = "cities.txt"
States = ["District of Columbia", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Rhode Island", "South Carolina", "South Dakota", "West Virginia", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming"]
Cities = []
CitiesNotAdded = []

## I use a lot of selenium find element methods here, which is bad, but who wants these warnings printed every time
warnings.filterwarnings("ignore", category=DeprecationWarning) 

## open browser
print("Opening browser")
driver = webdriver.Firefox()
driver.get(url)

## find city/state fields in cityquiz.io
cityInput = driver.find_element(By.ID, "city-input")
stateInput = Select(driver.find_element(By.ID, "state-input"))

## open provided text file
with codecs.open(txtfile, encoding='utf-8') as f:
    for line in f:
        Cities.append(line)
Cities.reverse()

## loop through the provided list, strip info to just city/state, and enter into site
print("Entering data")
index = -1
for line in Cities:
    index += 1
    line = line.strip()
    cityState = line[0:line.rindex('(') - 1]
    ## put the corrected record back in the array for later
    Cities[index] = cityState

    ## loop through states to find correct one
    for state in States:
        if cityState.endswith(state):
            ## once state is found, parse the city
            city = cityState[0:cityState.rindex(state)]
            
            ## input parsed city/state into the page and press enter
            cityInput.send_keys(city)
            stateInput.select_by_visible_text(state)
            cityInput.send_keys(Keys.ENTER)

            ## go to next record in Cities array
            break

###########
## This section is for verifying all cities entered went through correctly.
## It could easily break in the future so if this breaks you can just remove this whole section

## This is the terrible solution for opening the list of all entered cities
if len(Cities) > 20:
    print("Waiting to check for any missed cities...")
    ## jankiest solution: click the "show all" button to get the list of entered cities, then compare it with list in code
    ## opening this can take some time for large lists... I don't know if I can somehow wait right until I know it's open
    ## so I'll just wait 20 seconds and then hope it has loaded by then 
    unopenedListenedCities = driver.find_elements(By.XPATH, "//*[@class='my-cities-list']")[0]
    div = unopenedListenedCities.find_element(By.XPATH, "..")
    button = div.find_element(By.XPATH, './/button[@class="align-center"]').click()
    time.sleep(20)

## Get the list of cities now that the entire list is displayed
openedListenedCities = driver.find_elements(By.XPATH, "//*[@class='my-cities-list']")[0]
divAgain = openedListenedCities.find_element(By.XPATH, "..").text
## Put it into a list and make it look like the one made from the text file above
citiesList = divAgain.split('\n')
citiesList = citiesList[1:len(citiesList) - 1]
for index in range(len(citiesList)):
    citiesList[index] = citiesList[index][0:citiesList[index].rindex('(') - 1]

## Check if the entered cities actually made it in the list
for cityEntered in Cities:
    if cityEntered not in citiesList:
        CitiesNotAdded.append(cityEntered)

print(str(len(CitiesNotAdded)) + " cities missed!")
for notAdded in CitiesNotAdded:
    print(notAdded)
## End of verification section
###########
