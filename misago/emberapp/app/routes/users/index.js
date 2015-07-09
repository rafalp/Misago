import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  redirect: function() {
    return this.transitionTo('users.active');
  }
});
