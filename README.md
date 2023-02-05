# cityquiz-io-city-enterer

Enter a list of cities into https://cityquiz.io/quizzes/usa automatically

### Stuff needed:

1. Firefox

2. geckodriver for Firefox https://github.com/mozilla/geckodriver/releases
   * For Windows, you'll probably want the win64 download. Put the extracted exe somewhere in the file system and add its path to your PATH system variable

3. Python 3.?

4. Python tools: Selenium, seleniumwire (install using pip)

### Usage

Place the cityioscript.py script into any folder. In the same folder, place a "cities.txt" file with your list of cities. These will be formatted like the cities.txt file provided. Run the python script (double click or run via command line) and a new browser window will open and run the script (it may take a few minutes if you have thousands of entries).

Questions/suggestions: in Issues tab or message stupiddrew9#1349 on Discord
