
    with open(txt_file) as input_file:
        for line in input_file:
            # limits the parsing to the header section
            if lines_read > MAX_LINES_TO_READ:
                break
            
            # look for a line that contains a series of number
            fields = line.split('|')[1:-1]  # ignore first and last
            
            if len(fields) == 5:
                try:
                    numbers = list(map(int, fields))
                    return numbers[3] # regn column
                except ValueError:
                    # not the line we are after, skip                
                    lines_read += 1
    
    raise ValueError("{} deviates from the expected format".format(txt_file))    
    
def yield_csv(txt_file):
    pass    
    yield row
    
    
def yeild_rows_form_txt_101(txt_file):
    # may need to use .split("|") to obtain fields
    # must yeild same format as dbf_file
    # make test - get data from dbf and from 
    
    regn = get_regn(txt_file)
    dt = get_date(txt_file)
    
    is_in_section_a = False
    is_in_section_b = False
    a_p = 0
    
    for row in yield_csv(txt_file):
        if len(row) > 0:
            if is_in_section_a == False and row[0] == u"А.": is_in_section_a = True
            if is_in_section_b == False and row[0] == u"Б.": is_in_section_b = True
            if is_in_section_a == True and row[0] == u"Актив": a_p = 1
            if is_in_section_a == True and row[0] == u"Пассив": a_p = 2
            if is_in_section_b == True: a_p = 0
            
        if len(row) == 13:
            fe = row[0]
            flag = (fe.startswith("|") and len(fe) > 1)
            
        if flag:
            row[0] = row[0][1:]
            row[-1] = row[-1][:-1]
            row.append(dt)
            row.append(str(a_p))
            row.append(regn)
            yield(row)
    
    
    
def convert_f101_txt2csv(txt_file, csv_file, isodate):

    regn = get_regn(txt_file)
    dt = get_date(txt_file)
    
    with open(csv_file, 'w') as targetfile:
        writer = csv.writer(targetfile, delimiter='\t', lineterminator = '\n')

        with open(txt_file, 'r') as sourcefile:
            reader = csv.reader(sourcefile, delimiter=' ', skipinitialspace = True)
            is_in_section_a = False
            is_in_section_b = False
            a_p = 0
            
            for row in reader:
                if len(row) > 0:
                    if is_in_section_a == False and row[0] == u"А.": is_in_section_a = True
                    if is_in_section_b == False and row[0] == u"Б.": is_in_section_b = True
                    if is_in_section_a == True and row[0] == u"Актив": a_p = 1
                    if is_in_section_a == True and row[0] == u"Пассив": a_p = 2
                    if is_in_section_b == True: a_p = 0
                    #  print(a_p)
                    
                if len(row) > 0:
                    flag = "|" == row[0][0] and len(row[0]) > 1 and len(row) == 13
                    
                if flag:
                    row[0] = row[0][1:]
                    row[-1] = row[-1][:-1]
                    row.append(isodate)
                    row.append(str(a_p))
                    row.append(regn)
                    writer.writerow(row)
                    
def convert_f102_txt2csv(txt_file, csv_file, isodate):
    """
    Special converter of form 102 text files to csv files.
    Note: skips rows with missing ('X') values.    
    """    
    SKIP_ROWS = 45
    regn = get_regn(txt_file)
    
    year, quarter = conv_date2quarter(isodate)
    
    with open(csv_file, 'w') as targetfile:
        writer = csv.writer(targetfile, delimiter='\t', lineterminator = '\n')

        with open(txt_file, 'r') as sourcefile:
            reader = csv.reader(sourcefile, delimiter='|', skipinitialspace=True)

            for _ in range(SKIP_ROWS):
                next(reader)
            
            for row in reader:
                if len(row) == 8:
                    try:
                        _ = int(row[1]) # just try to parse, should be int
                        fields = list(map(int, row[3:7]))
                        fields.insert(0, isodate)
                        fields.insert(0, regn)                        
                        fields.insert(0, quarter)
                        fields.insert(0, year)
                        writer.writerow(fields)
                    except ValueError:
                        pass
