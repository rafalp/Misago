export function startsWith(string, beginning) {
  return string.indexOf(beginning) === 0;
}

export function endsWith(string, tail) {
  return string.indexOf(tail, string.length - tail.length) !== -1;
}
