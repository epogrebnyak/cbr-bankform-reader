# cbr-bankform-reader
Reads bank form data from DBF and text files. Emits clean data by row, storable in a database. Supports form 101 and 102.

Principal operations:

.dbf -> csv with headers  
.txt -> csv with headers  
csv with headers -> ordered dict stream (strings as values)  
ordered dict stream (strings as values) -> typed ordered dict stream (strings, ints, dates) 

Each form yields its own resulting stream as typed ordered dicts. 
  
Resulting streams:
- f101
- f102
- plan101
- plan102
- names

Stage 1: source .dbf and .txt files referenced by filename 
Stage 2: streams are referenced by form, public/private, date and content.
  
Pseudocode:
```python
def get_steam_iterator(date, form, content, domain):
  content in ["data", "plan", "names"]
  form in ["101", "102"]
  domain in ["public", private]
  date unbound
  
  path = get_path(date, form, content, domain)
      folder = get_folder(form, content, domain)
      filenames, readers = get_file_reader_pair(date, form, content)
      return (paths, readers) tuple
  *** reader = get_reader(form, content)
  *** return reader(path)

  
```  
Stage 2 includes:
  folder structre and 
  
  
