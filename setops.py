#type: ignore
'''
Notes:
  Server times:
  MoWe 12pm-3pm 7pm-10pm
  TuTh 10am-1pm 7pm-10pm
  Fr   10am-2pm
  Sa   10am-2pm
'''
from sys import argv as system_argvs, exit, setrecursionlimit
from os.path import isfile

setrecursionlimit(999)

ERROR_MESSAGE = '''ERROR: Invalid inputs. Please try again.
Usage: python3 setops.py "set1=<file_1>;set2=<file_2>;operation=<operation>"'''

#Lambda functions to perform operations on iterables
i_head = lambda l: l[0]
i_tail = lambda l: l[1:]
slice = lambda l, start=None, end=None: l[start:end]
at_index = lambda l, n: l[n]
is_empty = lambda l: len(l) == 0
l_append = lambda l, elem: l + [elem]

#Lambda functions to perform operations on strings/chars
is_digit = lambda string: string.isdigit()
is_alnum = lambda string: string.isalnum()
is_alpha = lambda string: string.isalpha()
is_upper = lambda string: string >= 'A' and string <= 'Z'
"""

GENERAL LIST OPERATION FUNCTIONS

"""


#Checks if an element is in a list
def element_in_list(list, element, n=0):
  if list == []:
    return False
  if at_index(list, n) == element:
    return True
  if len(list) == n + 1:
    return False

  return element_in_list(list, element, n + 1)


#Recursive join function
def join(arr, joiner):
  if (is_empty(arr)):
    return ""

  return i_head(arr) + joiner + join(i_tail(arr), joiner)


#Recursive join function that doesn't append joiner at end
def file_join(arr, joiner):
  if (is_empty(arr)):
    return ""
  if len(arr) == 1:
    return i_head(arr)

  return i_head(arr) + joiner + file_join(i_tail(arr), joiner)


"""

END OF GENERAL LIST OPERATION FUNCTIONS

"""
"""

GENERAL STRING OPERATION FUNCTIONS

"""


#Checks if sub_string is in string
def is_sub(iter, sub_iter, n=0):
  if len(iter) < len(sub_iter):
    return False
  if slice(iter, n, (n + len(sub_iter))) == sub_iter:
    return True
  if (n + len(sub_iter)) == len(iter):
    return False
  return is_sub(iter, sub_iter, n + 1)


#Recursive Split function with O (n) time complexity where n is len(word)
def split(word, sep, arr=None, n=0):
  #Stops function from remembering array from prev calls
  if arr is None:
    arr = []
  #Guard Cases
  if (is_empty(word)):
    return []

  #If seperator is found, add the word before it to the list
  #and recursively call the function with the rest of the word,
  #the same list, and a reset index of 0 (implicit)
  if at_index(word, n) == sep:
    new_arr = l_append(arr, slice(word, end=n))
    if len(word) == n + 1:
      return new_arr
    else:
      return split(slice(word, start=(n + 1)), sep, new_arr)

  #If at end of word, add the word to the list and return array
  if len(word) == (n + 1):
    return l_append(arr, slice(word, end=(n + 1)))

  #If not found, increment index and recursively call the function
  return split(word, sep, arr, n + 1)


#Strips characters (one or multiple key chars) from a string
def strip(string, chars):
  if is_empty(string):
    return ""

  if is_sub(chars, i_head(string)):
    return strip(i_tail(string), chars)

  return i_head(string) + strip(i_tail(string), chars)


"""

END OF GENERAL STRING OPERATION FUNCTIONS

"""
"""

SYSTEM ARGUMENTS PARSING AND VALIDATION FUNCTIONS

"""


#Checking if argument syntax is correct
def validate_args(args):
  #Guard Cases
  if len(args) != 2:
    return False

  string_arg = at_index(args, 1)

  if not is_sub(string_arg, "set1="):
    return False
  if not is_sub(string_arg, "set2="):
    return False
  if not is_sub(string_arg, "operation="):
    return False

  return True


