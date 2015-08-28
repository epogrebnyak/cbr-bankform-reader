# -*- coding: utf-8 -*-
"Use get_regn(f) and get_date(f)."

MAX_TOP_LINES = 20

def yield_by_line(f, max_lines):
    cnt = 0 
    with open(f, encoding="utf8") as input_file:
        for line in input_file:
            if cnt <= max_lines:
                yield line
                cnt += 1
               
def which_field_is_pivotal(fields):
    marker = "Регистрационный номер"
    for i, f in enumerate(fields):
        if marker in f:
            return i
    return None

def get_integers(fields):
    try:
        return list(map(int, fields))
    except:
        return None
    return None
                    
def get_regn_from_stream(lines_stream):
    """
    Parse and retrun regn code from *lines_stream*.
    """
    pivot_index = None
    for line in lines_stream:
            # print(line)
            fields = line.split('|')[2:-1]
            
            if len(fields) > 0: 
                if which_field_is_pivotal(fields) is not None:
                    pivot_index = which_field_is_pivotal(fields)                    
                #  print("pivot_index:", pivot_index) 
                #  print("fields: ", fields)
                #  print("ints:", get_integers(fields))
                
                if get_integers(fields) is not None:
                     return get_integers(fields)[pivot_index]

    raise ValueError("Format not recognised.")

def get_regn(f):
    lines_stream = yield_by_line(f, MAX_TOP_LINES)
    return get_regn_from_stream(lines_stream)
 
import re   
PAT = re.compile("за (\S*) (\d{4}) г.")
MONTHS = ["январь", "февраль", "март",
          "апрель", "май", "июнь",
          "июль", "август", "сентябрь",
          "октябрь", "ноябрь", "декабрь"]
MONTHS_DICT = dict((m,i+1) for i, m in enumerate(MONTHS))

def get_month_by_name(text):
    return MONTHS_DICT[text]
   


from datetime import date
from dateutil.relativedelta import relativedelta

def extract_date(line, pat = PAT):
    r = pat.findall(line)
    if len(r) > 0:
        g = r[0]
        month = get_month_by_name(g[0])
        year = int(g[1])
        return date(year,month,1) + relativedelta(months=1) 
    else:
        return None        
   
def get_date_from_stream(lines_stream):
    for line in lines_stream:
        if extract_date(line) is not None:
            return extract_date(line) 

def get_date(f): 
    lines_stream = yield_by_line(f, MAX_TOP_LINES)
    return get_date_from_stream(lines_stream)
 
if __name__ == "__main__":
    assert date(2016,1,1) == date(2015,12,1) + relativedelta(months=1) 
    
    def yield_doc(lines):
        for line in lines.split("\n"):
            yield line
            
    doc1 = """
Must parse table below to obtain "1481" 
 
                                              Банковская отчетность
         +--------------+-----------------------------------------+
         |Код территории|   Код кредитной организации (филиала)   |
         |  по ОКАТО    +-----------------+-----------------------+
         |              |    по ОКПО      | Регистрационный номер |
         |              |                 |  (/порядковый номер)  |
         +--------------+-----------------+-----------------------+
         |45293554000   |00032537         |       1481            |
         +--------------+-----------------+-----------------------+

"""

    doc2  = """
Must parse table below to obtain "0964" 

                                                                                Банковская отчетность
       +--------------+-----------------------------------------------------------------------------+
       |Код территории|                 Код кредитной организации (филиала)                         |
       |  по ОКАТО    +----------------+---------------------+---------------------+----------------+
       |              |    по ОКПО     |      Основной       |Регистрационный номер|      БИК       |
       |              |                |   государственный   |(/порядковый номер)  |                |
       |              |                |регистрационный номер|                     |                |
       +--------------+----------------+---------------------+---------------------+----------------+
       |45286         |00005061        |1077711000102        |      0964           |   044525060    |
       +--------------+----------------+---------------------+---------------------+----------------+
"""

    def test_get_regn():
         assert get_regn_from_stream(yield_doc(doc1)) == 1481
         assert get_regn_from_stream(yield_doc(doc2)) == 964

    test_get_regn()

    str1 = "       |              |    по ОКПО     |      Основной       |Регистрационный номер|      БИК       |"
    assert which_field_is_pivotal(str1.split('|')) == 4   
    str2 = "       |Код территории|                 Код кредитной организации (филиала)                         |"
    assert which_field_is_pivotal(str2.split('|')) == None   

    assert get_regn("data\SBER_F101_07_2015.txt") == 1481
    assert get_regn("data\F101_12.txt") == 964     
    # WARNING: fails by encoding. 

    dt1 = "за декабрь 2012 г."
    dt2 = "за июль 2015 г."

    assert extract_date(dt1) == date(2013,1,1) # (12, 2012)
    assert extract_date(dt2) == date(2015,8,1) # (7, 2015)
    assert extract_date(str1) == None
     
    assert get_date("data\SBER_F101_07_2015.txt") == date(2015,8,1)
    assert get_date("data\F101_12.txt") == date(2013,1,1)   

    
