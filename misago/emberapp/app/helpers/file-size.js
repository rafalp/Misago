import Ember from 'ember';

export function fileSize(bytes) {
  if (bytes > 1000 * 1000 * 1000) {
    return (Math.round(bytes * 100 / (1000 * 1000 * 1000)) / 100) + ' GB';
  } else if (bytes > 1000 * 1000) {
    return (Math.round(bytes * 100 / (1000 * 1000)) / 100) + ' MB';
  } else if (bytes > 1000) {
    return (Math.round(bytes * 100 / 1000) / 100) + ' KB';
  } else {
    return (Math.round(bytes * 100) / 100) + ' B';
  }
}

export default Ember.Handlebars.makeBoundHelper(fileSize);
