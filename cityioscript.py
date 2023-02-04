import webbrowser
import codecs
import time
from urllib.parse import unquote
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

url = "https://cityquiz.io/quizzes/usa"
txtfile = "cities.txt"
States = ["District of Columbia", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Rhode Island", "South Carolina", "South Dakota", "West Virginia", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming"]
Cities = []
CitiesNotAdded = []

## open browser
driver = webdriver.Firefox()
driver.get(url)

## find city/state fields in cityquiz.io
cityInput = driver.find_element_by_id("city-input")
stateInput = Select(driver.find_element_by_id("state-input"))

## open provided list
with codecs.open(txtfile, encoding='utf-8') as f:
    for line in f:
        Cities.append(line)
Cities.reverse()

## take the list provided and strip away population info
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
for request in driver.requests:
    if request.response:
        if "cityquiz.io/api/cities" in request.url:
            city = unquote(request.url[(request.url.index("&query=") + 7):request.url.index("&dropdown=")])
            state = unquote(request.url[(request.url.index("&dropdown=") + 10):])
            combined = city + " " + state
            if combined not in Cities:
                CitiesNotAdded.append(combined)
            if "\"cities\": []" in str(request.response.body):
                CitiesNotAdded.append(combined)

##dead code for checking if the list of cities increased after entering a city
##existingCities = driver.find_elements_by_xpath("//*[@class='my-cities-list']")
##print(existingCities[0].get_attribute('start'))

print(str(len(CitiesNotAdded)) + " cities missed!")
for notAdded in CitiesNotAdded:
    print(notAdded)
## End of section
###########
