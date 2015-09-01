import Ember from 'ember';

export function joinStrings() {
  if (arguments.length > 1) {
    var args = Array.prototype.slice.call(arguments, 0, arguments.length - 1);
    return args.join('');
  } else {
    return '';
  }
}

export default Ember.Handlebars.makeBoundHelper(joinStrings);
