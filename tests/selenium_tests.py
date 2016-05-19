#!/usr/bin/env python3

import unittest 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class GoogleTestCase(unittest.TestCase):

    def testPageTitle(self):
        self.browser.get('http://beta.is-an-engineer.com/')
        self.assertIn("Welcome Page", self.browser.title)

    def testHometoStudent(self):    
        self.browser.get("http://beta.is-an-engineer.com/")
        student = self.browser.find_element_by_xpath("/html/body/ol/a")
        student.click()
        self.assertIn("Student's Page", self.browser.title)

    def testStudentPageTitle(self):
        self.browser.get('http://beta.is-an-engineer.com/cgi-bin/student_meetings.py')
        self.assertIn("Student's Page", self.browser.title)

    def testElementsOnStudentPage(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/student_meetings.py")
        self.browser.find_element_by_name("lecturer_id")
        self.browser.find_element_by_name("start_date")

    def testSubmittingLecturerAndWeekByStudent(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/student_meetings.py")
        lecturer = Select(self.browser.find_element_by_name("lecturer_id"))
        lecturer.select_by_value('1')
        submit_button = self.browser.find_element_by_xpath("/html/body/ol/form/div/input[2]")
        submit_button.click()
        self.assertIn("Calendar Template", self.browser.title)

    def testHometoLecturer(self):    
        self.browser.get("http://beta.is-an-engineer.com/")
        student = self.browser.find_element_by_xpath("/html/body/ol/form/input")
        student.click()
        self.assertIn("Lecturer's Page", self.browser.title)

    def testLecturerPageTitle(self):
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/lecturer_page.py"
            "?lecturer_id=1")
        self.assertIn("Lecturer's Page", self.browser.title)  

    def testElementsOnLecturerPage(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/lecturer_page.py"
            "?lecturer_id=1")
        self.browser.find_element_by_name("start_date")

    def testSubmittingWeekByLecturer(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/lecturer_page.py"
            "?lecturer_id=1")
        submit_button = self.browser.find_element_by_xpath("/html/body/ol/form/div/input[4]")
        submit_button.click()
        self.assertIn("Calendar Template", self.browser.title)

    def testCalendarTemplateTitle(self):
        self.browser.get('http://beta.is-an-engineer.com/cgi-bin/calendar_template.py')
        self.assertIn("Calendar Template", self.browser.title)

    def testBookingFormTitle(self):
        self.browser.get('http://beta.is-an-engineer.com/cgi-bin/booking_form.py')
        self.assertIn("Booking Form", self.browser.title)

    def testElementsOnStudentBookingForm(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/booking_form.py"
            "?student_booking=True")
        self.browser.find_element_by_name("student_id")
        self.browser.find_element_by_name("subject")

    def testSubmittingStudentBookingForm(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/"
            "booking_form.py?student_booking=True")
        meeting_subject = self.browser.find_element_by_name("subject")
        meeting_subject.send_keys("testingsubject")
        student_id = self.browser.find_element_by_name("student_id")
        student_id.send_keys("678851")
        submit_button = self.browser.find_element_by_xpath("/html/body/doctype/form"
            "/input[7]")
        submit_button.click()
        self.assertIn("Booking Successful", self.browser.title)

    def testSubmittingLecturerBookingForm(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/"
            "booking_form.py?student_booking=False")
        meeting_subject = self.browser.find_element_by_name("subject")
        meeting_subject.send_keys("testingsubject")
        student_attendees = self.browser.find_element_by_name("attendees")
        student_attendees.send_keys("597609,678851,547937")
        submit_button = self.browser.find_element_by_xpath("/html/body/doctype/form"
            "/input[8]")
        submit_button.click()
        self.assertIn("Booking Successful", self.browser.title)

    def testReturnToHomepageAfterBookingSuccess(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/schedule_meeting.py?"
            "student_id=345345&subject=hello&lecturer_id=None&date_time=None")
        submit_button = self.browser.find_element_by_xpath("/html/body/center/p/a")
        submit_button.click()
        self.assertIn("Welcome Page", self.browser.title)

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    # Group bookings testing    

    def testThatLecturerCanSpecifyGroupMeeting(self):    
        self.browser.get("http://beta.is-an-engineer.com/cgi-bin/booking_form.py"
            "?lecturer_id=2&date_time=2016-05-19T09:00&student_booking=False&")

        group_booking = self.browser.find_element_by_xpath("/html/body/doctype/form"
            "/input[3]")
        group_booking.click()

        submit_button = self.browser.find_element_by_xpath("/html/body/doctype/form"
            "/input[8]")
        submit_button.click()
        self.assertIn("group_booking=True", self.browser.current_url)

    def testThatGroupMeetingHasBeenMade(self):    
        self.browser.get("http://beta.is-an-engineer.com/")
        student = self.browser.find_element_by_xpath("/html/body/ol/a")
        student.click()

        lecturer = Select(self.browser.find_element_by_name("lecturer_id"))
        lecturer.select_by_value('2')
        submit_button = self.browser.find_element_by_xpath("/html/body/ol/form/div/input[2]")
        submit_button.click()

        group_booking = self.browser.find_element_by_xpath("//*[@id='meetings']/tbody/tr[2]/td[4]/a")
        value = group_booking.get_attribute('text')
     
        self.assertEqual(value,"Join")

    


if __name__ == '__main__':
    unittest.main(verbosity=2)