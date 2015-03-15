import RequestLinkRoute from 'misago/routes/activation/index';

export default RequestLinkRoute.extend({
  title: gettext('Change forgotten password'),
  templateName: 'forgotten-password.request-link',

  sentTitle: gettext('Change password form link sent'),
  sentTemplateName: 'forgotten-password.link-sent'
});
