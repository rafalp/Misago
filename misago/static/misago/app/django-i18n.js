/*
Handlebars helpers for calling djangojs translation functions

gettext = function (msgid) { return msgid; };
ngettext = function (singular, plural, count) { return (count == 1) ? singular : plural; };
gettext_noop = function (msgid) { return msgid; };
pgettext = function (context, msgid) { return msgid; };
npgettext = function (context, singular, plural, count) { return (count == 1) ? singular : plural; };
django.interpolate = function (fmt, obj, named);
*/


(function() {

  var registerHelper = Ember.HTMLBars.registerHelper;
  var makeBoundHelper = Ember.HTMLBars.makeBoundHelper;

  registerHelper('gettext', makeBoundHelper(function(args, kwargs) {

    var msgid = args[0];
    console.log(kwargs);

    if (Object.getOwnPropertyNames(kwargs).length > 0) {
      return interpolate(gettext(msgid), kwargs, true);
    } else {
      return gettext(msgid);
    }

  }));

  registerHelper('ngettext', makeBoundHelper(function(args, kwargs) {

    var singular = args[0];
    var plural = args[1];
    var count = args[2];

    kwargs.count = count;

    return interpolate(ngettext(singular, plural, count), kwargs, true);
  }));

  registerHelper('gettext_noop', makeBoundHelper(function(args, kwargs) {

    var msgid = args[0];

    if (Object.getOwnPropertyNames(kwargs).length > 0) {
      return interpolate(gettext_noop(msgid), kwargs, true);
    } else {
      return gettext_noop(msgid);
    }
  }));

  registerHelper('pgettext', makeBoundHelper(function(args, kwargs) {

    var context = args[0];
    var msgid = args[1];

    if (Object.getOwnPropertyNames(kwargs).length > 0) {
      return interpolate(pgettext(context, msgid), kwargs, true);
    } else {
      return pgettext(context, msgid);
    }
  }));

  registerHelper('npgettext', makeBoundHelper(function(args, kwargs) {

    var context = args[0];
    var singular = args[1];
    var plural = args[2];
    var count = args[3];

    kwargs.count = count;

    return interpolate(npgettext(context, singular, plural, count), kwargs, true);
  }));

}());

