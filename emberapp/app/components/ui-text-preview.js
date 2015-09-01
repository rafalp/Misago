import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'span',

  minLength: 3,
  maxLength: 10,

  fillWithRandomText: function() {
    var targetLen = Math.floor(Math.random() * (this.get('maxLength') - this.get('minLength')));
    targetLen += this.get('minLength');

    var htmlFiller = '';
    for (var i = 0; i <= targetLen; i ++) {
      htmlFiller += '&nbsp;&nbsp;';
    }

    this.$().html(htmlFiller);
  }.on('didInsertElement')
});
