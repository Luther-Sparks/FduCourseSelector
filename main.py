#coding=UTF-8
import json
import re
import base64
import pytz
import os
from datetime import datetime
import time
from cookie_getter import CookieGetter
from captcha import read_captcha
from email_sender import sendEmail
from utils import *

_, URL_DICT = ReadNetWorkJson()

class CourseSearcher(CookieGetter):
    def __init__(self):
        super(CourseSearcher, self).__init__()
        self.mainUrl = URL_DICT['MAIN_PAGE']
        self.xkPageUrl = URL_DICT['XK_PAGE']
        self.baseUrl = URL_DICT['BASE_URL']
        self.selCourseUrl = URL_DICT['SELECT_COURSE']
        self.captchaUrl = URL_DICT['CAPTCHA']
        
        self.form_data = PayloadGetter('formData')
        self.main_page_data = PayloadGetter('mainPageData')
        self.courseIdList = ReadLessonJson()
        self.cookies = self.getCookies()
        
    def RunScript(self):
        datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        while datetime.now().hour < 13 and datetime.now().minute < 59:
            continue
        print(datetime.now())
        while self.courseIdList and datetime.now.hour <= 13 and datetime.now().minute <= 5:
            for lessonNo in self.courseIdList:
                if self.addCourse(lessonNo):
                    self.courseIdList.remove(lessonNo)
                    time.sleep(0.2)
            
        
    def addCourse(self, lessonNo):
        res = self.searchCourse(lessonNo)
        course_no, course_id, course_name = findClassList(res.text, lessonNo)
        if isCourseAvailable(res.text, course_no):
            info = "课程 [" + course_name + " " + course_id +"], 可选, 正在选课中"
            print(info)
            #sendEmail(info)
            result = self.selCourse(course_no)
            return True
        else:
            info = "课程 [" + course_name + " " + course_id +"], 目前不可选"
            print(info)
            return False
        
    def searchCourse(self, lessonNo):
        form = self.form_data
        form['lessonNo'] = lessonNo
        
        self.direct_to_selCoursePage() # 验证步骤，必须执行，不然会被服务器反制
        res = self.Post(
            url=self.baseUrl,
            cookies=self.cookies,
            data = form,
            ErrMsg="Serch Course Error (getCourseNoAndId)"
        )
        return res
    
    def direct_to_selCoursePage(self):
        self.Get(
            url=self.xkPageUrl,
            cookies=self.cookies,
            ErrMsg="Get Main Page Error (getCourseNoAndId) Get"
        )
        self.Post(
            url=self.mainUrl,
            cookies=self.cookies,
            data = self.main_page_data,
            ErrMsg="Into Xk Page Error (getCourseNoAndId) Post"
        )
                
    # 抢课（捡漏）
    def selCourse(self, course_no):
        form_data = {
            'optype': 'true',
            'operator0': course_no + ':true:0',
            'captcha_response': self.getCaptcha()
        }
        response = self.Post(
            url=self.selCourseUrl,
            cookies=self.cookies,
            data=form_data,
            ErrMsg="selCourse Error (selCourse)"
        )
        #print(response.content.decode(encoding='utf-8'))
        print("选课成功")
        
    def getCaptcha(self):
        response = self.Get(
            url=self.captchaUrl,
            cookies=self.cookies,
            ErrMsg="Get Captcha Error (getCaptcha)"
        )
        captcha =  read_captcha(response.content)
        return captcha
    

if __name__ == "__main__":
    launcher = CourseSearcher()
    launcher.RunScript()
            