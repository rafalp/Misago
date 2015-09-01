import Ember from 'ember';

export default Ember.Mixin.create({
  url_name: function() {
    return this.get('slug') + '-' + this.get('id');
  }.property('id', 'slug')
});
