import urllib2 as urlLib
import sys
import socket
from bs4 import BeautifulSoup
from functools import reduce

MAX_HOPS = 100
WIKI_URL_PREFIX = 'http://en.wikipedia.org'
TARGET_SUFFIX = '/wiki/Philosophy'

def findPhilosophyPath(start_page):
	path_array = []
	link_suffix = start_page
	path_array.append(link_suffix)

	for x in xrange(0,MAX_HOPS):
		if(link_suffix == TARGET_SUFFIX):
			break
		
		try:
			# Create a URL: 'http://en.wikipedia.org' + page_name
			link = WIKI_URL_PREFIX + link_suffix
			html_content = urlLib.urlopen(link).read()
		except urlLib.URLError as e:
			print ("Broken link")
			break
		except socket.timeout as e:
			print "Timed out trying to connect to link"

		b_soup = BeautifulSoup(html_content)
		
		# Main content block of the Wiki entry
		content_block = b_soup.find(id="mw-content-text")
		
		# Take all non-nested paragraphs and unordered lists
		paragraphs_lists = content_block.find_all('p', recursive=False) + content_block.find_all('ul', recursive=False)
		
		# First create a list of all the links contained in each paragraph and list
		# Reduce this list of lists using the reduceLinksList method into one List
		# containing all the links
		links_array = reduce( reduceLinksList, map(findLinks, paragraphs_lists))


		for l in links_array:
			link_suffix = str(l.get('href'))
			# Continue searching through links until a link that has not been followed
			# before and is a main wikipedia article is found
			if(link_suffix not in path_array 
				and '/wiki/' in link_suffix 
				and ':' not in link_suffix 
				and '#' not in link_suffix 
				and "wiktionary" not in link_suffix):
				break
		
		path_array.append(link_suffix)
	return path_array

def findLinks(paragraph):
	return paragraph.find_all('a')

def reduceLinksList(l_first,l_second):
	return l_first+l_second

def printPhilosophyPath(start_page):
	start_page_suffix = start_page[start_page.find('/wiki'):]
	if(start_page_suffix == TARGET_SUFFIX):
		print start_page
		print "0 hops"
	else:
		path_array = findPhilosophyPath(start_page_suffix)
		path_length = len(path_array)
		
		if(path_length > 1 and path_array[-1] == TARGET_SUFFIX):
			for suffix in path_array:
				print WIKI_URL_PREFIX + suffix
			print str(path_length-1) + " hops"
		else:
			print "Unable to find path to Philosophy"

printPhilosophyPath(sys.argv[1])



