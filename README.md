"""Complete description can be found in the file: CodeHSProgrammingChallenge-WikipediaPhilosophy.pdf"""  

The purpose of this project is to get to the Philosophy article on wikipedia starting
from an intitial article. This solution uses a Python script that fetches the initial wikipedia page with urllib2 and follows the first link until reaching Philosophy by parsing the HTML with BeautifulSoup. Only pages that have not been seen before, and are main wikipedia articles are followed. This script prints out the path taken from the first article to Philosophy if it converges and the number of articles in the path to Philosophy.
