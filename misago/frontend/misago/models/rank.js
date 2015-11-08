(function (Misago) {
  'use strict';

  var Rank = function(data) {
    this.id = data.id;

    this.name = data.name;
    this.slug = data.slug;

    this.description = data.description;

    this.title = data.title;
    this.css_class = data.css_class;

    this.is_tab = data.is_tab;
  };

  Misago.addService('model:rank', function(_) {
    _.models.add('rank', {
      class: Rank
    });
  },
  {
    after: 'models'
  });
} (Misago.prototype));
