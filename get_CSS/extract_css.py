from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Step 1: Setup Chrome and open the page
driver = webdriver.Chrome()
driver.get("https://test-ipglobal.cd.xiaoxigroup.net/en")
time.sleep(5)  # Let the page load

# Step 2: Collect all tag.class combinations
selectors = []

elements = driver.find_elements(By.CSS_SELECTOR, "*")

for el in elements:
    tag = el.tag_name
    class_attr = el.get_attribute("class")
    if class_attr:
        class_list = class_attr.strip().split()
        for class_name in class_list:
            selectors.append({"tag": tag, "class": class_name, "selector": f"{tag}.{class_name}"})

# Step 3: Convert to DataFrame
df = pd.DataFrame(selectors).drop_duplicates()

# Step 4: Export to CSV
df.to_csv("css_selectors.csv", index=False)

# Step 5: Export to Excel
df.to_excel("css_selectors.xlsx", index=False)

print("Exported to css_selectors.csv and css_selectors.xlsx")

# Step 6: Close browser
driver.quit()
