import Ember from 'ember';

export default Ember.Mixin.create({
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
      console.log('invalid page!');
      this.throw404(); // not a valid page number
    }
  },
});
