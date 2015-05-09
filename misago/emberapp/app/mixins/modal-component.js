import Ember from 'ember';

export default Ember.Mixin.create({
  classNames: 'modal-dialog',
  classNameBindings: ['isSmall:modal-sm', 'isLarge:modal-lg', 'className'],

  isSmall: false,
  isLarge: false,

  className: 'misago-modal'
});
