import webbrowser
import codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://cityquiz.io/quizzes/usa"
txtfile = "cities.txt"
States = ["District of Columbia", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Rhode Island", "South Carolina", "South Dakota", "West Virginia", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming"]
Cities = []

## open browser
driver = webdriver.Firefox()
driver.get(url)

## find city/state fields in cityquiz.io
cityInput = driver.find_element_by_id("city-input")
stateInput = driver.find_element_by_id("state-input")

## open provided list
with codecs.open(txtfile, encoding='utf-8') as f:
    for line in f:
        Cities.append(line)
Cities.reverse()

## take the list provided and strip away population info
for line in Cities:
    line = line.strip()
    cityState = line[0:line.rindex('(') - 1]
    print(cityState)
    for state in States:
        ## find correct state and parse the city
        if cityState.endswith(state):
            city = cityState[0:cityState.rindex(state)]
            ## input parsed city/state into the page and press enter
            cityInput.send_keys(city)
            stateInput.send_keys(state)
            cityInput.send_keys(Keys.ENTER)
            break
