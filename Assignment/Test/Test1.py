import time
from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class jupitor_toys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.set_page_load_timeout(10)
        cls.driver.get("http://jupiter.cloud.planittesting.com")
        cls.driver.set_page_load_timeout(20)
        cls.driver.maximize_window()

    def setUp(self):
        self.driver.find_element(By.ID, 'nav-home').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        time.sleep(1)

    def test_contact_jupitor_toys(self):
        # This test case will test the functionality of Contact page and submission of the feedback
        # Go to Contact and wait for the page to load
        self.driver.find_element(By.ID, 'nav-contact').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="form-actions"]//a')))
        time.sleep(1)
        print('TestCase1:')
        # Fill in contact information for client and submit the form one by one
        for i in range(1, 6):
            self.driver.find_element(By.ID, 'forename').send_keys('Tester'+str(i))
            self.driver.find_element(By.ID, 'email').send_keys('Tester'+str(i)+'@gmail.com')
            self.driver.find_element(By.ID, 'message').send_keys('Message from Tester'+str(i))
            self.driver.find_element(By.XPATH, '//div[@class="form-actions"]//a').click()
            # Wait for the submission message to appear and then click back to go to Contact page
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="alert alert-success"]')))
            time.sleep(1)
            message = self.driver.find_element(By.XPATH, '//div[@class="alert alert-success"]').text
            print(message)
            self.driver.find_element(By.XPATH, '//div[@class="ng-scope"]//a').click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="form-actions"]//a')))
            time.sleep(1)

    def test_verify_items_in_cart(self):
        # This test case will test the functionality of adding items to cart and verify if items are added successfully
        # Go to Shop
        self.driver.find_element(By.ID, 'nav-shop').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="product-6"]/div/p/a')))
        time.sleep(1)
        print('TestCase2:')

        # Add items to Cart
        # 2 Funny Cow & 1 Fluffy Bunny
        for i in range(2):
            self.driver.find_element(By.XPATH, '//*[@id="product-6"]/div/p/a').click()
            time.sleep(1)

        self.driver.find_element(By.XPATH, '//*[@id="product-4"]/div/p/a').click()
        time.sleep(1)

        # Go To Cart
        self.driver.find_element(By.ID, 'nav-cart').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[normalize-space()="Check Out"]')))
        time.sleep(1)

        # Verify the items in Cart
        # Verify item1
        toyname = self.driver.find_element(By.XPATH, '//tbody/tr[1]/td[1]').text
        assert toyname == "Funny Cow", "Item mismatch"
        price = self.driver.find_element(By.XPATH, '//tbody/tr[1]/td[2]').text
        assert price == "$10.99", "Item mismatch"
        quantity = self.driver.find_element(By.XPATH, '//tbody/tr[1]/td[3]/input').get_attribute("value")
        assert quantity == "2", "Item mismatch"
        print('Item1: ' + toyname + " - Price: " + price + ' - Quantity: ' + quantity)
        # Verify item2
        toyname = self.driver.find_element(By.XPATH, '//tbody/tr[2]/td[1]').text
        assert toyname == "Fluffy Bunny", "Item mismatch"
        price = self.driver.find_element(By.XPATH, '//tbody/tr[2]/td[2]').text
        assert price == "$9.99", "Item mismatch"
        quantity = self.driver.find_element(By.XPATH, '//tbody/tr[2]/td[3]/input').get_property("value")
        assert quantity == "1", "Item mismatch"
        print('Item2: ' + toyname + " - Price: " + price + ' - Quantity: ' + quantity)
        # Empty Cart
        self.driver.find_element(By.XPATH, '//ng-confirm[@title="Empty Cart"]').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-footer"]//a[1]'))).click()


    def test_verify_subtotal_in_cart(self):
        # This test case will verify if the subtotal of the items added are calculated correctly
        # Go to Shop
        self.driver.find_element(By.ID, 'nav-shop').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="product-6"]/div/p/a')))
        time.sleep(1)
        print('TestCase3:')

        # Add items to Cart
        for i in range(2):
            self.driver.find_element(By.XPATH, '//*[@id="product-2"]/div/p/a').click()
            time.sleep(1)
        for i in range(5):
            self.driver.find_element(By.XPATH, '//*[@id="product-4"]/div/p/a').click()
            time.sleep(1)
        for i in range(3):
            self.driver.find_element(By.XPATH, '//*[@id="product-7"]/div/p/a').click()
            time.sleep(1)

        # Go To Cart
        self.driver.find_element(By.ID, 'nav-cart').click()
        time.sleep(2)

        # Verify the items in Cart
        # Verify item1
        toyname = self.driver.find_element(By.XPATH, '//tbody/tr[1]/td[1]').text
        assert toyname == "Stuffed Frog", "Item mismatch"
        price = self.driver.find_element(By.XPATH, '//tbody/tr[1]/td[2]').text
        assert price == "$10.99", "Item mismatch"
        quantity = self.driver.find_element(By.XPATH, '//tbody/tr[1]/td[3]/input').get_attribute("value")
        assert quantity == "2", "Item mismatch"
        subtotal = self.driver.find_element(By.XPATH, '//tbody/tr[1]/td[4]').text
        assert subtotal[1:6] == str(int(quantity) * float(price[1:6])), "Item mismatch"
        print('Item1: ' + toyname + " - Price: " + price + ' - Quantity: ' + quantity + ' - Subtotal: ' + subtotal)
        # Verify item2
        toyname = self.driver.find_element(By.XPATH, '//tbody/tr[2]/td[1]').text
        assert toyname == "Fluffy Bunny", "Item mismatch"
        price = self.driver.find_element(By.XPATH, '//tbody/tr[2]/td[2]').text
        assert price == "$9.99", "Item mismatch"
        quantity = self.driver.find_element(By.XPATH, '//tbody/tr[2]/td[3]/input').get_property("value")
        assert quantity == "5", "Item mismatch"
        subtotal = self.driver.find_element(By.XPATH, '//tbody/tr[2]/td[4]').text
        assert subtotal[1:6] == str(int(quantity) * float(price[1:6])), "Item mismatch"
        print('Item2: ' + toyname + " - Price: " + price + ' - Quantity: ' + quantity + ' - Subtotal: ' + subtotal)
        # Verify item3
        toyname = self.driver.find_element(By.XPATH, '//tbody/tr[3]/td[1]').text
        assert toyname == "Valentine Bear", "Item mismatch"
        price = self.driver.find_element(By.XPATH, '//tbody/tr[3]/td[2]').text
        assert price == "$14.99", "Item mismatch"
        quantity = self.driver.find_element(By.XPATH, '//tbody/tr[3]/td[3]/input').get_property("value")
        assert quantity == "3", "Item mismatch"
        subtotal = self.driver.find_element(By.XPATH, '//tbody/tr[3]/td[4]').text
        assert subtotal[1:6] == str(int(quantity) * float(price[1:6])), "Item mismatch"
        print('Item3: ' + toyname + " - Price: " + price + ' - Quantity: ' + quantity + ' - Subtotal: ' + subtotal)
        # Empty Cart
        self.driver.find_element(By.XPATH, '//ng-confirm[@title="Empty Cart"]').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-footer"]//a[1]'))).click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()

