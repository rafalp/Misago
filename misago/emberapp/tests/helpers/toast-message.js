import Ember from 'ember';

export default function getToastMessage() {
  return Ember.$.trim(Ember.$('.toast-message p').text());
}
