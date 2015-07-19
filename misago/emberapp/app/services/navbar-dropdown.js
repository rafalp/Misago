import Ember from 'ember';

export default Ember.Service.extend({
  activeComponent: 'empty-modal',
  activeModel: null,
  isOpen: false,

  toggle: function(component, model) {
    if (this.get('activeComponent') === component) {
      this.hide();
    } else {
      this.setProperties({
        activeComponent: component,
        activeModel: model,
        isOpen: true
      });
    }

    // Reset scroll so opened dropdown is visible in viewport
    window.scrollTo(0,0);
  },

  hide: function() {
    this.setProperties({
      activeComponent: 'empty-modal',
      activeModel: null,
      isOpen: false
    });
  }
});
