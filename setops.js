"use strict";

const fs = require("fs");

// Turn into const when no longer debugging
const system_argvs = process.argv.slice(1);

const ERROR_MESSAGE =
  'ERROR: Invalid inputs. Please try again.\nUsage: node setops.js "set1=<file_1>;set2=<file_2>;operation=<operation>"';

// Lambda functions to perform operations on iterables
const i_head = (l) => l[0];
const i_tail = (l) => l.slice(1);
const slice = (l, start = 0, end = l.length) => l.slice(start, end);
const at_index = (l, n) => l[n];
const is_empty = (l) => l.length === 0 || (l.length === 1 && l[0] === "");
const l_append = (l, elem) => [...l, elem];
const len = (l) => l.length;

const c_is_digit = (char) => char >= "0" && char <= "9";
const c_is_upper = (char) => char >= "A" && char <= "Z";
const c_is_lower = (char) => char >= "a" && char <= "z";
const c_is_alpha = (char) => c_is_upper(char) || c_is_lower(char);
const c_is_alnum = (char) => c_is_alpha(char) || c_is_digit(char);
const ord = (char) => char.charCodeAt(0);
const chr = (n) => String.fromCharCode(n);

/*

GENERAL LIST OPERATION FUNCTIONS

*/

// Checks if an element is in a list
function element_in_list(list, element, n = 0) {
  if (is_empty(list)) {
    return false;
  }
  if (at_index(list, n) === element) {
    return true;
  }
  if (len(list) === n + 1) {
    return false;
  }
  return element_in_list(list, element, n + 1);
}

//Recursive join function
function join(arr, joiner) {
  if (is_empty(arr)) {
    return "";
  }

  return i_head(arr) + joiner + join(i_tail(arr), joiner);
}

// Recursive join function that doesn't append joiner at end
function file_join(arr, joiner) {
  if (is_empty(arr)) {
    return "";
  }
  if (len(arr) === 1) {
    return i_head(arr);
  }

  return i_head(arr) + joiner + file_join(i_tail(arr), joiner);
}

// Performs a filter recursively
function recursive_filter(lambda_exp, list) {
  if (is_empty(list)) {
    return [];
  }

  if (lambda_exp(i_head(list))) {
    return [i_head(list)].concat(recursive_filter(lambda_exp, i_tail(list)));
  }

  return recursive_filter(lambda_exp, i_tail(list));
}

/*

END OF GENERAL LIST OPERATION FUNCTIONS

*/

/*

GENERAL STRING OPERATION FUNCTIONS

*/

// Lowercases all chars in a string
function lower_case(string) {
  if (is_empty(string)) {
    return "";
  }

  if (c_is_upper(i_head(string))) {
    return chr(ord(i_head(string)) + 32) + lower_case(i_tail(string));
  }

  return i_head(string) + lower_case(i_tail(string));
}

// Checks if sub_string is in string
function is_sub(iter, sub_iter, n = 0) {
  if (len(iter) < len(sub_iter)) {
    return false;
  }
  if (slice(iter, n, n + len(sub_iter)) === sub_iter) {
    return true;
  }
  if (n + len(sub_iter) === len(iter)) {
    return false;
  }
  return is_sub(iter, sub_iter, n + 1);
}

// Recursive Split function with O(n) time complexity where n is len(word)
function split(word, sep, arr = null, n = 0) {
  // Stops function from remembering array from previous calls (IS NECESSARY FOR RECURSION)
  if (arr === null) {
    arr = [];
  }

  // Guard Cases
  if (is_empty(word)) {
    return [];
  }

  // If separator is found, add the word before it to the list
  // and recursively call the function with the rest of the word,
  // the same list, and a reset index of 0 (implicit)
  if (at_index(word, n) === sep) {
    const new_arr = l_append(arr, slice(word, 0, n));
    if (len(word) === n + 1) {
      return new_arr;
    } else {
      return split(slice(word, n + 1), sep, new_arr);
    }
  }

  // If at end of word, add the word to the list and return array
  if (len(word) === n + 1) {
    return l_append(arr, slice(word, 0, n + 1));
  }

  // If not found, increment index and recursively call the function
  return split(word, sep, arr, n + 1);
}

// Strips characters (one or multiple key chars) from a string
function strip(string, chars) {
  if (is_empty(string)) {
    return "";
  }

  if (is_sub(chars, i_head(string))) {
    return strip(i_tail(string), chars);
  }

  return i_head(string) + strip(i_tail(string), chars);
}

/*

END OF GENERAL STRING OPERATION FUNCTIONS

*/

