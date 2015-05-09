import Ember from 'ember';
import ModalComponent from 'misago/mixins/modal-component';

export default Ember.Component.extend(ModalComponent, {
  className: 'modal-change-avatar',

  hello: function() {
    console.log('hello!');
  }.on('didInsertElement'),

  bye: function() {
    console.log('bubai!');
  }.on('willDestroyElement')
});