#Recursively puts input into a list
def split_args_helper(args_array, arr=None):
  if arr is None:
    arr = []

  if is_empty(args_array):
    return arr

  new_arr = l_append(arr, i_head((i_tail(i_head(args_array)))))
  return split_args_helper(i_tail(args_array), new_arr)


#Organizes system args into a list
def split_args(args):
  return split_args_helper(
      list(map(lambda x: split(x, "="), split(at_index(args, 1), ";"))))


#Checks if file1 and file2 exist, and that operation is valid
def is_inputs_valid_helper(file1, file2, operation):
  if not isfile(file1):
    return False
  if not isfile(file2):
    return False
  if not is_sub(["union", "intersection", "difference"], [operation]):
    return False

  return True


#Returns file inputs if they're valid
def validate_file_inputs(args):
  file1, file2, op = split_args(args)

  if not is_inputs_valid_helper(file1, file2, op):
    return False

  return [file1, file2, op]


"""

END OF SYSTEM ARGUMENTS PARSING AND VALIDATION FUNCTIONS

"""

"""

FILE PARSING AND SET CREATION FUNCTIONS

"""


#Helps parse periods when floats are detected
#Works by checking if succeeding characters are digits until non-alphanumeric character is found
#If another period is found, it is replaced with a space
def period_helper(string, n=0):

  if is_empty(string):
    return ""

  if at_index(string, n) == ".":
    return slice(string, end=n) + " " + slice(string, start=n + 1)

  if len(string) == n + 1:
    return string

  if not is_alnum(at_index(string, n)):
    return string

  return period_helper(string, n + 1)


#Cuts out unneccessary periods and leaves in periods for floats
def handle_periods(string, n=0):
  if is_empty(string):
    return ""

  if at_index(string, n) == ".":
    if n == 0:
      return handle_periods(i_tail(string))
    if len(string) == n + 1:
      #FIXME
      #NEED TESTING FUNCTION
      return slice(string, end=n)
    #FIXME: Fix helper function
    if is_digit(at_index(string, n - 1)) and is_digit(at_index(string, n + 1)):
      return handle_periods(period_helper(string, n + 1), n + 1)

    return handle_periods(
        slice(string, end=n) + " " + slice(string, start=n + 1), n - 1)

  if len(string) == n + 1:
    return string

  return handle_periods(string, n + 1)


#Replace punctuation with spaces (expect for periods for floats)
def replace_punc(string, n=0):
  if is_empty(string):
    return ""

  if not is_alnum(at_index(string, n)) and not at_index(string, n) == ".":
    if len(string) == n + 1:
      return slice(string, end=n) + " " + slice(string, start=n + 1)

    return replace_punc(
        slice(string, end=n) + " " + slice(string, start=n + 1), n + 1)

  if len(string) == n + 1:
    return string

  return replace_punc(string, n + 1)


#Seperates words and letters
def sep_words_letters(string, n=0):
  if is_empty(string):
    return ""

  if len(string) == n + 1:
    return string

  if is_alpha(at_index(string, n)) and is_digit(at_index(string, n + 1)):
    return sep_words_letters(
        slice(string, end=n + 1) + " " + slice(string, start=n + 1), n + 2)

  if is_digit(at_index(string, n)) and is_alpha(at_index(string, n + 1)):
    return sep_words_letters(
        slice(string, end=n + 1) + " " + slice(string, start=n + 1), n + 2)

  return sep_words_letters(string, n + 1)


#Deletes duplicate spaces created by filtering functions
def delete_dupe_spaces(string, n=0):
  if is_empty(string):
    return ""

  if len(string) == n + 1:
    if at_index(string, n) == " ":
      return slice(string, end=n)
    return string

  if at_index(string, n) == " " and at_index(string, n + 1) == " ":
    if len(string) == n + 2:
      return slice(string, end=n)

    return delete_dupe_spaces(
        slice(string, end=n + 1) + slice(string, start=n + 2), n)

  return delete_dupe_spaces(string, n + 1)


