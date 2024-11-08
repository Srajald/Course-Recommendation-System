
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Analytics Vidhya Free Courses page
url = "https://courses.analyticsvidhya.com/pages/all-free-courses"

# Step 1: Make an HTTP GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Initialize lists to store course data
course_titles = []
course_descriptions = []
course_links = []
course_tags = []  # Add tags if available on the site

# Step 4: Extract course details
# This part depends on the HTML structure, here’s a general example.
# Inspect the page to find the HTML structure for courses

# Example assuming each course is in a <div> with class "course-card"
courses = soup.find_all("div", class_="course-card")

for course in courses:
    # Extract title
    title = course.find("h3").get_text(strip=True) if course.find("h3") else "N/A"
    course_titles.append(title)
    
    # Extract description
    description = course.find("p").get_text(strip=True) if course.find("p") else "N/A"
    course_descriptions.append(description)
    
    # Extract course link
    link = course.find("a", href=True)
    course_links.append(link['href'] if link else "N/A")
    
    # Extract tags or topics if available
    tags = course.find("div", class_="tags").get_text(strip=True) if course.find("div", class_="tags") else "N/A"
    course_tags.append(tags)

# Step 5: Store data in a DataFrame
data = pd.DataFrame({
    "Title": course_titles,
    "Description": course_descriptions,
    "Link": course_links,
    "Tags": course_tags
})

# Step 6: Save data to JSON and CSV files
data.to_csv("analytics_vidhya_courses.csv", index=False)
data.to_json("analytics_vidhya_courses.json", orient="records", lines=True)

print("Data saved to analytics_vidhya_courses.csv and analytics_vidhya_courses.json")
