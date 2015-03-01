import Ember from 'ember';

export function fromNow(input, options) {
  if (typeof options !== 'undefined' && typeof options.hash.nosuffix !== 'undefined') {
    return input.fromNow(options.hash.nosuffix);
  } else {
    return input.fromNow();
  }
}

export default Ember.Handlebars.makeBoundHelper(fromNow);
