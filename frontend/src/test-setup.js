var jQuery = require('jQuery'); // jshint ignore:line

global.$ = jQuery;
global.jQuery = jQuery;

require('bootstrap-transition');
require('bootstrap-affix');
require('bootstrap-modal');
require('bootstrap-dropdown');

require('jquery-mockjax')(jQuery, window);
$.mockjaxSettings.logging = false;
$.mockjaxSettings.responseTime = 100;

require("babel-polyfill");

// Mock base href element
$('head').append('<base href="/test-runner/">');

// Bootstrap's modal (we'll need it anyway for tests);
$('body').append('<div class="modal fade" id="modal-mount" tabindex="-1" role="dialog" aria-labelledby="misago-modal-label"></div>');
$('body').append('<div id="dropdown-mount"></div>');
$('body').append('<div id="page-mount"></div>');
$('body').append('<div id="test-mount"></div>');

// set global utility function for cleaning test containers
var ReactDOM = require('react-dom');
global.emptyTestContainers = function() {
  ReactDOM.unmountComponentAtNode(document.getElementById('dropdown-mount'));
  ReactDOM.unmountComponentAtNode(document.getElementById('modal-mount'));
  ReactDOM.unmountComponentAtNode(document.getElementById('page-mount'));
  ReactDOM.unmountComponentAtNode(document.getElementById('test-mount'));
};

// global utility for mocking context
global.contextClear = function(misago) {
  misago._context = {};
};

global.contextGuest = function(misago) {
  misago._context = Object.assign({}, misago._context, {
    isAuthenticated: false,

    user: {
      id : null,

      acl: {}
    }
  });
};

global.contextAuthenticated = function(misago, overrides) {
  misago._context = Object.assign({}, misago._context, {
    isAuthenticated: true,

    user: {
      id : 42,
      absolute_url: "/user/loremipsum-1/",
      avatar_hash: "5c6a04b4",
      email: "test@example.com",
      full_title: "Forum team",
      is_hiding_presence: false,
      joined_on: "2015-05-09T16:13:33.973603Z",
      limits_private_thread_invites_to: 0,
      new_notifications: 0,
      posts: 30,
      rank: {
        id: 1,

        css_class: "team",
        description: '<p>Lorem ipsum dolor met sit amet elit, si vis pacem para bellum.</p>\n<p>To help see <a href="http://wololo.com/something.php?page=2131">http://wololo.com/something.php?page=2131</a></p>',
        is_tab: true,
        name: "Forum team",
        slug: "forum-team",
        title: "Team"
      },
      short_title: "Team",
      slug: "loremipsum",
      subscribe_to_replied_threads: 2,
      subscribe_to_started_threads: 1,
      threads: 0,
      title: "",
      unread_private_threads: 0,
      username: "LoremIpsum",

      acl: {}
    }
  });

  if (overrides) {
    Object.assign(misago._context.user, overrides);
  }
};

// global utility function for store mocking
global.initEmptyStore = function(store) {
  store.constructor();
  store.addReducer('test', function(state={}, action=null) { return {}; }, {}); // jshint ignore:line
  store.init();
};

global.snackbarStoreMock = function() {
  return {
    message: [],

    dispatch: function(action) {
      if (action.type === 'SHOW_SNACKBAR') {
        this.message = {
          message: action.message,
          type: action.messageType
        };
      }
    }
  };
};

// global init function for modal and dropdown services
global.initModal = function(modal) {
  modal.init(document.getElementById('modal-mount'));
};

global.initDropdown = function(dropdown) {
  dropdown.init(document.getElementById('dropdown-mount'));
};

// global util functions for events
var ReactTestUtils = require('react-addons-test-utils');
global.simulateClick = function(selector) {
  if ($(selector).length) {
    ReactTestUtils.Simulate.click($(selector).get(0));
  } else {
    throw 'selector "' + selector + '" did not match anything';
  }
};

global.simulateSubmit = function(selector) {
  if ($(selector).length) {
    ReactTestUtils.Simulate.submit($(selector).get(0));
  } else {
    throw 'selector "' + selector + '" did not match anything';
  }
};

global.simulateChange = function(selector, value) {
  if ($(selector).length) {
    $(selector).val(value);
    ReactTestUtils.Simulate.change($(selector).get(0));
  } else {
    throw 'selector "' + selector + '" did not match anything';
  }
};

global.afterAjax = function(component, callback) {
  window.setTimeout(function() {
    component.forceUpdate(callback);
  }, 200);
};

global.onElement = function(selector, callback) {
  var _getElement = function() {
    window.setTimeout(function() {
      var element = $(selector);
      if (element.length >= 1) {
        callback(element);
      } else {
        _getElement();
      }
    }, 50);
  };

  _getElement();
};

// inlined gettext functions form Django
// jshint ignore: start
(function (globals) {

  var django = globals.django || (globals.django = {});

  django.pluralidx = function (count) { return (count == 1) ? 0 : 1; };

  /* gettext identity library */

  django.gettext = function (msgid) { return msgid; };
  django.ngettext = function (singular, plural, count) { return (count == 1) ? singular : plural; };
  django.gettext_noop = function (msgid) { return msgid; };
  django.pgettext = function (context, msgid) { return msgid; };
  django.npgettext = function (context, singular, plural, count) { return (count == 1) ? singular : plural; };


  django.interpolate = function (fmt, obj, named) {
    if (named) {
      return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
    } else {
      return fmt.replace(/%s/g, function(match){return String(obj.shift())});
    }
  };


  /* formatting library */

  django.formats = {
    "DATETIME_FORMAT": "N j, Y, P",
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d",
      "%m/%d/%Y %H:%M:%S",
      "%m/%d/%Y %H:%M:%S.%f",
      "%m/%d/%Y %H:%M",
      "%m/%d/%Y",
      "%m/%d/%y %H:%M:%S",
      "%m/%d/%y %H:%M:%S.%f",
      "%m/%d/%y %H:%M",
      "%m/%d/%y"
    ],
    "DATE_FORMAT": "N j, Y",
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d",
      "%m/%d/%Y",
      "%m/%d/%y"
    ],
    "DECIMAL_SEPARATOR": ".",
    "FIRST_DAY_OF_WEEK": "0",
    "MONTH_DAY_FORMAT": "F j",
    "NUMBER_GROUPING": "3",
    "SHORT_DATETIME_FORMAT": "m/d/Y P",
    "SHORT_DATE_FORMAT": "m/d/Y",
    "THOUSAND_SEPARATOR": ",",
    "TIME_FORMAT": "P",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

  django.get_format = function (format_type) {
    var value = django.formats[format_type];
    if (typeof(value) == 'undefined') {
      return format_type;
    } else {
      return value;
    }
  };

  /* add to global namespace */
  window.pluralidx = django.pluralidx;
  window.gettext = django.gettext;
  window.ngettext = django.ngettext;
  window.gettext_noop = django.gettext_noop;
  window.pgettext = django.pgettext;
  window.npgettext = django.npgettext;
  window.interpolate = django.interpolate;
  window.get_format = django.get_format;

}(global));
// jshint ignore: end
