import Ember from 'ember';
import DocumentTitle from 'misago/mixins/document-title';
import ResetScroll from 'misago/mixins/reset-scroll';
import ModelUrlName from 'misago/mixins/model-url-name';

export default Ember.Route.extend(DocumentTitle, ResetScroll, ModelUrlName, {
  // Shorthand for validating page number
  cleanPage: function(page, transition) {
    var cleanPage = parseInt(page);
    if ("" + cleanPage === page && cleanPage > 0) {
      if (cleanPage > 1) {
        // return page number for an app
        return cleanPage;
      } else {
        // redirect to first page
        var routePath = transition.targetName.split('.');
        routePath[routePath.length - 1] = 'index';
        this.transitionTo(routePath.join('.'));
      }
    } else {
      this.throw404(); // not a valid page number
    }
  },

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
