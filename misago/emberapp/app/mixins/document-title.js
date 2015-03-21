import Ember from 'ember';

export default Ember.Mixin.create({
  title: function(key, value) {
    // setter
    if (arguments.length > 1) {
      this._changeTitle(value);
    }

    // getter
    return document.title;
  }.property(),

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

    complete_title += ' | ' + this.get('settings.forum_name');

    document.title = complete_title;
  }
});
