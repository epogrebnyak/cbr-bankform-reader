# -*- coding: utf-8 -*-
"""
Directory structure navigation and data stream emitters.

Directory structure:
- data
-- public
   - ziprar
   - dbf
   - txt
   - csv_from_dbf
   - csv_from_txt
-- private
   - txt
   - csv_from_txt
""" 

def check_arg(string, allowed_values):
    if string not in allowed_values:
        raise ValueError ("Invalid parameter: " + string)    

def check_stream_arg(date, form, content, domain, source):
  check_arg(content, ["data", "plan", "names"])
  check_arg(form,    ["101", "102"])
  check_arg(domain,  ["public", "private"])
  check_arg(source,  ["dbf", "csv_from_dbf", "txt", "csv_from_txt"])      
  # note: date not cheked
  
def get_data_dir():
    return "data"

import os
def get_folder(domain, source):
    return os.path.join(get_data_dir(), domain, source)

def get_steam_iterator(date, form, content, domain, source):
    check_stream_arg(date, form, content, domain, source)
    folder = get_folder(domain, source)
    emitter = func_navigation[content][form][source]
    return emitter(date, folder) 

def dbf_f101(date, folder):
    pass

def txt_f101(date, folder):
    pass

def csv_f101(date, folder):
    pass

def dbf_f102(date, folder):
    pass

def txt_f102(date, folder):
    pass

def csv_f102(date, folder):
    pass

reader_funcs_101_by_source =    {'dbf': dbf_f101, 
                                 'txt': txt_f101,
                        'csv_from_dbf': csv_f101,
                        'csv_from_txt': csv_f101  }

reader_funcs_102_by_source  =   {'dbf': dbf_f102, 
                                 'txt': txt_f102,
                        'csv_from_dbf': csv_f102,
                        'csv_from_txt': csv_f102 }
                        
func_navigation = {'plan': None, 
                  'names': None,
                   'data': { "101" : reader_funcs_101_by_source  , 
                             "102" : reader_funcs_102_by_source  }
                   }            
            
#  path = get_path(date, form, content, domain)
#      folder = get_folder(form, content, domain)
#      filenames, readers = get_file_reader_pair(date, form, content)
#      return (paths, readers) tuple
#  *** reader = get_reader(form, content)
#  *** return reader(path)
