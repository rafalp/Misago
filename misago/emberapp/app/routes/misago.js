import Ember from 'ember';
import DocumentTitle from 'misago/mixins/document-title';
import ExceptionsShortcuts from 'misago/mixins/exceptions-shortcuts';
import ModelPagination from 'misago/mixins/model-pagination';
import ModelUrlName from 'misago/mixins/model-url-name';
import ResetScroll from 'misago/mixins/reset-scroll';

export default Ember.Route.extend(
  DocumentTitle,
  ExceptionsShortcuts,
  ModelPagination,
  ModelUrlName,
  ResetScroll
);
