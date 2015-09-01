import Ember from 'ember';

export function relativeDate(date) {
  if (date) {
    var days = moment().diff(date, 'days');

    if (days === 0) {
      var hours = moment().diff(date, 'hours');
      if (hours < 5){
        return date.fromNow();
      } else {
        return date.format('LT');
      }
    } else if (days < 7) {
      return moment(date).add(7, 'd').calendar();// tiny trick to get rid of "last"
    } else {
      var years = moment().diff(date, 'years');
      if (years) {
        return date.format('D MMM YYYY');
      } else {
        return date.format('D MMM');
      }
    }
  } else {
    return gettext('never');
  }
}

export default Ember.Handlebars.makeBoundHelper(relativeDate);
