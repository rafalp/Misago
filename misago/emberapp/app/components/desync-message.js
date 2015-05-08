import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'desync-message',
  classNameBindings: ['auth.needsSync:visible']
});
