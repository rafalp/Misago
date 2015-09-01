import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'a',

  attributeBindings: ['href', 'toggle:data-toggle', 'expanded:aria-expanded'],
  classNames: 'dropdown-toggle',
  toggle: 'dropdown',
  expanded: 'false',
  ariaRoleString: 'button',

  href: function() {
    var router = this.container.lookup('router:main');

    var route = this.get('route');
    var params = this.get('params');

    return router.generate(route, params);
  }.property('route', 'params.@each')
});
