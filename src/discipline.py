import os

class Discipline:
    def __init__(self, code, room, d, h):
        self.day_hour = {}
        self.code = code
        self.day_hour[d, room] = (h, h + 1)
    

    def add_day_hour(self, room, d, h):
        if (d, room) in self.day_hour:
            s_i, s_f = self.day_hour[d, room]
            self.day_hour[d, room] = (min(s_i, h), max(s_f, h + 1))
        else:
            self.day_hour[d, room] = (h, h + 1)
    
   
    def to_item(self):
        hours = []
        for (d, room) in self.day_hour:
            hours.append({
                'day' : d,
                'room' : room, 
                'ini' : self.day_hour[d,room][0],
                'end' : self.day_hour[d,room][1]
            })
        return {
            'code' : self.code,
            'hours' : hours
        }

    def __str__(self):
        return '%s %s' % (self.code, str(self.day_hour))