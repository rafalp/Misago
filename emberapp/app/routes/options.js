import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  beforeModel: function() {
    this.auth.denyAnonymous(gettext('You have to sign in to change options.'));
  }
});