/*

SYSTEM ARGUMENTS PARSING AND VALIDATION FUNCTIONS

*/

// Checking if argument syntax is correct
function validate_args(args) {
  // Guard Cases
  if (len(args) !== 2) {
    return false;
  }

  const string_arg = at_index(args, 1);

  if (!is_sub(string_arg, "set1=")) {
    return false;
  }
  if (!is_sub(string_arg, "set2=")) {
    return false;
  }
  if (!is_sub(string_arg, "operation=")) {
    return false;
  }

  return true;
}

// Recursively puts input into a list
function split_args_helper(args_array, arr = null) {
  if (arr === null) {
    arr = [];
  }

  if (is_empty(args_array)) {
    return arr;
  }

  const new_arr = l_append(arr, i_head(i_tail(i_head(args_array))));
  return split_args_helper(i_tail(args_array), new_arr);
}

// Organizes system args into a list
function split_args(args) {
  // Splits the second argument by ";" and then splits each element by "="
  return split_args_helper(
    split(at_index(args, 1), ";").map((x) => split(x, "=")),
  );
}

// Checks if file1 and file2 exist, and that operation is valid
function is_inputs_valid_helper(file1, file2, operation) {
  if (!fs.existsSync(file1)) {
    return false;
  }
  if (!fs.existsSync(file2)) {
    return false;
  }
  if (!element_in_list(["union", "intersection", "difference"], operation)) {
    return false;
  }

  return true;
}

// Returns file inputs if they're valid
function validate_file_inputs(args) {
  const [file1, file2, op] = split_args(args);

  const lowercased_op = lower_case(op);

  if (!is_inputs_valid_helper(file1, file2, lowercased_op)) {
    return false;
  }

  return [file1, file2, lowercased_op];
}

/*

END OF SYSTEM ARGUMENTS PARSING AND VALIDATION FUNCTIONS

*/

/*

FILE PARSING AND SET CREATION FUNCTIONS

*/

// Helps parse periods when floats are detected
// Works by checking if succeeding characters are digits until non-alphanumeric character is found
// If another period is found, it is replaced with a space
function period_helper(string, n = 0) {
  if (is_empty(string)) {
    return "";
  }

  if (at_index(string, n) === ".") {
    return slice(string, 0, n) + " " + slice(string, n + 1);
  }

  if (len(string) === n + 1) {
    return string;
  }

  if (!c_is_alnum(at_index(string, n))) {
    return string;
  }

  return period_helper(string, n + 1);
}

// Cuts out unnecessary periods and leaves in periods for floats
function handle_periods(string, n = 0) {
  if (is_empty(string)) {
    return "";
  }

  if (at_index(string, n) === ".") {
    if (n === 0) {
      return handle_periods(i_tail(string));
    }
    if (len(string) === n + 1) {
      return slice(string, 0, n);
    }
    if (
      c_is_digit(at_index(string, n - 1)) &&
      c_is_digit(at_index(string, n + 1))
    ) {
      return handle_periods(period_helper(string, n + 1), n + 1);
    }

    return handle_periods(
      slice(string, 0, n) + " " + slice(string, n + 1),
      n - 1,
    );
  }

  if (len(string) === n + 1) {
    return string;
  }

  return handle_periods(string, n + 1);
}

// Replace punctuation with spaces (except for periods for floats)
function replace_punc(string, n = 0) {
  if (is_empty(string)) {
    return "";
  }

  if (!c_is_alnum(at_index(string, n)) && at_index(string, n) !== ".") {
    if (len(string) === n + 1) {
      return slice(string, 0, n) + " " + slice(string, n + 1);
    }
    return replace_punc(
      slice(string, 0, n) + " " + slice(string, n + 1),
      n + 1,
    );
  }

  if (len(string) === n + 1) {
    return string;
  }

  return replace_punc(string, n + 1);
}

// Separates words and letters
function sep_words_letters(string, n = 0) {
  if (is_empty(string)) {
    return "";
  }

  if (len(string) === n + 1) {
    return string;
  }

  if (c_is_alpha(at_index(string, n)) && c_is_digit(at_index(string, n + 1))) {
    return sep_words_letters(
      slice(string, 0, n + 1) + " " + slice(string, n + 1),
      n + 2,
    );
  }

  if (c_is_digit(at_index(string, n)) && c_is_alpha(at_index(string, n + 1))) {
    return sep_words_letters(
      slice(string, 0, n + 1) + " " + slice(string, n + 1),
      n + 2,
    );
  }

  return sep_words_letters(string, n + 1);
}

