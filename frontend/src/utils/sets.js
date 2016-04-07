export function push(array, value) {
  if (array.indexOf(value) === -1) {
    array.push(value);
  }

  return array;
}

export function remove(array, value) {
  if (array.indexOf(value) >= 0) {
    return array.filter(function(i) {
      return i !== value;
    });
  } else {
    return array;
  }
}

export function toggle(array, value) {
  if (array.indexOf(value) === -1) {
    array.push(value);
    return array;
  } else {
    return array.filter(function(i) {
      return i !== value;
    });
  }
}