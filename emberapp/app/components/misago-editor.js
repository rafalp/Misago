import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['misago-editor'],

  _ace: null,
  isLoaded: false,

  inputHeight: 200,
  toolbar: true,
  limit: 0,

  value: '',

  setupAce: function() {
    var aceLoader = this.container.lookup('service:ace-editor');
    var self = this;
    aceLoader.load().then(function() {
      if (self.isDestroyed) { return; }
      self.set('isLoaded', true);
      Ember.run.scheduleOnce('afterRender', function() {
        Ember.$('#editor-input').height(self.get('inputHeight') + 'px');
        var editor = aceLoader.edit('editor-input');

        // configure ace
        editor.$blockScrolling = Infinity;
        editor.getSession().setUseSoftTabs(true);
        editor.getSession().setTabSize(2);
        editor.getSession().setUseWrapMode(true);
        editor.setHighlightActiveLine(false);
        editor.renderer.setShowGutter(false);
        editor.getSession().setMode("ace/mode/markdown");

        editor.setValue(self.get('value'), 1);

        // set callbacks
        editor.getSession().on('change', function() {
            self.set('value', editor.getValue());
        });

        // store ace on component
        self.set('_ace', editor);
      });
    });
  }.on('didInsertElement'),

  destroyAce: function() {
    if (this.get('_ace')) {
      this.get('_ace').destroy();
    }
  }.on('willDestroyElement'),

  showLimitNote: function() {
    if (!this.get('limit')) {
      return false;
    } else {
      var len = this.get('value').length;
      return this.get('limit') * 0.8 <= len;
    }

  }.property('value', 'limit'),

  limitExceeded: function() {
    if (!this.get('limit')) {
      return false;
    } else {
      return this.get('limit') < this.get('value').length;
    }
  }.property('value', 'limit'),

  limitLeft: function() {
    if (!this.get('limit')) {
      return false;
    } else {
      return this.get('limit') - this.get('value').length;
    }
  }.property('value', 'limit')
});
