export default function(bytes) {
  if (bytes > 1024 * 1024 * 1024) {
    return (Math.round(bytes * 100 / (1024 * 1024 * 1024)) / 100) + ' GB';
  } else if (bytes > 1024 * 1024) {
    return (Math.round(bytes * 100 / (1024 * 1024)) / 100) + ' MB';
  } else if (bytes > 1024) {
    return (Math.round(bytes * 100 / 1024) / 100) + ' KB';
  } else {
    return (Math.round(bytes * 100) / 100) + ' B';
  }
}