import Ember from 'ember';

export default Ember.Service.extend({
  indexTitle: '',
  forumName: '',

  init: function() {
    this.set('indexTitle', this.get('settings.forum_index_title'));
    this.set('forumName', this.get('settings.forum_name'));
  },

  setTitle: function(title) {
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

    complete_title += ' | ' + this.get('forumName');

    document.title = complete_title;
  },

  setPlaceholderTitle: function() {
    document.title = this.get('forumName');
  },

  setIndexTitle: function() {
    document.title = this.get('indexTitle') || this.get('forumName');
  }
});
