from datetime import datetime

def isLeapYear(year: int) -> bool:
    """Check if a year is a leap year."""
    return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))

def ConvertDayToTimestamp(day: int, month: int, year: int) -> tuple[int, str]:
    """
    Convert a given day (e.g., 01/01/2025) with defaul time 00:00:00 
    into a Unix timestamp (e.g., 1735743797).
    Input: day, month, year (integers).
    Output: timestamp (in seconds), error message (if any).
    """

    if year <= 1970:
        return 0, "Invalid input: The year must be 1971 or later."
    if (month < 1) or (month > 12):
        return 0, "Invalid input: The month must be between 1 and 12."

    if day < 1: 
        return 0, "Invalid input: The day must be greater than 0"
    if (month in {1, 3, 5, 7, 8, 10, 12}) and (day > 31):
        return 0, f"Invalid input: The month {month} only has 31 days."
    if (month in {4, 6, 9, 11}) and (day > 30):
        return 0, f"Invalid input: The month {month} only has 30 days."
    
    if isLeapYear(year):
        if (month == 2) and (day > 29):
            return 0, f"Invalid input: February {year} (Leap year) only has 29 days."
    elif (month == 2) and (day > 28):
        return 0, f"Invalid input day. February {year} (Common year) only has 28 days." 
    
    dt = datetime(year, month, day, 0, 0) 
    unixTimestamp = int(dt.timestamp())
    err = None

    return unixTimestamp, err

def GetMonthRange(month: int, year: int) -> tuple[int, int, str]:
    """
    Calculate the Unix timestamp range for a given month of a year.
    Input: month, year (integers).
    Output: 
        startOfMonth (int): Unix timestamp for the start of the month (00:00:00 on the 1st day).
        endOfMonth (int): Unix timestamp for the end of the month (23:59:59 on the last day).
        err (str or None): An error message if input is invalid, or None if no errors.
    """

    # Calculate the start of the month
    startOfMonth, err1 = ConvertDayToTimestamp(1, month, year)
    if err1:
        return startOfMonth, 0, err1

    # Calculate the start of the next month
    if month == 12:
        endOfMonth, err2 = ConvertDayToTimestamp(1, 1, year + 1)
    else:
        endOfMonth, err2 = ConvertDayToTimestamp(1, month + 1, year)
    endOfMonth -= 1 if endOfMonth > 0 else 0 # Adjust to the end of the month (from 00:00:00 of 01/mm + 1/yyyy to 23:59:59 of dd/mm/yyyy)

    err = err1 if err1 == err2 else err2 or err1 or f"{err1}; {err2}"

    return startOfMonth, endOfMonth, err

def GetYearRange(year: int) -> tuple[int, int, str]:
    """
    Calculate the Unix timestamp range for a given year.
    Input: year (integers).
    Output: 
        startOfYear (int): Unix timestamp for the start of the year (00:00:00 on 01/01/year).
        endOfYear (int): Unix timestamp for the end of the month (23:59:59 on 31/12/year).
        err (str or None): An error message if input is invalid, or None if no errors.
    """

    # Calculate the start of the year
    startOfYear, err1 = ConvertDayToTimestamp(1, 1, year)
    if err1:
        return startOfYear, 0, err1
    
    # Calculate the start of the next year
    endOfYear, err2 = ConvertDayToTimestamp(1, 1, year + 1)
    endOfYear -= 1 if endOfYear > 0 else 0 # Adjust to 31st December 23:59:59
    err = err1 if err1 == err2 else err2 or err1 or f"{err1}; {err2}"

    return startOfYear, endOfYear, err