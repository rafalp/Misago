import LinkDropdownToggle from 'misago/components/link-dropdown-toggle';

export default LinkDropdownToggle.extend({
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
  }.property('route', 'params.@each'),

  click: function() {
    this.get('navbar-dropdown').toggle(this.get('dropdown'), this.get('model'));
    return false;
  }
});
