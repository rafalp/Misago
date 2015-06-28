import Ember from 'ember';
import DocumentTitle from 'misago/mixins/document-title';
import ResetScroll from 'misago/mixins/reset-scroll';
import ModelUrlName from 'misago/mixins/model-url-name';

export default Ember.Route.extend(DocumentTitle, ResetScroll, ModelUrlName, {
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
