import Ember from 'ember';

export function initialize() {
  moment.locale(Ember.$('html').attr('lang'));
}

export default {
  name: 'moment-locale',
  initialize: initialize
};
