import Ember from 'ember';

export default function destroyModal() {
  Ember.$('#appModal').off();
  Ember.$('body').removeClass('modal-open');
  Ember.$('.modal-backdrop').remove();
}
