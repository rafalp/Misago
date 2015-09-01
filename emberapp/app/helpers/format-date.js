import Ember from 'ember';

export function formatDate(moment, options) {
  if (moment) {
    return moment.format(options.hash.format || 'LL, LT');
  } else {
    return gettext('never');
  }
}

export default Ember.Handlebars.makeBoundHelper(formatDate);
