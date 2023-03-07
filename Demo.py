import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
from tkinter import filedialog

from playwright.async_api import async_playwright
import asyncio
import csv
import os
from bs4 import BeautifulSoup, PageElement

filePath = os.path.abspath(os.path.dirname(__file__))

class AppScrape:

  def verify(self):
    user = self.entry_user.get()
    password = self.entry_password.get()
    passed = test(user, password)
    if passed:
      self.window.destroy()
      MasterPanel()
    elif user == "" or password == "":
      messagebox.showerror("Error", "Please fill all fields")
    else:
      messagebox.showerror("Error", "Invalid username or password")

  def __init__(self):
    
    self.window = tk.Tk()
    self.window.title("Login")
    self.window.geometry("800x500")
    self.window.configure(bg="#FCFCFC")
    self.window.resizable(False, False)
    center_window(self.window, 800, 500)

    # logo = read_image("GUI/build/assets/logo.png", (200, 200))

    # Frame Logo
    frame_logo = tk.Frame(self.window, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg="#3a7ff6")
    frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
    # label = tk.Label(frame_logo, image=logo, bg="#3a7ff6")
    # label.place(x=0, y=0, relwidth=1, relheight=1)

    # Frame Login
    frame_form = tk.Frame(self.window, bd=0, relief=tk.SOLID, bg="#FCFCFC")
    frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

    # Frame_form_top
    frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="black")
    frame_form_top.pack(side="top", fill=tk.X)
    title = tk.Label(frame_form_top, text="Login", font=("Times", 30), fg="#666a88", bg="#FCFCFC", pady=50)
    title.pack(expand=tk.YES, fill=tk.BOTH)

    # Frame_form_fill
    frame_form_fill = tk.Frame(frame_form, height= 50, bd=0, relief=tk.SOLID, bg="#FCFCFC")
    frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

    label_user = tk.Label(frame_form_fill, text="Username", font=("Times", 14), fg="#666a88", bg="#FCFCFC", anchor="w")
    label_user.pack(fill=tk.X, padx=20, pady=5)
    self.entry_user = tk.Entry(frame_form_fill, font=("Times", 14))
    self.entry_user.pack(fill=tk.X, padx=20, pady=10)

    label_password = tk.Label(frame_form_fill, text="Password", font=("Times", 14), fg="#666a88", bg="#FCFCFC", anchor="w")
    label_password.pack(fill=tk.X, padx=20, pady=5)
    self.entry_password = tk.Entry(frame_form_fill, font=("Times", 14))
    self.entry_password.pack(fill=tk.X, padx=20, pady=10)
    self.entry_password.config(show="*")

    button_login = tk.Button(frame_form_fill, text="Login", font=("Times", 14), bg="#3a7ff6", fg="#FCFCFC", bd=0, command=self.verify)
    button_login.pack(fill=tk.X, padx=20, pady=20)

    self.window.mainloop()
    
class MasterPanel:

  def startMainScrap(self):
    #Save combo box value
    state = self.state.get()
    #Save to file

    with open(os.path.join(filePath, "state.txt"), "w") as file:
      file.write(state)
    #Run the scraper
    startScrap()
    self.window.destroy()

  def select_file(self):
    self.file = filedialog.askdirectory()
    self.output_file.set(self.file)
    
  def __init__(self):
    
    self.window = tk.Tk()
    self.window.title("Foresclosure Data Scraper")
    self.window.geometry("800x500")
    self.window.configure(bg="#FCFCFC")
    self.window.resizable(False, False)
    center_window(self.window, 800, 500)

    # Frame Configs
    frame_Configs = tk.Frame(self.window, bd=0, width=300, relief=tk.SOLID, padx=5, pady=5, bg="#3a7ff6")
    frame_Configs.pack(side="left", expand=tk.NO, fill=tk.BOTH)

    title = tk.Label(frame_Configs, text="Please select the data to scrap", font=("Times", 14), fg="white", bg="#3a7ff6", pady=10)
    title.pack(expand=tk.YES, fill=tk.BOTH)

    state_lbl = tk.Label(frame_Configs, text="State", font=("Times", 12), fg="white", bg="#3a7ff6", pady=1, padx=5)
    state_lbl.pack(fill=tk.X, padx=10, pady=5)

    # State Combobox
    self.state = tk.StringVar()
    state_combo = ttk.Combobox(frame_Configs, state="readonly", textvariable=self.state, font=("Times", 12), width=10, height=10)
    state_combo['values'] = ("Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming")
    state_combo.current(0)
    state_combo.pack(fill=tk.X, padx=10, pady=10)

    # # Output File Label
    # output_lbl = tk.Label(frame_Configs, text="Output File", font=("Times", 12), fg="white", bg="#3a7ff6", pady=1, padx=5)
    # output_lbl.pack(fill=tk.X, padx=10, pady=5)

    # # Output File Entry
    # self.output_file = tk.StringVar()
    # output_file_entry = tk.Entry(frame_Configs, state="readonly" ,textvariable=self.output_file, font=("Times", 12), width=10)
    # output_file_entry.pack(fill=tk.X, padx=10, pady=10)

    # # Output File Button
    # output_file_btn = tk.Button(frame_Configs, text="Browse", font=("Times", 12), command=self.select_file)
    # output_file_btn.pack(fill=tk.X, padx=10, pady=10)

    # Start Button
    start_btn = tk.Button(frame_Configs, text="Start", font=("Times", 12), command=self.startMainScrap)
    start_btn.pack(fill=tk.X, padx=10, pady=10)

    # Frame Results
    frame_Results = tk.Frame(self.window, bd=0, width=500, relief=tk.SOLID, padx=5, pady=5, bg="#FCFCFC")
    frame_Results.pack(side="right", expand=tk.YES, fill=tk.BOTH)

    # Results Label
    results_lbl = tk.Label(frame_Results, text="Results", font=("Times", 14), fg="black", bg="#FCFCFC", pady=10)
    results_lbl.pack(fill=tk.X, padx=10, pady=5)





    # Loop
    self.window.mainloop()

