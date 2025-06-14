import requests
from bs4 import BeautifulSoup
import lxml
import csv
import os


def main(page):
    """
    Scrape job listings from Wuzzuf.net for the specified job title.
    
    Args:
        page: The requests response object containing the webpage content
    """
    src = page.content
    soup = BeautifulSoup(src, 'lxml')

    job_details = []

    # Find all relevant job information
    job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
    companys_name = soup.find_all('a', {'class': 'css-17s97q8'})
    job_type = soup.find_all('a', {'class': 'css-n2jc4m'})
    location = soup.find_all('span', {'class': 'css-5wys0k'})
    job_posted = soup.find_all('div', {'class': 'css-do6t5g'})
    

    # Get the minimum length to avoid index errors
    min_length = min(len(job_titles), len(companys_name), len(job_type), 
                    len(location), len(job_posted))

    # Extract job details
    for i in range(min_length):
        try:
            job_details.append({
                'Job Title': job_titles[i].text.strip(),
                'Company Name': companys_name[i].text.strip(),
                'Job Type': job_type[i].text.strip(),
                'Location': location[i].text.strip(),
                'Job Posted': job_posted[i].text.strip()
            })
        except (IndexError, AttributeError) as e:
            print(f"Error processing job {i}: {str(e)}")
            continue
    
    if not job_details:
        print("No job listings found!")
        return

    # Save to CSV file
    output_path = os.path.join(os.path.expanduser('~'), 'Documents', 'result.csv')
    keys = job_details[0].keys()
    
    with open(output_path, 'w', newline='', encoding='utf-8') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(job_details)
        print('File created successfully at:', output_path)


if __name__ == "__main__":
    try:
        job = input('Enter Job Title: ')
        # Replace spaces with plus signs for URL
        job = job.replace(' ', '+')
        
        page = requests.get(f"https://wuzzuf.net/search/jobs/?q={job}&a=navbl")
        page.raise_for_status()  # Raise an exception for bad status codes
        
        main(page)
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        