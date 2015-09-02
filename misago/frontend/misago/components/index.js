(function (Misago) {
  'use strict';

  var self = {
    controller: function() {
      var _ = self.container;
      _.setTitle(_.settings.forum_index_title);
    },
    view: function() {
      return m('.container', [
        m('h1', 'Forum index page!'),
        m('p', 'Lorem ipsum dolor met sit amet elit.'),
        m('p', 'Sequar elit dolor nihi putto.')
      ]);
    }
  };
  Misago.IndexPage = self;
}(Misago.prototype));
