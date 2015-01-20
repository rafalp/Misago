import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    setTitle: function(title) {

      if (typeof title === "string") {
        title = {title: title};
      }

      var complete_title = title.title;
      complete_title += " | " + this.get('settings.forum_name');

      document.title = complete_title;
      return false;

    }
  }
});
