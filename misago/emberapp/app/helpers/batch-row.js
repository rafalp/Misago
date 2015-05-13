import Ember from 'ember';

export function batchRow(list, rowWidth) {
  var rows = [];
  var row = [];

  Ember.EnumerableUtils.forEach(list, function(element) {
    row.push(element);
    if (row.length === rowWidth) {
      rows.push(row);
      row = [];
    }
  });

  if (row.length) {
    rows.push(row);
  }

  return rows;
}

export default Ember.Handlebars.makeBoundHelper(batchRow);
