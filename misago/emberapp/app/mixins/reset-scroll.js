import Ember from 'ember';

export default Ember.Mixin.create({
  resetScroll: function() {
    window.scrollTo(0,0);
  }.on('activate')
});
