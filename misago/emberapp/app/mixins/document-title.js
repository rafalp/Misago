/* jshint unused:false */
import Ember from 'ember';

export default Ember.Mixin.create({
  title: Ember.computed({
    get(key) {
      return document.title;
    },
    set(key, value) {
      this._changeTitle(value);
    }
  }),

  _changeTitle: function(title) {
    if (typeof title === 'string') {
      title = {title: title};
    }

    var complete_title = title.title;

    if (typeof title.page !== 'undefined') {
      complete_title += ' (' + interpolate(gettext('page %(page)s'), {page:title.page}, true) + ')';
    }

    if (typeof title.parent !== 'undefined') {
      complete_title += ' | ' + title.parent;
    }

    document.title = complete_title + ' | ' + this.get('settings.forum_name');
  }
});
