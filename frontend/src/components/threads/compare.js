export function compareLastPostAge(a, b) {
  if (a.last_post > b.last_post) {
    return -1;
  } else if (a.last_post < b.last_post) {
    return 1;
  } else {
    return 0;
  }
}

export function compareGlobalWeight(a, b) {
  if (a.weight === 2 && a.weight > b.weight) {
    return -1;
  } else if (b.weight === 2 && a.weight < b.weight) {
    return 1;
  } else {
    return compareLastPostAge(a, b);
  }
}

export function compareWeight(a, b) {
  if (a.weight > b.weight) {
    return -1;
  } else if (a.weight < b.weight) {
    return 1;
  } else {
    return compareLastPostAge(a, b);
  }
}