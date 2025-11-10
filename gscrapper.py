print("Initiating... please wait.\n")

import requests
import csv
import re
import random
import time
import pandas as pd
from sys import exit
from bs4 import BeautifulSoup

# ===== DEFINE FUNCTIONS =====

search_from, URL_edit= "", ""

def wait():
	print("Waiting for a few secs...")
	time.sleep(random.randrange(1, 6))
	print("Waiting done. Continuing...\n")

def checkPage():
	global search_from
	if "scholar.google.com/scholar?" in URL_input:
		search_from = "Google Scholar"
		print("Input is from: Google Scholar (Search Results).\n")
	elif "scholar.google.com/citations?" in URL_input:
		search_from = "Google Scholar Profile"
		print("Input is from: Google Scholar (Author Profile).\n")
	else:
		print("Page URL undefined.\n")
		print("Please use one of these URL formats:")
		print("  - Google Scholar Search: https://scholar.google.com/scholar?q=...")
		print("  - Google Scholar Profile: https://scholar.google.com/citations?user=...\n")
		exit()


# ===== GETTING AND SETTING THE URL =====

URL_input = input("Please paste search URL and press Enter:")
URL_ori = URL_input
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/15.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20210916 Firefox/95.0',
})
checkPage()


# ===== MAIN FRAMEWORK =====

# ===== CODE FOR GOOGLE SCHOLAR =====

if search_from == "Google Scholar":

	try:

		# SETTING UP THE CSV FILE

		outfile = open("scrapped_gscholar.csv","w",newline='',encoding='utf-8')
		writer = csv.writer(outfile)
		df = pd.DataFrame(columns=['Title','Links','References'])

		# SETTING & GETTING PAGE NUMBER

		page_num = 0
		URL_edit = str(URL_ori + "&start=" + str(page_num))

		page = requests.get(URL_edit, headers=headers, timeout=None)
		soup = BeautifulSoup(page.content, "html.parser")
		wait()

		search_results = soup.find_all("div", class_="gs_ab_mdw")[1].text

		if "About" in search_results:
			search_results_split = search_results.split("results")[0].split("About")[1]
		elif "results" in search_results:
			search_results_split = search_results.split("results")[0]
		else:	
			search_results_split = search_results.split("result")[0]

		search_results_num = int(''.join(filter(str.isdigit, search_results_split)))
		page_total_num = int(search_results_num / 10) + 1
		print(f"Total page number: {page_total_num}")
		print(f"Total search results: {search_results_num}.\n")

	except AttributeError:

		print("Opss! ReCaptcha is probably preventing the code from running.")
		print("Please consider running in another time.\n")
		exit()

	wait()

	# EXTRACTING INFORMATION

	for i in range(page_total_num):

		# SETTING UP URL SECOND TIME

		page_num_up = page_num + i
		print(f"Going to page {page_num_up}.\n")
		URL_edit = str(URL_ori + "&start=" + str(page_num_up) + "0")

		headers = requests.utils.default_headers()
		headers.update({
	    	'User-Agent': 'Mozilla/15.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20210916 Firefox/95.0',
			})
		
		page = requests.get(URL_edit, headers=headers, timeout=None)
		soup = BeautifulSoup(page.content, "html.parser")
		wait()

		results = soup.find("div", id="gs_res_ccl_mid")
		
		# EXTRACTING INFORMATION

		try:

			job_elements = results.find_all("div", class_="gs_ri")
			for job_element in job_elements:

				ref_element = job_element.find("div", class_="gs_a").text
				links = job_element.find("a") 
				link_url = links["href"]
				title_element = links.text.strip()

				print(title_element)
				print(link_url)
				print(ref_element)
				print()

				df2 = pd.DataFrame([[title_element, link_url, ref_element]], columns=['Title','Links','References'])
				df = pd.concat([df, df2], ignore_index=True)

		except AttributeError:
			print("Opss! ReCaptcha is probably preventing the code from running.")
			print("Please consider running in another time.\n")
			exit()

	df.index += 1
	df.to_csv('scrapped_gscholar.csv',encoding='utf-8')
	outfile.close()

