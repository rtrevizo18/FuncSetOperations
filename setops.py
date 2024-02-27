#type: ignore
'''
Notes:
  Server times:
  MoWe 12pm-3pm 7pm-10pm
  TuTh 10am-1pm 7pm-10pm
  Fr   10am-2pm
  Sa   10am-2pm
'''
from os import system
from sys import argv as system_argvs
from os.path import isfile

ERROR_MESSAGE = '''ERROR: Invalid inputs. Please try again.
Usage: python3 setops.py "set1=<file_1>;set2=<file_2>;operation=<operation>"'''

#Lambda functions to perform operations on iterables
i_head = lambda l: l[0]
i_tail = lambda l: l[1:]
slice = lambda l, start=None, end=None: l[start:end]
at_index = lambda l, n: l[n]
is_empty = lambda l: len(l) == 0 or l == ['']
l_append = lambda l, elem: l + [elem]

#Lambda functions to perform operations on strings/chars
is_digit = lambda char: char >= '0' and char <= '9'
is_upper = lambda char: char >= 'A' and char <= 'Z'
is_lower = lambda char: char >= 'a' and char <= 'z'
is_alpha = lambda char: is_upper(char) or is_lower(char)
is_alnum = lambda char: is_alpha(char) or is_digit(char)
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


# Performs a filter recursively
def recursive_filter(lambda_exp, list):
  if is_empty(list):
    return []

  if lambda_exp(i_head(list)):
    return [i_head(list)] + recursive_filter(lambda_exp, i_tail(list))

  return recursive_filter(lambda_exp, i_tail(list))


"""

END OF GENERAL LIST OPERATION FUNCTIONS

"""
"""

GENERAL STRING OPERATION FUNCTIONS

"""


#Lowercases all chars in a string
def lower_case(string):
  if is_empty(string):
    return ""

  if is_upper(i_head(string)):
    return chr(ord(i_head(string)) + 32) + lower_case(i_tail(string))

  return i_head(string) + lower_case(i_tail(string))


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

  lowercased_op = lower_case(op)

  if not is_inputs_valid_helper(file1, file2, lowercased_op):
    return False

  return [file1, file2, lowercased_op]


"""

END OF SYSTEM ARGUMENTS PARSING AND VALIDATION FUNCTIONS

"""
"""

FILE PARSING AND SET CREATION FUNCTIONS

"""


#Helps parse periods when floats are detected
#Works by checking if succeeding characters are digits
#until non-alphanumeric character is found
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
      return slice(string, end=n)
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

#Peforms several filtering functions in order to get set from file
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


def union(set1, set2):
  if is_empty(set1) and is_empty(set2):
    return []
  if is_empty(set1):
    return set2
  if is_empty(set2):
    return set1

  return recursive_filter(lambda elem: not element_in_list(set1, elem), set2) + set1


def intersection(set1, set2):
  if is_empty(set1) or is_empty(set2):
    return []

  return recursive_filter(lambda x: element_in_list(set2, x), set1)


def difference(set1, set2):
  if is_empty(set1):
    return []
  if is_empty(set2):
    return set1

  return recursive_filter(lambda x: not element_in_list(set2, x), set1)


def perform_operation(set1, set2, operation):
  if operation == "union":
    return union(set1, set2)
  if operation == "intersection":
    return intersection(set1, set2)
  if operation == "difference":
    return difference(set1, set2)


#Performs qksort on array using filter function
def qksrt(arr):
  if len(arr) <= 1:
    return arr

  pivot = arr[len(arr) // 2]

  left = recursive_filter(lambda x: x < pivot, arr)
  middle = recursive_filter(lambda x: x == pivot, arr)
  right = recursive_filter(lambda x: x > pivot, arr)

  return qksrt(left) + middle + qksrt(right)


def set_operations(file1, file2, operation):

  set1, set2 = get_set(file1), get_set(file2)

  operated_set = perform_operation(set1, set2, operation)
  
  sorted_set = qksrt(operated_set)

  return sorted_set


"""

END OF SET OPERATION FUNCTIONS

"""
"""

FILE WRITE AND MAIN FUNCTIONS

"""


def write_to_file(list):
  with open("result.txt", "w") as f:
    f.write(file_join(list, "\n"))


def main(sys_argv):
  if not validate_args(sys_argv):
    print(ERROR_MESSAGE)
    return

  inputs = validate_file_inputs(sys_argv)

  if not inputs:
    print(ERROR_MESSAGE)
    return

  file1, file2, op = inputs

  write_to_file(set_operations(file1, file2, op))


if __name__ == "__main__":
  main(system_argvs)
