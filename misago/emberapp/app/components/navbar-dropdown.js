import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['compact-navbar-dropdown', 'hidden-md', 'hidden-lg'],

  dropdown: Ember.computed.alias('navbar-dropdown'),

  closeOnLinkClick: function() {
    var self = this;
    Ember.$(document).on('click.misagoNavbarDropdown', function() {
      self.get('navbar-dropdown').hide();
    });
  }.on('didInsertElement'),

  removeClickDelegation: function() {
    Ember.$(document).off('click.misagoNavbarDropdown');
  }.on('willDestroyElement')
});
