import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['toast-message'],
  classNameBindings: ['toast.isVisible:visible'],
});