async def get_Data_Login(loginUrl, user, password, state):

  with open(os.path.join(filePath, "credentials.txt"), "r") as file:
    credentials = file.read().split("|")
    user = credentials[0]
    password = credentials[1]

  data = [["ListingID", "Status", "Address", "Region", "Price", "Bedrooms", "Bathrooms", "LivingArea", "YearBuilt", "DeedCategory", "PropertyType", "APN", "TownShip", "Description", "AuctionDate", "TrusteeName", "TrusteePhone", "CaseNumber"]]
  async with async_playwright() as page:
   # Launch browser
   browser = await page.chromium.launch(headless=False)
   page = await browser.new_page()
   # Go to login page
   await page.goto(loginUrl)
   # Fill in login form
   await page.get_by_placeholder('Email').fill(user);
   await page.get_by_placeholder('Password').fill(password);
   await page.locator("#btnLoginUsernamePassword").click();
   print("Login successful")
   # Go to redirect page
   await page.goto(f"https://foreclosures.al.com/listing/search?q={state}&lc=preforeclosure&pi=&pa=&bdi=&bhi=&loc={state}&boundingTopLeft=&boundingBottomRight=&st=&cno=&ci=&ps=100&pg=15&o=&ob=&zip=&");
   # Get Usefull Data
   results_Expected = await page.locator("#fragmentsSearchHeader > div.SearchResultCountBar.pull-left > strong").inner_text()
   # Iterate through "View Details" links
   async def iterate_ViewDetails():
     for i in range(0, 2):
       await page.locator('text=View Details').nth(i).click();
       
       # Get data from page
       await page.wait_for_selector("#additional_info div.description")
       html = await page.inner_html('div#main.container-fluid')
       # Parse html
       soup = BeautifulSoup(html, 'html.parser')
       # Data to be scraped:
       # listingId: div#fixed-details h4.listingId
       # status: div#fixed-details h4.status
       # address: div#fixed-details h3.address span
       # region: div#fixed-details h1.region span
       # price: div#fixed-details h3.price strong
       ## INFORMATION ##
       # bedrooms: #additional_info li.details_li_bedrooms span.value
       # bathrooms: #additional_info li.details_li_bathrooms span.value
       # livingArea: #additional_info li.details_li_living_area_size span.value
       # yearBuilt: #additional_info li.details_li_year_built span.value
       # deedCategory: #additional_info li.details_li_deed_category span.value
       # propertyType: #additional_info li.details_li_property_type span.value
       # apn: #additional_info li.details_li_apn span.value
       # townShip: #additional_info li.details_li_township span.value
       # description: #additional_info div.description 
       # auctionDate: #attributegroup_auction_information li.details_li_auction_date span.value
       # trusteeName: #additional_info li.details_li_trustee_name span.value
       # trusteePhone: #additional_info li.details_li_trustee_phone span.value
       # caseNumber: #additional_info li.details_li_case_number span.value
       try:
         listingId = soup.select_one("div#fixed-details h4.listingId").text
         listingId = listingId.replace("Listing ID: ", "")
         #remove enters
         listingId = listingId.replace("\n", "")
         #remove spaces
         listingId = listingId.replace(" ", "")
       except:
         listingId = "N/A"
       try:
         status = soup.select_one("div#fixed-details h4.status").text
         status = status.replace("Status: ", "")
         #remove enters
         status = status.replace("\n", "")
         #remove spaces
         status = status.replace(" ", "")
       except:
         status = "N/A"
       try:
         address = soup.select_one("div#fixed-details h3.address span").text
       except:
         address = "N/A"
       try:
         region = soup.select_one("div#fixed-details h1.region span").text
       except:
         region = "N/A"
       try:
         price = soup.select_one("div#fixed-details h3.price strong").text
       except:
         price = "N/A"
       try:
         bedrooms = soup.select_one("#additional_info li.details_li_bedrooms span.value").text
       except:
         bedrooms = "N/A"
       try:
         bathrooms = soup.select_one("#additional_info li.details_li_bathrooms span.value").text
       except:
         bathrooms = "N/A"
       try:
         livingArea = soup.select_one("#additional_info li.details_li_living_area_size span.value").text
       except:
         livingArea = "N/A"
       try:
         yearBuilt = soup.select_one("#additional_info li.details_li_year_built span.value").text
       except:
         yearBuilt = "N/A"
       try:
         deedCategory = soup.select_one("#additional_info li.details_li_deed_category span.value").text
       except:
         deedCategory = "N/A"
       try:
         propertyType = soup.select_one("#additional_info li.details_li_property_type span.value").text
       except:
         propertyType = "N/A"
       try:
         apn = soup.select_one("#additional_info li.details_li_apn span.value").text
       except:
         apn = "N/A"
       try:
         townShip = soup.select_one("#additional_info li.details_li_township span.value").text
       except:
         townShip = "N/A"
       try:
         description = soup.select_one("#additional_info div.description").text
         description = description.replace("Property Description", "")
         #remove enters
         description = description.replace("\n", "")
       except:
         description = "N/A"
       try:
         auctionDate = soup.select_one("#attributegroup_auction_information li.details_li_auction_date span.value").text
       except:
         auctionDate = "N/A"
       try:
         trusteeName = soup.select_one("#additional_info li.details_li_trustee_name span.value").text
       except:
         trusteeName = "N/A"
       try:
         trusteePhone = soup.select_one("#additional_info li.details_li_trustee_phone span.value").text
       except:
         trusteePhone = "N/A"
       try:
         caseNumber = soup.select_one("#additional_info li.details_li_case_number span.value").text
       except:
         caseNumber = "N/A"
       # Append data to array
       data.append([listingId, status, address, region, price, bedrooms, bathrooms, livingArea, yearBuilt, deedCategory, propertyType, apn, townShip, description, auctionDate, trusteeName, trusteePhone, caseNumber])
       # Log result number
       print("Result: " + str(i))
       # Go back to previous page
       await page.go_back();
       await page.wait_for_selector('text=View Details');
       # Keep loop until "Next" button is disabled
       
     while await page.is_visible('#pageNextTop') == True:
       print("Page completed")
       await page.click('#pageNextTop');
       await page.wait_for_selector('text=View Details');
       await iterate_ViewDetails();
   # Call iterate_ViewDetails function
   await iterate_ViewDetails();
   # Stop the browser
   await page.close()
   await browser.close()
   # Save data to csv in path
   os.path.join(filePath)
  with open(os.path.join(filePath, f"{state}-Data.csv"), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
  
  # delete txt files
  os.remove(os.path.join(filePath, "state.txt"))
  os.remove(os.path.join(filePath, "credentials.txt"))

def startScrap():

  with open(os.path.join(filePath, "credentials.txt"), "r") as file:
    credentials = file.read().split("|")
    user = credentials[0]
    password = credentials[1]

  with open(os.path.join(filePath, "state.txt"), "r") as file:
    state = file.read()
  asyncio.run(get_Data_Login("https://foreclosures.al.com/login.html", user, password, state))


def center_window(window, app_width, app_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    return window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

async def verifyLogin(user, password):
    async with async_playwright() as page:
    # Launch browser
      browser = await page.chromium.launch(headless=False)
      page = await browser.new_page()

    # Go to login page
      await page.goto("https://foreclosures.al.com/login.html")
    
    # Fill in login form
      await page.get_by_placeholder('Email').fill(user);
      await page.get_by_placeholder('Password').fill(password);
      await page.locator("#btnLoginUsernamePassword").click();

    # Wait for page to load
      await page.wait_for_load_state("networkidle")
    
    if page.url == "https://foreclosures.al.com/":
        #write credentials to file

        with open(os.path.join(filePath, "credentials.txt"), "w") as file:
            file.write(user + "|" + password)
        return True
    else:
        return False

def test(user, password):
  # asd = asyncio.run(verifyLogin(user, password))

  with open(os.path.join(filePath, "credentials.txt"), "w") as file:
    file.write(user + "|" + password)
  asd = True
  return asd

AppScrape()