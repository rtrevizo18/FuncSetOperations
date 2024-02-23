"use strict";

const i_head = l => l[0];
const i_tail = l => l.slice(1);
const slice = (l, start = 0, end = l.length) => l.slice(start, end);
const at_index = (l, n) => l[n];
const is_empty = l => l.length === 0;
const l_append = (l, elem) => [...l, elem];
const is_digit = string => !isNaN(string);
const len = l => l.length;

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

console.log(is_sub("hellowdr", "hello"))