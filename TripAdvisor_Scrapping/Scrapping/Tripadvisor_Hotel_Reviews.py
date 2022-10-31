def Reviews(Link):

    # Link = 'https://www.tripadvisor.com/Hotel_Review-g616162-d14965680-Reviews-High_Beach_White-Malia_Crete.html'

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    revs = []


    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument("headless")
    # options.add_argument("start-maximized")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
    driver.get(Link)

    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="OK"]'))).click()
    except:
        print('\nNo cookie')
    # counter = 0
    # cookie_clicked = 0
    # while True:
    #     if cookie_clicked == 0:
    #         try:
    #             time.sleep(3)
    #             WebDriverWait(driver, 3).until(
    #                     EC.element_to_be_clickable((By.XPATH, '//button[text()="Manage Settings"]'))).click()
    #             cookie_clicked = 1
    #         except:
    #             print('\nNo cookie')
    #
    #
    #     try:
    #         element = WebDriverWait(driver, 3).until(
    #                 EC.presence_of_element_located((By.XPATH, '//button[text()="Decline All"]')))
    #         element.click()
    #
    #     except:
    #         time.sleep(2)
    #         driver.find_element_by_id('evidon-prefdiag-decline').click()
    #
    #     if driver.find_elements_by_xpath('//button[@id="evidon-prefdiag-decline"]') == []:
    #         break
    #
    #     if counter >= 3:
    #         driver.refresh()
    #         break
    #     if counter == 2:
    #         driver.refresh()
    #     counter += 1

    try:





        try:
            last = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="pageNumbers"]/a[last()]'))).text)
        except:
            last = 1

        print('\nreviews pages = ', last)

        # if not WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]'))):
        #     driver.quit()
        #     return 'No reviews'
        # else:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]')))
        except:
            print('Not present all reviews')
        for page in range(last):
            print('\nPage=' + str(page+1)+'  (%.2f'%(((page+1)/last)*100)+'%)')
            try:
                more = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "_3maEfNCR"))).text
                if more == 'Read more':
                    time.sleep(2)
                    driver.find_element_by_class_name("_3maEfNCR").click()
            except:
                print('\n-No Read more-')

            try:
                WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]')))
            except:
                driver.close()
                return revs

            # window = WebDriverWait(driver, 10).until(
            #     EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]')))[0]

            for window in WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]'))):

                try:
                    reviewer = window.find_element_by_class_name("ui_header_link._1r_My98y").text
                except:
                    reviewer = window.find_element_by_class_name("ui_header_link._1r_My98y verified").text

                try:
                    reviewer_link = window.find_element_by_class_name("ui_header_link._1r_My98y").get_attribute('href')
                except:
                    reviewer_link = window.find_element_by_class_name("ui_header_link._1r_My98y verified").get_attribute('href')

                try:
                    country = window.find_element_by_class_name("_1TuWwpYf").text
                except:
                    country = ''

                rating = window.find_element_by_class_name("nf9vGX55").find_element_by_tag_name('span').get_attribute('class').split()[-1].split('_')[-1]
                rating = rating[0] + '.' + rating[1]

                try:
                    date_of_stay = window.find_element_by_class_name('_34Xs-BQm').text
                except:
                    date_of_stay = ''

                try:
                    date_of_review = window.find_element_by_class_name('_2fxQ4TOx').text.split('review ')[-1]
                except:
                    date_of_review = ''
                try:
                    title = window.find_element_by_class_name('glasR4aX').text
                except:
                    title = ''

                try:
                    comment = window.find_element_by_class_name('IRsGHoPm').text
                except:
                    comment = ''

                try:
                    trip_type = window.find_element_by_class_name('_2bVY3aT5').text
                    trip_type = trip_type.replace('Trip type: ', '')
                except:
                    trip_type = ''

                try:
                    contributions = ''
                    helpfulvotes = ''
                    for c in window.find_elements_by_class_name('_3fPsSAYi'):
                            if 'contribution' in c.text:
                                contributions = c.text.split()[0]
                            elif 'helpful vote' in c.text:
                                helpfulvotes = c.text.split()[0]

                except:
                    contributions = ''
                    helpfulvotes = ''







                try:
                    Stars = window.find_element_by_class_name('_1HQD2bGG')

                    Stars_Value = ''
                    Stars_Rooms = ''
                    Stars_Service = ''
                    Stars_Cleanliness = ''
                    Stars_Location = ''
                    Stars_Sleepquality = ''

                    for stars in Stars.find_elements_by_class_name('_3ErKuh24._1OrVnQ-J'):
                        if 'Value' in stars.text:
                            Stars_Value = stars.find_element_by_class_name('ui_bubble_rating').get_attribute('class').split('_')[-1]
                            Stars_Value = Stars_Value[0] + '.' + Stars_Value[1]
                        elif 'Rooms' in stars.text:
                            Stars_Rooms = stars.find_element_by_class_name('ui_bubble_rating').get_attribute('class').split('_')[-1]
                            Stars_Rooms = Stars_Rooms[0] + '.' + Stars_Rooms[1]
                        elif 'Service' in stars.text:
                            Stars_Service = stars.find_element_by_class_name('ui_bubble_rating').get_attribute('class').split('_')[-1]
                            Stars_Service = Stars_Service[0] + '.' + Stars_Service[1]
                        elif 'Cleanliness' in stars.text:
                            Stars_Cleanliness = stars.find_element_by_class_name('ui_bubble_rating').get_attribute('class').split('_')[-1]
                            Stars_Cleanliness = Stars_Cleanliness[0] + '.' + Stars_Cleanliness[1]
                        elif 'Location' in stars.text:
                            Stars_Location = stars.find_element_by_class_name('ui_bubble_rating').get_attribute('class').split('_')[-1]
                            Stars_Location = Stars_Location[0] + '.' + Stars_Location[1]
                        elif 'Sleep Quality' in stars.text:
                            Stars_Sleepquality = stars.find_element_by_class_name('ui_bubble_rating').get_attribute('class').split('_')[-1]
                            Stars_Sleepquality = Stars_Sleepquality[0] + '.' + Stars_Sleepquality[1]
                except:
                    Stars_Value = ''
                    Stars_Rooms = ''
                    Stars_Service = ''
                    Stars_Cleanliness = ''
                    Stars_Location = ''
                    Stars_Sleepquality=''


                revs.append({"Reviewer Username": reviewer,
                                    "Reviewer Link": reviewer_link,
                                   "Country": country,
                                   "Rating": rating,
                                   "Date of stay": date_of_stay,
                                   "Date of review": date_of_review,
                                   "Title": title,
                                   "Comment": comment,
                                   "Helpful Votes": helpfulvotes,
                                   "Contribution Votes": contributions,
                                   "Trip Type": trip_type,
                                   "Value Stars": Stars_Value,
                                   "Rooms Stars": Stars_Rooms,
                                   "Service Stars": Stars_Service,
                                   "Cleanliness Stars": Stars_Cleanliness,
                                   "Location Stars": Stars_Location,
                                   "Sleep Quality Stars": Stars_Sleepquality
                                    })

                #print(reviewer+'\n')
                #if page == 5: break
            if page >= last -1: break

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Next"]'))).click()

            time.sleep(2)
                # try:
                #     driver.find_element_by_class_name("ui_button.nav.next.primary").click()
                # except:
                #     driver.find_element_by_partial_link_text('Next').click()
                # else:
                #     driver.refresh()




                #if page == 5: break

        driver.quit()
        return revs

    except:
        driver.quit()
        return revs

