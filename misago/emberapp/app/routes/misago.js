import Ember from 'ember';
import DocumentTitle from 'misago/mixins/document-title';
import ResetScroll from 'misago/mixins/reset-scroll';

export default Ember.Route.extend(DocumentTitle, ResetScroll);