#Completely filters lines
def filter_input(line):
  return delete_dupe_spaces(
      sep_words_letters(replace_punc(handle_periods(line))))


#Lowercases all chars in a string
def lower_case(string):
  if is_empty(string):
    return ""

  if is_upper(i_head(string)):
    return chr(ord(i_head(string)) + 32) + lower_case(i_tail(string))

  return i_head(string) + lower_case(i_tail(string))


#Iterates through list and deletes elements in list equal to arr[tag]
def delete_dupes_helper(arr, tag, n=0):
  if is_empty(arr):
    return []

  if len(arr) == n:
    return arr

  if tag == n:
    return delete_dupes_helper(arr, tag, n + 1)

  if at_index(arr, tag) == at_index(arr, n):
    return delete_dupes_helper(
        slice(arr, end=n) + slice(arr, start=n + 1), tag, n)

  return delete_dupes_helper(arr, tag, n + 1)


#Iterates through list and deletes duplicates
def delete_dupes(arr, n=0):
  if is_empty(arr):
    return []

  if len(arr) == n + 1:
    return delete_dupes_helper(arr, n)

  new_arr = delete_dupes_helper(arr, n)

  if len(new_arr) <= n + 1:
    return new_arr

  return delete_dupes(new_arr, n + 1)

def get_set(file):
  with open(file, "r") as f:
    filelines = f.readlines()

  parsed_output = list(map(filter_input, filelines))

  full_word_list = split(join(parsed_output, " "), " ")

  lowercased_list = list(map(lower_case, full_word_list))

  set = delete_dupes(lowercased_list)

  return set

"""

END OF FILE PARSING AND SET CREATION FUNCTIONS

"""


"""

SET OPERATION FUNCTIONS

"""


def union_helper(list, set, n=0):
  if len(set) == n:
    return list

  if not element_in_list(list, at_index(set, n)):
    return union_helper(l_append(list, at_index(set, n)), set, n + 1)

  return union_helper(list, set, n + 1)


def union(set1, set2):
  if is_empty(set1) and is_empty(set2):
    return []
  if is_empty(set1):
    return set2
  if is_empty(set2):
    return set1

  return union_helper(set1, set2)


def intersection(set1, set2):
  if is_empty(set1) or is_empty(set2):
    return []

  return list(filter(lambda x: element_in_list(set2, x), set1))


def difference(set1, set2):
  if is_empty(set1):
    return []
  if is_empty(set2):
    return set1

  return list(filter(lambda x: not element_in_list(set2, x), set1))


def perform_operation(set1, set2, operation):
  if operation == "union":
    return union(set1, set2)
  if operation == "intersection":
    return intersection(set1, set2)
  if operation == "difference":
    return difference(set1, set2)

#FIXME
#FIXME
#FIXME
def qksrt():
  pass

def set_operations(file1, file2, operation):

  set1, set2 = get_set(file1), get_set(file2)
  
  operated_set = perform_operation(set1, set2, operation)
  #FIXME
  #FIXME
  #FIXME
  #sorted_set = qksrt(operated_set)
  return perform_operation(set1, set2, operation)

"""

END OF SET OPERATION FUNCTIONS

"""

"""

FILE WRITE AND MAIN FUNCTIONS

"""

def write_to_file(list):
  with open("result.txt", "w") as f:
    f.write(file_join(list, "\n"))


#for debugging purposes (COMMENT OUT IF INPUTTING ARGS IN SHELL)
system_argvs = ["setops.py", "set1=a5.txt;set2=b5.txt;operation=difference"]


def main(sys_argv):
  if not validate_args(sys_argv):
    exit(ERROR_MESSAGE)

  inputs = validate_file_inputs(sys_argv)

  if not inputs:
    exit(ERROR_MESSAGE)

  file1, file2, op = inputs

  write_to_file(set_operations(file1, file2, op))


if __name__ == "__main__":
  main(system_argvs)
