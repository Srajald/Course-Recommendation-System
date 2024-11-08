from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Optional: Run in headless mode for faster execution
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the Analytics Vidhya Free Courses page
url = "https://courses.analyticsvidhya.com/pages/all-free-courses"

# Fetch the page content using Selenium
driver.get(url)
time.sleep(3)  # Wait for JavaScript to load content

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()  # Close the browser after fetching the page source

# Initialize lists to store course data
course_titles = []
course_links = []
course_ratings = []
course_reviews = []
course_lesson_counts = []
course_prices = []
course_images = []

# Extract course details
courses = soup.find_all("li", class_="course-cards__list-item")

for course in courses:
    # Extract title
    title = course.find("h3").get_text(strip=True) if course.find("h3") else "N/A"
    course_titles.append(title)
    
    # Extract link (appending base URL if needed)
    link = course.find("a", href=True)
    course_links.append("https://courses.analyticsvidhya.com" + link['href'] if link else "N/A")
    
    # Extract ratings
    rating_elements = course.find_all("i", class_="fa fa-star review__star")
    rating = len(rating_elements)  # Number of stars as the rating
    course_ratings.append(rating)
    
    # Extract number of reviews
    review_count = course.find("span", class_="review__stars-count")
    course_reviews.append(review_count.get_text(strip=True) if review_count else "N/A")
    
    # Extract lesson count
    lesson_count = course.find("span", class_="course-card__lesson-count")
    course_lesson_counts.append(lesson_count.get_text(strip=True) if lesson_count else "N/A")
    
    # Extract price
    price = course.find("span", class_="course-card__price")
    course_prices.append(price.get_text(strip=True) if price else "N/A")
    
    # Extract image URL
    image = course.find("img", class_="course-card__img")
    course_images.append(image['src'] if image else "N/A")

# Store data in a DataFrame
data = pd.DataFrame({
    "Title": course_titles,
    "Link": course_links,
    "Rating": course_ratings,
    "Reviews": course_reviews,
    "Lesson Count": course_lesson_counts,
    "Price": course_prices,
    "Image URL": course_images
})

# Save data to JSON and CSV files
data.to_csv("analytics_vidhya_courses.csv", index=False)
data.to_json("analytics_vidhya_courses.json", orient="records", lines=True)

print("Data saved to analytics_vidhya_courses.csv and analytics_vidhya_courses.json")
