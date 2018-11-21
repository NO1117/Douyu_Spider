
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import json
import time
from selenium import webdriver
import logging

class DouYu:
    def __init__(self):
        # start url
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()


    def get_room_info(self):
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        item_list = []
        for li in li_list:
            room_name = li.find_element_by_xpath("./a").get_attribute("title")
            room_link = li.find_element_by_xpath("./a").get_attribute("href")
            room_img = li.find_element_by_xpath("./a/span/img").get_attribute("src")
            room_category = li.find_element_by_xpath(".//span[@class='tag ellipsis']").text
            room_author = li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
            watch_number = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
            item = dict(
                room_name=room_name,
                room_link=room_link,
                room_img=room_img,
                room_category=room_category,
                room_author=room_author,
                watch_number=watch_number,
            )
            item_list.append(item)
            # print(item)
        return item_list

    def save_item_list(self, item_list):
        with open('Douyu.txt', 'a+', encoding='utf-8') as f:
            for item in item_list:
                json.dump(item, f, ensure_ascii=False, indent=2)
                # f.write(json.dumps(item, ensure_ascii=False, indent=2))
            # f.flush()
            f.close()
        print("Save success!")


    def __del__(self):
        self.driver.close()


    def run(self):
        times = 0
        # 1.获取首页URL,并请求URL
        self.driver.get(self.start_url)
        # 2.提取当前页面房间信息
        item_list = self.get_room_info()
        self.save_item_list(item_list)
        # 3.点击下一页
        print('Next Page!')
        temp_list = self.driver.find_elements_by_class_name("shark-pager-next")
        # 4.进行循环获取所有的房间信息
        while len(temp_list) > 0 and times < 3:
            times += 1
            temp_list[0].click()
            time.sleep(3)
            item_list = self.get_room_info()
            self.save_item_list(item_list)
            print('Next Page!')
            temp_list = self.driver.find_elements_by_class_name("shark-pager-next")

if __name__=='__main__':
    douyu = DouYu()
    douyu.run()
