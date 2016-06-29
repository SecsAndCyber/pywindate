import windate

import ctypes

from ctypes import *

DWORD = ctypes.c_uint32
WORD = ctypes.c_uint16

class FILETIME(Structure):
    _pack_ = 1
    _fields_ = [
                    ('dwLowDateTime', DWORD ),
                    ('dwHighDateTime', DWORD ),
                ]
    def uint64(self):
        return self.dwHighDateTime << 32 | self.dwLowDateTime
class SYSTEMTIME(Structure):
    _pack_ = 1
    _fields_ = [
                    ('wYear', WORD ),
                    ('wMonth', WORD ),
                    ('wDayOfWeek', WORD ),
                    ('wDay', WORD ),
                    ('wHour', WORD ),
                    ('wMinute', WORD ),
                    ('wSecond', WORD ),
                    ('wMilliseconds', WORD ),
                ]
           
Kernel32 = windll.LoadLibrary("Kernel32")
FileTimeToSystemTime = Kernel32.FileTimeToSystemTime
FileTimeToSystemTime.argtypes = [ ctypes.POINTER(FILETIME), ctypes.POINTER(SYSTEMTIME) ]
FileTimeToSystemTime.restype = c_bool

SystemTimeToFileTime = Kernel32.SystemTimeToFileTime
SystemTimeToFileTime.argtypes = [ ctypes.POINTER(SYSTEMTIME), ctypes.POINTER(FILETIME) ]
SystemTimeToFileTime.restype = c_bool           

def test_windows_apis():
    ST = SYSTEMTIME(0)
    FT = FILETIME(0x48251600, 0x01D1D1B9)
    
    assert FT.dwHighDateTime == 0x01D1D1B9
    assert FT.dwLowDateTime == 0x48251600
    assert FT.uint64() == 0x01D1D1B948251600
    
    assert FileTimeToSystemTime( FT, ST )
    assert ST.wYear == 2016
    assert ST.wMonth == 6
    assert ST.wDay == 29
    assert ST.wHour == 3
    assert ST.wMinute == 49
    assert ST.wSecond == 48
    
    ST = SYSTEMTIME(2016,2,0,14,13,37)
    assert SystemTimeToFileTime(ST, FT)
    assert FT.dwHighDateTime == 0x01D1672C
    assert FT.dwLowDateTime == 0xC7DFA600
    
def test_windate():
    ST = SYSTEMTIME(0)
    FT = FILETIME(0x48251600, 0x01D1D1B9)
    assert FileTimeToSystemTime( FT, ST )
    
    assert windate.FileTimeToDateTime( FT.uint64() ).year == 2016
    assert windate.FileTimeToDateTime( FT.uint64() ).month == 6
    assert windate.FileTimeToDateTime( FT.uint64() ).day == 29
    assert windate.FileTimeToDateTime( FT.uint64() ).hour == 3
    assert windate.FileTimeToDateTime( FT.uint64() ).minute == 49
    assert windate.FileTimeToDateTime( FT.uint64() ).second == 48
    
    dt = windate.datetime(2016,2,14,13,37)
    assert windate.DateTimeToFileTime( dt ) == 0x01D1672CC7DFA600
    
    
if __name__ == "__main__":
    test_windows_apis()
    test_windate()