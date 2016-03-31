export default function(array, value) {
  if (array.indexOf(value) === -1) {
    array.push(value);
    return array;
  } else {
    return array.filter(function(i) {
      return i !== value;
    });
  }
}