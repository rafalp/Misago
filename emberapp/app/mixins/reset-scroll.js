import Ember from 'ember';

export default Ember.Mixin.create({
  scrollToTop: true,

  _resetScroll: function() {
    if (this.get('scrollToTop')) {
      window.scrollTo(0,0);
    }
  }.on('activate')
});