// Deletes duplicate spaces created by filtering functions
function delete_dupe_spaces(string, n = 0) {
  if (is_empty(string)) {
    return "";
  }

  if (len(string) === n + 1) {
    if (at_index(string, n) === " ") {
      return slice(string, 0, n);
    }
    return string;
  }

  if (at_index(string, n) === " " && at_index(string, n + 1) === " ") {
    if (len(string) === n + 2) {
      return slice(string, 0, n);
    }
    return delete_dupe_spaces(
      slice(string, 0, n + 1) + slice(string, n + 2),
      n,
    );
  }

  return delete_dupe_spaces(string, n + 1);
}

// Completely filters lines
function filter_input(line) {
  return delete_dupe_spaces(
    sep_words_letters(replace_punc(handle_periods(line))),
  );
}

// Iterates through list and deletes elements in list equal to arr[tag]
function delete_dupes_helper(arr, tag, n = 0) {
  if (is_empty(arr)) {
    return [];
  }

  if (len(arr) === n) {
    return arr;
  }

  if (tag === n) {
    return delete_dupes_helper(arr, tag, n + 1);
  }

  if (at_index(arr, tag) === at_index(arr, n)) {
    return delete_dupes_helper(
      slice(arr, 0, n).concat(slice(arr, n + 1)), tag, n);
  }

  return delete_dupes_helper(arr, tag, n + 1);
}

// Iterates through list and deletes duplicates
function delete_dupes(arr, n = 0) {
  if (is_empty(arr)) {
    return [];
  }

  if (len(arr) === n + 1) {
    return delete_dupes_helper(arr, n);
  }

  const new_arr = delete_dupes_helper(arr, n);

  if (len(new_arr) <= n + 1) {
    return new_arr;
  }

  return delete_dupes(new_arr, n + 1);
}

// Helper functions
function get_filelines(file) {
  return split(fs.readFileSync(file, "utf8"), "\n");
}

function get_set(file) {
  const filelines = get_filelines(file);

  const parsed_output = filelines.map(filter_input);

  const full_word_list = split(join(parsed_output, " "), " ");

  const lowercased_list = full_word_list.map(lower_case);

  const set = delete_dupes(lowercased_list);

  return set;
}

/*

END OF FILE PARSING AND SET CREATION FUNCTIONS

*/

/*

SET OPERATION FUNCTIONS

*/

// Union operation
function union(set1, set2) {
  if (is_empty(set1) && is_empty(set2)) {
    return [];
  }
  if (is_empty(set1)) {
    return set2;
  }
  if (is_empty(set2)) {
    return set1;
  }

  return recursive_filter((elem) => !element_in_list(set1, elem), set2).concat(set1);
}

function intersection(set1, set2) {
  if (is_empty(set1) || is_empty(set2)) {
    return [];
  }

  return recursive_filter((x) => element_in_list(set2, x), set1);
}

function difference(set1, set2) {
  if (is_empty(set1)) {
    return [];
  }
  if (is_empty(set2)) {
    return set1;
  }

  return recursive_filter((x) => !element_in_list(set2, x), set1);
}

function perform_operation(set1, set2, operation) {
  if (operation === "union") {
    return union(set1, set2);
  }
  if (operation === "intersection") {
    return intersection(set1, set2);
  }
  if (operation === "difference") {
    return difference(set1, set2);
  }
}

function qksrt(arr) {
  if (len(arr) <= 1) {
    return arr;
  }
  const pivot = arr[Math.floor(len(arr) / 2)];
  const left = recursive_filter((x) => x < pivot, arr);
  const middle = recursive_filter((x) => x === pivot, arr);
  const right = recursive_filter((x) => x > pivot, arr);
  return qksrt(left).concat(middle, qksrt(right));
}

function set_operations(file1, file2, operation) {
  // Get sets from files
  const set1 = get_set(file1);
  const set2 = get_set(file2);

  // Perform the specified set operation
  const operated_set = perform_operation(set1, set2, operation);

  const sorted_set = qksrt(operated_set);

  return sorted_set;
}

/*

END OF SET OPERATION FUNCTIONS

*/

/*

FILE WRITE AND MAIN FUNCTIONS

*/

function write_to_file(list) {
  fs.writeFileSync("result.txt", file_join(list, "\n"));
}

function main(sys_argv) {
  if (!validate_args(sys_argv)) {
    console.log(ERROR_MESSAGE);
    return;
  }

  const inputs = validate_file_inputs(sys_argv);

  if (!inputs) {
    console.log(ERROR_MESSAGE);
    return;
  }

  const [file1, file2, op] = inputs;

  write_to_file(set_operations(file1, file2, op));
}

if (require.main === module) {
  main(system_argvs);
}
