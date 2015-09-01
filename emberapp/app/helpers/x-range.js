import Ember from 'ember';

export function xRange(length) {
  return new Array(length);
}

export default Ember.Handlebars.makeBoundHelper(xRange);
