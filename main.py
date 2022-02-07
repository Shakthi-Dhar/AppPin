# Import all the required libraries
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from appium import webdriver
import time
import csv

# Set the file name to which the data is to be stored/updated
file_name = "data/Weather.csv"
# Initialize the webdriver parameters
desired_cap = {
    "deviceName": "Y9_2019",
    "udid": "DHE4C18C11000809",
    "platformName": "Android",
    "platformVersion": "9",
    "appPackage": "com.android.vending",
    "appActivity": "com.google.android.finsky.activities.MainActivity"
}
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
wait = WebDriverWait(driver, 10)
# An empty list to keep track of the collected app's name
app_rank_list = []


# Function to simulate swipe up action in the app
def swipe():
    # Drags the fourth element from its position to that of the second element
    element_5 = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[1]/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[5]')))
    # element_4 = wait.until(EC.presence_of_element_located((By.XPATH,
    #                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[1]/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[4]')))
    element_2 = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[1]/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]')))
    driver.drag_and_drop(element_5, element_2)
    # driver.drag_and_drop(element_4, element_2)


# Function to get the app data
def app_info(app_element):
    # Collect the app name, category and size from the home page containing the list of apps
    main_page_content = app_element.find_element(By.CLASS_NAME, 'android.view.ViewGroup').find_element(By.CLASS_NAME,
                                                                                                       'android.view.View')
    name_and_category_and_size = main_page_content.get_attribute('content-desc').splitlines()
    # Collect the app rank from the home page containing the list of apps
    rank = int(app_element.find_element(By.CLASS_NAME, 'android.widget.TextView').get_attribute('text'))
    # Formatting the app name, category and size
    name = name_and_category_and_size[0][5:]
    category = name_and_category_and_size[1]
    stars = name_and_category_and_size[2][13:]
    size = name_and_category_and_size[-1]
    if size == "Editors' Choice":
        size = name_and_category_and_size[-2]
    # Click to open the detailed app page
    app_element.click()
    time.sleep(1)
    try:
        dev_by = wait.until(EC.presence_of_element_located((By.XPATH,
                                                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView'))).get_attribute(
            'text')
    except:
        dev_by = None
    try:
        # Identify the horizontal row element containing the data such as stars, reviews, downloads, and rated for
        horizontal_row = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]')))
        row_elements = horizontal_row.find_elements(By.CLASS_NAME, 'android.widget.TextView')
        # Collect all these row values in an empty list
        row_data = []
        for row_element in row_elements:
            row_data.append(row_element.get_attribute('text'))
        # Formatting the app stars, reviews, downloads, rated for content from the row_data list
        reviews = row_data[1]
        downloads = row_data[row_data.index('Downloads') - 1]
        rated_for = row_data[-1][10:]
        try:
            reviews = reviews.replace(' reviews', '')
        except:
            pass
        try:
            rated_for = rated_for.replace('\xa0 ', '')
        except:
            pass

    except:
        try:
            # Identify the horizontal row element containing the data such as stars, reviews, downloads, and rated for
            horizontal_row = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]')))
            row_elements = horizontal_row.find_elements(By.CLASS_NAME, 'android.widget.TextView')
            # Collect all these row values in an empty list
            row_data = []
            for row_element in row_elements:
                row_data.append(row_element.get_attribute('text'))
            downloads = row_data[row_data.index('Downloads') - 1]
            rated_for = row_data[-1][10:]
            reviews = None
            try:
                rated_for = rated_for.replace('\xa0 ', '')
            except:
                pass
        except:
            # If unable to identify the horizontal row element then it's probably because the app is installed in device
            # stars = None
            reviews = None
            downloads = None
            rated_for = None

    # Store the collected app content as a list
    if reviews == "Downloads":
        reviews = None
    app_content = [rank, name, dev_by, category, size, stars, reviews, downloads, rated_for]
    # If the app name is not in the list, then it's a new app data and hence update the data sheet
    if rank not in app_rank_list:
        # Append/Update the CSV file with the app content
        with open(file_name, 'a', newline='', encoding='utf-8') as csv_obj:
            writer_object = csv.writer(csv_obj)
            writer_object.writerow(app_content)
            csv_obj.close()
        # Update app list with the newly added apps name
        app_rank_list.append(rank)
        # Print the collected app information on the terminal
        print("Rank: ", rank, "\nApp Name: ", name, "\nDeveloper: ", dev_by, "\nCategory: ", category, "\nSize: ", size, "\nStar Rating: ",
              stars,
              "\nReviews: ", reviews, "\nDownloads: ", downloads, "\nRated for: ", rated_for)
        print(u'\u2500' * 100)


# Function to begin the search from the opened screen
def begin_search(number_of_times):
    # First element special case, as the top list button on Google Play Store has same XPATH as first app in the list
    app_element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                             '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[1]/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]')))
    # Call the app_info() function to collect the app data
    app_info(app_element)
    # Go back to home page containing the list of apps
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//android.widget.ImageButton[@content-desc="Navigate up"]'))).click()

    # Loop through the hope page containing the list of apps for the given number of time
    for flag in range(number_of_times):
        # At maximum there are 12 or 14 apps (depending on screen size) in the page at a time, so loop through each app
        for i in range(2, 14):
            try:
                # XPATH for the app element in the page visible
                app_element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[1]/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[' + str(
                                                                             i) + ']')))
                # Call the app_info() function to collect the app data
                app_info(app_element)
                # Go back to home page containing the list of apps
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//android.widget.ImageButton[@content-desc="Navigate up"]'))).click()
            except:
                pass
        # Swipe up for next set of app data
        swipe()


# Main function for the Scrapping code
if __name__ == '__main__':
    # Generate a CSV File with the required columns
    csv_file = open(file_name, "w", newline='', encoding='utf-8')
    writer = csv.DictWriter(csv_file,
                            fieldnames=["Rank", "Name", "Developer", "Category", "Size", "Star Rating", "Reviews", "Downloads",
                                        "Rated for"])
    writer.writeheader()
    csv_file.close()

    # Click on Apps button at the bottom
    wait.until(EC.presence_of_element_located((By.XPATH,
                                               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]'))).click()
    # Click on Top charts button at the top
    wait.until(EC.presence_of_element_located((By.XPATH,
                                               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.TextView[2]'))).click()

    # Click on Categories
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//android.widget.Button[@content-desc="Categories – double-tap to change the filter"]'))).click()
    # Swipe for more Categories
    cat_1 = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.LinearLayout[@content-desc="Entertainment"]')))
    cat_2 = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.LinearLayout[@content-desc="Watch apps"]')))
    driver.drag_and_drop(cat_1, cat_2)
    # Click on the Category you want
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//android.widget.LinearLayout[@content-desc="Weather"]'))).click()

    # for i in range(0, 40):
    #     swipe()
    #     print(i)

    # Begin the search with all categories for n pages (here: 10)
    begin_search(400)

