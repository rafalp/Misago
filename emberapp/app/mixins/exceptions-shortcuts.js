import Ember from 'ember';

export default Ember.Mixin.create({
  // Shorthands for raising errors
  throw403: function(reason) {
    if (reason) {
      throw {
        status: 403,
        responseJSON: {
          detail: reason
        }
      };
    } else {
      throw { status: 403 };
    }
  },

  throw404: function() {
    throw { status: 404 };
  }
});