# ===== CODE FOR GOOGLE SCHOLAR PROFILE =====

elif search_from == "Google Scholar Profile":

	try:

		# SETTING UP THE CSV FILE

		outfile = open("scrapped_gscholar_profile.csv","w",newline='',encoding='utf-8')
		writer = csv.writer(outfile)
		df = pd.DataFrame(columns=['Title','Links','References'])

		print("Fetching author profile page...\n")

		# First, get the page to check author name and total articles
		page = requests.get(URL_ori, headers=headers, timeout=None)
		soup = BeautifulSoup(page.content, "html.parser")
		wait()

		# Check if we can access the page
		author_name = soup.find("div", id="gsc_prf_in")
		if author_name:
			print(f"Author: {author_name.text}\n")
		
		# Now fetch with pagination to get ALL articles (up to 100 per page)
		# Google Scholar allows pagesize up to 100
		all_articles_collected = False
		cstart = 0
		pagesize = 100
		total_articles = 0

		while not all_articles_collected:
			
			# Build URL with pagination
			if "?" in URL_ori:
				URL_paginated = f"{URL_ori}&cstart={cstart}&pagesize={pagesize}"
			else:
				URL_paginated = f"{URL_ori}?cstart={cstart}&pagesize={pagesize}"
			
			print(f"Fetching articles {cstart} to {cstart + pagesize}...")
			page = requests.get(URL_paginated, headers=headers, timeout=None)
			soup = BeautifulSoup(page.content, "html.parser")
			wait()

			# Find all article rows
			article_rows = soup.find_all("tr", class_="gsc_a_tr")
			
			if not article_rows:
				if cstart == 0:
					print("No articles found. The page might be protected or the structure has changed.")
					print("Try accessing the page in a browser first to check if CAPTCHA is required.\n")
					exit()
				else:
					# No more articles to fetch
					all_articles_collected = True
					break

			print(f"Found {len(article_rows)} articles on this page.\n")

			# EXTRACTING INFORMATION

			for row in article_rows:
				try:
					# Get title and link
					title_cell = row.find("td", class_="gsc_a_t")
					if title_cell:
						link_element = title_cell.find("a", class_="gsc_a_at")
						if link_element:
							title = link_element.text.strip()
							link_href = link_element.get("href", "")
							link_url = "https://scholar.google.com" + link_href if link_href else "N/A"
						else:
							continue
					else:
						continue

					# Get authors and publication info
					author_cell = row.find_all("div", class_="gs_gray")
					ref_parts = []
					for cell in author_cell:
						if cell.text.strip():
							ref_parts.append(cell.text.strip())
					ref_element = ", ".join(ref_parts) if ref_parts else "N/A"

					print(title)
					print(link_url)
					print(ref_element)
					print()

					df2 = pd.DataFrame([[title, link_url, ref_element]], columns=['Title','Links','References'])
					df = pd.concat([df, df2], ignore_index=True)
					total_articles += 1

				except AttributeError as e:
					print(f"Error extracting article info: {e}")
					continue

			# Check if we need to fetch more pages
			# If we got fewer articles than pagesize, we've reached the end
			if len(article_rows) < pagesize:
				all_articles_collected = True
			else:
				cstart += pagesize

			# Check if we need to fetch more pages
			# If we got fewer articles than pagesize, we've reached the end
			if len(article_rows) < pagesize:
				all_articles_collected = True
			else:
				cstart += pagesize

		if len(df) == 0:
			print("No articles were extracted. The page structure might have changed.")
			exit()

		print(f"\nTotal articles extracted: {total_articles}\n")

	except Exception as e:
		print(f"Error: {e}")
		print("Please check your internet connection or try again later.\n")
		exit()

	df.index += 1
	df.to_csv('scrapped_gscholar_profile.csv', encoding='utf-8')
	outfile.close()

# END OF PROGRAM

print("Job finished, Godspeed you! Cite us.")
