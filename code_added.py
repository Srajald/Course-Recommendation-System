import json
import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os

with open("C:\\Users\\LENOVO\\Desktop\\Course_Recomender\\analytics_vidhya_courses_new.json", "r") as file:
    data = json.load(file)

# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


descriptions = []
curricula = []

max_retries = 3  

for course in data:
    full_link = course.get("Link", "N/A")
    description_text = "N/A"
    curriculum_text = "N/A"

    if full_link != "N/A":
        attempt = 0
        while attempt < max_retries:
            try:
                driver.get(full_link)
                
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                course_soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                description_section = course_soup.find("section", class_="rich-text")
                if description_section:
                    container = description_section.find("div", class_="rich-text__container")
                    if container:
                        wrapper = container.find("div", class_="rich-text__wrapper")
                        if wrapper:
                            article = wrapper.find("article", class_="section__content")
                            if article:
                                section_body = article.find("section", class_="section__body")
                                if section_body:
                                  
                                    description_text_tag = section_body.find("p")
                                    if description_text_tag:
                                        description_text = description_text_tag.get_text(strip=True)
                                    else:
                                        print(f"Description <span> tag not found for {full_link}")
                                else:
                                    print(f"section_body not found for {full_link}")
                            else:
                                print(f"Article content wrapper not found for {full_link}")
                        else:
                            print(f"Wrapper not found for {full_link}")
                    else:
                        print(f"Container not found for {full_link}")
                else:
                    print(f"Description section not found for {full_link}")

                curriculum_section = course_soup.find("div", class_="course-curriculum__container")
                curriculum_content = []
                
                if curriculum_section:
                    chapters = curriculum_section.find_all("li", class_="course-curriculum__chapter")
                    
                   
                    for chapter in chapters:
                        chapter_title = chapter.find("h5", class_="course-curriculum__chapter-title")
                        chapter_text = chapter_title.get_text(strip=True) if chapter_title else "Untitled Chapter"
                        
                       
                        lessons = chapter.find_all("span", class_="course-curriculum__chapter-lesson")
                        lesson_texts = [lesson.get_text(strip=True) for lesson in lessons]
                        
                        
                        curriculum_content.append(f"{chapter_text}: " + ", ".join(lesson_texts))
                    
                    curriculum_text = " | ".join(curriculum_content)  
                else:
                    print(f"Curriculum section not found for {full_link}")

               
                break
            
            except (TimeoutException, NoSuchElementException, WebDriverException) as e:
                print(f"Attempt {attempt + 1} - Error fetching data for {full_link}: {e}")
                
                
                screenshot_path = os.path.join(os.getcwd(), f"screenshot_{attempt + 1}_{course['Link'].split('/')[-1]}.png")
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved at {screenshot_path} for debugging.")
                
                attempt += 1
                time.sleep(2)  

            if attempt == max_retries:
                print(f"Failed to fetch data for {full_link} after {max_retries} attempts.")

    
    descriptions.append(description_text)
    curricula.append(curriculum_text)

driver.quit()

for i, course in enumerate(data):
    course["Description"] = descriptions[i]
    course["Curriculum"] = curricula[i]

df = pd.DataFrame(data)
df.to_csv("updated_courses_with_details.csv", index=False)

print("Data extraction complete. Saved to updated_course_with_details.csv")
