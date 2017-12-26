import io


def breakLinePosChk(stream, strLn):
    spc_no = 0
    text=""
    pos=strLn
    while text != "\n":
        text = stream.read(1)
        pos = stream.tell()
        if text == " ":
            spc_no += 1
        else:
            spc_no = 0
        if spc_no > 4:
            break

    return pos - 1 # Remove pos of "\n"

def ensureCorrectPaddingWtSpc2dRht(_str, suppose_size):
    len_str = len(_str)
    padding_size = suppose_size - len_str
    if padding_size > 0:
        _str += (" " * padding_size)
    elif padding_size < 0:
        _str += ("\n")

    return _str
    

def ReplaceHelper(stream, beginPos, replace_with, str_length):
    # Equalize length
    replace_with = ensureCorrectPaddingWtSpc2dRht(replace_with, str_length)

    stream.seek(beginPos)
    stream.write(unicode(replace_with))
    return True

def SearchHelper(stream, find_str, assumed_str_length, replace_whole_line=False):
    strtLn = stream.tell()
    text = stream.readline(assumed_str_length)
    endLn = stream.tell()
    found = False
    total_overrite_length=None

    if text.find(find_str) != -1:
        stream.readline(assumed_str_length)
        if replace_whole_line: 
            endLn = breakLinePosChk(stream, strtLn)
        else:
            endLn = stream.tell()
        total_overrite_length = endLn - strtLn
        found = True

    while found is False and text:
        text= stream.readline(assumed_str_length)
        if text.find(find_str) != -1:
            if replace_whole_line: 
                endLn = breakLinePosChk(stream, strtLn)
            else:
                endLn = stream.tell()

            total_overrite_length = endLn - strtLn
            found = True
            break
        strtLn = stream.tell()
            
    return found, strtLn, total_overrite_length
    
def SearchReplace(_file, find_str, replace_with, replace_whole_line=False,
           assumed_str_length=50):
    stream = io.open(_file, "r+")

    found, strtLn, total_overrite_length = SearchHelper(stream, find_str,
                                                         assumed_str_length)

    if found:
        if not replace_whole_line:
            return ReplaceHelper(stream, strtLn, replace_with, assumed_str_length)
        else:
            return ReplaceHelper(stream, strtLn, replace_with, total_overrite_length)

    return False



    
