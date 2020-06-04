'''Extract the feedback, price, Seller name and product name from the given 
url : https://feedback.ebay.com/ws/eBayISAPI.dll?ViewFeedback2&userid=littlekitty0103&ftab=AllFeedback&myworld=true&rt=nc
and store the data into a csv file. 
Language to be used : Python3 + , You can use libraries like beautiful soup
Tutorial : https://www.youtube.com/watch?v=XQgXKtPSzUI
Deadline: June 4th 2:00 PM.'''



from selenium import webdriver
import time


#function for count the available pages
def count_pages(driver):
    pages=driver.find_element_by_class_name("footer")
    no_of_pages=max([int(i)  for i in pages.text.split("\n")[0].split() if i.isdigit()])
    return no_of_pages


#function for count the number of rows in the page
def count_rows(driver):
    rows=driver.find_elements_by_xpath('//*[@id="feedback-cards"]/tbody/tr')
    rows=len(rows)+1
    return rows


#function for grab the needed information from the web page
def grab_information(driver,row):
    #get the information in the row
    row_info=driver.find_element_by_xpath('//*[@id="feedback-cards"]/tbody/tr[{}]'.format(row))
    row_info=row_info.text.splitlines()
    #intialize the strings
    feedback,product_name,price,seller_name='','','',''
    #get the needed information in the row_info list
    if len(row_info)!=1:
        feedback=str(row_info[0]).replace(",",";").encode('utf-8')
        if len(row_info)==5:
            product_name=row_info[1].replace(",",";")
            price=row_info[3].replace(",",";")
        if len(row_info)==4:
            if row_info[2][0]=='S':
                seller_name=row_info[2].replace(",",";")
        if len(row_info)==3:
            if row_info[1][0]=='S':
                seller_name=row_info[1].replace(",",";")
    return feedback,price,seller_name,product_name
    
    
def main():
    #open the csv file in write mode
    file_name="feedback.csv"
    f=open(file_name,"w")
    #write the header
    f.write("Feedback , Price , Seller Name , Product Name\n")
    #open the chromedriver
    driver=webdriver.Chrome()
    driver.get("https://feedback.ebay.com/ws/eBayISAPI.dll?ViewFeedback2&userid=littlekitty0103&ftab=AllFeedback&myworld=true&rt=nc")
    #get the no of pages available
    pages=count_pages(driver) 
    #Iterate the pages
    for page in range(pages):
        #get the number of rows in the table
        rows=count_rows(driver)
        #Iterate the rows
        for row in range(1,rows):
            #get the needed information 
            feedback,price,seller_name,product_name=grab_information(driver,row)
            #write the information in csv file
            f.write(str(feedback) + "," + price + "," + seller_name + "," + product_name + " \n ")    
        #click the next button to go next page
        next_button=driver.find_element_by_xpath('//*[@id="next-page"]')
        next_button.click()
        time.sleep(3)
    #close the csv file and chromedriver
    f.close()
    driver.close()


    
if __name__=="__main__":
    main()
    
    

