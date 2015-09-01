import RequestLinkRoute from 'misago/routes/activation/index';

export default RequestLinkRoute.extend({
  formTitle: gettext('Change forgotten password'),
  formTemplate: 'forgotten-password.request-link',

  sentTitle: gettext('Change password form link sent'),
  sentTemplate: 'forgotten-password.link-sent'
});
