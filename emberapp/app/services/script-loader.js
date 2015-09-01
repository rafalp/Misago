import Ember from 'ember';

export default Ember.Service.extend({
  require: function(script, remote) {
    var url = script;
    if (!remote) {
      url = this.get('staticUrl') + url;
    }

    Ember.$.ajax({
      url: url,
      cache: true,
      dataType: 'script'
    });
  }
});
