/*
Handlebars helpers for calling djangojs translation functions

gettext = function (msgid) { return msgid; };
ngettext = function (singular, plural, count) { return (count == 1) ? singular : plural; };
gettext_noop = function (msgid) { return msgid; };
pgettext = function (context, msgid) { return msgid; };
npgettext = function (context, singular, plural, count) { return (count == 1) ? singular : plural; };
django.interpolate = function (fmt, obj, named);
*/

Ember.Handlebars.registerBoundHelper('gettext', function(msgid, options) {
  if (Object.getOwnPropertyNames(options.hash).length > 0) {
    return interpolate(gettext(msgid), options.hash, true);
  } else {
    return gettext(msgid);
  }
});

Ember.Handlebars.registerBoundHelper('ngettext', function(singular, plural, count, options) {
  options.hash['count'] = count
  return interpolate(ngettext(singular, plural, count), options.hash, true);
});

Ember.Handlebars.registerBoundHelper('gettext_noop', function(msgid, options) {
  if (Object.getOwnPropertyNames(options.hash).length > 0) {
    return interpolate(gettext_noop(msgid), options.hash, true);
  } else {
    return gettext_noop(msgid);
  }
});

Ember.Handlebars.registerBoundHelper('pgettext', function(context, msgid, options) {
  if (Object.getOwnPropertyNames(options.hash).length > 0) {
    return interpolate(pgettext(context, msgid), options.hash, true);
  } else {
    return pgettext(context, msgid);
  }
});

Ember.Handlebars.registerBoundHelper('npgettext', function(context, singular, plural, count, options) {
  return interpolate(npgettext(context, singular, plural, count), options.hash, true);
});
