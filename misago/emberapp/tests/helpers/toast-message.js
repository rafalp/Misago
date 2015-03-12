import Ember from 'ember';

export default function getToastMessage() {
  return Ember.$.trim(find('.toast-message p').text());
}
