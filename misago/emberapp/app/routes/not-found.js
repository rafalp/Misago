import MisagoRoute from 'misago/routes/misago';
import ResetScroll from 'misago/mixins/reset-scroll';

export default MisagoRoute.extend(ResetScroll, {
  actions: {
    didTransition: function() {
      // Not found route transitions to error404
      throw {status: 404};
    }
  }
});
