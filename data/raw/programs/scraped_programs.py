from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import random
import re

def clean_text(text):
    """Cleans extracted text by removing extra spaces and escape sequences."""
    text = text.replace('\n', ' ').replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def scrape_page_content(url):
    """Scrapes page title, and course links from Bournemouth University."""
    driver = webdriver.Chrome()  # Launch Chrome WebDriver
    driver.get(url)
    
    # Introduce a random delay to prevent overwhelming the server
    sleep_time = random.randint(5, 10)
    print(f"Waiting for {sleep_time} seconds before scraping {url}...")
    time.sleep(sleep_time)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract all courses
    course_section = soup.find_all("div", class_="related-items view-mode-summary-only")
    
    courses = []
    for section in course_section:
        course_links = section.find_all("a")
        for course in course_links:
            title = clean_text(course.get_text(strip=True))
            link = course["href"] if "http" in course["href"] else f"https://www.bournemouth.ac.uk{course['href']}"
            courses.append({"title": title, "url": link})
    
    driver.quit()
    return courses

def scrape_all_courses():
    """Scrapes all courses and saves them to a CSV file."""
    URLS = {
        "undergraduate": "https://www.bournemouth.ac.uk/study/undergraduate/courses/undergraduate-course-list",
        "postgraduate": "https://www.bournemouth.ac.uk/study/postgraduate-research/postgraduate-research-courses"
    }

    all_courses = []
    
    for category, url in URLS.items():
        print(f"\nScraping {category} courses...")
        courses = scrape_page_content(url)
        for course in courses:
            course["category"] = category
        all_courses.extend(courses)
    
    # Save courses to CSV
    with open('bournemouth_courses.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Course Title', 'Course URL'])
        
        for course in all_courses:
            writer.writerow([course['category'], course['title'], course['url']])

    print(f"\n✅ Scraping completed! {len(all_courses)} courses saved to 'bournemouth_courses.csv'.")

# Run the scraper
scrape_all_courses()
