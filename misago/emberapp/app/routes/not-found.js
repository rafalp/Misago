import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  actions: {
    didTransition: function() {
      // Not found route transitions to error404
      throw {status: 404};
    }
  }
});
