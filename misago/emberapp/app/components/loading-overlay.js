import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['loading-overlay', 'fade'],
  classNameBindings: ['_visible:in'],

  visible: false,
  itemName: null,
  activeItem: null,

  _visible: function() {
    if (this.get('itemName')) {
      return this.get('itemName') === this.get('activeItem');
    } else {
      return this.get('visible');
    }
  }.property('visible', 'itemName', 'activeItem'),

  selector: 'img',

  positionOverlay: function() {
    var $target = this.$().parent().find(this.get('selector'));

    var self = this;
    var _positionOverlay = function($target) {
      if (self.isDestroyed) { return; }
      // see if image was loaded
      if ($target.width() === 0 || $target.height() === 0) {
        Ember.run.later(function () {
          _positionOverlay($target);
        }, 200);
      } else {
        self.$().find('.overlay-icon').width($target.width());
        self.$().find('.overlay-icon').height($target.height());
      }
    };

    _positionOverlay($target);
  }.on('didInsertElement')
});
