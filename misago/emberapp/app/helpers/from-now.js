import Ember from 'ember';

export function fromNow(input, options) {
  if (input) {
    if (typeof options !== 'undefined' && typeof options.hash.nosuffix !== 'undefined') {
      return input.fromNow(options.hash.nosuffix);
    } else {
      return input.fromNow();
    }
  } else {
    return gettext('never');
  }
}

export default Ember.Handlebars.makeBoundHelper(fromNow);
