import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  beforeModel: function() {
    if (!this.auth.get('user.acl.can_browse_users_list')) {
      this.throw403(gettext("You can't browse users list."));
    }
  },

  model: function() {
    return this.store.find('rank');
  }
});
