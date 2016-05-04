import ast
""" This method converts a string that is in the proper form of a dictionary
into a dictionary using the ast"""

def convert_string_into_dict(str_in_dict_form):
    split_string = str_in_dict_form.split()
    for i in range(len(split_string)):
        if split_string[i][-1:] == ':':
            split_string[i] = '(' + '"' + ' '.join(re.findall('[a-zA-Z1-9]',split_string[i])) + '"'+','
        elif split_string[i][-2:] == '],':
            split_string[i] = ' '.join(re.findall('[a-zA-Z1-9]',split_string[i])) + ']),'
        elif split_string[i][-2:] == ']}':
            split_string[i] = ' '.join(re.findall('[a-zA-Z1-9]',split_string[i])) + '])'
    
    string_to_tuple = list(ast.literal_eval(' '.join(test_dict_split)))
    return dict(string_to_tuple)
