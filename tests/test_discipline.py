# -*- coding: utf-8 -*-
import unittest
from src.discipline import Discipline

class TestDiscipline(unittest.TestCase):

    def test_constructor(self):
        d = Discipline('MC102', 'CC01', 1, 10)
        self.assertEqual(d.code, 'MC102')
        self.assertTrue((1, 'CC01') in d.day_hour)
        self.assertEqual(d.day_hour[1, 'CC01'], (10, 11))


    def test_add_day_hour(self):
        d = Discipline('MC102', 'CC01', 1, 10)
        d.add_day_hour('CC01', 1, 8)
        self.assertEqual(d.code, 'MC102')
        self.assertTrue((1, 'CC01') in d.day_hour)
        self.assertEqual(d.day_hour[1, 'CC01'], (8, 11))
        
        d.add_day_hour('CC01', 2, 8)
        self.assertEqual(d.code, 'MC102')
        self.assertTrue((2, 'CC01') in d.day_hour)
        self.assertEqual(d.day_hour[2, 'CC01'], (8, 9))


    def test_to_item(self):
        d = Discipline('MC102', 'CC01', 1, 10)
        self.assertEqual(d.to_item(), {
            'code' : 'MC102', 
            'hours' : [{
                'day' : 1,
                'room' : 'CC01', 
                'ini' : 10,
                'end' : 11,
            }] 
        })

    def test_to_string(self):
        d = Discipline('MC102', 'CC01', 1, 10)
        self.assertEqual(str(d), 'MC102')

if __name__ == '__main__':
    unittest.main()