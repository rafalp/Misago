(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
// shim for using process in browser

var process = module.exports = {};
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = setTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    clearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        setTimeout(drainQueue, 0);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };

},{}],2:[function(require,module,exports){
(function (global){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Misago = undefined;

var _orderedList = require('../../../../documents/misago/frontend/src/utils/ordered-list');

var _orderedList2 = _interopRequireDefault(_orderedList);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Misago = exports.Misago = function () {
  function Misago() {
    _classCallCheck(this, Misago);

    this._initializers = [];
    this._context = {};
  }

  _createClass(Misago, [{
    key: 'addInitializer',
    value: function addInitializer(initializer) {
      this._initializers.push({
        key: initializer.name,

        item: initializer.initializer,

        after: initializer.after,
        before: initializer.before
      });
    }
  }, {
    key: 'init',
    value: function init(context) {
      var _this = this;

      this._context = context;

      var initOrder = new _orderedList2.default(this._initializers).orderedValues();
      initOrder.forEach(function (initializer) {
        initializer(_this);
      });
    }

    // context accessors

  }, {
    key: 'has',
    value: function has(key) {
      return !!this._context[key];
    }
  }, {
    key: 'get',
    value: function get(key, fallback) {
      if (this.has(key)) {
        return this._context[key];
      } else {
        return fallback || undefined;
      }
    }
  }, {
    key: 'pop',
    value: function pop(key) {
      if (this.has(key)) {
        var value = this._context[key];
        this._context[key] = null;
        return value;
      } else {
        return undefined;
      }
    }
  }]);

  return Misago;
}();

// create  singleton

var misago = new Misago();

// expose it globally
global.misago = misago;

// and export it for tests and stuff
exports.default = misago;

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{"../../../../documents/misago/frontend/src/utils/ordered-list":106}],3:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _ajax = require('../../../../../documents/misago/frontend/src/services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _ajax2.default.init(_index2.default.get('CSRF_COOKIE_NAME'));
}

_index2.default.addInitializer({
  name: 'ajax',
  initializer: initializer
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/ajax":91}],4:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _reactRedux = require('react-redux');

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _authMessage = require('../../../../../documents/misago/frontend/src/components/auth-message');

var _authMessage2 = _interopRequireDefault(_authMessage);

var _mountComponent = require('../../../../../documents/misago/frontend/src/utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  (0, _mountComponent2.default)((0, _reactRedux.connect)(_authMessage.select)(_authMessage2.default), 'auth-message-mount');
}

_index2.default.addInitializer({
  name: 'component:auth-message',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/components/auth-message":48,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/utils/mount-component":105,"react-redux":"react-redux"}],5:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _auth = require('../../../../../documents/misago/frontend/src/reducers/auth');

var _auth2 = _interopRequireDefault(_auth);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  _store2.default.addReducer('auth', _auth2.default, Object.assign({
    'isAuthenticated': context.get('isAuthenticated'),
    'isAnonymous': !context.get('isAuthenticated'),

    'user': context.get('user')
  }, _auth.initialState));
}

_index2.default.addInitializer({
  name: 'reducer:auth',
  initializer: initializer,
  before: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/reducers/auth":86,"../../../../../documents/misago/frontend/src/services/store":100}],6:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _auth = require('../../../../../documents/misago/frontend/src/services/auth');

var _auth2 = _interopRequireDefault(_auth);

var _modal = require('../../../../../documents/misago/frontend/src/services/modal');

var _modal2 = _interopRequireDefault(_modal);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

var _localStorage = require('../../../../../documents/misago/frontend/src/services/local-storage');

var _localStorage2 = _interopRequireDefault(_localStorage);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _auth2.default.init(_store2.default, _localStorage2.default, _modal2.default);
}

_index2.default.addInitializer({
  name: 'auth',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/auth":92,"../../../../../documents/misago/frontend/src/services/local-storage":95,"../../../../../documents/misago/frontend/src/services/modal":97,"../../../../../documents/misago/frontend/src/services/store":100}],7:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _bannedPage = require('../../../../../documents/misago/frontend/src/utils/banned-page');

var _bannedPage2 = _interopRequireDefault(_bannedPage);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  if (context.has('BAN_MESSAGE')) {
    (0, _bannedPage2.default)(context.get('BAN_MESSAGE'), false);
  }
}

_index2.default.addInitializer({
  name: 'component:baned-page',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/utils/banned-page":102}],8:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _ajax = require('../../../../../documents/misago/frontend/src/services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _captcha = require('../../../../../documents/misago/frontend/src/services/captcha');

var _captcha2 = _interopRequireDefault(_captcha);

var _include = require('../../../../../documents/misago/frontend/src/services/include');

var _include2 = _interopRequireDefault(_include);

var _snackbar = require('../../../../../documents/misago/frontend/src/services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  _captcha2.default.init(context, _ajax2.default, _include2.default, _snackbar2.default);
}

_index2.default.addInitializer({
  name: 'captcha',
  initializer: initializer
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/ajax":91,"../../../../../documents/misago/frontend/src/services/captcha":93,"../../../../../documents/misago/frontend/src/services/include":94,"../../../../../documents/misago/frontend/src/services/snackbar":99}],9:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _include = require('../../../../../documents/misago/frontend/src/services/include');

var _include2 = _interopRequireDefault(_include);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  _include2.default.init(context.get('STATIC_URL'));
}

_index2.default.addInitializer({
  name: 'include',
  initializer: initializer
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/include":94}],10:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _localStorage = require('../../../../../documents/misago/frontend/src/services/local-storage');

var _localStorage2 = _interopRequireDefault(_localStorage);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _localStorage2.default.init('misago_');
}

_index2.default.addInitializer({
  name: 'local-storage',
  initializer: initializer
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/local-storage":95}],11:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _mobileNavbarDropdown = require('../../../../../documents/misago/frontend/src/services/mobile-navbar-dropdown');

var _mobileNavbarDropdown2 = _interopRequireDefault(_mobileNavbarDropdown);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  var element = document.getElementById('mobile-navbar-dropdown-mount');
  if (element) {
    _mobileNavbarDropdown2.default.init(element);
  }
}

_index2.default.addInitializer({
  name: 'dropdown',
  initializer: initializer,
  before: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/mobile-navbar-dropdown":96}],12:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _modal = require('../../../../../documents/misago/frontend/src/services/modal');

var _modal2 = _interopRequireDefault(_modal);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  var element = document.getElementById('modal-mount');
  if (element) {
    _modal2.default.init(element);
  }
}

_index2.default.addInitializer({
  name: 'modal',
  initializer: initializer,
  before: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/modal":97}],13:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _moment2.default.locale($('html').attr('lang'));
}

_index2.default.addInitializer({
  name: 'moment',
  initializer: initializer
});

},{"../../../../../documents/misago/frontend/src/index":85,"moment":"moment"}],14:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _root = require('../../../../../documents/misago/frontend/src/components/options/root');

var _root2 = _interopRequireDefault(_root);

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

var _routedComponent = require('../../../../../documents/misago/frontend/src/utils/routed-component');

var _routedComponent2 = _interopRequireDefault(_routedComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  if (context.has('USER_OPTIONS')) {
    (0, _routedComponent2.default)({
      root: _index2.default.get('USERCP_URL'),
      component: _root2.default,
      paths: (0, _root.paths)(_store2.default)
    });
  }
}

_index2.default.addInitializer({
  name: 'component:options',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/components/options/root":65,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/store":100,"../../../../../documents/misago/frontend/src/utils/routed-component":108}],15:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _pageTitle = require('../../../../../documents/misago/frontend/src/services/page-title');

var _pageTitle2 = _interopRequireDefault(_pageTitle);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  _pageTitle2.default.init(context.get('SETTINGS').forum_name);
}

_index2.default.addInitializer({
  name: 'page-title',
  initializer: initializer
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/page-title":98}],16:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _requestActivationLink = require('../../../../../documents/misago/frontend/src/components/request-activation-link');

var _requestActivationLink2 = _interopRequireDefault(_requestActivationLink);

var _mountComponent = require('../../../../../documents/misago/frontend/src/utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  if (document.getElementById('request-activation-link-mount')) {
    (0, _mountComponent2.default)(_requestActivationLink2.default, 'request-activation-link-mount', false);
  }
}

_index2.default.addInitializer({
  name: 'component:request-activation-link',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/components/request-activation-link":70,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/utils/mount-component":105}],17:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _requestPasswordReset = require('../../../../../documents/misago/frontend/src/components/request-password-reset');

var _requestPasswordReset2 = _interopRequireDefault(_requestPasswordReset);

var _mountComponent = require('../../../../../documents/misago/frontend/src/utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  if (document.getElementById('request-password-reset-mount')) {
    (0, _mountComponent2.default)(_requestPasswordReset2.default, 'request-password-reset-mount', false);
  }
}

_index2.default.addInitializer({
  name: 'component:request-password-reset',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/components/request-password-reset":71,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/utils/mount-component":105}],18:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _resetPasswordForm = require('../../../../../documents/misago/frontend/src/components/reset-password-form');

var _resetPasswordForm2 = _interopRequireDefault(_resetPasswordForm);

var _mountComponent = require('../../../../../documents/misago/frontend/src/utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  if (document.getElementById('reset-password-form-mount')) {
    (0, _mountComponent2.default)(_resetPasswordForm2.default, 'reset-password-form-mount', false);
  }
}

_index2.default.addInitializer({
  name: 'component:reset-password-form',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/components/reset-password-form":72,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/utils/mount-component":105}],19:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _reactRedux = require('react-redux');

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _snackbar = require('../../../../../documents/misago/frontend/src/components/snackbar');

var _mountComponent = require('../../../../../documents/misago/frontend/src/utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  (0, _mountComponent2.default)((0, _reactRedux.connect)(_snackbar.select)(_snackbar.Snackbar), 'snackbar-mount');
}

_index2.default.addInitializer({
  name: 'component:snackbar',
  initializer: initializer,
  after: 'snackbar'
});

},{"../../../../../documents/misago/frontend/src/components/snackbar":75,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/utils/mount-component":105,"react-redux":"react-redux"}],20:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _snackbar = require('../../../../../documents/misago/frontend/src/reducers/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _store2.default.addReducer('snackbar', _snackbar2.default, _snackbar.initialState);
}

_index2.default.addInitializer({
  name: 'reducer:snackbar',
  initializer: initializer,
  before: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/reducers/snackbar":87,"../../../../../documents/misago/frontend/src/services/store":100}],21:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _snackbar = require('../../../../../documents/misago/frontend/src/services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _snackbar2.default.init(_store2.default);
}

_index2.default.addInitializer({
  name: 'snackbar',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/snackbar":99,"../../../../../documents/misago/frontend/src/services/store":100}],22:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _store2.default.init();
}

_index2.default.addInitializer({
  name: 'store',
  initializer: initializer,
  before: '_end'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/store":100}],23:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _tick = require('../../../../../documents/misago/frontend/src/reducers/tick');

var _tick2 = _interopRequireDefault(_tick);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _store2.default.addReducer('tick', _tick2.default, _tick.initialState);
}

_index2.default.addInitializer({
  name: 'reducer:tick',
  initializer: initializer,
  before: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/reducers/tick":88,"../../../../../documents/misago/frontend/src/services/store":100}],24:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _tick = require('../../../../../documents/misago/frontend/src/reducers/tick');

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var TICK_PERIOD = 50 * 1000; //do the tick every 50s

function initializer() {
  window.setInterval(function () {
    _store2.default.dispatch((0, _tick.doTick)());
  }, TICK_PERIOD);
}

_index2.default.addInitializer({
  name: 'tick-start',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/reducers/tick":88,"../../../../../documents/misago/frontend/src/services/store":100}],25:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _reactRedux = require('react-redux');

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _root = require('../../../../../documents/misago/frontend/src/components/user-menu/root');

var _mountComponent = require('../../../../../documents/misago/frontend/src/utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  (0, _mountComponent2.default)((0, _reactRedux.connect)(_root.select)(_root.UserMenu), 'user-menu-mount');
  (0, _mountComponent2.default)((0, _reactRedux.connect)(_root.select)(_root.CompactUserMenu), 'user-menu-compact-mount');
}

_index2.default.addInitializer({
  name: 'component:user-menu',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/components/user-menu/root":77,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/utils/mount-component":105,"react-redux":"react-redux"}],26:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _usernameHistory = require('../../../../../documents/misago/frontend/src/reducers/username-history');

var _usernameHistory2 = _interopRequireDefault(_usernameHistory);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _store2.default.addReducer('username-history', _usernameHistory2.default, []);
}

_index2.default.addInitializer({
  name: 'reducer:username-history',
  initializer: initializer,
  before: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/reducers/username-history":89,"../../../../../documents/misago/frontend/src/services/store":100}],27:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _root = require('../../../../../documents/misago/frontend/src/components/users/root');

var _root2 = _interopRequireDefault(_root);

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

var _routedComponent = require('../../../../../documents/misago/frontend/src/utils/routed-component');

var _routedComponent2 = _interopRequireDefault(_routedComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  if (context.has('USERS_LISTS')) {
    (0, _routedComponent2.default)({
      root: _index2.default.get('USERS_LIST_URL'),
      component: _root2.default,
      paths: (0, _root.paths)(_store2.default)
    });
  }
}

_index2.default.addInitializer({
  name: 'component:users',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/components/users/root":83,"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/store":100,"../../../../../documents/misago/frontend/src/utils/routed-component":108}],28:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _users = require('../../../../../documents/misago/frontend/src/reducers/users');

var _users2 = _interopRequireDefault(_users);

var _store = require('../../../../../documents/misago/frontend/src/services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _store2.default.addReducer('users', _users2.default, []);
}

_index2.default.addInitializer({
  name: 'reducer:users',
  initializer: initializer,
  before: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/reducers/users":90,"../../../../../documents/misago/frontend/src/services/store":100}],29:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../../../../../documents/misago/frontend/src/index');

var _index2 = _interopRequireDefault(_index);

var _include = require('../../../../../documents/misago/frontend/src/services/include');

var _include2 = _interopRequireDefault(_include);

var _zxcvbn = require('../../../../../documents/misago/frontend/src/services/zxcvbn');

var _zxcvbn2 = _interopRequireDefault(_zxcvbn);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _zxcvbn2.default.init(_include2.default);
}

_index2.default.addInitializer({
  name: 'zxcvbn',
  initializer: initializer
});

},{"../../../../../documents/misago/frontend/src/index":85,"../../../../../documents/misago/frontend/src/services/include":94,"../../../../../documents/misago/frontend/src/services/zxcvbn":101}],30:[function(require,module,exports){
var pSlice = Array.prototype.slice;
var objectKeys = require('./lib/keys.js');
var isArguments = require('./lib/is_arguments.js');

var deepEqual = module.exports = function (actual, expected, opts) {
  if (!opts) opts = {};
  // 7.1. All identical values are equivalent, as determined by ===.
  if (actual === expected) {
    return true;

  } else if (actual instanceof Date && expected instanceof Date) {
    return actual.getTime() === expected.getTime();

  // 7.3. Other pairs that do not both pass typeof value == 'object',
  // equivalence is determined by ==.
  } else if (!actual || !expected || typeof actual != 'object' && typeof expected != 'object') {
    return opts.strict ? actual === expected : actual == expected;

  // 7.4. For all other Object pairs, including Array objects, equivalence is
  // determined by having the same number of owned properties (as verified
  // with Object.prototype.hasOwnProperty.call), the same set of keys
  // (although not necessarily the same order), equivalent values for every
  // corresponding key, and an identical 'prototype' property. Note: this
  // accounts for both named and indexed properties on Arrays.
  } else {
    return objEquiv(actual, expected, opts);
  }
}

function isUndefinedOrNull(value) {
  return value === null || value === undefined;
}

function isBuffer (x) {
  if (!x || typeof x !== 'object' || typeof x.length !== 'number') return false;
  if (typeof x.copy !== 'function' || typeof x.slice !== 'function') {
    return false;
  }
  if (x.length > 0 && typeof x[0] !== 'number') return false;
  return true;
}

function objEquiv(a, b, opts) {
  var i, key;
  if (isUndefinedOrNull(a) || isUndefinedOrNull(b))
    return false;
  // an identical 'prototype' property.
  if (a.prototype !== b.prototype) return false;
  //~~~I've managed to break Object.keys through screwy arguments passing.
  //   Converting to array solves the problem.
  if (isArguments(a)) {
    if (!isArguments(b)) {
      return false;
    }
    a = pSlice.call(a);
    b = pSlice.call(b);
    return deepEqual(a, b, opts);
  }
  if (isBuffer(a)) {
    if (!isBuffer(b)) {
      return false;
    }
    if (a.length !== b.length) return false;
    for (i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) return false;
    }
    return true;
  }
  try {
    var ka = objectKeys(a),
        kb = objectKeys(b);
  } catch (e) {//happens when one is a string literal and the other isn't
    return false;
  }
  // having the same number of owned properties (keys incorporates
  // hasOwnProperty)
  if (ka.length != kb.length)
    return false;
  //the same set of keys (although not necessarily the same order),
  ka.sort();
  kb.sort();
  //~~~cheap key test
  for (i = ka.length - 1; i >= 0; i--) {
    if (ka[i] != kb[i])
      return false;
  }
  //equivalent values for every corresponding key, and
  //~~~possibly expensive deep test
  for (i = ka.length - 1; i >= 0; i--) {
    key = ka[i];
    if (!deepEqual(a[key], b[key], opts)) return false;
  }
  return typeof a === typeof b;
}

},{"./lib/is_arguments.js":31,"./lib/keys.js":32}],31:[function(require,module,exports){
var supportsArgumentsClass = (function(){
  return Object.prototype.toString.call(arguments)
})() == '[object Arguments]';

exports = module.exports = supportsArgumentsClass ? supported : unsupported;

exports.supported = supported;
function supported(object) {
  return Object.prototype.toString.call(object) == '[object Arguments]';
};

exports.unsupported = unsupported;
function unsupported(object){
  return object &&
    typeof object == 'object' &&
    typeof object.length == 'number' &&
    Object.prototype.hasOwnProperty.call(object, 'callee') &&
    !Object.prototype.propertyIsEnumerable.call(object, 'callee') ||
    false;
};

},{}],32:[function(require,module,exports){
exports = module.exports = typeof Object.keys === 'function'
  ? Object.keys : shim;

exports.shim = shim;
function shim (obj) {
  var keys = [];
  for (var key in obj) keys.push(key);
  return keys;
}

},{}],33:[function(require,module,exports){
/**
 * Indicates that navigation was caused by a call to history.push.
 */
'use strict';

exports.__esModule = true;
var PUSH = 'PUSH';

exports.PUSH = PUSH;
/**
 * Indicates that navigation was caused by a call to history.replace.
 */
var REPLACE = 'REPLACE';

exports.REPLACE = REPLACE;
/**
 * Indicates that navigation was caused by some other action such
 * as using a browser's back/forward buttons and/or manually manipulating
 * the URL in a browser's location bar. This is the default.
 *
 * See https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onpopstate
 * for more information.
 */
var POP = 'POP';

exports.POP = POP;
exports['default'] = {
  PUSH: PUSH,
  REPLACE: REPLACE,
  POP: POP
};
},{}],34:[function(require,module,exports){
"use strict";

exports.__esModule = true;
exports.loopAsync = loopAsync;

function loopAsync(turns, work, callback) {
  var currentTurn = 0;
  var isDone = false;

  function done() {
    isDone = true;
    callback.apply(this, arguments);
  }

  function next() {
    if (isDone) return;

    if (currentTurn < turns) {
      work.call(this, currentTurn++, next, done);
    } else {
      done.apply(this, arguments);
    }
  }

  next();
}
},{}],35:[function(require,module,exports){
(function (process){
/*eslint-disable no-empty */
'use strict';

exports.__esModule = true;
exports.saveState = saveState;
exports.readState = readState;

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _warning = require('warning');

var _warning2 = _interopRequireDefault(_warning);

var KeyPrefix = '@@History/';
var QuotaExceededError = 'QuotaExceededError';
var SecurityError = 'SecurityError';

function createKey(key) {
  return KeyPrefix + key;
}

function saveState(key, state) {
  try {
    window.sessionStorage.setItem(createKey(key), JSON.stringify(state));
  } catch (error) {
    if (error.name === SecurityError) {
      // Blocking cookies in Chrome/Firefox/Safari throws SecurityError on any
      // attempt to access window.sessionStorage.
      process.env.NODE_ENV !== 'production' ? _warning2['default'](false, '[history] Unable to save state; sessionStorage is not available due to security settings') : undefined;

      return;
    }

    if (error.name === QuotaExceededError && window.sessionStorage.length === 0) {
      // Safari "private mode" throws QuotaExceededError.
      process.env.NODE_ENV !== 'production' ? _warning2['default'](false, '[history] Unable to save state; sessionStorage is not available in Safari private mode') : undefined;

      return;
    }

    throw error;
  }
}

function readState(key) {
  var json = undefined;
  try {
    json = window.sessionStorage.getItem(createKey(key));
  } catch (error) {
    if (error.name === SecurityError) {
      // Blocking cookies in Chrome/Firefox/Safari throws SecurityError on any
      // attempt to access window.sessionStorage.
      process.env.NODE_ENV !== 'production' ? _warning2['default'](false, '[history] Unable to read state; sessionStorage is not available due to security settings') : undefined;

      return null;
    }
  }

  if (json) {
    try {
      return JSON.parse(json);
    } catch (error) {
      // Ignore invalid JSON.
    }
  }

  return null;
}
}).call(this,require('_process'))

},{"_process":1,"warning":47}],36:[function(require,module,exports){
'use strict';

exports.__esModule = true;
exports.addEventListener = addEventListener;
exports.removeEventListener = removeEventListener;
exports.getHashPath = getHashPath;
exports.replaceHashPath = replaceHashPath;
exports.getWindowPath = getWindowPath;
exports.go = go;
exports.getUserConfirmation = getUserConfirmation;
exports.supportsHistory = supportsHistory;
exports.supportsGoWithoutReloadUsingHash = supportsGoWithoutReloadUsingHash;

function addEventListener(node, event, listener) {
  if (node.addEventListener) {
    node.addEventListener(event, listener, false);
  } else {
    node.attachEvent('on' + event, listener);
  }
}

function removeEventListener(node, event, listener) {
  if (node.removeEventListener) {
    node.removeEventListener(event, listener, false);
  } else {
    node.detachEvent('on' + event, listener);
  }
}

function getHashPath() {
  // We can't use window.location.hash here because it's not
  // consistent across browsers - Firefox will pre-decode it!
  return window.location.href.split('#')[1] || '';
}

function replaceHashPath(path) {
  window.location.replace(window.location.pathname + window.location.search + '#' + path);
}

function getWindowPath() {
  return window.location.pathname + window.location.search + window.location.hash;
}

function go(n) {
  if (n) window.history.go(n);
}

function getUserConfirmation(message, callback) {
  callback(window.confirm(message));
}

/**
 * Returns true if the HTML5 history API is supported. Taken from Modernizr.
 *
 * https://github.com/Modernizr/Modernizr/blob/master/LICENSE
 * https://github.com/Modernizr/Modernizr/blob/master/feature-detects/history.js
 * changed to avoid false negatives for Windows Phones: https://github.com/rackt/react-router/issues/586
 */

function supportsHistory() {
  var ua = navigator.userAgent;
  if ((ua.indexOf('Android 2.') !== -1 || ua.indexOf('Android 4.0') !== -1) && ua.indexOf('Mobile Safari') !== -1 && ua.indexOf('Chrome') === -1 && ua.indexOf('Windows Phone') === -1) {
    return false;
  }
  // FIXME: Work around our browser history not working correctly on Chrome
  // iOS: https://github.com/rackt/react-router/issues/2565
  if (ua.indexOf('CriOS') !== -1) {
    return false;
  }
  return window.history && 'pushState' in window.history;
}

/**
 * Returns false if using go(n) with hash history causes a full page reload.
 */

function supportsGoWithoutReloadUsingHash() {
  var ua = navigator.userAgent;
  return ua.indexOf('Firefox') === -1;
}
},{}],37:[function(require,module,exports){
'use strict';

exports.__esModule = true;
var canUseDOM = !!(typeof window !== 'undefined' && window.document && window.document.createElement);
exports.canUseDOM = canUseDOM;
},{}],38:[function(require,module,exports){
(function (process){
'use strict';

exports.__esModule = true;

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _invariant = require('invariant');

var _invariant2 = _interopRequireDefault(_invariant);

var _Actions = require('./Actions');

var _ExecutionEnvironment = require('./ExecutionEnvironment');

var _DOMUtils = require('./DOMUtils');

var _DOMStateStorage = require('./DOMStateStorage');

var _createDOMHistory = require('./createDOMHistory');

var _createDOMHistory2 = _interopRequireDefault(_createDOMHistory);

var _parsePath = require('./parsePath');

var _parsePath2 = _interopRequireDefault(_parsePath);

/**
 * Creates and returns a history object that uses HTML5's history API
 * (pushState, replaceState, and the popstate event) to manage history.
 * This is the recommended method of managing history in browsers because
 * it provides the cleanest URLs.
 *
 * Note: In browsers that do not support the HTML5 history API full
 * page reloads will be used to preserve URLs.
 */
function createBrowserHistory() {
  var options = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

  !_ExecutionEnvironment.canUseDOM ? process.env.NODE_ENV !== 'production' ? _invariant2['default'](false, 'Browser history needs a DOM') : _invariant2['default'](false) : undefined;

  var forceRefresh = options.forceRefresh;

  var isSupported = _DOMUtils.supportsHistory();
  var useRefresh = !isSupported || forceRefresh;

  function getCurrentLocation(historyState) {
    historyState = historyState || window.history.state || {};

    var path = _DOMUtils.getWindowPath();
    var _historyState = historyState;
    var key = _historyState.key;

    var state = undefined;
    if (key) {
      state = _DOMStateStorage.readState(key);
    } else {
      state = null;
      key = history.createKey();

      if (isSupported) window.history.replaceState(_extends({}, historyState, { key: key }), null, path);
    }

    var location = _parsePath2['default'](path);

    return history.createLocation(_extends({}, location, { state: state }), undefined, key);
  }

  function startPopStateListener(_ref) {
    var transitionTo = _ref.transitionTo;

    function popStateListener(event) {
      if (event.state === undefined) return; // Ignore extraneous popstate events in WebKit.

      transitionTo(getCurrentLocation(event.state));
    }

    _DOMUtils.addEventListener(window, 'popstate', popStateListener);

    return function () {
      _DOMUtils.removeEventListener(window, 'popstate', popStateListener);
    };
  }

  function finishTransition(location) {
    var basename = location.basename;
    var pathname = location.pathname;
    var search = location.search;
    var hash = location.hash;
    var state = location.state;
    var action = location.action;
    var key = location.key;

    if (action === _Actions.POP) return; // Nothing to do.

    _DOMStateStorage.saveState(key, state);

    var path = (basename || '') + pathname + search + hash;
    var historyState = {
      key: key
    };

    if (action === _Actions.PUSH) {
      if (useRefresh) {
        window.location.href = path;
        return false; // Prevent location update.
      } else {
          window.history.pushState(historyState, null, path);
        }
    } else {
      // REPLACE
      if (useRefresh) {
        window.location.replace(path);
        return false; // Prevent location update.
      } else {
          window.history.replaceState(historyState, null, path);
        }
    }
  }

  var history = _createDOMHistory2['default'](_extends({}, options, {
    getCurrentLocation: getCurrentLocation,
    finishTransition: finishTransition,
    saveState: _DOMStateStorage.saveState
  }));

  var listenerCount = 0,
      stopPopStateListener = undefined;

  function listenBefore(listener) {
    if (++listenerCount === 1) stopPopStateListener = startPopStateListener(history);

    var unlisten = history.listenBefore(listener);

    return function () {
      unlisten();

      if (--listenerCount === 0) stopPopStateListener();
    };
  }

  function listen(listener) {
    if (++listenerCount === 1) stopPopStateListener = startPopStateListener(history);

    var unlisten = history.listen(listener);

    return function () {
      unlisten();

      if (--listenerCount === 0) stopPopStateListener();
    };
  }

  // deprecated
  function registerTransitionHook(hook) {
    if (++listenerCount === 1) stopPopStateListener = startPopStateListener(history);

    history.registerTransitionHook(hook);
  }

  // deprecated
  function unregisterTransitionHook(hook) {
    history.unregisterTransitionHook(hook);

    if (--listenerCount === 0) stopPopStateListener();
  }

  return _extends({}, history, {
    listenBefore: listenBefore,
    listen: listen,
    registerTransitionHook: registerTransitionHook,
    unregisterTransitionHook: unregisterTransitionHook
  });
}

exports['default'] = createBrowserHistory;
module.exports = exports['default'];
}).call(this,require('_process'))

},{"./Actions":33,"./DOMStateStorage":35,"./DOMUtils":36,"./ExecutionEnvironment":37,"./createDOMHistory":39,"./parsePath":44,"_process":1,"invariant":46}],39:[function(require,module,exports){
(function (process){
'use strict';

exports.__esModule = true;

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _invariant = require('invariant');

var _invariant2 = _interopRequireDefault(_invariant);

var _ExecutionEnvironment = require('./ExecutionEnvironment');

var _DOMUtils = require('./DOMUtils');

var _createHistory = require('./createHistory');

var _createHistory2 = _interopRequireDefault(_createHistory);

function createDOMHistory(options) {
  var history = _createHistory2['default'](_extends({
    getUserConfirmation: _DOMUtils.getUserConfirmation
  }, options, {
    go: _DOMUtils.go
  }));

  function listen(listener) {
    !_ExecutionEnvironment.canUseDOM ? process.env.NODE_ENV !== 'production' ? _invariant2['default'](false, 'DOM history needs a DOM') : _invariant2['default'](false) : undefined;

    return history.listen(listener);
  }

  return _extends({}, history, {
    listen: listen
  });
}

exports['default'] = createDOMHistory;
module.exports = exports['default'];
}).call(this,require('_process'))

},{"./DOMUtils":36,"./ExecutionEnvironment":37,"./createHistory":40,"_process":1,"invariant":46}],40:[function(require,module,exports){
//import warning from 'warning'
'use strict';

exports.__esModule = true;

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _deepEqual = require('deep-equal');

var _deepEqual2 = _interopRequireDefault(_deepEqual);

var _AsyncUtils = require('./AsyncUtils');

var _Actions = require('./Actions');

var _createLocation2 = require('./createLocation');

var _createLocation3 = _interopRequireDefault(_createLocation2);

var _runTransitionHook = require('./runTransitionHook');

var _runTransitionHook2 = _interopRequireDefault(_runTransitionHook);

var _parsePath = require('./parsePath');

var _parsePath2 = _interopRequireDefault(_parsePath);

var _deprecate = require('./deprecate');

var _deprecate2 = _interopRequireDefault(_deprecate);

function createRandomKey(length) {
  return Math.random().toString(36).substr(2, length);
}

function locationsAreEqual(a, b) {
  return a.pathname === b.pathname && a.search === b.search &&
  //a.action === b.action && // Different action !== location change.
  a.key === b.key && _deepEqual2['default'](a.state, b.state);
}

var DefaultKeyLength = 6;

function createHistory() {
  var options = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];
  var getCurrentLocation = options.getCurrentLocation;
  var finishTransition = options.finishTransition;
  var saveState = options.saveState;
  var go = options.go;
  var keyLength = options.keyLength;
  var getUserConfirmation = options.getUserConfirmation;

  if (typeof keyLength !== 'number') keyLength = DefaultKeyLength;

  var transitionHooks = [];

  function listenBefore(hook) {
    transitionHooks.push(hook);

    return function () {
      transitionHooks = transitionHooks.filter(function (item) {
        return item !== hook;
      });
    };
  }

  var allKeys = [];
  var changeListeners = [];
  var location = undefined;

  function getCurrent() {
    if (pendingLocation && pendingLocation.action === _Actions.POP) {
      return allKeys.indexOf(pendingLocation.key);
    } else if (location) {
      return allKeys.indexOf(location.key);
    } else {
      return -1;
    }
  }

  function updateLocation(newLocation) {
    var current = getCurrent();

    location = newLocation;

    if (location.action === _Actions.PUSH) {
      allKeys = [].concat(allKeys.slice(0, current + 1), [location.key]);
    } else if (location.action === _Actions.REPLACE) {
      allKeys[current] = location.key;
    }

    changeListeners.forEach(function (listener) {
      listener(location);
    });
  }

  function listen(listener) {
    changeListeners.push(listener);

    if (location) {
      listener(location);
    } else {
      var _location = getCurrentLocation();
      allKeys = [_location.key];
      updateLocation(_location);
    }

    return function () {
      changeListeners = changeListeners.filter(function (item) {
        return item !== listener;
      });
    };
  }

  function confirmTransitionTo(location, callback) {
    _AsyncUtils.loopAsync(transitionHooks.length, function (index, next, done) {
      _runTransitionHook2['default'](transitionHooks[index], location, function (result) {
        if (result != null) {
          done(result);
        } else {
          next();
        }
      });
    }, function (message) {
      if (getUserConfirmation && typeof message === 'string') {
        getUserConfirmation(message, function (ok) {
          callback(ok !== false);
        });
      } else {
        callback(message !== false);
      }
    });
  }

  var pendingLocation = undefined;

  function transitionTo(nextLocation) {
    if (location && locationsAreEqual(location, nextLocation)) return; // Nothing to do.

    pendingLocation = nextLocation;

    confirmTransitionTo(nextLocation, function (ok) {
      if (pendingLocation !== nextLocation) return; // Transition was interrupted.

      if (ok) {
        // treat PUSH to current path like REPLACE to be consistent with browsers
        if (nextLocation.action === _Actions.PUSH) {
          var prevPath = createPath(location);
          var nextPath = createPath(nextLocation);

          if (nextPath === prevPath) nextLocation.action = _Actions.REPLACE;
        }

        if (finishTransition(nextLocation) !== false) updateLocation(nextLocation);
      } else if (location && nextLocation.action === _Actions.POP) {
        var prevIndex = allKeys.indexOf(location.key);
        var nextIndex = allKeys.indexOf(nextLocation.key);

        if (prevIndex !== -1 && nextIndex !== -1) go(prevIndex - nextIndex); // Restore the URL.
      }
    });
  }

  function push(location) {
    transitionTo(createLocation(location, _Actions.PUSH, createKey()));
  }

  function replace(location) {
    transitionTo(createLocation(location, _Actions.REPLACE, createKey()));
  }

  function goBack() {
    go(-1);
  }

  function goForward() {
    go(1);
  }

  function createKey() {
    return createRandomKey(keyLength);
  }

  function createPath(location) {
    if (location == null || typeof location === 'string') return location;

    var pathname = location.pathname;
    var search = location.search;
    var hash = location.hash;

    var result = pathname;

    if (search) result += search;

    if (hash) result += hash;

    return result;
  }

  function createHref(location) {
    return createPath(location);
  }

  function createLocation(location, action) {
    var key = arguments.length <= 2 || arguments[2] === undefined ? createKey() : arguments[2];

    if (typeof action === 'object') {
      //warning(
      //  false,
      //  'The state (2nd) argument to history.createLocation is deprecated; use a ' +
      //  'location descriptor instead'
      //)

      if (typeof location === 'string') location = _parsePath2['default'](location);

      location = _extends({}, location, { state: action });

      action = key;
      key = arguments[3] || createKey();
    }

    return _createLocation3['default'](location, action, key);
  }

  // deprecated
  function setState(state) {
    if (location) {
      updateLocationState(location, state);
      updateLocation(location);
    } else {
      updateLocationState(getCurrentLocation(), state);
    }
  }

  function updateLocationState(location, state) {
    location.state = _extends({}, location.state, state);
    saveState(location.key, location.state);
  }

  // deprecated
  function registerTransitionHook(hook) {
    if (transitionHooks.indexOf(hook) === -1) transitionHooks.push(hook);
  }

  // deprecated
  function unregisterTransitionHook(hook) {
    transitionHooks = transitionHooks.filter(function (item) {
      return item !== hook;
    });
  }

  // deprecated
  function pushState(state, path) {
    if (typeof path === 'string') path = _parsePath2['default'](path);

    push(_extends({ state: state }, path));
  }

  // deprecated
  function replaceState(state, path) {
    if (typeof path === 'string') path = _parsePath2['default'](path);

    replace(_extends({ state: state }, path));
  }

  return {
    listenBefore: listenBefore,
    listen: listen,
    transitionTo: transitionTo,
    push: push,
    replace: replace,
    go: go,
    goBack: goBack,
    goForward: goForward,
    createKey: createKey,
    createPath: createPath,
    createHref: createHref,
    createLocation: createLocation,

    setState: _deprecate2['default'](setState, 'setState is deprecated; use location.key to save state instead'),
    registerTransitionHook: _deprecate2['default'](registerTransitionHook, 'registerTransitionHook is deprecated; use listenBefore instead'),
    unregisterTransitionHook: _deprecate2['default'](unregisterTransitionHook, 'unregisterTransitionHook is deprecated; use the callback returned from listenBefore instead'),
    pushState: _deprecate2['default'](pushState, 'pushState is deprecated; use push instead'),
    replaceState: _deprecate2['default'](replaceState, 'replaceState is deprecated; use replace instead')
  };
}

exports['default'] = createHistory;
module.exports = exports['default'];
},{"./Actions":33,"./AsyncUtils":34,"./createLocation":41,"./deprecate":42,"./parsePath":44,"./runTransitionHook":45,"deep-equal":30}],41:[function(require,module,exports){
//import warning from 'warning'
'use strict';

exports.__esModule = true;

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _Actions = require('./Actions');

var _parsePath = require('./parsePath');

var _parsePath2 = _interopRequireDefault(_parsePath);

function createLocation() {
  var location = arguments.length <= 0 || arguments[0] === undefined ? '/' : arguments[0];
  var action = arguments.length <= 1 || arguments[1] === undefined ? _Actions.POP : arguments[1];
  var key = arguments.length <= 2 || arguments[2] === undefined ? null : arguments[2];

  var _fourthArg = arguments.length <= 3 || arguments[3] === undefined ? null : arguments[3];

  if (typeof location === 'string') location = _parsePath2['default'](location);

  if (typeof action === 'object') {
    //warning(
    //  false,
    //  'The state (2nd) argument to createLocation is deprecated; use a ' +
    //  'location descriptor instead'
    //)

    location = _extends({}, location, { state: action });

    action = key || _Actions.POP;
    key = _fourthArg;
  }

  var pathname = location.pathname || '/';
  var search = location.search || '';
  var hash = location.hash || '';
  var state = location.state || null;

  return {
    pathname: pathname,
    search: search,
    hash: hash,
    state: state,
    action: action,
    key: key
  };
}

exports['default'] = createLocation;
module.exports = exports['default'];
},{"./Actions":33,"./parsePath":44}],42:[function(require,module,exports){
//import warning from 'warning'

"use strict";

exports.__esModule = true;
function deprecate(fn) {
  return fn;
  //return function () {
  //  warning(false, '[history] ' + message)
  //  return fn.apply(this, arguments)
  //}
}

exports["default"] = deprecate;
module.exports = exports["default"];
},{}],43:[function(require,module,exports){
"use strict";

exports.__esModule = true;
function extractPath(string) {
  var match = string.match(/^https?:\/\/[^\/]*/);

  if (match == null) return string;

  return string.substring(match[0].length);
}

exports["default"] = extractPath;
module.exports = exports["default"];
},{}],44:[function(require,module,exports){
(function (process){
'use strict';

exports.__esModule = true;

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _warning = require('warning');

var _warning2 = _interopRequireDefault(_warning);

var _extractPath = require('./extractPath');

var _extractPath2 = _interopRequireDefault(_extractPath);

function parsePath(path) {
  var pathname = _extractPath2['default'](path);
  var search = '';
  var hash = '';

  process.env.NODE_ENV !== 'production' ? _warning2['default'](path === pathname, 'A path must be pathname + search + hash only, not a fully qualified URL like "%s"', path) : undefined;

  var hashIndex = pathname.indexOf('#');
  if (hashIndex !== -1) {
    hash = pathname.substring(hashIndex);
    pathname = pathname.substring(0, hashIndex);
  }

  var searchIndex = pathname.indexOf('?');
  if (searchIndex !== -1) {
    search = pathname.substring(searchIndex);
    pathname = pathname.substring(0, searchIndex);
  }

  if (pathname === '') pathname = '/';

  return {
    pathname: pathname,
    search: search,
    hash: hash
  };
}

exports['default'] = parsePath;
module.exports = exports['default'];
}).call(this,require('_process'))

},{"./extractPath":43,"_process":1,"warning":47}],45:[function(require,module,exports){
(function (process){
'use strict';

exports.__esModule = true;

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _warning = require('warning');

var _warning2 = _interopRequireDefault(_warning);

function runTransitionHook(hook, location, callback) {
  var result = hook(location, callback);

  if (hook.length < 2) {
    // Assume the hook runs synchronously and automatically
    // call the callback with the return value.
    callback(result);
  } else {
    process.env.NODE_ENV !== 'production' ? _warning2['default'](result === undefined, 'You should not "return" in a transition hook with a callback argument; call the callback instead') : undefined;
  }
}

exports['default'] = runTransitionHook;
module.exports = exports['default'];
}).call(this,require('_process'))

},{"_process":1,"warning":47}],46:[function(require,module,exports){
(function (process){
/**
 * Copyright 2013-2015, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

'use strict';

/**
 * Use invariant() to assert state which your program assumes to be true.
 *
 * Provide sprintf-style format (only %s is supported) and arguments
 * to provide information about what broke and what you were
 * expecting.
 *
 * The invariant message will be stripped in production, but the invariant
 * will remain to ensure logic does not differ in production.
 */

var invariant = function(condition, format, a, b, c, d, e, f) {
  if (process.env.NODE_ENV !== 'production') {
    if (format === undefined) {
      throw new Error('invariant requires an error message argument');
    }
  }

  if (!condition) {
    var error;
    if (format === undefined) {
      error = new Error(
        'Minified exception occurred; use the non-minified dev environment ' +
        'for the full error message and additional helpful warnings.'
      );
    } else {
      var args = [a, b, c, d, e, f];
      var argIndex = 0;
      error = new Error(
        format.replace(/%s/g, function() { return args[argIndex++]; })
      );
      error.name = 'Invariant Violation';
    }

    error.framesToPop = 1; // we don't care about invariant's own frame
    throw error;
  }
};

module.exports = invariant;

}).call(this,require('_process'))

},{"_process":1}],47:[function(require,module,exports){
(function (process){
/**
 * Copyright 2014-2015, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

'use strict';

/**
 * Similar to invariant but only logs a warning if the condition is not met.
 * This can be used to log issues in development environments in critical
 * paths. Removing the logging code for production environments will keep the
 * same logic and follow the same code paths.
 */

var warning = function() {};

if (process.env.NODE_ENV !== 'production') {
  warning = function(condition, format, args) {
    var len = arguments.length;
    args = new Array(len > 2 ? len - 2 : 0);
    for (var key = 2; key < len; key++) {
      args[key - 2] = arguments[key];
    }
    if (format === undefined) {
      throw new Error(
        '`warning(condition, format, ...args)` requires a warning ' +
        'message argument'
      );
    }

    if (format.length < 10 || (/^[s\W]*$/).test(format)) {
      throw new Error(
        'The warning format should be able to uniquely identify this ' +
        'warning. Please, use a more descriptive format than: ' + format
      );
    }

    if (!condition) {
      var argIndex = 0;
      var message = 'Warning: ' +
        format.replace(/%s/g, function() {
          return args[argIndex++];
        });
      if (typeof console !== 'undefined') {
        console.error(message);
      }
      try {
        // This error was thrown as a convenience so that you can use this stack
        // to find the callsite that caused this warning to fire.
        throw new Error(message);
      } catch(x) {}
    }
  };
}

module.exports = warning;

}).call(this,require('_process'))

},{"_process":1}],48:[function(require,module,exports){
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.select = select;

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: "refresh",
    value: function refresh() {
      window.location.reload();
    }
  }, {
    key: "getMessage",
    value: function getMessage() {
      if (this.props.signedIn) {
        return interpolate(gettext("You have signed in as %(username)s. Please refresh the page before continuing."), { username: this.props.signedIn.username }, true);
      } else if (this.props.signedOut) {
        return interpolate(gettext("%(username)s, you have been signed out. Please refresh the page before continuing."), { username: this.props.user.username }, true);
      }
    }
  }, {
    key: "getClassName",
    value: function getClassName() {
      if (this.props.signedIn || this.props.signedOut) {
        return "auth-message show";
      } else {
        return "auth-message";
      }
    }
  }, {
    key: "render",
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        "div",
        { className: this.getClassName() },
        _react2.default.createElement(
          "div",
          { className: "container" },
          _react2.default.createElement(
            "p",
            { className: "lead" },
            this.getMessage()
          ),
          _react2.default.createElement(
            "p",
            null,
            _react2.default.createElement(
              "button",
              { type: "button", className: "btn btn-default",
                onClick: this.refresh },
              gettext("Reload page")
            ),
            " ",
            _react2.default.createElement(
              "span",
              { className: "hidden-xs hidden-sm text-muted" },
              gettext("or press F5 key.")
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;
function select(state) {
  return {
    user: state.auth.user,
    signedIn: state.auth.signedIn,
    signedOut: state.auth.signedOut
  };
}

},{"react":"react"}],49:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var BASE_URL = $('base').attr('href') + 'user-avatar/';

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'getSrc',
    value: function getSrc() {
      var size = this.props.size || 100; // jshint ignore:line
      var url = BASE_URL;

      if (this.props.user && this.props.user.id) {
        // just avatar hash, size and user id
        url += this.props.user.avatar_hash + '/' + size + '/' + this.props.user.id + '.png';
      } else {
        // just append avatar size to file to produce no-avatar placeholder
        url += size + '.png';
      }

      return url;
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement('img', { src: this.getSrc(),
        className: this.props.className || 'user-avatar',
        title: gettext("User avatar") });
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],50:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'getReasonMessage',
    value: function getReasonMessage() {
      /* jshint ignore:start */
      if (this.props.message.html) {
        return _react2.default.createElement('div', { className: 'lead',
          dangerouslySetInnerHTML: { __html: this.props.message.html } });
      } else {
        return _react2.default.createElement(
          'p',
          { className: 'lead' },
          this.props.message.plain
        );
      }
      /* jshint ignore:end */
    }
  }, {
    key: 'getExpirationMessage',
    value: function getExpirationMessage() {
      if (this.props.expires) {
        if (this.props.expires.isAfter((0, _moment2.default)())) {
          return interpolate(gettext("This ban expires %(expires_on)s."), { 'expires_on': this.props.expires.fromNow() }, true);
        } else {
          return gettext("This ban has expired.");
        }
      } else {
        return gettext("This ban is permanent.");
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'page page-error page-error-banned' },
        _react2.default.createElement(
          'div',
          { className: 'container' },
          _react2.default.createElement(
            'div',
            { className: 'message-panel' },
            _react2.default.createElement(
              'div',
              { className: 'message-icon' },
              _react2.default.createElement(
                'span',
                { className: 'material-icon' },
                'highlight_off'
              )
            ),
            _react2.default.createElement(
              'div',
              { className: 'message-body' },
              this.getReasonMessage(),
              _react2.default.createElement(
                'p',
                { className: 'message-footnote' },
                this.getExpirationMessage()
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"moment":"moment","react":"react"}],51:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _loader = require('./loader');

var _loader2 = _interopRequireDefault(_loader);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// jshint ignore:line

var Button = function (_React$Component) {
  _inherits(Button, _React$Component);

  function Button() {
    _classCallCheck(this, Button);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(Button).apply(this, arguments));
  }

  _createClass(Button, [{
    key: 'render',
    value: function render() {
      var className = 'btn ' + this.props.className;
      var disabled = this.props.disabled;

      if (this.props.loading) {
        className += ' btn-loading';
        disabled = true;
      }

      /* jshint ignore:start */
      return _react2.default.createElement(
        'button',
        { type: this.props.onClick ? 'button' : 'submit',
          className: className,
          disabled: disabled,
          onClick: this.props.onClick },
        this.props.children,
        this.props.loading ? _react2.default.createElement(_loader2.default, null) : null
      );
      /* jshint ignore:end */
    }
  }]);

  return Button;
}(_react2.default.Component);

exports.default = Button;

Button.defaultProps = {
  className: "btn-default",

  type: "submit",

  loading: false,
  disabled: false,

  onClick: null
};

},{"./loader":60,"react":"react"}],52:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _avatar = require('../avatar');

var _avatar2 = _interopRequireDefault(_avatar);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _snackbar = require('../../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line

// jshint ignore:line

var BASE_URL = $('base').attr('href') + 'user-avatar';

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.cropAvatar = function () {
      if (_this.state.isLoading) {
        return false;
      }

      _this.setState({
        'isLoading': true
      });

      var avatarType = _this.props.upload ? 'crop_tmp' : 'crop_org';
      var cropit = $('.crop-form');

      _ajax2.default.post(_this.props.user.api_url.avatar, {
        'avatar': avatarType,
        'crop': {
          'offset': cropit.cropit('offset'),
          'zoom': cropit.cropit('zoom')
        }
      }).then(function (data) {
        _this.props.onComplete(data.avatar_hash, data.options);
        _snackbar2.default.success(data.detail);
      }, function (rejection) {
        if (rejection.status === 400) {
          _snackbar2.default.error(rejection.detail);
          _this.setState({
            'isLoading': false
          });
        } else {
          _this.props.showError(rejection);
        }
      });
    };

    _this.state = {
      'isLoading': false
    };
    return _this;
  }

  _createClass(_class, [{
    key: 'getAvatarSize',
    value: function getAvatarSize() {
      if (this.props.upload) {
        return this.props.options.crop_tmp.size;
      } else {
        return this.props.options.crop_org.size;
      }
    }
  }, {
    key: 'getAvatarSecret',
    value: function getAvatarSecret() {
      if (this.props.upload) {
        return this.props.options.crop_tmp.secret;
      } else {
        return this.props.options.crop_org.secret;
      }
    }
  }, {
    key: 'getAvatarHash',
    value: function getAvatarHash() {
      return this.props.upload || this.props.user.avatar_hash;
    }
  }, {
    key: 'getImagePath',
    value: function getImagePath() {
      return [BASE_URL, this.getAvatarSecret() + ':' + this.getAvatarHash(), this.props.user.id + '.png'].join('/');
    }
  }, {
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this2 = this;

      var cropit = $('.crop-form');
      cropit.width(this.getAvatarSize());

      cropit.cropit({
        'width': this.getAvatarSize(),
        'height': this.getAvatarSize(),
        'imageState': {
          'src': this.getImagePath()
        },
        onImageLoaded: function onImageLoaded() {
          if (_this2.props.upload) {
            // center uploaded image
            var zoomLevel = cropit.cropit('zoom');
            var imageSize = cropit.cropit('imageSize');

            // is it wider than taller?
            if (imageSize.width > imageSize.height) {
              var displayedWidth = imageSize.width * zoomLevel;
              var offsetX = (displayedWidth - _this2.getAvatarSize()) / -2;

              cropit.cropit('offset', {
                'x': offsetX,
                'y': 0
              });
            } else if (imageSize.width < imageSize.height) {
              var displayedHeight = imageSize.height * zoomLevel;
              var offsetY = (displayedHeight - _this2.getAvatarSize()) / -2;

              cropit.cropit('offset', {
                'x': 0,
                'y': offsetY
              });
            }
          } else {
            // use preserved crop
            var crop = _this2.props.options.crop_org.crop;
            if (crop) {
              cropit.cropit('zoom', crop.zoom);
              cropit.cropit('offset', {
                'x': crop.x,
                'y': crop.y
              });
            }
          }
        }
      });
    }
  }, {
    key: 'componentWillUnmount',
    value: function componentWillUnmount() {
      $('.crop-form').cropit('disable');
    }

    /* jshint ignore:start */

  }, {
    key: 'render',

    /* jshint ignore:end */

    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        null,
        _react2.default.createElement(
          'div',
          { className: 'modal-body modal-avatar-crop' },
          _react2.default.createElement(
            'div',
            { className: 'crop-form' },
            _react2.default.createElement('div', { className: 'cropit-image-preview' }),
            _react2.default.createElement('input', { type: 'range', className: 'cropit-image-zoom-input' })
          )
        ),
        _react2.default.createElement(
          'div',
          { className: 'modal-footer' },
          _react2.default.createElement(
            'div',
            { className: 'col-md-6 col-md-offset-3' },
            _react2.default.createElement(
              _button2.default,
              { onClick: this.cropAvatar,
                loading: this.state.isLoading,
                className: 'btn-primary btn-block' },
              this.props.upload ? gettext("Set avatar") : gettext("Crop image")
            ),
            _react2.default.createElement(
              _button2.default,
              { onClick: this.props.showIndex,
                disabled: this.state.isLoading,
                className: 'btn-default btn-block' },
              gettext("Cancel")
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../services/ajax":91,"../../services/snackbar":99,"../avatar":49,"../button":51,"react":"react"}],53:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Gallery = exports.GalleryItem = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _snackbar = require('../../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _batch = require('../../utils/batch');

var _batch2 = _interopRequireDefault(_batch);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

// jshint ignore:line

var GalleryItem = exports.GalleryItem = function (_React$Component) {
  _inherits(GalleryItem, _React$Component);

  function GalleryItem() {
    var _Object$getPrototypeO;

    var _temp, _this, _ret;

    _classCallCheck(this, GalleryItem);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_Object$getPrototypeO = Object.getPrototypeOf(GalleryItem)).call.apply(_Object$getPrototypeO, [this].concat(args))), _this), _this.select = function () {
      _this.props.select(_this.props.image);
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }
  /* jshint ignore:start */

  _createClass(GalleryItem, [{
    key: 'getClassName',

    /* jshint ignore:end */

    value: function getClassName() {
      if (this.props.selection === this.props.image) {
        if (this.props.disabled) {
          return 'btn btn-avatar btn-disabled avatar-selected';
        } else {
          return 'btn btn-avatar avatar-selected';
        }
      } else if (this.props.disabled) {
        return 'btn btn-avatar btn-disabled';
      } else {
        return 'btn btn-avatar';
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'button',
        { type: 'button',
          className: this.getClassName(),
          disabled: this.props.disabled,
          onClick: this.select },
        _react2.default.createElement('img', { src: _index2.default.get('MEDIA_URL') + this.props.image })
      );
      /* jshint ignore:end */
    }
  }]);

  return GalleryItem;
}(_react2.default.Component);

var Gallery = exports.Gallery = function (_React$Component2) {
  _inherits(Gallery, _React$Component2);

  function Gallery() {
    _classCallCheck(this, Gallery);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(Gallery).apply(this, arguments));
  }

  _createClass(Gallery, [{
    key: 'render',
    value: function render() {
      var _this3 = this;

      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'avatars-gallery' },
        _react2.default.createElement(
          'h3',
          null,
          this.props.name
        ),
        _react2.default.createElement(
          'div',
          { className: 'avatars-gallery-images' },
          (0, _batch2.default)(this.props.images, 4, null).map(function (row, i) {
            return _react2.default.createElement(
              'div',
              { className: 'row', key: i },
              row.map(function (item, i) {
                return _react2.default.createElement(
                  'div',
                  { className: 'col-xs-3', key: i },
                  item ? _react2.default.createElement(GalleryItem, { image: item,
                    disabled: _this3.props.disabled,
                    select: _this3.props.select,
                    selection: _this3.props.selection }) : _react2.default.createElement('div', { className: 'blank-avatar' })
                );
              })
            );
          })
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return Gallery;
}(_react2.default.Component);

var _class = function (_React$Component3) {
  _inherits(_class, _React$Component3);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this4 = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this4.select = function (image) {
      _this4.setState({
        selection: image
      });
    };

    _this4.save = function () {
      if (_this4.state.isLoading) {
        return false;
      }

      _this4.setState({
        'isLoading': true
      });

      _ajax2.default.post(_this4.props.user.api_url.avatar, {
        avatar: 'galleries',
        image: _this4.state.selection
      }).then(function (response) {
        _this4.setState({
          'isLoading': false
        });

        _snackbar2.default.success(response.detail);
        _this4.props.onComplete(response.avatar_hash, response.options);
      }, function (rejection) {
        if (rejection.status === 400) {
          _snackbar2.default.error(rejection.detail);
          _this4.setState({
            'isLoading': false
          });
        } else {
          _this4.props.showError(rejection);
        }
      });
    };

    _this4.state = {
      'selection': null,
      'isLoading': false
    };
    return _this4;
  }

  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'render',

    /* jshint ignore:end */

    value: function render() {
      var _this5 = this;

      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        null,
        _react2.default.createElement(
          'div',
          { className: 'modal-body modal-avatar-gallery' },
          this.props.options.galleries.map(function (item, i) {
            return _react2.default.createElement(Gallery, { name: item.name,
              images: item.images,
              selection: _this5.state.selection,
              disabled: _this5.state.isLoading,
              select: _this5.select,
              key: i });
          })
        ),
        _react2.default.createElement(
          'div',
          { className: 'modal-footer' },
          _react2.default.createElement(
            'div',
            { className: 'row' },
            _react2.default.createElement(
              'div',
              { className: 'col-md-6 col-md-offset-3' },
              _react2.default.createElement(
                _button2.default,
                { onClick: this.save,
                  loading: this.state.isLoading,
                  disabled: !this.state.selection,
                  className: 'btn-primary btn-block' },
                this.state.selection ? gettext("Save choice") : gettext("Select avatar")
              ),
              _react2.default.createElement(
                _button2.default,
                { onClick: this.props.showIndex,
                  disabled: this.state.isLoading,
                  className: 'btn-default btn-block' },
                gettext("Cancel")
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../index":85,"../../services/ajax":91,"../../services/snackbar":99,"../../utils/batch":103,"../button":51,"react":"react"}],54:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _avatar = require('../avatar');

var _avatar2 = _interopRequireDefault(_avatar);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _loader = require('../loader');

var _loader2 = _interopRequireDefault(_loader);

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _snackbar = require('../../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.setGravatar = function () {
      _this.callApi('gravatar');
    };

    _this.setGenerated = function () {
      _this.callApi('generated');
    };

    _this.state = {
      'isLoading': false
    };
    return _this;
  }

  _createClass(_class, [{
    key: 'callApi',
    value: function callApi(avatarType) {
      var _this2 = this;

      if (this.state.isLoading) {
        return false;
      }

      this.setState({
        'isLoading': true
      });

      _ajax2.default.post(this.props.user.api_url.avatar, {
        avatar: avatarType
      }).then(function (response) {
        _this2.setState({
          'isLoading': false
        });

        _snackbar2.default.success(response.detail);
        _this2.props.onComplete(response.avatar_hash, response.options);
      }, function (rejection) {
        if (rejection.status === 400) {
          _snackbar2.default.error(rejection.detail);
          _this2.setState({
            'isLoading': false
          });
        } else {
          _this2.props.showError(rejection);
        }
      });
    }

    /* jshint ignore:start */

  }, {
    key: 'getGravatarButton',

    /* jshint ignore:end */

    value: function getGravatarButton() {
      if (this.props.options.gravatar) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          _button2.default,
          { onClick: this.setGravatar,
            disabled: this.state.isLoading,
            className: 'btn-default btn-block btn-avatar-gravatar' },
          gettext("Download my Gravatar")
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'getCropButton',
    value: function getCropButton() {
      if (this.props.options.crop_org) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          _button2.default,
          { onClick: this.props.showCrop,
            disabled: this.state.isLoading,
            className: 'btn-default btn-block btn-avatar-crop' },
          gettext("Re-crop uploaded image")
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'getUploadButton',
    value: function getUploadButton() {
      if (this.props.options.upload) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          _button2.default,
          { onClick: this.props.showUpload,
            disabled: this.state.isLoading,
            className: 'btn-default btn-block btn-avatar-upload' },
          gettext("Upload new image")
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'getGalleryButton',
    value: function getGalleryButton() {
      if (this.props.options.galleries) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          _button2.default,
          { onClick: this.props.showGallery,
            disabled: this.state.isLoading,
            className: 'btn-default btn-block btn-avatar-gallery' },
          gettext("Pick avatar from gallery")
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'getAvatarPreview',
    value: function getAvatarPreview() {
      if (this.state.isLoading) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'div',
          { className: 'avatar-preview preview-loading' },
          _react2.default.createElement(_avatar2.default, { user: this.props.user, size: '200' }),
          _react2.default.createElement(_loader2.default, null)
        );
        /* jshint ignore:end */
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(
            'div',
            { className: 'avatar-preview' },
            _react2.default.createElement(_avatar2.default, { user: this.props.user, size: '200' })
          );
          /* jshint ignore:end */
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-body modal-avatar-index' },
        _react2.default.createElement(
          'div',
          { className: 'row' },
          _react2.default.createElement(
            'div',
            { className: 'col-md-5' },
            this.getAvatarPreview()
          ),
          _react2.default.createElement(
            'div',
            { className: 'col-md-7' },
            this.getGravatarButton(),
            _react2.default.createElement(
              _button2.default,
              { onClick: this.setGenerated,
                disabled: this.state.isLoading,
                className: 'btn-default btn-block btn-avatar-generate' },
              gettext("Generate my individual avatar")
            ),
            this.getCropButton(),
            this.getUploadButton(),
            this.getGalleryButton()
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../services/ajax":91,"../../services/snackbar":99,"../avatar":49,"../button":51,"../loader":60,"react":"react"}],55:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.ChangeAvatarError = undefined;
exports.select = select;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _index = require('./index');

var _index2 = _interopRequireDefault(_index);

var _crop = require('./crop');

var _crop2 = _interopRequireDefault(_crop);

var _upload = require('./upload');

var _upload2 = _interopRequireDefault(_upload);

var _gallery = require('./gallery');

var _gallery2 = _interopRequireDefault(_gallery);

var _modalLoader = require('../modal-loader');

var _modalLoader2 = _interopRequireDefault(_modalLoader);

var _users = require('../../reducers/users');

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _store = require('../../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

// jshint ignore:line

var ChangeAvatarError = exports.ChangeAvatarError = function (_React$Component) {
  _inherits(ChangeAvatarError, _React$Component);

  function ChangeAvatarError() {
    _classCallCheck(this, ChangeAvatarError);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(ChangeAvatarError).apply(this, arguments));
  }

  _createClass(ChangeAvatarError, [{
    key: 'getErrorReason',
    value: function getErrorReason() {
      if (this.props.reason) {
        /* jshint ignore:start */
        return _react2.default.createElement('p', { dangerouslySetInnerHTML: { __html: this.props.reason } });
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-body' },
        _react2.default.createElement(
          'div',
          { className: 'message-icon' },
          _react2.default.createElement(
            'span',
            { className: 'material-icon' },
            'remove_circle_outline'
          )
        ),
        _react2.default.createElement(
          'div',
          { className: 'message-body' },
          _react2.default.createElement(
            'p',
            { className: 'lead' },
            this.props.message
          ),
          this.getErrorReason()
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ChangeAvatarError;
}(_react2.default.Component);

var _class = function (_React$Component2) {
  _inherits(_class, _React$Component2);

  function _class() {
    var _Object$getPrototypeO;

    var _temp, _this2, _ret;

    _classCallCheck(this, _class);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this2 = _possibleConstructorReturn(this, (_Object$getPrototypeO = Object.getPrototypeOf(_class)).call.apply(_Object$getPrototypeO, [this].concat(args))), _this2), _this2.showError = function (error) {
      _this2.setState({
        error: error
      });
    }, _this2.showIndex = function () {
      _this2.setState({
        'component': _index2.default
      });
    }, _this2.showUpload = function () {
      _this2.setState({
        'component': _upload2.default
      });
    }, _this2.showCrop = function () {
      _this2.setState({
        'component': _crop2.default
      });
    }, _this2.showGallery = function () {
      _this2.setState({
        'component': _gallery2.default
      });
    }, _this2.completeFlow = function (avatarHash, options) {
      _store2.default.dispatch((0, _users.updateAvatar)(_this2.props.user, avatarHash));

      _this2.setState({
        'component': _index2.default,
        options: options
      });
    }, _temp), _possibleConstructorReturn(_this2, _ret);
  }

  _createClass(_class, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this3 = this;

      _ajax2.default.get(this.props.user.api_url.avatar).then(function (options) {
        _this3.setState({
          'component': _index2.default,
          'options': options,
          'error': null
        });
      }, function (rejection) {
        _this3.showError(rejection);
      });
    }

    /* jshint ignore:start */

  }, {
    key: 'getBody',

    /* jshint ignore:end */

    value: function getBody() {
      if (this.state) {
        if (this.state.error) {
          /* jshint ignore:start */
          return _react2.default.createElement(ChangeAvatarError, { message: this.state.error.detail,
            reason: this.state.error.reason });
          /* jshint ignore:end */
        } else {
            /* jshint ignore:start */
            return _react2.default.createElement(this.state.component, { options: this.state.options,
              user: this.props.user,
              onComplete: this.completeFlow,
              showError: this.showError,
              showIndex: this.showIndex,
              showCrop: this.showCrop,
              showUpload: this.showUpload,
              showGallery: this.showGallery });
            /* jshint ignore:end */
          }
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(_modalLoader2.default, null);
          /* jshint ignore:end */
        }
    }
  }, {
    key: 'getClassName',
    value: function getClassName() {
      if (this.state && this.state.error) {
        return "modal-dialog modal-message modal-change-avatar";
      } else {
        return "modal-dialog modal-change-avatar";
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: this.getClassName(),
          role: 'document' },
        _react2.default.createElement(
          'div',
          { className: 'modal-content' },
          _react2.default.createElement(
            'div',
            { className: 'modal-header' },
            _react2.default.createElement(
              'button',
              { type: 'button', className: 'close', 'data-dismiss': 'modal',
                'aria-label': gettext("Close") },
              _react2.default.createElement(
                'span',
                { 'aria-hidden': 'true' },
                '×'
              )
            ),
            _react2.default.createElement(
              'h4',
              { className: 'modal-title' },
              gettext("Change your avatar")
            )
          ),
          this.getBody()
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;
function select(state) {
  return {
    'user': state.auth.user
  };
}

},{"../../reducers/users":90,"../../services/ajax":91,"../../services/store":100,"../modal-loader":61,"./crop":52,"./gallery":53,"./index":54,"./upload":56,"react":"react"}],56:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _crop = require('./crop');

var _crop2 = _interopRequireDefault(_crop);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _snackbar = require('../../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _fileSize = require('../../utils/file-size');

var _fileSize2 = _interopRequireDefault(_fileSize);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.pickFile = function () {
      document.getElementById('avatar-hidden-upload').click();
    };

    _this.uploadFile = function () {
      var image = document.getElementById('avatar-hidden-upload').files[0];

      var validationError = _this.validateFile(image);
      if (validationError) {
        _snackbar2.default.error(validationError);
        return;
      }

      _this.setState({
        image: image,
        'preview': URL.createObjectURL(image),
        'progress': 0
      });

      var data = new FormData();
      data.append('avatar', 'upload');
      data.append('image', image);

      _ajax2.default.upload(_this.props.user.api_url.avatar, data, function (progress) {
        _this.setState({
          progress: progress
        });
      }).then(function (data) {
        _this.setState({
          'options': data.options,
          'uploaded': data.detail
        });
        _snackbar2.default.info(gettext("Your image has been uploaded and you may now crop it."));
      }, function (rejection) {
        if (rejection.status === 400) {
          _snackbar2.default.error(rejection.detail);
          _this.setState({
            'isLoading': false,
            'image': null,
            'progress': 0
          });
        } else {
          _this.props.showError(rejection);
        }
      });
    };

    _this.state = {
      'image': null,
      'preview': null,
      'progress': 0,
      'uploaded': null
    };
    return _this;
  }

  _createClass(_class, [{
    key: 'validateFile',
    value: function validateFile(image) {
      if (image.size > this.props.options.upload.limit) {
        return interpolate(gettext("Selected file is too big. (%(filesize)s)"), {
          'filesize': (0, _fileSize2.default)(image.size)
        }, true);
      }

      var invalidTypeMsg = gettext("Selected file type is not supported.");
      if (this.props.options.upload.allowed_mime_types.indexOf(image.type) === -1) {
        return invalidTypeMsg;
      }

      var extensionFound = false;
      var loweredFilename = image.name.toLowerCase();
      this.props.options.upload.allowed_extensions.map(function (extension) {
        if (loweredFilename.substr(extension.length * -1) === extension) {
          extensionFound = true;
        }
      });

      if (!extensionFound) {
        return invalidTypeMsg;
      }

      return false;
    }

    /* jshint ignore:start */

  }, {
    key: 'getUploadRequirements',

    /* jshint ignore:end */

    value: function getUploadRequirements(options) {
      var extensions = options.allowed_extensions.map(function (extension) {
        return extension.substr(1);
      });

      return interpolate(gettext("%(files)s files smaller than %(limit)s"), {
        'files': extensions.join(', '),
        'limit': (0, _fileSize2.default)(options.limit)
      }, true);
    }
  }, {
    key: 'getUploadButton',
    value: function getUploadButton() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-body modal-avatar-upload' },
        _react2.default.createElement(
          _button2.default,
          { className: 'btn-pick-file',
            onClick: this.pickFile },
          _react2.default.createElement(
            'div',
            { className: 'material-icon' },
            'input'
          ),
          gettext("Select file")
        ),
        _react2.default.createElement(
          'p',
          { className: 'text-muted' },
          this.getUploadRequirements(this.props.options.upload)
        )
      );
      /* jshint ignore:end */
    }
  }, {
    key: 'getUploadProgressLabel',
    value: function getUploadProgressLabel() {
      return interpolate(gettext("%(progress)s % complete"), {
        'progress': this.state.progress
      }, true);
    }
  }, {
    key: 'getUploadProgress',
    value: function getUploadProgress() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-body modal-avatar-upload' },
        _react2.default.createElement(
          'div',
          { className: 'upload-progress' },
          _react2.default.createElement('img', { src: this.state.preview }),
          _react2.default.createElement(
            'div',
            { className: 'progress' },
            _react2.default.createElement(
              'div',
              { className: 'progress-bar', role: 'progressbar',
                'aria-valuenow': '{this.state.progress}',
                'aria-valuemin': '0', 'aria-valuemax': '100',
                style: { width: this.state.progress + '%' } },
              _react2.default.createElement(
                'span',
                { className: 'sr-only' },
                this.getUploadProgressLabel()
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }, {
    key: 'renderUpload',
    value: function renderUpload() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        null,
        _react2.default.createElement('input', { type: 'file',
          id: 'avatar-hidden-upload',
          className: 'hidden-file-upload',
          onChange: this.uploadFile }),
        this.state.image ? this.getUploadProgress() : this.getUploadButton(),
        _react2.default.createElement(
          'div',
          { className: 'modal-footer' },
          _react2.default.createElement(
            'div',
            { className: 'col-md-6 col-md-offset-3' },
            _react2.default.createElement(
              _button2.default,
              { onClick: this.props.showIndex,
                disabled: !!this.state.image,
                className: 'btn-default btn-block' },
              gettext("Cancel")
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }, {
    key: 'renderCrop',
    value: function renderCrop() {
      /* jshint ignore:start */
      return _react2.default.createElement(_crop2.default, { options: this.state.options,
        user: this.props.user,
        upload: this.state.uploaded,
        onComplete: this.props.onComplete,
        showError: this.props.showError,
        showIndex: this.props.showIndex });
      /* jshint ignore:end */
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return this.state.uploaded ? this.renderCrop() : this.renderUpload();
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../services/ajax":91,"../../services/snackbar":99,"../../utils/file-size":104,"../button":51,"./crop":52,"react":"react"}],57:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'isValidated',
    value: function isValidated() {
      return typeof this.props.validation !== "undefined";
    }
  }, {
    key: 'getClassName',
    value: function getClassName() {
      var className = 'form-group';
      if (this.isValidated()) {
        className += ' has-feedback';
        if (this.props.validation === null) {
          className += ' has-success';
        } else {
          className += ' has-error';
        }
      }
      return className;
    }
  }, {
    key: 'getFeedback',
    value: function getFeedback() {
      var _this2 = this;

      if (this.props.validation) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'div',
          { className: 'help-block errors' },
          this.props.validation.map(function (error, i) {
            return _react2.default.createElement(
              'p',
              { key: _this2.props.for + 'FeedbackItem' + i },
              error
            );
          })
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'getFeedbackIcon',
    value: function getFeedbackIcon() {
      if (this.isValidated()) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'span',
          { className: 'material-icon form-control-feedback',
            'aria-hidden': 'true', key: this.props.for + 'FeedbackIcon' },
          this.props.validation ? 'clear' : 'check'
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'getFeedbackDescription',
    value: function getFeedbackDescription() {
      if (this.isValidated()) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'span',
          { id: this.props.for + '_status', className: 'sr-only' },
          this.props.validation ? gettext('(error)') : gettext('(success)')
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'getHelpText',
    value: function getHelpText() {
      if (this.props.helpText) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'p',
          { className: 'help-block' },
          this.props.helpText
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: this.getClassName() },
        _react2.default.createElement(
          'label',
          { className: 'control-label ' + (this.props.labelClass || ''),
            htmlFor: this.props.for || '' },
          this.props.label + ':'
        ),
        _react2.default.createElement(
          'div',
          { className: this.props.controlClass || '' },
          this.props.children,
          this.getFeedbackIcon(),
          this.getFeedbackDescription(),
          this.getFeedback(),
          this.getHelpText(),
          this.props.extra || null
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],58:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _validators = require('../utils/validators');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var validateRequired = (0, _validators.required)();

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    var _Object$getPrototypeO;

    var _temp, _this, _ret;

    _classCallCheck(this, _class);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_Object$getPrototypeO = Object.getPrototypeOf(_class)).call.apply(_Object$getPrototypeO, [this].concat(args))), _this), _this.bindInput = function (name) {
      return function (event) {
        var newState = _defineProperty({}, name, event.target.value);

        var formErrors = _this.state.errors || {};
        formErrors[name] = _this.validateField(name, newState[name]);
        newState.errors = formErrors;

        _this.setState(newState);
      };
    }, _this.handleSubmit = function (event) {
      // we don't reload page on submissions
      event.preventDefault();
      if (_this.state.isLoading) {
        return;
      }

      if (_this.clean()) {
        _this.setState({ isLoading: true });
        var promise = _this.send();

        if (promise) {
          promise.then(function (success) {
            _this.setState({ isLoading: false });
            _this.handleSuccess(success);
          }, function (rejection) {
            _this.setState({ isLoading: false });
            _this.handleError(rejection);
          });
        } else {
          _this.setState({ isLoading: false });
        }
      }
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(_class, [{
    key: 'validate',
    value: function validate() {
      var errors = {};
      if (!this.state.validators) {
        return errors;
      }

      var validators = {
        required: this.state.validators.required || this.state.validators,
        optional: this.state.validators.optional || {}
      };

      var validatedFields = [];

      // add required fields to validation
      for (var name in validators.required) {
        if (validators.required.hasOwnProperty(name) && validators.required[name]) {
          validatedFields.push(name);
        }
      }

      // add optional fields to validation
      for (var name in validators.optional) {
        if (validators.optional.hasOwnProperty(name) && validators.optional[name]) {
          validatedFields.push(name);
        }
      }

      // validate fields values
      for (var i in validatedFields) {
        var name = validatedFields[i];
        var fieldErrors = this.validateField(name, this.state[name]);

        if (fieldErrors === null) {
          errors[name] = null;
        } else if (fieldErrors) {
          errors[name] = fieldErrors;
        }
      }

      return errors;
    }
  }, {
    key: 'isValid',
    value: function isValid() {
      var errors = this.validate();
      for (var field in errors) {
        if (errors.hasOwnProperty(field)) {
          if (errors[field] !== null) {
            return false;
          }
        }
      }

      return true;
    }
  }, {
    key: 'validateField',
    value: function validateField(name, value) {
      var errors = [];
      if (!this.state.validators) {
        return errors;
      }

      var validators = {
        required: (this.state.validators.required || this.state.validators)[name],
        optional: (this.state.validators.optional || {})[name]
      };

      var requiredError = validateRequired(value) || false;

      if (validators.required) {
        if (requiredError) {
          errors = [requiredError];
        } else {
          for (var i in validators.required) {
            var validationError = validators.required[i](value);
            if (validationError) {
              errors.push(validationError);
            }
          }
        }

        return errors.length ? errors : null;
      } else if (requiredError === false && validators.optional) {
        for (var i in validators.optional) {
          var validationError = validators.optional[i](value);
          if (validationError) {
            errors.push(validationError);
          }
        }

        return errors.length ? errors : null;
      }

      return false; // false === field wasn't validated
    }

    /* jshint ignore:start */

  }, {
    key: 'clean',
    value: function clean() {
      return true;
    }
  }, {
    key: 'send',
    value: function send() {
      return null;
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(success) {
      return;
    }
  }, {
    key: 'handleError',

    /* jshint ignore:end */
    value: function handleError(rejection) {
      return;
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../utils/validators":109,"react":"react"}],59:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'isActive',
    value: function isActive() {
      if (this.props.path) {
        return document.location.pathname.indexOf(this.props.path) === 0;
      } else {
        return false;
      }
    }
  }, {
    key: 'getClassName',
    value: function getClassName() {
      if (this.isActive()) {
        return (this.props.className || '') + ' ' + (this.props.activeClassName || 'active');
      } else {
        return this.props.className || '';
      }
    }
  }, {
    key: 'render',
    value: function render() {
      // jshint ignore:start
      return _react2.default.createElement(
        'li',
        { className: this.getClassName() },
        this.props.children
      );
      // jshint ignore:end
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],60:[function(require,module,exports){
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: "render",
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        "div",
        { className: this.props.className || "loader" },
        _react2.default.createElement("div", { className: "loader-spinning-wheel" })
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],61:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _loader = require('./loader');

var _loader2 = _interopRequireDefault(_loader);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// jshint ignore:line

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-body modal-loader' },
        _react2.default.createElement(_loader2.default, null)
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"./loader":60,"react":"react"}],62:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.UsernameHistory = exports.ChangeUsernameLoading = exports.NoChangesLeft = exports.ChangeUsername = undefined;

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _avatar = require('../avatar');

var _avatar2 = _interopRequireDefault(_avatar);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _form = require('../form');

var _form2 = _interopRequireDefault(_form);

var _formGroup = require('../form-group');

var _formGroup2 = _interopRequireDefault(_formGroup);

var _loader = require('../loader');

var _loader2 = _interopRequireDefault(_loader);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

var _usernameHistory = require('../../reducers/username-history');

var _users = require('../../reducers/users');

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _pageTitle = require('../../services/page-title');

var _pageTitle2 = _interopRequireDefault(_pageTitle);

var _snackbar = require('../../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _store = require('../../services/store');

var _store2 = _interopRequireDefault(_store);

var _random = require('../../utils/random');

var random = _interopRequireWildcard(_random);

var _validators = require('../../utils/validators');

var validators = _interopRequireWildcard(_validators);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var ChangeUsername = exports.ChangeUsername = function (_Form) {
  _inherits(ChangeUsername, _Form);

  function ChangeUsername(props) {
    _classCallCheck(this, ChangeUsername);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(ChangeUsername).call(this, props));

    _this.state = {
      username: '',

      validators: {
        username: [validators.usernameContent(), validators.usernameMinLength({
          username_length_min: props.options.length_min
        }), validators.usernameMaxLength({
          username_length_max: props.options.length_max
        })]
      },

      isLoading: false
    };
    return _this;
  }

  _createClass(ChangeUsername, [{
    key: 'getHelpText',
    value: function getHelpText() {
      var phrases = [];

      if (this.props.options.changes_left > 0) {
        var message = ngettext("You can change your username %(changes_left)s more time.", "You can change your username %(changes_left)s more times.", this.props.options.changes_left);

        phrases.push(interpolate(message, {
          'changes_left': this.props.options.changes_left
        }, true));
      }

      if (this.props.user.acl.name_changes_expire > 0) {
        var message = ngettext("Used changes redeem after %(name_changes_expire)s day.", "Used changes redeem after %(name_changes_expire)s days.", this.props.user.acl.name_changes_expire);

        phrases.push(interpolate(message, {
          'name_changes_expire': this.props.user.acl.name_changes_expire
        }, true));
      }

      return phrases.length ? phrases.join(' ') : null;
    }
  }, {
    key: 'clean',
    value: function clean() {
      var errors = this.validate();
      if (errors.username) {
        _snackbar2.default.error(errors.username[0]);
        return false;
      }if (this.state.username.trim() === this.props.user.username) {
        _snackbar2.default.info(gettext("Your new username is same as current one."));
        return false;
      } else {
        return true;
      }
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(this.props.user.api_url.username, {
        'username': this.state.username
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(success) {
      this.setState({
        'username': ''
      });

      this.props.complete(success.username, success.slug, success.options);
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      _snackbar2.default.apiError(rejection);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'form',
        { onSubmit: this.handleSubmit, className: 'form-horizontal' },
        _react2.default.createElement(
          'div',
          { className: 'panel panel-default panel-form' },
          _react2.default.createElement(
            'div',
            { className: 'panel-heading' },
            _react2.default.createElement(
              'h3',
              { className: 'panel-title' },
              gettext("Change username")
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-body' },
            _react2.default.createElement(
              _formGroup2.default,
              { label: gettext("New username"), 'for': 'id_username',
                labelClass: 'col-sm-4', controlClass: 'col-sm-8',
                helpText: this.getHelpText() },
              _react2.default.createElement('input', { type: 'text', id: 'id_username', className: 'form-control',
                disabled: this.state.isLoading,
                onChange: this.bindInput('username'),
                value: this.state.username })
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-footer' },
            _react2.default.createElement(
              'div',
              { className: 'row' },
              _react2.default.createElement(
                'div',
                { className: 'col-sm-8 col-sm-offset-4' },
                _react2.default.createElement(
                  _button2.default,
                  { className: 'btn-primary', loading: this.state.isLoading },
                  gettext("Change username")
                )
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ChangeUsername;
}(_form2.default);

var NoChangesLeft = exports.NoChangesLeft = function (_React$Component) {
  _inherits(NoChangesLeft, _React$Component);

  function NoChangesLeft() {
    _classCallCheck(this, NoChangesLeft);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(NoChangesLeft).apply(this, arguments));
  }

  _createClass(NoChangesLeft, [{
    key: 'getHelpText',
    value: function getHelpText() {
      if (this.props.options.next_on) {
        return interpolate(gettext("You will be able to change your username %(next_change)s."), { 'next_change': this.props.options.next_on.fromNow() }, true);
      } else {
        return gettext("You have used up available name changes.");
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'panel panel-default panel-form' },
        _react2.default.createElement(
          'div',
          { className: 'panel-heading' },
          _react2.default.createElement(
            'h3',
            { className: 'panel-title' },
            gettext("Change username")
          )
        ),
        _react2.default.createElement(
          'div',
          { className: 'panel-body panel-message-body' },
          _react2.default.createElement(
            'div',
            { className: 'message-icon' },
            _react2.default.createElement(
              'span',
              { className: 'material-icon' },
              'info_outline'
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'message-body' },
            _react2.default.createElement(
              'p',
              { className: 'lead' },
              gettext("You can't change your username at the moment.")
            ),
            _react2.default.createElement(
              'p',
              { className: 'help-block' },
              this.getHelpText()
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return NoChangesLeft;
}(_react2.default.Component);

var ChangeUsernameLoading = exports.ChangeUsernameLoading = function (_React$Component2) {
  _inherits(ChangeUsernameLoading, _React$Component2);

  function ChangeUsernameLoading() {
    _classCallCheck(this, ChangeUsernameLoading);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(ChangeUsernameLoading).apply(this, arguments));
  }

  _createClass(ChangeUsernameLoading, [{
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'panel panel-default panel-form' },
        _react2.default.createElement(
          'div',
          { className: 'panel-heading' },
          _react2.default.createElement(
            'h3',
            { className: 'panel-title' },
            gettext("Change username")
          )
        ),
        _react2.default.createElement(
          'div',
          { className: 'panel-body panel-body-loading' },
          _react2.default.createElement(_loader2.default, { className: 'loader loader-spaced' })
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ChangeUsernameLoading;
}(_react2.default.Component);

var UsernameHistory = exports.UsernameHistory = function (_React$Component3) {
  _inherits(UsernameHistory, _React$Component3);

  function UsernameHistory() {
    _classCallCheck(this, UsernameHistory);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(UsernameHistory).apply(this, arguments));
  }

  _createClass(UsernameHistory, [{
    key: 'renderUserAvatar',
    value: function renderUserAvatar(item) {
      if (item.changed_by) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'a',
          { href: item.changed_by.absolute_url, className: 'user-avatar' },
          _react2.default.createElement(_avatar2.default, { user: item.changed_by, size: '100' })
        );
        /* jshint ignore:end */
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(
            'span',
            { className: 'user-avatar' },
            _react2.default.createElement(_avatar2.default, { size: '100' })
          );
          /* jshint ignore:end */
        }
    }
  }, {
    key: 'renderUsername',
    value: function renderUsername(item) {
      if (item.changed_by) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'a',
          { href: item.changed_by.absolute_url, className: 'item-title' },
          item.changed_by.username
        );
        /* jshint ignore:end */
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(
            'span',
            { className: 'item-title' },
            item.changed_by_username
          );
          /* jshint ignore:end */
        }
    }
  }, {
    key: 'renderHistory',
    value: function renderHistory() {
      var _this5 = this;

      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'username-history ui-ready' },
        _react2.default.createElement(
          'ul',
          { className: 'list-group' },
          this.props.changes.map(function (item) {
            return _react2.default.createElement(
              'li',
              { className: 'list-group-item', key: item.id },
              _react2.default.createElement(
                'div',
                { className: 'username-change-avatar' },
                _this5.renderUserAvatar(item)
              ),
              _react2.default.createElement(
                'div',
                { className: 'username-change-author' },
                _this5.renderUsername(item)
              ),
              _react2.default.createElement(
                'div',
                { className: 'username-change' },
                item.old_username,
                _react2.default.createElement(
                  'span',
                  { className: 'material-icon' },
                  'arrow_forward'
                ),
                item.new_username
              ),
              _react2.default.createElement(
                'div',
                { className: 'username-change-date' },
                _react2.default.createElement(
                  'abbr',
                  { title: item.changed_on.format('LLL') },
                  item.changed_on.fromNow()
                )
              )
            );
          })
        )
      );
      /* jshint ignore:end */
    }
  }, {
    key: 'renderEmptyHistory',
    value: function renderEmptyHistory() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'username-history ui-ready' },
        _react2.default.createElement(
          'ul',
          { className: 'list-group' },
          _react2.default.createElement(
            'li',
            { className: 'list-group-item empty-message' },
            gettext("No name changes have been recorded for your account.")
          )
        )
      );
      /* jshint ignore:end */
    }
  }, {
    key: 'renderHistoryPreview',
    value: function renderHistoryPreview() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'username-history ui-preview' },
        _react2.default.createElement(
          'ul',
          { className: 'list-group' },
          random.range(3, 5).map(function (i) {
            return _react2.default.createElement(
              'li',
              { className: 'list-group-item', key: i },
              _react2.default.createElement(
                'div',
                { className: 'username-change-avatar' },
                _react2.default.createElement(
                  'span',
                  { className: 'user-avatar' },
                  _react2.default.createElement(_avatar2.default, { size: '100' })
                )
              ),
              _react2.default.createElement(
                'div',
                { className: 'username-change-author' },
                _react2.default.createElement(
                  'span',
                  { className: 'ui-preview-text', style: { width: random.int(30, 100) + "px" } },
                  ' '
                )
              ),
              _react2.default.createElement(
                'div',
                { className: 'username-change' },
                _react2.default.createElement(
                  'span',
                  { className: 'ui-preview-text', style: { width: random.int(30, 50) + "px" } },
                  ' '
                ),
                _react2.default.createElement(
                  'span',
                  { className: 'material-icon' },
                  'arrow_forward'
                ),
                _react2.default.createElement(
                  'span',
                  { className: 'ui-preview-text', style: { width: random.int(30, 50) + "px" } },
                  ' '
                )
              ),
              _react2.default.createElement(
                'div',
                { className: 'username-change-date' },
                _react2.default.createElement(
                  'span',
                  { className: 'ui-preview-text', style: { width: random.int(50, 100) + "px" } },
                  ' '
                )
              )
            );
          })
        )
      );
      /* jshint ignore:end */
    }
  }, {
    key: 'render',
    value: function render() {
      if (this.props.isLoaded) {
        if (this.props.changes.length) {
          return this.renderHistory();
        } else {
          return this.renderEmptyHistory();
        }
      } else {
        return this.renderHistoryPreview();
      }
    }
  }]);

  return UsernameHistory;
}(_react2.default.Component);

var _class = function (_React$Component4) {
  _inherits(_class, _React$Component4);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this6 = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this6.onComplete = function (username, slug, options) {
      _this6.setState({
        options: options
      });

      _store2.default.dispatch((0, _usernameHistory.addNameChange)({ username: username, slug: slug }, _this6.props.user, _this6.props.user));
      _store2.default.dispatch((0, _users.updateUsername)(_this6.props.user, username, slug));

      _snackbar2.default.success(gettext("Your username has been changed successfully."));
    };

    _this6.state = {
      isLoaded: false,
      options: null
    };
    return _this6;
  }

  _createClass(_class, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this7 = this;

      _pageTitle2.default.set({
        title: gettext("Change username"),
        parent: gettext("Change your options")
      });

      Promise.all([_ajax2.default.get(this.props.user.api_url.username), _ajax2.default.get(_index2.default.get('USERNAME_CHANGES_API'), { user: this.props.user.id })]).then(function (data) {
        _this7.setState({
          isLoaded: true,
          options: {
            changes_left: data[0].changes_left,
            length_min: data[0].length_min,
            length_max: data[0].length_max,
            next_on: data[0].next_on ? (0, _moment2.default)(data[0].next_on) : null
          }
        });

        _store2.default.dispatch((0, _usernameHistory.dehydrate)(data[1].results));
      });
    }

    /* jshint ignore:start */

  }, {
    key: 'getChangeForm',

    /* jshint ignore:end */

    value: function getChangeForm() {
      if (this.state.isLoaded) {
        if (this.state.options.changes_left > 0) {
          /* jshint ignore:start */
          return _react2.default.createElement(ChangeUsername, { user: this.props.user,
            options: this.state.options,
            complete: this.onComplete });
          /* jshint ignore:end */
        } else {
            /* jshint ignore:start */
            return _react2.default.createElement(NoChangesLeft, { options: this.state.options });
            /* jshint ignore:end */
          }
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(ChangeUsernameLoading, null);
          /* jshint ignore:end */
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        null,
        this.getChangeForm(),
        _react2.default.createElement(UsernameHistory, { isLoaded: this.state.isLoaded,
          changes: this.props['username-history'] })
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../index":85,"../../reducers/username-history":89,"../../reducers/users":90,"../../services/ajax":91,"../../services/page-title":98,"../../services/snackbar":99,"../../services/store":100,"../../utils/random":107,"../../utils/validators":109,"../avatar":49,"../button":51,"../form":58,"../form-group":57,"../loader":60,"moment":"moment","react":"react"}],63:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _form = require('../form');

var _form2 = _interopRequireDefault(_form);

var _formGroup = require('../form-group');

var _formGroup2 = _interopRequireDefault(_formGroup);

var _select = require('../select');

var _select2 = _interopRequireDefault(_select);

var _yesNoSwitch = require('../yes-no-switch');

var _yesNoSwitch2 = _interopRequireDefault(_yesNoSwitch);

var _auth = require('../../reducers/auth');

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _pageTitle = require('../../services/page-title');

var _pageTitle2 = _interopRequireDefault(_pageTitle);

var _snackbar = require('../../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _store = require('../../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var _class = function (_Form) {
  _inherits(_class, _Form);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.state = {
      'isLoading': false,

      'is_hiding_presence': props.user.is_hiding_presence,
      'limits_private_thread_invites_to': props.user.limits_private_thread_invites_to,
      'subscribe_to_started_threads': props.user.subscribe_to_started_threads,
      'subscribe_to_replied_threads': props.user.subscribe_to_replied_threads,

      'errors': {}
    };

    _this.privateThreadInvitesChoices = [{
      'value': 0,
      'icon': 'help_outline',
      'label': gettext('Everybody')
    }, {
      'value': 1,
      'icon': 'done_all',
      'label': gettext('Users I follow')
    }, {
      'value': 2,
      'icon': 'highlight_off',
      'label': gettext('Nobody')
    }];

    _this.subscribeToChoices = [{
      'value': 0,
      'icon': 'bookmark_border',
      'label': gettext('No')
    }, {
      'value': 1,
      'icon': 'bookmark',
      'label': gettext('Bookmark')
    }, {
      'value': 2,
      'icon': 'mail',
      'label': gettext('Bookmark with e-mail notification')
    }];
    return _this;
  }

  _createClass(_class, [{
    key: 'send',
    value: function send() {
      return _ajax2.default.post(this.props.user.api_url.options, {
        'is_hiding_presence': this.state.is_hiding_presence,
        'limits_private_thread_invites_to': this.state.limits_private_thread_invites_to,
        'subscribe_to_started_threads': this.state.subscribe_to_started_threads,
        'subscribe_to_replied_threads': this.state.subscribe_to_replied_threads
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess() {
      _store2.default.dispatch((0, _auth.patchUser)({
        'is_hiding_presence': this.state.is_hiding_presence,
        'limits_private_thread_invites_to': this.state.limits_private_thread_invites_to,
        'subscribe_to_started_threads': this.state.subscribe_to_started_threads,
        'subscribe_to_replied_threads': this.state.subscribe_to_replied_threads
      }));
      _snackbar2.default.success(gettext("Your forum options have been changed."));
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (rejection.status === 400) {
        _snackbar2.default.error(gettext("Please reload page and try again."));
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'componentDidMount',
    value: function componentDidMount() {
      _pageTitle2.default.set({
        title: gettext("Forum options"),
        parent: gettext("Change your options")
      });
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'form',
        { onSubmit: this.handleSubmit, className: 'form-horizontal' },
        _react2.default.createElement(
          'div',
          { className: 'panel panel-default panel-form' },
          _react2.default.createElement(
            'div',
            { className: 'panel-heading' },
            _react2.default.createElement(
              'h3',
              { className: 'panel-title' },
              gettext("Change forum options")
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-body' },
            _react2.default.createElement(
              'fieldset',
              null,
              _react2.default.createElement(
                'legend',
                null,
                gettext("Privacy settings")
              ),
              _react2.default.createElement(
                _formGroup2.default,
                { label: gettext("Hide my presence"),
                  helpText: gettext("If you hide your presence, only members with permission to see hidden users will see when you are online."),
                  'for': 'id_is_hiding_presence',
                  labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
                _react2.default.createElement(_yesNoSwitch2.default, { id: 'id_is_hiding_presence',
                  disabled: this.state.isLoading,
                  iconOn: 'visibility',
                  iconOff: 'visibility_off',
                  labelOn: gettext("Show my presence to other users"),
                  labelOff: gettext("Hide my presence from other users"),
                  onChange: this.bindInput('is_hiding_presence'),
                  value: this.state.is_hiding_presence })
              ),
              _react2.default.createElement(
                _formGroup2.default,
                { label: gettext("Private thread invitations"),
                  'for': 'id_limits_private_thread_invites_to',
                  labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
                _react2.default.createElement(_select2.default, { id: 'id_limits_private_thread_invites_to',
                  disabled: this.state.isLoading,
                  onChange: this.bindInput('limits_private_thread_invites_to'),
                  value: this.state.limits_private_thread_invites_to,
                  choices: this.privateThreadInvitesChoices })
              )
            ),
            _react2.default.createElement(
              'fieldset',
              null,
              _react2.default.createElement(
                'legend',
                null,
                gettext("Automatic subscriptions")
              ),
              _react2.default.createElement(
                _formGroup2.default,
                { label: gettext("Threads I start"),
                  'for': 'id_subscribe_to_started_threads',
                  labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
                _react2.default.createElement(_select2.default, { id: 'id_subscribe_to_started_threads',
                  disabled: this.state.isLoading,
                  onChange: this.bindInput('subscribe_to_started_threads'),
                  value: this.state.subscribe_to_started_threads,
                  choices: this.subscribeToChoices })
              ),
              _react2.default.createElement(
                _formGroup2.default,
                { label: gettext("Threads I reply to"),
                  'for': 'id_subscribe_to_replied_threads',
                  labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
                _react2.default.createElement(_select2.default, { id: 'id_subscribe_to_replied_threads',
                  disabled: this.state.isLoading,
                  onChange: this.bindInput('subscribe_to_replied_threads'),
                  value: this.state.subscribe_to_replied_threads,
                  choices: this.subscribeToChoices })
              )
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-footer' },
            _react2.default.createElement(
              'div',
              { className: 'row' },
              _react2.default.createElement(
                'div',
                { className: 'col-sm-8 col-sm-offset-4' },
                _react2.default.createElement(
                  _button2.default,
                  { className: 'btn-primary', loading: this.state.isLoading },
                  gettext("Save changes")
                )
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_form2.default);

exports.default = _class;

},{"../../reducers/auth":86,"../../services/ajax":91,"../../services/page-title":98,"../../services/snackbar":99,"../../services/store":100,"../button":51,"../form":58,"../form-group":57,"../select":73,"../yes-no-switch":84,"react":"react"}],64:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.CompactNav = exports.SideNav = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRouter = require('react-router');

var _li = require('../li');

var _li2 = _interopRequireDefault(_li);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
//jshint ignore:line

//jshint ignore:line

var SideNav = exports.SideNav = function (_React$Component) {
  _inherits(SideNav, _React$Component);

  function SideNav() {
    _classCallCheck(this, SideNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(SideNav).apply(this, arguments));
  }

  _createClass(SideNav, [{
    key: 'render',
    value: function render() {
      var _this2 = this;

      // jshint ignore:start
      return _react2.default.createElement(
        'div',
        { className: 'list-group nav-side' },
        this.props.options.map(function (option) {
          return _react2.default.createElement(
            _reactRouter.Link,
            { to: _this2.props.baseUrl + option.component + '/',
              className: 'list-group-item',
              activeClassName: 'active',
              key: option.component },
            _react2.default.createElement(
              'span',
              { className: 'material-icon' },
              option.icon
            ),
            option.name
          );
        })
      );
      // jshint ignore:end
    }
  }]);

  return SideNav;
}(_react2.default.Component);

var CompactNav = exports.CompactNav = function (_React$Component2) {
  _inherits(CompactNav, _React$Component2);

  function CompactNav() {
    _classCallCheck(this, CompactNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(CompactNav).apply(this, arguments));
  }

  _createClass(CompactNav, [{
    key: 'render',
    value: function render() {
      var _this4 = this;

      // jshint ignore:start
      return _react2.default.createElement(
        'ul',
        { className: 'dropdown-menu', role: 'menu' },
        this.props.options.map(function (option) {
          return _react2.default.createElement(
            _li2.default,
            { path: _this4.props.baseUrl + option.component + '/',
              key: option.component },
            _react2.default.createElement(
              _reactRouter.Link,
              { to: _this4.props.baseUrl + option.component + '/' },
              _react2.default.createElement(
                'span',
                { className: 'material-icon' },
                option.icon
              ),
              option.name
            )
          );
        })
      );
      // jshint ignore:end
    }
  }]);

  return CompactNav;
}(_react2.default.Component);

},{"../../index":85,"../li":59,"react":"react","react-router":"react-router"}],65:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.select = select;
exports.paths = paths;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRedux = require('react-redux');

var _navs = require('./navs');

var _forumOptions = require('./forum-options');

var _forumOptions2 = _interopRequireDefault(_forumOptions);

var _changeUsername = require('./change-username');

var _changeUsername2 = _interopRequireDefault(_changeUsername);

var _signInCredentials = require('./sign-in-credentials');

var _signInCredentials2 = _interopRequireDefault(_signInCredentials);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.toggleNav = function () {
      if (_this.state.dropdown) {
        _this.setState({
          dropdown: false
        });
      } else {
        _this.setState({
          dropdown: true
        });
      }
    };

    _this.state = {
      dropdown: false
    };
    return _this;
  }

  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'getToggleNavClassName',

    /* jshint ignore:end */

    value: function getToggleNavClassName() {
      if (this.state.dropdown) {
        return 'btn btn-default btn-icon open';
      } else {
        return 'btn btn-default btn-icon';
      }
    }
  }, {
    key: 'getCompactNavClassName',
    value: function getCompactNavClassName() {
      if (this.state.dropdown) {
        return 'compact-nav open';
      } else {
        return 'compact-nav';
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'page page-options' },
        _react2.default.createElement(
          'div',
          { className: 'page-header' },
          _react2.default.createElement(
            'div',
            { className: 'container' },
            _react2.default.createElement(
              'h1',
              { className: 'pull-left' },
              gettext("Change your options")
            ),
            _react2.default.createElement(
              'button',
              { className: 'btn btn-default btn-icon btn-dropdown-toggle hidden-md hidden-lg',
                type: 'button',
                onClick: this.toggleNav,
                'aria-haspopup': 'true',
                'aria-expanded': this.state.dropdown ? 'true' : 'false' },
              _react2.default.createElement(
                'i',
                { className: 'material-icon' },
                'menu'
              )
            )
          )
        ),
        _react2.default.createElement(
          'div',
          { className: this.getCompactNavClassName() },
          _react2.default.createElement(_navs.CompactNav, { options: _index2.default.get('USER_OPTIONS'),
            baseUrl: _index2.default.get('USERCP_URL') })
        ),
        _react2.default.createElement(
          'div',
          { className: 'container' },
          _react2.default.createElement(
            'div',
            { className: 'row' },
            _react2.default.createElement(
              'div',
              { className: 'col-md-3 hidden-xs hidden-sm' },
              _react2.default.createElement(_navs.SideNav, { options: _index2.default.get('USER_OPTIONS'),
                baseUrl: _index2.default.get('USERCP_URL') })
            ),
            _react2.default.createElement(
              'div',
              { className: 'col-md-9' },
              this.props.children
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;
function select(store) {
  return {
    'tick': store.tick.tick,
    'user': store.auth.user,
    'username-history': store['username-history']
  };
}

function paths() {
  return [{
    path: _index2.default.get('USERCP_URL') + 'forum-options/',
    component: (0, _reactRedux.connect)(select)(_forumOptions2.default)
  }, {
    path: _index2.default.get('USERCP_URL') + 'change-username/',
    component: (0, _reactRedux.connect)(select)(_changeUsername2.default)
  }, {
    path: _index2.default.get('USERCP_URL') + 'sign-in-credentials/',
    component: (0, _reactRedux.connect)(select)(_signInCredentials2.default)
  }];
}

},{"../../index":85,"./change-username":62,"./forum-options":63,"./navs":64,"./sign-in-credentials":66,"react":"react","react-redux":"react-redux"}],66:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.ChangePassword = exports.ChangeEmail = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _form = require('../form');

var _form2 = _interopRequireDefault(_form);

var _formGroup = require('../form-group');

var _formGroup2 = _interopRequireDefault(_formGroup);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

var _ajax = require('../../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _pageTitle = require('../../services/page-title');

var _pageTitle2 = _interopRequireDefault(_pageTitle);

var _snackbar = require('../../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _validators = require('../../utils/validators');

var validators = _interopRequireWildcard(_validators);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line

var ChangeEmail = exports.ChangeEmail = function (_Form) {
  _inherits(ChangeEmail, _Form);

  function ChangeEmail(props) {
    _classCallCheck(this, ChangeEmail);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(ChangeEmail).call(this, props));

    _this.state = {
      new_email: '',
      password: '',

      validators: {
        new_email: [validators.email()],
        password: []
      },

      isLoading: false
    };
    return _this;
  }

  _createClass(ChangeEmail, [{
    key: 'clean',
    value: function clean() {
      var errors = this.validate();
      var lengths = [this.state.new_email.trim().length, this.state.password.trim().length];

      if (lengths.indexOf(0) !== -1) {
        _snackbar2.default.error(gettext("Fill out all fields."));
        return false;
      }

      if (errors.new_email) {
        _snackbar2.default.error(errors.new_email[0]);
        return false;
      }

      return true;
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(this.props.user.api_url.change_email, {
        new_email: this.state.new_email,
        password: this.state.password
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(response) {
      this.setState({
        new_email: '',
        password: ''
      });

      _snackbar2.default.success(response.detail);
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (rejection.status === 400) {
        if (rejection.new_email) {
          _snackbar2.default.error(rejection.new_email);
        } else {
          _snackbar2.default.error(rejection.password);
        }
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'form',
        { onSubmit: this.handleSubmit, className: 'form-horizontal' },
        _react2.default.createElement('input', { type: 'type', style: { display: 'none' } }),
        _react2.default.createElement('input', { type: 'password', style: { display: 'none' } }),
        _react2.default.createElement(
          'div',
          { className: 'panel panel-default panel-form' },
          _react2.default.createElement(
            'div',
            { className: 'panel-heading' },
            _react2.default.createElement(
              'h3',
              { className: 'panel-title' },
              gettext("Change e-mail address")
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-body' },
            _react2.default.createElement(
              _formGroup2.default,
              { label: gettext("New e-mail"), 'for': 'id_new_email',
                labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
              _react2.default.createElement('input', { type: 'text', id: 'id_new_email', className: 'form-control',
                disabled: this.state.isLoading,
                onChange: this.bindInput('new_email'),
                value: this.state.new_email })
            ),
            _react2.default.createElement('hr', null),
            _react2.default.createElement(
              _formGroup2.default,
              { label: gettext("Your current password"), 'for': 'id_password',
                labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
              _react2.default.createElement('input', { type: 'password', id: 'id_password', className: 'form-control',
                disabled: this.state.isLoading,
                onChange: this.bindInput('password'),
                value: this.state.password })
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-footer' },
            _react2.default.createElement(
              'div',
              { className: 'row' },
              _react2.default.createElement(
                'div',
                { className: 'col-sm-8 col-sm-offset-4' },
                _react2.default.createElement(
                  _button2.default,
                  { className: 'btn-primary', loading: this.state.isLoading },
                  gettext("Change e-mail")
                )
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ChangeEmail;
}(_form2.default);

var ChangePassword = exports.ChangePassword = function (_Form2) {
  _inherits(ChangePassword, _Form2);

  function ChangePassword(props) {
    _classCallCheck(this, ChangePassword);

    var _this2 = _possibleConstructorReturn(this, Object.getPrototypeOf(ChangePassword).call(this, props));

    _this2.state = {
      new_password: '',
      repeat_password: '',
      password: '',

      validators: {
        new_password: [validators.passwordMinLength(_index2.default.get('SETTINGS'))],
        repeat_password: [],
        password: []
      },

      isLoading: false
    };
    return _this2;
  }

  _createClass(ChangePassword, [{
    key: 'clean',
    value: function clean() {
      var errors = this.validate();
      var lengths = [this.state.new_password.trim().length, this.state.repeat_password.trim().length, this.state.password.trim().length];

      if (lengths.indexOf(0) !== -1) {
        _snackbar2.default.error(gettext("Fill out all fields."));
        return false;
      }

      if (errors.new_password) {
        _snackbar2.default.error(errors.new_password[0]);
        return false;
      }

      if (this.state.new_password.trim() !== this.state.repeat_password.trim()) {
        _snackbar2.default.error(gettext("New passwords are different."));
        return false;
      }

      return true;
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(this.props.user.api_url.change_password, {
        new_password: this.state.new_password,
        password: this.state.password
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(response) {
      this.setState({
        new_password: '',
        repeat_password: '',
        password: ''
      });

      _snackbar2.default.success(response.detail);
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (rejection.status === 400) {
        if (rejection.new_password) {
          _snackbar2.default.error(rejection.new_password);
        } else {
          _snackbar2.default.error(rejection.password);
        }
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'form',
        { onSubmit: this.handleSubmit, className: 'form-horizontal' },
        _react2.default.createElement('input', { type: 'type', style: { display: 'none' } }),
        _react2.default.createElement('input', { type: 'password', style: { display: 'none' } }),
        _react2.default.createElement(
          'div',
          { className: 'panel panel-default panel-form' },
          _react2.default.createElement(
            'div',
            { className: 'panel-heading' },
            _react2.default.createElement(
              'h3',
              { className: 'panel-title' },
              gettext("Change password")
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-body' },
            _react2.default.createElement(
              _formGroup2.default,
              { label: gettext("New password"), 'for': 'id_new_password',
                labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
              _react2.default.createElement('input', { type: 'password', id: 'id_new_password', className: 'form-control',
                disabled: this.state.isLoading,
                onChange: this.bindInput('new_password'),
                value: this.state.new_password })
            ),
            _react2.default.createElement(
              _formGroup2.default,
              { label: gettext("Repeat password"), 'for': 'id_repeat_password',
                labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
              _react2.default.createElement('input', { type: 'password', id: 'id_repeat_password', className: 'form-control',
                disabled: this.state.isLoading,
                onChange: this.bindInput('repeat_password'),
                value: this.state.repeat_password })
            ),
            _react2.default.createElement('hr', null),
            _react2.default.createElement(
              _formGroup2.default,
              { label: gettext("Your current password"), 'for': 'id_password',
                labelClass: 'col-sm-4', controlClass: 'col-sm-8' },
              _react2.default.createElement('input', { type: 'password', id: 'id_password', className: 'form-control',
                disabled: this.state.isLoading,
                onChange: this.bindInput('password'),
                value: this.state.password })
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'panel-footer' },
            _react2.default.createElement(
              'div',
              { className: 'row' },
              _react2.default.createElement(
                'div',
                { className: 'col-sm-8 col-sm-offset-4' },
                _react2.default.createElement(
                  _button2.default,
                  { className: 'btn-primary', loading: this.state.isLoading },
                  gettext("Change password")
                )
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ChangePassword;
}(_form2.default);

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      _pageTitle2.default.set({
        title: gettext("Change email or password"),
        parent: gettext("Change your options")
      });
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        null,
        _react2.default.createElement(ChangeEmail, { user: this.props.user }),
        _react2.default.createElement(ChangePassword, { user: this.props.user }),
        _react2.default.createElement(
          'p',
          { className: 'message-line' },
          _react2.default.createElement(
            'span',
            { className: 'material-icon' },
            'warning'
          ),
          _react2.default.createElement(
            'a',
            { href: _index2.default.get('FORGOTTEN_PASSWORD_URL') },
            gettext("Change forgotten password")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../index":85,"../../services/ajax":91,"../../services/page-title":98,"../../services/snackbar":99,"../../utils/validators":109,"../button":51,"../form":58,"../form-group":57,"react":"react"}],67:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.LABELS = exports.STYLES = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _zxcvbn = require('../services/zxcvbn');

var _zxcvbn2 = _interopRequireDefault(_zxcvbn);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var STYLES = exports.STYLES = ['progress-bar-danger', 'progress-bar-warning', 'progress-bar-warning', 'progress-bar-primary', 'progress-bar-success'];

var LABELS = exports.LABELS = [gettext("Entered password is very weak."), gettext("Entered password is weak."), gettext("Entered password is average."), gettext("Entered password is strong."), gettext("Entered password is very strong.")];

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this._score = 0;
    _this._password = null;
    _this._inputs = [];
    return _this;
  }

  _createClass(_class, [{
    key: 'getScore',
    value: function getScore(password, inputs) {
      var _this2 = this;

      var cacheStale = false;

      if (password.trim() !== this._password) {
        cacheStale = true;
      }

      if (inputs.length !== this._inputs.length) {
        cacheStale = true;
      } else {
        inputs.map(function (value, i) {
          if (value.trim() !== _this2._inputs[i]) {
            cacheStale = true;
          }
        });
      }

      if (cacheStale) {
        this._score = _zxcvbn2.default.scorePassword(password, inputs);
        this._password = password.trim();
        this._inputs = inputs.map(function (value) {
          return value.trim();
        });
      }

      return this._score;
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      var score = this.getScore(this.props.password, this.props.inputs);

      return _react2.default.createElement(
        'div',
        { className: 'help-block password-strength' },
        _react2.default.createElement(
          'div',
          { className: 'progress' },
          _react2.default.createElement(
            'div',
            { className: "progress-bar " + STYLES[score],
              style: { width: 20 + 20 * score + '%' },
              role: 'progress-bar',
              'aria-valuenow': score,
              'aria-valuemin': '0',
              'aria-valuemax': '4' },
            _react2.default.createElement(
              'span',
              { className: 'sr-only' },
              LABELS[score]
            )
          )
        ),
        _react2.default.createElement(
          'p',
          { className: 'text-small' },
          LABELS[score]
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../services/zxcvbn":101,"react":"react"}],68:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _loader = require('./loader');

var _loader2 = _interopRequireDefault(_loader);

var _register = require('./register.js');

var _register2 = _interopRequireDefault(_register);

var _captcha = require('../services/captcha');

var _captcha2 = _interopRequireDefault(_captcha);

var _modal = require('../services/modal');

var _modal2 = _interopRequireDefault(_modal);

var _snackbar = require('../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _zxcvbn = require('../services/zxcvbn');

var _zxcvbn2 = _interopRequireDefault(_zxcvbn);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

// jshint ignore:line

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.showRegisterModal = function () {
      if (misago.get('SETTINGS').account_activation === 'closed') {
        _snackbar2.default.info(gettext("New registrations are currently disabled."));
      } else if (_this.state.isLoaded) {
        _modal2.default.show(_register2.default);
      } else {
        _this.setState({
          'isLoading': true
        });

        Promise.all([_captcha2.default.load(), _zxcvbn2.default.load()]).then(function () {
          if (!_this.state.isLoaded) {
            _this.setState({
              'isLoading': false,
              'isLoaded': false
            });
          }

          _modal2.default.show(_register2.default);
        });
      }
    };

    _this.state = {
      'isLoading': false,
      'isLoaded': false
    };
    return _this;
  }

  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'getClassName',

    /* jshint ignore:end */

    value: function getClassName() {
      return this.props.className + (this.state.isLoading ? ' btn-loading' : '');
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'button',
        { type: 'button', onClick: this.showRegisterModal,
          className: 'btn ' + this.getClassName(),
          disabled: this.state.isLoaded },
        gettext("Register"),
        this.state.isLoading ? _react2.default.createElement(_loader2.default, null) : null
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../services/captcha":93,"../services/modal":97,"../services/snackbar":99,"../services/zxcvbn":101,"./loader":60,"./register.js":69,"react":"react"}],69:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.RegisterComplete = exports.RegisterForm = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _button = require('./button');

var _button2 = _interopRequireDefault(_button);

var _form = require('./form');

var _form2 = _interopRequireDefault(_form);

var _formGroup = require('./form-group');

var _formGroup2 = _interopRequireDefault(_formGroup);

var _passwordStrength = require('./password-strength');

var _passwordStrength2 = _interopRequireDefault(_passwordStrength);

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _ajax = require('../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _auth = require('../services/auth');

var _auth2 = _interopRequireDefault(_auth);

var _captcha = require('../services/captcha');

var _captcha2 = _interopRequireDefault(_captcha);

var _modal = require('../services/modal');

var _modal2 = _interopRequireDefault(_modal);

var _snackbar = require('../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _bannedPage = require('../utils/banned-page');

var _bannedPage2 = _interopRequireDefault(_bannedPage);

var _validators = require('../utils/validators');

var validators = _interopRequireWildcard(_validators);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var RegisterForm = exports.RegisterForm = function (_Form) {
  _inherits(RegisterForm, _Form);

  function RegisterForm(props) {
    _classCallCheck(this, RegisterForm);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(RegisterForm).call(this, props));

    _this.state = {
      'isLoading': false,

      'username': '',
      'email': '',
      'password': '',
      'captcha': '',

      'validators': {
        'username': [validators.usernameContent(), validators.usernameMinLength(_index2.default.get('SETTINGS')), validators.usernameMaxLength(_index2.default.get('SETTINGS'))],
        'email': [validators.email()],
        'password': [validators.passwordMinLength(_index2.default.get('SETTINGS'))],
        'captcha': _captcha2.default.validator()
      },

      'errors': {}
    };
    return _this;
  }

  _createClass(RegisterForm, [{
    key: 'clean',
    value: function clean() {
      if (this.isValid()) {
        return true;
      } else {
        _snackbar2.default.error(gettext("Form contains errors."));
        this.setState({
          'errors': this.validate()
        });
        return false;
      }
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(_index2.default.get('USERS_API'), {
        'username': this.state.username,
        'email': this.state.email,
        'password': this.state.password,
        'captcha': this.state.captcha
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(apiResponse) {
      this.props.callback(apiResponse);
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (rejection.status === 400) {
        this.setState({
          'errors': Object.assign({}, this.state.errors, rejection)
        });
        _snackbar2.default.error(gettext("Form contains errors."));
      } else if (rejection.status === 403 && rejection.ban) {
        (0, _bannedPage2.default)(rejection.ban);
        _modal2.default.hide();
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'getLegalFootNote',
    value: function getLegalFootNote() {
      if (_index2.default.get('TERMS_OF_SERVICE_URL')) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'a',
          { href: _index2.default.get('TERMS_OF_SERVICE_URL'),
            target: '_blank' },
          gettext("By registering you agree to site's terms and conditions.")
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-dialog modal-register', role: 'document' },
        _react2.default.createElement(
          'div',
          { className: 'modal-content' },
          _react2.default.createElement(
            'div',
            { className: 'modal-header' },
            _react2.default.createElement(
              'button',
              { type: 'button', className: 'close', 'data-dismiss': 'modal',
                'aria-label': gettext("Close") },
              _react2.default.createElement(
                'span',
                { 'aria-hidden': 'true' },
                '×'
              )
            ),
            _react2.default.createElement(
              'h4',
              { className: 'modal-title' },
              gettext("Register")
            )
          ),
          _react2.default.createElement(
            'form',
            { onSubmit: this.handleSubmit, className: 'form-horizontal' },
            _react2.default.createElement('input', { type: 'type', style: { display: 'none' } }),
            _react2.default.createElement('input', { type: 'password', style: { display: 'none' } }),
            _react2.default.createElement(
              'div',
              { className: 'modal-body' },
              _react2.default.createElement(
                _formGroup2.default,
                { label: gettext("Username"), 'for': 'id_username',
                  labelClass: 'col-sm-4', controlClass: 'col-sm-8',
                  validation: this.state.errors.username },
                _react2.default.createElement('input', { type: 'text', id: 'id_username', className: 'form-control',
                  'aria-describedby': 'id_username_status',
                  disabled: this.state.isLoading,
                  onChange: this.bindInput('username'),
                  value: this.state.username })
              ),
              _react2.default.createElement(
                _formGroup2.default,
                { label: gettext("E-mail"), 'for': 'id_email',
                  labelClass: 'col-sm-4', controlClass: 'col-sm-8',
                  validation: this.state.errors.email },
                _react2.default.createElement('input', { type: 'text', id: 'id_email', className: 'form-control',
                  'aria-describedby': 'id_email_status',
                  disabled: this.state.isLoading,
                  onChange: this.bindInput('email'),
                  value: this.state.email })
              ),
              _react2.default.createElement(
                _formGroup2.default,
                { label: gettext("Password"), 'for': 'id_password',
                  labelClass: 'col-sm-4', controlClass: 'col-sm-8',
                  validation: this.state.errors.password,
                  extra: _react2.default.createElement(_passwordStrength2.default, { password: this.state.password,
                    inputs: [this.state.username, this.state.email] }) },
                _react2.default.createElement('input', { type: 'password', id: 'id_password', className: 'form-control',
                  'aria-describedby': 'id_password_status',
                  disabled: this.state.isLoading,
                  onChange: this.bindInput('password'),
                  value: this.state.password })
              ),
              _captcha2.default.component({
                form: this,
                labelClass: "col-sm-4",
                controlClass: "col-sm-8"
              })
            ),
            _react2.default.createElement(
              'div',
              { className: 'modal-footer' },
              this.getLegalFootNote(),
              _react2.default.createElement(
                _button2.default,
                { className: 'btn-primary', loading: this.state.isLoading },
                gettext("Register account")
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return RegisterForm;
}(_form2.default);

var RegisterComplete = exports.RegisterComplete = function (_React$Component) {
  _inherits(RegisterComplete, _React$Component);

  function RegisterComplete() {
    _classCallCheck(this, RegisterComplete);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(RegisterComplete).apply(this, arguments));
  }

  _createClass(RegisterComplete, [{
    key: 'getLead',
    value: function getLead() {
      if (this.props.activation === 'user') {
        return gettext("%(username)s, your account has been created but you need to activate it before you will be able to sign in.");
      } else if (this.props.activation === 'admin') {
        return gettext("%(username)s, your account has been created but board administrator will have to activate it before you will be able to sign in.");
      }
    }
  }, {
    key: 'getSubscript',
    value: function getSubscript() {
      if (this.props.activation === 'user') {
        return gettext("We have sent an e-mail to %(email)s with link that you have to click to activate your account.");
      } else if (this.props.activation === 'admin') {
        return gettext("We will send an e-mail to %(email)s when this takes place.");
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-dialog modal-message modal-register',
          role: 'document' },
        _react2.default.createElement(
          'div',
          { className: 'modal-content' },
          _react2.default.createElement(
            'div',
            { className: 'modal-header' },
            _react2.default.createElement(
              'button',
              { type: 'button', className: 'close', 'data-dismiss': 'modal',
                'aria-label': gettext("Close") },
              _react2.default.createElement(
                'span',
                { 'aria-hidden': 'true' },
                '×'
              )
            ),
            _react2.default.createElement(
              'h4',
              { className: 'modal-title' },
              gettext("Registration complete")
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'modal-body' },
            _react2.default.createElement(
              'div',
              { className: 'message-icon' },
              _react2.default.createElement(
                'span',
                { className: 'material-icon' },
                'info_outline'
              )
            ),
            _react2.default.createElement(
              'div',
              { className: 'message-body' },
              _react2.default.createElement(
                'p',
                { className: 'lead' },
                interpolate(this.getLead(), { 'username': this.props.username }, true)
              ),
              _react2.default.createElement(
                'p',
                null,
                interpolate(this.getSubscript(), { 'email': this.props.email }, true)
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return RegisterComplete;
}(_react2.default.Component);

var _class = function (_React$Component2) {
  _inherits(_class, _React$Component2);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this3 = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this3.completeRegistration = function (apiResponse) {
      if (apiResponse.activation === 'active') {
        _modal2.default.hide();
        _auth2.default.signIn(apiResponse);
      } else {
        _this3.setState({
          'complete': apiResponse
        });
      }
    };

    _this3.state = {
      'complete': false
    };
    return _this3;
  }

  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'render',

    /* jshint ignore:end */

    value: function render() {
      /* jshint ignore:start */
      if (this.state.complete) {
        return _react2.default.createElement(RegisterComplete, { activation: this.state.complete.activation,
          username: this.state.complete.username,
          email: this.state.complete.email });
      } else {
        return _react2.default.createElement(RegisterForm, { callback: this.completeRegistration });
      }
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../index":85,"../services/ajax":91,"../services/auth":92,"../services/captcha":93,"../services/modal":97,"../services/snackbar":99,"../utils/banned-page":102,"../utils/validators":109,"./button":51,"./form":58,"./form-group":57,"./password-strength":67,"react":"react"}],70:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.LinkSent = exports.RequestLinkForm = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _button = require('./button');

var _button2 = _interopRequireDefault(_button);

var _form = require('./form');

var _form2 = _interopRequireDefault(_form);

var _ajax = require('../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _snackbar = require('../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _validators = require('../utils/validators');

var validators = _interopRequireWildcard(_validators);

var _bannedPage = require('../utils/banned-page');

var _bannedPage2 = _interopRequireDefault(_bannedPage);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line

var RequestLinkForm = exports.RequestLinkForm = function (_Form) {
  _inherits(RequestLinkForm, _Form);

  function RequestLinkForm(props) {
    _classCallCheck(this, RequestLinkForm);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(RequestLinkForm).call(this, props));

    _this.state = {
      'isLoading': false,

      'email': '',

      'validators': {
        'email': [validators.email()]
      }
    };
    return _this;
  }

  _createClass(RequestLinkForm, [{
    key: 'clean',
    value: function clean() {
      if (this.isValid()) {
        return true;
      } else {
        _snackbar2.default.error(gettext("Enter a valid email address."));
        return false;
      }
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(_index2.default.get('SEND_ACTIVATION_API'), {
        'email': this.state.email
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(apiResponse) {
      this.props.callback(apiResponse);
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (['already_active', 'inactive_admin'].indexOf(rejection.code) > -1) {
        _snackbar2.default.info(rejection.detail);
      } else if (rejection.status === 403 && rejection.ban) {
        (0, _bannedPage2.default)(rejection.ban);
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'well well-form well-form-request-activation-link' },
        _react2.default.createElement(
          'form',
          { onSubmit: this.handleSubmit },
          _react2.default.createElement(
            'div',
            { className: 'form-group' },
            _react2.default.createElement(
              'div',
              { className: 'control-input' },
              _react2.default.createElement('input', { type: 'text', className: 'form-control',
                placeholder: gettext("Your e-mail address"),
                disabled: this.state.isLoading,
                onChange: this.bindInput('email'),
                value: this.state.email })
            )
          ),
          _react2.default.createElement(
            _button2.default,
            { className: 'btn-primary btn-block',
              loading: this.state.isLoading },
            gettext("Send link")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return RequestLinkForm;
}(_form2.default);

var LinkSent = exports.LinkSent = function (_React$Component) {
  _inherits(LinkSent, _React$Component);

  function LinkSent() {
    _classCallCheck(this, LinkSent);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(LinkSent).apply(this, arguments));
  }

  _createClass(LinkSent, [{
    key: 'getMessage',
    value: function getMessage() {
      return interpolate(gettext("Activation link was sent to %(email)s"), {
        email: this.props.user.email
      }, true);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'well well-form well-form-request-activation-link well-done' },
        _react2.default.createElement(
          'div',
          { className: 'done-message' },
          _react2.default.createElement(
            'div',
            { className: 'message-icon' },
            _react2.default.createElement(
              'span',
              { className: 'material-icon' },
              'check'
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'message-body' },
            _react2.default.createElement(
              'p',
              null,
              this.getMessage()
            )
          ),
          _react2.default.createElement(
            'button',
            { type: 'button', className: 'btn btn-primary btn-block',
              onClick: this.props.callback },
            gettext("Request another link")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return LinkSent;
}(_react2.default.Component);

var _class = function (_React$Component2) {
  _inherits(_class, _React$Component2);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this3 = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this3.complete = function (apiResponse) {
      _this3.setState({
        complete: apiResponse
      });
    };

    _this3.reset = function () {
      _this3.setState({
        complete: false
      });
    };

    _this3.state = {
      complete: false
    };
    return _this3;
  }

  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'render',

    /* jshint ignore:end */

    value: function render() {
      /* jshint ignore:start */
      if (this.state.complete) {
        return _react2.default.createElement(LinkSent, { user: this.state.complete, callback: this.reset });
      } else {
        return _react2.default.createElement(RequestLinkForm, { callback: this.complete });
      };
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../index":85,"../services/ajax":91,"../services/snackbar":99,"../utils/banned-page":102,"../utils/validators":109,"./button":51,"./form":58,"react":"react"}],71:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.AccountInactivePage = exports.LinkSent = exports.RequestResetForm = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _button = require('./button');

var _button2 = _interopRequireDefault(_button);

var _form = require('./form');

var _form2 = _interopRequireDefault(_form);

var _ajax = require('../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _snackbar = require('../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _validators = require('../utils/validators');

var validators = _interopRequireWildcard(_validators);

var _bannedPage = require('../utils/banned-page');

var _bannedPage2 = _interopRequireDefault(_bannedPage);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var RequestResetForm = exports.RequestResetForm = function (_Form) {
  _inherits(RequestResetForm, _Form);

  function RequestResetForm(props) {
    _classCallCheck(this, RequestResetForm);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(RequestResetForm).call(this, props));

    _this.state = {
      'isLoading': false,

      'email': '',

      'validators': {
        'email': [validators.email()]
      }
    };
    return _this;
  }

  _createClass(RequestResetForm, [{
    key: 'clean',
    value: function clean() {
      if (this.isValid()) {
        return true;
      } else {
        _snackbar2.default.error(gettext("Enter a valid email address."));
        return false;
      }
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(_index2.default.get('SEND_PASSWORD_RESET_API'), {
        'email': this.state.email
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(apiResponse) {
      this.props.callback(apiResponse);
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (['inactive_user', 'inactive_admin'].indexOf(rejection.code) > -1) {
        this.props.showInactivePage(rejection);
      } else if (rejection.status === 403 && rejection.ban) {
        (0, _bannedPage2.default)(rejection.ban);
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'well well-form well-form-request-password-reset' },
        _react2.default.createElement(
          'form',
          { onSubmit: this.handleSubmit },
          _react2.default.createElement(
            'div',
            { className: 'form-group' },
            _react2.default.createElement(
              'div',
              { className: 'control-input' },
              _react2.default.createElement('input', { type: 'text', className: 'form-control',
                placeholder: gettext("Your e-mail address"),
                disabled: this.state.isLoading,
                onChange: this.bindInput('email'),
                value: this.state.email })
            )
          ),
          _react2.default.createElement(
            _button2.default,
            { className: 'btn-primary btn-block',
              loading: this.state.isLoading },
            gettext("Send link")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return RequestResetForm;
}(_form2.default);

var LinkSent = exports.LinkSent = function (_React$Component) {
  _inherits(LinkSent, _React$Component);

  function LinkSent() {
    _classCallCheck(this, LinkSent);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(LinkSent).apply(this, arguments));
  }

  _createClass(LinkSent, [{
    key: 'getMessage',
    value: function getMessage() {
      return interpolate(gettext("Reset password link was sent to %(email)s"), {
        email: this.props.user.email
      }, true);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'well well-form well-form-request-password-reset well-done' },
        _react2.default.createElement(
          'div',
          { className: 'done-message' },
          _react2.default.createElement(
            'div',
            { className: 'message-icon' },
            _react2.default.createElement(
              'span',
              { className: 'material-icon' },
              'check'
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'message-body' },
            _react2.default.createElement(
              'p',
              null,
              this.getMessage()
            )
          ),
          _react2.default.createElement(
            'button',
            { type: 'button', className: 'btn btn-primary btn-block',
              onClick: this.props.callback },
            gettext("Request another link")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return LinkSent;
}(_react2.default.Component);

var AccountInactivePage = exports.AccountInactivePage = function (_React$Component2) {
  _inherits(AccountInactivePage, _React$Component2);

  function AccountInactivePage() {
    _classCallCheck(this, AccountInactivePage);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(AccountInactivePage).apply(this, arguments));
  }

  _createClass(AccountInactivePage, [{
    key: 'getActivateButton',
    value: function getActivateButton() {
      if (this.props.activation === 'inactive_user') {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'p',
          null,
          _react2.default.createElement(
            'a',
            { href: _index2.default.get('REQUEST_ACTIVATION_URL') },
            gettext("Activate your account.")
          )
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'page page-message page-message-info page-forgotten-password-inactive' },
        _react2.default.createElement(
          'div',
          { className: 'container' },
          _react2.default.createElement(
            'div',
            { className: 'message-panel' },
            _react2.default.createElement(
              'div',
              { className: 'message-icon' },
              _react2.default.createElement(
                'span',
                { className: 'material-icon' },
                'info_outline'
              )
            ),
            _react2.default.createElement(
              'div',
              { className: 'message-body' },
              _react2.default.createElement(
                'p',
                { className: 'lead' },
                gettext("Your account is inactive.")
              ),
              _react2.default.createElement(
                'p',
                null,
                this.props.message
              ),
              this.getActivateButton()
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return AccountInactivePage;
}(_react2.default.Component);

var _class = function (_React$Component3) {
  _inherits(_class, _React$Component3);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this4 = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this4.complete = function (apiResponse) {
      _this4.setState({
        complete: apiResponse
      });
    };

    _this4.reset = function () {
      _this4.setState({
        complete: false
      });
    };

    _this4.state = {
      complete: false
    };
    return _this4;
  }

  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'showInactivePage',
    value: function showInactivePage(apiResponse) {
      _reactDom2.default.render(_react2.default.createElement(AccountInactivePage, { activation: apiResponse.code,
        message: apiResponse.detail }), document.getElementById('page-mount'));
    }
    /* jshint ignore:end */

  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      if (this.state.complete) {
        return _react2.default.createElement(LinkSent, { user: this.state.complete, callback: this.reset });
      } else {
        return _react2.default.createElement(RequestResetForm, { callback: this.complete,
          showInactivePage: this.showInactivePage });
      };
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../index":85,"../services/ajax":91,"../services/snackbar":99,"../utils/banned-page":102,"../utils/validators":109,"./button":51,"./form":58,"react":"react","react-dom":"react-dom"}],72:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.PasswordChangedPage = exports.ResetPasswordForm = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _button = require('./button');

var _button2 = _interopRequireDefault(_button);

var _form = require('./form');

var _form2 = _interopRequireDefault(_form);

var _signIn = require('./sign-in.js');

var _signIn2 = _interopRequireDefault(_signIn);

var _ajax = require('../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _auth = require('../services/auth');

var _auth2 = _interopRequireDefault(_auth);

var _modal = require('../services/modal');

var _modal2 = _interopRequireDefault(_modal);

var _snackbar = require('../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _validators = require('../utils/validators');

var validators = _interopRequireWildcard(_validators);

var _bannedPage = require('../utils/banned-page');

var _bannedPage2 = _interopRequireDefault(_bannedPage);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var ResetPasswordForm = exports.ResetPasswordForm = function (_Form) {
  _inherits(ResetPasswordForm, _Form);

  function ResetPasswordForm(props) {
    _classCallCheck(this, ResetPasswordForm);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(ResetPasswordForm).call(this, props));

    _this.state = {
      'isLoading': false,

      'password': '',

      'validators': {
        'password': [validators.passwordMinLength(_index2.default.get('SETTINGS'))]
      }
    };
    return _this;
  }

  _createClass(ResetPasswordForm, [{
    key: 'clean',
    value: function clean() {
      if (this.isValid()) {
        return true;
      } else {
        if (this.state.password.trim().length) {
          _snackbar2.default.error(this.state.errors.password[0]);
        } else {
          _snackbar2.default.error(gettext("Enter new password."));
        }
        return false;
      }
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(_index2.default.get('CHANGE_PASSWORD_API'), {
        'password': this.state.password
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess(apiResponse) {
      this.props.callback(apiResponse);
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (rejection.status === 403 && rejection.ban) {
        (0, _bannedPage2.default)(rejection.ban);
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'well well-form well-form-reset-password' },
        _react2.default.createElement(
          'form',
          { onSubmit: this.handleSubmit },
          _react2.default.createElement(
            'div',
            { className: 'form-group' },
            _react2.default.createElement(
              'div',
              { className: 'control-input' },
              _react2.default.createElement('input', { type: 'password', className: 'form-control',
                placeholder: gettext("Enter new password"),
                disabled: this.state.isLoading,
                onChange: this.bindInput('password'),
                value: this.state.password })
            )
          ),
          _react2.default.createElement(
            _button2.default,
            { className: 'btn-primary btn-block',
              loading: this.state.isLoading },
            gettext("Change password")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ResetPasswordForm;
}(_form2.default);

var PasswordChangedPage = exports.PasswordChangedPage = function (_React$Component) {
  _inherits(PasswordChangedPage, _React$Component);

  function PasswordChangedPage() {
    _classCallCheck(this, PasswordChangedPage);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(PasswordChangedPage).apply(this, arguments));
  }

  _createClass(PasswordChangedPage, [{
    key: 'getMessage',
    value: function getMessage() {
      return interpolate(gettext("%(username)s, your password has been changed successfully."), {
        username: this.props.user.username
      }, true);
    }
  }, {
    key: 'showSignIn',
    value: function showSignIn() {
      _modal2.default.show(_signIn2.default);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'page page-message page-message-success page-forgotten-password-changed' },
        _react2.default.createElement(
          'div',
          { className: 'container' },
          _react2.default.createElement(
            'div',
            { className: 'message-panel' },
            _react2.default.createElement(
              'div',
              { className: 'message-icon' },
              _react2.default.createElement(
                'span',
                { className: 'material-icon' },
                'check'
              )
            ),
            _react2.default.createElement(
              'div',
              { className: 'message-body' },
              _react2.default.createElement(
                'p',
                { className: 'lead' },
                this.getMessage()
              ),
              _react2.default.createElement(
                'p',
                null,
                gettext("You will have to sign in using new password before continuing.")
              ),
              _react2.default.createElement(
                'p',
                null,
                _react2.default.createElement(
                  'button',
                  { type: 'button', className: 'btn btn-primary', onClick: this.showSignIn },
                  gettext("Sign in")
                )
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return PasswordChangedPage;
}(_react2.default.Component);

var _class = function (_React$Component2) {
  _inherits(_class, _React$Component2);

  function _class() {
    var _Object$getPrototypeO;

    var _temp, _this3, _ret;

    _classCallCheck(this, _class);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this3 = _possibleConstructorReturn(this, (_Object$getPrototypeO = Object.getPrototypeOf(_class)).call.apply(_Object$getPrototypeO, [this].concat(args))), _this3), _this3.complete = function (apiResponse) {
      _auth2.default.softSignOut();

      // nuke "redirect_to" field so we don't end
      // coming back to error page after sign in
      $('#hidden-login-form input[name="redirect_to"]').remove();

      _reactDom2.default.render(_react2.default.createElement(PasswordChangedPage, { user: apiResponse }), document.getElementById('page-mount'));
    }, _temp), _possibleConstructorReturn(_this3, _ret);
  }
  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'render',

    /* jshint ignore:end */

    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(ResetPasswordForm, { callback: this.complete });
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../index":85,"../services/ajax":91,"../services/auth":92,"../services/modal":97,"../services/snackbar":99,"../utils/banned-page":102,"../utils/validators":109,"./button":51,"./form":58,"./sign-in.js":74,"react":"react","react-dom":"react-dom"}],73:[function(require,module,exports){
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    var _Object$getPrototypeO;

    var _temp, _this, _ret;

    _classCallCheck(this, _class);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_Object$getPrototypeO = Object.getPrototypeOf(_class)).call.apply(_Object$getPrototypeO, [this].concat(args))), _this), _this.change = function (value) {
      return function () {
        _this.props.onChange({
          target: {
            value: value
          }
        });
      };
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(_class, [{
    key: "getChoice",
    value: function getChoice() {
      var _this2 = this;

      var choice = null;
      this.props.choices.map(function (item) {
        if (item.value === _this2.props.value) {
          choice = item;
        }
      });
      return choice;
    }
  }, {
    key: "getIcon",
    value: function getIcon() {
      return this.getChoice().icon;
    }
  }, {
    key: "getLabel",
    value: function getLabel() {
      return this.getChoice().label;
    }

    /* jshint ignore:start */

  }, {
    key: "render",

    /* jshint ignore:end */

    value: function render() {
      var _this3 = this;

      /* jshint ignore:start */
      return _react2.default.createElement(
        "div",
        { className: "btn-group btn-select-group" },
        _react2.default.createElement(
          "button",
          { type: "button",
            className: "btn btn-select dropdown-toggle",
            id: this.props.id || null,
            "data-toggle": "dropdown",
            "aria-haspopup": "true",
            "aria-expanded": "false",
            "aria-describedby": this.props['aria-describedby'] || null,
            disabled: this.props.disabled || false },
          _react2.default.createElement(
            "span",
            { className: "material-icon" },
            this.getIcon()
          ),
          this.getLabel()
        ),
        _react2.default.createElement(
          "ul",
          { className: "dropdown-menu" },
          this.props.choices.map(function (item, i) {
            return _react2.default.createElement(
              "li",
              { key: i },
              _react2.default.createElement(
                "button",
                { type: "button", className: "btn-link",
                  onClick: _this3.change(item.value) },
                _react2.default.createElement(
                  "span",
                  { className: "material-icon" },
                  item.icon
                ),
                item.label
              )
            );
          })
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],74:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _button = require('./button');

var _button2 = _interopRequireDefault(_button);

var _form = require('./form');

var _form2 = _interopRequireDefault(_form);

var _ajax = require('../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

var _modal = require('../services/modal');

var _modal2 = _interopRequireDefault(_modal);

var _snackbar = require('../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _bannedPage = require('../utils/banned-page');

var _bannedPage2 = _interopRequireDefault(_bannedPage);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line

var _class = function (_Form) {
  _inherits(_class, _Form);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.state = {
      'isLoading': false,
      'showActivation': false,

      'username': '',
      'password': '',

      'validators': {
        'username': [],
        'password': []
      }
    };
    return _this;
  }

  _createClass(_class, [{
    key: 'clean',
    value: function clean() {
      if (!this.isValid()) {
        _snackbar2.default.error(gettext("Fill out both fields."));
        return false;
      } else {
        return true;
      }
    }
  }, {
    key: 'send',
    value: function send() {
      return _ajax2.default.post(_index2.default.get('AUTH_API'), {
        'username': this.state.username,
        'password': this.state.password
      });
    }
  }, {
    key: 'handleSuccess',
    value: function handleSuccess() {
      var form = $('#hidden-login-form');

      form.append('<input type="text" name="username" />');
      form.append('<input type="password" name="password" />');

      // fill out form with user credentials and submit it, this will tell
      // Misago to redirect user back to right page, and will trigger browser's
      // key ring feature
      form.find('input[type="hidden"]').val(_ajax2.default.getCsrfToken());
      form.find('input[name="redirect_to"]').val(window.location.pathname);
      form.find('input[name="username"]').val(this.state.username);
      form.find('input[name="password"]').val(this.state.password);
      form.submit();

      // keep form loading
      this.setState({
        'isLoading': true
      });
    }
  }, {
    key: 'handleError',
    value: function handleError(rejection) {
      if (rejection.status === 400) {
        if (rejection.code === 'inactive_admin') {
          _snackbar2.default.info(rejection.detail);
        } else if (rejection.code === 'inactive_user') {
          _snackbar2.default.info(rejection.detail);
          this.setState({
            'showActivation': true
          });
        } else if (rejection.code === 'banned') {
          (0, _bannedPage2.default)(rejection.detail);
          _modal2.default.hide();
        } else {
          _snackbar2.default.error(rejection.detail);
        }
      } else if (rejection.status === 403 && rejection.ban) {
        (0, _bannedPage2.default)(rejection.ban);
        _modal2.default.hide();
      } else {
        _snackbar2.default.apiError(rejection);
      }
    }
  }, {
    key: 'getActivationButton',
    value: function getActivationButton() {
      if (this.state.showActivation) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'a',
          { href: _index2.default.get('REQUEST_ACTIVATION_URL'),
            className: 'btn btn-success btn-block' },
          gettext("Activate account")
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'modal-dialog modal-sm modal-sign-in',
          role: 'document' },
        _react2.default.createElement(
          'div',
          { className: 'modal-content' },
          _react2.default.createElement(
            'div',
            { className: 'modal-header' },
            _react2.default.createElement(
              'button',
              { type: 'button', className: 'close', 'data-dismiss': 'modal',
                'aria-label': gettext("Close") },
              _react2.default.createElement(
                'span',
                { 'aria-hidden': 'true' },
                '×'
              )
            ),
            _react2.default.createElement(
              'h4',
              { className: 'modal-title' },
              gettext("Sign in")
            )
          ),
          _react2.default.createElement(
            'form',
            { onSubmit: this.handleSubmit },
            _react2.default.createElement(
              'div',
              { className: 'modal-body' },
              _react2.default.createElement(
                'div',
                { className: 'form-group' },
                _react2.default.createElement(
                  'div',
                  { className: 'control-input' },
                  _react2.default.createElement('input', { id: 'id_username', className: 'form-control', type: 'text',
                    disabled: this.state.isLoading,
                    placeholder: gettext("Username or e-mail"),
                    onChange: this.bindInput('username'),
                    value: this.state.username })
                )
              ),
              _react2.default.createElement(
                'div',
                { className: 'form-group' },
                _react2.default.createElement(
                  'div',
                  { className: 'control-input' },
                  _react2.default.createElement('input', { id: 'id_password', className: 'form-control', type: 'password',
                    disabled: this.state.isLoading,
                    placeholder: gettext("Password"),
                    onChange: this.bindInput('password'),
                    value: this.state.password })
                )
              )
            ),
            _react2.default.createElement(
              'div',
              { className: 'modal-footer' },
              this.getActivationButton(),
              _react2.default.createElement(
                _button2.default,
                { className: 'btn-primary btn-block',
                  loading: this.state.isLoading },
                gettext("Sign in")
              ),
              _react2.default.createElement(
                'a',
                { href: _index2.default.get('FORGOTTEN_PASSWORD_URL'),
                  className: 'btn btn-default btn-block' },
                gettext("Forgot password?")
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_form2.default);

exports.default = _class;

},{"../index":85,"../services/ajax":91,"../services/modal":97,"../services/snackbar":99,"../utils/banned-page":102,"./button":51,"./form":58,"react":"react"}],75:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Snackbar = undefined;
exports.select = select;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

/* jshint ignore:start */
var TYPES_CLASSES = {
  'info': 'alert-info',
  'success': 'alert-success',
  'warning': 'alert-warning',
  'error': 'alert-danger'
};
/* jshint ignore:end */

var Snackbar = exports.Snackbar = function (_React$Component) {
  _inherits(Snackbar, _React$Component);

  function Snackbar() {
    _classCallCheck(this, Snackbar);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(Snackbar).apply(this, arguments));
  }

  _createClass(Snackbar, [{
    key: 'getSnackbarClass',
    value: function getSnackbarClass() {
      var snackbarClass = 'alerts-snackbar';
      if (this.props.isVisible) {
        snackbarClass += ' in';
      } else {
        snackbarClass += ' out';
      }
      return snackbarClass;
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: this.getSnackbarClass() },
        _react2.default.createElement(
          'p',
          { className: 'alert ' + TYPES_CLASSES[this.props.type] },
          this.props.message
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return Snackbar;
}(_react2.default.Component);

function select(state) {
  return state.snackbar;
}

},{"react":"react"}],76:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.CompactGuestNav = exports.GuestNav = exports.GuestMenu = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _avatar = require('../avatar');

var _avatar2 = _interopRequireDefault(_avatar);

var _registerButton = require('../register-button');

var _registerButton2 = _interopRequireDefault(_registerButton);

var _signIn = require('../sign-in.js');

var _signIn2 = _interopRequireDefault(_signIn);

var _mobileNavbarDropdown = require('../../services/mobile-navbar-dropdown');

var _mobileNavbarDropdown2 = _interopRequireDefault(_mobileNavbarDropdown);

var _modal = require('../../services/modal');

var _modal2 = _interopRequireDefault(_modal);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line

var GuestMenu = exports.GuestMenu = function (_React$Component) {
  _inherits(GuestMenu, _React$Component);

  function GuestMenu() {
    _classCallCheck(this, GuestMenu);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(GuestMenu).apply(this, arguments));
  }

  _createClass(GuestMenu, [{
    key: 'showSignInModal',
    value: function showSignInModal() {
      _modal2.default.show(_signIn2.default);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'ul',
        { className: 'dropdown-menu user-dropdown dropdown-menu-right',
          role: 'menu' },
        _react2.default.createElement(
          'li',
          { className: 'guest-preview' },
          _react2.default.createElement(
            'h4',
            null,
            gettext("You are browsing as guest.")
          ),
          _react2.default.createElement(
            'p',
            null,
            gettext('Sign in or register to start and participate in discussions.')
          ),
          _react2.default.createElement(
            'div',
            { className: 'row' },
            _react2.default.createElement(
              'div',
              { className: 'col-xs-6' },
              _react2.default.createElement(
                'button',
                { type: 'button', className: 'btn btn-default btn-block',
                  onClick: this.showSignInModal },
                gettext("Sign in")
              )
            ),
            _react2.default.createElement(
              'div',
              { className: 'col-xs-6' },
              _react2.default.createElement(
                _registerButton2.default,
                { className: 'btn-primary btn-block' },
                gettext("Register")
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return GuestMenu;
}(_react2.default.Component);

var GuestNav = exports.GuestNav = function (_GuestMenu) {
  _inherits(GuestNav, _GuestMenu);

  function GuestNav() {
    _classCallCheck(this, GuestNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(GuestNav).apply(this, arguments));
  }

  _createClass(GuestNav, [{
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'nav nav-guest' },
        _react2.default.createElement(
          'button',
          { type: 'button', className: 'btn navbar-btn btn-default',
            onClick: this.showSignInModal },
          gettext("Sign in")
        ),
        _react2.default.createElement(
          _registerButton2.default,
          { className: 'navbar-btn btn-primary' },
          gettext("Register")
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return GuestNav;
}(GuestMenu);

var CompactGuestNav = exports.CompactGuestNav = function (_React$Component2) {
  _inherits(CompactGuestNav, _React$Component2);

  function CompactGuestNav() {
    _classCallCheck(this, CompactGuestNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(CompactGuestNav).apply(this, arguments));
  }

  _createClass(CompactGuestNav, [{
    key: 'showGuestMenu',
    value: function showGuestMenu() {
      _mobileNavbarDropdown2.default.show(GuestMenu);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'button',
        { type: 'button', onClick: this.showGuestMenu },
        _react2.default.createElement(_avatar2.default, { size: '64' })
      );
      /* jshint ignore:end */
    }
  }]);

  return CompactGuestNav;
}(_react2.default.Component);

},{"../../services/mobile-navbar-dropdown":96,"../../services/modal":97,"../avatar":49,"../register-button":68,"../sign-in.js":74,"react":"react"}],77:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.CompactUserMenu = exports.UserMenu = undefined;
exports.select = select;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _guestNav = require('./guest-nav');

var _userNav = require('./user-nav');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line

// jshint ignore:line

var UserMenu = exports.UserMenu = function (_React$Component) {
  _inherits(UserMenu, _React$Component);

  function UserMenu() {
    _classCallCheck(this, UserMenu);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(UserMenu).apply(this, arguments));
  }

  _createClass(UserMenu, [{
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      if (this.props.isAuthenticated) {
        return _react2.default.createElement(_userNav.UserNav, { user: this.props.user });
      } else {
        return _react2.default.createElement(_guestNav.GuestNav, null);
      }
      /* jshint ignore:end */
    }
  }]);

  return UserMenu;
}(_react2.default.Component);

var CompactUserMenu = exports.CompactUserMenu = function (_React$Component2) {
  _inherits(CompactUserMenu, _React$Component2);

  function CompactUserMenu() {
    _classCallCheck(this, CompactUserMenu);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(CompactUserMenu).apply(this, arguments));
  }

  _createClass(CompactUserMenu, [{
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      if (this.props.isAuthenticated) {
        return _react2.default.createElement(_userNav.CompactUserNav, { user: this.props.user });
      } else {
        return _react2.default.createElement(_guestNav.CompactGuestNav, null);
      }
      /* jshint ignore:end */
    }
  }]);

  return CompactUserMenu;
}(_react2.default.Component);

function select(state) {
  return state.auth;
}

},{"./guest-nav":76,"./user-nav":78,"react":"react"}],78:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.CompactUserNav = exports.UserNav = exports.UserMenu = undefined;
exports.selectUserMenu = selectUserMenu;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRedux = require('react-redux');

var _avatar = require('../avatar');

var _avatar2 = _interopRequireDefault(_avatar);

var _root = require('../change-avatar/root');

var _root2 = _interopRequireDefault(_root);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

var _mobileNavbarDropdown = require('../../services/mobile-navbar-dropdown');

var _mobileNavbarDropdown2 = _interopRequireDefault(_mobileNavbarDropdown);

var _modal = require('../../services/modal');

var _modal2 = _interopRequireDefault(_modal);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var UserMenu = exports.UserMenu = function (_React$Component) {
  _inherits(UserMenu, _React$Component);

  function UserMenu() {
    _classCallCheck(this, UserMenu);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(UserMenu).apply(this, arguments));
  }

  _createClass(UserMenu, [{
    key: 'logout',
    value: function logout() {
      var decision = confirm(gettext("Are you sure you want to sign out?"));
      if (decision) {
        $('#hidden-logout-form').submit();
      }
    }
  }, {
    key: 'changeAvatar',
    value: function changeAvatar() {
      _modal2.default.show((0, _reactRedux.connect)(_root.select)(_root2.default));
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'ul',
        { className: 'dropdown-menu user-dropdown dropdown-menu-right',
          role: 'menu' },
        _react2.default.createElement(
          'li',
          { className: 'dropdown-header' },
          _react2.default.createElement(
            'strong',
            null,
            this.props.user.username
          )
        ),
        _react2.default.createElement('li', { className: 'divider' }),
        _react2.default.createElement(
          'li',
          null,
          _react2.default.createElement(
            'a',
            { href: this.props.user.absolute_url },
            _react2.default.createElement(
              'span',
              { className: 'material-icon' },
              'account_circle'
            ),
            gettext("See your profile")
          )
        ),
        _react2.default.createElement(
          'li',
          null,
          _react2.default.createElement(
            'a',
            { href: _index2.default.get('USERCP_URL') },
            _react2.default.createElement(
              'span',
              { className: 'material-icon' },
              'done_all'
            ),
            gettext("Change options")
          )
        ),
        _react2.default.createElement(
          'li',
          null,
          _react2.default.createElement(
            'button',
            { type: 'button', className: 'btn-link', onClick: this.changeAvatar },
            _react2.default.createElement(
              'span',
              { className: 'material-icon' },
              'portrait'
            ),
            gettext("Change avatar")
          )
        ),
        _react2.default.createElement('li', { className: 'divider' }),
        _react2.default.createElement(
          'li',
          { className: 'dropdown-footer' },
          _react2.default.createElement(
            'button',
            { type: 'button', className: 'btn btn-default btn-block',
              onClick: this.logout },
            gettext("Log out")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return UserMenu;
}(_react2.default.Component);

var UserNav = exports.UserNav = function (_React$Component2) {
  _inherits(UserNav, _React$Component2);

  function UserNav() {
    _classCallCheck(this, UserNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(UserNav).apply(this, arguments));
  }

  _createClass(UserNav, [{
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'ul',
        { className: 'ul nav navbar-nav nav-user' },
        _react2.default.createElement(
          'li',
          { className: 'dropdown' },
          _react2.default.createElement(
            'a',
            { href: this.props.user.absolute_url, className: 'dropdown-toggle',
              'data-toggle': 'dropdown', 'aria-haspopup': 'true', 'aria-expanded': 'false',
              role: 'button' },
            _react2.default.createElement(_avatar2.default, { user: this.props.user, size: '64' })
          ),
          _react2.default.createElement(UserMenu, { user: this.props.user })
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return UserNav;
}(_react2.default.Component);

function selectUserMenu(state) {
  return { user: state.auth.user };
}

var CompactUserNav = exports.CompactUserNav = function (_React$Component3) {
  _inherits(CompactUserNav, _React$Component3);

  function CompactUserNav() {
    _classCallCheck(this, CompactUserNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(CompactUserNav).apply(this, arguments));
  }

  _createClass(CompactUserNav, [{
    key: 'showUserMenu',
    value: function showUserMenu() {
      _mobileNavbarDropdown2.default.showConnected('user-menu', (0, _reactRedux.connect)(selectUserMenu)(UserMenu));
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'button',
        { type: 'button', onClick: this.showUserMenu },
        _react2.default.createElement(_avatar2.default, { user: this.props.user, size: '64' })
      );
      /* jshint ignore:end */
    }
  }]);

  return CompactUserNav;
}(_react2.default.Component);

},{"../../index":85,"../../services/mobile-navbar-dropdown":96,"../../services/modal":97,"../avatar":49,"../change-avatar/root":55,"react":"react","react-redux":"react-redux"}],79:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.StatusLabel = exports.StatusIcon = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'getClass',
    value: function getClass() {
      var status = '';
      if (this.props.status.is_banned) {
        status = 'banned';
      } else if (this.props.status.is_hidden) {
        status = 'offline';
      } else if (this.props.status.is_online_hidden) {
        status = 'online';
      } else if (this.props.status.is_offline_hidden) {
        status = 'offline';
      } else if (this.props.status.is_online) {
        status = 'online';
      } else if (this.props.status.is_offline) {
        status = 'offline';
      }

      return 'user-status user-' + status;
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'span',
        { className: this.getClass() },
        this.props.children
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

var StatusIcon = exports.StatusIcon = function (_React$Component2) {
  _inherits(StatusIcon, _React$Component2);

  function StatusIcon() {
    _classCallCheck(this, StatusIcon);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(StatusIcon).apply(this, arguments));
  }

  _createClass(StatusIcon, [{
    key: 'getIcon',
    value: function getIcon() {
      if (this.props.status.is_banned) {
        return 'remove_circle_outline';
      } else if (this.props.status.is_hidden) {
        return 'help_outline';
      } else if (this.props.status.is_online_hidden) {
        return 'label';
      } else if (this.props.status.is_offline_hidden) {
        return 'label_outline';
      } else if (this.props.status.is_online) {
        return 'lens';
      } else if (this.props.status.is_offline) {
        return 'panorama_fish_eye';
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'span',
        { className: 'status-icon' },
        this.getIcon()
      );
      /* jshint ignore:end */
    }
  }]);

  return StatusIcon;
}(_react2.default.Component);

var StatusLabel = exports.StatusLabel = function (_React$Component3) {
  _inherits(StatusLabel, _React$Component3);

  function StatusLabel() {
    _classCallCheck(this, StatusLabel);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(StatusLabel).apply(this, arguments));
  }

  _createClass(StatusLabel, [{
    key: 'getHelp',
    value: function getHelp() {
      if (this.props.status.is_banned) {
        if (this.props.status.banned_until) {
          return interpolate(gettext("%(username)s is hiding banned until %(ban_expires)s"), {
            username: this.props.user.username,
            ban_expires: this.props.status.banned_until.format('LL, LT')
          }, true);
        } else {
          return interpolate(gettext("%(username)s is hiding banned"), {
            username: this.props.user.username
          }, true);
        }
      } else if (this.props.status.is_hidden) {
        return interpolate(gettext("%(username)s is hiding activity"), {
          username: this.props.user.username
        }, true);
      } else if (this.props.status.is_online_hidden) {
        return interpolate(gettext("%(username)s is online (hidden)"), {
          username: this.props.user.username
        }, true);
      } else if (this.props.status.is_offline_hidden) {
        return interpolate(gettext("%(username)s was last seen %(last_click)s (hidden)"), {
          username: this.props.user.username,
          last_click: this.props.state.lastClick.fromNow()
        }, true);
      } else if (this.props.status.is_online) {
        return interpolate(gettext("%(username)s is online"), {
          username: this.props.user.username
        }, true);
      } else if (this.props.status.is_offline) {
        return interpolate(gettext("%(username)s was last seen %(last_click)s"), {
          username: this.props.user.username,
          last_click: this.props.state.lastClick.fromNow()
        }, true);
      }
    }
  }, {
    key: 'getLabel',
    value: function getLabel() {
      if (this.props.status.is_banned) {
        return gettext("Banned");
      } else if (this.props.status.is_hidden) {
        return gettext("Hiding activity");
      } else if (this.props.status.is_online_hidden) {
        return gettext("Online (hidden)");
      } else if (this.props.status.is_offline_hidden) {
        return gettext("Offline (hidden)");
      } else if (this.props.status.is_online) {
        return gettext("Online");
      } else if (this.props.status.is_offline) {
        return gettext("Offline");
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'span',
        { className: this.props.className || "status-label",
          title: this.getHelp() },
        this.getLabel()
      );
      /* jshint ignore:end */
    }
  }]);

  return StatusLabel;
}(_react2.default.Component);

},{"react":"react"}],80:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.NoActivePosters = exports.ActivePostersLoading = exports.ActivePosters = exports.ActivePoster = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRouter = require('react-router');

var _avatar = require('../avatar');

var _avatar2 = _interopRequireDefault(_avatar);

var _userStatus = require('../user-status');

var _userStatus2 = _interopRequireDefault(_userStatus);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

var _users = require('../../reducers/users');

var _pageTitle = require('../../services/page-title');

var _pageTitle2 = _interopRequireDefault(_pageTitle);

var _store = require('../../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
// jshint ignore:line
// jshint ignore:line

var ActivePoster = exports.ActivePoster = function (_React$Component) {
  _inherits(ActivePoster, _React$Component);

  function ActivePoster() {
    _classCallCheck(this, ActivePoster);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(ActivePoster).apply(this, arguments));
  }

  _createClass(ActivePoster, [{
    key: 'getClassName',
    value: function getClassName() {
      if (this.props.rank.css_class) {
        return "list-group-item list-group-rank-" + this.props.rank.css_class;
      } else {
        return "list-group-item";
      }
    }
  }, {
    key: 'getUserStatus',
    value: function getUserStatus() {
      if (this.props.user.status) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          _userStatus2.default,
          { user: this.props.user, status: this.props.user.status },
          _react2.default.createElement(_userStatus.StatusIcon, { user: this.props.user,
            status: this.props.user.status }),
          _react2.default.createElement(_userStatus.StatusLabel, { user: this.props.user,
            status: this.props.user.status,
            className: 'status-label hidden-xs hidden-sm' })
        );
        /* jshint ignore:end */
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(
            'span',
            { className: 'user-status' },
            _react2.default.createElement(
              'span',
              { className: 'status-icon ui-preview' },
              ' '
            ),
            _react2.default.createElement(
              'span',
              { className: 'status-label ui-preview hidden-xs hidden-sm' },
              ' '
            )
          );
          /* jshint ignore:end */
        }
    }
  }, {
    key: 'getRankName',
    value: function getRankName() {
      if (this.props.rank.is_tab) {
        /* jshint ignore:start */
        var rankUrl = _index2.default.get('USERS_LIST_URL') + this.props.rank.slug + '/';
        return _react2.default.createElement(
          _reactRouter.Link,
          { to: rankUrl, className: 'rank-name' },
          this.props.rank.name
        );
        /* jshint ignore:end */
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(
            'span',
            { className: 'rank-name' },
            this.props.rank.name
          );
          /* jshint ignore:end */
        }
    }
  }, {
    key: 'getUserTitle',
    value: function getUserTitle() {
      if (this.props.user.title) {
        /* jshint ignore:start */
        return _react2.default.createElement(
          'span',
          { className: 'user-title hidden-xs hidden-sm' },
          this.props.user.title
        );
        /* jshint ignore:end */
      } else {
          return null;
        }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'li',
        { className: this.getClassName() },
        _react2.default.createElement(
          'div',
          { className: 'rank-user-avatar' },
          _react2.default.createElement(
            'a',
            { href: this.props.user.absolute_url },
            _react2.default.createElement(_avatar2.default, { user: this.props.user, size: '50' })
          )
        ),
        _react2.default.createElement(
          'div',
          { className: 'rank-user' },
          _react2.default.createElement(
            'div',
            { className: 'user-name' },
            _react2.default.createElement(
              'a',
              { href: this.props.user.absolute_url, className: 'item-title' },
              this.props.user.username
            )
          ),
          this.getUserStatus(),
          this.getRankName(),
          this.getUserTitle()
        ),
        _react2.default.createElement(
          'div',
          { className: 'rank-position' },
          _react2.default.createElement(
            'div',
            { className: 'stat-value' },
            '#',
            this.props.counter
          ),
          _react2.default.createElement(
            'div',
            { className: 'text-muted' },
            gettext("Rank")
          )
        ),
        _react2.default.createElement(
          'div',
          { className: 'rank-posts-counted' },
          _react2.default.createElement(
            'div',
            { className: 'stat-value' },
            this.props.user.meta.score
          ),
          _react2.default.createElement(
            'div',
            { className: 'text-muted' },
            gettext("Ranked posts")
          )
        ),
        _react2.default.createElement(
          'div',
          { className: 'rank-posts-total' },
          _react2.default.createElement(
            'div',
            { className: 'stat-value' },
            this.props.user.posts
          ),
          _react2.default.createElement(
            'div',
            { className: 'text-muted' },
            gettext("Total posts")
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ActivePoster;
}(_react2.default.Component);

var ActivePosters = exports.ActivePosters = function (_React$Component2) {
  _inherits(ActivePosters, _React$Component2);

  function ActivePosters() {
    _classCallCheck(this, ActivePosters);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(ActivePosters).apply(this, arguments));
  }

  _createClass(ActivePosters, [{
    key: 'getLeadMessage',
    value: function getLeadMessage() {
      var message = ngettext("%(posters)s most active poster from last %(days)s days.", "%(posters)s most active posters from last %(days)s days.", this.props.count);

      return interpolate(message, {
        posters: this.props.count,
        days: this.props.trackedPeriod
      }, true);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'active-posters-list' },
        _react2.default.createElement(
          'div',
          { className: 'container' },
          _react2.default.createElement(
            'p',
            { className: 'lead' },
            this.getLeadMessage()
          ),
          _react2.default.createElement(
            'div',
            { className: 'active-posters ui-ready' },
            _react2.default.createElement(
              'ul',
              { className: 'list-group' },
              this.props.users.map(function (user, i) {
                return _react2.default.createElement(ActivePoster, { user: user,
                  rank: user.rank,
                  counter: i + 1,
                  key: user.id });
              })
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ActivePosters;
}(_react2.default.Component);

var ActivePostersLoading = exports.ActivePostersLoading = function (_React$Component3) {
  _inherits(ActivePostersLoading, _React$Component3);

  function ActivePostersLoading() {
    _classCallCheck(this, ActivePostersLoading);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(ActivePostersLoading).apply(this, arguments));
  }

  _createClass(ActivePostersLoading, [{
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'active-posters-list' },
        _react2.default.createElement(
          'div',
          { className: 'container' },
          'This is UI preview!'
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return ActivePostersLoading;
}(_react2.default.Component);

var NoActivePosters = exports.NoActivePosters = function (_React$Component4) {
  _inherits(NoActivePosters, _React$Component4);

  function NoActivePosters() {
    _classCallCheck(this, NoActivePosters);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(NoActivePosters).apply(this, arguments));
  }

  _createClass(NoActivePosters, [{
    key: 'getEmptyMessage',
    value: function getEmptyMessage() {
      return interpolate(gettext("No users have posted any new messages during last %(days)s days."), { 'days': this.props.trackedPeriod }, true);
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'active-posters-list' },
        _react2.default.createElement(
          'div',
          { className: 'container' },
          _react2.default.createElement(
            'p',
            { className: 'lead' },
            this.getEmptyMessage()
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return NoActivePosters;
}(_react2.default.Component);

var _class = function (_React$Component5) {
  _inherits(_class, _React$Component5);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this5 = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    if (_index2.default.has('USERS')) {
      _this5.initWithPreloadedData(_index2.default.pop('USERS'));
    } else {
      _this5.initWithoutPreloadedData();
    }
    return _this5;
  }

  _createClass(_class, [{
    key: 'initWithPreloadedData',
    value: function initWithPreloadedData(data) {
      this.state = {
        isLoaded: true,

        trackedPeriod: data.tracked_period,
        count: data.count
      };

      _store2.default.dispatch((0, _users.dehydrate)(data.results));
    }
  }, {
    key: 'initWithoutPreloadedData',
    value: function initWithoutPreloadedData() {
      this.state = {
        isLoaded: false
      };
    }
  }, {
    key: 'componentDidMount',
    value: function componentDidMount() {
      _pageTitle2.default.set({
        title: this.props.route.extra.name,
        parent: gettext("Users")
      });
    }
  }, {
    key: 'render',
    value: function render() {
      if (this.state.isLoaded) {
        if (this.state.count > 0) {
          /* jshint ignore:start */
          return _react2.default.createElement(ActivePosters, { users: this.props.users,
            trackedPeriod: this.state.trackedPeriod,
            count: this.state.count });
          /* jshint ignore:end */
        } else {
            /* jshint ignore:start */
            return _react2.default.createElement(NoActivePosters, { trackedPeriod: this.state.trackedPeriod });
            /* jshint ignore:end */
          }
      } else {
          /* jshint ignore:start */
          return _react2.default.createElement(ActivePostersLoading, null);
          /* jshint ignore:end */
        }
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../index":85,"../../reducers/users":90,"../../services/page-title":98,"../../services/store":100,"../avatar":49,"../user-status":79,"react":"react","react-router":"react-router"}],81:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.CompactNav = exports.TabsNav = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRouter = require('react-router');

var _li = require('../li');

var _li2 = _interopRequireDefault(_li);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line
//jshint ignore:line

//jshint ignore:line

// jshint ignore:start
var listUrl = function listUrl(baseUrl, list) {
  var url = baseUrl;
  if (list.component === 'rank') {
    url += list.slug;
  } else {
    url += list.component;
  }
  return url + '/';
};

var navLinks = function navLinks(baseUrl, lists) {
  return lists.map(function (list) {
    var url = listUrl(baseUrl, list);
    return _react2.default.createElement(
      _li2.default,
      { path: url,
        key: url },
      _react2.default.createElement(
        _reactRouter.Link,
        { to: url },
        list.name
      )
    );
  });
};
// jshint ignore:end

var TabsNav = exports.TabsNav = function (_React$Component) {
  _inherits(TabsNav, _React$Component);

  function TabsNav() {
    _classCallCheck(this, TabsNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(TabsNav).apply(this, arguments));
  }

  _createClass(TabsNav, [{
    key: 'render',
    value: function render() {
      // jshint ignore:start
      return _react2.default.createElement(
        'ul',
        { className: 'nav nav-pills' },
        navLinks(this.props.baseUrl, this.props.lists)
      );
      // jshint ignore:end
    }
  }]);

  return TabsNav;
}(_react2.default.Component);

var CompactNav = exports.CompactNav = function (_React$Component2) {
  _inherits(CompactNav, _React$Component2);

  function CompactNav() {
    _classCallCheck(this, CompactNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(CompactNav).apply(this, arguments));
  }

  _createClass(CompactNav, [{
    key: 'render',
    value: function render() {
      // jshint ignore:start
      return _react2.default.createElement(
        'ul',
        { className: 'dropdown-menu', role: 'menu' },
        navLinks(this.props.baseUrl, this.props.lists)
      );
      // jshint ignore:end
    }
  }]);

  return CompactNav;
}(_react2.default.Component);

},{"../../index":85,"../li":59,"react":"react","react-router":"react-router"}],82:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _pageTitle = require('../../services/page-title');

var _pageTitle2 = _interopRequireDefault(_pageTitle);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    _classCallCheck(this, _class);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(_class).apply(this, arguments));
  }

  _createClass(_class, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      _pageTitle2.default.set({
        title: this.props.route.rank.name,
        parent: gettext("Users")
      });
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        null,
        _react2.default.createElement(
          'div',
          { className: 'container' },
          'Hello, this is users with rank list!'
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"../../services/page-title":98,"react":"react"}],83:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.select = select;
exports.paths = paths;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRedux = require('react-redux');

var _navs = require('./navs');

var _activePosters = require('./active-posters');

var _activePosters2 = _interopRequireDefault(_activePosters);

var _rank = require('./rank');

var _rank2 = _interopRequireDefault(_rank);

var _index = require('../../index');

var _index2 = _interopRequireDefault(_index);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.toggleNav = function () {
      if (_this.state.dropdown) {
        _this.setState({
          dropdown: false
        });
      } else {
        _this.setState({
          dropdown: true
        });
      }
    };

    _this.state = {
      dropdown: false
    };
    return _this;
  }

  /* jshint ignore:start */

  _createClass(_class, [{
    key: 'getToggleNavClassName',

    /* jshint ignore:end */

    value: function getToggleNavClassName() {
      if (this.state.dropdown) {
        return 'btn btn-default btn-icon open';
      } else {
        return 'btn btn-default btn-icon';
      }
    }
  }, {
    key: 'getCompactNavClassName',
    value: function getCompactNavClassName() {
      if (this.state.dropdown) {
        return 'compact-nav open';
      } else {
        return 'compact-nav';
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'page page-users-lists' },
        _react2.default.createElement(
          'div',
          { className: 'page-header tabbed' },
          _react2.default.createElement(
            'div',
            { className: 'container' },
            _react2.default.createElement(
              'h1',
              null,
              gettext("Users")
            ),
            _react2.default.createElement(
              'button',
              { className: 'btn btn-default btn-icon btn-dropdown-toggle hidden-md hidden-lg',
                type: 'button',
                onClick: this.toggleNav,
                'aria-haspopup': 'true',
                'aria-expanded': this.state.dropdown ? 'true' : 'false' },
              _react2.default.createElement(
                'i',
                { className: 'material-icon' },
                'menu'
              )
            )
          ),
          _react2.default.createElement(
            'div',
            { className: 'page-tabs hidden-xs hidden-sm' },
            _react2.default.createElement(
              'div',
              { className: 'container' },
              _react2.default.createElement(_navs.TabsNav, { lists: _index2.default.get('USERS_LISTS'),
                baseUrl: _index2.default.get('USERS_LIST_URL') })
            )
          )
        ),
        _react2.default.createElement(
          'div',
          { className: this.getCompactNavClassName() },
          _react2.default.createElement(_navs.CompactNav, { lists: _index2.default.get('USERS_LISTS'),
            baseUrl: _index2.default.get('USERS_LIST_URL') })
        ),
        this.props.children
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;
function select(store) {
  return {
    'tick': store.tick.tick,
    'user': store.auth.user,
    'users': store.users
  };
}

function paths() {
  var paths = [];

  _index2.default.get('USERS_LISTS').forEach(function (item) {
    if (item.component === 'rank') {
      paths.push({
        path: _index2.default.get('USERS_LIST_URL') + item.slug + '/',
        component: (0, _reactRedux.connect)(select)(_rank2.default),
        rank: {
          name: item.name,
          slug: item.slug,
          css_class: item.css_class,
          description: item.description
        }
      });
    } else if (item.component === 'active-posters') {
      paths.push({
        path: _index2.default.get('USERS_LIST_URL') + item.component + '/',
        component: (0, _reactRedux.connect)(select)(_activePosters2.default),
        extra: {
          name: item.name
        }
      });
    }
  });

  return paths;
}

},{"../../index":85,"./active-posters":80,"./navs":81,"./rank":82,"react":"react","react-redux":"react-redux"}],84:[function(require,module,exports){
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = function (_React$Component) {
  _inherits(_class, _React$Component);

  function _class() {
    var _Object$getPrototypeO;

    var _temp, _this, _ret;

    _classCallCheck(this, _class);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_Object$getPrototypeO = Object.getPrototypeOf(_class)).call.apply(_Object$getPrototypeO, [this].concat(args))), _this), _this.toggle = function () {
      _this.props.onChange({
        target: {
          value: !_this.props.value
        }
      });
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(_class, [{
    key: "getClassName",
    value: function getClassName() {
      if (this.props.value) {
        return "btn btn-yes-no btn-yes-no-on";
      } else {
        return "btn btn-yes-no btn-yes-no-off";
      }
    }
  }, {
    key: "getIcon",
    value: function getIcon() {
      if (this.props.value) {
        return this.props.iconOn || 'check_box';
      } else {
        return this.props.iconOff || 'check_box_outline_blank';
      }
    }
  }, {
    key: "getLabel",
    value: function getLabel() {
      if (this.props.value) {
        return this.props.labelOn || gettext("yes");
      } else {
        return this.props.labelOff || gettext("no");
      }
    }

    /* jshint ignore:start */

  }, {
    key: "render",

    /* jshint ignore:end */

    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        "button",
        { type: "button",
          onClick: this.toggle,
          className: this.getClassName(),
          id: this.props.id || null,
          "aria-describedby": this.props['aria-describedby'] || null,
          disabled: this.props.disabled || false },
        _react2.default.createElement(
          "span",
          { className: "material-icon" },
          this.getIcon()
        ),
        this.getLabel()
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],85:[function(require,module,exports){
(function (global){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Misago = undefined;

var _orderedList = require('./utils/ordered-list');

var _orderedList2 = _interopRequireDefault(_orderedList);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Misago = exports.Misago = function () {
  function Misago() {
    _classCallCheck(this, Misago);

    this._initializers = [];
    this._context = {};
  }

  _createClass(Misago, [{
    key: 'addInitializer',
    value: function addInitializer(initializer) {
      this._initializers.push({
        key: initializer.name,

        item: initializer.initializer,

        after: initializer.after,
        before: initializer.before
      });
    }
  }, {
    key: 'init',
    value: function init(context) {
      var _this = this;

      this._context = context;

      var initOrder = new _orderedList2.default(this._initializers).orderedValues();
      initOrder.forEach(function (initializer) {
        initializer(_this);
      });
    }

    // context accessors

  }, {
    key: 'has',
    value: function has(key) {
      return !!this._context[key];
    }
  }, {
    key: 'get',
    value: function get(key, fallback) {
      if (this.has(key)) {
        return this._context[key];
      } else {
        return fallback || undefined;
      }
    }
  }, {
    key: 'pop',
    value: function pop(key) {
      if (this.has(key)) {
        var value = this._context[key];
        this._context[key] = null;
        return value;
      } else {
        return undefined;
      }
    }
  }]);

  return Misago;
}();

// create  singleton

var misago = new Misago();

// expose it globally
global.misago = misago;

// and export it for tests and stuff
exports.default = misago;

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{"./utils/ordered-list":106}],86:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.SIGN_OUT = exports.SIGN_IN = exports.PATCH_USER = exports.initialState = undefined;
exports.patchUser = patchUser;
exports.signIn = signIn;
exports.signOut = signOut;
exports.default = auth;

var _users = require('./users');

var initialState = exports.initialState = {
  signedIn: false,
  signedOut: false
};

var PATCH_USER = exports.PATCH_USER = 'PATCH_USER';
var SIGN_IN = exports.SIGN_IN = 'SIGN_IN';
var SIGN_OUT = exports.SIGN_OUT = 'SIGN_OUT';

function patchUser(patch) {
  return {
    type: PATCH_USER,
    patch: patch
  };
}

function signIn(user) {
  return {
    type: SIGN_IN,
    user: user
  };
}

function signOut() {
  var soft = arguments.length <= 0 || arguments[0] === undefined ? false : arguments[0];

  return {
    type: SIGN_OUT,
    soft: soft
  };
}

function auth() {
  var state = arguments.length <= 0 || arguments[0] === undefined ? initialState : arguments[0];
  var action = arguments.length <= 1 || arguments[1] === undefined ? null : arguments[1];

  switch (action.type) {
    case PATCH_USER:
      var newState = Object.assign({}, state);
      newState.user = Object.assign({}, state.user, action.patch);
      return newState;

    case SIGN_IN:
      return Object.assign({}, state, {
        signedIn: action.user
      });

    case SIGN_OUT:
      return Object.assign({}, state, {
        isAuthenticated: false,
        isAnonymous: true,
        signedOut: !action.soft
      });

    case _users.UPDATE_AVATAR:
      if (state.isAuthenticated && state.user.id === action.userId) {
        var _newState = Object.assign({}, state);
        _newState.user = Object.assign({}, state.user, {
          'avatar_hash': action.avatarHash
        });
        return _newState;
      }
      return state;

    case _users.UPDATE_USERNAME:
      if (state.isAuthenticated && state.user.id === action.userId) {
        var _newState2 = Object.assign({}, state);
        _newState2.user = Object.assign({}, state.user, {
          username: action.username,
          slug: action.slug
        });
        return _newState2;
      }
      return state;

    default:
      return state;
  }
}

},{"./users":90}],87:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.showSnackbar = showSnackbar;
exports.hideSnackbar = hideSnackbar;
exports.default = snackbar;
var initialState = exports.initialState = {
  type: 'info',
  message: '',
  isVisible: false
};

var SHOW_SNACKBAR = exports.SHOW_SNACKBAR = 'SHOW_SNACKBAR';
var HIDE_SNACKBAR = exports.HIDE_SNACKBAR = 'HIDE_SNACKBAR';

function showSnackbar(message, type) {
  return {
    type: SHOW_SNACKBAR,
    message: message,
    messageType: type
  };
}

function hideSnackbar() {
  return {
    type: HIDE_SNACKBAR
  };
}

function snackbar() {
  var state = arguments.length <= 0 || arguments[0] === undefined ? initialState : arguments[0];
  var action = arguments.length <= 1 || arguments[1] === undefined ? null : arguments[1];

  if (action.type === SHOW_SNACKBAR) {
    return {
      type: action.messageType,
      message: action.message,
      isVisible: true
    };
  } else if (action.type === HIDE_SNACKBAR) {
    return Object.assign({}, state, {
      isVisible: false
    });
  } else {
    return state;
  }
}

},{}],88:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.doTick = doTick;
exports.default = tick;
var initialState = exports.initialState = {
  tick: 0
};

var TICK = exports.TICK = 'TICK';

function doTick() {
  return {
    type: TICK
  };
}

function tick() {
  var state = arguments.length <= 0 || arguments[0] === undefined ? initialState : arguments[0];
  var action = arguments.length <= 1 || arguments[1] === undefined ? null : arguments[1];

  if (action.type === TICK) {
    return Object.assign({}, state, {
      tick: state.tick + 1
    });
  } else {
    return state;
  }
}

},{}],89:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.DEHYDRATE_RESULT = exports.ADD_NAME_CHANGE = undefined;
exports.addNameChange = addNameChange;
exports.dehydrate = dehydrate;
exports.default = username;

var _users = require('./users');

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var ADD_NAME_CHANGE = exports.ADD_NAME_CHANGE = 'ADD_NAME_CHANGE';
var DEHYDRATE_RESULT = exports.DEHYDRATE_RESULT = 'DEHYDRATE_RESULT';

function addNameChange(change, user, changedBy) {
  return {
    type: ADD_NAME_CHANGE,
    change: change,
    user: user,
    changedBy: changedBy
  };
}

function dehydrate(items) {
  return {
    type: DEHYDRATE_RESULT,
    items: items
  };
}

function username() {
  var state = arguments.length <= 0 || arguments[0] === undefined ? [] : arguments[0];
  var action = arguments.length <= 1 || arguments[1] === undefined ? null : arguments[1];

  switch (action.type) {
    case ADD_NAME_CHANGE:
      var newState = state.slice();
      newState.unshift({
        id: Math.floor(Date.now() / 1000), // just small hax for getting id
        changed_by: action.changedBy,
        changed_by_username: action.changedBy.username,
        changed_on: (0, _moment2.default)(),
        new_username: action.change.username,
        old_username: action.user.username
      });
      return newState;

    case DEHYDRATE_RESULT:
      return action.items.map(function (item) {
        return Object.assign({}, item, {
          changed_on: (0, _moment2.default)(item.changed_on)
        });
      });

    case _users.UPDATE_AVATAR:
      return state.map(function (item) {
        item = Object.assign({}, item);
        if (item.changed_by && item.changed_by.id === action.userId) {
          item.changed_by = Object.assign({}, item.changed_by, {
            'avatar_hash': action.avatarHash
          });
        }

        return Object.assign({}, item);
      });

    case _users.UPDATE_USERNAME:
      return state.map(function (item) {
        item = Object.assign({}, item);
        if (item.changed_by && item.changed_by.id === action.userId) {
          item.changed_by = Object.assign({}, item.changed_by, {
            'username': action.username,
            'slug': action.slug
          });
        }

        return Object.assign({}, item);
      });

    default:
      return state;
  }
}

},{"./users":90,"moment":"moment"}],90:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.dehydrate = dehydrate;
exports.updateAvatar = updateAvatar;
exports.updateUsername = updateUsername;
exports.default = user;
var DEHYDRATE_RESULT = exports.DEHYDRATE_RESULT = 'DEHYDRATE_RESULT';
var UPDATE_AVATAR = exports.UPDATE_AVATAR = 'UPDATE_AVATAR';
var UPDATE_USERNAME = exports.UPDATE_USERNAME = 'UPDATE_USERNAME';

function dehydrate(items) {
  return {
    type: DEHYDRATE_RESULT,
    items: items
  };
}

function updateAvatar(user, avatarHash) {
  return {
    type: UPDATE_AVATAR,
    userId: user.id,
    avatarHash: avatarHash
  };
}

function updateUsername(user, username, slug) {
  return {
    type: UPDATE_USERNAME,
    userId: user.id,
    username: username,
    slug: slug
  };
}

function user() {
  var state = arguments.length <= 0 || arguments[0] === undefined ? [] : arguments[0];
  var action = arguments.length <= 1 || arguments[1] === undefined ? null : arguments[1];

  switch (action.type) {
    case DEHYDRATE_RESULT:
      return action.items.map(function (item) {
        return Object.assign({}, item, {});
      });

    default:
      return state;
  }
}

},{}],91:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Ajax = exports.Ajax = function () {
  function Ajax() {
    _classCallCheck(this, Ajax);

    this._cookieName = null;
    this._csrfToken = null;
  }

  _createClass(Ajax, [{
    key: 'init',
    value: function init(cookieName) {
      this._cookieName = cookieName;
      this._csrfToken = this.getCsrfToken();
    }
  }, {
    key: 'getCsrfToken',
    value: function getCsrfToken() {
      if (document.cookie.indexOf(this._cookieName) !== -1) {
        var cookieRegex = new RegExp(this._cookieName + '\=([^;]*)');
        var cookie = document.cookie.match(cookieRegex)[0];
        return cookie ? cookie.split('=')[1] : null;
      } else {
        return null;
      }
    }
  }, {
    key: 'request',
    value: function request(method, url, data) {
      var self = this;
      return new Promise(function (resolve, reject) {
        var xhr = {
          url: url,
          method: method,
          headers: {
            'X-CSRFToken': self._csrfToken
          },

          data: data ? JSON.stringify(data) : null,
          contentType: "application/json; charset=utf-8",
          dataType: 'json',

          success: function success(data) {
            resolve(data);
          },

          error: function error(jqXHR) {
            var rejection = jqXHR.responseJSON || {};

            rejection.status = jqXHR.status;

            if (rejection.status === 0) {
              rejection.detail = gettext("Lost connection with application.");
            }

            rejection.statusText = jqXHR.statusText;

            reject(rejection);
          }
        };

        $.ajax(xhr);
      });
    }
  }, {
    key: 'get',
    value: function get(url, params) {
      if (params) {
        url += '?' + $.param(params);
      }
      return this.request('GET', url);
    }
  }, {
    key: 'post',
    value: function post(url, data) {
      return this.request('POST', url, data);
    }
  }, {
    key: 'patch',
    value: function patch(url, data) {
      return this.request('PATCH', url, data);
    }
  }, {
    key: 'put',
    value: function put(url, data) {
      return this.request('PUT', url, data);
    }
  }, {
    key: 'delete',
    value: function _delete(url) {
      return this.request('DELETE', url);
    }
  }, {
    key: 'upload',
    value: function upload(url, data, progress) {
      var self = this;
      return new Promise(function (resolve, reject) {
        var xhr = {
          url: url,
          method: 'POST',
          headers: {
            'X-CSRFToken': self._csrfToken
          },

          data: data,
          contentType: false,
          processData: false,

          xhr: function xhr() {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function (evt) {
              if (evt.lengthComputable) {
                progress(Math.round(evt.loaded / evt.total * 100));
              }
            }, false);
            return xhr;
          },

          success: function success(response) {
            resolve(response);
          },

          error: function error(jqXHR) {
            var rejection = jqXHR.responseJSON || {};

            rejection.status = jqXHR.status;

            if (rejection.status === 0) {
              rejection.detail = gettext("Lost connection with application.");
            }

            rejection.statusText = jqXHR.statusText;

            reject(rejection);
          }
        };

        $.ajax(xhr);
      });
    }
  }]);

  return Ajax;
}();

exports.default = new Ajax();

},{}],92:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Auth = undefined;

var _auth = require('../reducers/auth');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

// jshint ignore:line

var Auth = exports.Auth = function () {
  function Auth() {
    _classCallCheck(this, Auth);
  }

  _createClass(Auth, [{
    key: 'init',
    value: function init(store, local, modal) {
      this._store = store;
      this._local = local;
      this._modal = modal;

      // tell other tabs what auth state is because we are most current with it
      this.syncSession();

      // listen for other tabs to tell us that state changed
      this.watchState();
    }
  }, {
    key: 'syncSession',
    value: function syncSession() {
      var state = this._store.getState().auth;
      if (state.isAuthenticated) {
        this._local.set('auth', {
          isAuthenticated: true,
          username: state.user.username
        });
      } else {
        this._local.set('auth', {
          isAuthenticated: false
        });
      }
    }
  }, {
    key: 'watchState',
    value: function watchState() {
      var _this = this;

      this._local.watch('auth', function (newState) {
        if (newState.isAuthenticated) {
          _this._store.dispatch((0, _auth.signIn)({
            username: newState.username
          }));
        } else {
          _this._store.dispatch((0, _auth.signOut)());
        }
      });
      this._modal.hide();
    }
  }, {
    key: 'signIn',
    value: function signIn(user) {
      this._store.dispatch((0, _auth.signIn)(user));
      this._local.set('auth', {
        isAuthenticated: true,
        username: user.username
      });
      this._modal.hide();
    }
  }, {
    key: 'signOut',
    value: function signOut() {
      this._store.dispatch((0, _auth.signOut)());
      this._local.set('auth', {
        isAuthenticated: false
      });
      this._modal.hide();
    }
  }, {
    key: 'softSignOut',
    value: function softSignOut() {
      this._store.dispatch((0, _auth.signOut)(true));
      this._local.set('auth', {
        isAuthenticated: false
      });
      this._modal.hide();
    }
  }]);

  return Auth;
}();

exports.default = new Auth();

},{"../reducers/auth":86}],93:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }(); /* global grecaptcha */
// jshint ignore:line

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Captcha = exports.ReCaptcha = exports.ReCaptchaComponent = exports.QACaptcha = exports.NoCaptcha = exports.BaseCaptcha = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _formGroup = require('../components/form-group');

var _formGroup2 = _interopRequireDefault(_formGroup);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

// jshint ignore:line

var BaseCaptcha = exports.BaseCaptcha = function () {
  function BaseCaptcha() {
    _classCallCheck(this, BaseCaptcha);
  }

  _createClass(BaseCaptcha, [{
    key: 'init',
    value: function init(context, ajax, include, snackbar) {
      this._context = context;
      this._ajax = ajax;
      this._include = include;
      this._snackbar = snackbar;
    }
  }]);

  return BaseCaptcha;
}();

var NoCaptcha = exports.NoCaptcha = function (_BaseCaptcha) {
  _inherits(NoCaptcha, _BaseCaptcha);

  function NoCaptcha() {
    _classCallCheck(this, NoCaptcha);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(NoCaptcha).apply(this, arguments));
  }

  _createClass(NoCaptcha, [{
    key: 'load',
    value: function load() {
      return new Promise(function (resolve) {
        // immediately resolve as we don't have anything to validate
        resolve();
      });
    }
  }, {
    key: 'validator',
    value: function validator() {
      return null;
    }
  }, {
    key: 'component',
    value: function component() {
      return null;
    }
  }]);

  return NoCaptcha;
}(BaseCaptcha);

var QACaptcha = exports.QACaptcha = function (_BaseCaptcha2) {
  _inherits(QACaptcha, _BaseCaptcha2);

  function QACaptcha() {
    _classCallCheck(this, QACaptcha);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(QACaptcha).apply(this, arguments));
  }

  _createClass(QACaptcha, [{
    key: 'load',
    value: function load() {
      var self = this;
      return new Promise(function (resolve, reject) {
        self._ajax.get(self._context.get('CAPTCHA_API_URL')).then(function (data) {
          self.question = data.question;
          self.helpText = data.help_text;
          resolve();
        }, function () {
          self._snackbar.error(gettext("Failed to load CAPTCHA."));
          reject();
        });
      });
    }
  }, {
    key: 'validator',
    value: function validator() {
      return [];
    }

    /* jshint ignore:start */

  }, {
    key: 'component',
    value: function component(kwargs) {
      return _react2.default.createElement(
        _formGroup2.default,
        { label: this.question, 'for': 'id_captcha',
          labelClass: kwargs.labelClass || "col-sm-4",
          controlClass: kwargs.controlClass || "col-sm-8",
          validation: kwargs.form.state.errors.captcha,
          helpText: this.helpText || null },
        _react2.default.createElement('input', { type: 'text', id: 'id_captcha', className: 'form-control',
          'aria-describedby': 'id_captcha_status',
          disabled: kwargs.form.state.isLoading,
          onChange: kwargs.form.bindInput('captcha'),
          value: kwargs.form.state.captcha })
      );
    }
    /* jshint ignore:end */

  }]);

  return QACaptcha;
}(BaseCaptcha);

var ReCaptchaComponent = exports.ReCaptchaComponent = function (_React$Component) {
  _inherits(ReCaptchaComponent, _React$Component);

  function ReCaptchaComponent() {
    _classCallCheck(this, ReCaptchaComponent);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(ReCaptchaComponent).apply(this, arguments));
  }

  _createClass(ReCaptchaComponent, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this4 = this;

      grecaptcha.render('recaptcha', {
        'sitekey': this.props.siteKey,
        'callback': function callback(response) {
          // fire fakey event to binding
          _this4.props.binding({
            target: {
              value: response
            }
          });
        }
      });
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement('div', { id: 'recaptcha' });
      /* jshint ignore:end */
    }
  }]);

  return ReCaptchaComponent;
}(_react2.default.Component);

var ReCaptcha = exports.ReCaptcha = function (_BaseCaptcha3) {
  _inherits(ReCaptcha, _BaseCaptcha3);

  function ReCaptcha() {
    _classCallCheck(this, ReCaptcha);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(ReCaptcha).apply(this, arguments));
  }

  _createClass(ReCaptcha, [{
    key: 'load',
    value: function load() {
      this._include.include('https://www.google.com/recaptcha/api.js', true);

      return new Promise(function (resolve) {
        var wait = function wait() {
          if (typeof grecaptcha === "undefined") {
            window.setTimeout(function () {
              wait();
            }, 200);
          } else {
            resolve();
          }
        };
        wait();
      });
    }
  }, {
    key: 'validator',
    value: function validator() {
      return [];
    }

    /* jshint ignore:start */

  }, {
    key: 'component',
    value: function component(kwargs) {
      return _react2.default.createElement(
        _formGroup2.default,
        { label: gettext("Captcha"), 'for': 'id_captcha',
          labelClass: kwargs.labelClass || "col-sm-4",
          controlClass: kwargs.controlClass || "col-sm-8",
          validation: kwargs.form.state.errors.captcha,
          helpText: gettext("Please solve the quick test.") },
        _react2.default.createElement(ReCaptchaComponent, { siteKey: this._context.get('SETTINGS').recaptcha_site_key,
          binding: kwargs.form.bindInput('captcha') })
      );
    }
    /* jshint ignore:end */

  }]);

  return ReCaptcha;
}(BaseCaptcha);

var Captcha = exports.Captcha = function () {
  function Captcha() {
    _classCallCheck(this, Captcha);
  }

  _createClass(Captcha, [{
    key: 'init',
    value: function init(context, ajax, include, snackbar) {
      switch (context.get('SETTINGS').captcha_type) {
        case 'no':
          this._captcha = new NoCaptcha();
          break;

        case 'qa':
          this._captcha = new QACaptcha();
          break;

        case 're':
          this._captcha = new ReCaptcha();
          break;
      }

      this._captcha.init(context, ajax, include, snackbar);
    }

    // accessors for underlying strategy

  }, {
    key: 'load',
    value: function load() {
      return this._captcha.load();
    }
  }, {
    key: 'validator',
    value: function validator() {
      return this._captcha.validator();
    }
  }, {
    key: 'component',
    value: function component(kwargs) {
      return this._captcha.component(kwargs);
    }
  }]);

  return Captcha;
}();

exports.default = new Captcha();

},{"../components/form-group":57,"react":"react"}],94:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Include = exports.Include = function () {
  function Include() {
    _classCallCheck(this, Include);
  }

  _createClass(Include, [{
    key: 'init',
    value: function init(staticUrl) {
      this._staticUrl = staticUrl;
      this._included = [];
    }
  }, {
    key: 'include',
    value: function include(script) {
      var remote = arguments.length <= 1 || arguments[1] === undefined ? false : arguments[1];

      if (this._included.indexOf(script) === -1) {
        this._included.push(script);
        this._include(script, remote);
      }
    }
  }, {
    key: '_include',
    value: function _include(script, remote) {
      $.ajax({
        url: (!remote ? this._staticUrl : '') + script,
        cache: true,
        dataType: 'script'
      });
    }
  }]);

  return Include;
}();

exports.default = new Include();

},{}],95:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var storage = window.localStorage;

var LocalStorage = exports.LocalStorage = function () {
  function LocalStorage() {
    _classCallCheck(this, LocalStorage);
  }

  _createClass(LocalStorage, [{
    key: 'init',
    value: function init(prefix) {
      var _this = this;

      this._prefix = prefix;
      this._watchers = [];

      window.addEventListener('storage', function (e) {
        var newValueJson = JSON.parse(e.newValue);
        _this._watchers.forEach(function (watcher) {
          if (watcher.key === e.key && e.oldValue !== e.newValue) {
            watcher.callback(newValueJson);
          }
        });
      });
    }
  }, {
    key: 'set',
    value: function set(key, value) {
      storage.setItem(this._prefix + key, JSON.stringify(value));
    }
  }, {
    key: 'get',
    value: function get(key) {
      var itemString = storage.getItem(this._prefix + key);
      if (itemString) {
        return JSON.parse(itemString);
      } else {
        return null;
      }
    }
  }, {
    key: 'watch',
    value: function watch(key, callback) {
      this._watchers.push({
        key: this._prefix + key,
        callback: callback
      });
    }
  }]);

  return LocalStorage;
}();

exports.default = new LocalStorage();

},{}],96:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.MobileNavbarDropdown = undefined;

var _mountComponent = require('../utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var MobileNavbarDropdown = exports.MobileNavbarDropdown = function () {
  function MobileNavbarDropdown() {
    _classCallCheck(this, MobileNavbarDropdown);
  }

  _createClass(MobileNavbarDropdown, [{
    key: 'init',
    value: function init(element) {
      this._element = element;
      this._component = null;
    }
  }, {
    key: 'show',
    value: function show(component) {
      if (this._component === component) {
        this.hide();
      } else {
        this._component = component;
        (0, _mountComponent2.default)(component, this._element.id);
        $(this._element).addClass('open');
      }
    }
  }, {
    key: 'showConnected',
    value: function showConnected(name, component) {
      if (this._component === name) {
        this.hide();
      } else {
        this._component = name;
        (0, _mountComponent2.default)(component, this._element.id, true);
        $(this._element).addClass('open');
      }
    }
  }, {
    key: 'hide',
    value: function hide() {
      $(this._element).removeClass('open');
      this._component = null;
    }
  }]);

  return MobileNavbarDropdown;
}();

exports.default = new MobileNavbarDropdown();

},{"../utils/mount-component":105}],97:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Modal = undefined;

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _mountComponent = require('../utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Modal = exports.Modal = function () {
  function Modal() {
    _classCallCheck(this, Modal);
  }

  _createClass(Modal, [{
    key: 'init',
    value: function init(element) {
      var _this = this;

      this._element = element;

      this._modal = $(element).modal({ show: false });

      this._modal.on('hidden.bs.modal', function () {
        _reactDom2.default.unmountComponentAtNode(_this._element);
      });
    }
  }, {
    key: 'show',
    value: function show(component) {
      (0, _mountComponent2.default)(component, this._element.id);
      this._modal.modal('show');
    }
  }, {
    key: 'hide',
    value: function hide() {
      this._modal.modal('hide');
    }
  }]);

  return Modal;
}();

exports.default = new Modal();

},{"../utils/mount-component":105,"react-dom":"react-dom"}],98:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var PageTitle = exports.PageTitle = function () {
  function PageTitle() {
    _classCallCheck(this, PageTitle);
  }

  _createClass(PageTitle, [{
    key: 'init',
    value: function init(forumName) {
      this._forumName = forumName;
    }
  }, {
    key: 'set',
    value: function set(title) {
      if (typeof title === 'string') {
        title = { title: title };
      }

      var finalTitle = title.title;

      if (title.page) {
        var pageLabel = interpolate(gettext('page %(page)s'), {
          page: title.page
        }, true);

        finalTitle += ' (' + pageLabel + ')';
      }

      if (title.parent) {
        finalTitle += ' | ' + title.parent;
      }

      document.title = finalTitle + ' | ' + this._forumName;
    }
  }]);

  return PageTitle;
}();

exports.default = new PageTitle();

},{}],99:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Snackbar = undefined;

var _snackbar = require('../reducers/snackbar');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var HIDE_ANIMATION_LENGTH = 300;
var MESSAGE_SHOW_LENGTH = 5000;

var Snackbar = exports.Snackbar = function () {
  function Snackbar() {
    _classCallCheck(this, Snackbar);
  }

  _createClass(Snackbar, [{
    key: 'init',
    value: function init(store) {
      this._store = store;
      this._timeout = null;
    }
  }, {
    key: 'alert',
    value: function alert(message, type) {
      var _this = this;

      if (this._timeout) {
        window.clearTimeout(this._timeout);
        this._store.dispatch((0, _snackbar.hideSnackbar)());

        this._timeout = window.setTimeout(function () {
          _this._timeout = null;
          _this.alert(message, type);
        }, HIDE_ANIMATION_LENGTH);
      } else {
        this._store.dispatch((0, _snackbar.showSnackbar)(message, type));
        this._timeout = window.setTimeout(function () {
          _this._store.dispatch((0, _snackbar.hideSnackbar)());
          _this._timeout = null;
        }, MESSAGE_SHOW_LENGTH);
      }
    }

    // shorthands for message types

  }, {
    key: 'info',
    value: function info(message) {
      this.alert(message, 'info');
    }
  }, {
    key: 'success',
    value: function success(message) {
      this.alert(message, 'success');
    }
  }, {
    key: 'warning',
    value: function warning(message) {
      this.alert(message, 'warning');
    }
  }, {
    key: 'error',
    value: function error(message) {
      this.alert(message, 'error');
    }

    // shorthand for api errors

  }, {
    key: 'apiError',
    value: function apiError(rejection) {
      var message = gettext("Unknown error has occured.");

      if (rejection.status === 0) {
        message = rejection.detail;
      }

      if (rejection.status === 400 && rejection.detail) {
        message = rejection.detail;
      }

      if (rejection.status === 403) {
        message = rejection.detail;
        if (message === "Permission denied") {
          message = gettext("You don't have permission to perform this action.");
        }
      }

      if (rejection.status === 404) {
        message = gettext("Action link is invalid.");
      }

      this.error(message);
    }
  }]);

  return Snackbar;
}();

exports.default = new Snackbar();

},{"../reducers/snackbar":87}],100:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.StoreWrapper = undefined;

var _redux = require('redux');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var StoreWrapper = exports.StoreWrapper = function () {
  function StoreWrapper() {
    _classCallCheck(this, StoreWrapper);

    this._store = null;
    this._reducers = {};
    this._initialState = {};
  }

  _createClass(StoreWrapper, [{
    key: 'addReducer',
    value: function addReducer(name, reducer, initialState) {
      this._reducers[name] = reducer;
      this._initialState[name] = initialState;
    }
  }, {
    key: 'init',
    value: function init() {
      this._store = (0, _redux.createStore)((0, _redux.combineReducers)(this._reducers), this._initialState);
    }
  }, {
    key: 'getStore',
    value: function getStore() {
      return this._store;
    }

    // Store API

  }, {
    key: 'getState',
    value: function getState() {
      return this._store.getState();
    }
  }, {
    key: 'dispatch',
    value: function dispatch(action) {
      return this._store.dispatch(action);
    }
  }]);

  return StoreWrapper;
}();

exports.default = new StoreWrapper();

},{"redux":"redux"}],101:[function(require,module,exports){
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/* global zxcvbn */

var Zxcvbn = exports.Zxcvbn = function () {
  function Zxcvbn() {
    _classCallCheck(this, Zxcvbn);
  }

  _createClass(Zxcvbn, [{
    key: "init",
    value: function init(include) {
      this._include = include;
    }
  }, {
    key: "scorePassword",
    value: function scorePassword(password, inputs) {
      // 0-4 score, the more the stronger password
      return zxcvbn(password, inputs).score;
    }
  }, {
    key: "load",
    value: function load() {
      if (typeof zxcvbn === "undefined") {
        this._include.include('misago/js/zxcvbn.js');
        return this._loadingPromise();
      } else {
        return this._loadedPromise();
      }
    }
  }, {
    key: "_loadingPromise",
    value: function _loadingPromise() {
      return new Promise(function (resolve) {
        var wait = function wait() {
          if (typeof zxcvbn === "undefined") {
            window.setTimeout(function () {
              wait();
            }, 200);
          } else {
            resolve();
          }
        };
        wait();
      });
    }
  }, {
    key: "_loadedPromise",
    value: function _loadedPromise() {
      // we have already loaded zxcvbn.js, resolve away!
      return new Promise(function (resolve) {
        resolve();
      });
    }
  }]);

  return Zxcvbn;
}();

exports.default = new Zxcvbn();

},{}],102:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

exports.default = function (ban, changeState) {
  _reactDom2.default.render(
  /* jshint ignore:start */
  _react2.default.createElement(
    _reactRedux.Provider,
    { store: _store2.default.getStore() },
    _react2.default.createElement(RedrawedBannedPage, { message: ban.message,
      expires: ban.expires_on ? (0, _moment2.default)(ban.expires_on) : null })
  ),
  /* jshint ignore:end */
  document.getElementById('page-mount'));

  if (typeof changeState === 'undefined' || changeState) {
    var forumName = _index2.default.get('SETTINGS').forum_name;
    document.title = gettext("You are banned") + ' | ' + forumName;
    window.history.pushState({}, "", _index2.default.get('BANNED_URL'));
  }
};

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _reactRedux = require('react-redux');

var _bannedPage = require('../components/banned-page');

var _bannedPage2 = _interopRequireDefault(_bannedPage);

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _store = require('../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// jshint ignore:line

/* jshint ignore:start */
// jshint ignore:line
// jshint ignore:line
var select = function select(state) {
  return state.tick;
}; // jshint ignore:line
// jshint ignore:line

var RedrawedBannedPage = (0, _reactRedux.connect)(select)(_bannedPage2.default);
/* jshint ignore:end */

},{"../components/banned-page":50,"../index":85,"../services/store":100,"moment":"moment","react":"react","react-dom":"react-dom","react-redux":"react-redux"}],103:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});

exports.default = function (list, rowWidth) {
  var padding = arguments.length <= 2 || arguments[2] === undefined ? false : arguments[2];

  var rows = [];
  var row = [];

  list.forEach(function (element) {
    row.push(element);
    if (row.length === rowWidth) {
      rows.push(row);
      row = [];
    }
  });

  // pad row to required length?
  if (padding !== false && row.length > 0 && row.length < rowWidth) {
    for (var i = row.length; i < rowWidth; i++) {
      row.push(padding);
    }
  }

  if (row.length) {
    rows.push(row);
  }

  return rows;
};

},{}],104:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

exports.default = function (bytes) {
  if (bytes > 1000 * 1000 * 1000) {
    return Math.round(bytes * 100 / (1000 * 1000 * 1000)) / 100 + ' GB';
  } else if (bytes > 1000 * 1000) {
    return Math.round(bytes * 100 / (1000 * 1000)) / 100 + ' MB';
  } else if (bytes > 1000) {
    return Math.round(bytes * 100 / 1000) / 100 + ' KB';
  } else {
    return Math.round(bytes * 100) / 100 + ' B';
  }
};

},{}],105:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

exports.default = function (Component, rootElementId) {
  var connected = arguments.length <= 2 || arguments[2] === undefined ? true : arguments[2];

  var rootElement = document.getElementById(rootElementId);

  if (rootElement) {
    if (connected) {
      _reactDom2.default.render(
      /* jshint ignore:start */
      _react2.default.createElement(
        _reactRedux.Provider,
        { store: _store2.default.getStore() },
        _react2.default.createElement(Component, null)
      ),
      /* jshint ignore:end */
      rootElement);
    } else {
      _reactDom2.default.render(
      /* jshint ignore:start */
      _react2.default.createElement(Component, null),
      /* jshint ignore:end */
      rootElement);
    }
  }
};

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _reactRedux = require('react-redux');

var _store = require('../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

},{"../services/store":100,"react":"react","react-dom":"react-dom","react-redux":"react-redux"}],106:[function(require,module,exports){
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var OrderedList = function () {
  function OrderedList(items) {
    _classCallCheck(this, OrderedList);

    this.isOrdered = false;
    this._items = items || [];
  }

  _createClass(OrderedList, [{
    key: "add",
    value: function add(key, item, order) {
      this._items.push({
        key: key,
        item: item,

        after: order ? order.after || null : null,
        before: order ? order.before || null : null
      });
    }
  }, {
    key: "get",
    value: function get(key, value) {
      for (var i = 0; i < this._items.length; i++) {
        if (this._items[i].key === key) {
          return this._items[i].item;
        }
      }

      return value;
    }
  }, {
    key: "has",
    value: function has(key) {
      return this.get(key) !== undefined;
    }
  }, {
    key: "values",
    value: function values() {
      var values = [];
      for (var i = 0; i < this._items.length; i++) {
        values.push(this._items[i].item);
      }
      return values;
    }
  }, {
    key: "order",
    value: function order(values_only) {
      if (!this.isOrdered) {
        this._items = this._order(this._items);
        this.isOrdered = true;
      }

      if (values_only || typeof values_only === 'undefined') {
        return this.values();
      } else {
        return this._items;
      }
    }
  }, {
    key: "orderedValues",
    value: function orderedValues() {
      return this.order(true);
    }
  }, {
    key: "_order",
    value: function _order(unordered) {
      // Index of unordered items
      var index = [];
      unordered.forEach(function (item) {
        index.push(item.key);
      });

      // Ordered items
      var ordered = [];
      var ordering = [];

      // First pass: register items that
      // don't specify their order
      unordered.forEach(function (item) {
        if (!item.after && !item.before) {
          ordered.push(item);
          ordering.push(item.key);
        }
      });

      // Second pass: register items that
      // specify their before to "_end"
      unordered.forEach(function (item) {
        if (item.before === "_end") {
          ordered.push(item);
          ordering.push(item.key);
        }
      });

      // Third pass: keep iterating items
      // until we hit iterations limit or finish
      // ordering list
      function insertItem(item) {
        var insertAt = -1;
        if (ordering.indexOf(item.key) === -1) {
          if (item.after) {
            insertAt = ordering.indexOf(item.after);
            if (insertAt !== -1) {
              insertAt += 1;
            }
          } else if (item.before) {
            insertAt = ordering.indexOf(item.before);
          }

          if (insertAt !== -1) {
            ordered.splice(insertAt, 0, item);
            ordering.splice(insertAt, 0, item.key);
          }
        }
      }

      var iterations = 200;
      while (iterations > 0 && index.length !== ordering.length) {
        iterations -= 1;
        unordered.forEach(insertItem);
      }

      return ordered;
    }
  }]);

  return OrderedList;
}();

exports.default = OrderedList;

},{}],107:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.int = int;
exports.range = range;
function int(min, max) {
  return Math.floor(Math.random() * (max + 1)) + min;
}

function range(min, max) {
  var array = new Array(int(min, max));
  for (var i = 0; i < array.length; i++) {
    array[i] = i;
  }

  return array;
}

},{}],108:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

exports.default = function (options) {
  var routes = {
    component: options.component,
    childRoutes: [{
      path: options.root,
      onEnter: function onEnter(nextState, replaceState) {
        replaceState(null, options.paths[0].path);
      }
    }].concat(options.paths.map(function (path) {
      return path;
    }))
  };

  _reactDom2.default.render(_react2.default.createElement(
    _reactRedux.Provider,
    { store: _store2.default.getStore() },
    _react2.default.createElement(_reactRouter.Router, { routes: routes, history: history })
  ), rootElement);
};

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _reactRedux = require('react-redux');

var _reactRouter = require('react-router');

var _createBrowserHistory = require('history/lib/createBrowserHistory');

var _createBrowserHistory2 = _interopRequireDefault(_createBrowserHistory);

var _store = require('../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// jshint ignore:start

var rootElement = document.getElementById('page-mount');
var history = new _createBrowserHistory2.default();

},{"../services/store":100,"history/lib/createBrowserHistory":38,"react":"react","react-dom":"react-dom","react-redux":"react-redux","react-router":"react-router"}],109:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.required = required;
exports.email = email;
exports.minLength = minLength;
exports.maxLength = maxLength;
exports.usernameMinLength = usernameMinLength;
exports.usernameMaxLength = usernameMaxLength;
exports.usernameContent = usernameContent;
exports.passwordMinLength = passwordMinLength;
var EMAIL = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
var USERNAME = new RegExp('^[0-9a-z]+$', 'i');

function required() {
  return function (value) {
    if ($.trim(value).length === 0) {
      return gettext("This field is required.");
    }
  };
}

function email(message) {
  return function (value) {
    if (!EMAIL.test(value)) {
      return message || gettext("Enter a valid email address.");
    }
  };
}

function minLength(limitValue, message) {
  return function (value) {
    var returnMessage = '';
    var length = $.trim(value).length;

    if (length < limitValue) {
      if (message) {
        returnMessage = message(limitValue, length);
      } else {
        returnMessage = ngettext("Ensure this value has at least %(limit_value)s character (it has %(show_value)s).", "Ensure this value has at least %(limit_value)s characters (it has %(show_value)s).", limitValue);
      }
      return interpolate(returnMessage, {
        limit_value: limitValue,
        show_value: length
      }, true);
    }
  };
}

function maxLength(limitValue, message) {
  return function (value) {
    var returnMessage = '';
    var length = $.trim(value).length;

    if (length > limitValue) {
      if (message) {
        returnMessage = message(limitValue, length);
      } else {
        returnMessage = ngettext("Ensure this value has at most %(limit_value)s character (it has %(show_value)s).", "Ensure this value has at most %(limit_value)s characters (it has %(show_value)s).", limitValue);
      }
      return interpolate(returnMessage, {
        limit_value: limitValue,
        show_value: length
      }, true);
    }
  };
}

function usernameMinLength(settings) {
  var message = function message(limitValue) {
    return ngettext("Username must be at least %(limit_value)s character long.", "Username must be at least %(limit_value)s characters long.", limitValue);
  };
  return this.minLength(settings.username_length_min, message);
}

function usernameMaxLength(settings) {
  var message = function message(limitValue) {
    return ngettext("Username cannot be longer than %(limit_value)s character.", "Username cannot be longer than %(limit_value)s characters.", limitValue);
  };
  return this.maxLength(settings.username_length_max, message);
}

function usernameContent() {
  return function (value) {
    if (!USERNAME.test($.trim(value))) {
      return gettext("Username can only contain latin alphabet letters and digits.");
    }
  };
}

function passwordMinLength(settings) {
  var message = function message(limitValue) {
    return ngettext("Valid password must be at least %(limit_value)s character long.", "Valid password must be at least %(limit_value)s characters long.", limitValue);
  };
  return this.minLength(settings.password_length_min, message);
}

},{}]},{},[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJub2RlX21vZHVsZXMvcHJvY2Vzcy9icm93c2VyLmpzIiwic3JjL2luZGV4LmpzIiwic3JjL2luaXRpYWxpemVycy9hamF4LmpzIiwic3JjL2luaXRpYWxpemVycy9hdXRoLW1lc3NhZ2UtY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy9hdXRoLXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2F1dGguanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2Jhbm5lZC1wYWdlLWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvY2F0Y2hhLmpzIiwic3JjL2luaXRpYWxpemVycy9pbmNsdWRlLmpzIiwic3JjL2luaXRpYWxpemVycy9sb2NhbC1zdG9yYWdlLmpzIiwic3JjL2luaXRpYWxpemVycy9tb2JpbGUtbmF2YmFyLWRyb3Bkb3duLmpzIiwic3JjL2luaXRpYWxpemVycy9tb2RhbC5qcyIsInNyYy9pbml0aWFsaXplcnMvbW9tZW50LWxvY2FsZS5qcyIsInNyYy9pbml0aWFsaXplcnMvb3B0aW9ucy1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3BhZ2UtdGl0bGUuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rLWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvcmVxdWVzdC1wYXNzd29yZC1yZXNldC1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3Jlc2V0LXBhc3N3b3JkLWZvcm0tY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy9zbmFja2Jhci1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3NuYWNrYmFyLXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3NuYWNrYmFyLmpzIiwic3JjL2luaXRpYWxpemVycy9zdG9yZS5qcyIsInNyYy9pbml0aWFsaXplcnMvdGljay1yZWR1Y2VyLmpzIiwic3JjL2luaXRpYWxpemVycy90aWNrLXN0YXJ0LmpzIiwic3JjL2luaXRpYWxpemVycy91c2VyLW1lbnUtY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy91c2VybmFtZS1oaXN0b3J5LXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3VzZXJzLWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvdXNlcnMtcmVkdWNlci5qcyIsInNyYy9pbml0aWFsaXplcnMvenhjdmJuLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvZGVlcC1lcXVhbC9pbmRleC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2RlZXAtZXF1YWwvbGliL2lzX2FyZ3VtZW50cy5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2RlZXAtZXF1YWwvbGliL2tleXMuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9BY3Rpb25zLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaGlzdG9yeS9saWIvQXN5bmNVdGlscy5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL0RPTVN0YXRlU3RvcmFnZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL0RPTVV0aWxzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaGlzdG9yeS9saWIvRXhlY3V0aW9uRW52aXJvbm1lbnQuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9jcmVhdGVCcm93c2VySGlzdG9yeS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL2NyZWF0ZURPTUhpc3RvcnkuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9jcmVhdGVIaXN0b3J5LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaGlzdG9yeS9saWIvY3JlYXRlTG9jYXRpb24uanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9kZXByZWNhdGUuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9leHRyYWN0UGF0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL3BhcnNlUGF0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL3J1blRyYW5zaXRpb25Ib29rLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaW52YXJpYW50L2Jyb3dzZXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy93YXJuaW5nL2Jyb3dzZXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2F1dGgtbWVzc2FnZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvYXZhdGFyLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9iYW5uZWQtcGFnZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvYnV0dG9uLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL2Nyb3AuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2NoYW5nZS1hdmF0YXIvZ2FsbGVyeS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9pbmRleC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9yb290LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL3VwbG9hZC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvZm9ybS1ncm91cC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvZm9ybS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvbGkuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2xvYWRlci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvbW9kYWwtbG9hZGVyLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9vcHRpb25zL2NoYW5nZS11c2VybmFtZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvb3B0aW9ucy9mb3J1bS1vcHRpb25zLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9vcHRpb25zL25hdnMuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL29wdGlvbnMvcm9vdC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvb3B0aW9ucy9zaWduLWluLWNyZWRlbnRpYWxzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9wYXNzd29yZC1zdHJlbmd0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvcmVnaXN0ZXItYnV0dG9uLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9yZWdpc3Rlci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvcmVxdWVzdC1hY3RpdmF0aW9uLWxpbmsuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3JlcXVlc3QtcGFzc3dvcmQtcmVzZXQuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3Jlc2V0LXBhc3N3b3JkLWZvcm0uanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3NlbGVjdC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvc2lnbi1pbi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvc25hY2tiYXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3VzZXItbWVudS9ndWVzdC1uYXYuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3VzZXItbWVudS9yb290LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy91c2VyLW1lbnUvdXNlci1uYXYuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3VzZXItc3RhdHVzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy91c2Vycy9hY3RpdmUtcG9zdGVycy5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvdXNlcnMvbmF2cy5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvdXNlcnMvcmFuay5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvdXNlcnMvcm9vdC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMveWVzLW5vLXN3aXRjaC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2luZGV4LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvcmVkdWNlcnMvYXV0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3JlZHVjZXJzL3NuYWNrYmFyLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvcmVkdWNlcnMvdGljay5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3JlZHVjZXJzL3VzZXJuYW1lLWhpc3RvcnkuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9yZWR1Y2Vycy91c2Vycy5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL2FqYXguanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9hdXRoLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvY2FwdGNoYS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL2luY2x1ZGUuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9sb2NhbC1zdG9yYWdlLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvbW9iaWxlLW5hdmJhci1kcm9wZG93bi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL21vZGFsLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvcGFnZS10aXRsZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL3NuYWNrYmFyLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvc3RvcmUuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy96eGN2Ym4uanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9iYW5uZWQtcGFnZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3V0aWxzL2JhdGNoLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvZmlsZS1zaXplLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvbW91bnQtY29tcG9uZW50LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvb3JkZXJlZC1saXN0LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvcmFuZG9tLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvcm91dGVkLWNvbXBvbmVudC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3V0aWxzL3ZhbGlkYXRvcnMuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7QUNBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7OztJQ3pGYSxNQUFNLFdBQU4sTUFBTTtBQUNqQixXQURXLE1BQU0sR0FDSDswQkFESCxNQUFNOztB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QTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDOUZBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNwQkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDVEE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDOUJBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7OztBQ3pCQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7O0FDbkVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDL0VBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7OztBQ0pBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7OztBQ2pMQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7OztBQ3ZDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDbFNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNyREE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ2RBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7QUNaQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7OztBQzNDQTtBQUNBO0FBQ0E7QUFDQTtBQUNB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VixPQUFPLENBQVksVUFBVSxFQUFFO0FBQ2pDLFdBQU8sUUFBUSxDQUNiLGlFQUFpRSxFQUNqRSxrRUFBa0UsRUFDbEUsVUFBVSxDQUFDLENBQUM7R0FDZixDQUFDO0FBQ0YsU0FBTyxJQUFJLENBQUMsU0FBUyxDQUFDLFFBQVEsQ0FBQyxtQkFBbUIsRUFBRSxPQUFPLENBQUMsQ0FBQztDQUM5RCIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIGUodCxuLHIpe2Z1bmN0aW9uIHMobyx1KXtpZighbltvXSl7aWYoIXRbb10pe3ZhciBhPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7aWYoIXUmJmEpcmV0dXJuIGEobywhMCk7aWYoaSlyZXR1cm4gaShvLCEwKTt2YXIgZj1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK28rXCInXCIpO3Rocm93IGYuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixmfXZhciBsPW5bb109e2V4cG9ydHM6e319O3Rbb11bMF0uY2FsbChsLmV4cG9ydHMsZnVuY3Rpb24oZSl7dmFyIG49dFtvXVsxXVtlXTtyZXR1cm4gcyhuP246ZSl9LGwsbC5leHBvcnRzLGUsdCxuLHIpfXJldHVybiBuW29dLmV4cG9ydHN9dmFyIGk9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtmb3IodmFyIG89MDtvPHIubGVuZ3RoO28rKylzKHJbb10pO3JldHVybiBzfSkiLCIvLyBzaGltIGZvciB1c2luZyBwcm9jZXNzIGluIGJyb3dzZXJcblxudmFyIHByb2Nlc3MgPSBtb2R1bGUuZXhwb3J0cyA9IHt9O1xudmFyIHF1ZXVlID0gW107XG52YXIgZHJhaW5pbmcgPSBmYWxzZTtcbnZhciBjdXJyZW50UXVldWU7XG52YXIgcXVldWVJbmRleCA9IC0xO1xuXG5mdW5jdGlvbiBjbGVhblVwTmV4dFRpY2soKSB7XG4gICAgZHJhaW5pbmcgPSBmYWxzZTtcbiAgICBpZiAoY3VycmVudFF1ZXVlLmxlbmd0aCkge1xuICAgICAgICBxdWV1ZSA9IGN1cnJlbnRRdWV1ZS5jb25jYXQocXVldWUpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIHF1ZXVlSW5kZXggPSAtMTtcbiAgICB9XG4gICAgaWYgKHF1ZXVlLmxlbmd0aCkge1xuICAgICAgICBkcmFpblF1ZXVlKCk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBkcmFpblF1ZXVlKCkge1xuICAgIGlmIChkcmFpbmluZykge1xuICAgICAgICByZXR1cm47XG4gICAgfVxuICAgIHZhciB0aW1lb3V0ID0gc2V0VGltZW91dChjbGVhblVwTmV4dFRpY2spO1xuICAgIGRyYWluaW5nID0gdHJ1ZTtcblxuICAgIHZhciBsZW4gPSBxdWV1ZS5sZW5ndGg7XG4gICAgd2hpbGUobGVuKSB7XG4gICAgICAgIGN1cnJlbnRRdWV1ZSA9IHF1ZXVlO1xuICAgICAgICBxdWV1ZSA9IFtdO1xuICAgICAgICB3aGlsZSAoKytxdWV1ZUluZGV4IDwgbGVuKSB7XG4gICAgICAgICAgICBpZiAoY3VycmVudFF1ZXVlKSB7XG4gICAgICAgICAgICAgICAgY3VycmVudFF1ZXVlW3F1ZXVlSW5kZXhdLnJ1bigpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHF1ZXVlSW5kZXggPSAtMTtcbiAgICAgICAgbGVuID0gcXVldWUubGVuZ3RoO1xuICAgIH1cbiAgICBjdXJyZW50UXVldWUgPSBudWxsO1xuICAgIGRyYWluaW5nID0gZmFsc2U7XG4gICAgY2xlYXJUaW1lb3V0KHRpbWVvdXQpO1xufVxuXG5wcm9jZXNzLm5leHRUaWNrID0gZnVuY3Rpb24gKGZ1bikge1xuICAgIHZhciBhcmdzID0gbmV3IEFycmF5KGFyZ3VtZW50cy5sZW5ndGggLSAxKTtcbiAgICBpZiAoYXJndW1lbnRzLmxlbmd0aCA+IDEpIHtcbiAgICAgICAgZm9yICh2YXIgaSA9IDE7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGFyZ3NbaSAtIDFdID0gYXJndW1lbnRzW2ldO1xuICAgICAgICB9XG4gICAgfVxuICAgIHF1ZXVlLnB1c2gobmV3IEl0ZW0oZnVuLCBhcmdzKSk7XG4gICAgaWYgKHF1ZXVlLmxlbmd0aCA9PT0gMSAmJiAhZHJhaW5pbmcpIHtcbiAgICAgICAgc2V0VGltZW91dChkcmFpblF1ZXVlLCAwKTtcbiAgICB9XG59O1xuXG4vLyB2OCBsaWtlcyBwcmVkaWN0aWJsZSBvYmplY3RzXG5mdW5jdGlvbiBJdGVtKGZ1biwgYXJyYXkpIHtcbiAgICB0aGlzLmZ1biA9IGZ1bjtcbiAgICB0aGlzLmFycmF5ID0gYXJyYXk7XG59XG5JdGVtLnByb3RvdHlwZS5ydW4gPSBmdW5jdGlvbiAoKSB7XG4gICAgdGhpcy5mdW4uYXBwbHkobnVsbCwgdGhpcy5hcnJheSk7XG59O1xucHJvY2Vzcy50aXRsZSA9ICdicm93c2VyJztcbnByb2Nlc3MuYnJvd3NlciA9IHRydWU7XG5wcm9jZXNzLmVudiA9IHt9O1xucHJvY2Vzcy5hcmd2ID0gW107XG5wcm9jZXNzLnZlcnNpb24gPSAnJzsgLy8gZW1wdHkgc3RyaW5nIHRvIGF2b2lkIHJlZ2V4cCBpc3N1ZXNcbnByb2Nlc3MudmVyc2lvbnMgPSB7fTtcblxuZnVuY3Rpb24gbm9vcCgpIHt9XG5cbnByb2Nlc3Mub24gPSBub29wO1xucHJvY2Vzcy5hZGRMaXN0ZW5lciA9IG5vb3A7XG5wcm9jZXNzLm9uY2UgPSBub29wO1xucHJvY2Vzcy5vZmYgPSBub29wO1xucHJvY2Vzcy5yZW1vdmVMaXN0ZW5lciA9IG5vb3A7XG5wcm9jZXNzLnJlbW92ZUFsbExpc3RlbmVycyA9IG5vb3A7XG5wcm9jZXNzLmVtaXQgPSBub29wO1xuXG5wcm9jZXNzLmJpbmRpbmcgPSBmdW5jdGlvbiAobmFtZSkge1xuICAgIHRocm93IG5ldyBFcnJvcigncHJvY2Vzcy5iaW5kaW5nIGlzIG5vdCBzdXBwb3J0ZWQnKTtcbn07XG5cbnByb2Nlc3MuY3dkID0gZnVuY3Rpb24gKCkgeyByZXR1cm4gJy8nIH07XG5wcm9jZXNzLmNoZGlyID0gZnVuY3Rpb24gKGRpcikge1xuICAgIHRocm93IG5ldyBFcnJvcigncHJvY2Vzcy5jaGRpciBpcyBub3Qgc3VwcG9ydGVkJyk7XG59O1xucHJvY2Vzcy51bWFzayA9IGZ1bmN0aW9uKCkgeyByZXR1cm4gMDsgfTtcbiIsImltcG9ydCBPcmRlcmVkTGlzdCBmcm9tICdtaXNhZ28vdXRpbHMvb3JkZXJlZC1saXN0JztcblxuZXhwb3J0IGNsYXNzIE1pc2FnbyB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2luaXRpYWxpemVycyA9IFtdO1xuICAgIHRoaXMuX2NvbnRleHQgPSB7fTtcbiAgfVxuXG4gIGFkZEluaXRpYWxpemVyKGluaXRpYWxpemVyKSB7XG4gICAgdGhpcy5faW5pdGlhbGl6ZXJzLnB1c2goe1xuICAgICAga2V5OiBpbml0aWFsaXplci5uYW1lLFxuXG4gICAgICBpdGVtOiBpbml0aWFsaXplci5pbml0aWFsaXplcixcblxuICAgICAgYWZ0ZXI6IGluaXRpYWxpemVyLmFmdGVyLFxuICAgICAgYmVmb3JlOiBpbml0aWFsaXplci5iZWZvcmVcbiAgICB9KTtcbiAgfVxuXG4gIGluaXQoY29udGV4dCkge1xuICAgIHRoaXMuX2NvbnRleHQgPSBjb250ZXh0O1xuXG4gICAgdmFyIGluaXRPcmRlciA9IG5ldyBPcmRlcmVkTGlzdCh0aGlzLl9pbml0aWFsaXplcnMpLm9yZGVyZWRWYWx1ZXMoKTtcbiAgICBpbml0T3JkZXIuZm9yRWFjaChpbml0aWFsaXplciA9PiB7XG4gICAgICBpbml0aWFsaXplcih0aGlzKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8vIGNvbnRleHQgYWNjZXNzb3JzXG4gIGhhcyhrZXkpIHtcbiAgICByZXR1cm4gISF0aGlzLl9jb250ZXh0W2tleV07XG4gIH1cblxuICBnZXQoa2V5LCBmYWxsYmFjaykge1xuICAgIGlmICh0aGlzLmhhcyhrZXkpKSB7XG4gICAgICByZXR1cm4gdGhpcy5fY29udGV4dFtrZXldO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gZmFsbGJhY2sgfHwgdW5kZWZpbmVkO1xuICAgIH1cbiAgfVxuXG4gIHBvcChrZXkpIHtcbiAgICBpZiAodGhpcy5oYXMoa2V5KSkge1xuICAgICAgbGV0IHZhbHVlID0gdGhpcy5fY29udGV4dFtrZXldO1xuICAgICAgdGhpcy5fY29udGV4dFtrZXldID0gbnVsbDtcbiAgICAgIHJldHVybiB2YWx1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG4gIH1cbn1cblxuLy8gY3JlYXRlICBzaW5nbGV0b25cbnZhciBtaXNhZ28gPSBuZXcgTWlzYWdvKCk7XG5cbi8vIGV4cG9zZSBpdCBnbG9iYWxseVxuZ2xvYmFsLm1pc2FnbyA9IG1pc2FnbztcblxuLy8gYW5kIGV4cG9ydCBpdCBmb3IgdGVzdHMgYW5kIHN0dWZmXG5leHBvcnQgZGVmYXVsdCBtaXNhZ287XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBhamF4LmluaXQobWlzYWdvLmdldCgnQ1NSRl9DT09LSUVfTkFNRScpKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2FqYXgnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXJcbn0pO1xuIiwiaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBBdXRoTWVzc2FnZSwgeyBzZWxlY3QgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdXRoLW1lc3NhZ2UnO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbW91bnQoY29ubmVjdChzZWxlY3QpKEF1dGhNZXNzYWdlKSwgJ2F1dGgtbWVzc2FnZS1tb3VudCcpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OmF1dGgtbWVzc2FnZScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHJlZHVjZXIsIHsgaW5pdGlhbFN0YXRlIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL2F1dGgnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKGNvbnRleHQpIHtcbiAgc3RvcmUuYWRkUmVkdWNlcignYXV0aCcsIHJlZHVjZXIsIE9iamVjdC5hc3NpZ24oe1xuICAgICdpc0F1dGhlbnRpY2F0ZWQnOiBjb250ZXh0LmdldCgnaXNBdXRoZW50aWNhdGVkJyksXG4gICAgJ2lzQW5vbnltb3VzJzogIWNvbnRleHQuZ2V0KCdpc0F1dGhlbnRpY2F0ZWQnKSxcblxuICAgICd1c2VyJzogY29udGV4dC5nZXQoJ3VzZXInKVxuICB9LCBpbml0aWFsU3RhdGUpKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3JlZHVjZXI6YXV0aCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYmVmb3JlOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBhdXRoIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hdXRoJztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5pbXBvcnQgc3RvcmFnZSBmcm9tICdtaXNhZ28vc2VydmljZXMvbG9jYWwtc3RvcmFnZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBhdXRoLmluaXQoc3RvcmUsIHN0b3JhZ2UsIG1vZGFsKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2F1dGgnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTsiLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoY29udGV4dCkge1xuICBpZiAoY29udGV4dC5oYXMoJ0JBTl9NRVNTQUdFJykpIHtcbiAgICBzaG93QmFubmVkUGFnZShjb250ZXh0LmdldCgnQkFOX01FU1NBR0UnKSwgZmFsc2UpO1xuICB9XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6YmFuZWQtcGFnZScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IGNhcHRjaGEgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2NhcHRjaGEnO1xuaW1wb3J0IGluY2x1ZGUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2luY2x1ZGUnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKGNvbnRleHQpIHtcbiAgY2FwdGNoYS5pbml0KGNvbnRleHQsIGFqYXgsIGluY2x1ZGUsIHNuYWNrYmFyKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NhcHRjaGEnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXJcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGluY2x1ZGUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2luY2x1ZGUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcihjb250ZXh0KSB7XG4gIGluY2x1ZGUuaW5pdChjb250ZXh0LmdldCgnU1RBVElDX1VSTCcpKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2luY2x1ZGUnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXJcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHN0b3JhZ2UgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2xvY2FsLXN0b3JhZ2UnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc3RvcmFnZS5pbml0KCdtaXNhZ29fJyk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdsb2NhbC1zdG9yYWdlJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBkcm9wZG93biBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9iaWxlLW5hdmJhci1kcm9wZG93bic7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBsZXQgZWxlbWVudCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdtb2JpbGUtbmF2YmFyLWRyb3Bkb3duLW1vdW50Jyk7XG4gIGlmIChlbGVtZW50KSB7XG4gICAgZHJvcGRvd24uaW5pdChlbGVtZW50KTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnZHJvcGRvd24nLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGxldCBlbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ21vZGFsLW1vdW50Jyk7XG4gIGlmIChlbGVtZW50KSB7XG4gICAgbW9kYWwuaW5pdChlbGVtZW50KTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnbW9kYWwnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbW9tZW50IGZyb20gJ21vbWVudCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBtb21lbnQubG9jYWxlKCQoJ2h0bWwnKS5hdHRyKCdsYW5nJykpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnbW9tZW50JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCBPcHRpb25zLCB7IHBhdGhzIH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvb3B0aW9ucy9yb290JztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9yb3V0ZWQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoY29udGV4dCkge1xuICBpZiAoY29udGV4dC5oYXMoJ1VTRVJfT1BUSU9OUycpKSB7XG4gICAgbW91bnQoe1xuICAgICAgcm9vdDogbWlzYWdvLmdldCgnVVNFUkNQX1VSTCcpLFxuICAgICAgY29tcG9uZW50OiBPcHRpb25zLFxuICAgICAgcGF0aHM6IHBhdGhzKHN0b3JlKVxuICAgIH0pO1xuICB9XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6b3B0aW9ucycsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHRpdGxlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9wYWdlLXRpdGxlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoY29udGV4dCkge1xuICB0aXRsZS5pbml0KGNvbnRleHQuZ2V0KCdTRVRUSU5HUycpLmZvcnVtX25hbWUpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAncGFnZS10aXRsZScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplclxufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgUmVxdWVzdEFjdGl2YXRpb25MaW5rIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGlmIChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVxdWVzdC1hY3RpdmF0aW9uLWxpbmstbW91bnQnKSkge1xuICAgIG1vdW50KFJlcXVlc3RBY3RpdmF0aW9uTGluaywgJ3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rLW1vdW50JywgZmFsc2UpO1xuICB9XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6cmVxdWVzdC1hY3RpdmF0aW9uLWxpbmsnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBSZXF1ZXN0UGFzc3dvcmRSZXNldCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9yZXF1ZXN0LXBhc3N3b3JkLXJlc2V0JztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGlmIChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVxdWVzdC1wYXNzd29yZC1yZXNldC1tb3VudCcpKSB7XG4gICAgbW91bnQoUmVxdWVzdFBhc3N3b3JkUmVzZXQsICdyZXF1ZXN0LXBhc3N3b3JkLXJlc2V0LW1vdW50JywgZmFsc2UpO1xuICB9XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6cmVxdWVzdC1wYXNzd29yZC1yZXNldCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IFJlc2V0UGFzc3dvcmRGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3Jlc2V0LXBhc3N3b3JkLWZvcm0nO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgaWYgKGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZXNldC1wYXNzd29yZC1mb3JtLW1vdW50JykpIHtcbiAgICBtb3VudChSZXNldFBhc3N3b3JkRm9ybSwgJ3Jlc2V0LXBhc3N3b3JkLWZvcm0tbW91bnQnLCBmYWxzZSk7XG4gIH1cbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NvbXBvbmVudDpyZXNldC1wYXNzd29yZC1mb3JtJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgeyBjb25uZWN0IH0gZnJvbSAncmVhY3QtcmVkdXgnO1xuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHsgU25hY2tiYXIsIHNlbGVjdCB9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3NuYWNrYmFyJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIG1vdW50KGNvbm5lY3Qoc2VsZWN0KShTbmFja2JhciksICdzbmFja2Jhci1tb3VudCcpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OnNuYWNrYmFyJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3NuYWNrYmFyJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgcmVkdWNlciwgeyBpbml0aWFsU3RhdGUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvc25hY2tiYXInO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBzdG9yZS5hZGRSZWR1Y2VyKCdzbmFja2JhcicsIHJlZHVjZXIsIGluaXRpYWxTdGF0ZSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOnNuYWNrYmFyJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHNuYWNrYmFyLmluaXQoc3RvcmUpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnc25hY2tiYXInLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc3RvcmUuaW5pdCgpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnc3RvcmUnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ19lbmQnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCByZWR1Y2VyLCB7IGluaXRpYWxTdGF0ZSB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy90aWNrJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc3RvcmUuYWRkUmVkdWNlcigndGljaycsIHJlZHVjZXIsIGluaXRpYWxTdGF0ZSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOnRpY2snLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgeyBkb1RpY2sgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdGljayc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuY29uc3QgVElDS19QRVJJT0QgPSA1MCAqIDEwMDA7IC8vZG8gdGhlIHRpY2sgZXZlcnkgNTBzXG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICB3aW5kb3cuc2V0SW50ZXJ2YWwoZnVuY3Rpb24oKSB7XG4gICAgc3RvcmUuZGlzcGF0Y2goZG9UaWNrKCkpO1xuICB9LCBUSUNLX1BFUklPRCk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICd0aWNrLXN0YXJ0JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgeyBjb25uZWN0IH0gZnJvbSAncmVhY3QtcmVkdXgnO1xuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHsgVXNlck1lbnUsIENvbXBhY3RVc2VyTWVudSwgc2VsZWN0IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvdXNlci1tZW51L3Jvb3QnO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbW91bnQoY29ubmVjdChzZWxlY3QpKFVzZXJNZW51KSwgJ3VzZXItbWVudS1tb3VudCcpO1xuICBtb3VudChjb25uZWN0KHNlbGVjdCkoQ29tcGFjdFVzZXJNZW51KSwgJ3VzZXItbWVudS1jb21wYWN0LW1vdW50Jyk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6dXNlci1tZW51JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgcmVkdWNlciBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcm5hbWUtaGlzdG9yeSc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHN0b3JlLmFkZFJlZHVjZXIoJ3VzZXJuYW1lLWhpc3RvcnknLCByZWR1Y2VyLCBbXSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOnVzZXJuYW1lLWhpc3RvcnknLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgVXNlcnMsIHsgcGF0aHMgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2Vycy9yb290JztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9yb3V0ZWQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoY29udGV4dCkge1xuICBpZiAoY29udGV4dC5oYXMoJ1VTRVJTX0xJU1RTJykpIHtcbiAgICBtb3VudCh7XG4gICAgICByb290OiBtaXNhZ28uZ2V0KCdVU0VSU19MSVNUX1VSTCcpLFxuICAgICAgY29tcG9uZW50OiBVc2VycyxcbiAgICAgIHBhdGhzOiBwYXRocyhzdG9yZSlcbiAgICB9KTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OnVzZXJzJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgcmVkdWNlciBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcnMnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBzdG9yZS5hZGRSZWR1Y2VyKCd1c2VycycsIHJlZHVjZXIsIFtdKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3JlZHVjZXI6dXNlcnMnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgaW5jbHVkZSBmcm9tICdtaXNhZ28vc2VydmljZXMvaW5jbHVkZSc7XG5pbXBvcnQgenhjdmJuIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy96eGN2Ym4nO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgenhjdmJuLmluaXQoaW5jbHVkZSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICd6eGN2Ym4nLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXJcbn0pO1xuIiwidmFyIHBTbGljZSA9IEFycmF5LnByb3RvdHlwZS5zbGljZTtcbnZhciBvYmplY3RLZXlzID0gcmVxdWlyZSgnLi9saWIva2V5cy5qcycpO1xudmFyIGlzQXJndW1lbnRzID0gcmVxdWlyZSgnLi9saWIvaXNfYXJndW1lbnRzLmpzJyk7XG5cbnZhciBkZWVwRXF1YWwgPSBtb2R1bGUuZXhwb3J0cyA9IGZ1bmN0aW9uIChhY3R1YWwsIGV4cGVjdGVkLCBvcHRzKSB7XG4gIGlmICghb3B0cykgb3B0cyA9IHt9O1xuICAvLyA3LjEuIEFsbCBpZGVudGljYWwgdmFsdWVzIGFyZSBlcXVpdmFsZW50LCBhcyBkZXRlcm1pbmVkIGJ5ID09PS5cbiAgaWYgKGFjdHVhbCA9PT0gZXhwZWN0ZWQpIHtcbiAgICByZXR1cm4gdHJ1ZTtcblxuICB9IGVsc2UgaWYgKGFjdHVhbCBpbnN0YW5jZW9mIERhdGUgJiYgZXhwZWN0ZWQgaW5zdGFuY2VvZiBEYXRlKSB7XG4gICAgcmV0dXJuIGFjdHVhbC5nZXRUaW1lKCkgPT09IGV4cGVjdGVkLmdldFRpbWUoKTtcblxuICAvLyA3LjMuIE90aGVyIHBhaXJzIHRoYXQgZG8gbm90IGJvdGggcGFzcyB0eXBlb2YgdmFsdWUgPT0gJ29iamVjdCcsXG4gIC8vIGVxdWl2YWxlbmNlIGlzIGRldGVybWluZWQgYnkgPT0uXG4gIH0gZWxzZSBpZiAoIWFjdHVhbCB8fCAhZXhwZWN0ZWQgfHwgdHlwZW9mIGFjdHVhbCAhPSAnb2JqZWN0JyAmJiB0eXBlb2YgZXhwZWN0ZWQgIT0gJ29iamVjdCcpIHtcbiAgICByZXR1cm4gb3B0cy5zdHJpY3QgPyBhY3R1YWwgPT09IGV4cGVjdGVkIDogYWN0dWFsID09IGV4cGVjdGVkO1xuXG4gIC8vIDcuNC4gRm9yIGFsbCBvdGhlciBPYmplY3QgcGFpcnMsIGluY2x1ZGluZyBBcnJheSBvYmplY3RzLCBlcXVpdmFsZW5jZSBpc1xuICAvLyBkZXRlcm1pbmVkIGJ5IGhhdmluZyB0aGUgc2FtZSBudW1iZXIgb2Ygb3duZWQgcHJvcGVydGllcyAoYXMgdmVyaWZpZWRcbiAgLy8gd2l0aCBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwpLCB0aGUgc2FtZSBzZXQgb2Yga2V5c1xuICAvLyAoYWx0aG91Z2ggbm90IG5lY2Vzc2FyaWx5IHRoZSBzYW1lIG9yZGVyKSwgZXF1aXZhbGVudCB2YWx1ZXMgZm9yIGV2ZXJ5XG4gIC8vIGNvcnJlc3BvbmRpbmcga2V5LCBhbmQgYW4gaWRlbnRpY2FsICdwcm90b3R5cGUnIHByb3BlcnR5LiBOb3RlOiB0aGlzXG4gIC8vIGFjY291bnRzIGZvciBib3RoIG5hbWVkIGFuZCBpbmRleGVkIHByb3BlcnRpZXMgb24gQXJyYXlzLlxuICB9IGVsc2Uge1xuICAgIHJldHVybiBvYmpFcXVpdihhY3R1YWwsIGV4cGVjdGVkLCBvcHRzKTtcbiAgfVxufVxuXG5mdW5jdGlvbiBpc1VuZGVmaW5lZE9yTnVsbCh2YWx1ZSkge1xuICByZXR1cm4gdmFsdWUgPT09IG51bGwgfHwgdmFsdWUgPT09IHVuZGVmaW5lZDtcbn1cblxuZnVuY3Rpb24gaXNCdWZmZXIgKHgpIHtcbiAgaWYgKCF4IHx8IHR5cGVvZiB4ICE9PSAnb2JqZWN0JyB8fCB0eXBlb2YgeC5sZW5ndGggIT09ICdudW1iZXInKSByZXR1cm4gZmFsc2U7XG4gIGlmICh0eXBlb2YgeC5jb3B5ICE9PSAnZnVuY3Rpb24nIHx8IHR5cGVvZiB4LnNsaWNlICE9PSAnZnVuY3Rpb24nKSB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG4gIGlmICh4Lmxlbmd0aCA+IDAgJiYgdHlwZW9mIHhbMF0gIT09ICdudW1iZXInKSByZXR1cm4gZmFsc2U7XG4gIHJldHVybiB0cnVlO1xufVxuXG5mdW5jdGlvbiBvYmpFcXVpdihhLCBiLCBvcHRzKSB7XG4gIHZhciBpLCBrZXk7XG4gIGlmIChpc1VuZGVmaW5lZE9yTnVsbChhKSB8fCBpc1VuZGVmaW5lZE9yTnVsbChiKSlcbiAgICByZXR1cm4gZmFsc2U7XG4gIC8vIGFuIGlkZW50aWNhbCAncHJvdG90eXBlJyBwcm9wZXJ0eS5cbiAgaWYgKGEucHJvdG90eXBlICE9PSBiLnByb3RvdHlwZSkgcmV0dXJuIGZhbHNlO1xuICAvL35+fkkndmUgbWFuYWdlZCB0byBicmVhayBPYmplY3Qua2V5cyB0aHJvdWdoIHNjcmV3eSBhcmd1bWVudHMgcGFzc2luZy5cbiAgLy8gICBDb252ZXJ0aW5nIHRvIGFycmF5IHNvbHZlcyB0aGUgcHJvYmxlbS5cbiAgaWYgKGlzQXJndW1lbnRzKGEpKSB7XG4gICAgaWYgKCFpc0FyZ3VtZW50cyhiKSkge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgICBhID0gcFNsaWNlLmNhbGwoYSk7XG4gICAgYiA9IHBTbGljZS5jYWxsKGIpO1xuICAgIHJldHVybiBkZWVwRXF1YWwoYSwgYiwgb3B0cyk7XG4gIH1cbiAgaWYgKGlzQnVmZmVyKGEpKSB7XG4gICAgaWYgKCFpc0J1ZmZlcihiKSkge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgICBpZiAoYS5sZW5ndGggIT09IGIubGVuZ3RoKSByZXR1cm4gZmFsc2U7XG4gICAgZm9yIChpID0gMDsgaSA8IGEubGVuZ3RoOyBpKyspIHtcbiAgICAgIGlmIChhW2ldICE9PSBiW2ldKSByZXR1cm4gZmFsc2U7XG4gICAgfVxuICAgIHJldHVybiB0cnVlO1xuICB9XG4gIHRyeSB7XG4gICAgdmFyIGthID0gb2JqZWN0S2V5cyhhKSxcbiAgICAgICAga2IgPSBvYmplY3RLZXlzKGIpO1xuICB9IGNhdGNoIChlKSB7Ly9oYXBwZW5zIHdoZW4gb25lIGlzIGEgc3RyaW5nIGxpdGVyYWwgYW5kIHRoZSBvdGhlciBpc24ndFxuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuICAvLyBoYXZpbmcgdGhlIHNhbWUgbnVtYmVyIG9mIG93bmVkIHByb3BlcnRpZXMgKGtleXMgaW5jb3Jwb3JhdGVzXG4gIC8vIGhhc093blByb3BlcnR5KVxuICBpZiAoa2EubGVuZ3RoICE9IGtiLmxlbmd0aClcbiAgICByZXR1cm4gZmFsc2U7XG4gIC8vdGhlIHNhbWUgc2V0IG9mIGtleXMgKGFsdGhvdWdoIG5vdCBuZWNlc3NhcmlseSB0aGUgc2FtZSBvcmRlciksXG4gIGthLnNvcnQoKTtcbiAga2Iuc29ydCgpO1xuICAvL35+fmNoZWFwIGtleSB0ZXN0XG4gIGZvciAoaSA9IGthLmxlbmd0aCAtIDE7IGkgPj0gMDsgaS0tKSB7XG4gICAgaWYgKGthW2ldICE9IGtiW2ldKVxuICAgICAgcmV0dXJuIGZhbHNlO1xuICB9XG4gIC8vZXF1aXZhbGVudCB2YWx1ZXMgZm9yIGV2ZXJ5IGNvcnJlc3BvbmRpbmcga2V5LCBhbmRcbiAgLy9+fn5wb3NzaWJseSBleHBlbnNpdmUgZGVlcCB0ZXN0XG4gIGZvciAoaSA9IGthLmxlbmd0aCAtIDE7IGkgPj0gMDsgaS0tKSB7XG4gICAga2V5ID0ga2FbaV07XG4gICAgaWYgKCFkZWVwRXF1YWwoYVtrZXldLCBiW2tleV0sIG9wdHMpKSByZXR1cm4gZmFsc2U7XG4gIH1cbiAgcmV0dXJuIHR5cGVvZiBhID09PSB0eXBlb2YgYjtcbn1cbiIsInZhciBzdXBwb3J0c0FyZ3VtZW50c0NsYXNzID0gKGZ1bmN0aW9uKCl7XG4gIHJldHVybiBPYmplY3QucHJvdG90eXBlLnRvU3RyaW5nLmNhbGwoYXJndW1lbnRzKVxufSkoKSA9PSAnW29iamVjdCBBcmd1bWVudHNdJztcblxuZXhwb3J0cyA9IG1vZHVsZS5leHBvcnRzID0gc3VwcG9ydHNBcmd1bWVudHNDbGFzcyA/IHN1cHBvcnRlZCA6IHVuc3VwcG9ydGVkO1xuXG5leHBvcnRzLnN1cHBvcnRlZCA9IHN1cHBvcnRlZDtcbmZ1bmN0aW9uIHN1cHBvcnRlZChvYmplY3QpIHtcbiAgcmV0dXJuIE9iamVjdC5wcm90b3R5cGUudG9TdHJpbmcuY2FsbChvYmplY3QpID09ICdbb2JqZWN0IEFyZ3VtZW50c10nO1xufTtcblxuZXhwb3J0cy51bnN1cHBvcnRlZCA9IHVuc3VwcG9ydGVkO1xuZnVuY3Rpb24gdW5zdXBwb3J0ZWQob2JqZWN0KXtcbiAgcmV0dXJuIG9iamVjdCAmJlxuICAgIHR5cGVvZiBvYmplY3QgPT0gJ29iamVjdCcgJiZcbiAgICB0eXBlb2Ygb2JqZWN0Lmxlbmd0aCA9PSAnbnVtYmVyJyAmJlxuICAgIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmplY3QsICdjYWxsZWUnKSAmJlxuICAgICFPYmplY3QucHJvdG90eXBlLnByb3BlcnR5SXNFbnVtZXJhYmxlLmNhbGwob2JqZWN0LCAnY2FsbGVlJykgfHxcbiAgICBmYWxzZTtcbn07XG4iLCJleHBvcnRzID0gbW9kdWxlLmV4cG9ydHMgPSB0eXBlb2YgT2JqZWN0LmtleXMgPT09ICdmdW5jdGlvbidcbiAgPyBPYmplY3Qua2V5cyA6IHNoaW07XG5cbmV4cG9ydHMuc2hpbSA9IHNoaW07XG5mdW5jdGlvbiBzaGltIChvYmopIHtcbiAgdmFyIGtleXMgPSBbXTtcbiAgZm9yICh2YXIga2V5IGluIG9iaikga2V5cy5wdXNoKGtleSk7XG4gIHJldHVybiBrZXlzO1xufVxuIiwiLyoqXG4gKiBJbmRpY2F0ZXMgdGhhdCBuYXZpZ2F0aW9uIHdhcyBjYXVzZWQgYnkgYSBjYWxsIHRvIGhpc3RvcnkucHVzaC5cbiAqL1xuJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xudmFyIFBVU0ggPSAnUFVTSCc7XG5cbmV4cG9ydHMuUFVTSCA9IFBVU0g7XG4vKipcbiAqIEluZGljYXRlcyB0aGF0IG5hdmlnYXRpb24gd2FzIGNhdXNlZCBieSBhIGNhbGwgdG8gaGlzdG9yeS5yZXBsYWNlLlxuICovXG52YXIgUkVQTEFDRSA9ICdSRVBMQUNFJztcblxuZXhwb3J0cy5SRVBMQUNFID0gUkVQTEFDRTtcbi8qKlxuICogSW5kaWNhdGVzIHRoYXQgbmF2aWdhdGlvbiB3YXMgY2F1c2VkIGJ5IHNvbWUgb3RoZXIgYWN0aW9uIHN1Y2hcbiAqIGFzIHVzaW5nIGEgYnJvd3NlcidzIGJhY2svZm9yd2FyZCBidXR0b25zIGFuZC9vciBtYW51YWxseSBtYW5pcHVsYXRpbmdcbiAqIHRoZSBVUkwgaW4gYSBicm93c2VyJ3MgbG9jYXRpb24gYmFyLiBUaGlzIGlzIHRoZSBkZWZhdWx0LlxuICpcbiAqIFNlZSBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9BUEkvV2luZG93RXZlbnRIYW5kbGVycy9vbnBvcHN0YXRlXG4gKiBmb3IgbW9yZSBpbmZvcm1hdGlvbi5cbiAqL1xudmFyIFBPUCA9ICdQT1AnO1xuXG5leHBvcnRzLlBPUCA9IFBPUDtcbmV4cG9ydHNbJ2RlZmF1bHQnXSA9IHtcbiAgUFVTSDogUFVTSCxcbiAgUkVQTEFDRTogUkVQTEFDRSxcbiAgUE9QOiBQT1Bcbn07IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbmV4cG9ydHMuX19lc01vZHVsZSA9IHRydWU7XG5leHBvcnRzLmxvb3BBc3luYyA9IGxvb3BBc3luYztcblxuZnVuY3Rpb24gbG9vcEFzeW5jKHR1cm5zLCB3b3JrLCBjYWxsYmFjaykge1xuICB2YXIgY3VycmVudFR1cm4gPSAwO1xuICB2YXIgaXNEb25lID0gZmFsc2U7XG5cbiAgZnVuY3Rpb24gZG9uZSgpIHtcbiAgICBpc0RvbmUgPSB0cnVlO1xuICAgIGNhbGxiYWNrLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XG4gIH1cblxuICBmdW5jdGlvbiBuZXh0KCkge1xuICAgIGlmIChpc0RvbmUpIHJldHVybjtcblxuICAgIGlmIChjdXJyZW50VHVybiA8IHR1cm5zKSB7XG4gICAgICB3b3JrLmNhbGwodGhpcywgY3VycmVudFR1cm4rKywgbmV4dCwgZG9uZSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIGRvbmUuYXBwbHkodGhpcywgYXJndW1lbnRzKTtcbiAgICB9XG4gIH1cblxuICBuZXh0KCk7XG59IiwiLyplc2xpbnQtZGlzYWJsZSBuby1lbXB0eSAqL1xuJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuZXhwb3J0cy5zYXZlU3RhdGUgPSBzYXZlU3RhdGU7XG5leHBvcnRzLnJlYWRTdGF0ZSA9IHJlYWRTdGF0ZTtcblxuZnVuY3Rpb24gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChvYmopIHsgcmV0dXJuIG9iaiAmJiBvYmouX19lc01vZHVsZSA/IG9iaiA6IHsgJ2RlZmF1bHQnOiBvYmogfTsgfVxuXG52YXIgX3dhcm5pbmcgPSByZXF1aXJlKCd3YXJuaW5nJyk7XG5cbnZhciBfd2FybmluZzIgPSBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KF93YXJuaW5nKTtcblxudmFyIEtleVByZWZpeCA9ICdAQEhpc3RvcnkvJztcbnZhciBRdW90YUV4Y2VlZGVkRXJyb3IgPSAnUXVvdGFFeGNlZWRlZEVycm9yJztcbnZhciBTZWN1cml0eUVycm9yID0gJ1NlY3VyaXR5RXJyb3InO1xuXG5mdW5jdGlvbiBjcmVhdGVLZXkoa2V5KSB7XG4gIHJldHVybiBLZXlQcmVmaXggKyBrZXk7XG59XG5cbmZ1bmN0aW9uIHNhdmVTdGF0ZShrZXksIHN0YXRlKSB7XG4gIHRyeSB7XG4gICAgd2luZG93LnNlc3Npb25TdG9yYWdlLnNldEl0ZW0oY3JlYXRlS2V5KGtleSksIEpTT04uc3RyaW5naWZ5KHN0YXRlKSk7XG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgaWYgKGVycm9yLm5hbWUgPT09IFNlY3VyaXR5RXJyb3IpIHtcbiAgICAgIC8vIEJsb2NraW5nIGNvb2tpZXMgaW4gQ2hyb21lL0ZpcmVmb3gvU2FmYXJpIHRocm93cyBTZWN1cml0eUVycm9yIG9uIGFueVxuICAgICAgLy8gYXR0ZW1wdCB0byBhY2Nlc3Mgd2luZG93LnNlc3Npb25TdG9yYWdlLlxuICAgICAgcHJvY2Vzcy5lbnYuTk9ERV9FTlYgIT09ICdwcm9kdWN0aW9uJyA/IF93YXJuaW5nMlsnZGVmYXVsdCddKGZhbHNlLCAnW2hpc3RvcnldIFVuYWJsZSB0byBzYXZlIHN0YXRlOyBzZXNzaW9uU3RvcmFnZSBpcyBub3QgYXZhaWxhYmxlIGR1ZSB0byBzZWN1cml0eSBzZXR0aW5ncycpIDogdW5kZWZpbmVkO1xuXG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgaWYgKGVycm9yLm5hbWUgPT09IFF1b3RhRXhjZWVkZWRFcnJvciAmJiB3aW5kb3cuc2Vzc2lvblN0b3JhZ2UubGVuZ3RoID09PSAwKSB7XG4gICAgICAvLyBTYWZhcmkgXCJwcml2YXRlIG1vZGVcIiB0aHJvd3MgUXVvdGFFeGNlZWRlZEVycm9yLlxuICAgICAgcHJvY2Vzcy5lbnYuTk9ERV9FTlYgIT09ICdwcm9kdWN0aW9uJyA/IF93YXJuaW5nMlsnZGVmYXVsdCddKGZhbHNlLCAnW2hpc3RvcnldIFVuYWJsZSB0byBzYXZlIHN0YXRlOyBzZXNzaW9uU3RvcmFnZSBpcyBub3QgYXZhaWxhYmxlIGluIFNhZmFyaSBwcml2YXRlIG1vZGUnKSA6IHVuZGVmaW5lZDtcblxuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRocm93IGVycm9yO1xuICB9XG59XG5cbmZ1bmN0aW9uIHJlYWRTdGF0ZShrZXkpIHtcbiAgdmFyIGpzb24gPSB1bmRlZmluZWQ7XG4gIHRyeSB7XG4gICAganNvbiA9IHdpbmRvdy5zZXNzaW9uU3RvcmFnZS5nZXRJdGVtKGNyZWF0ZUtleShrZXkpKTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBpZiAoZXJyb3IubmFtZSA9PT0gU2VjdXJpdHlFcnJvcikge1xuICAgICAgLy8gQmxvY2tpbmcgY29va2llcyBpbiBDaHJvbWUvRmlyZWZveC9TYWZhcmkgdGhyb3dzIFNlY3VyaXR5RXJyb3Igb24gYW55XG4gICAgICAvLyBhdHRlbXB0IHRvIGFjY2VzcyB3aW5kb3cuc2Vzc2lvblN0b3JhZ2UuXG4gICAgICBwcm9jZXNzLmVudi5OT0RFX0VOViAhPT0gJ3Byb2R1Y3Rpb24nID8gX3dhcm5pbmcyWydkZWZhdWx0J10oZmFsc2UsICdbaGlzdG9yeV0gVW5hYmxlIHRvIHJlYWQgc3RhdGU7IHNlc3Npb25TdG9yYWdlIGlzIG5vdCBhdmFpbGFibGUgZHVlIHRvIHNlY3VyaXR5IHNldHRpbmdzJykgOiB1bmRlZmluZWQ7XG5cbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIGlmIChqc29uKSB7XG4gICAgdHJ5IHtcbiAgICAgIHJldHVybiBKU09OLnBhcnNlKGpzb24pO1xuICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAvLyBJZ25vcmUgaW52YWxpZCBKU09OLlxuICAgIH1cbiAgfVxuXG4gIHJldHVybiBudWxsO1xufSIsIid1c2Ugc3RyaWN0JztcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcbmV4cG9ydHMuYWRkRXZlbnRMaXN0ZW5lciA9IGFkZEV2ZW50TGlzdGVuZXI7XG5leHBvcnRzLnJlbW92ZUV2ZW50TGlzdGVuZXIgPSByZW1vdmVFdmVudExpc3RlbmVyO1xuZXhwb3J0cy5nZXRIYXNoUGF0aCA9IGdldEhhc2hQYXRoO1xuZXhwb3J0cy5yZXBsYWNlSGFzaFBhdGggPSByZXBsYWNlSGFzaFBhdGg7XG5leHBvcnRzLmdldFdpbmRvd1BhdGggPSBnZXRXaW5kb3dQYXRoO1xuZXhwb3J0cy5nbyA9IGdvO1xuZXhwb3J0cy5nZXRVc2VyQ29uZmlybWF0aW9uID0gZ2V0VXNlckNvbmZpcm1hdGlvbjtcbmV4cG9ydHMuc3VwcG9ydHNIaXN0b3J5ID0gc3VwcG9ydHNIaXN0b3J5O1xuZXhwb3J0cy5zdXBwb3J0c0dvV2l0aG91dFJlbG9hZFVzaW5nSGFzaCA9IHN1cHBvcnRzR29XaXRob3V0UmVsb2FkVXNpbmdIYXNoO1xuXG5mdW5jdGlvbiBhZGRFdmVudExpc3RlbmVyKG5vZGUsIGV2ZW50LCBsaXN0ZW5lcikge1xuICBpZiAobm9kZS5hZGRFdmVudExpc3RlbmVyKSB7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKGV2ZW50LCBsaXN0ZW5lciwgZmFsc2UpO1xuICB9IGVsc2Uge1xuICAgIG5vZGUuYXR0YWNoRXZlbnQoJ29uJyArIGV2ZW50LCBsaXN0ZW5lcik7XG4gIH1cbn1cblxuZnVuY3Rpb24gcmVtb3ZlRXZlbnRMaXN0ZW5lcihub2RlLCBldmVudCwgbGlzdGVuZXIpIHtcbiAgaWYgKG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcikge1xuICAgIG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcihldmVudCwgbGlzdGVuZXIsIGZhbHNlKTtcbiAgfSBlbHNlIHtcbiAgICBub2RlLmRldGFjaEV2ZW50KCdvbicgKyBldmVudCwgbGlzdGVuZXIpO1xuICB9XG59XG5cbmZ1bmN0aW9uIGdldEhhc2hQYXRoKCkge1xuICAvLyBXZSBjYW4ndCB1c2Ugd2luZG93LmxvY2F0aW9uLmhhc2ggaGVyZSBiZWNhdXNlIGl0J3Mgbm90XG4gIC8vIGNvbnNpc3RlbnQgYWNyb3NzIGJyb3dzZXJzIC0gRmlyZWZveCB3aWxsIHByZS1kZWNvZGUgaXQhXG4gIHJldHVybiB3aW5kb3cubG9jYXRpb24uaHJlZi5zcGxpdCgnIycpWzFdIHx8ICcnO1xufVxuXG5mdW5jdGlvbiByZXBsYWNlSGFzaFBhdGgocGF0aCkge1xuICB3aW5kb3cubG9jYXRpb24ucmVwbGFjZSh3aW5kb3cubG9jYXRpb24ucGF0aG5hbWUgKyB3aW5kb3cubG9jYXRpb24uc2VhcmNoICsgJyMnICsgcGF0aCk7XG59XG5cbmZ1bmN0aW9uIGdldFdpbmRvd1BhdGgoKSB7XG4gIHJldHVybiB3aW5kb3cubG9jYXRpb24ucGF0aG5hbWUgKyB3aW5kb3cubG9jYXRpb24uc2VhcmNoICsgd2luZG93LmxvY2F0aW9uLmhhc2g7XG59XG5cbmZ1bmN0aW9uIGdvKG4pIHtcbiAgaWYgKG4pIHdpbmRvdy5oaXN0b3J5LmdvKG4pO1xufVxuXG5mdW5jdGlvbiBnZXRVc2VyQ29uZmlybWF0aW9uKG1lc3NhZ2UsIGNhbGxiYWNrKSB7XG4gIGNhbGxiYWNrKHdpbmRvdy5jb25maXJtKG1lc3NhZ2UpKTtcbn1cblxuLyoqXG4gKiBSZXR1cm5zIHRydWUgaWYgdGhlIEhUTUw1IGhpc3RvcnkgQVBJIGlzIHN1cHBvcnRlZC4gVGFrZW4gZnJvbSBNb2Rlcm5penIuXG4gKlxuICogaHR0cHM6Ly9naXRodWIuY29tL01vZGVybml6ci9Nb2Rlcm5penIvYmxvYi9tYXN0ZXIvTElDRU5TRVxuICogaHR0cHM6Ly9naXRodWIuY29tL01vZGVybml6ci9Nb2Rlcm5penIvYmxvYi9tYXN0ZXIvZmVhdHVyZS1kZXRlY3RzL2hpc3RvcnkuanNcbiAqIGNoYW5nZWQgdG8gYXZvaWQgZmFsc2UgbmVnYXRpdmVzIGZvciBXaW5kb3dzIFBob25lczogaHR0cHM6Ly9naXRodWIuY29tL3JhY2t0L3JlYWN0LXJvdXRlci9pc3N1ZXMvNTg2XG4gKi9cblxuZnVuY3Rpb24gc3VwcG9ydHNIaXN0b3J5KCkge1xuICB2YXIgdWEgPSBuYXZpZ2F0b3IudXNlckFnZW50O1xuICBpZiAoKHVhLmluZGV4T2YoJ0FuZHJvaWQgMi4nKSAhPT0gLTEgfHwgdWEuaW5kZXhPZignQW5kcm9pZCA0LjAnKSAhPT0gLTEpICYmIHVhLmluZGV4T2YoJ01vYmlsZSBTYWZhcmknKSAhPT0gLTEgJiYgdWEuaW5kZXhPZignQ2hyb21lJykgPT09IC0xICYmIHVhLmluZGV4T2YoJ1dpbmRvd3MgUGhvbmUnKSA9PT0gLTEpIHtcbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cbiAgLy8gRklYTUU6IFdvcmsgYXJvdW5kIG91ciBicm93c2VyIGhpc3Rvcnkgbm90IHdvcmtpbmcgY29ycmVjdGx5IG9uIENocm9tZVxuICAvLyBpT1M6IGh0dHBzOi8vZ2l0aHViLmNvbS9yYWNrdC9yZWFjdC1yb3V0ZXIvaXNzdWVzLzI1NjVcbiAgaWYgKHVhLmluZGV4T2YoJ0NyaU9TJykgIT09IC0xKSB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG4gIHJldHVybiB3aW5kb3cuaGlzdG9yeSAmJiAncHVzaFN0YXRlJyBpbiB3aW5kb3cuaGlzdG9yeTtcbn1cblxuLyoqXG4gKiBSZXR1cm5zIGZhbHNlIGlmIHVzaW5nIGdvKG4pIHdpdGggaGFzaCBoaXN0b3J5IGNhdXNlcyBhIGZ1bGwgcGFnZSByZWxvYWQuXG4gKi9cblxuZnVuY3Rpb24gc3VwcG9ydHNHb1dpdGhvdXRSZWxvYWRVc2luZ0hhc2goKSB7XG4gIHZhciB1YSA9IG5hdmlnYXRvci51c2VyQWdlbnQ7XG4gIHJldHVybiB1YS5pbmRleE9mKCdGaXJlZm94JykgPT09IC0xO1xufSIsIid1c2Ugc3RyaWN0JztcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcbnZhciBjYW5Vc2VET00gPSAhISh0eXBlb2Ygd2luZG93ICE9PSAndW5kZWZpbmVkJyAmJiB3aW5kb3cuZG9jdW1lbnQgJiYgd2luZG93LmRvY3VtZW50LmNyZWF0ZUVsZW1lbnQpO1xuZXhwb3J0cy5jYW5Vc2VET00gPSBjYW5Vc2VET007IiwiJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuXG52YXIgX2V4dGVuZHMgPSBPYmplY3QuYXNzaWduIHx8IGZ1bmN0aW9uICh0YXJnZXQpIHsgZm9yICh2YXIgaSA9IDE7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyBpKyspIHsgdmFyIHNvdXJjZSA9IGFyZ3VtZW50c1tpXTsgZm9yICh2YXIga2V5IGluIHNvdXJjZSkgeyBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKHNvdXJjZSwga2V5KSkgeyB0YXJnZXRba2V5XSA9IHNvdXJjZVtrZXldOyB9IH0gfSByZXR1cm4gdGFyZ2V0OyB9O1xuXG5mdW5jdGlvbiBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KG9iaikgeyByZXR1cm4gb2JqICYmIG9iai5fX2VzTW9kdWxlID8gb2JqIDogeyAnZGVmYXVsdCc6IG9iaiB9OyB9XG5cbnZhciBfaW52YXJpYW50ID0gcmVxdWlyZSgnaW52YXJpYW50Jyk7XG5cbnZhciBfaW52YXJpYW50MiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX2ludmFyaWFudCk7XG5cbnZhciBfQWN0aW9ucyA9IHJlcXVpcmUoJy4vQWN0aW9ucycpO1xuXG52YXIgX0V4ZWN1dGlvbkVudmlyb25tZW50ID0gcmVxdWlyZSgnLi9FeGVjdXRpb25FbnZpcm9ubWVudCcpO1xuXG52YXIgX0RPTVV0aWxzID0gcmVxdWlyZSgnLi9ET01VdGlscycpO1xuXG52YXIgX0RPTVN0YXRlU3RvcmFnZSA9IHJlcXVpcmUoJy4vRE9NU3RhdGVTdG9yYWdlJyk7XG5cbnZhciBfY3JlYXRlRE9NSGlzdG9yeSA9IHJlcXVpcmUoJy4vY3JlYXRlRE9NSGlzdG9yeScpO1xuXG52YXIgX2NyZWF0ZURPTUhpc3RvcnkyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfY3JlYXRlRE9NSGlzdG9yeSk7XG5cbnZhciBfcGFyc2VQYXRoID0gcmVxdWlyZSgnLi9wYXJzZVBhdGgnKTtcblxudmFyIF9wYXJzZVBhdGgyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfcGFyc2VQYXRoKTtcblxuLyoqXG4gKiBDcmVhdGVzIGFuZCByZXR1cm5zIGEgaGlzdG9yeSBvYmplY3QgdGhhdCB1c2VzIEhUTUw1J3MgaGlzdG9yeSBBUElcbiAqIChwdXNoU3RhdGUsIHJlcGxhY2VTdGF0ZSwgYW5kIHRoZSBwb3BzdGF0ZSBldmVudCkgdG8gbWFuYWdlIGhpc3RvcnkuXG4gKiBUaGlzIGlzIHRoZSByZWNvbW1lbmRlZCBtZXRob2Qgb2YgbWFuYWdpbmcgaGlzdG9yeSBpbiBicm93c2VycyBiZWNhdXNlXG4gKiBpdCBwcm92aWRlcyB0aGUgY2xlYW5lc3QgVVJMcy5cbiAqXG4gKiBOb3RlOiBJbiBicm93c2VycyB0aGF0IGRvIG5vdCBzdXBwb3J0IHRoZSBIVE1MNSBoaXN0b3J5IEFQSSBmdWxsXG4gKiBwYWdlIHJlbG9hZHMgd2lsbCBiZSB1c2VkIHRvIHByZXNlcnZlIFVSTHMuXG4gKi9cbmZ1bmN0aW9uIGNyZWF0ZUJyb3dzZXJIaXN0b3J5KCkge1xuICB2YXIgb3B0aW9ucyA9IGFyZ3VtZW50cy5sZW5ndGggPD0gMCB8fCBhcmd1bWVudHNbMF0gPT09IHVuZGVmaW5lZCA/IHt9IDogYXJndW1lbnRzWzBdO1xuXG4gICFfRXhlY3V0aW9uRW52aXJvbm1lbnQuY2FuVXNlRE9NID8gcHJvY2Vzcy5lbnYuTk9ERV9FTlYgIT09ICdwcm9kdWN0aW9uJyA/IF9pbnZhcmlhbnQyWydkZWZhdWx0J10oZmFsc2UsICdCcm93c2VyIGhpc3RvcnkgbmVlZHMgYSBET00nKSA6IF9pbnZhcmlhbnQyWydkZWZhdWx0J10oZmFsc2UpIDogdW5kZWZpbmVkO1xuXG4gIHZhciBmb3JjZVJlZnJlc2ggPSBvcHRpb25zLmZvcmNlUmVmcmVzaDtcblxuICB2YXIgaXNTdXBwb3J0ZWQgPSBfRE9NVXRpbHMuc3VwcG9ydHNIaXN0b3J5KCk7XG4gIHZhciB1c2VSZWZyZXNoID0gIWlzU3VwcG9ydGVkIHx8IGZvcmNlUmVmcmVzaDtcblxuICBmdW5jdGlvbiBnZXRDdXJyZW50TG9jYXRpb24oaGlzdG9yeVN0YXRlKSB7XG4gICAgaGlzdG9yeVN0YXRlID0gaGlzdG9yeVN0YXRlIHx8IHdpbmRvdy5oaXN0b3J5LnN0YXRlIHx8IHt9O1xuXG4gICAgdmFyIHBhdGggPSBfRE9NVXRpbHMuZ2V0V2luZG93UGF0aCgpO1xuICAgIHZhciBfaGlzdG9yeVN0YXRlID0gaGlzdG9yeVN0YXRlO1xuICAgIHZhciBrZXkgPSBfaGlzdG9yeVN0YXRlLmtleTtcblxuICAgIHZhciBzdGF0ZSA9IHVuZGVmaW5lZDtcbiAgICBpZiAoa2V5KSB7XG4gICAgICBzdGF0ZSA9IF9ET01TdGF0ZVN0b3JhZ2UucmVhZFN0YXRlKGtleSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0YXRlID0gbnVsbDtcbiAgICAgIGtleSA9IGhpc3RvcnkuY3JlYXRlS2V5KCk7XG5cbiAgICAgIGlmIChpc1N1cHBvcnRlZCkgd2luZG93Lmhpc3RvcnkucmVwbGFjZVN0YXRlKF9leHRlbmRzKHt9LCBoaXN0b3J5U3RhdGUsIHsga2V5OiBrZXkgfSksIG51bGwsIHBhdGgpO1xuICAgIH1cblxuICAgIHZhciBsb2NhdGlvbiA9IF9wYXJzZVBhdGgyWydkZWZhdWx0J10ocGF0aCk7XG5cbiAgICByZXR1cm4gaGlzdG9yeS5jcmVhdGVMb2NhdGlvbihfZXh0ZW5kcyh7fSwgbG9jYXRpb24sIHsgc3RhdGU6IHN0YXRlIH0pLCB1bmRlZmluZWQsIGtleSk7XG4gIH1cblxuICBmdW5jdGlvbiBzdGFydFBvcFN0YXRlTGlzdGVuZXIoX3JlZikge1xuICAgIHZhciB0cmFuc2l0aW9uVG8gPSBfcmVmLnRyYW5zaXRpb25UbztcblxuICAgIGZ1bmN0aW9uIHBvcFN0YXRlTGlzdGVuZXIoZXZlbnQpIHtcbiAgICAgIGlmIChldmVudC5zdGF0ZSA9PT0gdW5kZWZpbmVkKSByZXR1cm47IC8vIElnbm9yZSBleHRyYW5lb3VzIHBvcHN0YXRlIGV2ZW50cyBpbiBXZWJLaXQuXG5cbiAgICAgIHRyYW5zaXRpb25UbyhnZXRDdXJyZW50TG9jYXRpb24oZXZlbnQuc3RhdGUpKTtcbiAgICB9XG5cbiAgICBfRE9NVXRpbHMuYWRkRXZlbnRMaXN0ZW5lcih3aW5kb3csICdwb3BzdGF0ZScsIHBvcFN0YXRlTGlzdGVuZXIpO1xuXG4gICAgcmV0dXJuIGZ1bmN0aW9uICgpIHtcbiAgICAgIF9ET01VdGlscy5yZW1vdmVFdmVudExpc3RlbmVyKHdpbmRvdywgJ3BvcHN0YXRlJywgcG9wU3RhdGVMaXN0ZW5lcik7XG4gICAgfTtcbiAgfVxuXG4gIGZ1bmN0aW9uIGZpbmlzaFRyYW5zaXRpb24obG9jYXRpb24pIHtcbiAgICB2YXIgYmFzZW5hbWUgPSBsb2NhdGlvbi5iYXNlbmFtZTtcbiAgICB2YXIgcGF0aG5hbWUgPSBsb2NhdGlvbi5wYXRobmFtZTtcbiAgICB2YXIgc2VhcmNoID0gbG9jYXRpb24uc2VhcmNoO1xuICAgIHZhciBoYXNoID0gbG9jYXRpb24uaGFzaDtcbiAgICB2YXIgc3RhdGUgPSBsb2NhdGlvbi5zdGF0ZTtcbiAgICB2YXIgYWN0aW9uID0gbG9jYXRpb24uYWN0aW9uO1xuICAgIHZhciBrZXkgPSBsb2NhdGlvbi5rZXk7XG5cbiAgICBpZiAoYWN0aW9uID09PSBfQWN0aW9ucy5QT1ApIHJldHVybjsgLy8gTm90aGluZyB0byBkby5cblxuICAgIF9ET01TdGF0ZVN0b3JhZ2Uuc2F2ZVN0YXRlKGtleSwgc3RhdGUpO1xuXG4gICAgdmFyIHBhdGggPSAoYmFzZW5hbWUgfHwgJycpICsgcGF0aG5hbWUgKyBzZWFyY2ggKyBoYXNoO1xuICAgIHZhciBoaXN0b3J5U3RhdGUgPSB7XG4gICAgICBrZXk6IGtleVxuICAgIH07XG5cbiAgICBpZiAoYWN0aW9uID09PSBfQWN0aW9ucy5QVVNIKSB7XG4gICAgICBpZiAodXNlUmVmcmVzaCkge1xuICAgICAgICB3aW5kb3cubG9jYXRpb24uaHJlZiA9IHBhdGg7XG4gICAgICAgIHJldHVybiBmYWxzZTsgLy8gUHJldmVudCBsb2NhdGlvbiB1cGRhdGUuXG4gICAgICB9IGVsc2Uge1xuICAgICAgICAgIHdpbmRvdy5oaXN0b3J5LnB1c2hTdGF0ZShoaXN0b3J5U3RhdGUsIG51bGwsIHBhdGgpO1xuICAgICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIFJFUExBQ0VcbiAgICAgIGlmICh1c2VSZWZyZXNoKSB7XG4gICAgICAgIHdpbmRvdy5sb2NhdGlvbi5yZXBsYWNlKHBhdGgpO1xuICAgICAgICByZXR1cm4gZmFsc2U7IC8vIFByZXZlbnQgbG9jYXRpb24gdXBkYXRlLlxuICAgICAgfSBlbHNlIHtcbiAgICAgICAgICB3aW5kb3cuaGlzdG9yeS5yZXBsYWNlU3RhdGUoaGlzdG9yeVN0YXRlLCBudWxsLCBwYXRoKTtcbiAgICAgICAgfVxuICAgIH1cbiAgfVxuXG4gIHZhciBoaXN0b3J5ID0gX2NyZWF0ZURPTUhpc3RvcnkyWydkZWZhdWx0J10oX2V4dGVuZHMoe30sIG9wdGlvbnMsIHtcbiAgICBnZXRDdXJyZW50TG9jYXRpb246IGdldEN1cnJlbnRMb2NhdGlvbixcbiAgICBmaW5pc2hUcmFuc2l0aW9uOiBmaW5pc2hUcmFuc2l0aW9uLFxuICAgIHNhdmVTdGF0ZTogX0RPTVN0YXRlU3RvcmFnZS5zYXZlU3RhdGVcbiAgfSkpO1xuXG4gIHZhciBsaXN0ZW5lckNvdW50ID0gMCxcbiAgICAgIHN0b3BQb3BTdGF0ZUxpc3RlbmVyID0gdW5kZWZpbmVkO1xuXG4gIGZ1bmN0aW9uIGxpc3RlbkJlZm9yZShsaXN0ZW5lcikge1xuICAgIGlmICgrK2xpc3RlbmVyQ291bnQgPT09IDEpIHN0b3BQb3BTdGF0ZUxpc3RlbmVyID0gc3RhcnRQb3BTdGF0ZUxpc3RlbmVyKGhpc3RvcnkpO1xuXG4gICAgdmFyIHVubGlzdGVuID0gaGlzdG9yeS5saXN0ZW5CZWZvcmUobGlzdGVuZXIpO1xuXG4gICAgcmV0dXJuIGZ1bmN0aW9uICgpIHtcbiAgICAgIHVubGlzdGVuKCk7XG5cbiAgICAgIGlmICgtLWxpc3RlbmVyQ291bnQgPT09IDApIHN0b3BQb3BTdGF0ZUxpc3RlbmVyKCk7XG4gICAgfTtcbiAgfVxuXG4gIGZ1bmN0aW9uIGxpc3RlbihsaXN0ZW5lcikge1xuICAgIGlmICgrK2xpc3RlbmVyQ291bnQgPT09IDEpIHN0b3BQb3BTdGF0ZUxpc3RlbmVyID0gc3RhcnRQb3BTdGF0ZUxpc3RlbmVyKGhpc3RvcnkpO1xuXG4gICAgdmFyIHVubGlzdGVuID0gaGlzdG9yeS5saXN0ZW4obGlzdGVuZXIpO1xuXG4gICAgcmV0dXJuIGZ1bmN0aW9uICgpIHtcbiAgICAgIHVubGlzdGVuKCk7XG5cbiAgICAgIGlmICgtLWxpc3RlbmVyQ291bnQgPT09IDApIHN0b3BQb3BTdGF0ZUxpc3RlbmVyKCk7XG4gICAgfTtcbiAgfVxuXG4gIC8vIGRlcHJlY2F0ZWRcbiAgZnVuY3Rpb24gcmVnaXN0ZXJUcmFuc2l0aW9uSG9vayhob29rKSB7XG4gICAgaWYgKCsrbGlzdGVuZXJDb3VudCA9PT0gMSkgc3RvcFBvcFN0YXRlTGlzdGVuZXIgPSBzdGFydFBvcFN0YXRlTGlzdGVuZXIoaGlzdG9yeSk7XG5cbiAgICBoaXN0b3J5LnJlZ2lzdGVyVHJhbnNpdGlvbkhvb2soaG9vayk7XG4gIH1cblxuICAvLyBkZXByZWNhdGVkXG4gIGZ1bmN0aW9uIHVucmVnaXN0ZXJUcmFuc2l0aW9uSG9vayhob29rKSB7XG4gICAgaGlzdG9yeS51bnJlZ2lzdGVyVHJhbnNpdGlvbkhvb2soaG9vayk7XG5cbiAgICBpZiAoLS1saXN0ZW5lckNvdW50ID09PSAwKSBzdG9wUG9wU3RhdGVMaXN0ZW5lcigpO1xuICB9XG5cbiAgcmV0dXJuIF9leHRlbmRzKHt9LCBoaXN0b3J5LCB7XG4gICAgbGlzdGVuQmVmb3JlOiBsaXN0ZW5CZWZvcmUsXG4gICAgbGlzdGVuOiBsaXN0ZW4sXG4gICAgcmVnaXN0ZXJUcmFuc2l0aW9uSG9vazogcmVnaXN0ZXJUcmFuc2l0aW9uSG9vayxcbiAgICB1bnJlZ2lzdGVyVHJhbnNpdGlvbkhvb2s6IHVucmVnaXN0ZXJUcmFuc2l0aW9uSG9va1xuICB9KTtcbn1cblxuZXhwb3J0c1snZGVmYXVsdCddID0gY3JlYXRlQnJvd3Nlckhpc3Rvcnk7XG5tb2R1bGUuZXhwb3J0cyA9IGV4cG9ydHNbJ2RlZmF1bHQnXTsiLCIndXNlIHN0cmljdCc7XG5cbmV4cG9ydHMuX19lc01vZHVsZSA9IHRydWU7XG5cbnZhciBfZXh0ZW5kcyA9IE9iamVjdC5hc3NpZ24gfHwgZnVuY3Rpb24gKHRhcmdldCkgeyBmb3IgKHZhciBpID0gMTsgaSA8IGFyZ3VtZW50cy5sZW5ndGg7IGkrKykgeyB2YXIgc291cmNlID0gYXJndW1lbnRzW2ldOyBmb3IgKHZhciBrZXkgaW4gc291cmNlKSB7IGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwoc291cmNlLCBrZXkpKSB7IHRhcmdldFtrZXldID0gc291cmNlW2tleV07IH0gfSB9IHJldHVybiB0YXJnZXQ7IH07XG5cbmZ1bmN0aW9uIF9pbnRlcm9wUmVxdWlyZURlZmF1bHQob2JqKSB7IHJldHVybiBvYmogJiYgb2JqLl9fZXNNb2R1bGUgPyBvYmogOiB7ICdkZWZhdWx0Jzogb2JqIH07IH1cblxudmFyIF9pbnZhcmlhbnQgPSByZXF1aXJlKCdpbnZhcmlhbnQnKTtcblxudmFyIF9pbnZhcmlhbnQyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfaW52YXJpYW50KTtcblxudmFyIF9FeGVjdXRpb25FbnZpcm9ubWVudCA9IHJlcXVpcmUoJy4vRXhlY3V0aW9uRW52aXJvbm1lbnQnKTtcblxudmFyIF9ET01VdGlscyA9IHJlcXVpcmUoJy4vRE9NVXRpbHMnKTtcblxudmFyIF9jcmVhdGVIaXN0b3J5ID0gcmVxdWlyZSgnLi9jcmVhdGVIaXN0b3J5Jyk7XG5cbnZhciBfY3JlYXRlSGlzdG9yeTIgPSBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KF9jcmVhdGVIaXN0b3J5KTtcblxuZnVuY3Rpb24gY3JlYXRlRE9NSGlzdG9yeShvcHRpb25zKSB7XG4gIHZhciBoaXN0b3J5ID0gX2NyZWF0ZUhpc3RvcnkyWydkZWZhdWx0J10oX2V4dGVuZHMoe1xuICAgIGdldFVzZXJDb25maXJtYXRpb246IF9ET01VdGlscy5nZXRVc2VyQ29uZmlybWF0aW9uXG4gIH0sIG9wdGlvbnMsIHtcbiAgICBnbzogX0RPTVV0aWxzLmdvXG4gIH0pKTtcblxuICBmdW5jdGlvbiBsaXN0ZW4obGlzdGVuZXIpIHtcbiAgICAhX0V4ZWN1dGlvbkVudmlyb25tZW50LmNhblVzZURPTSA/IHByb2Nlc3MuZW52Lk5PREVfRU5WICE9PSAncHJvZHVjdGlvbicgPyBfaW52YXJpYW50MlsnZGVmYXVsdCddKGZhbHNlLCAnRE9NIGhpc3RvcnkgbmVlZHMgYSBET00nKSA6IF9pbnZhcmlhbnQyWydkZWZhdWx0J10oZmFsc2UpIDogdW5kZWZpbmVkO1xuXG4gICAgcmV0dXJuIGhpc3RvcnkubGlzdGVuKGxpc3RlbmVyKTtcbiAgfVxuXG4gIHJldHVybiBfZXh0ZW5kcyh7fSwgaGlzdG9yeSwge1xuICAgIGxpc3RlbjogbGlzdGVuXG4gIH0pO1xufVxuXG5leHBvcnRzWydkZWZhdWx0J10gPSBjcmVhdGVET01IaXN0b3J5O1xubW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzWydkZWZhdWx0J107IiwiLy9pbXBvcnQgd2FybmluZyBmcm9tICd3YXJuaW5nJ1xuJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuXG52YXIgX2V4dGVuZHMgPSBPYmplY3QuYXNzaWduIHx8IGZ1bmN0aW9uICh0YXJnZXQpIHsgZm9yICh2YXIgaSA9IDE7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyBpKyspIHsgdmFyIHNvdXJjZSA9IGFyZ3VtZW50c1tpXTsgZm9yICh2YXIga2V5IGluIHNvdXJjZSkgeyBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKHNvdXJjZSwga2V5KSkgeyB0YXJnZXRba2V5XSA9IHNvdXJjZVtrZXldOyB9IH0gfSByZXR1cm4gdGFyZ2V0OyB9O1xuXG5mdW5jdGlvbiBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KG9iaikgeyByZXR1cm4gb2JqICYmIG9iai5fX2VzTW9kdWxlID8gb2JqIDogeyAnZGVmYXVsdCc6IG9iaiB9OyB9XG5cbnZhciBfZGVlcEVxdWFsID0gcmVxdWlyZSgnZGVlcC1lcXVhbCcpO1xuXG52YXIgX2RlZXBFcXVhbDIgPSBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KF9kZWVwRXF1YWwpO1xuXG52YXIgX0FzeW5jVXRpbHMgPSByZXF1aXJlKCcuL0FzeW5jVXRpbHMnKTtcblxudmFyIF9BY3Rpb25zID0gcmVxdWlyZSgnLi9BY3Rpb25zJyk7XG5cbnZhciBfY3JlYXRlTG9jYXRpb24yID0gcmVxdWlyZSgnLi9jcmVhdGVMb2NhdGlvbicpO1xuXG52YXIgX2NyZWF0ZUxvY2F0aW9uMyA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX2NyZWF0ZUxvY2F0aW9uMik7XG5cbnZhciBfcnVuVHJhbnNpdGlvbkhvb2sgPSByZXF1aXJlKCcuL3J1blRyYW5zaXRpb25Ib29rJyk7XG5cbnZhciBfcnVuVHJhbnNpdGlvbkhvb2syID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfcnVuVHJhbnNpdGlvbkhvb2spO1xuXG52YXIgX3BhcnNlUGF0aCA9IHJlcXVpcmUoJy4vcGFyc2VQYXRoJyk7XG5cbnZhciBfcGFyc2VQYXRoMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX3BhcnNlUGF0aCk7XG5cbnZhciBfZGVwcmVjYXRlID0gcmVxdWlyZSgnLi9kZXByZWNhdGUnKTtcblxudmFyIF9kZXByZWNhdGUyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfZGVwcmVjYXRlKTtcblxuZnVuY3Rpb24gY3JlYXRlUmFuZG9tS2V5KGxlbmd0aCkge1xuICByZXR1cm4gTWF0aC5yYW5kb20oKS50b1N0cmluZygzNikuc3Vic3RyKDIsIGxlbmd0aCk7XG59XG5cbmZ1bmN0aW9uIGxvY2F0aW9uc0FyZUVxdWFsKGEsIGIpIHtcbiAgcmV0dXJuIGEucGF0aG5hbWUgPT09IGIucGF0aG5hbWUgJiYgYS5zZWFyY2ggPT09IGIuc2VhcmNoICYmXG4gIC8vYS5hY3Rpb24gPT09IGIuYWN0aW9uICYmIC8vIERpZmZlcmVudCBhY3Rpb24gIT09IGxvY2F0aW9uIGNoYW5nZS5cbiAgYS5rZXkgPT09IGIua2V5ICYmIF9kZWVwRXF1YWwyWydkZWZhdWx0J10oYS5zdGF0ZSwgYi5zdGF0ZSk7XG59XG5cbnZhciBEZWZhdWx0S2V5TGVuZ3RoID0gNjtcblxuZnVuY3Rpb24gY3JlYXRlSGlzdG9yeSgpIHtcbiAgdmFyIG9wdGlvbnMgPSBhcmd1bWVudHMubGVuZ3RoIDw9IDAgfHwgYXJndW1lbnRzWzBdID09PSB1bmRlZmluZWQgPyB7fSA6IGFyZ3VtZW50c1swXTtcbiAgdmFyIGdldEN1cnJlbnRMb2NhdGlvbiA9IG9wdGlvbnMuZ2V0Q3VycmVudExvY2F0aW9uO1xuICB2YXIgZmluaXNoVHJhbnNpdGlvbiA9IG9wdGlvbnMuZmluaXNoVHJhbnNpdGlvbjtcbiAgdmFyIHNhdmVTdGF0ZSA9IG9wdGlvbnMuc2F2ZVN0YXRlO1xuICB2YXIgZ28gPSBvcHRpb25zLmdvO1xuICB2YXIga2V5TGVuZ3RoID0gb3B0aW9ucy5rZXlMZW5ndGg7XG4gIHZhciBnZXRVc2VyQ29uZmlybWF0aW9uID0gb3B0aW9ucy5nZXRVc2VyQ29uZmlybWF0aW9uO1xuXG4gIGlmICh0eXBlb2Yga2V5TGVuZ3RoICE9PSAnbnVtYmVyJykga2V5TGVuZ3RoID0gRGVmYXVsdEtleUxlbmd0aDtcblxuICB2YXIgdHJhbnNpdGlvbkhvb2tzID0gW107XG5cbiAgZnVuY3Rpb24gbGlzdGVuQmVmb3JlKGhvb2spIHtcbiAgICB0cmFuc2l0aW9uSG9va3MucHVzaChob29rKTtcblxuICAgIHJldHVybiBmdW5jdGlvbiAoKSB7XG4gICAgICB0cmFuc2l0aW9uSG9va3MgPSB0cmFuc2l0aW9uSG9va3MuZmlsdGVyKGZ1bmN0aW9uIChpdGVtKSB7XG4gICAgICAgIHJldHVybiBpdGVtICE9PSBob29rO1xuICAgICAgfSk7XG4gICAgfTtcbiAgfVxuXG4gIHZhciBhbGxLZXlzID0gW107XG4gIHZhciBjaGFuZ2VMaXN0ZW5lcnMgPSBbXTtcbiAgdmFyIGxvY2F0aW9uID0gdW5kZWZpbmVkO1xuXG4gIGZ1bmN0aW9uIGdldEN1cnJlbnQoKSB7XG4gICAgaWYgKHBlbmRpbmdMb2NhdGlvbiAmJiBwZW5kaW5nTG9jYXRpb24uYWN0aW9uID09PSBfQWN0aW9ucy5QT1ApIHtcbiAgICAgIHJldHVybiBhbGxLZXlzLmluZGV4T2YocGVuZGluZ0xvY2F0aW9uLmtleSk7XG4gICAgfSBlbHNlIGlmIChsb2NhdGlvbikge1xuICAgICAgcmV0dXJuIGFsbEtleXMuaW5kZXhPZihsb2NhdGlvbi5rZXkpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gLTE7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gdXBkYXRlTG9jYXRpb24obmV3TG9jYXRpb24pIHtcbiAgICB2YXIgY3VycmVudCA9IGdldEN1cnJlbnQoKTtcblxuICAgIGxvY2F0aW9uID0gbmV3TG9jYXRpb247XG5cbiAgICBpZiAobG9jYXRpb24uYWN0aW9uID09PSBfQWN0aW9ucy5QVVNIKSB7XG4gICAgICBhbGxLZXlzID0gW10uY29uY2F0KGFsbEtleXMuc2xpY2UoMCwgY3VycmVudCArIDEpLCBbbG9jYXRpb24ua2V5XSk7XG4gICAgfSBlbHNlIGlmIChsb2NhdGlvbi5hY3Rpb24gPT09IF9BY3Rpb25zLlJFUExBQ0UpIHtcbiAgICAgIGFsbEtleXNbY3VycmVudF0gPSBsb2NhdGlvbi5rZXk7XG4gICAgfVxuXG4gICAgY2hhbmdlTGlzdGVuZXJzLmZvckVhY2goZnVuY3Rpb24gKGxpc3RlbmVyKSB7XG4gICAgICBsaXN0ZW5lcihsb2NhdGlvbik7XG4gICAgfSk7XG4gIH1cblxuICBmdW5jdGlvbiBsaXN0ZW4obGlzdGVuZXIpIHtcbiAgICBjaGFuZ2VMaXN0ZW5lcnMucHVzaChsaXN0ZW5lcik7XG5cbiAgICBpZiAobG9jYXRpb24pIHtcbiAgICAgIGxpc3RlbmVyKGxvY2F0aW9uKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdmFyIF9sb2NhdGlvbiA9IGdldEN1cnJlbnRMb2NhdGlvbigpO1xuICAgICAgYWxsS2V5cyA9IFtfbG9jYXRpb24ua2V5XTtcbiAgICAgIHVwZGF0ZUxvY2F0aW9uKF9sb2NhdGlvbik7XG4gICAgfVxuXG4gICAgcmV0dXJuIGZ1bmN0aW9uICgpIHtcbiAgICAgIGNoYW5nZUxpc3RlbmVycyA9IGNoYW5nZUxpc3RlbmVycy5maWx0ZXIoZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICAgICAgcmV0dXJuIGl0ZW0gIT09IGxpc3RlbmVyO1xuICAgICAgfSk7XG4gICAgfTtcbiAgfVxuXG4gIGZ1bmN0aW9uIGNvbmZpcm1UcmFuc2l0aW9uVG8obG9jYXRpb24sIGNhbGxiYWNrKSB7XG4gICAgX0FzeW5jVXRpbHMubG9vcEFzeW5jKHRyYW5zaXRpb25Ib29rcy5sZW5ndGgsIGZ1bmN0aW9uIChpbmRleCwgbmV4dCwgZG9uZSkge1xuICAgICAgX3J1blRyYW5zaXRpb25Ib29rMlsnZGVmYXVsdCddKHRyYW5zaXRpb25Ib29rc1tpbmRleF0sIGxvY2F0aW9uLCBmdW5jdGlvbiAocmVzdWx0KSB7XG4gICAgICAgIGlmIChyZXN1bHQgIT0gbnVsbCkge1xuICAgICAgICAgIGRvbmUocmVzdWx0KTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBuZXh0KCk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH0sIGZ1bmN0aW9uIChtZXNzYWdlKSB7XG4gICAgICBpZiAoZ2V0VXNlckNvbmZpcm1hdGlvbiAmJiB0eXBlb2YgbWVzc2FnZSA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgZ2V0VXNlckNvbmZpcm1hdGlvbihtZXNzYWdlLCBmdW5jdGlvbiAob2spIHtcbiAgICAgICAgICBjYWxsYmFjayhvayAhPT0gZmFsc2UpO1xuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGNhbGxiYWNrKG1lc3NhZ2UgIT09IGZhbHNlKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIHZhciBwZW5kaW5nTG9jYXRpb24gPSB1bmRlZmluZWQ7XG5cbiAgZnVuY3Rpb24gdHJhbnNpdGlvblRvKG5leHRMb2NhdGlvbikge1xuICAgIGlmIChsb2NhdGlvbiAmJiBsb2NhdGlvbnNBcmVFcXVhbChsb2NhdGlvbiwgbmV4dExvY2F0aW9uKSkgcmV0dXJuOyAvLyBOb3RoaW5nIHRvIGRvLlxuXG4gICAgcGVuZGluZ0xvY2F0aW9uID0gbmV4dExvY2F0aW9uO1xuXG4gICAgY29uZmlybVRyYW5zaXRpb25UbyhuZXh0TG9jYXRpb24sIGZ1bmN0aW9uIChvaykge1xuICAgICAgaWYgKHBlbmRpbmdMb2NhdGlvbiAhPT0gbmV4dExvY2F0aW9uKSByZXR1cm47IC8vIFRyYW5zaXRpb24gd2FzIGludGVycnVwdGVkLlxuXG4gICAgICBpZiAob2spIHtcbiAgICAgICAgLy8gdHJlYXQgUFVTSCB0byBjdXJyZW50IHBhdGggbGlrZSBSRVBMQUNFIHRvIGJlIGNvbnNpc3RlbnQgd2l0aCBicm93c2Vyc1xuICAgICAgICBpZiAobmV4dExvY2F0aW9uLmFjdGlvbiA9PT0gX0FjdGlvbnMuUFVTSCkge1xuICAgICAgICAgIHZhciBwcmV2UGF0aCA9IGNyZWF0ZVBhdGgobG9jYXRpb24pO1xuICAgICAgICAgIHZhciBuZXh0UGF0aCA9IGNyZWF0ZVBhdGgobmV4dExvY2F0aW9uKTtcblxuICAgICAgICAgIGlmIChuZXh0UGF0aCA9PT0gcHJldlBhdGgpIG5leHRMb2NhdGlvbi5hY3Rpb24gPSBfQWN0aW9ucy5SRVBMQUNFO1xuICAgICAgICB9XG5cbiAgICAgICAgaWYgKGZpbmlzaFRyYW5zaXRpb24obmV4dExvY2F0aW9uKSAhPT0gZmFsc2UpIHVwZGF0ZUxvY2F0aW9uKG5leHRMb2NhdGlvbik7XG4gICAgICB9IGVsc2UgaWYgKGxvY2F0aW9uICYmIG5leHRMb2NhdGlvbi5hY3Rpb24gPT09IF9BY3Rpb25zLlBPUCkge1xuICAgICAgICB2YXIgcHJldkluZGV4ID0gYWxsS2V5cy5pbmRleE9mKGxvY2F0aW9uLmtleSk7XG4gICAgICAgIHZhciBuZXh0SW5kZXggPSBhbGxLZXlzLmluZGV4T2YobmV4dExvY2F0aW9uLmtleSk7XG5cbiAgICAgICAgaWYgKHByZXZJbmRleCAhPT0gLTEgJiYgbmV4dEluZGV4ICE9PSAtMSkgZ28ocHJldkluZGV4IC0gbmV4dEluZGV4KTsgLy8gUmVzdG9yZSB0aGUgVVJMLlxuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgZnVuY3Rpb24gcHVzaChsb2NhdGlvbikge1xuICAgIHRyYW5zaXRpb25UbyhjcmVhdGVMb2NhdGlvbihsb2NhdGlvbiwgX0FjdGlvbnMuUFVTSCwgY3JlYXRlS2V5KCkpKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIHJlcGxhY2UobG9jYXRpb24pIHtcbiAgICB0cmFuc2l0aW9uVG8oY3JlYXRlTG9jYXRpb24obG9jYXRpb24sIF9BY3Rpb25zLlJFUExBQ0UsIGNyZWF0ZUtleSgpKSk7XG4gIH1cblxuICBmdW5jdGlvbiBnb0JhY2soKSB7XG4gICAgZ28oLTEpO1xuICB9XG5cbiAgZnVuY3Rpb24gZ29Gb3J3YXJkKCkge1xuICAgIGdvKDEpO1xuICB9XG5cbiAgZnVuY3Rpb24gY3JlYXRlS2V5KCkge1xuICAgIHJldHVybiBjcmVhdGVSYW5kb21LZXkoa2V5TGVuZ3RoKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIGNyZWF0ZVBhdGgobG9jYXRpb24pIHtcbiAgICBpZiAobG9jYXRpb24gPT0gbnVsbCB8fCB0eXBlb2YgbG9jYXRpb24gPT09ICdzdHJpbmcnKSByZXR1cm4gbG9jYXRpb247XG5cbiAgICB2YXIgcGF0aG5hbWUgPSBsb2NhdGlvbi5wYXRobmFtZTtcbiAgICB2YXIgc2VhcmNoID0gbG9jYXRpb24uc2VhcmNoO1xuICAgIHZhciBoYXNoID0gbG9jYXRpb24uaGFzaDtcblxuICAgIHZhciByZXN1bHQgPSBwYXRobmFtZTtcblxuICAgIGlmIChzZWFyY2gpIHJlc3VsdCArPSBzZWFyY2g7XG5cbiAgICBpZiAoaGFzaCkgcmVzdWx0ICs9IGhhc2g7XG5cbiAgICByZXR1cm4gcmVzdWx0O1xuICB9XG5cbiAgZnVuY3Rpb24gY3JlYXRlSHJlZihsb2NhdGlvbikge1xuICAgIHJldHVybiBjcmVhdGVQYXRoKGxvY2F0aW9uKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIGNyZWF0ZUxvY2F0aW9uKGxvY2F0aW9uLCBhY3Rpb24pIHtcbiAgICB2YXIga2V5ID0gYXJndW1lbnRzLmxlbmd0aCA8PSAyIHx8IGFyZ3VtZW50c1syXSA9PT0gdW5kZWZpbmVkID8gY3JlYXRlS2V5KCkgOiBhcmd1bWVudHNbMl07XG5cbiAgICBpZiAodHlwZW9mIGFjdGlvbiA9PT0gJ29iamVjdCcpIHtcbiAgICAgIC8vd2FybmluZyhcbiAgICAgIC8vICBmYWxzZSxcbiAgICAgIC8vICAnVGhlIHN0YXRlICgybmQpIGFyZ3VtZW50IHRvIGhpc3RvcnkuY3JlYXRlTG9jYXRpb24gaXMgZGVwcmVjYXRlZDsgdXNlIGEgJyArXG4gICAgICAvLyAgJ2xvY2F0aW9uIGRlc2NyaXB0b3IgaW5zdGVhZCdcbiAgICAgIC8vKVxuXG4gICAgICBpZiAodHlwZW9mIGxvY2F0aW9uID09PSAnc3RyaW5nJykgbG9jYXRpb24gPSBfcGFyc2VQYXRoMlsnZGVmYXVsdCddKGxvY2F0aW9uKTtcblxuICAgICAgbG9jYXRpb24gPSBfZXh0ZW5kcyh7fSwgbG9jYXRpb24sIHsgc3RhdGU6IGFjdGlvbiB9KTtcblxuICAgICAgYWN0aW9uID0ga2V5O1xuICAgICAga2V5ID0gYXJndW1lbnRzWzNdIHx8IGNyZWF0ZUtleSgpO1xuICAgIH1cblxuICAgIHJldHVybiBfY3JlYXRlTG9jYXRpb24zWydkZWZhdWx0J10obG9jYXRpb24sIGFjdGlvbiwga2V5KTtcbiAgfVxuXG4gIC8vIGRlcHJlY2F0ZWRcbiAgZnVuY3Rpb24gc2V0U3RhdGUoc3RhdGUpIHtcbiAgICBpZiAobG9jYXRpb24pIHtcbiAgICAgIHVwZGF0ZUxvY2F0aW9uU3RhdGUobG9jYXRpb24sIHN0YXRlKTtcbiAgICAgIHVwZGF0ZUxvY2F0aW9uKGxvY2F0aW9uKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdXBkYXRlTG9jYXRpb25TdGF0ZShnZXRDdXJyZW50TG9jYXRpb24oKSwgc3RhdGUpO1xuICAgIH1cbiAgfVxuXG4gIGZ1bmN0aW9uIHVwZGF0ZUxvY2F0aW9uU3RhdGUobG9jYXRpb24sIHN0YXRlKSB7XG4gICAgbG9jYXRpb24uc3RhdGUgPSBfZXh0ZW5kcyh7fSwgbG9jYXRpb24uc3RhdGUsIHN0YXRlKTtcbiAgICBzYXZlU3RhdGUobG9jYXRpb24ua2V5LCBsb2NhdGlvbi5zdGF0ZSk7XG4gIH1cblxuICAvLyBkZXByZWNhdGVkXG4gIGZ1bmN0aW9uIHJlZ2lzdGVyVHJhbnNpdGlvbkhvb2soaG9vaykge1xuICAgIGlmICh0cmFuc2l0aW9uSG9va3MuaW5kZXhPZihob29rKSA9PT0gLTEpIHRyYW5zaXRpb25Ib29rcy5wdXNoKGhvb2spO1xuICB9XG5cbiAgLy8gZGVwcmVjYXRlZFxuICBmdW5jdGlvbiB1bnJlZ2lzdGVyVHJhbnNpdGlvbkhvb2soaG9vaykge1xuICAgIHRyYW5zaXRpb25Ib29rcyA9IHRyYW5zaXRpb25Ib29rcy5maWx0ZXIoZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICAgIHJldHVybiBpdGVtICE9PSBob29rO1xuICAgIH0pO1xuICB9XG5cbiAgLy8gZGVwcmVjYXRlZFxuICBmdW5jdGlvbiBwdXNoU3RhdGUoc3RhdGUsIHBhdGgpIHtcbiAgICBpZiAodHlwZW9mIHBhdGggPT09ICdzdHJpbmcnKSBwYXRoID0gX3BhcnNlUGF0aDJbJ2RlZmF1bHQnXShwYXRoKTtcblxuICAgIHB1c2goX2V4dGVuZHMoeyBzdGF0ZTogc3RhdGUgfSwgcGF0aCkpO1xuICB9XG5cbiAgLy8gZGVwcmVjYXRlZFxuICBmdW5jdGlvbiByZXBsYWNlU3RhdGUoc3RhdGUsIHBhdGgpIHtcbiAgICBpZiAodHlwZW9mIHBhdGggPT09ICdzdHJpbmcnKSBwYXRoID0gX3BhcnNlUGF0aDJbJ2RlZmF1bHQnXShwYXRoKTtcblxuICAgIHJlcGxhY2UoX2V4dGVuZHMoeyBzdGF0ZTogc3RhdGUgfSwgcGF0aCkpO1xuICB9XG5cbiAgcmV0dXJuIHtcbiAgICBsaXN0ZW5CZWZvcmU6IGxpc3RlbkJlZm9yZSxcbiAgICBsaXN0ZW46IGxpc3RlbixcbiAgICB0cmFuc2l0aW9uVG86IHRyYW5zaXRpb25UbyxcbiAgICBwdXNoOiBwdXNoLFxuICAgIHJlcGxhY2U6IHJlcGxhY2UsXG4gICAgZ286IGdvLFxuICAgIGdvQmFjazogZ29CYWNrLFxuICAgIGdvRm9yd2FyZDogZ29Gb3J3YXJkLFxuICAgIGNyZWF0ZUtleTogY3JlYXRlS2V5LFxuICAgIGNyZWF0ZVBhdGg6IGNyZWF0ZVBhdGgsXG4gICAgY3JlYXRlSHJlZjogY3JlYXRlSHJlZixcbiAgICBjcmVhdGVMb2NhdGlvbjogY3JlYXRlTG9jYXRpb24sXG5cbiAgICBzZXRTdGF0ZTogX2RlcHJlY2F0ZTJbJ2RlZmF1bHQnXShzZXRTdGF0ZSwgJ3NldFN0YXRlIGlzIGRlcHJlY2F0ZWQ7IHVzZSBsb2NhdGlvbi5rZXkgdG8gc2F2ZSBzdGF0ZSBpbnN0ZWFkJyksXG4gICAgcmVnaXN0ZXJUcmFuc2l0aW9uSG9vazogX2RlcHJlY2F0ZTJbJ2RlZmF1bHQnXShyZWdpc3RlclRyYW5zaXRpb25Ib29rLCAncmVnaXN0ZXJUcmFuc2l0aW9uSG9vayBpcyBkZXByZWNhdGVkOyB1c2UgbGlzdGVuQmVmb3JlIGluc3RlYWQnKSxcbiAgICB1bnJlZ2lzdGVyVHJhbnNpdGlvbkhvb2s6IF9kZXByZWNhdGUyWydkZWZhdWx0J10odW5yZWdpc3RlclRyYW5zaXRpb25Ib29rLCAndW5yZWdpc3RlclRyYW5zaXRpb25Ib29rIGlzIGRlcHJlY2F0ZWQ7IHVzZSB0aGUgY2FsbGJhY2sgcmV0dXJuZWQgZnJvbSBsaXN0ZW5CZWZvcmUgaW5zdGVhZCcpLFxuICAgIHB1c2hTdGF0ZTogX2RlcHJlY2F0ZTJbJ2RlZmF1bHQnXShwdXNoU3RhdGUsICdwdXNoU3RhdGUgaXMgZGVwcmVjYXRlZDsgdXNlIHB1c2ggaW5zdGVhZCcpLFxuICAgIHJlcGxhY2VTdGF0ZTogX2RlcHJlY2F0ZTJbJ2RlZmF1bHQnXShyZXBsYWNlU3RhdGUsICdyZXBsYWNlU3RhdGUgaXMgZGVwcmVjYXRlZDsgdXNlIHJlcGxhY2UgaW5zdGVhZCcpXG4gIH07XG59XG5cbmV4cG9ydHNbJ2RlZmF1bHQnXSA9IGNyZWF0ZUhpc3Rvcnk7XG5tb2R1bGUuZXhwb3J0cyA9IGV4cG9ydHNbJ2RlZmF1bHQnXTsiLCIvL2ltcG9ydCB3YXJuaW5nIGZyb20gJ3dhcm5pbmcnXG4ndXNlIHN0cmljdCc7XG5cbmV4cG9ydHMuX19lc01vZHVsZSA9IHRydWU7XG5cbnZhciBfZXh0ZW5kcyA9IE9iamVjdC5hc3NpZ24gfHwgZnVuY3Rpb24gKHRhcmdldCkgeyBmb3IgKHZhciBpID0gMTsgaSA8IGFyZ3VtZW50cy5sZW5ndGg7IGkrKykgeyB2YXIgc291cmNlID0gYXJndW1lbnRzW2ldOyBmb3IgKHZhciBrZXkgaW4gc291cmNlKSB7IGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwoc291cmNlLCBrZXkpKSB7IHRhcmdldFtrZXldID0gc291cmNlW2tleV07IH0gfSB9IHJldHVybiB0YXJnZXQ7IH07XG5cbmZ1bmN0aW9uIF9pbnRlcm9wUmVxdWlyZURlZmF1bHQob2JqKSB7IHJldHVybiBvYmogJiYgb2JqLl9fZXNNb2R1bGUgPyBvYmogOiB7ICdkZWZhdWx0Jzogb2JqIH07IH1cblxudmFyIF9BY3Rpb25zID0gcmVxdWlyZSgnLi9BY3Rpb25zJyk7XG5cbnZhciBfcGFyc2VQYXRoID0gcmVxdWlyZSgnLi9wYXJzZVBhdGgnKTtcblxudmFyIF9wYXJzZVBhdGgyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfcGFyc2VQYXRoKTtcblxuZnVuY3Rpb24gY3JlYXRlTG9jYXRpb24oKSB7XG4gIHZhciBsb2NhdGlvbiA9IGFyZ3VtZW50cy5sZW5ndGggPD0gMCB8fCBhcmd1bWVudHNbMF0gPT09IHVuZGVmaW5lZCA/ICcvJyA6IGFyZ3VtZW50c1swXTtcbiAgdmFyIGFjdGlvbiA9IGFyZ3VtZW50cy5sZW5ndGggPD0gMSB8fCBhcmd1bWVudHNbMV0gPT09IHVuZGVmaW5lZCA/IF9BY3Rpb25zLlBPUCA6IGFyZ3VtZW50c1sxXTtcbiAgdmFyIGtleSA9IGFyZ3VtZW50cy5sZW5ndGggPD0gMiB8fCBhcmd1bWVudHNbMl0gPT09IHVuZGVmaW5lZCA/IG51bGwgOiBhcmd1bWVudHNbMl07XG5cbiAgdmFyIF9mb3VydGhBcmcgPSBhcmd1bWVudHMubGVuZ3RoIDw9IDMgfHwgYXJndW1lbnRzWzNdID09PSB1bmRlZmluZWQgPyBudWxsIDogYXJndW1lbnRzWzNdO1xuXG4gIGlmICh0eXBlb2YgbG9jYXRpb24gPT09ICdzdHJpbmcnKSBsb2NhdGlvbiA9IF9wYXJzZVBhdGgyWydkZWZhdWx0J10obG9jYXRpb24pO1xuXG4gIGlmICh0eXBlb2YgYWN0aW9uID09PSAnb2JqZWN0Jykge1xuICAgIC8vd2FybmluZyhcbiAgICAvLyAgZmFsc2UsXG4gICAgLy8gICdUaGUgc3RhdGUgKDJuZCkgYXJndW1lbnQgdG8gY3JlYXRlTG9jYXRpb24gaXMgZGVwcmVjYXRlZDsgdXNlIGEgJyArXG4gICAgLy8gICdsb2NhdGlvbiBkZXNjcmlwdG9yIGluc3RlYWQnXG4gICAgLy8pXG5cbiAgICBsb2NhdGlvbiA9IF9leHRlbmRzKHt9LCBsb2NhdGlvbiwgeyBzdGF0ZTogYWN0aW9uIH0pO1xuXG4gICAgYWN0aW9uID0ga2V5IHx8IF9BY3Rpb25zLlBPUDtcbiAgICBrZXkgPSBfZm91cnRoQXJnO1xuICB9XG5cbiAgdmFyIHBhdGhuYW1lID0gbG9jYXRpb24ucGF0aG5hbWUgfHwgJy8nO1xuICB2YXIgc2VhcmNoID0gbG9jYXRpb24uc2VhcmNoIHx8ICcnO1xuICB2YXIgaGFzaCA9IGxvY2F0aW9uLmhhc2ggfHwgJyc7XG4gIHZhciBzdGF0ZSA9IGxvY2F0aW9uLnN0YXRlIHx8IG51bGw7XG5cbiAgcmV0dXJuIHtcbiAgICBwYXRobmFtZTogcGF0aG5hbWUsXG4gICAgc2VhcmNoOiBzZWFyY2gsXG4gICAgaGFzaDogaGFzaCxcbiAgICBzdGF0ZTogc3RhdGUsXG4gICAgYWN0aW9uOiBhY3Rpb24sXG4gICAga2V5OiBrZXlcbiAgfTtcbn1cblxuZXhwb3J0c1snZGVmYXVsdCddID0gY3JlYXRlTG9jYXRpb247XG5tb2R1bGUuZXhwb3J0cyA9IGV4cG9ydHNbJ2RlZmF1bHQnXTsiLCIvL2ltcG9ydCB3YXJuaW5nIGZyb20gJ3dhcm5pbmcnXG5cblwidXNlIHN0cmljdFwiO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuZnVuY3Rpb24gZGVwcmVjYXRlKGZuKSB7XG4gIHJldHVybiBmbjtcbiAgLy9yZXR1cm4gZnVuY3Rpb24gKCkge1xuICAvLyAgd2FybmluZyhmYWxzZSwgJ1toaXN0b3J5XSAnICsgbWVzc2FnZSlcbiAgLy8gIHJldHVybiBmbi5hcHBseSh0aGlzLCBhcmd1bWVudHMpXG4gIC8vfVxufVxuXG5leHBvcnRzW1wiZGVmYXVsdFwiXSA9IGRlcHJlY2F0ZTtcbm1vZHVsZS5leHBvcnRzID0gZXhwb3J0c1tcImRlZmF1bHRcIl07IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbmV4cG9ydHMuX19lc01vZHVsZSA9IHRydWU7XG5mdW5jdGlvbiBleHRyYWN0UGF0aChzdHJpbmcpIHtcbiAgdmFyIG1hdGNoID0gc3RyaW5nLm1hdGNoKC9eaHR0cHM/OlxcL1xcL1teXFwvXSovKTtcblxuICBpZiAobWF0Y2ggPT0gbnVsbCkgcmV0dXJuIHN0cmluZztcblxuICByZXR1cm4gc3RyaW5nLnN1YnN0cmluZyhtYXRjaFswXS5sZW5ndGgpO1xufVxuXG5leHBvcnRzW1wiZGVmYXVsdFwiXSA9IGV4dHJhY3RQYXRoO1xubW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzW1wiZGVmYXVsdFwiXTsiLCIndXNlIHN0cmljdCc7XG5cbmV4cG9ydHMuX19lc01vZHVsZSA9IHRydWU7XG5cbmZ1bmN0aW9uIF9pbnRlcm9wUmVxdWlyZURlZmF1bHQob2JqKSB7IHJldHVybiBvYmogJiYgb2JqLl9fZXNNb2R1bGUgPyBvYmogOiB7ICdkZWZhdWx0Jzogb2JqIH07IH1cblxudmFyIF93YXJuaW5nID0gcmVxdWlyZSgnd2FybmluZycpO1xuXG52YXIgX3dhcm5pbmcyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfd2FybmluZyk7XG5cbnZhciBfZXh0cmFjdFBhdGggPSByZXF1aXJlKCcuL2V4dHJhY3RQYXRoJyk7XG5cbnZhciBfZXh0cmFjdFBhdGgyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfZXh0cmFjdFBhdGgpO1xuXG5mdW5jdGlvbiBwYXJzZVBhdGgocGF0aCkge1xuICB2YXIgcGF0aG5hbWUgPSBfZXh0cmFjdFBhdGgyWydkZWZhdWx0J10ocGF0aCk7XG4gIHZhciBzZWFyY2ggPSAnJztcbiAgdmFyIGhhc2ggPSAnJztcblxuICBwcm9jZXNzLmVudi5OT0RFX0VOViAhPT0gJ3Byb2R1Y3Rpb24nID8gX3dhcm5pbmcyWydkZWZhdWx0J10ocGF0aCA9PT0gcGF0aG5hbWUsICdBIHBhdGggbXVzdCBiZSBwYXRobmFtZSArIHNlYXJjaCArIGhhc2ggb25seSwgbm90IGEgZnVsbHkgcXVhbGlmaWVkIFVSTCBsaWtlIFwiJXNcIicsIHBhdGgpIDogdW5kZWZpbmVkO1xuXG4gIHZhciBoYXNoSW5kZXggPSBwYXRobmFtZS5pbmRleE9mKCcjJyk7XG4gIGlmIChoYXNoSW5kZXggIT09IC0xKSB7XG4gICAgaGFzaCA9IHBhdGhuYW1lLnN1YnN0cmluZyhoYXNoSW5kZXgpO1xuICAgIHBhdGhuYW1lID0gcGF0aG5hbWUuc3Vic3RyaW5nKDAsIGhhc2hJbmRleCk7XG4gIH1cblxuICB2YXIgc2VhcmNoSW5kZXggPSBwYXRobmFtZS5pbmRleE9mKCc/Jyk7XG4gIGlmIChzZWFyY2hJbmRleCAhPT0gLTEpIHtcbiAgICBzZWFyY2ggPSBwYXRobmFtZS5zdWJzdHJpbmcoc2VhcmNoSW5kZXgpO1xuICAgIHBhdGhuYW1lID0gcGF0aG5hbWUuc3Vic3RyaW5nKDAsIHNlYXJjaEluZGV4KTtcbiAgfVxuXG4gIGlmIChwYXRobmFtZSA9PT0gJycpIHBhdGhuYW1lID0gJy8nO1xuXG4gIHJldHVybiB7XG4gICAgcGF0aG5hbWU6IHBhdGhuYW1lLFxuICAgIHNlYXJjaDogc2VhcmNoLFxuICAgIGhhc2g6IGhhc2hcbiAgfTtcbn1cblxuZXhwb3J0c1snZGVmYXVsdCddID0gcGFyc2VQYXRoO1xubW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzWydkZWZhdWx0J107IiwiJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuXG5mdW5jdGlvbiBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KG9iaikgeyByZXR1cm4gb2JqICYmIG9iai5fX2VzTW9kdWxlID8gb2JqIDogeyAnZGVmYXVsdCc6IG9iaiB9OyB9XG5cbnZhciBfd2FybmluZyA9IHJlcXVpcmUoJ3dhcm5pbmcnKTtcblxudmFyIF93YXJuaW5nMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX3dhcm5pbmcpO1xuXG5mdW5jdGlvbiBydW5UcmFuc2l0aW9uSG9vayhob29rLCBsb2NhdGlvbiwgY2FsbGJhY2spIHtcbiAgdmFyIHJlc3VsdCA9IGhvb2sobG9jYXRpb24sIGNhbGxiYWNrKTtcblxuICBpZiAoaG9vay5sZW5ndGggPCAyKSB7XG4gICAgLy8gQXNzdW1lIHRoZSBob29rIHJ1bnMgc3luY2hyb25vdXNseSBhbmQgYXV0b21hdGljYWxseVxuICAgIC8vIGNhbGwgdGhlIGNhbGxiYWNrIHdpdGggdGhlIHJldHVybiB2YWx1ZS5cbiAgICBjYWxsYmFjayhyZXN1bHQpO1xuICB9IGVsc2Uge1xuICAgIHByb2Nlc3MuZW52Lk5PREVfRU5WICE9PSAncHJvZHVjdGlvbicgPyBfd2FybmluZzJbJ2RlZmF1bHQnXShyZXN1bHQgPT09IHVuZGVmaW5lZCwgJ1lvdSBzaG91bGQgbm90IFwicmV0dXJuXCIgaW4gYSB0cmFuc2l0aW9uIGhvb2sgd2l0aCBhIGNhbGxiYWNrIGFyZ3VtZW50OyBjYWxsIHRoZSBjYWxsYmFjayBpbnN0ZWFkJykgOiB1bmRlZmluZWQ7XG4gIH1cbn1cblxuZXhwb3J0c1snZGVmYXVsdCddID0gcnVuVHJhbnNpdGlvbkhvb2s7XG5tb2R1bGUuZXhwb3J0cyA9IGV4cG9ydHNbJ2RlZmF1bHQnXTsiLCIvKipcbiAqIENvcHlyaWdodCAyMDEzLTIwMTUsIEZhY2Vib29rLCBJbmMuXG4gKiBBbGwgcmlnaHRzIHJlc2VydmVkLlxuICpcbiAqIFRoaXMgc291cmNlIGNvZGUgaXMgbGljZW5zZWQgdW5kZXIgdGhlIEJTRC1zdHlsZSBsaWNlbnNlIGZvdW5kIGluIHRoZVxuICogTElDRU5TRSBmaWxlIGluIHRoZSByb290IGRpcmVjdG9yeSBvZiB0aGlzIHNvdXJjZSB0cmVlLiBBbiBhZGRpdGlvbmFsIGdyYW50XG4gKiBvZiBwYXRlbnQgcmlnaHRzIGNhbiBiZSBmb3VuZCBpbiB0aGUgUEFURU5UUyBmaWxlIGluIHRoZSBzYW1lIGRpcmVjdG9yeS5cbiAqL1xuXG4ndXNlIHN0cmljdCc7XG5cbi8qKlxuICogVXNlIGludmFyaWFudCgpIHRvIGFzc2VydCBzdGF0ZSB3aGljaCB5b3VyIHByb2dyYW0gYXNzdW1lcyB0byBiZSB0cnVlLlxuICpcbiAqIFByb3ZpZGUgc3ByaW50Zi1zdHlsZSBmb3JtYXQgKG9ubHkgJXMgaXMgc3VwcG9ydGVkKSBhbmQgYXJndW1lbnRzXG4gKiB0byBwcm92aWRlIGluZm9ybWF0aW9uIGFib3V0IHdoYXQgYnJva2UgYW5kIHdoYXQgeW91IHdlcmVcbiAqIGV4cGVjdGluZy5cbiAqXG4gKiBUaGUgaW52YXJpYW50IG1lc3NhZ2Ugd2lsbCBiZSBzdHJpcHBlZCBpbiBwcm9kdWN0aW9uLCBidXQgdGhlIGludmFyaWFudFxuICogd2lsbCByZW1haW4gdG8gZW5zdXJlIGxvZ2ljIGRvZXMgbm90IGRpZmZlciBpbiBwcm9kdWN0aW9uLlxuICovXG5cbnZhciBpbnZhcmlhbnQgPSBmdW5jdGlvbihjb25kaXRpb24sIGZvcm1hdCwgYSwgYiwgYywgZCwgZSwgZikge1xuICBpZiAocHJvY2Vzcy5lbnYuTk9ERV9FTlYgIT09ICdwcm9kdWN0aW9uJykge1xuICAgIGlmIChmb3JtYXQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdpbnZhcmlhbnQgcmVxdWlyZXMgYW4gZXJyb3IgbWVzc2FnZSBhcmd1bWVudCcpO1xuICAgIH1cbiAgfVxuXG4gIGlmICghY29uZGl0aW9uKSB7XG4gICAgdmFyIGVycm9yO1xuICAgIGlmIChmb3JtYXQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgZXJyb3IgPSBuZXcgRXJyb3IoXG4gICAgICAgICdNaW5pZmllZCBleGNlcHRpb24gb2NjdXJyZWQ7IHVzZSB0aGUgbm9uLW1pbmlmaWVkIGRldiBlbnZpcm9ubWVudCAnICtcbiAgICAgICAgJ2ZvciB0aGUgZnVsbCBlcnJvciBtZXNzYWdlIGFuZCBhZGRpdGlvbmFsIGhlbHBmdWwgd2FybmluZ3MuJ1xuICAgICAgKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdmFyIGFyZ3MgPSBbYSwgYiwgYywgZCwgZSwgZl07XG4gICAgICB2YXIgYXJnSW5kZXggPSAwO1xuICAgICAgZXJyb3IgPSBuZXcgRXJyb3IoXG4gICAgICAgIGZvcm1hdC5yZXBsYWNlKC8lcy9nLCBmdW5jdGlvbigpIHsgcmV0dXJuIGFyZ3NbYXJnSW5kZXgrK107IH0pXG4gICAgICApO1xuICAgICAgZXJyb3IubmFtZSA9ICdJbnZhcmlhbnQgVmlvbGF0aW9uJztcbiAgICB9XG5cbiAgICBlcnJvci5mcmFtZXNUb1BvcCA9IDE7IC8vIHdlIGRvbid0IGNhcmUgYWJvdXQgaW52YXJpYW50J3Mgb3duIGZyYW1lXG4gICAgdGhyb3cgZXJyb3I7XG4gIH1cbn07XG5cbm1vZHVsZS5leHBvcnRzID0gaW52YXJpYW50O1xuIiwiLyoqXG4gKiBDb3B5cmlnaHQgMjAxNC0yMDE1LCBGYWNlYm9vaywgSW5jLlxuICogQWxsIHJpZ2h0cyByZXNlcnZlZC5cbiAqXG4gKiBUaGlzIHNvdXJjZSBjb2RlIGlzIGxpY2Vuc2VkIHVuZGVyIHRoZSBCU0Qtc3R5bGUgbGljZW5zZSBmb3VuZCBpbiB0aGVcbiAqIExJQ0VOU0UgZmlsZSBpbiB0aGUgcm9vdCBkaXJlY3Rvcnkgb2YgdGhpcyBzb3VyY2UgdHJlZS4gQW4gYWRkaXRpb25hbCBncmFudFxuICogb2YgcGF0ZW50IHJpZ2h0cyBjYW4gYmUgZm91bmQgaW4gdGhlIFBBVEVOVFMgZmlsZSBpbiB0aGUgc2FtZSBkaXJlY3RvcnkuXG4gKi9cblxuJ3VzZSBzdHJpY3QnO1xuXG4vKipcbiAqIFNpbWlsYXIgdG8gaW52YXJpYW50IGJ1dCBvbmx5IGxvZ3MgYSB3YXJuaW5nIGlmIHRoZSBjb25kaXRpb24gaXMgbm90IG1ldC5cbiAqIFRoaXMgY2FuIGJlIHVzZWQgdG8gbG9nIGlzc3VlcyBpbiBkZXZlbG9wbWVudCBlbnZpcm9ubWVudHMgaW4gY3JpdGljYWxcbiAqIHBhdGhzLiBSZW1vdmluZyB0aGUgbG9nZ2luZyBjb2RlIGZvciBwcm9kdWN0aW9uIGVudmlyb25tZW50cyB3aWxsIGtlZXAgdGhlXG4gKiBzYW1lIGxvZ2ljIGFuZCBmb2xsb3cgdGhlIHNhbWUgY29kZSBwYXRocy5cbiAqL1xuXG52YXIgd2FybmluZyA9IGZ1bmN0aW9uKCkge307XG5cbmlmIChwcm9jZXNzLmVudi5OT0RFX0VOViAhPT0gJ3Byb2R1Y3Rpb24nKSB7XG4gIHdhcm5pbmcgPSBmdW5jdGlvbihjb25kaXRpb24sIGZvcm1hdCwgYXJncykge1xuICAgIHZhciBsZW4gPSBhcmd1bWVudHMubGVuZ3RoO1xuICAgIGFyZ3MgPSBuZXcgQXJyYXkobGVuID4gMiA/IGxlbiAtIDIgOiAwKTtcbiAgICBmb3IgKHZhciBrZXkgPSAyOyBrZXkgPCBsZW47IGtleSsrKSB7XG4gICAgICBhcmdzW2tleSAtIDJdID0gYXJndW1lbnRzW2tleV07XG4gICAgfVxuICAgIGlmIChmb3JtYXQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFxuICAgICAgICAnYHdhcm5pbmcoY29uZGl0aW9uLCBmb3JtYXQsIC4uLmFyZ3MpYCByZXF1aXJlcyBhIHdhcm5pbmcgJyArXG4gICAgICAgICdtZXNzYWdlIGFyZ3VtZW50J1xuICAgICAgKTtcbiAgICB9XG5cbiAgICBpZiAoZm9ybWF0Lmxlbmd0aCA8IDEwIHx8ICgvXltzXFxXXSokLykudGVzdChmb3JtYXQpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoXG4gICAgICAgICdUaGUgd2FybmluZyBmb3JtYXQgc2hvdWxkIGJlIGFibGUgdG8gdW5pcXVlbHkgaWRlbnRpZnkgdGhpcyAnICtcbiAgICAgICAgJ3dhcm5pbmcuIFBsZWFzZSwgdXNlIGEgbW9yZSBkZXNjcmlwdGl2ZSBmb3JtYXQgdGhhbjogJyArIGZvcm1hdFxuICAgICAgKTtcbiAgICB9XG5cbiAgICBpZiAoIWNvbmRpdGlvbikge1xuICAgICAgdmFyIGFyZ0luZGV4ID0gMDtcbiAgICAgIHZhciBtZXNzYWdlID0gJ1dhcm5pbmc6ICcgK1xuICAgICAgICBmb3JtYXQucmVwbGFjZSgvJXMvZywgZnVuY3Rpb24oKSB7XG4gICAgICAgICAgcmV0dXJuIGFyZ3NbYXJnSW5kZXgrK107XG4gICAgICAgIH0pO1xuICAgICAgaWYgKHR5cGVvZiBjb25zb2xlICE9PSAndW5kZWZpbmVkJykge1xuICAgICAgICBjb25zb2xlLmVycm9yKG1lc3NhZ2UpO1xuICAgICAgfVxuICAgICAgdHJ5IHtcbiAgICAgICAgLy8gVGhpcyBlcnJvciB3YXMgdGhyb3duIGFzIGEgY29udmVuaWVuY2Ugc28gdGhhdCB5b3UgY2FuIHVzZSB0aGlzIHN0YWNrXG4gICAgICAgIC8vIHRvIGZpbmQgdGhlIGNhbGxzaXRlIHRoYXQgY2F1c2VkIHRoaXMgd2FybmluZyB0byBmaXJlLlxuICAgICAgICB0aHJvdyBuZXcgRXJyb3IobWVzc2FnZSk7XG4gICAgICB9IGNhdGNoKHgpIHt9XG4gICAgfVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHdhcm5pbmc7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlZnJlc2goKSB7XG4gICAgd2luZG93LmxvY2F0aW9uLnJlbG9hZCgpO1xuICB9XG5cbiAgZ2V0TWVzc2FnZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5zaWduZWRJbikge1xuICAgICAgcmV0dXJuIGludGVycG9sYXRlKFxuICAgICAgICBnZXR0ZXh0KFwiWW91IGhhdmUgc2lnbmVkIGluIGFzICUodXNlcm5hbWUpcy4gUGxlYXNlIHJlZnJlc2ggdGhlIHBhZ2UgYmVmb3JlIGNvbnRpbnVpbmcuXCIpLFxuICAgICAgICB7dXNlcm5hbWU6IHRoaXMucHJvcHMuc2lnbmVkSW4udXNlcm5hbWV9LCB0cnVlKTtcbiAgICB9IGVsc2UgaWYgKHRoaXMucHJvcHMuc2lnbmVkT3V0KSB7XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUoXG4gICAgICAgIGdldHRleHQoXCIlKHVzZXJuYW1lKXMsIHlvdSBoYXZlIGJlZW4gc2lnbmVkIG91dC4gUGxlYXNlIHJlZnJlc2ggdGhlIHBhZ2UgYmVmb3JlIGNvbnRpbnVpbmcuXCIpLFxuICAgICAgICB7dXNlcm5hbWU6IHRoaXMucHJvcHMudXNlci51c2VybmFtZX0sIHRydWUpO1xuICAgIH1cbiAgfVxuXG4gIGdldENsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5zaWduZWRJbiB8fCB0aGlzLnByb3BzLnNpZ25lZE91dCkge1xuICAgICAgcmV0dXJuIFwiYXV0aC1tZXNzYWdlIHNob3dcIjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIFwiYXV0aC1tZXNzYWdlXCI7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9e3RoaXMuZ2V0Q2xhc3NOYW1lKCl9PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cbiAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPnt0aGlzLmdldE1lc3NhZ2UoKX08L3A+XG4gICAgICAgIDxwPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBidG4tZGVmYXVsdFwiXG4gICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnJlZnJlc2h9PlxuICAgICAgICAgICAge2dldHRleHQoXCJSZWxvYWQgcGFnZVwiKX1cbiAgICAgICAgICA8L2J1dHRvbj4gPHNwYW4gY2xhc3NOYW1lPVwiaGlkZGVuLXhzIGhpZGRlbi1zbSB0ZXh0LW11dGVkXCI+XG4gICAgICAgICAgICB7Z2V0dGV4dChcIm9yIHByZXNzIEY1IGtleS5cIil9XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICA8L3A+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0KHN0YXRlKSB7XG4gIHJldHVybiB7XG4gICAgdXNlcjogc3RhdGUuYXV0aC51c2VyLFxuICAgIHNpZ25lZEluOiBzdGF0ZS5hdXRoLnNpZ25lZEluLFxuICAgIHNpZ25lZE91dDogc3RhdGUuYXV0aC5zaWduZWRPdXRcbiAgfTtcbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5jb25zdCBCQVNFX1VSTCA9ICQoJ2Jhc2UnKS5hdHRyKCdocmVmJykgKyAndXNlci1hdmF0YXIvJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRTcmMoKSB7XG4gICAgbGV0IHNpemUgPSB0aGlzLnByb3BzLnNpemUgfHwgMTAwOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbiAgICBsZXQgdXJsID0gQkFTRV9VUkw7XG5cbiAgICBpZiAodGhpcy5wcm9wcy51c2VyICYmIHRoaXMucHJvcHMudXNlci5pZCkge1xuICAgICAgLy8ganVzdCBhdmF0YXIgaGFzaCwgc2l6ZSBhbmQgdXNlciBpZFxuICAgICAgdXJsICs9IHRoaXMucHJvcHMudXNlci5hdmF0YXJfaGFzaCArICcvJyArIHNpemUgKyAnLycgKyB0aGlzLnByb3BzLnVzZXIuaWQgKyAnLnBuZyc7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIGp1c3QgYXBwZW5kIGF2YXRhciBzaXplIHRvIGZpbGUgdG8gcHJvZHVjZSBuby1hdmF0YXIgcGxhY2Vob2xkZXJcbiAgICAgIHVybCArPSBzaXplICsgJy5wbmcnO1xuICAgIH1cblxuICAgIHJldHVybiB1cmw7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8aW1nIHNyYz17dGhpcy5nZXRTcmMoKX1cbiAgICAgICAgICAgICAgICBjbGFzc05hbWU9e3RoaXMucHJvcHMuY2xhc3NOYW1lIHx8ICd1c2VyLWF2YXRhcid9XG4gICAgICAgICAgICAgICAgdGl0bGU9e2dldHRleHQoXCJVc2VyIGF2YXRhclwiKX0vPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgbW9tZW50IGZyb20gJ21vbWVudCc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldFJlYXNvbk1lc3NhZ2UoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGlmICh0aGlzLnByb3BzLm1lc3NhZ2UuaHRtbCkge1xuICAgICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibGVhZFwiXG4gICAgICAgICAgICAgICAgICBkYW5nZXJvdXNseVNldElubmVySFRNTD17e19faHRtbDogdGhpcy5wcm9wcy5tZXNzYWdlLmh0bWx9fSAvPjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIDxwIGNsYXNzTmFtZT1cImxlYWRcIj57dGhpcy5wcm9wcy5tZXNzYWdlLnBsYWlufTwvcD47XG4gICAgfVxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cblxuICBnZXRFeHBpcmF0aW9uTWVzc2FnZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5leHBpcmVzKSB7XG4gICAgICBpZiAodGhpcy5wcm9wcy5leHBpcmVzLmlzQWZ0ZXIobW9tZW50KCkpKSB7XG4gICAgICAgIHJldHVybiBpbnRlcnBvbGF0ZShcbiAgICAgICAgICBnZXR0ZXh0KFwiVGhpcyBiYW4gZXhwaXJlcyAlKGV4cGlyZXNfb24pcy5cIiksXG4gICAgICAgICAgeydleHBpcmVzX29uJzogdGhpcy5wcm9wcy5leHBpcmVzLmZyb21Ob3coKX0sXG4gICAgICAgICAgdHJ1ZSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gZ2V0dGV4dChcIlRoaXMgYmFuIGhhcyBleHBpcmVkLlwiKTtcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCJUaGlzIGJhbiBpcyBwZXJtYW5lbnQuXCIpO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwicGFnZSBwYWdlLWVycm9yIHBhZ2UtZXJyb3ItYmFubmVkXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtcGFuZWxcIj5cblxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+aGlnaGxpZ2h0X29mZjwvc3Bhbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgICAge3RoaXMuZ2V0UmVhc29uTWVzc2FnZSgpfVxuICAgICAgICAgICAgPHAgY2xhc3NOYW1lPVwibWVzc2FnZS1mb290bm90ZVwiPlxuICAgICAgICAgICAgICB7dGhpcy5nZXRFeHBpcmF0aW9uTWVzc2FnZSgpfVxuICAgICAgICAgICAgPC9wPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IExvYWRlciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9sb2FkZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgQnV0dG9uIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIGxldCBjbGFzc05hbWUgPSAnYnRuICcgKyB0aGlzLnByb3BzLmNsYXNzTmFtZTtcbiAgICBsZXQgZGlzYWJsZWQgPSB0aGlzLnByb3BzLmRpc2FibGVkO1xuXG4gICAgaWYgKHRoaXMucHJvcHMubG9hZGluZykge1xuICAgICAgY2xhc3NOYW1lICs9ICcgYnRuLWxvYWRpbmcnO1xuICAgICAgZGlzYWJsZWQgPSB0cnVlO1xuICAgIH1cblxuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGJ1dHRvbiB0eXBlPXt0aGlzLnByb3BzLm9uQ2xpY2sgPyAnYnV0dG9uJyA6ICdzdWJtaXQnfVxuICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17Y2xhc3NOYW1lfVxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXtkaXNhYmxlZH1cbiAgICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnByb3BzLm9uQ2xpY2t9PlxuICAgICAge3RoaXMucHJvcHMuY2hpbGRyZW59XG4gICAgICB7dGhpcy5wcm9wcy5sb2FkaW5nID8gPExvYWRlciAvPiA6IG51bGx9XG4gICAgPC9idXR0b24+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuXG5CdXR0b24uZGVmYXVsdFByb3BzID0ge1xuICBjbGFzc05hbWU6IFwiYnRuLWRlZmF1bHRcIixcblxuICB0eXBlOiBcInN1Ym1pdFwiLFxuXG4gIGxvYWRpbmc6IGZhbHNlLFxuICBkaXNhYmxlZDogZmFsc2UsXG5cbiAgb25DbGljazogbnVsbFxufTtcbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgQXZhdGFyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2F2YXRhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmNvbnN0IEJBU0VfVVJMID0gJCgnYmFzZScpLmF0dHIoJ2hyZWYnKSArICd1c2VyLWF2YXRhcic7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIGdldEF2YXRhclNpemUoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMudXBsb2FkKSB7XG4gICAgICByZXR1cm4gdGhpcy5wcm9wcy5vcHRpb25zLmNyb3BfdG1wLnNpemU7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLnByb3BzLm9wdGlvbnMuY3JvcF9vcmcuc2l6ZTtcbiAgICB9XG4gIH1cblxuICBnZXRBdmF0YXJTZWNyZXQoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMudXBsb2FkKSB7XG4gICAgICByZXR1cm4gdGhpcy5wcm9wcy5vcHRpb25zLmNyb3BfdG1wLnNlY3JldDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHRoaXMucHJvcHMub3B0aW9ucy5jcm9wX29yZy5zZWNyZXQ7XG4gICAgfVxuICB9XG5cbiAgZ2V0QXZhdGFySGFzaCgpIHtcbiAgICByZXR1cm4gdGhpcy5wcm9wcy51cGxvYWQgfHwgdGhpcy5wcm9wcy51c2VyLmF2YXRhcl9oYXNoO1xuICB9XG5cbiAgZ2V0SW1hZ2VQYXRoKCkge1xuICAgIHJldHVybiBbXG4gICAgICBCQVNFX1VSTCxcbiAgICAgIHRoaXMuZ2V0QXZhdGFyU2VjcmV0KCkgKyAnOicgKyB0aGlzLmdldEF2YXRhckhhc2goKSxcbiAgICAgIHRoaXMucHJvcHMudXNlci5pZCArICcucG5nJ1xuICAgIF0uam9pbignLycpO1xuICB9XG5cbiAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgbGV0IGNyb3BpdCA9ICQoJy5jcm9wLWZvcm0nKTtcbiAgICBjcm9waXQud2lkdGgodGhpcy5nZXRBdmF0YXJTaXplKCkpO1xuXG4gICAgY3JvcGl0LmNyb3BpdCh7XG4gICAgICAnd2lkdGgnOiB0aGlzLmdldEF2YXRhclNpemUoKSxcbiAgICAgICdoZWlnaHQnOiB0aGlzLmdldEF2YXRhclNpemUoKSxcbiAgICAgICdpbWFnZVN0YXRlJzoge1xuICAgICAgICAnc3JjJzogdGhpcy5nZXRJbWFnZVBhdGgoKVxuICAgICAgfSxcbiAgICAgIG9uSW1hZ2VMb2FkZWQ6ICgpID0+IHtcbiAgICAgICAgaWYgKHRoaXMucHJvcHMudXBsb2FkKSB7XG4gICAgICAgICAgLy8gY2VudGVyIHVwbG9hZGVkIGltYWdlXG4gICAgICAgICAgbGV0IHpvb21MZXZlbCA9IGNyb3BpdC5jcm9waXQoJ3pvb20nKTtcbiAgICAgICAgICBsZXQgaW1hZ2VTaXplID0gY3JvcGl0LmNyb3BpdCgnaW1hZ2VTaXplJyk7XG5cbiAgICAgICAgICAvLyBpcyBpdCB3aWRlciB0aGFuIHRhbGxlcj9cbiAgICAgICAgICBpZiAoaW1hZ2VTaXplLndpZHRoID4gaW1hZ2VTaXplLmhlaWdodCkge1xuICAgICAgICAgICAgbGV0IGRpc3BsYXllZFdpZHRoID0gKGltYWdlU2l6ZS53aWR0aCAqIHpvb21MZXZlbCk7XG4gICAgICAgICAgICBsZXQgb2Zmc2V0WCA9IChkaXNwbGF5ZWRXaWR0aCAtIHRoaXMuZ2V0QXZhdGFyU2l6ZSgpKSAvIC0yO1xuXG4gICAgICAgICAgICBjcm9waXQuY3JvcGl0KCdvZmZzZXQnLCB7XG4gICAgICAgICAgICAgICd4Jzogb2Zmc2V0WCxcbiAgICAgICAgICAgICAgJ3knOiAwXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9IGVsc2UgaWYgKGltYWdlU2l6ZS53aWR0aCA8IGltYWdlU2l6ZS5oZWlnaHQpIHtcbiAgICAgICAgICAgIGxldCBkaXNwbGF5ZWRIZWlnaHQgPSAoaW1hZ2VTaXplLmhlaWdodCAqIHpvb21MZXZlbCk7XG4gICAgICAgICAgICBsZXQgb2Zmc2V0WSA9IChkaXNwbGF5ZWRIZWlnaHQgLSB0aGlzLmdldEF2YXRhclNpemUoKSkgLyAtMjtcblxuICAgICAgICAgICAgY3JvcGl0LmNyb3BpdCgnb2Zmc2V0Jywge1xuICAgICAgICAgICAgICAneCc6IDAsXG4gICAgICAgICAgICAgICd5Jzogb2Zmc2V0WVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIC8vIHVzZSBwcmVzZXJ2ZWQgY3JvcFxuICAgICAgICAgIGxldCBjcm9wID0gdGhpcy5wcm9wcy5vcHRpb25zLmNyb3Bfb3JnLmNyb3A7XG4gICAgICAgICAgaWYgKGNyb3ApIHtcbiAgICAgICAgICAgIGNyb3BpdC5jcm9waXQoJ3pvb20nLCBjcm9wLnpvb20pO1xuICAgICAgICAgICAgY3JvcGl0LmNyb3BpdCgnb2Zmc2V0Jywge1xuICAgICAgICAgICAgICAneCc6IGNyb3AueCxcbiAgICAgICAgICAgICAgJ3knOiBjcm9wLnlcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgY29tcG9uZW50V2lsbFVubW91bnQoKSB7XG4gICAgJCgnLmNyb3AtZm9ybScpLmNyb3BpdCgnZGlzYWJsZScpO1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBjcm9wQXZhdGFyID0gKCkgPT4ge1xuICAgIGlmICh0aGlzLnN0YXRlLmlzTG9hZGluZykge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ2lzTG9hZGluZyc6IHRydWVcbiAgICB9KTtcblxuICAgIGxldCBhdmF0YXJUeXBlID0gdGhpcy5wcm9wcy51cGxvYWQgPyAnY3JvcF90bXAnIDogJ2Nyb3Bfb3JnJztcbiAgICBsZXQgY3JvcGl0ID0gJCgnLmNyb3AtZm9ybScpO1xuXG4gICAgYWpheC5wb3N0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLmF2YXRhciwge1xuICAgICAgJ2F2YXRhcic6IGF2YXRhclR5cGUsXG4gICAgICAnY3JvcCc6IHtcbiAgICAgICAgJ29mZnNldCc6IGNyb3BpdC5jcm9waXQoJ29mZnNldCcpLFxuICAgICAgICAnem9vbSc6IGNyb3BpdC5jcm9waXQoJ3pvb20nKVxuICAgICAgfVxuICAgIH0pLnRoZW4oKGRhdGEpID0+IHtcbiAgICAgIHRoaXMucHJvcHMub25Db21wbGV0ZShkYXRhLmF2YXRhcl9oYXNoLCBkYXRhLm9wdGlvbnMpO1xuICAgICAgc25hY2tiYXIuc3VjY2VzcyhkYXRhLmRldGFpbCk7XG4gICAgfSwgKHJlamVjdGlvbikgPT4ge1xuICAgICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMCkge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlXG4gICAgICAgIH0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgdGhpcy5wcm9wcy5zaG93RXJyb3IocmVqZWN0aW9uKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5IG1vZGFsLWF2YXRhci1jcm9wXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY3JvcC1mb3JtXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjcm9waXQtaW1hZ2UtcHJldmlld1wiPjwvZGl2PlxuICAgICAgICAgIDxpbnB1dCB0eXBlPVwicmFuZ2VcIiBjbGFzc05hbWU9XCJjcm9waXQtaW1hZ2Utem9vbS1pbnB1dFwiIC8+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWZvb3RlclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1tZC02IGNvbC1tZC1vZmZzZXQtM1wiPlxuXG4gICAgICAgICAgPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLmNyb3BBdmF0YXJ9XG4gICAgICAgICAgICAgICAgICBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAge3RoaXMucHJvcHMudXBsb2FkID8gZ2V0dGV4dChcIlNldCBhdmF0YXJcIilcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA6IGdldHRleHQoXCJDcm9wIGltYWdlXCIpfVxuICAgICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICAgICAgPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnByb3BzLnNob3dJbmRleH1cbiAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAge2dldHRleHQoXCJDYW5jZWxcIil9XG4gICAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgQnV0dG9uIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2J1dHRvbic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgYmF0Y2ggZnJvbSAnbWlzYWdvL3V0aWxzL2JhdGNoJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBjbGFzcyBHYWxsZXJ5SXRlbSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgc2VsZWN0ID0gKCkgPT4ge1xuICAgIHRoaXMucHJvcHMuc2VsZWN0KHRoaXMucHJvcHMuaW1hZ2UpO1xuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIGdldENsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5zZWxlY3Rpb24gPT09IHRoaXMucHJvcHMuaW1hZ2UpIHtcbiAgICAgIGlmICh0aGlzLnByb3BzLmRpc2FibGVkKSB7XG4gICAgICAgIHJldHVybiAnYnRuIGJ0bi1hdmF0YXIgYnRuLWRpc2FibGVkIGF2YXRhci1zZWxlY3RlZCc7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gJ2J0biBidG4tYXZhdGFyIGF2YXRhci1zZWxlY3RlZCc7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLmRpc2FibGVkKSB7XG4gICAgICByZXR1cm4gJ2J0biBidG4tYXZhdGFyIGJ0bi1kaXNhYmxlZCc7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiAnYnRuIGJ0bi1hdmF0YXInO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxidXR0b24gdHlwZT1cImJ1dHRvblwiXG4gICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPXt0aGlzLmdldENsYXNzTmFtZSgpfVxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnByb3BzLmRpc2FibGVkfVxuICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMuc2VsZWN0fT5cbiAgICAgIDxpbWcgc3JjPXttaXNhZ28uZ2V0KCdNRURJQV9VUkwnKSArIHRoaXMucHJvcHMuaW1hZ2V9IC8+XG4gICAgPC9idXR0b24+XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgR2FsbGVyeSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiYXZhdGFycy1nYWxsZXJ5XCI+XG4gICAgICA8aDM+e3RoaXMucHJvcHMubmFtZX08L2gzPlxuXG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImF2YXRhcnMtZ2FsbGVyeS1pbWFnZXNcIj5cbiAgICAgICAge2JhdGNoKHRoaXMucHJvcHMuaW1hZ2VzLCA0LCBudWxsKS5tYXAoKHJvdywgaSkgPT4ge1xuICAgICAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInJvd1wiIGtleT17aX0+XG4gICAgICAgICAgICB7cm93Lm1hcCgoaXRlbSwgaSkgPT4ge1xuICAgICAgICAgICAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJjb2wteHMtM1wiIGtleT17aX0+XG4gICAgICAgICAgICAgICAge2l0ZW0gPyA8R2FsbGVyeUl0ZW0gaW1hZ2U9e2l0ZW19XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMucHJvcHMuZGlzYWJsZWR9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc2VsZWN0PXt0aGlzLnByb3BzLnNlbGVjdH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzZWxlY3Rpb249e3RoaXMucHJvcHMuc2VsZWN0aW9ufSAvPlxuICAgICAgICAgICAgICAgICAgICAgIDogPGRpdiBjbGFzc05hbWU9XCJibGFuay1hdmF0YXJcIiAvPn1cbiAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICB9KX1cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgfSl9XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdzZWxlY3Rpb24nOiBudWxsLFxuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgc2VsZWN0ID0gKGltYWdlKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBzZWxlY3Rpb246IGltYWdlXG4gICAgfSk7XG4gIH07XG5cbiAgc2F2ZSA9ICgpID0+IHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRpbmcpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdpc0xvYWRpbmcnOiB0cnVlXG4gICAgfSk7XG5cbiAgICBhamF4LnBvc3QodGhpcy5wcm9wcy51c2VyLmFwaV91cmwuYXZhdGFyLCB7XG4gICAgICBhdmF0YXI6ICdnYWxsZXJpZXMnLFxuICAgICAgaW1hZ2U6IHRoaXMuc3RhdGUuc2VsZWN0aW9uXG4gICAgfSkudGhlbigocmVzcG9uc2UpID0+IHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnaXNMb2FkaW5nJzogZmFsc2VcbiAgICAgIH0pO1xuXG4gICAgICBzbmFja2Jhci5zdWNjZXNzKHJlc3BvbnNlLmRldGFpbCk7XG4gICAgICB0aGlzLnByb3BzLm9uQ29tcGxldGUocmVzcG9uc2UuYXZhdGFyX2hhc2gsIHJlc3BvbnNlLm9wdGlvbnMpO1xuICAgIH0sIChyZWplY3Rpb24pID0+IHtcbiAgICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMucHJvcHMuc2hvd0Vycm9yKHJlamVjdGlvbik7XG4gICAgICB9XG4gICAgfSk7XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keSBtb2RhbC1hdmF0YXItZ2FsbGVyeVwiPlxuXG4gICAgICAgIHt0aGlzLnByb3BzLm9wdGlvbnMuZ2FsbGVyaWVzLm1hcCgoaXRlbSwgaSkgPT4ge1xuICAgICAgICAgIHJldHVybiA8R2FsbGVyeSBuYW1lPXtpdGVtLm5hbWV9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIGltYWdlcz17aXRlbS5pbWFnZXN9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHNlbGVjdGlvbj17dGhpcy5zdGF0ZS5zZWxlY3Rpb259XG4gICAgICAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgICAgICAgc2VsZWN0PXt0aGlzLnNlbGVjdH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAga2V5PXtpfSAvPjtcbiAgICAgICAgfSl9XG5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1mb290ZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1tZC02IGNvbC1tZC1vZmZzZXQtM1wiPlxuXG4gICAgICAgICAgICA8QnV0dG9uIG9uQ2xpY2s9e3RoaXMuc2F2ZX1cbiAgICAgICAgICAgICAgICAgICAgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXshdGhpcy5zdGF0ZS5zZWxlY3Rpb259XG4gICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAgICB7dGhpcy5zdGF0ZS5zZWxlY3Rpb24gPyBnZXR0ZXh0KFwiU2F2ZSBjaG9pY2VcIilcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDogZ2V0dGV4dChcIlNlbGVjdCBhdmF0YXJcIil9XG4gICAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICAgICAgPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnByb3BzLnNob3dJbmRleH1cbiAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4tZGVmYXVsdCBidG4tYmxvY2tcIj5cbiAgICAgICAgICAgICAge2dldHRleHQoXCJDYW5jZWxcIil9XG4gICAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBBdmF0YXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYXZhdGFyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQnV0dG9uIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2J1dHRvbic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IExvYWRlciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9sb2FkZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICBjYWxsQXBpKGF2YXRhclR5cGUpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRpbmcpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdpc0xvYWRpbmcnOiB0cnVlXG4gICAgfSk7XG5cbiAgICBhamF4LnBvc3QodGhpcy5wcm9wcy51c2VyLmFwaV91cmwuYXZhdGFyLCB7XG4gICAgICBhdmF0YXI6IGF2YXRhclR5cGVcbiAgICB9KS50aGVuKChyZXNwb25zZSkgPT4ge1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgICAgfSk7XG5cbiAgICAgIHNuYWNrYmFyLnN1Y2Nlc3MocmVzcG9uc2UuZGV0YWlsKTtcbiAgICAgIHRoaXMucHJvcHMub25Db21wbGV0ZShyZXNwb25zZS5hdmF0YXJfaGFzaCwgcmVzcG9uc2Uub3B0aW9ucyk7XG4gICAgfSwgKHJlamVjdGlvbikgPT4ge1xuICAgICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMCkge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlXG4gICAgICAgIH0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgdGhpcy5wcm9wcy5zaG93RXJyb3IocmVqZWN0aW9uKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgc2V0R3JhdmF0YXIgPSAoKSA9PiB7XG4gICAgdGhpcy5jYWxsQXBpKCdncmF2YXRhcicpO1xuICB9O1xuXG4gIHNldEdlbmVyYXRlZCA9ICgpID0+IHtcbiAgICB0aGlzLmNhbGxBcGkoJ2dlbmVyYXRlZCcpO1xuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIGdldEdyYXZhdGFyQnV0dG9uKCkge1xuICAgIGlmICh0aGlzLnByb3BzLm9wdGlvbnMuZ3JhdmF0YXIpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8QnV0dG9uIG9uQ2xpY2s9e3RoaXMuc2V0R3JhdmF0YXJ9XG4gICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuLWRlZmF1bHQgYnRuLWJsb2NrIGJ0bi1hdmF0YXItZ3JhdmF0YXJcIj5cbiAgICAgICAge2dldHRleHQoXCJEb3dubG9hZCBteSBHcmF2YXRhclwiKX1cbiAgICAgIDwvQnV0dG9uPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIGdldENyb3BCdXR0b24oKSB7XG4gICAgaWYgKHRoaXMucHJvcHMub3B0aW9ucy5jcm9wX29yZykge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxCdXR0b24gb25DbGljaz17dGhpcy5wcm9wcy5zaG93Q3JvcH1cbiAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4tZGVmYXVsdCBidG4tYmxvY2sgYnRuLWF2YXRhci1jcm9wXCI+XG4gICAgICAgIHtnZXR0ZXh0KFwiUmUtY3JvcCB1cGxvYWRlZCBpbWFnZVwiKX1cbiAgICAgIDwvQnV0dG9uPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIGdldFVwbG9hZEJ1dHRvbigpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5vcHRpb25zLnVwbG9hZCkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxCdXR0b24gb25DbGljaz17dGhpcy5wcm9wcy5zaG93VXBsb2FkfVxuICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9jayBidG4tYXZhdGFyLXVwbG9hZFwiPlxuICAgICAgICB7Z2V0dGV4dChcIlVwbG9hZCBuZXcgaW1hZ2VcIil9XG4gICAgICA8L0J1dHRvbj47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICBnZXRHYWxsZXJ5QnV0dG9uKCkge1xuICAgIGlmICh0aGlzLnByb3BzLm9wdGlvbnMuZ2FsbGVyaWVzKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnByb3BzLnNob3dHYWxsZXJ5fVxuICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9jayBidG4tYXZhdGFyLWdhbGxlcnlcIj5cbiAgICAgICAge2dldHRleHQoXCJQaWNrIGF2YXRhciBmcm9tIGdhbGxlcnlcIil9XG4gICAgICA8L0J1dHRvbj47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICBnZXRBdmF0YXJQcmV2aWV3KCkge1xuICAgIGlmICh0aGlzLnN0YXRlLmlzTG9hZGluZykge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiYXZhdGFyLXByZXZpZXcgcHJldmlldy1sb2FkaW5nXCI+XG4gICAgICAgIDxBdmF0YXIgdXNlcj17dGhpcy5wcm9wcy51c2VyfSBzaXplPVwiMjAwXCIgLz5cbiAgICAgICAgPExvYWRlciAvPlxuICAgICAgPC9kaXY+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiYXZhdGFyLXByZXZpZXdcIj5cbiAgICAgICAgPEF2YXRhciB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IHNpemU9XCIyMDBcIiAvPlxuICAgICAgPC9kaXY+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHkgbW9kYWwtYXZhdGFyLWluZGV4XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInJvd1wiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1tZC01XCI+XG5cbiAgICAgICAgICB7dGhpcy5nZXRBdmF0YXJQcmV2aWV3KCl9XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLW1kLTdcIj5cblxuICAgICAgICAgIHt0aGlzLmdldEdyYXZhdGFyQnV0dG9uKCl9XG5cbiAgICAgICAgICA8QnV0dG9uIG9uQ2xpY2s9e3RoaXMuc2V0R2VuZXJhdGVkfVxuICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuLWRlZmF1bHQgYnRuLWJsb2NrIGJ0bi1hdmF0YXItZ2VuZXJhdGVcIj5cbiAgICAgICAgICAgIHtnZXR0ZXh0KFwiR2VuZXJhdGUgbXkgaW5kaXZpZHVhbCBhdmF0YXJcIil9XG4gICAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgICAgICB7dGhpcy5nZXRDcm9wQnV0dG9uKCl9XG4gICAgICAgICAge3RoaXMuZ2V0VXBsb2FkQnV0dG9uKCl9XG4gICAgICAgICAge3RoaXMuZ2V0R2FsbGVyeUJ1dHRvbigpfVxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEF2YXRhckluZGV4IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2NoYW5nZS1hdmF0YXIvaW5kZXgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBBdmF0YXJDcm9wIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2NoYW5nZS1hdmF0YXIvY3JvcCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEF2YXRhclVwbG9hZCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL3VwbG9hZCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEF2YXRhckdhbGxlcnkgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9nYWxsZXJ5JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgTG9hZGVyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL21vZGFsLWxvYWRlcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHsgdXBkYXRlQXZhdGFyIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3VzZXJzJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBjbGFzcyBDaGFuZ2VBdmF0YXJFcnJvciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldEVycm9yUmVhc29uKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnJlYXNvbikge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxwIGRhbmdlcm91c2x5U2V0SW5uZXJIVE1MPXt7X19odG1sOiB0aGlzLnByb3BzLnJlYXNvbn19IC8+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgcmVtb3ZlX2NpcmNsZV9vdXRsaW5lXG4gICAgICAgIDwvc3Bhbj5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWJvZHlcIj5cbiAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgIHt0aGlzLnByb3BzLm1lc3NhZ2V9XG4gICAgICAgIDwvcD5cbiAgICAgICAge3RoaXMuZ2V0RXJyb3JSZWFzb24oKX1cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgYWpheC5nZXQodGhpcy5wcm9wcy51c2VyLmFwaV91cmwuYXZhdGFyKS50aGVuKChvcHRpb25zKSA9PiB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ2NvbXBvbmVudCc6IEF2YXRhckluZGV4LFxuICAgICAgICAnb3B0aW9ucyc6IG9wdGlvbnMsXG4gICAgICAgICdlcnJvcic6IG51bGxcbiAgICAgIH0pO1xuICAgIH0sIChyZWplY3Rpb24pID0+IHtcbiAgICAgIHRoaXMuc2hvd0Vycm9yKHJlamVjdGlvbik7XG4gICAgfSk7XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHNob3dFcnJvciA9IChlcnJvcikgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgZXJyb3JcbiAgICB9KTtcbiAgfTtcblxuICBzaG93SW5kZXggPSAoKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAnY29tcG9uZW50JzogQXZhdGFySW5kZXhcbiAgICB9KTtcbiAgfTtcblxuICBzaG93VXBsb2FkID0gKCkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ2NvbXBvbmVudCc6IEF2YXRhclVwbG9hZFxuICAgIH0pO1xuICB9O1xuXG4gIHNob3dDcm9wID0gKCkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ2NvbXBvbmVudCc6IEF2YXRhckNyb3BcbiAgICB9KTtcbiAgfTtcblxuICBzaG93R2FsbGVyeSA9ICgpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdjb21wb25lbnQnOiBBdmF0YXJHYWxsZXJ5XG4gICAgfSk7XG4gIH07XG5cbiAgY29tcGxldGVGbG93ID0gKGF2YXRhckhhc2gsIG9wdGlvbnMpID0+IHtcbiAgICBzdG9yZS5kaXNwYXRjaCh1cGRhdGVBdmF0YXIodGhpcy5wcm9wcy51c2VyLCBhdmF0YXJIYXNoKSk7XG5cbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdjb21wb25lbnQnOiBBdmF0YXJJbmRleCxcbiAgICAgIG9wdGlvbnNcbiAgICB9KTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRCb2R5KCkge1xuICAgIGlmICh0aGlzLnN0YXRlKSB7XG4gICAgICBpZiAodGhpcy5zdGF0ZS5lcnJvcikge1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIHJldHVybiA8Q2hhbmdlQXZhdGFyRXJyb3IgbWVzc2FnZT17dGhpcy5zdGF0ZS5lcnJvci5kZXRhaWx9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVhc29uPXt0aGlzLnN0YXRlLmVycm9yLnJlYXNvbn0gLz47XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIHJldHVybiA8dGhpcy5zdGF0ZS5jb21wb25lbnQgb3B0aW9ucz17dGhpcy5zdGF0ZS5vcHRpb25zfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVzZXI9e3RoaXMucHJvcHMudXNlcn1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBvbkNvbXBsZXRlPXt0aGlzLmNvbXBsZXRlRmxvd31cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzaG93RXJyb3I9e3RoaXMuc2hvd0Vycm9yfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNob3dJbmRleD17dGhpcy5zaG93SW5kZXh9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc2hvd0Nyb3A9e3RoaXMuc2hvd0Nyb3B9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc2hvd1VwbG9hZD17dGhpcy5zaG93VXBsb2FkfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNob3dHYWxsZXJ5PXt0aGlzLnNob3dHYWxsZXJ5fSAvPjtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxMb2FkZXIgLz47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH1cbiAgfVxuXG4gIGdldENsYXNzTmFtZSgpIHtcbiAgIGlmICh0aGlzLnN0YXRlICYmIHRoaXMuc3RhdGUuZXJyb3IpIHtcbiAgICAgIHJldHVybiBcIm1vZGFsLWRpYWxvZyBtb2RhbC1tZXNzYWdlIG1vZGFsLWNoYW5nZS1hdmF0YXJcIjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIFwibW9kYWwtZGlhbG9nIG1vZGFsLWNoYW5nZS1hdmF0YXJcIjtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzc05hbWUoKX1cbiAgICAgICAgICAgICAgICByb2xlPVwiZG9jdW1lbnRcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtY29udGVudFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWhlYWRlclwiPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImNsb3NlXCIgZGF0YS1kaXNtaXNzPVwibW9kYWxcIlxuICAgICAgICAgICAgICAgICAgYXJpYS1sYWJlbD17Z2V0dGV4dChcIkNsb3NlXCIpfT5cbiAgICAgICAgICAgIDxzcGFuIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPiZ0aW1lczs8L3NwYW4+XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgPGg0IGNsYXNzTmFtZT1cIm1vZGFsLXRpdGxlXCI+e2dldHRleHQoXCJDaGFuZ2UgeW91ciBhdmF0YXJcIil9PC9oND5cbiAgICAgICAgPC9kaXY+XG5cbiAgICAgICAge3RoaXMuZ2V0Qm9keSgpfVxuXG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0KHN0YXRlKSB7XG4gIHJldHVybiB7XG4gICAgJ3VzZXInOiBzdGF0ZS5hdXRoLnVzZXJcbiAgfTtcbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgQXZhdGFyQ3JvcCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL2Nyb3AnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGZpbGVTaXplIGZyb20gJ21pc2Fnby91dGlscy9maWxlLXNpemUnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpbWFnZSc6IG51bGwsXG4gICAgICAncHJldmlldyc6IG51bGwsXG4gICAgICAncHJvZ3Jlc3MnOiAwLFxuICAgICAgJ3VwbG9hZGVkJzogbnVsbCxcbiAgICB9O1xuICB9XG5cbiAgdmFsaWRhdGVGaWxlKGltYWdlKSB7XG4gICAgaWYgKGltYWdlLnNpemUgPiB0aGlzLnByb3BzLm9wdGlvbnMudXBsb2FkLmxpbWl0KSB7XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIlNlbGVjdGVkIGZpbGUgaXMgdG9vIGJpZy4gKCUoZmlsZXNpemUpcylcIiksIHtcbiAgICAgICAgJ2ZpbGVzaXplJzogZmlsZVNpemUoaW1hZ2Uuc2l6ZSlcbiAgICAgIH0sIHRydWUpO1xuICAgIH1cblxuICAgIGxldCBpbnZhbGlkVHlwZU1zZyA9IGdldHRleHQoXCJTZWxlY3RlZCBmaWxlIHR5cGUgaXMgbm90IHN1cHBvcnRlZC5cIik7XG4gICAgaWYgKHRoaXMucHJvcHMub3B0aW9ucy51cGxvYWQuYWxsb3dlZF9taW1lX3R5cGVzLmluZGV4T2YoaW1hZ2UudHlwZSkgPT09IC0xKSB7XG4gICAgICByZXR1cm4gaW52YWxpZFR5cGVNc2c7XG4gICAgfVxuXG4gICAgbGV0IGV4dGVuc2lvbkZvdW5kID0gZmFsc2U7XG4gICAgbGV0IGxvd2VyZWRGaWxlbmFtZSA9IGltYWdlLm5hbWUudG9Mb3dlckNhc2UoKTtcbiAgICB0aGlzLnByb3BzLm9wdGlvbnMudXBsb2FkLmFsbG93ZWRfZXh0ZW5zaW9ucy5tYXAoZnVuY3Rpb24oZXh0ZW5zaW9uKSB7XG4gICAgICBpZiAobG93ZXJlZEZpbGVuYW1lLnN1YnN0cihleHRlbnNpb24ubGVuZ3RoICogLTEpID09PSBleHRlbnNpb24pIHtcbiAgICAgICAgZXh0ZW5zaW9uRm91bmQgPSB0cnVlO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKCFleHRlbnNpb25Gb3VuZCkge1xuICAgICAgcmV0dXJuIGludmFsaWRUeXBlTXNnO1xuICAgIH1cblxuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgcGlja0ZpbGUgPSAoKSA9PiB7XG4gICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2F2YXRhci1oaWRkZW4tdXBsb2FkJykuY2xpY2soKTtcbiAgfTtcblxuICB1cGxvYWRGaWxlID0gKCkgPT4ge1xuICAgIGxldCBpbWFnZSA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdhdmF0YXItaGlkZGVuLXVwbG9hZCcpLmZpbGVzWzBdO1xuXG4gICAgbGV0IHZhbGlkYXRpb25FcnJvciA9IHRoaXMudmFsaWRhdGVGaWxlKGltYWdlKTtcbiAgICBpZiAodmFsaWRhdGlvbkVycm9yKSB7XG4gICAgICBzbmFja2Jhci5lcnJvcih2YWxpZGF0aW9uRXJyb3IpO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgaW1hZ2UsXG4gICAgICAncHJldmlldyc6IFVSTC5jcmVhdGVPYmplY3RVUkwoaW1hZ2UpLFxuICAgICAgJ3Byb2dyZXNzJzogMFxuICAgIH0pO1xuXG4gICAgbGV0IGRhdGEgPSBuZXcgRm9ybURhdGEoKTtcbiAgICBkYXRhLmFwcGVuZCgnYXZhdGFyJywgJ3VwbG9hZCcpO1xuICAgIGRhdGEuYXBwZW5kKCdpbWFnZScsIGltYWdlKTtcblxuICAgIGFqYXgudXBsb2FkKHRoaXMucHJvcHMudXNlci5hcGlfdXJsLmF2YXRhciwgZGF0YSwgKHByb2dyZXNzKSA9PiB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgcHJvZ3Jlc3NcbiAgICAgIH0pO1xuICAgIH0pLnRoZW4oKGRhdGEpID0+IHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnb3B0aW9ucyc6IGRhdGEub3B0aW9ucyxcbiAgICAgICAgJ3VwbG9hZGVkJzogZGF0YS5kZXRhaWxcbiAgICAgIH0pO1xuICAgICAgc25hY2tiYXIuaW5mbyhnZXR0ZXh0KFwiWW91ciBpbWFnZSBoYXMgYmVlbiB1cGxvYWRlZCBhbmQgeW91IG1heSBub3cgY3JvcCBpdC5cIikpO1xuICAgIH0sIChyZWplY3Rpb24pID0+IHtcbiAgICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICdpc0xvYWRpbmcnOiBmYWxzZSxcbiAgICAgICAgICAnaW1hZ2UnOiBudWxsLFxuICAgICAgICAgICdwcm9ncmVzcyc6IDBcbiAgICAgICAgfSlcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMucHJvcHMuc2hvd0Vycm9yKHJlamVjdGlvbik7XG4gICAgICB9XG4gICAgfSk7XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgZ2V0VXBsb2FkUmVxdWlyZW1lbnRzKG9wdGlvbnMpIHtcbiAgICBsZXQgZXh0ZW5zaW9ucyA9IG9wdGlvbnMuYWxsb3dlZF9leHRlbnNpb25zLm1hcChmdW5jdGlvbihleHRlbnNpb24pIHtcbiAgICAgIHJldHVybiBleHRlbnNpb24uc3Vic3RyKDEpO1xuICAgIH0pO1xuXG4gICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCIlKGZpbGVzKXMgZmlsZXMgc21hbGxlciB0aGFuICUobGltaXQpc1wiKSwge1xuICAgICAgICAnZmlsZXMnOiBleHRlbnNpb25zLmpvaW4oJywgJyksXG4gICAgICAgICdsaW1pdCc6IGZpbGVTaXplKG9wdGlvbnMubGltaXQpXG4gICAgICB9LCB0cnVlKTtcbiAgfVxuXG4gIGdldFVwbG9hZEJ1dHRvbigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keSBtb2RhbC1hdmF0YXItdXBsb2FkXCI+XG4gICAgICAgIDxCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXBpY2stZmlsZVwiXG4gICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5waWNrRmlsZX0+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICBpbnB1dFxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiU2VsZWN0IGZpbGVcIil9XG4gICAgICAgIDwvQnV0dG9uPlxuICAgICAgICA8cCBjbGFzc05hbWU9XCJ0ZXh0LW11dGVkXCI+XG4gICAgICAgICAge3RoaXMuZ2V0VXBsb2FkUmVxdWlyZW1lbnRzKHRoaXMucHJvcHMub3B0aW9ucy51cGxvYWQpfVxuICAgICAgICA8L3A+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cblxuICBnZXRVcGxvYWRQcm9ncmVzc0xhYmVsKCkge1xuICAgIHJldHVybiBpbnRlcnBvbGF0ZShnZXR0ZXh0KFwiJShwcm9ncmVzcylzICUgY29tcGxldGVcIiksIHtcbiAgICAgICAgJ3Byb2dyZXNzJzogdGhpcy5zdGF0ZS5wcm9ncmVzc1xuICAgICAgfSwgdHJ1ZSk7XG4gIH1cblxuICBnZXRVcGxvYWRQcm9ncmVzcygpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keSBtb2RhbC1hdmF0YXItdXBsb2FkXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidXBsb2FkLXByb2dyZXNzXCI+XG4gICAgICAgICAgPGltZyBzcmM9e3RoaXMuc3RhdGUucHJldmlld30gLz5cblxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicHJvZ3Jlc3NcIj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicHJvZ3Jlc3MtYmFyXCIgcm9sZT1cInByb2dyZXNzYmFyXCJcbiAgICAgICAgICAgICAgICAgYXJpYS12YWx1ZW5vdz1cInt0aGlzLnN0YXRlLnByb2dyZXNzfVwiXG4gICAgICAgICAgICAgICAgIGFyaWEtdmFsdWVtaW49XCIwXCIgYXJpYS12YWx1ZW1heD1cIjEwMFwiXG4gICAgICAgICAgICAgICAgIHN0eWxlPXt7d2lkdGg6IHRoaXMuc3RhdGUucHJvZ3Jlc3MgKyAnJSd9fT5cbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwic3Itb25seVwiPnt0aGlzLmdldFVwbG9hZFByb2dyZXNzTGFiZWwoKX08L3NwYW4+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cblxuICByZW5kZXJVcGxvYWQoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2PlxuICAgICAgPGlucHV0IHR5cGU9XCJmaWxlXCJcbiAgICAgICAgICAgICBpZD1cImF2YXRhci1oaWRkZW4tdXBsb2FkXCJcbiAgICAgICAgICAgICBjbGFzc05hbWU9XCJoaWRkZW4tZmlsZS11cGxvYWRcIlxuICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLnVwbG9hZEZpbGV9IC8+XG4gICAgICB7dGhpcy5zdGF0ZS5pbWFnZSA/IHRoaXMuZ2V0VXBsb2FkUHJvZ3Jlc3MoKVxuICAgICAgICAgICAgICAgICAgICAgICAgOiB0aGlzLmdldFVwbG9hZEJ1dHRvbigpfVxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1mb290ZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wtbWQtNiBjb2wtbWQtb2Zmc2V0LTNcIj5cblxuICAgICAgICAgIDxCdXR0b24gb25DbGljaz17dGhpcy5wcm9wcy5zaG93SW5kZXh9XG4gICAgICAgICAgICAgICAgICBkaXNhYmxlZD17ISF0aGlzLnN0YXRlLmltYWdlfVxuICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuLWRlZmF1bHQgYnRuLWJsb2NrXCI+XG4gICAgICAgICAgICB7Z2V0dGV4dChcIkNhbmNlbFwiKX1cbiAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG5cbiAgcmVuZGVyQ3JvcCgpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxBdmF0YXJDcm9wIG9wdGlvbnM9e3RoaXMuc3RhdGUub3B0aW9uc31cbiAgICAgICAgICAgICAgICAgICAgICAgdXNlcj17dGhpcy5wcm9wcy51c2VyfVxuICAgICAgICAgICAgICAgICAgICAgICB1cGxvYWQ9e3RoaXMuc3RhdGUudXBsb2FkZWR9XG4gICAgICAgICAgICAgICAgICAgICAgIG9uQ29tcGxldGU9e3RoaXMucHJvcHMub25Db21wbGV0ZX1cbiAgICAgICAgICAgICAgICAgICAgICAgc2hvd0Vycm9yPXt0aGlzLnByb3BzLnNob3dFcnJvcn1cbiAgICAgICAgICAgICAgICAgICAgICAgc2hvd0luZGV4PXt0aGlzLnByb3BzLnNob3dJbmRleH0gLz47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuICh0aGlzLnN0YXRlLnVwbG9hZGVkID8gdGhpcy5yZW5kZXJDcm9wKClcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgOiB0aGlzLnJlbmRlclVwbG9hZCgpKTtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBpc1ZhbGlkYXRlZCgpIHtcbiAgICByZXR1cm4gdHlwZW9mIHRoaXMucHJvcHMudmFsaWRhdGlvbiAhPT0gXCJ1bmRlZmluZWRcIjtcbiAgfVxuXG4gIGdldENsYXNzTmFtZSgpIHtcbiAgICBsZXQgY2xhc3NOYW1lID0gJ2Zvcm0tZ3JvdXAnO1xuICAgIGlmICh0aGlzLmlzVmFsaWRhdGVkKCkpIHtcbiAgICAgIGNsYXNzTmFtZSArPSAnIGhhcy1mZWVkYmFjayc7XG4gICAgICBpZiAodGhpcy5wcm9wcy52YWxpZGF0aW9uID09PSBudWxsKSB7XG4gICAgICAgIGNsYXNzTmFtZSArPSAnIGhhcy1zdWNjZXNzJztcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGNsYXNzTmFtZSArPSAnIGhhcy1lcnJvcic7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBjbGFzc05hbWU7XG4gIH1cblxuICBnZXRGZWVkYmFjaygpIHtcbiAgICBpZiAodGhpcy5wcm9wcy52YWxpZGF0aW9uKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJoZWxwLWJsb2NrIGVycm9yc1wiPlxuICAgICAgICB7dGhpcy5wcm9wcy52YWxpZGF0aW9uLm1hcCgoZXJyb3IsIGkpID0+IHtcbiAgICAgICAgICByZXR1cm4gPHAga2V5PXt0aGlzLnByb3BzLmZvciArICdGZWVkYmFja0l0ZW0nICsgaX0+e2Vycm9yfTwvcD47XG4gICAgICAgIH0pfVxuICAgICAgPC9kaXY+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgZ2V0RmVlZGJhY2tJY29uKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWRhdGVkKCkpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uIGZvcm0tY29udHJvbC1mZWVkYmFja1wiXG4gICAgICAgICAgICAgICAgICAgYXJpYS1oaWRkZW49XCJ0cnVlXCIga2V5PXt0aGlzLnByb3BzLmZvciArICdGZWVkYmFja0ljb24nfT5cbiAgICAgICAge3RoaXMucHJvcHMudmFsaWRhdGlvbiA/ICdjbGVhcicgOiAnY2hlY2snfVxuICAgICAgPC9zcGFuPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIGdldEZlZWRiYWNrRGVzY3JpcHRpb24oKSB7XG4gICAgaWYgKHRoaXMuaXNWYWxpZGF0ZWQoKSkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxzcGFuIGlkPXt0aGlzLnByb3BzLmZvciArICdfc3RhdHVzJ30gY2xhc3NOYW1lPVwic3Itb25seVwiPlxuICAgICAgICB7dGhpcy5wcm9wcy52YWxpZGF0aW9uID8gZ2V0dGV4dCgnKGVycm9yKScpIDogZ2V0dGV4dCgnKHN1Y2Nlc3MpJyl9XG4gICAgICA8L3NwYW4+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgZ2V0SGVscFRleHQoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuaGVscFRleHQpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8cCBjbGFzc05hbWU9XCJoZWxwLWJsb2NrXCI+e3RoaXMucHJvcHMuaGVscFRleHR9PC9wPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPXt0aGlzLmdldENsYXNzTmFtZSgpfT5cbiAgICAgIDxsYWJlbCBjbGFzc05hbWU9eydjb250cm9sLWxhYmVsICcgKyAodGhpcy5wcm9wcy5sYWJlbENsYXNzIHx8ICcnKX1cbiAgICAgICAgICAgICBodG1sRm9yPXt0aGlzLnByb3BzLmZvciB8fCAnJ30+XG4gICAgICAgIHt0aGlzLnByb3BzLmxhYmVsICsgJzonfVxuICAgICAgPC9sYWJlbD5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPXt0aGlzLnByb3BzLmNvbnRyb2xDbGFzcyB8fCAnJ30+XG4gICAgICAgIHt0aGlzLnByb3BzLmNoaWxkcmVufVxuICAgICAgICB7dGhpcy5nZXRGZWVkYmFja0ljb24oKX1cbiAgICAgICAge3RoaXMuZ2V0RmVlZGJhY2tEZXNjcmlwdGlvbigpfVxuICAgICAgICB7dGhpcy5nZXRGZWVkYmFjaygpfVxuICAgICAgICB7dGhpcy5nZXRIZWxwVGV4dCgpfVxuICAgICAgICB7dGhpcy5wcm9wcy5leHRyYSB8fCBudWxsfVxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IHJlcXVpcmVkIH0gZnJvbSAnbWlzYWdvL3V0aWxzL3ZhbGlkYXRvcnMnO1xuXG5sZXQgdmFsaWRhdGVSZXF1aXJlZCA9IHJlcXVpcmVkKCk7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgdmFsaWRhdGUoKSB7XG4gICAgbGV0IGVycm9ycyA9IHt9O1xuICAgIGlmICghdGhpcy5zdGF0ZS52YWxpZGF0b3JzKSB7XG4gICAgICByZXR1cm4gZXJyb3JzO1xuICAgIH1cblxuICAgIGxldCB2YWxpZGF0b3JzID0ge1xuICAgICAgcmVxdWlyZWQ6IHRoaXMuc3RhdGUudmFsaWRhdG9ycy5yZXF1aXJlZCB8fCB0aGlzLnN0YXRlLnZhbGlkYXRvcnMsXG4gICAgICBvcHRpb25hbDogdGhpcy5zdGF0ZS52YWxpZGF0b3JzLm9wdGlvbmFsIHx8IHt9XG4gICAgfTtcblxuICAgIGxldCB2YWxpZGF0ZWRGaWVsZHMgPSBbXTtcblxuICAgIC8vIGFkZCByZXF1aXJlZCBmaWVsZHMgdG8gdmFsaWRhdGlvblxuICAgIGZvciAobGV0IG5hbWUgaW4gdmFsaWRhdG9ycy5yZXF1aXJlZCkge1xuICAgICAgaWYgKHZhbGlkYXRvcnMucmVxdWlyZWQuaGFzT3duUHJvcGVydHkobmFtZSkgJiZcbiAgICAgICAgICB2YWxpZGF0b3JzLnJlcXVpcmVkW25hbWVdKSB7XG4gICAgICAgIHZhbGlkYXRlZEZpZWxkcy5wdXNoKG5hbWUpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIGFkZCBvcHRpb25hbCBmaWVsZHMgdG8gdmFsaWRhdGlvblxuICAgIGZvciAobGV0IG5hbWUgaW4gdmFsaWRhdG9ycy5vcHRpb25hbCkge1xuICAgICAgaWYgKHZhbGlkYXRvcnMub3B0aW9uYWwuaGFzT3duUHJvcGVydHkobmFtZSkgJiZcbiAgICAgICAgICB2YWxpZGF0b3JzLm9wdGlvbmFsW25hbWVdKSB7XG4gICAgICAgIHZhbGlkYXRlZEZpZWxkcy5wdXNoKG5hbWUpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIHZhbGlkYXRlIGZpZWxkcyB2YWx1ZXNcbiAgICBmb3IgKGxldCBpIGluIHZhbGlkYXRlZEZpZWxkcykge1xuICAgICAgbGV0IG5hbWUgPSB2YWxpZGF0ZWRGaWVsZHNbaV07XG4gICAgICBsZXQgZmllbGRFcnJvcnMgPSB0aGlzLnZhbGlkYXRlRmllbGQobmFtZSwgdGhpcy5zdGF0ZVtuYW1lXSk7XG5cbiAgICAgIGlmIChmaWVsZEVycm9ycyA9PT0gbnVsbCkge1xuICAgICAgICBlcnJvcnNbbmFtZV0gPSBudWxsO1xuICAgICAgfSBlbHNlIGlmIChmaWVsZEVycm9ycykge1xuICAgICAgICBlcnJvcnNbbmFtZV0gPSBmaWVsZEVycm9ycztcbiAgICAgIH1cbiAgICB9XG5cbiAgICByZXR1cm4gZXJyb3JzO1xuICB9XG5cbiAgaXNWYWxpZCgpIHtcbiAgICBsZXQgZXJyb3JzID0gdGhpcy52YWxpZGF0ZSgpO1xuICAgIGZvciAobGV0IGZpZWxkIGluIGVycm9ycykge1xuICAgICAgaWYgKGVycm9ycy5oYXNPd25Qcm9wZXJ0eShmaWVsZCkpIHtcbiAgICAgICAgaWYgKGVycm9yc1tmaWVsZF0gIT09IG51bGwpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG5cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIHZhbGlkYXRlRmllbGQobmFtZSwgdmFsdWUpIHtcbiAgICBsZXQgZXJyb3JzID0gW107XG4gICAgaWYgKCF0aGlzLnN0YXRlLnZhbGlkYXRvcnMpIHtcbiAgICAgIHJldHVybiBlcnJvcnM7XG4gICAgfVxuXG4gICAgbGV0IHZhbGlkYXRvcnMgPSB7XG4gICAgICByZXF1aXJlZDogKHRoaXMuc3RhdGUudmFsaWRhdG9ycy5yZXF1aXJlZCB8fCB0aGlzLnN0YXRlLnZhbGlkYXRvcnMpW25hbWVdLFxuICAgICAgb3B0aW9uYWw6ICh0aGlzLnN0YXRlLnZhbGlkYXRvcnMub3B0aW9uYWwgfHwge30pW25hbWVdXG4gICAgfTtcblxuICAgIGxldCByZXF1aXJlZEVycm9yID0gdmFsaWRhdGVSZXF1aXJlZCh2YWx1ZSkgfHwgZmFsc2U7XG5cbiAgICBpZiAodmFsaWRhdG9ycy5yZXF1aXJlZCkge1xuICAgICAgaWYgKHJlcXVpcmVkRXJyb3IpIHtcbiAgICAgICAgZXJyb3JzID0gW3JlcXVpcmVkRXJyb3JdO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgZm9yIChsZXQgaSBpbiB2YWxpZGF0b3JzLnJlcXVpcmVkKSB7XG4gICAgICAgICAgbGV0IHZhbGlkYXRpb25FcnJvciA9IHZhbGlkYXRvcnMucmVxdWlyZWRbaV0odmFsdWUpO1xuICAgICAgICAgIGlmICh2YWxpZGF0aW9uRXJyb3IpIHtcbiAgICAgICAgICAgIGVycm9ycy5wdXNoKHZhbGlkYXRpb25FcnJvcik7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBlcnJvcnMubGVuZ3RoID8gZXJyb3JzIDogbnVsbDtcbiAgICB9IGVsc2UgaWYgKHJlcXVpcmVkRXJyb3IgPT09IGZhbHNlICYmIHZhbGlkYXRvcnMub3B0aW9uYWwpIHtcbiAgICAgIGZvciAobGV0IGkgaW4gdmFsaWRhdG9ycy5vcHRpb25hbCkge1xuICAgICAgICBsZXQgdmFsaWRhdGlvbkVycm9yID0gdmFsaWRhdG9ycy5vcHRpb25hbFtpXSh2YWx1ZSk7XG4gICAgICAgIGlmICh2YWxpZGF0aW9uRXJyb3IpIHtcbiAgICAgICAgICBlcnJvcnMucHVzaCh2YWxpZGF0aW9uRXJyb3IpO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBlcnJvcnMubGVuZ3RoID8gZXJyb3JzIDogbnVsbDtcbiAgICB9XG5cbiAgICByZXR1cm4gZmFsc2U7IC8vIGZhbHNlID09PSBmaWVsZCB3YXNuJ3QgdmFsaWRhdGVkXG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGJpbmRJbnB1dCA9IChuYW1lKSA9PiB7XG4gICAgcmV0dXJuIChldmVudCkgPT4ge1xuICAgICAgbGV0IG5ld1N0YXRlID0ge1xuICAgICAgICBbbmFtZV06IGV2ZW50LnRhcmdldC52YWx1ZVxuICAgICAgfTtcblxuICAgICAgbGV0IGZvcm1FcnJvcnMgPSB0aGlzLnN0YXRlLmVycm9ycyB8fCB7fTtcbiAgICAgIGZvcm1FcnJvcnNbbmFtZV0gPSB0aGlzLnZhbGlkYXRlRmllbGQobmFtZSwgbmV3U3RhdGVbbmFtZV0pO1xuICAgICAgbmV3U3RhdGUuZXJyb3JzID0gZm9ybUVycm9ycztcblxuICAgICAgdGhpcy5zZXRTdGF0ZShuZXdTdGF0ZSk7XG4gICAgfVxuICB9O1xuXG4gIGNsZWFuKCkge1xuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3Moc3VjY2Vzcykge1xuICAgIHJldHVybjtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIHJldHVybjtcbiAgfVxuXG4gIGhhbmRsZVN1Ym1pdCA9IChldmVudCkgPT4ge1xuICAgIC8vIHdlIGRvbid0IHJlbG9hZCBwYWdlIG9uIHN1Ym1pc3Npb25zXG4gICAgZXZlbnQucHJldmVudERlZmF1bHQoKVxuICAgIGlmICh0aGlzLnN0YXRlLmlzTG9hZGluZykge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGlmICh0aGlzLmNsZWFuKCkpIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe2lzTG9hZGluZzogdHJ1ZX0pO1xuICAgICAgbGV0IHByb21pc2UgPSB0aGlzLnNlbmQoKTtcblxuICAgICAgaWYgKHByb21pc2UpIHtcbiAgICAgICAgcHJvbWlzZS50aGVuKChzdWNjZXNzKSA9PiB7XG4gICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7aXNMb2FkaW5nOiBmYWxzZX0pO1xuICAgICAgICAgIHRoaXMuaGFuZGxlU3VjY2VzcyhzdWNjZXNzKTtcbiAgICAgICAgfSwgKHJlamVjdGlvbikgPT4ge1xuICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe2lzTG9hZGluZzogZmFsc2V9KTtcbiAgICAgICAgICB0aGlzLmhhbmRsZUVycm9yKHJlamVjdGlvbik7XG4gICAgICAgIH0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZSh7aXNMb2FkaW5nOiBmYWxzZX0pO1xuICAgICAgfVxuICAgIH1cbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGlzQWN0aXZlKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnBhdGgpIHtcbiAgICAgIHJldHVybiBkb2N1bWVudC5sb2NhdGlvbi5wYXRobmFtZS5pbmRleE9mKHRoaXMucHJvcHMucGF0aCkgPT09IDA7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gIH1cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICAgaWYgKHRoaXMuaXNBY3RpdmUoKSkge1xuICAgICAgcmV0dXJuICh0aGlzLnByb3BzLmNsYXNzTmFtZSB8fCAnJykgKyAnICcrICh0aGlzLnByb3BzLmFjdGl2ZUNsYXNzTmFtZSB8fCAnYWN0aXZlJyk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLnByb3BzLmNsYXNzTmFtZSB8fCAnJztcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLy8ganNoaW50IGlnbm9yZTpzdGFydFxuICAgIHJldHVybiA8bGkgY2xhc3NOYW1lPXt0aGlzLmdldENsYXNzTmFtZSgpfT5cbiAgICAgIHt0aGlzLnByb3BzLmNoaWxkcmVufVxuICAgIDwvbGk+O1xuICAgIC8vIGpzaGludCBpZ25vcmU6ZW5kXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPXt0aGlzLnByb3BzLmNsYXNzTmFtZSB8fCBcImxvYWRlclwifT5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibG9hZGVyLXNwaW5uaW5nLXdoZWVsXCI+PC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgTG9hZGVyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2xvYWRlcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keSBtb2RhbC1sb2FkZXJcIj5cbiAgICAgIDxMb2FkZXIgLz5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG4iLCJpbXBvcnQgbW9tZW50IGZyb20gJ21vbWVudCc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEF2YXRhciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdmF0YXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBGb3JtR3JvdXAgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybS1ncm91cCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IExvYWRlciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9sb2FkZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCB7IGRlaHlkcmF0ZSwgYWRkTmFtZUNoYW5nZSB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy91c2VybmFtZS1oaXN0b3J5JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgeyB1cGRhdGVVc2VybmFtZSB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy91c2Vycyc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IHRpdGxlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9wYWdlLXRpdGxlJztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5pbXBvcnQgKiBhcyByYW5kb20gZnJvbSAnbWlzYWdvL3V0aWxzL3JhbmRvbSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0ICogYXMgdmFsaWRhdG9ycyBmcm9tICdtaXNhZ28vdXRpbHMvdmFsaWRhdG9ycyc7XG5cbmV4cG9ydCBjbGFzcyBDaGFuZ2VVc2VybmFtZSBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICB1c2VybmFtZTogJycsXG5cbiAgICAgIHZhbGlkYXRvcnM6IHtcbiAgICAgICAgdXNlcm5hbWU6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnVzZXJuYW1lQ29udGVudCgpLFxuICAgICAgICAgIHZhbGlkYXRvcnMudXNlcm5hbWVNaW5MZW5ndGgoe1xuICAgICAgICAgICAgdXNlcm5hbWVfbGVuZ3RoX21pbjogcHJvcHMub3B0aW9ucy5sZW5ndGhfbWluXG4gICAgICAgICAgfSksXG4gICAgICAgICAgdmFsaWRhdG9ycy51c2VybmFtZU1heExlbmd0aCh7XG4gICAgICAgICAgICB1c2VybmFtZV9sZW5ndGhfbWF4OiBwcm9wcy5vcHRpb25zLmxlbmd0aF9tYXhcbiAgICAgICAgICB9KVxuICAgICAgICBdXG4gICAgICB9LFxuXG4gICAgICBpc0xvYWRpbmc6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIGdldEhlbHBUZXh0KCkge1xuICAgIGxldCBwaHJhc2VzID0gW107XG5cbiAgICBpZiAodGhpcy5wcm9wcy5vcHRpb25zLmNoYW5nZXNfbGVmdCA+IDApIHtcbiAgICAgIGxldCBtZXNzYWdlID0gbmdldHRleHQoXG4gICAgICAgIFwiWW91IGNhbiBjaGFuZ2UgeW91ciB1c2VybmFtZSAlKGNoYW5nZXNfbGVmdClzIG1vcmUgdGltZS5cIixcbiAgICAgICAgXCJZb3UgY2FuIGNoYW5nZSB5b3VyIHVzZXJuYW1lICUoY2hhbmdlc19sZWZ0KXMgbW9yZSB0aW1lcy5cIixcbiAgICAgICAgdGhpcy5wcm9wcy5vcHRpb25zLmNoYW5nZXNfbGVmdCk7XG5cbiAgICAgIHBocmFzZXMucHVzaChpbnRlcnBvbGF0ZShtZXNzYWdlLCB7XG4gICAgICAgICdjaGFuZ2VzX2xlZnQnOiB0aGlzLnByb3BzLm9wdGlvbnMuY2hhbmdlc19sZWZ0XG4gICAgICB9LCB0cnVlKSk7XG4gICAgfVxuXG4gICAgaWYgKHRoaXMucHJvcHMudXNlci5hY2wubmFtZV9jaGFuZ2VzX2V4cGlyZSA+IDApIHtcbiAgICAgIGxldCBtZXNzYWdlID0gbmdldHRleHQoXG4gICAgICAgIFwiVXNlZCBjaGFuZ2VzIHJlZGVlbSBhZnRlciAlKG5hbWVfY2hhbmdlc19leHBpcmUpcyBkYXkuXCIsXG4gICAgICAgIFwiVXNlZCBjaGFuZ2VzIHJlZGVlbSBhZnRlciAlKG5hbWVfY2hhbmdlc19leHBpcmUpcyBkYXlzLlwiLFxuICAgICAgICB0aGlzLnByb3BzLnVzZXIuYWNsLm5hbWVfY2hhbmdlc19leHBpcmUpO1xuXG4gICAgICBwaHJhc2VzLnB1c2goaW50ZXJwb2xhdGUobWVzc2FnZSwge1xuICAgICAgICAnbmFtZV9jaGFuZ2VzX2V4cGlyZSc6IHRoaXMucHJvcHMudXNlci5hY2wubmFtZV9jaGFuZ2VzX2V4cGlyZVxuICAgICAgfSwgdHJ1ZSkpO1xuICAgIH1cblxuICAgIHJldHVybiBwaHJhc2VzLmxlbmd0aCA/IHBocmFzZXMuam9pbignICcpIDogbnVsbDtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGxldCBlcnJvcnMgPSB0aGlzLnZhbGlkYXRlKCk7XG4gICAgaWYgKGVycm9ycy51c2VybmFtZSkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZXJyb3JzLnVzZXJuYW1lWzBdKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9IGlmICh0aGlzLnN0YXRlLnVzZXJuYW1lLnRyaW0oKSA9PT0gdGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lKSB7XG4gICAgICBzbmFja2Jhci5pbmZvKGdldHRleHQoXCJZb3VyIG5ldyB1c2VybmFtZSBpcyBzYW1lIGFzIGN1cnJlbnQgb25lLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdCh0aGlzLnByb3BzLnVzZXIuYXBpX3VybC51c2VybmFtZSwge1xuICAgICAgJ3VzZXJuYW1lJzogdGhpcy5zdGF0ZS51c2VybmFtZVxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhzdWNjZXNzKSB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAndXNlcm5hbWUnOiAnJ1xuICAgIH0pO1xuXG4gICAgdGhpcy5wcm9wcy5jb21wbGV0ZShzdWNjZXNzLnVzZXJuYW1lLCBzdWNjZXNzLnNsdWcsIHN1Y2Nlc3Mub3B0aW9ucyk7XG4gIH1cblxuICBoYW5kbGVFcnJvcihyZWplY3Rpb24pIHtcbiAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fSBjbGFzc05hbWU9XCJmb3JtLWhvcml6b250YWxcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwgcGFuZWwtZGVmYXVsdCBwYW5lbC1mb3JtXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtaGVhZGluZ1wiPlxuICAgICAgICAgIDxoMyBjbGFzc05hbWU9XCJwYW5lbC10aXRsZVwiPntnZXR0ZXh0KFwiQ2hhbmdlIHVzZXJuYW1lXCIpfTwvaDM+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWJvZHlcIj5cblxuICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJOZXcgdXNlcm5hbWVcIil9IGZvcj1cImlkX3VzZXJuYW1lXCJcbiAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCJcbiAgICAgICAgICAgICAgICAgICAgIGhlbHBUZXh0PXt0aGlzLmdldEhlbHBUZXh0KCl9PlxuICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgaWQ9XCJpZF91c2VybmFtZVwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgndXNlcm5hbWUnKX1cbiAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS51c2VybmFtZX0gLz5cbiAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1mb290ZXJcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInJvd1wiPlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wtc20tOCBjb2wtc20tb2Zmc2V0LTRcIj5cblxuICAgICAgICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5XCIgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9PlxuICAgICAgICAgICAgICAgIHtnZXR0ZXh0KFwiQ2hhbmdlIHVzZXJuYW1lXCIpfVxuICAgICAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9mb3JtPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBOb0NoYW5nZXNMZWZ0IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0SGVscFRleHQoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMub3B0aW9ucy5uZXh0X29uKSB7XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUoXG4gICAgICAgICAgZ2V0dGV4dChcIllvdSB3aWxsIGJlIGFibGUgdG8gY2hhbmdlIHlvdXIgdXNlcm5hbWUgJShuZXh0X2NoYW5nZSlzLlwiKSxcbiAgICAgICAgICB7J25leHRfY2hhbmdlJzogdGhpcy5wcm9wcy5vcHRpb25zLm5leHRfb24uZnJvbU5vdygpfSwgdHJ1ZSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiWW91IGhhdmUgdXNlZCB1cCBhdmFpbGFibGUgbmFtZSBjaGFuZ2VzLlwiKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsIHBhbmVsLWRlZmF1bHQgcGFuZWwtZm9ybVwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1oZWFkaW5nXCI+XG4gICAgICAgIDxoMyBjbGFzc05hbWU9XCJwYW5lbC10aXRsZVwiPntnZXR0ZXh0KFwiQ2hhbmdlIHVzZXJuYW1lXCIpfTwvaDM+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtYm9keSBwYW5lbC1tZXNzYWdlLWJvZHlcIj5cblxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgIGluZm9fb3V0bGluZVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1ib2R5XCI+XG4gICAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgICAge2dldHRleHQoXCJZb3UgY2FuJ3QgY2hhbmdlIHlvdXIgdXNlcm5hbWUgYXQgdGhlIG1vbWVudC5cIil9XG4gICAgICAgICAgPC9wPlxuICAgICAgICAgIDxwIGNsYXNzTmFtZT1cImhlbHAtYmxvY2tcIj5cbiAgICAgICAgICAgIHt0aGlzLmdldEhlbHBUZXh0KCl9XG4gICAgICAgICAgPC9wPlxuICAgICAgICA8L2Rpdj5cblxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIENoYW5nZVVzZXJuYW1lTG9hZGluZyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwgcGFuZWwtZGVmYXVsdCBwYW5lbC1mb3JtXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWhlYWRpbmdcIj5cbiAgICAgICAgPGgzIGNsYXNzTmFtZT1cInBhbmVsLXRpdGxlXCI+e2dldHRleHQoXCJDaGFuZ2UgdXNlcm5hbWVcIil9PC9oMz5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1ib2R5IHBhbmVsLWJvZHktbG9hZGluZ1wiPlxuXG4gICAgICAgIDxMb2FkZXIgY2xhc3NOYW1lPVwibG9hZGVyIGxvYWRlci1zcGFjZWRcIiAvPlxuXG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgVXNlcm5hbWVIaXN0b3J5IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyVXNlckF2YXRhcihpdGVtKSB7XG4gICAgaWYgKGl0ZW0uY2hhbmdlZF9ieSkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxhIGhyZWY9e2l0ZW0uY2hhbmdlZF9ieS5hYnNvbHV0ZV91cmx9IGNsYXNzTmFtZT1cInVzZXItYXZhdGFyXCI+XG4gICAgICAgIDxBdmF0YXIgdXNlcj17aXRlbS5jaGFuZ2VkX2J5fSBzaXplPVwiMTAwXCIgLz5cbiAgICAgIDwvYT47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPHNwYW4gY2xhc3NOYW1lPVwidXNlci1hdmF0YXJcIj5cbiAgICAgICAgPEF2YXRhciBzaXplPVwiMTAwXCIgLz5cbiAgICAgIDwvc3Bhbj47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlclVzZXJuYW1lKGl0ZW0pIHtcbiAgICBpZiAoaXRlbS5jaGFuZ2VkX2J5KSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPGEgaHJlZj17aXRlbS5jaGFuZ2VkX2J5LmFic29sdXRlX3VybH0gY2xhc3NOYW1lPVwiaXRlbS10aXRsZVwiPlxuICAgICAgICB7aXRlbS5jaGFuZ2VkX2J5LnVzZXJuYW1lfVxuICAgICAgPC9hPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8c3BhbiBjbGFzc05hbWU9XCJpdGVtLXRpdGxlXCI+XG4gICAgICAgIHtpdGVtLmNoYW5nZWRfYnlfdXNlcm5hbWV9XG4gICAgICA8L3NwYW4+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cblxuICByZW5kZXJIaXN0b3J5KCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJ1c2VybmFtZS1oaXN0b3J5IHVpLXJlYWR5XCI+XG4gICAgICA8dWwgY2xhc3NOYW1lPVwibGlzdC1ncm91cFwiPlxuICAgICAgICB7dGhpcy5wcm9wcy5jaGFuZ2VzLm1hcCgoaXRlbSkgPT4ge1xuICAgICAgICAgIHJldHVybiA8bGkgY2xhc3NOYW1lPVwibGlzdC1ncm91cC1pdGVtXCIga2V5PXtpdGVtLmlkfT5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtY2hhbmdlLWF2YXRhclwiPlxuICAgICAgICAgICAgICB7dGhpcy5yZW5kZXJVc2VyQXZhdGFyKGl0ZW0pfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVzZXJuYW1lLWNoYW5nZS1hdXRob3JcIj5cbiAgICAgICAgICAgICAge3RoaXMucmVuZGVyVXNlcm5hbWUoaXRlbSl9XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtY2hhbmdlXCI+XG4gICAgICAgICAgICAgIHtpdGVtLm9sZF91c2VybmFtZX1cbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgICAgIGFycm93X2ZvcndhcmRcbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgICB7aXRlbS5uZXdfdXNlcm5hbWV9XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtY2hhbmdlLWRhdGVcIj5cbiAgICAgICAgICAgICAgPGFiYnIgdGl0bGU9e2l0ZW0uY2hhbmdlZF9vbi5mb3JtYXQoJ0xMTCcpfT5cbiAgICAgICAgICAgICAgICB7aXRlbS5jaGFuZ2VkX29uLmZyb21Ob3coKX1cbiAgICAgICAgICAgICAgPC9hYmJyPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9saT47XG4gICAgICAgIH0pfVxuICAgICAgPC91bD5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxuXG4gIHJlbmRlckVtcHR5SGlzdG9yeSgpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtaGlzdG9yeSB1aS1yZWFkeVwiPlxuICAgICAgPHVsIGNsYXNzTmFtZT1cImxpc3QtZ3JvdXBcIj5cbiAgICAgICAgPGxpIGNsYXNzTmFtZT1cImxpc3QtZ3JvdXAtaXRlbSBlbXB0eS1tZXNzYWdlXCI+XG4gICAgICAgICAge2dldHRleHQoXCJObyBuYW1lIGNoYW5nZXMgaGF2ZSBiZWVuIHJlY29yZGVkIGZvciB5b3VyIGFjY291bnQuXCIpfVxuICAgICAgICA8L2xpPlxuICAgICAgPC91bD5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxuXG4gIHJlbmRlckhpc3RvcnlQcmV2aWV3KCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJ1c2VybmFtZS1oaXN0b3J5IHVpLXByZXZpZXdcIj5cbiAgICAgIDx1bCBjbGFzc05hbWU9XCJsaXN0LWdyb3VwXCI+XG4gICAgICAgIHtyYW5kb20ucmFuZ2UoMywgNSkubWFwKChpKSA9PiB7XG4gICAgICAgICAgcmV0dXJuIDxsaSBjbGFzc05hbWU9XCJsaXN0LWdyb3VwLWl0ZW1cIiBrZXk9e2l9PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ1c2VybmFtZS1jaGFuZ2UtYXZhdGFyXCI+XG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInVzZXItYXZhdGFyXCI+XG4gICAgICAgICAgICAgICAgPEF2YXRhciBzaXplPVwiMTAwXCIgLz5cbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVzZXJuYW1lLWNoYW5nZS1hdXRob3JcIj5cbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwidWktcHJldmlldy10ZXh0XCIgc3R5bGU9e3t3aWR0aDogcmFuZG9tLmludCgzMCwgMTAwKSArIFwicHhcIn19PiZuYnNwOzwvc3Bhbj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ1c2VybmFtZS1jaGFuZ2VcIj5cbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwidWktcHJldmlldy10ZXh0XCIgc3R5bGU9e3t3aWR0aDogcmFuZG9tLmludCgzMCwgNTApICsgXCJweFwifX0+Jm5ic3A7PC9zcGFuPlxuICAgICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgICAgYXJyb3dfZm9yd2FyZFxuICAgICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInVpLXByZXZpZXctdGV4dFwiIHN0eWxlPXt7d2lkdGg6IHJhbmRvbS5pbnQoMzAsIDUwKSArIFwicHhcIn19PiZuYnNwOzwvc3Bhbj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ1c2VybmFtZS1jaGFuZ2UtZGF0ZVwiPlxuICAgICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJ1aS1wcmV2aWV3LXRleHRcIiBzdHlsZT17e3dpZHRoOiByYW5kb20uaW50KDUwLCAxMDApICsgXCJweFwifX0+Jm5ic3A7PC9zcGFuPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9saT5cbiAgICAgICAgfSl9XG4gICAgICA8L3VsPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIGlmICh0aGlzLnByb3BzLmlzTG9hZGVkKSB7XG4gICAgICBpZiAodGhpcy5wcm9wcy5jaGFuZ2VzLmxlbmd0aCkge1xuICAgICAgICByZXR1cm4gdGhpcy5yZW5kZXJIaXN0b3J5KCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gdGhpcy5yZW5kZXJFbXB0eUhpc3RvcnkoKTtcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHRoaXMucmVuZGVySGlzdG9yeVByZXZpZXcoKTtcbiAgICB9XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBpc0xvYWRlZDogZmFsc2UsXG4gICAgICBvcHRpb25zOiBudWxsXG4gICAgfTtcbiAgfVxuXG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIHRpdGxlLnNldCh7XG4gICAgICB0aXRsZTogZ2V0dGV4dChcIkNoYW5nZSB1c2VybmFtZVwiKSxcbiAgICAgIHBhcmVudDogZ2V0dGV4dChcIkNoYW5nZSB5b3VyIG9wdGlvbnNcIilcbiAgICB9KTtcblxuICAgIFByb21pc2UuYWxsKFtcbiAgICAgIGFqYXguZ2V0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLnVzZXJuYW1lKSxcbiAgICAgIGFqYXguZ2V0KG1pc2Fnby5nZXQoJ1VTRVJOQU1FX0NIQU5HRVNfQVBJJyksIHt1c2VyOiB0aGlzLnByb3BzLnVzZXIuaWR9KVxuICAgIF0pLnRoZW4oKGRhdGEpID0+IHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICBpc0xvYWRlZDogdHJ1ZSxcbiAgICAgICAgb3B0aW9uczoge1xuICAgICAgICAgIGNoYW5nZXNfbGVmdDogZGF0YVswXS5jaGFuZ2VzX2xlZnQsXG4gICAgICAgICAgbGVuZ3RoX21pbjogZGF0YVswXS5sZW5ndGhfbWluLFxuICAgICAgICAgIGxlbmd0aF9tYXg6IGRhdGFbMF0ubGVuZ3RoX21heCxcbiAgICAgICAgICBuZXh0X29uOiBkYXRhWzBdLm5leHRfb24gPyBtb21lbnQoZGF0YVswXS5uZXh0X29uKSA6IG51bGwsXG4gICAgICAgIH1cbiAgICAgIH0pO1xuXG4gICAgICBzdG9yZS5kaXNwYXRjaChkZWh5ZHJhdGUoZGF0YVsxXS5yZXN1bHRzKSk7XG4gICAgfSk7XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIG9uQ29tcGxldGUgPSAodXNlcm5hbWUsIHNsdWcsIG9wdGlvbnMpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIG9wdGlvbnNcbiAgICB9KTtcblxuICAgIHN0b3JlLmRpc3BhdGNoKFxuICAgICAgYWRkTmFtZUNoYW5nZSh7IHVzZXJuYW1lLCBzbHVnIH0sIHRoaXMucHJvcHMudXNlciwgdGhpcy5wcm9wcy51c2VyKSk7XG4gICAgc3RvcmUuZGlzcGF0Y2goXG4gICAgICB1cGRhdGVVc2VybmFtZSh0aGlzLnByb3BzLnVzZXIsIHVzZXJuYW1lLCBzbHVnKSk7XG5cbiAgICBzbmFja2Jhci5zdWNjZXNzKGdldHRleHQoXCJZb3VyIHVzZXJuYW1lIGhhcyBiZWVuIGNoYW5nZWQgc3VjY2Vzc2Z1bGx5LlwiKSk7XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgZ2V0Q2hhbmdlRm9ybSgpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRlZCkge1xuICAgICAgaWYgKHRoaXMuc3RhdGUub3B0aW9ucy5jaGFuZ2VzX2xlZnQgPiAwKSB7XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgICAgcmV0dXJuIDxDaGFuZ2VVc2VybmFtZSB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgb3B0aW9ucz17dGhpcy5zdGF0ZS5vcHRpb25zfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbXBsZXRlPXt0aGlzLm9uQ29tcGxldGV9IC8+O1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgICByZXR1cm4gPE5vQ2hhbmdlc0xlZnQgb3B0aW9ucz17dGhpcy5zdGF0ZS5vcHRpb25zfSAvPjtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxDaGFuZ2VVc2VybmFtZUxvYWRpbmcgLz47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXY+XG4gICAgICB7dGhpcy5nZXRDaGFuZ2VGb3JtKCl9XG4gICAgICA8VXNlcm5hbWVIaXN0b3J5IGlzTG9hZGVkPXt0aGlzLnN0YXRlLmlzTG9hZGVkfVxuICAgICAgICAgICAgICAgICAgICAgICBjaGFuZ2VzPXt0aGlzLnByb3BzWyd1c2VybmFtZS1oaXN0b3J5J119IC8+XG4gICAgPC9kaXY+XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IEZvcm1Hcm91cCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtLWdyb3VwJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgU2VsZWN0IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3NlbGVjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFllc05vU3dpdGNoIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3llcy1uby1zd2l0Y2gnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCB7IHBhdGNoVXNlciB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9hdXRoJztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCB0aXRsZSBmcm9tICdtaXNhZ28vc2VydmljZXMvcGFnZS10aXRsZSc7XG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG5cbiAgICAgICdpc19oaWRpbmdfcHJlc2VuY2UnOiBwcm9wcy51c2VyLmlzX2hpZGluZ19wcmVzZW5jZSxcbiAgICAgICdsaW1pdHNfcHJpdmF0ZV90aHJlYWRfaW52aXRlc190byc6IHByb3BzLnVzZXIubGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG8sXG4gICAgICAnc3Vic2NyaWJlX3RvX3N0YXJ0ZWRfdGhyZWFkcyc6IHByb3BzLnVzZXIuc3Vic2NyaWJlX3RvX3N0YXJ0ZWRfdGhyZWFkcyxcbiAgICAgICdzdWJzY3JpYmVfdG9fcmVwbGllZF90aHJlYWRzJzogcHJvcHMudXNlci5zdWJzY3JpYmVfdG9fcmVwbGllZF90aHJlYWRzLFxuXG4gICAgICAnZXJyb3JzJzoge31cbiAgICB9O1xuXG4gICAgdGhpcy5wcml2YXRlVGhyZWFkSW52aXRlc0Nob2ljZXMgPSBbXG4gICAgICB7XG4gICAgICAgICd2YWx1ZSc6IDAsXG4gICAgICAgICdpY29uJzogJ2hlbHBfb3V0bGluZScsXG4gICAgICAgICdsYWJlbCc6IGdldHRleHQoJ0V2ZXJ5Ym9keScpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAndmFsdWUnOiAxLFxuICAgICAgICAnaWNvbic6ICdkb25lX2FsbCcsXG4gICAgICAgICdsYWJlbCc6IGdldHRleHQoJ1VzZXJzIEkgZm9sbG93JylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgICd2YWx1ZSc6IDIsXG4gICAgICAgICdpY29uJzogJ2hpZ2hsaWdodF9vZmYnLFxuICAgICAgICAnbGFiZWwnOiBnZXR0ZXh0KCdOb2JvZHknKVxuICAgICAgfVxuICAgIF07XG5cbiAgICB0aGlzLnN1YnNjcmliZVRvQ2hvaWNlcyA9IFtcbiAgICAgIHtcbiAgICAgICAgJ3ZhbHVlJzogMCxcbiAgICAgICAgJ2ljb24nOiAnYm9va21hcmtfYm9yZGVyJyxcbiAgICAgICAgJ2xhYmVsJzogZ2V0dGV4dCgnTm8nKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgJ3ZhbHVlJzogMSxcbiAgICAgICAgJ2ljb24nOiAnYm9va21hcmsnLFxuICAgICAgICAnbGFiZWwnOiBnZXR0ZXh0KCdCb29rbWFyaycpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAndmFsdWUnOiAyLFxuICAgICAgICAnaWNvbic6ICdtYWlsJyxcbiAgICAgICAgJ2xhYmVsJzogZ2V0dGV4dCgnQm9va21hcmsgd2l0aCBlLW1haWwgbm90aWZpY2F0aW9uJylcbiAgICAgIH1cbiAgICBdO1xuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLm9wdGlvbnMsIHtcbiAgICAgICdpc19oaWRpbmdfcHJlc2VuY2UnOiB0aGlzLnN0YXRlLmlzX2hpZGluZ19wcmVzZW5jZSxcbiAgICAgICdsaW1pdHNfcHJpdmF0ZV90aHJlYWRfaW52aXRlc190byc6IHRoaXMuc3RhdGUubGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG8sXG4gICAgICAnc3Vic2NyaWJlX3RvX3N0YXJ0ZWRfdGhyZWFkcyc6IHRoaXMuc3RhdGUuc3Vic2NyaWJlX3RvX3N0YXJ0ZWRfdGhyZWFkcyxcbiAgICAgICdzdWJzY3JpYmVfdG9fcmVwbGllZF90aHJlYWRzJzogdGhpcy5zdGF0ZS5zdWJzY3JpYmVfdG9fcmVwbGllZF90aHJlYWRzXG4gICAgfSk7XG4gIH1cblxuICBoYW5kbGVTdWNjZXNzKCkge1xuICAgIHN0b3JlLmRpc3BhdGNoKHBhdGNoVXNlcih7XG4gICAgICAnaXNfaGlkaW5nX3ByZXNlbmNlJzogdGhpcy5zdGF0ZS5pc19oaWRpbmdfcHJlc2VuY2UsXG4gICAgICAnbGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG8nOiB0aGlzLnN0YXRlLmxpbWl0c19wcml2YXRlX3RocmVhZF9pbnZpdGVzX3RvLFxuICAgICAgJ3N1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHMnOiB0aGlzLnN0YXRlLnN1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHMsXG4gICAgICAnc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkcyc6IHRoaXMuc3RhdGUuc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkc1xuICAgIH0pKTtcbiAgICBzbmFja2Jhci5zdWNjZXNzKGdldHRleHQoXCJZb3VyIGZvcnVtIG9wdGlvbnMgaGF2ZSBiZWVuIGNoYW5nZWQuXCIpKTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJQbGVhc2UgcmVsb2FkIHBhZ2UgYW5kIHRyeSBhZ2Fpbi5cIikpO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIHRpdGxlLnNldCh7XG4gICAgICB0aXRsZTogZ2V0dGV4dChcIkZvcnVtIG9wdGlvbnNcIiksXG4gICAgICBwYXJlbnQ6IGdldHRleHQoXCJDaGFuZ2UgeW91ciBvcHRpb25zXCIpXG4gICAgfSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8Zm9ybSBvblN1Ym1pdD17dGhpcy5oYW5kbGVTdWJtaXR9IGNsYXNzTmFtZT1cImZvcm0taG9yaXpvbnRhbFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbCBwYW5lbC1kZWZhdWx0IHBhbmVsLWZvcm1cIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1oZWFkaW5nXCI+XG4gICAgICAgICAgPGgzIGNsYXNzTmFtZT1cInBhbmVsLXRpdGxlXCI+e2dldHRleHQoXCJDaGFuZ2UgZm9ydW0gb3B0aW9uc1wiKX08L2gzPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1ib2R5XCI+XG5cbiAgICAgICAgICA8ZmllbGRzZXQ+XG4gICAgICAgICAgICA8bGVnZW5kPntnZXR0ZXh0KFwiUHJpdmFjeSBzZXR0aW5nc1wiKX08L2xlZ2VuZD5cblxuICAgICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIkhpZGUgbXkgcHJlc2VuY2VcIil9XG4gICAgICAgICAgICAgICAgICAgICAgIGhlbHBUZXh0PXtnZXR0ZXh0KFwiSWYgeW91IGhpZGUgeW91ciBwcmVzZW5jZSwgb25seSBtZW1iZXJzIHdpdGggcGVybWlzc2lvbiB0byBzZWUgaGlkZGVuIHVzZXJzIHdpbGwgc2VlIHdoZW4geW91IGFyZSBvbmxpbmUuXCIpfVxuICAgICAgICAgICAgICAgICAgICAgICBmb3I9XCJpZF9pc19oaWRpbmdfcHJlc2VuY2VcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiPlxuICAgICAgICAgICAgICA8WWVzTm9Td2l0Y2ggaWQ9XCJpZF9pc19oaWRpbmdfcHJlc2VuY2VcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgaWNvbk9uPVwidmlzaWJpbGl0eVwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgICBpY29uT2ZmPVwidmlzaWJpbGl0eV9vZmZcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgbGFiZWxPbj17Z2V0dGV4dChcIlNob3cgbXkgcHJlc2VuY2UgdG8gb3RoZXIgdXNlcnNcIil9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICBsYWJlbE9mZj17Z2V0dGV4dChcIkhpZGUgbXkgcHJlc2VuY2UgZnJvbSBvdGhlciB1c2Vyc1wiKX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnaXNfaGlkaW5nX3ByZXNlbmNlJyl9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5pc19oaWRpbmdfcHJlc2VuY2V9IC8+XG4gICAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIlByaXZhdGUgdGhyZWFkIGludml0YXRpb25zXCIpfVxuICAgICAgICAgICAgICAgICAgICAgICBmb3I9XCJpZF9saW1pdHNfcHJpdmF0ZV90aHJlYWRfaW52aXRlc190b1wiXG4gICAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCI+XG4gICAgICAgICAgICAgIDxTZWxlY3QgaWQ9XCJpZF9saW1pdHNfcHJpdmF0ZV90aHJlYWRfaW52aXRlc190b1wiXG4gICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnbGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG8nKX1cbiAgICAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5saW1pdHNfcHJpdmF0ZV90aHJlYWRfaW52aXRlc190b31cbiAgICAgICAgICAgICAgICAgICAgICBjaG9pY2VzPXt0aGlzLnByaXZhdGVUaHJlYWRJbnZpdGVzQ2hvaWNlc30gLz5cbiAgICAgICAgICAgIDwvRm9ybUdyb3VwPlxuICAgICAgICAgIDwvZmllbGRzZXQ+XG5cbiAgICAgICAgICA8ZmllbGRzZXQ+XG4gICAgICAgICAgICA8bGVnZW5kPntnZXR0ZXh0KFwiQXV0b21hdGljIHN1YnNjcmlwdGlvbnNcIil9PC9sZWdlbmQ+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJUaHJlYWRzIEkgc3RhcnRcIil9XG4gICAgICAgICAgICAgICAgICAgICAgIGZvcj1cImlkX3N1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHNcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiPlxuICAgICAgICAgICAgICA8U2VsZWN0IGlkPVwiaWRfc3Vic2NyaWJlX3RvX3N0YXJ0ZWRfdGhyZWFkc1wiXG4gICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnc3Vic2NyaWJlX3RvX3N0YXJ0ZWRfdGhyZWFkcycpfVxuICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnN1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHN9XG4gICAgICAgICAgICAgICAgICAgICAgY2hvaWNlcz17dGhpcy5zdWJzY3JpYmVUb0Nob2ljZXN9IC8+XG4gICAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIlRocmVhZHMgSSByZXBseSB0b1wiKX1cbiAgICAgICAgICAgICAgICAgICAgICAgZm9yPVwiaWRfc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkc1wiXG4gICAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCI+XG4gICAgICAgICAgICAgIDxTZWxlY3QgaWQ9XCJpZF9zdWJzY3JpYmVfdG9fcmVwbGllZF90aHJlYWRzXCJcbiAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdzdWJzY3JpYmVfdG9fcmVwbGllZF90aHJlYWRzJyl9XG4gICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUuc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkc31cbiAgICAgICAgICAgICAgICAgICAgICBjaG9pY2VzPXt0aGlzLnN1YnNjcmliZVRvQ2hvaWNlc30gLz5cbiAgICAgICAgICAgIDwvRm9ybUdyb3VwPlxuICAgICAgICAgIDwvZmllbGRzZXQ+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtZm9vdGVyXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLXNtLTggY29sLXNtLW9mZnNldC00XCI+XG5cbiAgICAgICAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeVwiIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICAgICAgICB7Z2V0dGV4dChcIlNhdmUgY2hhbmdlc1wiKX1cbiAgICAgICAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZm9ybT5cbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IExpbmsgfSBmcm9tICdyZWFjdC1yb3V0ZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBMaSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9saSc7IC8vanNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7IC8vanNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBjbGFzcyBTaWRlTmF2IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8vIGpzaGludCBpZ25vcmU6c3RhcnRcbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJsaXN0LWdyb3VwIG5hdi1zaWRlXCI+XG4gICAgICB7dGhpcy5wcm9wcy5vcHRpb25zLm1hcCgob3B0aW9uKSA9PiB7XG4gICAgICAgIHJldHVybiA8TGluayB0bz17dGhpcy5wcm9wcy5iYXNlVXJsICsgb3B0aW9uLmNvbXBvbmVudCArICcvJ31cbiAgICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImxpc3QtZ3JvdXAtaXRlbVwiXG4gICAgICAgICAgICAgICAgICAgICBhY3RpdmVDbGFzc05hbWU9XCJhY3RpdmVcIlxuICAgICAgICAgICAgICAgICAgICAga2V5PXtvcHRpb24uY29tcG9uZW50fT5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICB7b3B0aW9uLmljb259XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIHtvcHRpb24ubmFtZX1cbiAgICAgICAgPC9MaW5rPjtcbiAgICAgIH0pfVxuICAgIDwvZGl2PjtcbiAgICAvLyBqc2hpbnQgaWdub3JlOmVuZFxuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBDb21wYWN0TmF2IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8vIGpzaGludCBpZ25vcmU6c3RhcnRcbiAgICByZXR1cm4gPHVsIGNsYXNzTmFtZT1cImRyb3Bkb3duLW1lbnVcIiByb2xlPVwibWVudVwiPlxuICAgICAge3RoaXMucHJvcHMub3B0aW9ucy5tYXAoKG9wdGlvbikgPT4ge1xuICAgICAgICByZXR1cm4gPExpIHBhdGg9e3RoaXMucHJvcHMuYmFzZVVybCArIG9wdGlvbi5jb21wb25lbnQgKyAnLyd9XG4gICAgICAgICAgICAgICAgICAga2V5PXtvcHRpb24uY29tcG9uZW50fT5cbiAgICAgICAgICA8TGluayB0bz17dGhpcy5wcm9wcy5iYXNlVXJsICsgb3B0aW9uLmNvbXBvbmVudCArICcvJ30+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgIHtvcHRpb24uaWNvbn1cbiAgICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICAgIHtvcHRpb24ubmFtZX1cbiAgICAgICAgICA8L0xpbms+XG4gICAgICAgIDwvTGk+O1xuICAgICAgfSl9XG4gICAgPC91bD47XG4gICAgLy8ganNoaW50IGlnbm9yZTplbmRcbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBjb25uZWN0IH0gZnJvbSAncmVhY3QtcmVkdXgnO1xuaW1wb3J0IHsgU2lkZU5hdiwgQ29tcGFjdE5hdiB9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL29wdGlvbnMvbmF2cyc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IENoYW5nZUZvcnVtT3B0aW9ucyBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9vcHRpb25zL2ZvcnVtLW9wdGlvbnMnO1xuaW1wb3J0IENoYW5nZVVzZXJuYW1lIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL29wdGlvbnMvY2hhbmdlLXVzZXJuYW1lJztcbmltcG9ydCBDaGFuZ2VTaWduSW5DcmVkZW50aWFscyBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9vcHRpb25zL3NpZ24taW4tY3JlZGVudGlhbHMnO1xuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgIGRyb3Bkb3duOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHRvZ2dsZU5hdiA9ICgpID0+IHtcbiAgICBpZiAodGhpcy5zdGF0ZS5kcm9wZG93bikge1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgIGRyb3Bkb3duOiBmYWxzZVxuICAgICAgfSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICBkcm9wZG93bjogdHJ1ZVxuICAgICAgfSk7XG4gICAgfVxuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIGdldFRvZ2dsZU5hdkNsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5kcm9wZG93bikge1xuICAgICAgcmV0dXJuICdidG4gYnRuLWRlZmF1bHQgYnRuLWljb24gb3Blbic7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiAnYnRuIGJ0bi1kZWZhdWx0IGJ0bi1pY29uJztcbiAgICB9XG4gIH1cblxuICBnZXRDb21wYWN0TmF2Q2xhc3NOYW1lKCkge1xuICAgIGlmICh0aGlzLnN0YXRlLmRyb3Bkb3duKSB7XG4gICAgICByZXR1cm4gJ2NvbXBhY3QtbmF2IG9wZW4nO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gJ2NvbXBhY3QtbmF2JztcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UgcGFnZS1vcHRpb25zXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UtaGVhZGVyXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG5cbiAgICAgICAgICA8aDEgY2xhc3NOYW1lPVwicHVsbC1sZWZ0XCI+e2dldHRleHQoXCJDaGFuZ2UgeW91ciBvcHRpb25zXCIpfTwvaDE+XG5cbiAgICAgICAgICA8YnV0dG9uIGNsYXNzTmFtZT1cImJ0biBidG4tZGVmYXVsdCBidG4taWNvbiBidG4tZHJvcGRvd24tdG9nZ2xlIGhpZGRlbi1tZCBoaWRkZW4tbGdcIlxuICAgICAgICAgICAgICAgICAgdHlwZT1cImJ1dHRvblwiXG4gICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnRvZ2dsZU5hdn1cbiAgICAgICAgICAgICAgICAgIGFyaWEtaGFzcG9wdXA9XCJ0cnVlXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtZXhwYW5kZWQ9e3RoaXMuc3RhdGUuZHJvcGRvd24gPyAndHJ1ZScgOiAnZmFsc2UnfT5cbiAgICAgICAgICAgIDxpIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgICAgbWVudVxuICAgICAgICAgICAgPC9pPlxuICAgICAgICAgIDwvYnV0dG9uPlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRDb21wYWN0TmF2Q2xhc3NOYW1lKCl9PlxuXG4gICAgICAgIDxDb21wYWN0TmF2IG9wdGlvbnM9e21pc2Fnby5nZXQoJ1VTRVJfT1BUSU9OUycpfVxuICAgICAgICAgICAgICAgICAgICBiYXNlVXJsPXttaXNhZ28uZ2V0KCdVU0VSQ1BfVVJMJyl9IC8+XG5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cblxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInJvd1wiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLW1kLTMgaGlkZGVuLXhzIGhpZGRlbi1zbVwiPlxuXG4gICAgICAgICAgICA8U2lkZU5hdiBvcHRpb25zPXttaXNhZ28uZ2V0KCdVU0VSX09QVElPTlMnKX1cbiAgICAgICAgICAgICAgICAgICAgIGJhc2VVcmw9e21pc2Fnby5nZXQoJ1VTRVJDUF9VUkwnKX0gLz5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLW1kLTlcIj5cblxuICAgICAgICAgICAge3RoaXMucHJvcHMuY2hpbGRyZW59XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzZWxlY3Qoc3RvcmUpIHtcbiAgcmV0dXJuIHtcbiAgICAndGljayc6IHN0b3JlLnRpY2sudGljayxcbiAgICAndXNlcic6IHN0b3JlLmF1dGgudXNlcixcbiAgICAndXNlcm5hbWUtaGlzdG9yeSc6IHN0b3JlWyd1c2VybmFtZS1oaXN0b3J5J11cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHBhdGhzKCkge1xuICByZXR1cm4gW1xuICAgIHtcbiAgICAgIHBhdGg6IG1pc2Fnby5nZXQoJ1VTRVJDUF9VUkwnKSArICdmb3J1bS1vcHRpb25zLycsXG4gICAgICBjb21wb25lbnQ6IGNvbm5lY3Qoc2VsZWN0KShDaGFuZ2VGb3J1bU9wdGlvbnMpXG4gICAgfSxcbiAgICB7XG4gICAgICBwYXRoOiBtaXNhZ28uZ2V0KCdVU0VSQ1BfVVJMJykgKyAnY2hhbmdlLXVzZXJuYW1lLycsXG4gICAgICBjb21wb25lbnQ6IGNvbm5lY3Qoc2VsZWN0KShDaGFuZ2VVc2VybmFtZSlcbiAgICB9LFxuICAgIHtcbiAgICAgIHBhdGg6IG1pc2Fnby5nZXQoJ1VTRVJDUF9VUkwnKSArICdzaWduLWluLWNyZWRlbnRpYWxzLycsXG4gICAgICBjb21wb25lbnQ6IGNvbm5lY3Qoc2VsZWN0KShDaGFuZ2VTaWduSW5DcmVkZW50aWFscylcbiAgICB9XG4gIF07XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IEZvcm1Hcm91cCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtLWdyb3VwJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5pbXBvcnQgdGl0bGUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3BhZ2UtdGl0bGUnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgKiBhcyB2YWxpZGF0b3JzIGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcblxuZXhwb3J0IGNsYXNzIENoYW5nZUVtYWlsIGV4dGVuZHMgRm9ybSB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgIG5ld19lbWFpbDogJycsXG4gICAgICBwYXNzd29yZDogJycsXG5cbiAgICAgIHZhbGlkYXRvcnM6IHtcbiAgICAgICAgbmV3X2VtYWlsOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy5lbWFpbCgpXG4gICAgICAgIF0sXG4gICAgICAgIHBhc3N3b3JkOiBbXVxuICAgICAgfSxcblxuICAgICAgaXNMb2FkaW5nOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBsZXQgZXJyb3JzID0gdGhpcy52YWxpZGF0ZSgpO1xuICAgIGxldCBsZW5ndGhzID0gW1xuICAgICAgdGhpcy5zdGF0ZS5uZXdfZW1haWwudHJpbSgpLmxlbmd0aCxcbiAgICAgIHRoaXMuc3RhdGUucGFzc3dvcmQudHJpbSgpLmxlbmd0aFxuICAgIF07XG5cbiAgICBpZiAobGVuZ3Rocy5pbmRleE9mKDApICE9PSAtMSkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZpbGwgb3V0IGFsbCBmaWVsZHMuXCIpKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICBpZiAoZXJyb3JzLm5ld19lbWFpbCkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZXJyb3JzLm5ld19lbWFpbFswXSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBhamF4LnBvc3QodGhpcy5wcm9wcy51c2VyLmFwaV91cmwuY2hhbmdlX2VtYWlsLCB7XG4gICAgICBuZXdfZW1haWw6IHRoaXMuc3RhdGUubmV3X2VtYWlsLFxuICAgICAgcGFzc3dvcmQ6IHRoaXMuc3RhdGUucGFzc3dvcmQsXG4gICAgfSk7XG4gIH1cblxuICBoYW5kbGVTdWNjZXNzKHJlc3BvbnNlKSB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBuZXdfZW1haWw6ICcnLFxuICAgICAgcGFzc3dvcmQ6ICcnXG4gICAgfSk7XG5cbiAgICBzbmFja2Jhci5zdWNjZXNzKHJlc3BvbnNlLmRldGFpbCk7XG4gIH1cblxuICBoYW5kbGVFcnJvcihyZWplY3Rpb24pIHtcbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAwKSB7XG4gICAgICBpZiAocmVqZWN0aW9uLm5ld19lbWFpbCkge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24ubmV3X2VtYWlsKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHNuYWNrYmFyLmVycm9yKHJlamVjdGlvbi5wYXNzd29yZCk7XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmFwaUVycm9yKHJlamVjdGlvbik7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fSBjbGFzc05hbWU9XCJmb3JtLWhvcml6b250YWxcIj5cbiAgICAgIDxpbnB1dCB0eXBlPVwidHlwZVwiIHN0eWxlPXt7ZGlzcGxheTogJ25vbmUnfX0gLz5cbiAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBzdHlsZT17e2Rpc3BsYXk6ICdub25lJ319IC8+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsIHBhbmVsLWRlZmF1bHQgcGFuZWwtZm9ybVwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWhlYWRpbmdcIj5cbiAgICAgICAgICA8aDMgY2xhc3NOYW1lPVwicGFuZWwtdGl0bGVcIj57Z2V0dGV4dChcIkNoYW5nZSBlLW1haWwgYWRkcmVzc1wiKX08L2gzPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1ib2R5XCI+XG5cbiAgICAgICAgICA8Rm9ybUdyb3VwIGxhYmVsPXtnZXR0ZXh0KFwiTmV3IGUtbWFpbFwiKX0gZm9yPVwiaWRfbmV3X2VtYWlsXCJcbiAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCI+XG4gICAgICAgICAgICA8aW5wdXQgdHlwZT1cInRleHRcIiBpZD1cImlkX25ld19lbWFpbFwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnbmV3X2VtYWlsJyl9XG4gICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUubmV3X2VtYWlsfSAvPlxuICAgICAgICAgIDwvRm9ybUdyb3VwPlxuXG4gICAgICAgICAgPGhyIC8+XG5cbiAgICAgICAgICA8Rm9ybUdyb3VwIGxhYmVsPXtnZXR0ZXh0KFwiWW91ciBjdXJyZW50IHBhc3N3b3JkXCIpfSBmb3I9XCJpZF9wYXNzd29yZFwiXG4gICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiPlxuICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJwYXNzd29yZFwiIGlkPVwiaWRfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3Bhc3N3b3JkJyl9XG4gICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUucGFzc3dvcmR9IC8+XG4gICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtZm9vdGVyXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLXNtLTggY29sLXNtLW9mZnNldC00XCI+XG5cbiAgICAgICAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeVwiIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICAgICAgICB7Z2V0dGV4dChcIkNoYW5nZSBlLW1haWxcIil9XG4gICAgICAgICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Zvcm0+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIENoYW5nZVBhc3N3b3JkIGV4dGVuZHMgRm9ybSB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgIG5ld19wYXNzd29yZDogJycsXG4gICAgICByZXBlYXRfcGFzc3dvcmQ6ICcnLFxuICAgICAgcGFzc3dvcmQ6ICcnLFxuXG4gICAgICB2YWxpZGF0b3JzOiB7XG4gICAgICAgIG5ld19wYXNzd29yZDogW1xuICAgICAgICAgIHZhbGlkYXRvcnMucGFzc3dvcmRNaW5MZW5ndGgobWlzYWdvLmdldCgnU0VUVElOR1MnKSlcbiAgICAgICAgXSxcbiAgICAgICAgcmVwZWF0X3Bhc3N3b3JkOiBbXSxcbiAgICAgICAgcGFzc3dvcmQ6IFtdXG4gICAgICB9LFxuXG4gICAgICBpc0xvYWRpbmc6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGxldCBlcnJvcnMgPSB0aGlzLnZhbGlkYXRlKCk7XG4gICAgbGV0IGxlbmd0aHMgPSBbXG4gICAgICB0aGlzLnN0YXRlLm5ld19wYXNzd29yZC50cmltKCkubGVuZ3RoLFxuICAgICAgdGhpcy5zdGF0ZS5yZXBlYXRfcGFzc3dvcmQudHJpbSgpLmxlbmd0aCxcbiAgICAgIHRoaXMuc3RhdGUucGFzc3dvcmQudHJpbSgpLmxlbmd0aFxuICAgIF07XG5cbiAgICBpZiAobGVuZ3Rocy5pbmRleE9mKDApICE9PSAtMSkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZpbGwgb3V0IGFsbCBmaWVsZHMuXCIpKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICBpZiAoZXJyb3JzLm5ld19wYXNzd29yZCkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZXJyb3JzLm5ld19wYXNzd29yZFswXSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgaWYgKHRoaXMuc3RhdGUubmV3X3Bhc3N3b3JkLnRyaW0oKSAhPT0gdGhpcy5zdGF0ZS5yZXBlYXRfcGFzc3dvcmQudHJpbSgpKSB7XG4gICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiTmV3IHBhc3N3b3JkcyBhcmUgZGlmZmVyZW50LlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBhamF4LnBvc3QodGhpcy5wcm9wcy51c2VyLmFwaV91cmwuY2hhbmdlX3Bhc3N3b3JkLCB7XG4gICAgICBuZXdfcGFzc3dvcmQ6IHRoaXMuc3RhdGUubmV3X3Bhc3N3b3JkLFxuICAgICAgcGFzc3dvcmQ6IHRoaXMuc3RhdGUucGFzc3dvcmRcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3MocmVzcG9uc2UpIHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIG5ld19wYXNzd29yZDogJycsXG4gICAgICByZXBlYXRfcGFzc3dvcmQ6ICcnLFxuICAgICAgcGFzc3dvcmQ6ICcnXG4gICAgfSk7XG5cbiAgICBzbmFja2Jhci5zdWNjZXNzKHJlc3BvbnNlLmRldGFpbCk7XG4gIH1cblxuICBoYW5kbGVFcnJvcihyZWplY3Rpb24pIHtcbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAwKSB7XG4gICAgICBpZiAocmVqZWN0aW9uLm5ld19wYXNzd29yZCkge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24ubmV3X3Bhc3N3b3JkKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHNuYWNrYmFyLmVycm9yKHJlamVjdGlvbi5wYXNzd29yZCk7XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmFwaUVycm9yKHJlamVjdGlvbik7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fSBjbGFzc05hbWU9XCJmb3JtLWhvcml6b250YWxcIj5cbiAgICAgIDxpbnB1dCB0eXBlPVwidHlwZVwiIHN0eWxlPXt7ZGlzcGxheTogJ25vbmUnfX0gLz5cbiAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBzdHlsZT17e2Rpc3BsYXk6ICdub25lJ319IC8+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsIHBhbmVsLWRlZmF1bHQgcGFuZWwtZm9ybVwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWhlYWRpbmdcIj5cbiAgICAgICAgICA8aDMgY2xhc3NOYW1lPVwicGFuZWwtdGl0bGVcIj57Z2V0dGV4dChcIkNoYW5nZSBwYXNzd29yZFwiKX08L2gzPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1ib2R5XCI+XG5cbiAgICAgICAgICA8Rm9ybUdyb3VwIGxhYmVsPXtnZXR0ZXh0KFwiTmV3IHBhc3N3b3JkXCIpfSBmb3I9XCJpZF9uZXdfcGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz1cImNvbC1zbS00XCIgY29udHJvbENsYXNzPVwiY29sLXNtLThcIj5cbiAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBpZD1cImlkX25ld19wYXNzd29yZFwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnbmV3X3Bhc3N3b3JkJyl9XG4gICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUubmV3X3Bhc3N3b3JkfSAvPlxuICAgICAgICAgIDwvRm9ybUdyb3VwPlxuXG4gICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIlJlcGVhdCBwYXNzd29yZFwiKX0gZm9yPVwiaWRfcmVwZWF0X3Bhc3N3b3JkXCJcbiAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCI+XG4gICAgICAgICAgICA8aW5wdXQgdHlwZT1cInBhc3N3b3JkXCIgaWQ9XCJpZF9yZXBlYXRfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3JlcGVhdF9wYXNzd29yZCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnJlcGVhdF9wYXNzd29yZH0gLz5cbiAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgIDxociAvPlxuXG4gICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIllvdXIgY3VycmVudCBwYXNzd29yZFwiKX0gZm9yPVwiaWRfcGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz1cImNvbC1zbS00XCIgY29udHJvbENsYXNzPVwiY29sLXNtLThcIj5cbiAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBpZD1cImlkX3Bhc3N3b3JkXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdwYXNzd29yZCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnBhc3N3b3JkfSAvPlxuICAgICAgICAgIDwvRm9ybUdyb3VwPlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWZvb3RlclwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicm93XCI+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1zbS04IGNvbC1zbS1vZmZzZXQtNFwiPlxuXG4gICAgICAgICAgICAgIDxCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXByaW1hcnlcIiBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAgICAgICAge2dldHRleHQoXCJDaGFuZ2UgcGFzc3dvcmRcIil9XG4gICAgICAgICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Zvcm0+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICB0aXRsZS5zZXQoe1xuICAgICAgdGl0bGU6IGdldHRleHQoXCJDaGFuZ2UgZW1haWwgb3IgcGFzc3dvcmRcIiksXG4gICAgICBwYXJlbnQ6IGdldHRleHQoXCJDaGFuZ2UgeW91ciBvcHRpb25zXCIpXG4gICAgfSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2PlxuICAgICAgPENoYW5nZUVtYWlsIHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz5cbiAgICAgIDxDaGFuZ2VQYXNzd29yZCB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IC8+XG5cbiAgICAgIDxwIGNsYXNzTmFtZT1cIm1lc3NhZ2UtbGluZVwiPlxuICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgd2FybmluZ1xuICAgICAgICA8L3NwYW4+XG4gICAgICAgIDxhIGhyZWY9e21pc2Fnby5nZXQoJ0ZPUkdPVFRFTl9QQVNTV09SRF9VUkwnKX0+XG4gICAgICAgICAge2dldHRleHQoXCJDaGFuZ2UgZm9yZ290dGVuIHBhc3N3b3JkXCIpfVxuICAgICAgICA8L2E+XG4gICAgICA8L3A+XG4gICAgPC9kaXY+XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgenhjdmJuIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy96eGN2Ym4nO1xuXG5leHBvcnQgY29uc3QgU1RZTEVTID0gW1xuICAncHJvZ3Jlc3MtYmFyLWRhbmdlcicsXG4gICdwcm9ncmVzcy1iYXItd2FybmluZycsXG4gICdwcm9ncmVzcy1iYXItd2FybmluZycsXG4gICdwcm9ncmVzcy1iYXItcHJpbWFyeScsXG4gICdwcm9ncmVzcy1iYXItc3VjY2Vzcydcbl07XG5cbmV4cG9ydCBjb25zdCBMQUJFTFMgPSBbXG4gIGdldHRleHQoXCJFbnRlcmVkIHBhc3N3b3JkIGlzIHZlcnkgd2Vhay5cIiksXG4gIGdldHRleHQoXCJFbnRlcmVkIHBhc3N3b3JkIGlzIHdlYWsuXCIpLFxuICBnZXR0ZXh0KFwiRW50ZXJlZCBwYXNzd29yZCBpcyBhdmVyYWdlLlwiKSxcbiAgZ2V0dGV4dChcIkVudGVyZWQgcGFzc3dvcmQgaXMgc3Ryb25nLlwiKSxcbiAgZ2V0dGV4dChcIkVudGVyZWQgcGFzc3dvcmQgaXMgdmVyeSBzdHJvbmcuXCIpXG5dO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5fc2NvcmUgPSAwO1xuICAgIHRoaXMuX3Bhc3N3b3JkID0gbnVsbDtcbiAgICB0aGlzLl9pbnB1dHMgPSBbXTtcbiAgfVxuXG4gIGdldFNjb3JlKHBhc3N3b3JkLCBpbnB1dHMpIHtcbiAgICBsZXQgY2FjaGVTdGFsZSA9IGZhbHNlO1xuXG4gICAgaWYgKHBhc3N3b3JkLnRyaW0oKSAhPT0gdGhpcy5fcGFzc3dvcmQpIHtcbiAgICAgIGNhY2hlU3RhbGUgPSB0cnVlO1xuICAgIH1cblxuICAgIGlmIChpbnB1dHMubGVuZ3RoICE9PSB0aGlzLl9pbnB1dHMubGVuZ3RoKSB7XG4gICAgICBjYWNoZVN0YWxlID0gdHJ1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgaW5wdXRzLm1hcCgodmFsdWUsIGkpID0+IHtcbiAgICAgICAgaWYgKHZhbHVlLnRyaW0oKSAhPT0gdGhpcy5faW5wdXRzW2ldKSB7XG4gICAgICAgICAgY2FjaGVTdGFsZSA9IHRydWU7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGlmIChjYWNoZVN0YWxlKSB7XG4gICAgICB0aGlzLl9zY29yZSA9IHp4Y3Zibi5zY29yZVBhc3N3b3JkKHBhc3N3b3JkLCBpbnB1dHMpO1xuICAgICAgdGhpcy5fcGFzc3dvcmQgPSBwYXNzd29yZC50cmltKCk7XG4gICAgICB0aGlzLl9pbnB1dHMgPSBpbnB1dHMubWFwKGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgICAgIHJldHVybiB2YWx1ZS50cmltKCk7XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICByZXR1cm4gdGhpcy5fc2NvcmU7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGxldCBzY29yZSA9IHRoaXMuZ2V0U2NvcmUodGhpcy5wcm9wcy5wYXNzd29yZCwgdGhpcy5wcm9wcy5pbnB1dHMpO1xuXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiaGVscC1ibG9jayBwYXNzd29yZC1zdHJlbmd0aFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwcm9ncmVzc1wiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT17XCJwcm9ncmVzcy1iYXIgXCIgKyBTVFlMRVNbc2NvcmVdfVxuICAgICAgICAgICAgIHN0eWxlPXt7d2lkdGg6ICgyMCArICgyMCAqIHNjb3JlKSkgKyAnJSd9fVxuICAgICAgICAgICAgIHJvbGU9XCJwcm9ncmVzcy1iYXJcIlxuICAgICAgICAgICAgIGFyaWEtdmFsdWVub3c9e3Njb3JlfVxuICAgICAgICAgICAgIGFyaWEtdmFsdWVtaW49XCIwXCJcbiAgICAgICAgICAgICBhcmlhLXZhbHVlbWF4PVwiNFwiPlxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInNyLW9ubHlcIj5cbiAgICAgICAgICAgIHtMQUJFTFNbc2NvcmVdfVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxwIGNsYXNzTmFtZT1cInRleHQtc21hbGxcIj5cbiAgICAgICAge0xBQkVMU1tzY29yZV19XG4gICAgICA8L3A+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IExvYWRlciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9sb2FkZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWdpc3Rlck1vZGFsIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3JlZ2lzdGVyLmpzJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgY2FwdGNoYSBmcm9tICdtaXNhZ28vc2VydmljZXMvY2FwdGNoYSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1vZGFsIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2RhbCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHp4Y3ZibiBmcm9tICdtaXNhZ28vc2VydmljZXMvenhjdmJuJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuICAgICAgJ2lzTG9hZGVkJzogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBzaG93UmVnaXN0ZXJNb2RhbCA9ICgpID0+IHtcbiAgICBpZiAobWlzYWdvLmdldCgnU0VUVElOR1MnKS5hY2NvdW50X2FjdGl2YXRpb24gPT09ICdjbG9zZWQnKSB7XG4gICAgICBzbmFja2Jhci5pbmZvKGdldHRleHQoXCJOZXcgcmVnaXN0cmF0aW9ucyBhcmUgY3VycmVudGx5IGRpc2FibGVkLlwiKSk7XG4gICAgfSBlbHNlIGlmICh0aGlzLnN0YXRlLmlzTG9hZGVkKSB7XG4gICAgICBtb2RhbC5zaG93KFJlZ2lzdGVyTW9kYWwpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ2lzTG9hZGluZyc6IHRydWVcbiAgICAgIH0pO1xuXG4gICAgICBQcm9taXNlLmFsbChbXG4gICAgICAgIGNhcHRjaGEubG9hZCgpLFxuICAgICAgICB6eGN2Ym4ubG9hZCgpXG4gICAgICBdKS50aGVuKCgpID0+IHtcbiAgICAgICAgaWYgKCF0aGlzLnN0YXRlLmlzTG9hZGVkKSB7XG4gICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG4gICAgICAgICAgICAnaXNMb2FkZWQnOiBmYWxzZVxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG5cbiAgICAgICAgbW9kYWwuc2hvdyhSZWdpc3Rlck1vZGFsKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICAgcmV0dXJuIHRoaXMucHJvcHMuY2xhc3NOYW1lICsgKHRoaXMuc3RhdGUuaXNMb2FkaW5nID8gJyBidG4tbG9hZGluZycgOiAnJyk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBvbkNsaWNrPXt0aGlzLnNob3dSZWdpc3Rlck1vZGFsfVxuICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17J2J0biAnICsgdGhpcy5nZXRDbGFzc05hbWUoKX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRlZH0+XG4gICAgICB7Z2V0dGV4dChcIlJlZ2lzdGVyXCIpfVxuICAgICAge3RoaXMuc3RhdGUuaXNMb2FkaW5nID8gPExvYWRlciAvPiA6IG51bGwgfVxuICAgIDwvYnV0dG9uPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IEZvcm1Hcm91cCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtLWdyb3VwJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgUGFzc3dvcmRTdHJlbmd0aCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9wYXNzd29yZC1zdHJlbmd0aCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IGF1dGggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2F1dGgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBjYXB0Y2hhIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9jYXB0Y2hhJztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcbmltcG9ydCAqIGFzIHZhbGlkYXRvcnMgZnJvbSAnbWlzYWdvL3V0aWxzL3ZhbGlkYXRvcnMnO1xuXG5leHBvcnQgY2xhc3MgUmVnaXN0ZXJGb3JtIGV4dGVuZHMgRm9ybSB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZSxcblxuICAgICAgJ3VzZXJuYW1lJzogJycsXG4gICAgICAnZW1haWwnOiAnJyxcbiAgICAgICdwYXNzd29yZCc6ICcnLFxuICAgICAgJ2NhcHRjaGEnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICd1c2VybmFtZSc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnVzZXJuYW1lQ29udGVudCgpLFxuICAgICAgICAgIHZhbGlkYXRvcnMudXNlcm5hbWVNaW5MZW5ndGgobWlzYWdvLmdldCgnU0VUVElOR1MnKSksXG4gICAgICAgICAgdmFsaWRhdG9ycy51c2VybmFtZU1heExlbmd0aChtaXNhZ28uZ2V0KCdTRVRUSU5HUycpKVxuICAgICAgICBdLFxuICAgICAgICAnZW1haWwnOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy5lbWFpbCgpXG4gICAgICAgIF0sXG4gICAgICAgICdwYXNzd29yZCc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnBhc3N3b3JkTWluTGVuZ3RoKG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykpXG4gICAgICAgIF0sXG4gICAgICAgICdjYXB0Y2hhJzogY2FwdGNoYS52YWxpZGF0b3IoKVxuICAgICAgfSxcblxuICAgICAgJ2Vycm9ycyc6IHt9XG4gICAgfTtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWQoKSkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJGb3JtIGNvbnRhaW5zIGVycm9ycy5cIikpO1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICdlcnJvcnMnOiB0aGlzLnZhbGlkYXRlKClcbiAgICAgIH0pO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdChtaXNhZ28uZ2V0KCdVU0VSU19BUEknKSwge1xuICAgICAgJ3VzZXJuYW1lJzogdGhpcy5zdGF0ZS51c2VybmFtZSxcbiAgICAgICdlbWFpbCc6IHRoaXMuc3RhdGUuZW1haWwsXG4gICAgICAncGFzc3dvcmQnOiB0aGlzLnN0YXRlLnBhc3N3b3JkLFxuICAgICAgJ2NhcHRjaGEnOiB0aGlzLnN0YXRlLmNhcHRjaGFcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3MoYXBpUmVzcG9uc2UpIHtcbiAgICB0aGlzLnByb3BzLmNhbGxiYWNrKGFwaVJlc3BvbnNlKTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnZXJyb3JzJzogT2JqZWN0LmFzc2lnbih7fSwgdGhpcy5zdGF0ZS5lcnJvcnMsIHJlamVjdGlvbilcbiAgICAgIH0pO1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZvcm0gY29udGFpbnMgZXJyb3JzLlwiKSk7XG4gICAgfSBlbHNlIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDMgJiYgcmVqZWN0aW9uLmJhbikge1xuICAgICAgc2hvd0Jhbm5lZFBhZ2UocmVqZWN0aW9uLmJhbik7XG4gICAgICBtb2RhbC5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmFwaUVycm9yKHJlamVjdGlvbik7XG4gICAgfVxuICB9XG5cbiAgZ2V0TGVnYWxGb290Tm90ZSgpIHtcbiAgICBpZiAobWlzYWdvLmdldCgnVEVSTVNfT0ZfU0VSVklDRV9VUkwnKSkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxhIGhyZWY9e21pc2Fnby5nZXQoJ1RFUk1TX09GX1NFUlZJQ0VfVVJMJyl9XG4gICAgICAgICAgICAgICAgdGFyZ2V0PVwiX2JsYW5rXCI+XG4gICAgICAgIHtnZXR0ZXh0KFwiQnkgcmVnaXN0ZXJpbmcgeW91IGFncmVlIHRvIHNpdGUncyB0ZXJtcyBhbmQgY29uZGl0aW9ucy5cIil9XG4gICAgICA8L2E+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1kaWFsb2cgbW9kYWwtcmVnaXN0ZXJcIiByb2xlPVwiZG9jdW1lbnRcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtY29udGVudFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWhlYWRlclwiPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImNsb3NlXCIgZGF0YS1kaXNtaXNzPVwibW9kYWxcIlxuICAgICAgICAgICAgICAgICAgYXJpYS1sYWJlbD17Z2V0dGV4dChcIkNsb3NlXCIpfT5cbiAgICAgICAgICAgIDxzcGFuIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPiZ0aW1lczs8L3NwYW4+XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgPGg0IGNsYXNzTmFtZT1cIm1vZGFsLXRpdGxlXCI+e2dldHRleHQoXCJSZWdpc3RlclwiKX08L2g0PlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fSBjbGFzc05hbWU9XCJmb3JtLWhvcml6b250YWxcIj5cbiAgICAgICAgICA8aW5wdXQgdHlwZT1cInR5cGVcIiBzdHlsZT17e2Rpc3BsYXk6ICdub25lJ319IC8+XG4gICAgICAgICAgPGlucHV0IHR5cGU9XCJwYXNzd29yZFwiIHN0eWxlPXt7ZGlzcGxheTogJ25vbmUnfX0gLz5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHlcIj5cblxuICAgICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIlVzZXJuYW1lXCIpfSBmb3I9XCJpZF91c2VybmFtZVwiXG4gICAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCJcbiAgICAgICAgICAgICAgICAgICAgICAgdmFsaWRhdGlvbj17dGhpcy5zdGF0ZS5lcnJvcnMudXNlcm5hbWV9PlxuICAgICAgICAgICAgICA8aW5wdXQgdHlwZT1cInRleHRcIiBpZD1cImlkX3VzZXJuYW1lXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICAgIGFyaWEtZGVzY3JpYmVkYnk9XCJpZF91c2VybmFtZV9zdGF0dXNcIlxuICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCd1c2VybmFtZScpfVxuICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUudXNlcm5hbWV9IC8+XG4gICAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIkUtbWFpbFwiKX0gZm9yPVwiaWRfZW1haWxcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiXG4gICAgICAgICAgICAgICAgICAgICAgIHZhbGlkYXRpb249e3RoaXMuc3RhdGUuZXJyb3JzLmVtYWlsfT5cbiAgICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgaWQ9XCJpZF9lbWFpbFwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgICBhcmlhLWRlc2NyaWJlZGJ5PVwiaWRfZW1haWxfc3RhdHVzXCJcbiAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnZW1haWwnKX1cbiAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLmVtYWlsfSAvPlxuICAgICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJQYXNzd29yZFwiKX0gZm9yPVwiaWRfcGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiXG4gICAgICAgICAgICAgICAgICAgICAgIHZhbGlkYXRpb249e3RoaXMuc3RhdGUuZXJyb3JzLnBhc3N3b3JkfVxuICAgICAgICAgICAgICAgICAgICAgICBleHRyYT17PFBhc3N3b3JkU3RyZW5ndGggcGFzc3dvcmQ9e3RoaXMuc3RhdGUucGFzc3dvcmR9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnB1dHM9e1tcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zdGF0ZS51c2VybmFtZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zdGF0ZS5lbWFpbFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgXX0gLz59ID5cbiAgICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJwYXNzd29yZFwiIGlkPVwiaWRfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgICAgYXJpYS1kZXNjcmliZWRieT1cImlkX3Bhc3N3b3JkX3N0YXR1c1wiXG4gICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3Bhc3N3b3JkJyl9XG4gICAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5wYXNzd29yZH0gLz5cbiAgICAgICAgICAgIDwvRm9ybUdyb3VwPlxuXG4gICAgICAgICAgICB7Y2FwdGNoYS5jb21wb25lbnQoe1xuICAgICAgICAgICAgICBmb3JtOiB0aGlzLFxuICAgICAgICAgICAgICBsYWJlbENsYXNzOiBcImNvbC1zbS00XCIsXG4gICAgICAgICAgICAgIGNvbnRyb2xDbGFzczogXCJjb2wtc20tOFwiXG4gICAgICAgICAgICB9KX1cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtZm9vdGVyXCI+XG4gICAgICAgICAgICB7dGhpcy5nZXRMZWdhbEZvb3ROb3RlKCl9XG4gICAgICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5XCIgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9PlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIlJlZ2lzdGVyIGFjY291bnRcIil9XG4gICAgICAgICAgICA8L0J1dHRvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9mb3JtPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFJlZ2lzdGVyQ29tcGxldGUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRMZWFkKCkge1xuICAgIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICd1c2VyJykge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCIlKHVzZXJuYW1lKXMsIHlvdXIgYWNjb3VudCBoYXMgYmVlbiBjcmVhdGVkIGJ1dCB5b3UgbmVlZCB0byBhY3RpdmF0ZSBpdCBiZWZvcmUgeW91IHdpbGwgYmUgYWJsZSB0byBzaWduIGluLlwiKTtcbiAgICB9IGVsc2UgaWYgKHRoaXMucHJvcHMuYWN0aXZhdGlvbiA9PT0gJ2FkbWluJykge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCIlKHVzZXJuYW1lKXMsIHlvdXIgYWNjb3VudCBoYXMgYmVlbiBjcmVhdGVkIGJ1dCBib2FyZCBhZG1pbmlzdHJhdG9yIHdpbGwgaGF2ZSB0byBhY3RpdmF0ZSBpdCBiZWZvcmUgeW91IHdpbGwgYmUgYWJsZSB0byBzaWduIGluLlwiKTtcbiAgICB9XG4gIH1cblxuICBnZXRTdWJzY3JpcHQoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuYWN0aXZhdGlvbiA9PT0gJ3VzZXInKSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIldlIGhhdmUgc2VudCBhbiBlLW1haWwgdG8gJShlbWFpbClzIHdpdGggbGluayB0aGF0IHlvdSBoYXZlIHRvIGNsaWNrIHRvIGFjdGl2YXRlIHlvdXIgYWNjb3VudC5cIik7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICdhZG1pbicpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiV2Ugd2lsbCBzZW5kIGFuIGUtbWFpbCB0byAlKGVtYWlsKXMgd2hlbiB0aGlzIHRha2VzIHBsYWNlLlwiKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWRpYWxvZyBtb2RhbC1tZXNzYWdlIG1vZGFsLXJlZ2lzdGVyXCJcbiAgICAgICAgICAgICAgICByb2xlPVwiZG9jdW1lbnRcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtY29udGVudFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWhlYWRlclwiPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImNsb3NlXCIgZGF0YS1kaXNtaXNzPVwibW9kYWxcIlxuICAgICAgICAgICAgICAgICAgYXJpYS1sYWJlbD17Z2V0dGV4dChcIkNsb3NlXCIpfT5cbiAgICAgICAgICAgIDxzcGFuIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPiZ0aW1lczs8L3NwYW4+XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgPGg0IGNsYXNzTmFtZT1cIm1vZGFsLXRpdGxlXCI+e2dldHRleHQoXCJSZWdpc3RyYXRpb24gY29tcGxldGVcIil9PC9oND5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keVwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgIGluZm9fb3V0bGluZVxuICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1ib2R5XCI+XG4gICAgICAgICAgICA8cCBjbGFzc05hbWU9XCJsZWFkXCI+XG4gICAgICAgICAgICAgIHtpbnRlcnBvbGF0ZShcbiAgICAgICAgICAgICAgICB0aGlzLmdldExlYWQoKSxcbiAgICAgICAgICAgICAgICB7J3VzZXJuYW1lJzogdGhpcy5wcm9wcy51c2VybmFtZX0sIHRydWUpfVxuICAgICAgICAgICAgPC9wPlxuICAgICAgICAgICAgPHA+XG4gICAgICAgICAgICAgIHtpbnRlcnBvbGF0ZShcbiAgICAgICAgICAgICAgICB0aGlzLmdldFN1YnNjcmlwdCgpLFxuICAgICAgICAgICAgICAgIHsnZW1haWwnOiB0aGlzLnByb3BzLmVtYWlsfSwgdHJ1ZSl9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnY29tcGxldGUnOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBsZXRlUmVnaXN0cmF0aW9uID0gKGFwaVJlc3BvbnNlKSA9PiB7XG4gICAgaWYgKGFwaVJlc3BvbnNlLmFjdGl2YXRpb24gPT09ICdhY3RpdmUnKSB7XG4gICAgICBtb2RhbC5oaWRlKCk7XG4gICAgICBhdXRoLnNpZ25JbihhcGlSZXNwb25zZSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnY29tcGxldGUnOiBhcGlSZXNwb25zZVxuICAgICAgfSk7XG4gICAgfVxuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgaWYgKHRoaXMuc3RhdGUuY29tcGxldGUpIHtcbiAgICAgIHJldHVybiA8UmVnaXN0ZXJDb21wbGV0ZSBhY3RpdmF0aW9uPXt0aGlzLnN0YXRlLmNvbXBsZXRlLmFjdGl2YXRpb259XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdXNlcm5hbWU9e3RoaXMuc3RhdGUuY29tcGxldGUudXNlcm5hbWV9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZW1haWw9e3RoaXMuc3RhdGUuY29tcGxldGUuZW1haWx9IC8+O1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gPFJlZ2lzdGVyRm9ybSBjYWxsYmFjaz17dGhpcy5jb21wbGV0ZVJlZ2lzdHJhdGlvbn0vPjtcbiAgICB9XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgQnV0dG9uIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2J1dHRvbic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEZvcm0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybSc7XG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJztcbmltcG9ydCAqIGFzIHZhbGlkYXRvcnMgZnJvbSAnbWlzYWdvL3V0aWxzL3ZhbGlkYXRvcnMnO1xuaW1wb3J0IHNob3dCYW5uZWRQYWdlIGZyb20gJ21pc2Fnby91dGlscy9iYW5uZWQtcGFnZSc7XG5cbmV4cG9ydCBjbGFzcyBSZXF1ZXN0TGlua0Zvcm0gZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuXG4gICAgICAnZW1haWwnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICdlbWFpbCc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLmVtYWlsKClcbiAgICAgICAgXVxuICAgICAgfVxuICAgIH07XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBpZiAodGhpcy5pc1ZhbGlkKCkpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRW50ZXIgYSB2YWxpZCBlbWFpbCBhZGRyZXNzLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KG1pc2Fnby5nZXQoJ1NFTkRfQUNUSVZBVElPTl9BUEknKSwge1xuICAgICAgJ2VtYWlsJzogdGhpcy5zdGF0ZS5lbWFpbFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhhcGlSZXNwb25zZSkge1xuICAgIHRoaXMucHJvcHMuY2FsbGJhY2soYXBpUmVzcG9uc2UpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKFsnYWxyZWFkeV9hY3RpdmUnLCAnaW5hY3RpdmVfYWRtaW4nXS5pbmRleE9mKHJlamVjdGlvbi5jb2RlKSA+IC0xKSB7XG4gICAgICBzbmFja2Jhci5pbmZvKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgIH0gZWxzZSBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAzICYmIHJlamVjdGlvbi5iYW4pIHtcbiAgICAgIHNob3dCYW5uZWRQYWdlKHJlamVjdGlvbi5iYW4pO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwid2VsbCB3ZWxsLWZvcm0gd2VsbC1mb3JtLXJlcXVlc3QtYWN0aXZhdGlvbi1saW5rXCI+XG4gICAgICA8Zm9ybSBvblN1Ym1pdD17dGhpcy5oYW5kbGVTdWJtaXR9PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXBcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRyb2wtaW5wdXRcIj5cblxuICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICBwbGFjZWhvbGRlcj17Z2V0dGV4dChcIllvdXIgZS1tYWlsIGFkZHJlc3NcIil9XG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnZW1haWwnKX1cbiAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5lbWFpbH0gLz5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cblxuICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiU2VuZCBsaW5rXCIpfVxuICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgPC9mb3JtPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBMaW5rU2VudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldE1lc3NhZ2UoKSB7XG4gICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCJBY3RpdmF0aW9uIGxpbmsgd2FzIHNlbnQgdG8gJShlbWFpbClzXCIpLCB7XG4gICAgICBlbWFpbDogdGhpcy5wcm9wcy51c2VyLmVtYWlsXG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXF1ZXN0LWFjdGl2YXRpb24tbGluayB3ZWxsLWRvbmVcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZG9uZS1tZXNzYWdlXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgY2hlY2tcbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgIDxwPlxuICAgICAgICAgICAge3RoaXMuZ2V0TWVzc2FnZSgpfVxuICAgICAgICAgIDwvcD5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMucHJvcHMuY2FsbGJhY2t9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiUmVxdWVzdCBhbm90aGVyIGxpbmtcIil9XG4gICAgICAgIDwvYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBjb21wbGV0ZTogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBjb21wbGV0ZSA9IChhcGlSZXNwb25zZSkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgY29tcGxldGU6IGFwaVJlc3BvbnNlXG4gICAgfSk7XG4gIH07XG5cbiAgcmVzZXQgPSAoKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBjb21wbGV0ZTogZmFsc2VcbiAgICB9KTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGlmICh0aGlzLnN0YXRlLmNvbXBsZXRlKSB7XG4gICAgICByZXR1cm4gPExpbmtTZW50IHVzZXI9e3RoaXMuc3RhdGUuY29tcGxldGV9IGNhbGxiYWNrPXt0aGlzLnJlc2V0fSAvPjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIDxSZXF1ZXN0TGlua0Zvcm0gY2FsbGJhY2s9e3RoaXMuY29tcGxldGV9IC8+O1xuICAgIH07XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgKiBhcyB2YWxpZGF0b3JzIGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcbmltcG9ydCBzaG93QmFubmVkUGFnZSBmcm9tICdtaXNhZ28vdXRpbHMvYmFubmVkLXBhZ2UnO1xuXG5leHBvcnQgY2xhc3MgUmVxdWVzdFJlc2V0Rm9ybSBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG5cbiAgICAgICdlbWFpbCc6ICcnLFxuXG4gICAgICAndmFsaWRhdG9ycyc6IHtcbiAgICAgICAgJ2VtYWlsJzogW1xuICAgICAgICAgIHZhbGlkYXRvcnMuZW1haWwoKVxuICAgICAgICBdXG4gICAgICB9XG4gICAgfTtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWQoKSkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJFbnRlciBhIHZhbGlkIGVtYWlsIGFkZHJlc3MuXCIpKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBhamF4LnBvc3QobWlzYWdvLmdldCgnU0VORF9QQVNTV09SRF9SRVNFVF9BUEknKSwge1xuICAgICAgJ2VtYWlsJzogdGhpcy5zdGF0ZS5lbWFpbFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhhcGlSZXNwb25zZSkge1xuICAgIHRoaXMucHJvcHMuY2FsbGJhY2soYXBpUmVzcG9uc2UpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKFsnaW5hY3RpdmVfdXNlcicsICdpbmFjdGl2ZV9hZG1pbiddLmluZGV4T2YocmVqZWN0aW9uLmNvZGUpID4gLTEpIHtcbiAgICAgIHRoaXMucHJvcHMuc2hvd0luYWN0aXZlUGFnZShyZWplY3Rpb24pO1xuICAgIH0gZWxzZSBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAzICYmIHJlamVjdGlvbi5iYW4pIHtcbiAgICAgIHNob3dCYW5uZWRQYWdlKHJlamVjdGlvbi5iYW4pO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwid2VsbCB3ZWxsLWZvcm0gd2VsbC1mb3JtLXJlcXVlc3QtcGFzc3dvcmQtcmVzZXRcIj5cbiAgICAgIDxmb3JtIG9uU3VibWl0PXt0aGlzLmhhbmRsZVN1Ym1pdH0+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZm9ybS1ncm91cFwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udHJvbC1pbnB1dFwiPlxuXG4gICAgICAgICAgICA8aW5wdXQgdHlwZT1cInRleHRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiWW91ciBlLW1haWwgYWRkcmVzc1wiKX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdlbWFpbCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLmVtYWlsfSAvPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuXG4gICAgICAgIDxCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXByaW1hcnkgYnRuLWJsb2NrXCJcbiAgICAgICAgICAgICAgICBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAge2dldHRleHQoXCJTZW5kIGxpbmtcIil9XG4gICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICA8L2Zvcm0+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIExpbmtTZW50IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0TWVzc2FnZSgpIHtcbiAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIlJlc2V0IHBhc3N3b3JkIGxpbmsgd2FzIHNlbnQgdG8gJShlbWFpbClzXCIpLCB7XG4gICAgICBlbWFpbDogdGhpcy5wcm9wcy51c2VyLmVtYWlsXG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXF1ZXN0LXBhc3N3b3JkLXJlc2V0IHdlbGwtZG9uZVwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJkb25lLW1lc3NhZ2VcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWljb25cIj5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICBjaGVja1xuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1ib2R5XCI+XG4gICAgICAgICAgPHA+XG4gICAgICAgICAgICB7dGhpcy5nZXRNZXNzYWdlKCl9XG4gICAgICAgICAgPC9wPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIGJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5wcm9wcy5jYWxsYmFja30+XG4gICAgICAgICAge2dldHRleHQoXCJSZXF1ZXN0IGFub3RoZXIgbGlua1wiKX1cbiAgICAgICAgPC9idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgQWNjb3VudEluYWN0aXZlUGFnZSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldEFjdGl2YXRlQnV0dG9uKCkge1xuICAgIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICdpbmFjdGl2ZV91c2VyJykge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxwPlxuICAgICAgICA8YSBocmVmPXttaXNhZ28uZ2V0KCdSRVFVRVNUX0FDVElWQVRJT05fVVJMJyl9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiQWN0aXZhdGUgeW91ciBhY2NvdW50LlwiKX1cbiAgICAgICAgPC9hPlxuICAgICAgPC9wPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwicGFnZSBwYWdlLW1lc3NhZ2UgcGFnZS1tZXNzYWdlLWluZm8gcGFnZS1mb3Jnb3R0ZW4tcGFzc3dvcmQtaW5hY3RpdmVcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1wYW5lbFwiPlxuXG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWljb25cIj5cbiAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgICAgaW5mb19vdXRsaW5lXG4gICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIllvdXIgYWNjb3VudCBpcyBpbmFjdGl2ZS5cIil9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgICA8cD5cbiAgICAgICAgICAgICAge3RoaXMucHJvcHMubWVzc2FnZX1cbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICAgIHt0aGlzLmdldEFjdGl2YXRlQnV0dG9uKCl9XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgIGNvbXBsZXRlOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBsZXRlID0gKGFwaVJlc3BvbnNlKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBjb21wbGV0ZTogYXBpUmVzcG9uc2VcbiAgICB9KTtcbiAgfTtcblxuICByZXNldCA9ICgpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIGNvbXBsZXRlOiBmYWxzZVxuICAgIH0pO1xuICB9O1xuXG4gIHNob3dJbmFjdGl2ZVBhZ2UoYXBpUmVzcG9uc2UpIHtcbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICA8QWNjb3VudEluYWN0aXZlUGFnZSBhY3RpdmF0aW9uPXthcGlSZXNwb25zZS5jb2RlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZT17YXBpUmVzcG9uc2UuZGV0YWlsfSAvPixcbiAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdwYWdlLW1vdW50JylcbiAgICApO1xuICB9XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBpZiAodGhpcy5zdGF0ZS5jb21wbGV0ZSkge1xuICAgICAgcmV0dXJuIDxMaW5rU2VudCB1c2VyPXt0aGlzLnN0YXRlLmNvbXBsZXRlfSBjYWxsYmFjaz17dGhpcy5yZXNldH0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8UmVxdWVzdFJlc2V0Rm9ybSBjYWxsYmFjaz17dGhpcy5jb21wbGV0ZX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzaG93SW5hY3RpdmVQYWdlPXt0aGlzLnNob3dJbmFjdGl2ZVBhZ2V9IC8+O1xuICAgIH07XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IFNpZ25Jbk1vZGFsIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3NpZ24taW4uanMnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IGF1dGggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2F1dGgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgKiBhcyB2YWxpZGF0b3JzIGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcbmltcG9ydCBzaG93QmFubmVkUGFnZSBmcm9tICdtaXNhZ28vdXRpbHMvYmFubmVkLXBhZ2UnO1xuXG5leHBvcnQgY2xhc3MgUmVzZXRQYXNzd29yZEZvcm0gZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuXG4gICAgICAncGFzc3dvcmQnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICdwYXNzd29yZCc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnBhc3N3b3JkTWluTGVuZ3RoKG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykpXG4gICAgICAgIF1cbiAgICAgIH1cbiAgICB9O1xuICB9XG5cbiAgY2xlYW4oKSB7XG4gICAgaWYgKHRoaXMuaXNWYWxpZCgpKSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgaWYgKHRoaXMuc3RhdGUucGFzc3dvcmQudHJpbSgpLmxlbmd0aCkge1xuICAgICAgICBzbmFja2Jhci5lcnJvcih0aGlzLnN0YXRlLmVycm9ycy5wYXNzd29yZFswXSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRW50ZXIgbmV3IHBhc3N3b3JkLlwiKSk7XG4gICAgICB9XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KG1pc2Fnby5nZXQoJ0NIQU5HRV9QQVNTV09SRF9BUEknKSwge1xuICAgICAgJ3Bhc3N3b3JkJzogdGhpcy5zdGF0ZS5wYXNzd29yZFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhhcGlSZXNwb25zZSkge1xuICAgIHRoaXMucHJvcHMuY2FsbGJhY2soYXBpUmVzcG9uc2UpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMyAmJiByZWplY3Rpb24uYmFuKSB7XG4gICAgICBzaG93QmFubmVkUGFnZShyZWplY3Rpb24uYmFuKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXNldC1wYXNzd29yZFwiPlxuICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fT5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJmb3JtLWdyb3VwXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250cm9sLWlucHV0XCI+XG5cbiAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiRW50ZXIgbmV3IHBhc3N3b3JkXCIpfVxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3Bhc3N3b3JkJyl9XG4gICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUucGFzc3dvcmR9IC8+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICB7Z2V0dGV4dChcIkNoYW5nZSBwYXNzd29yZFwiKX1cbiAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgIDwvZm9ybT5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgUGFzc3dvcmRDaGFuZ2VkUGFnZSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldE1lc3NhZ2UoKSB7XG4gICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCIlKHVzZXJuYW1lKXMsIHlvdXIgcGFzc3dvcmQgaGFzIGJlZW4gY2hhbmdlZCBzdWNjZXNzZnVsbHkuXCIpLCB7XG4gICAgICB1c2VybmFtZTogdGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lXG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxuICBzaG93U2lnbkluKCkge1xuICAgIG1vZGFsLnNob3coU2lnbkluTW9kYWwpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJwYWdlIHBhZ2UtbWVzc2FnZSBwYWdlLW1lc3NhZ2Utc3VjY2VzcyBwYWdlLWZvcmdvdHRlbi1wYXNzd29yZC1jaGFuZ2VkXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtcGFuZWxcIj5cblxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgIGNoZWNrXG4gICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgICAgICB7dGhpcy5nZXRNZXNzYWdlKCl9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgICA8cD5cbiAgICAgICAgICAgICAge2dldHRleHQoXCJZb3Ugd2lsbCBoYXZlIHRvIHNpZ24gaW4gdXNpbmcgbmV3IHBhc3N3b3JkIGJlZm9yZSBjb250aW51aW5nLlwiKX1cbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICAgIDxwPlxuICAgICAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLXByaW1hcnlcIiBvbkNsaWNrPXt0aGlzLnNob3dTaWduSW59PlxuICAgICAgICAgICAgICAgIHtnZXR0ZXh0KFwiU2lnbiBpblwiKX1cbiAgICAgICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgY29tcGxldGUgPSAoYXBpUmVzcG9uc2UpID0+IHtcbiAgICBhdXRoLnNvZnRTaWduT3V0KCk7XG5cbiAgICAvLyBudWtlIFwicmVkaXJlY3RfdG9cIiBmaWVsZCBzbyB3ZSBkb24ndCBlbmRcbiAgICAvLyBjb21pbmcgYmFjayB0byBlcnJvciBwYWdlIGFmdGVyIHNpZ24gaW5cbiAgICAkKCcjaGlkZGVuLWxvZ2luLWZvcm0gaW5wdXRbbmFtZT1cInJlZGlyZWN0X3RvXCJdJykucmVtb3ZlKCk7XG5cbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICA8UGFzc3dvcmRDaGFuZ2VkUGFnZSB1c2VyPXthcGlSZXNwb25zZX0gLz4sXG4gICAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncGFnZS1tb3VudCcpXG4gICAgKTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8UmVzZXRQYXNzd29yZEZvcm0gY2FsbGJhY2s9e3RoaXMuY29tcGxldGV9IC8+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldENob2ljZSgpIHtcbiAgICBsZXQgY2hvaWNlID0gbnVsbDtcbiAgICB0aGlzLnByb3BzLmNob2ljZXMubWFwKChpdGVtKSA9PiB7XG4gICAgICBpZiAoaXRlbS52YWx1ZSA9PT0gdGhpcy5wcm9wcy52YWx1ZSkge1xuICAgICAgICBjaG9pY2UgPSBpdGVtO1xuICAgICAgfVxuICAgIH0pO1xuICAgIHJldHVybiBjaG9pY2U7XG4gIH1cblxuICBnZXRJY29uKCkge1xuICAgIHJldHVybiB0aGlzLmdldENob2ljZSgpLmljb247XG4gIH1cblxuICBnZXRMYWJlbCgpIHtcbiAgICByZXR1cm4gdGhpcy5nZXRDaG9pY2UoKS5sYWJlbDtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgY2hhbmdlID0gKHZhbHVlKSA9PiB7XG4gICAgcmV0dXJuICgpID0+IHtcbiAgICAgIHRoaXMucHJvcHMub25DaGFuZ2Uoe1xuICAgICAgICB0YXJnZXQ6IHtcbiAgICAgICAgICB2YWx1ZTogdmFsdWVcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImJ0bi1ncm91cCBidG4tc2VsZWN0LWdyb3VwXCI+XG4gICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIlxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4gYnRuLXNlbGVjdCBkcm9wZG93bi10b2dnbGVcIlxuICAgICAgICAgICAgICBpZD17dGhpcy5wcm9wcy5pZCB8fCBudWxsfVxuICAgICAgICAgICAgICBkYXRhLXRvZ2dsZT1cImRyb3Bkb3duXCJcbiAgICAgICAgICAgICAgYXJpYS1oYXNwb3B1cD1cInRydWVcIlxuICAgICAgICAgICAgICBhcmlhLWV4cGFuZGVkPVwiZmFsc2VcIlxuICAgICAgICAgICAgICBhcmlhLWRlc2NyaWJlZGJ5PXt0aGlzLnByb3BzWydhcmlhLWRlc2NyaWJlZGJ5J10gfHwgbnVsbH1cbiAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMucHJvcHMuZGlzYWJsZWQgfHwgZmFsc2V9PlxuICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAge3RoaXMuZ2V0SWNvbigpfVxuICAgICAgICA8L3NwYW4+XG4gICAgICAgIHt0aGlzLmdldExhYmVsKCl9XG4gICAgICA8L2J1dHRvbj5cbiAgICAgIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51XCI+XG4gICAgICAgIHt0aGlzLnByb3BzLmNob2ljZXMubWFwKChpdGVtLCBpKSA9PiB7XG4gICAgICAgICAgcmV0dXJuIDxsaSBrZXk9e2l9PlxuICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuLWxpbmtcIlxuICAgICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLmNoYW5nZShpdGVtLnZhbHVlKX0+XG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgICAgICB7aXRlbS5pY29ufVxuICAgICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgICAgIHtpdGVtLmxhYmVsfVxuICAgICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgPC9saT47XG4gICAgICAgIH0pfVxuICAgICAgPC91bD5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IG1vZGFsIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2RhbCc7XG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJztcbmltcG9ydCBzaG93QmFubmVkUGFnZSBmcm9tICdtaXNhZ28vdXRpbHMvYmFubmVkLXBhZ2UnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG4gICAgICAnc2hvd0FjdGl2YXRpb24nOiBmYWxzZSxcblxuICAgICAgJ3VzZXJuYW1lJzogJycsXG4gICAgICAncGFzc3dvcmQnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICd1c2VybmFtZSc6IFtdLFxuICAgICAgICAncGFzc3dvcmQnOiBbXVxuICAgICAgfVxuICAgIH07XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBpZiAoIXRoaXMuaXNWYWxpZCgpKSB7XG4gICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRmlsbCBvdXQgYm90aCBmaWVsZHMuXCIpKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfVxuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KG1pc2Fnby5nZXQoJ0FVVEhfQVBJJyksIHtcbiAgICAgICd1c2VybmFtZSc6IHRoaXMuc3RhdGUudXNlcm5hbWUsXG4gICAgICAncGFzc3dvcmQnOiB0aGlzLnN0YXRlLnBhc3N3b3JkXG4gICAgfSk7XG4gIH1cblxuICBoYW5kbGVTdWNjZXNzKCkge1xuICAgIGxldCBmb3JtID0gJCgnI2hpZGRlbi1sb2dpbi1mb3JtJyk7XG5cbiAgICBmb3JtLmFwcGVuZCgnPGlucHV0IHR5cGU9XCJ0ZXh0XCIgbmFtZT1cInVzZXJuYW1lXCIgLz4nKTtcbiAgICBmb3JtLmFwcGVuZCgnPGlucHV0IHR5cGU9XCJwYXNzd29yZFwiIG5hbWU9XCJwYXNzd29yZFwiIC8+Jyk7XG5cbiAgICAvLyBmaWxsIG91dCBmb3JtIHdpdGggdXNlciBjcmVkZW50aWFscyBhbmQgc3VibWl0IGl0LCB0aGlzIHdpbGwgdGVsbFxuICAgIC8vIE1pc2FnbyB0byByZWRpcmVjdCB1c2VyIGJhY2sgdG8gcmlnaHQgcGFnZSwgYW5kIHdpbGwgdHJpZ2dlciBicm93c2VyJ3NcbiAgICAvLyBrZXkgcmluZyBmZWF0dXJlXG4gICAgZm9ybS5maW5kKCdpbnB1dFt0eXBlPVwiaGlkZGVuXCJdJykudmFsKGFqYXguZ2V0Q3NyZlRva2VuKCkpO1xuICAgIGZvcm0uZmluZCgnaW5wdXRbbmFtZT1cInJlZGlyZWN0X3RvXCJdJykudmFsKHdpbmRvdy5sb2NhdGlvbi5wYXRobmFtZSk7XG4gICAgZm9ybS5maW5kKCdpbnB1dFtuYW1lPVwidXNlcm5hbWVcIl0nKS52YWwodGhpcy5zdGF0ZS51c2VybmFtZSk7XG4gICAgZm9ybS5maW5kKCdpbnB1dFtuYW1lPVwicGFzc3dvcmRcIl0nKS52YWwodGhpcy5zdGF0ZS5wYXNzd29yZCk7XG4gICAgZm9ybS5zdWJtaXQoKTtcblxuICAgIC8vIGtlZXAgZm9ybSBsb2FkaW5nXG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAnaXNMb2FkaW5nJzogdHJ1ZVxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMCkge1xuICAgICAgaWYgKHJlamVjdGlvbi5jb2RlID09PSAnaW5hY3RpdmVfYWRtaW4nKSB7XG4gICAgICAgIHNuYWNrYmFyLmluZm8ocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICB9IGVsc2UgaWYgKHJlamVjdGlvbi5jb2RlID09PSAnaW5hY3RpdmVfdXNlcicpIHtcbiAgICAgICAgc25hY2tiYXIuaW5mbyhyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgJ3Nob3dBY3RpdmF0aW9uJzogdHJ1ZVxuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSBpZiAocmVqZWN0aW9uLmNvZGUgPT09ICdiYW5uZWQnKSB7XG4gICAgICAgIHNob3dCYW5uZWRQYWdlKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgICAgICBtb2RhbC5oaWRlKCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgIH1cbiAgICB9IGVsc2UgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMyAmJiByZWplY3Rpb24uYmFuKSB7XG4gICAgICBzaG93QmFubmVkUGFnZShyZWplY3Rpb24uYmFuKTtcbiAgICAgIG1vZGFsLmhpZGUoKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgICB9XG4gIH1cblxuICBnZXRBY3RpdmF0aW9uQnV0dG9uKCkge1xuICAgIGlmICh0aGlzLnN0YXRlLnNob3dBY3RpdmF0aW9uKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPGEgaHJlZj17bWlzYWdvLmdldCgnUkVRVUVTVF9BQ1RJVkFUSU9OX1VSTCcpfVxuICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0biBidG4tc3VjY2VzcyBidG4tYmxvY2tcIj5cbiAgICAgICAgIHtnZXR0ZXh0KFwiQWN0aXZhdGUgYWNjb3VudFwiKX1cbiAgICAgIDwvYT47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWRpYWxvZyBtb2RhbC1zbSBtb2RhbC1zaWduLWluXCJcbiAgICAgICAgICAgICAgICByb2xlPVwiZG9jdW1lbnRcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtY29udGVudFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWhlYWRlclwiPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImNsb3NlXCIgZGF0YS1kaXNtaXNzPVwibW9kYWxcIlxuICAgICAgICAgICAgICAgICAgYXJpYS1sYWJlbD17Z2V0dGV4dChcIkNsb3NlXCIpfT5cbiAgICAgICAgICAgIDxzcGFuIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPiZ0aW1lczs8L3NwYW4+XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgPGg0IGNsYXNzTmFtZT1cIm1vZGFsLXRpdGxlXCI+e2dldHRleHQoXCJTaWduIGluXCIpfTwvaDQ+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8Zm9ybSBvblN1Ym1pdD17dGhpcy5oYW5kbGVTdWJtaXR9PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keVwiPlxuXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXBcIj5cbiAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250cm9sLWlucHV0XCI+XG4gICAgICAgICAgICAgICAgPGlucHV0IGlkPVwiaWRfdXNlcm5hbWVcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIiB0eXBlPVwidGV4dFwiXG4gICAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9e2dldHRleHQoXCJVc2VybmFtZSBvciBlLW1haWxcIil9XG4gICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgndXNlcm5hbWUnKX1cbiAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUudXNlcm5hbWV9IC8+XG4gICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZm9ybS1ncm91cFwiPlxuICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRyb2wtaW5wdXRcIj5cbiAgICAgICAgICAgICAgICA8aW5wdXQgaWQ9XCJpZF9wYXNzd29yZFwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiIHR5cGU9XCJwYXNzd29yZFwiXG4gICAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9e2dldHRleHQoXCJQYXNzd29yZFwiKX1cbiAgICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdwYXNzd29yZCcpfVxuICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5wYXNzd29yZH0gLz5cbiAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8L2Rpdj5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtZm9vdGVyXCI+XG4gICAgICAgICAgICB7dGhpcy5nZXRBY3RpdmF0aW9uQnV0dG9uKCl9XG4gICAgICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgICAgIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICAgICAge2dldHRleHQoXCJTaWduIGluXCIpfVxuICAgICAgICAgICAgPC9CdXR0b24+XG4gICAgICAgICAgICA8YSBocmVmPXttaXNhZ28uZ2V0KCdGT1JHT1RURU5fUEFTU1dPUkRfVVJMJyl9XG4gICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4gYnRuLWRlZmF1bHQgYnRuLWJsb2NrXCI+XG4gICAgICAgICAgICAgICB7Z2V0dGV4dChcIkZvcmdvdCBwYXNzd29yZD9cIil9XG4gICAgICAgICAgICA8L2E+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZm9ybT5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG4vKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG5jb25zdCBUWVBFU19DTEFTU0VTID0ge1xuICAnaW5mbyc6ICdhbGVydC1pbmZvJyxcbiAgJ3N1Y2Nlc3MnOiAnYWxlcnQtc3VjY2VzcycsXG4gICd3YXJuaW5nJzogJ2FsZXJ0LXdhcm5pbmcnLFxuICAnZXJyb3InOiAnYWxlcnQtZGFuZ2VyJ1xufTtcbi8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbmV4cG9ydCBjbGFzcyBTbmFja2JhciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldFNuYWNrYmFyQ2xhc3MoKSB7XG4gICAgbGV0IHNuYWNrYmFyQ2xhc3MgPSAnYWxlcnRzLXNuYWNrYmFyJztcbiAgICBpZiAodGhpcy5wcm9wcy5pc1Zpc2libGUpIHtcbiAgICAgIHNuYWNrYmFyQ2xhc3MgKz0gJyBpbic7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyQ2xhc3MgKz0gJyBvdXQnO1xuICAgIH1cbiAgICByZXR1cm4gc25hY2tiYXJDbGFzcztcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPXt0aGlzLmdldFNuYWNrYmFyQ2xhc3MoKX0+XG4gICAgICA8cCBjbGFzc05hbWU9eydhbGVydCAnICsgVFlQRVNfQ0xBU1NFU1t0aGlzLnByb3BzLnR5cGVdfT5cbiAgICAgICAge3RoaXMucHJvcHMubWVzc2FnZX1cbiAgICAgIDwvcD5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0KHN0YXRlKSB7XG4gIHJldHVybiBzdGF0ZS5zbmFja2Jhcjtcbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgQXZhdGFyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2F2YXRhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlZ2lzdGVyQnV0dG9uIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3JlZ2lzdGVyLWJ1dHRvbic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFNpZ25Jbk1vZGFsIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3NpZ24taW4uanMnO1xuaW1wb3J0IGRyb3Bkb3duIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2JpbGUtbmF2YmFyLWRyb3Bkb3duJztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuXG5leHBvcnQgY2xhc3MgR3Vlc3RNZW51IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgc2hvd1NpZ25Jbk1vZGFsKCkge1xuICAgIG1vZGFsLnNob3coU2lnbkluTW9kYWwpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPHVsIGNsYXNzTmFtZT1cImRyb3Bkb3duLW1lbnUgdXNlci1kcm9wZG93biBkcm9wZG93bi1tZW51LXJpZ2h0XCJcbiAgICAgICAgICAgICAgIHJvbGU9XCJtZW51XCI+XG4gICAgICA8bGkgY2xhc3NOYW1lPVwiZ3Vlc3QtcHJldmlld1wiPlxuICAgICAgICA8aDQ+e2dldHRleHQoXCJZb3UgYXJlIGJyb3dzaW5nIGFzIGd1ZXN0LlwiKX08L2g0PlxuICAgICAgICA8cD5cbiAgICAgICAgICB7Z2V0dGV4dCgnU2lnbiBpbiBvciByZWdpc3RlciB0byBzdGFydCBhbmQgcGFydGljaXBhdGUgaW4gZGlzY3Vzc2lvbnMuJyl9XG4gICAgICAgIDwvcD5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC14cy02XCI+XG5cbiAgICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBidG4tZGVmYXVsdCBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnNob3dTaWduSW5Nb2RhbH0+XG4gICAgICAgICAgICAgIHtnZXR0ZXh0KFwiU2lnbiBpblwiKX1cbiAgICAgICAgICAgIDwvYnV0dG9uPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wteHMtNlwiPlxuXG4gICAgICAgICAgICA8UmVnaXN0ZXJCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXByaW1hcnkgYnRuLWJsb2NrXCI+XG4gICAgICAgICAgICAgIHtnZXR0ZXh0KFwiUmVnaXN0ZXJcIil9XG4gICAgICAgICAgICA8L1JlZ2lzdGVyQnV0dG9uPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9saT5cbiAgICA8L3VsPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBHdWVzdE5hdiBleHRlbmRzIEd1ZXN0TWVudSB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibmF2IG5hdi1ndWVzdFwiPlxuICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIG5hdmJhci1idG4gYnRuLWRlZmF1bHRcIlxuICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnNob3dTaWduSW5Nb2RhbH0+XG4gICAgICAgIHtnZXR0ZXh0KFwiU2lnbiBpblwiKX1cbiAgICAgIDwvYnV0dG9uPlxuICAgICAgPFJlZ2lzdGVyQnV0dG9uIGNsYXNzTmFtZT1cIm5hdmJhci1idG4gYnRuLXByaW1hcnlcIj5cbiAgICAgICAge2dldHRleHQoXCJSZWdpc3RlclwiKX1cbiAgICAgIDwvUmVnaXN0ZXJCdXR0b24+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIENvbXBhY3RHdWVzdE5hdiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHNob3dHdWVzdE1lbnUoKSB7XG4gICAgZHJvcGRvd24uc2hvdyhHdWVzdE1lbnUpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgb25DbGljaz17dGhpcy5zaG93R3Vlc3RNZW51fT5cbiAgICAgIDxBdmF0YXIgc2l6ZT1cIjY0XCIgLz5cbiAgICA8L2J1dHRvbj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IEd1ZXN0TmF2LCBDb21wYWN0R3Vlc3ROYXYgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2VyLW1lbnUvZ3Vlc3QtbmF2JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgeyBVc2VyTmF2LCBDb21wYWN0VXNlck5hdn0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvdXNlci1tZW51L3VzZXItbmF2JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBjbGFzcyBVc2VyTWVudSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgaWYgKHRoaXMucHJvcHMuaXNBdXRoZW50aWNhdGVkKSB7XG4gICAgICByZXR1cm4gPFVzZXJOYXYgdXNlcj17dGhpcy5wcm9wcy51c2VyfSAvPjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIDxHdWVzdE5hdiAvPjtcbiAgICB9XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgQ29tcGFjdFVzZXJNZW51IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBpZiAodGhpcy5wcm9wcy5pc0F1dGhlbnRpY2F0ZWQpIHtcbiAgICAgIHJldHVybiA8Q29tcGFjdFVzZXJOYXYgdXNlcj17dGhpcy5wcm9wcy51c2VyfSAvPjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIDxDb21wYWN0R3Vlc3ROYXYgLz47XG4gICAgfVxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4gc3RhdGUuYXV0aDtcbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBjb25uZWN0IH0gZnJvbSAncmVhY3QtcmVkdXgnO1xuaW1wb3J0IEF2YXRhciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdmF0YXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBDaGFuZ2VBdmF0YXJNb2RhbCwgeyBzZWxlY3QgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL3Jvb3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgZHJvcGRvd24gZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vYmlsZS1uYXZiYXItZHJvcGRvd24nO1xuaW1wb3J0IG1vZGFsIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2RhbCc7XG5cbmV4cG9ydCBjbGFzcyBVc2VyTWVudSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGxvZ291dCgpIHtcbiAgICBsZXQgZGVjaXNpb24gPSBjb25maXJtKGdldHRleHQoXCJBcmUgeW91IHN1cmUgeW91IHdhbnQgdG8gc2lnbiBvdXQ/XCIpKTtcbiAgICBpZiAoZGVjaXNpb24pIHtcbiAgICAgICQoJyNoaWRkZW4tbG9nb3V0LWZvcm0nKS5zdWJtaXQoKTtcbiAgICB9XG4gIH1cblxuICBjaGFuZ2VBdmF0YXIoKSB7XG4gICAgbW9kYWwuc2hvdyhjb25uZWN0KHNlbGVjdCkoQ2hhbmdlQXZhdGFyTW9kYWwpKTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51IHVzZXItZHJvcGRvd24gZHJvcGRvd24tbWVudS1yaWdodFwiXG4gICAgICAgICAgICAgICByb2xlPVwibWVudVwiPlxuICAgICAgPGxpIGNsYXNzTmFtZT1cImRyb3Bkb3duLWhlYWRlclwiPlxuICAgICAgICA8c3Ryb25nPnt0aGlzLnByb3BzLnVzZXIudXNlcm5hbWV9PC9zdHJvbmc+XG4gICAgICA8L2xpPlxuICAgICAgPGxpIGNsYXNzTmFtZT1cImRpdmlkZXJcIiAvPlxuICAgICAgPGxpPlxuICAgICAgICA8YSBocmVmPXt0aGlzLnByb3BzLnVzZXIuYWJzb2x1dGVfdXJsfT5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+YWNjb3VudF9jaXJjbGU8L3NwYW4+XG4gICAgICAgICAge2dldHRleHQoXCJTZWUgeW91ciBwcm9maWxlXCIpfVxuICAgICAgICA8L2E+XG4gICAgICA8L2xpPlxuICAgICAgPGxpPlxuICAgICAgICA8YSBocmVmPXttaXNhZ28uZ2V0KCdVU0VSQ1BfVVJMJyl9PlxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5kb25lX2FsbDwvc3Bhbj5cbiAgICAgICAgICB7Z2V0dGV4dChcIkNoYW5nZSBvcHRpb25zXCIpfVxuICAgICAgICA8L2E+XG4gICAgICA8L2xpPlxuICAgICAgPGxpPlxuICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4tbGlua1wiIG9uQ2xpY2s9e3RoaXMuY2hhbmdlQXZhdGFyfT5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+cG9ydHJhaXQ8L3NwYW4+XG4gICAgICAgICAge2dldHRleHQoXCJDaGFuZ2UgYXZhdGFyXCIpfVxuICAgICAgICA8L2J1dHRvbj5cbiAgICAgIDwvbGk+XG4gICAgICA8bGkgY2xhc3NOYW1lPVwiZGl2aWRlclwiIC8+XG4gICAgICA8bGkgY2xhc3NOYW1lPVwiZHJvcGRvd24tZm9vdGVyXCI+XG4gICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIGJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLmxvZ291dH0+XG4gICAgICAgICAgICB7Z2V0dGV4dChcIkxvZyBvdXRcIil9XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICA8L2xpPlxuICAgIDwvdWw+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFVzZXJOYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8dWwgY2xhc3NOYW1lPVwidWwgbmF2IG5hdmJhci1uYXYgbmF2LXVzZXJcIj5cbiAgICAgIDxsaSBjbGFzc05hbWU9XCJkcm9wZG93blwiPlxuICAgICAgICA8YSBocmVmPXt0aGlzLnByb3BzLnVzZXIuYWJzb2x1dGVfdXJsfSBjbGFzc05hbWU9XCJkcm9wZG93bi10b2dnbGVcIlxuICAgICAgICAgICBkYXRhLXRvZ2dsZT1cImRyb3Bkb3duXCIgYXJpYS1oYXNwb3B1cD1cInRydWVcIiBhcmlhLWV4cGFuZGVkPVwiZmFsc2VcIlxuICAgICAgICAgICByb2xlPVwiYnV0dG9uXCI+XG4gICAgICAgICAgPEF2YXRhciB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IHNpemU9XCI2NFwiIC8+XG4gICAgICAgIDwvYT5cbiAgICAgICAgPFVzZXJNZW51IHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz5cbiAgICAgIDwvbGk+XG4gICAgPC91bD47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0VXNlck1lbnUoc3RhdGUpIHtcbiAgcmV0dXJuIHt1c2VyOiBzdGF0ZS5hdXRoLnVzZXJ9O1xufVxuXG5leHBvcnQgY2xhc3MgQ29tcGFjdFVzZXJOYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBzaG93VXNlck1lbnUoKSB7XG4gICAgZHJvcGRvd24uc2hvd0Nvbm5lY3RlZCgndXNlci1tZW51JywgY29ubmVjdChzZWxlY3RVc2VyTWVudSkoVXNlck1lbnUpKTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIG9uQ2xpY2s9e3RoaXMuc2hvd1VzZXJNZW51fT5cbiAgICAgIDxBdmF0YXIgdXNlcj17dGhpcy5wcm9wcy51c2VyfSBzaXplPVwiNjRcIiAvPlxuICAgIDwvYnV0dG9uPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldENsYXNzKCkge1xuICAgIGxldCBzdGF0dXMgPSAnJztcbiAgICBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfYmFubmVkKSB7XG4gICAgICBzdGF0dXMgPSAnYmFubmVkJztcbiAgICB9IGVsc2UgaWYgKHRoaXMucHJvcHMuc3RhdHVzLmlzX2hpZGRlbikge1xuICAgICAgc3RhdHVzID0gJ29mZmxpbmUnO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfb25saW5lX2hpZGRlbikge1xuICAgICAgc3RhdHVzID0gJ29ubGluZSc7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19vZmZsaW5lX2hpZGRlbikge1xuICAgICAgc3RhdHVzID0gJ29mZmxpbmUnO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfb25saW5lKSB7XG4gICAgICBzdGF0dXMgPSAnb25saW5lJztcbiAgICB9IGVsc2UgaWYgKHRoaXMucHJvcHMuc3RhdHVzLmlzX29mZmxpbmUpIHtcbiAgICAgIHN0YXR1cyA9ICdvZmZsaW5lJztcbiAgICB9XG5cbiAgICByZXR1cm4gJ3VzZXItc3RhdHVzIHVzZXItJyArIHN0YXR1cztcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxzcGFuIGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzcygpfT5cbiAgICAgIHt0aGlzLnByb3BzLmNoaWxkcmVufVxuICAgIDwvc3Bhbj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgU3RhdHVzSWNvbiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldEljb24oKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuc3RhdHVzLmlzX2Jhbm5lZCkge1xuICAgICAgcmV0dXJuICdyZW1vdmVfY2lyY2xlX291dGxpbmUnO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfaGlkZGVuKSB7XG4gICAgICByZXR1cm4gJ2hlbHBfb3V0bGluZSc7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19vbmxpbmVfaGlkZGVuKSB7XG4gICAgICByZXR1cm4gJ2xhYmVsJztcbiAgICB9IGVsc2UgaWYgKHRoaXMucHJvcHMuc3RhdHVzLmlzX29mZmxpbmVfaGlkZGVuKSB7XG4gICAgICByZXR1cm4gJ2xhYmVsX291dGxpbmUnO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfb25saW5lKSB7XG4gICAgICByZXR1cm4gJ2xlbnMnO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfb2ZmbGluZSkge1xuICAgICAgcmV0dXJuICdwYW5vcmFtYV9maXNoX2V5ZSc7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPHNwYW4gY2xhc3NOYW1lPVwic3RhdHVzLWljb25cIj5cbiAgICAgIHt0aGlzLmdldEljb24oKX1cbiAgICA8L3NwYW4+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cblxufVxuXG5leHBvcnQgY2xhc3MgU3RhdHVzTGFiZWwgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRIZWxwKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19iYW5uZWQpIHtcbiAgICAgIGlmICh0aGlzLnByb3BzLnN0YXR1cy5iYW5uZWRfdW50aWwpIHtcbiAgICAgICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCIlKHVzZXJuYW1lKXMgaXMgaGlkaW5nIGJhbm5lZCB1bnRpbCAlKGJhbl9leHBpcmVzKXNcIiksIHtcbiAgICAgICAgICB1c2VybmFtZTogdGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lLFxuICAgICAgICAgIGJhbl9leHBpcmVzOiB0aGlzLnByb3BzLnN0YXR1cy5iYW5uZWRfdW50aWwuZm9ybWF0KCdMTCwgTFQnKVxuICAgICAgICB9LCB0cnVlKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBpbnRlcnBvbGF0ZShnZXR0ZXh0KFwiJSh1c2VybmFtZSlzIGlzIGhpZGluZyBiYW5uZWRcIiksIHtcbiAgICAgICAgICB1c2VybmFtZTogdGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lXG4gICAgICAgIH0sIHRydWUpO1xuICAgICAgfVxuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfaGlkZGVuKSB7XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIiUodXNlcm5hbWUpcyBpcyBoaWRpbmcgYWN0aXZpdHlcIiksIHtcbiAgICAgICAgdXNlcm5hbWU6IHRoaXMucHJvcHMudXNlci51c2VybmFtZVxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19vbmxpbmVfaGlkZGVuKSB7XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIiUodXNlcm5hbWUpcyBpcyBvbmxpbmUgKGhpZGRlbilcIiksIHtcbiAgICAgICAgdXNlcm5hbWU6IHRoaXMucHJvcHMudXNlci51c2VybmFtZVxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19vZmZsaW5lX2hpZGRlbikge1xuICAgICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCIlKHVzZXJuYW1lKXMgd2FzIGxhc3Qgc2VlbiAlKGxhc3RfY2xpY2spcyAoaGlkZGVuKVwiKSwge1xuICAgICAgICB1c2VybmFtZTogdGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lLFxuICAgICAgICBsYXN0X2NsaWNrOiB0aGlzLnByb3BzLnN0YXRlLmxhc3RDbGljay5mcm9tTm93KClcbiAgICAgIH0sIHRydWUpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfb25saW5lKSB7XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIiUodXNlcm5hbWUpcyBpcyBvbmxpbmVcIiksIHtcbiAgICAgICAgdXNlcm5hbWU6IHRoaXMucHJvcHMudXNlci51c2VybmFtZVxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19vZmZsaW5lKSB7XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIiUodXNlcm5hbWUpcyB3YXMgbGFzdCBzZWVuICUobGFzdF9jbGljaylzXCIpLCB7XG4gICAgICAgIHVzZXJuYW1lOiB0aGlzLnByb3BzLnVzZXIudXNlcm5hbWUsXG4gICAgICAgIGxhc3RfY2xpY2s6IHRoaXMucHJvcHMuc3RhdGUubGFzdENsaWNrLmZyb21Ob3coKVxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfVxuICB9XG5cbiAgZ2V0TGFiZWwoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuc3RhdHVzLmlzX2Jhbm5lZCkge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCJCYW5uZWRcIik7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19oaWRkZW4pIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiSGlkaW5nIGFjdGl2aXR5XCIpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfb25saW5lX2hpZGRlbikge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCJPbmxpbmUgKGhpZGRlbilcIik7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnN0YXR1cy5pc19vZmZsaW5lX2hpZGRlbikge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCJPZmZsaW5lIChoaWRkZW4pXCIpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5zdGF0dXMuaXNfb25saW5lKSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIk9ubGluZVwiKTtcbiAgICB9IGVsc2UgaWYgKHRoaXMucHJvcHMuc3RhdHVzLmlzX29mZmxpbmUpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiT2ZmbGluZVwiKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8c3BhbiBjbGFzc05hbWU9e3RoaXMucHJvcHMuY2xhc3NOYW1lIHx8IFwic3RhdHVzLWxhYmVsXCJ9XG4gICAgICAgICAgICAgICAgIHRpdGxlPXt0aGlzLmdldEhlbHAoKX0+XG4gICAgICB7dGhpcy5nZXRMYWJlbCgpfVxuICAgIDwvc3Bhbj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBMaW5rIH0gZnJvbSAncmVhY3Qtcm91dGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQXZhdGFyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2F2YXRhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFN0YXR1cywgeyBTdGF0dXNJY29uLCBTdGF0dXNMYWJlbCB9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3VzZXItc3RhdHVzJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgeyBkZWh5ZHJhdGUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcnMnO1xuaW1wb3J0IHRpdGxlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9wYWdlLXRpdGxlJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgY2xhc3MgQWN0aXZlUG9zdGVyIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0Q2xhc3NOYW1lKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnJhbmsuY3NzX2NsYXNzKSB7XG4gICAgICByZXR1cm4gXCJsaXN0LWdyb3VwLWl0ZW0gbGlzdC1ncm91cC1yYW5rLVwiICsgdGhpcy5wcm9wcy5yYW5rLmNzc19jbGFzcztcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIFwibGlzdC1ncm91cC1pdGVtXCI7XG4gICAgfVxuICB9XG5cbiAgZ2V0VXNlclN0YXR1cygpIHtcbiAgICBpZiAodGhpcy5wcm9wcy51c2VyLnN0YXR1cykge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxTdGF0dXMgdXNlcj17dGhpcy5wcm9wcy51c2VyfSBzdGF0dXM9e3RoaXMucHJvcHMudXNlci5zdGF0dXN9PlxuICAgICAgICA8U3RhdHVzSWNvbiB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9XG4gICAgICAgICAgICAgICAgICAgIHN0YXR1cz17dGhpcy5wcm9wcy51c2VyLnN0YXR1c30gLz5cbiAgICAgICAgPFN0YXR1c0xhYmVsIHVzZXI9e3RoaXMucHJvcHMudXNlcn1cbiAgICAgICAgICAgICAgICAgICAgIHN0YXR1cz17dGhpcy5wcm9wcy51c2VyLnN0YXR1c31cbiAgICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cInN0YXR1cy1sYWJlbCBoaWRkZW4teHMgaGlkZGVuLXNtXCIgLz5cbiAgICAgIDwvU3RhdHVzPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8c3BhbiBjbGFzc05hbWU9XCJ1c2VyLXN0YXR1c1wiPlxuICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJzdGF0dXMtaWNvbiB1aS1wcmV2aWV3XCI+XG4gICAgICAgICAgJm5ic3A7XG4gICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwic3RhdHVzLWxhYmVsIHVpLXByZXZpZXcgaGlkZGVuLXhzIGhpZGRlbi1zbVwiPlxuICAgICAgICAgICZuYnNwO1xuICAgICAgICA8L3NwYW4+XG4gICAgICA8L3NwYW4+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cblxuICBnZXRSYW5rTmFtZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5yYW5rLmlzX3RhYikge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgbGV0IHJhbmtVcmwgPSBtaXNhZ28uZ2V0KCdVU0VSU19MSVNUX1VSTCcpICsgdGhpcy5wcm9wcy5yYW5rLnNsdWcgKyAnLyc7XG4gICAgICByZXR1cm4gPExpbmsgdG89e3JhbmtVcmx9IGNsYXNzTmFtZT1cInJhbmstbmFtZVwiPlxuICAgICAgICB7dGhpcy5wcm9wcy5yYW5rLm5hbWV9XG4gICAgICA8L0xpbms+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxzcGFuIGNsYXNzTmFtZT1cInJhbmstbmFtZVwiPlxuICAgICAgICB7dGhpcy5wcm9wcy5yYW5rLm5hbWV9XG4gICAgICA8L3NwYW4+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cblxuICBnZXRVc2VyVGl0bGUoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMudXNlci50aXRsZSkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxzcGFuIGNsYXNzTmFtZT1cInVzZXItdGl0bGUgaGlkZGVuLXhzIGhpZGRlbi1zbVwiPlxuICAgICAgICB7dGhpcy5wcm9wcy51c2VyLnRpdGxlfVxuICAgICAgPC9zcGFuPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxsaSBjbGFzc05hbWU9e3RoaXMuZ2V0Q2xhc3NOYW1lKCl9PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyYW5rLXVzZXItYXZhdGFyXCI+XG4gICAgICAgIDxhIGhyZWY9e3RoaXMucHJvcHMudXNlci5hYnNvbHV0ZV91cmx9PlxuICAgICAgICAgIDxBdmF0YXIgdXNlcj17dGhpcy5wcm9wcy51c2VyfSBzaXplPVwiNTBcIiAvPlxuICAgICAgICA8L2E+XG4gICAgICA8L2Rpdj5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyYW5rLXVzZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ1c2VyLW5hbWVcIj5cbiAgICAgICAgICA8YSBocmVmPXt0aGlzLnByb3BzLnVzZXIuYWJzb2x1dGVfdXJsfSBjbGFzc05hbWU9XCJpdGVtLXRpdGxlXCI+XG4gICAgICAgICAgICB7dGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lfVxuICAgICAgICAgIDwvYT5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIHt0aGlzLmdldFVzZXJTdGF0dXMoKX1cbiAgICAgICAge3RoaXMuZ2V0UmFua05hbWUoKX1cbiAgICAgICAge3RoaXMuZ2V0VXNlclRpdGxlKCl9XG4gICAgICA8L2Rpdj5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyYW5rLXBvc2l0aW9uXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwic3RhdC12YWx1ZVwiPiN7dGhpcy5wcm9wcy5jb3VudGVyfTwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInRleHQtbXV0ZWRcIj57Z2V0dGV4dChcIlJhbmtcIil9PC9kaXY+XG4gICAgICA8L2Rpdj5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyYW5rLXBvc3RzLWNvdW50ZWRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJzdGF0LXZhbHVlXCI+e3RoaXMucHJvcHMudXNlci5tZXRhLnNjb3JlfTwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInRleHQtbXV0ZWRcIj57Z2V0dGV4dChcIlJhbmtlZCBwb3N0c1wiKX08L2Rpdj5cbiAgICAgIDwvZGl2PlxuXG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInJhbmstcG9zdHMtdG90YWxcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJzdGF0LXZhbHVlXCI+e3RoaXMucHJvcHMudXNlci5wb3N0c308L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ0ZXh0LW11dGVkXCI+e2dldHRleHQoXCJUb3RhbCBwb3N0c1wiKX08L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvbGk+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIEFjdGl2ZVBvc3RlcnMgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRMZWFkTWVzc2FnZSgpIHtcbiAgICBsZXQgbWVzc2FnZSA9IG5nZXR0ZXh0KFxuICAgICAgICBcIiUocG9zdGVycylzIG1vc3QgYWN0aXZlIHBvc3RlciBmcm9tIGxhc3QgJShkYXlzKXMgZGF5cy5cIixcbiAgICAgICAgXCIlKHBvc3RlcnMpcyBtb3N0IGFjdGl2ZSBwb3N0ZXJzIGZyb20gbGFzdCAlKGRheXMpcyBkYXlzLlwiLFxuICAgICAgICB0aGlzLnByb3BzLmNvdW50KTtcblxuICAgIHJldHVybiBpbnRlcnBvbGF0ZShtZXNzYWdlLCB7XG4gICAgICBwb3N0ZXJzOiB0aGlzLnByb3BzLmNvdW50LFxuICAgICAgZGF5czogdGhpcy5wcm9wcy50cmFja2VkUGVyaW9kXG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImFjdGl2ZS1wb3N0ZXJzLWxpc3RcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICB7dGhpcy5nZXRMZWFkTWVzc2FnZSgpfVxuICAgICAgICA8L3A+XG5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJhY3RpdmUtcG9zdGVycyB1aS1yZWFkeVwiPlxuICAgICAgICAgIDx1bCBjbGFzc05hbWU9XCJsaXN0LWdyb3VwXCI+XG4gICAgICAgICAgICB7dGhpcy5wcm9wcy51c2Vycy5tYXAoKHVzZXIsIGkpID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIDxBY3RpdmVQb3N0ZXIgdXNlcj17dXNlcn1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmFuaz17dXNlci5yYW5rfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb3VudGVyPXtpICsgMX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAga2V5PXt1c2VyLmlkfSAvPjtcbiAgICAgICAgICAgIH0pfVxuICAgICAgICAgIDwvdWw+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIEFjdGl2ZVBvc3RlcnNMb2FkaW5nIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJhY3RpdmUtcG9zdGVycy1saXN0XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgICBUaGlzIGlzIFVJIHByZXZpZXchXG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgTm9BY3RpdmVQb3N0ZXJzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0RW1wdHlNZXNzYWdlKCkge1xuICAgIHJldHVybiBpbnRlcnBvbGF0ZShcbiAgICAgIGdldHRleHQoXCJObyB1c2VycyBoYXZlIHBvc3RlZCBhbnkgbmV3IG1lc3NhZ2VzIGR1cmluZyBsYXN0ICUoZGF5cylzIGRheXMuXCIpLFxuICAgICAgeydkYXlzJzogdGhpcy5wcm9wcy50cmFja2VkUGVyaW9kfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImFjdGl2ZS1wb3N0ZXJzLWxpc3RcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICB7dGhpcy5nZXRFbXB0eU1lc3NhZ2UoKX1cbiAgICAgICAgPC9wPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIGlmIChtaXNhZ28uaGFzKCdVU0VSUycpKSB7XG4gICAgICB0aGlzLmluaXRXaXRoUHJlbG9hZGVkRGF0YShtaXNhZ28ucG9wKCdVU0VSUycpKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5pbml0V2l0aG91dFByZWxvYWRlZERhdGEoKTtcbiAgICB9XG4gIH1cblxuICBpbml0V2l0aFByZWxvYWRlZERhdGEoZGF0YSkge1xuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBpc0xvYWRlZDogdHJ1ZSxcblxuICAgICAgdHJhY2tlZFBlcmlvZDogZGF0YS50cmFja2VkX3BlcmlvZCxcbiAgICAgIGNvdW50OiBkYXRhLmNvdW50XG4gICAgfTtcblxuICAgIHN0b3JlLmRpc3BhdGNoKGRlaHlkcmF0ZShkYXRhLnJlc3VsdHMpKTtcbiAgfVxuXG4gIGluaXRXaXRob3V0UHJlbG9hZGVkRGF0YSgpIHtcbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgaXNMb2FkZWQ6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIHRpdGxlLnNldCh7XG4gICAgICB0aXRsZTogdGhpcy5wcm9wcy5yb3V0ZS5leHRyYS5uYW1lLFxuICAgICAgcGFyZW50OiBnZXR0ZXh0KFwiVXNlcnNcIilcbiAgICB9KTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRlZCkge1xuICAgICAgaWYgKHRoaXMuc3RhdGUuY291bnQgPiAwKSB7XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgICAgcmV0dXJuIDxBY3RpdmVQb3N0ZXJzIHVzZXJzPXt0aGlzLnByb3BzLnVzZXJzfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdHJhY2tlZFBlcmlvZD17dGhpcy5zdGF0ZS50cmFja2VkUGVyaW9kfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY291bnQ9e3RoaXMuc3RhdGUuY291bnR9IC8+O1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgICByZXR1cm4gPE5vQWN0aXZlUG9zdGVycyB0cmFja2VkUGVyaW9kPXt0aGlzLnN0YXRlLnRyYWNrZWRQZXJpb2R9IC8+O1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPEFjdGl2ZVBvc3RlcnNMb2FkaW5nIC8+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgTGluayB9IGZyb20gJ3JlYWN0LXJvdXRlcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IExpIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2xpJzsgLy9qc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JzsgLy9qc2hpbnQgaWdub3JlOmxpbmVcblxuLy8ganNoaW50IGlnbm9yZTpzdGFydFxubGV0IGxpc3RVcmwgPSBmdW5jdGlvbihiYXNlVXJsLCBsaXN0KSB7XG4gIGxldCB1cmwgPSBiYXNlVXJsO1xuICBpZiAobGlzdC5jb21wb25lbnQgPT09ICdyYW5rJykge1xuICAgIHVybCArPSBsaXN0LnNsdWc7XG4gIH0gZWxzZSB7XG4gICAgdXJsICs9IGxpc3QuY29tcG9uZW50O1xuICB9XG4gIHJldHVybiB1cmwgKyAnLyc7XG59O1xuXG5sZXQgbmF2TGlua3MgPSBmdW5jdGlvbihiYXNlVXJsLCBsaXN0cykge1xuICAgIHJldHVybiBsaXN0cy5tYXAoZnVuY3Rpb24obGlzdCkge1xuICAgICAgbGV0IHVybCA9IGxpc3RVcmwoYmFzZVVybCwgbGlzdCk7XG4gICAgICByZXR1cm4gPExpIHBhdGg9e3VybH1cbiAgICAgICAgICAgICAgICAga2V5PXt1cmx9PlxuICAgICAgICA8TGluayB0bz17dXJsfT5cbiAgICAgICAgICB7bGlzdC5uYW1lfVxuICAgICAgICA8L0xpbms+XG4gICAgICA8L0xpPjtcbiAgfSk7XG59O1xuLy8ganNoaW50IGlnbm9yZTplbmRcblxuZXhwb3J0IGNsYXNzIFRhYnNOYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLy8ganNoaW50IGlnbm9yZTpzdGFydFxuICAgIHJldHVybiA8dWwgY2xhc3NOYW1lPVwibmF2IG5hdi1waWxsc1wiPlxuICAgICAge25hdkxpbmtzKHRoaXMucHJvcHMuYmFzZVVybCwgdGhpcy5wcm9wcy5saXN0cyl9XG4gICAgPC91bD47XG4gICAgLy8ganNoaW50IGlnbm9yZTplbmRcbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgQ29tcGFjdE5hdiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvLyBqc2hpbnQgaWdub3JlOnN0YXJ0XG4gICAgcmV0dXJuIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51XCIgcm9sZT1cIm1lbnVcIj5cbiAgICAgIHtuYXZMaW5rcyh0aGlzLnByb3BzLmJhc2VVcmwsIHRoaXMucHJvcHMubGlzdHMpfVxuICAgIDwvdWw+O1xuICAgIC8vIGpzaGludCBpZ25vcmU6ZW5kXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHRpdGxlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9wYWdlLXRpdGxlJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICB0aXRsZS5zZXQoe1xuICAgICAgdGl0bGU6IHRoaXMucHJvcHMucm91dGUucmFuay5uYW1lLFxuICAgICAgcGFyZW50OiBnZXR0ZXh0KFwiVXNlcnNcIilcbiAgICB9KTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgIEhlbGxvLCB0aGlzIGlzIHVzZXJzIHdpdGggcmFuayBsaXN0IVxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCB7IFRhYnNOYXYsIENvbXBhY3ROYXYgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2Vycy9uYXZzJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQWN0aXZlUG9zdGVycyBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2Vycy9hY3RpdmUtcG9zdGVycyc7XG5pbXBvcnQgUmFuayBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2Vycy9yYW5rJztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBkcm9wZG93bjogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICB0b2dnbGVOYXYgPSAoKSA9PiB7XG4gICAgaWYgKHRoaXMuc3RhdGUuZHJvcGRvd24pIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICBkcm9wZG93bjogZmFsc2VcbiAgICAgIH0pO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgZHJvcGRvd246IHRydWVcbiAgICAgIH0pO1xuICAgIH1cbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRUb2dnbGVOYXZDbGFzc05hbWUoKSB7XG4gICAgaWYgKHRoaXMuc3RhdGUuZHJvcGRvd24pIHtcbiAgICAgIHJldHVybiAnYnRuIGJ0bi1kZWZhdWx0IGJ0bi1pY29uIG9wZW4nO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gJ2J0biBidG4tZGVmYXVsdCBidG4taWNvbic7XG4gICAgfVxuICB9XG5cbiAgZ2V0Q29tcGFjdE5hdkNsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5kcm9wZG93bikge1xuICAgICAgcmV0dXJuICdjb21wYWN0LW5hdiBvcGVuJztcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuICdjb21wYWN0LW5hdic7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJwYWdlIHBhZ2UtdXNlcnMtbGlzdHNcIj5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYWdlLWhlYWRlciB0YWJiZWRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cblxuICAgICAgICAgIDxoMT57Z2V0dGV4dChcIlVzZXJzXCIpfTwvaDE+XG5cbiAgICAgICAgICA8YnV0dG9uIGNsYXNzTmFtZT1cImJ0biBidG4tZGVmYXVsdCBidG4taWNvbiBidG4tZHJvcGRvd24tdG9nZ2xlIGhpZGRlbi1tZCBoaWRkZW4tbGdcIlxuICAgICAgICAgICAgICAgICAgdHlwZT1cImJ1dHRvblwiXG4gICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnRvZ2dsZU5hdn1cbiAgICAgICAgICAgICAgICAgIGFyaWEtaGFzcG9wdXA9XCJ0cnVlXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtZXhwYW5kZWQ9e3RoaXMuc3RhdGUuZHJvcGRvd24gPyAndHJ1ZScgOiAnZmFsc2UnfT5cbiAgICAgICAgICAgIDxpIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgICAgbWVudVxuICAgICAgICAgICAgPC9pPlxuICAgICAgICAgIDwvYnV0dG9uPlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UtdGFicyBoaWRkZW4teHMgaGlkZGVuLXNtXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cblxuICAgICAgICAgICAgPFRhYnNOYXYgbGlzdHM9e21pc2Fnby5nZXQoJ1VTRVJTX0xJU1RTJyl9XG4gICAgICAgICAgICAgICAgICAgICBiYXNlVXJsPXttaXNhZ28uZ2V0KCdVU0VSU19MSVNUX1VSTCcpfSAvPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRDb21wYWN0TmF2Q2xhc3NOYW1lKCl9PlxuXG4gICAgICAgIDxDb21wYWN0TmF2IGxpc3RzPXttaXNhZ28uZ2V0KCdVU0VSU19MSVNUUycpfVxuICAgICAgICAgICAgICAgICAgICBiYXNlVXJsPXttaXNhZ28uZ2V0KCdVU0VSU19MSVNUX1VSTCcpfSAvPlxuXG4gICAgICA8L2Rpdj5cblxuICAgICAge3RoaXMucHJvcHMuY2hpbGRyZW59XG5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0KHN0b3JlKSB7XG4gIHJldHVybiB7XG4gICAgJ3RpY2snOiBzdG9yZS50aWNrLnRpY2ssXG4gICAgJ3VzZXInOiBzdG9yZS5hdXRoLnVzZXIsXG4gICAgJ3VzZXJzJzogc3RvcmUudXNlcnNcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHBhdGhzKCkge1xuICBsZXQgcGF0aHMgPSBbXTtcblxuICBtaXNhZ28uZ2V0KCdVU0VSU19MSVNUUycpLmZvckVhY2goZnVuY3Rpb24oaXRlbSkge1xuICAgIGlmIChpdGVtLmNvbXBvbmVudCA9PT0gJ3JhbmsnKSB7XG4gICAgICBwYXRocy5wdXNoKHtcbiAgICAgICAgcGF0aDogbWlzYWdvLmdldCgnVVNFUlNfTElTVF9VUkwnKSArIGl0ZW0uc2x1ZyArICcvJyxcbiAgICAgICAgY29tcG9uZW50OiBjb25uZWN0KHNlbGVjdCkoUmFuayksXG4gICAgICAgIHJhbms6IHtcbiAgICAgICAgICBuYW1lOiBpdGVtLm5hbWUsXG4gICAgICAgICAgc2x1ZzogaXRlbS5zbHVnLFxuICAgICAgICAgIGNzc19jbGFzczogaXRlbS5jc3NfY2xhc3MsXG4gICAgICAgICAgZGVzY3JpcHRpb246IGl0ZW0uZGVzY3JpcHRpb25cbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfSBlbHNlIGlmIChpdGVtLmNvbXBvbmVudCA9PT0gJ2FjdGl2ZS1wb3N0ZXJzJyl7XG4gICAgICBwYXRocy5wdXNoKHtcbiAgICAgICAgcGF0aDogbWlzYWdvLmdldCgnVVNFUlNfTElTVF9VUkwnKSArIGl0ZW0uY29tcG9uZW50ICsgJy8nLFxuICAgICAgICBjb21wb25lbnQ6IGNvbm5lY3Qoc2VsZWN0KShBY3RpdmVQb3N0ZXJzKSxcbiAgICAgICAgZXh0cmE6IHtcbiAgICAgICAgICBuYW1lOiBpdGVtLm5hbWVcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICB9KTtcblxuICByZXR1cm4gcGF0aHM7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldENsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy52YWx1ZSkge1xuICAgICAgcmV0dXJuIFwiYnRuIGJ0bi15ZXMtbm8gYnRuLXllcy1uby1vblwiO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gXCJidG4gYnRuLXllcy1ubyBidG4teWVzLW5vLW9mZlwiO1xuICAgIH1cbiAgfVxuXG4gIGdldEljb24oKSB7XG4gICAgaWYgKHRoaXMucHJvcHMudmFsdWUpIHtcbiAgICAgIHJldHVybiB0aGlzLnByb3BzLmljb25PbiB8fCAnY2hlY2tfYm94JztcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHRoaXMucHJvcHMuaWNvbk9mZiB8fCAnY2hlY2tfYm94X291dGxpbmVfYmxhbmsnO1xuICAgIH1cbiAgfVxuXG4gIGdldExhYmVsKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnZhbHVlKSB7XG4gICAgICByZXR1cm4gdGhpcy5wcm9wcy5sYWJlbE9uIHx8IGdldHRleHQoXCJ5ZXNcIik7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLnByb3BzLmxhYmVsT2ZmIHx8IGdldHRleHQoXCJub1wiKTtcbiAgICB9XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHRvZ2dsZSA9ICgpID0+IHtcbiAgICB0aGlzLnByb3BzLm9uQ2hhbmdlKHtcbiAgICAgIHRhcmdldDoge1xuICAgICAgICB2YWx1ZTogIXRoaXMucHJvcHMudmFsdWVcbiAgICAgIH1cbiAgICB9KTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8YnV0dG9uIHR5cGU9XCJidXR0b25cIlxuICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMudG9nZ2xlfVxuICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzc05hbWUoKX1cbiAgICAgICAgICAgICAgICAgICBpZD17dGhpcy5wcm9wcy5pZCB8fCBudWxsfVxuICAgICAgICAgICAgICAgICAgIGFyaWEtZGVzY3JpYmVkYnk9e3RoaXMucHJvcHNbJ2FyaWEtZGVzY3JpYmVkYnknXSB8fCBudWxsfVxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnByb3BzLmRpc2FibGVkIHx8IGZhbHNlfT5cbiAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAge3RoaXMuZ2V0SWNvbigpfVxuICAgICAgPC9zcGFuPlxuICAgICAge3RoaXMuZ2V0TGFiZWwoKX1cbiAgICA8L2J1dHRvbj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBPcmRlcmVkTGlzdCBmcm9tICdtaXNhZ28vdXRpbHMvb3JkZXJlZC1saXN0JztcblxuZXhwb3J0IGNsYXNzIE1pc2FnbyB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2luaXRpYWxpemVycyA9IFtdO1xuICAgIHRoaXMuX2NvbnRleHQgPSB7fTtcbiAgfVxuXG4gIGFkZEluaXRpYWxpemVyKGluaXRpYWxpemVyKSB7XG4gICAgdGhpcy5faW5pdGlhbGl6ZXJzLnB1c2goe1xuICAgICAga2V5OiBpbml0aWFsaXplci5uYW1lLFxuXG4gICAgICBpdGVtOiBpbml0aWFsaXplci5pbml0aWFsaXplcixcblxuICAgICAgYWZ0ZXI6IGluaXRpYWxpemVyLmFmdGVyLFxuICAgICAgYmVmb3JlOiBpbml0aWFsaXplci5iZWZvcmVcbiAgICB9KTtcbiAgfVxuXG4gIGluaXQoY29udGV4dCkge1xuICAgIHRoaXMuX2NvbnRleHQgPSBjb250ZXh0O1xuXG4gICAgdmFyIGluaXRPcmRlciA9IG5ldyBPcmRlcmVkTGlzdCh0aGlzLl9pbml0aWFsaXplcnMpLm9yZGVyZWRWYWx1ZXMoKTtcbiAgICBpbml0T3JkZXIuZm9yRWFjaChpbml0aWFsaXplciA9PiB7XG4gICAgICBpbml0aWFsaXplcih0aGlzKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8vIGNvbnRleHQgYWNjZXNzb3JzXG4gIGhhcyhrZXkpIHtcbiAgICByZXR1cm4gISF0aGlzLl9jb250ZXh0W2tleV07XG4gIH1cblxuICBnZXQoa2V5LCBmYWxsYmFjaykge1xuICAgIGlmICh0aGlzLmhhcyhrZXkpKSB7XG4gICAgICByZXR1cm4gdGhpcy5fY29udGV4dFtrZXldO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gZmFsbGJhY2sgfHwgdW5kZWZpbmVkO1xuICAgIH1cbiAgfVxuXG4gIHBvcChrZXkpIHtcbiAgICBpZiAodGhpcy5oYXMoa2V5KSkge1xuICAgICAgbGV0IHZhbHVlID0gdGhpcy5fY29udGV4dFtrZXldO1xuICAgICAgdGhpcy5fY29udGV4dFtrZXldID0gbnVsbDtcbiAgICAgIHJldHVybiB2YWx1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG4gIH1cbn1cblxuLy8gY3JlYXRlICBzaW5nbGV0b25cbnZhciBtaXNhZ28gPSBuZXcgTWlzYWdvKCk7XG5cbi8vIGV4cG9zZSBpdCBnbG9iYWxseVxuZ2xvYmFsLm1pc2FnbyA9IG1pc2FnbztcblxuLy8gYW5kIGV4cG9ydCBpdCBmb3IgdGVzdHMgYW5kIHN0dWZmXG5leHBvcnQgZGVmYXVsdCBtaXNhZ287XG4iLCJpbXBvcnQgeyBVUERBVEVfQVZBVEFSLCBVUERBVEVfVVNFUk5BTUUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcnMnO1xuXG5leHBvcnQgdmFyIGluaXRpYWxTdGF0ZSA9IHtcbiAgc2lnbmVkSW46IGZhbHNlLFxuICBzaWduZWRPdXQ6IGZhbHNlXG59O1xuXG5leHBvcnQgY29uc3QgUEFUQ0hfVVNFUiA9ICdQQVRDSF9VU0VSJztcbmV4cG9ydCBjb25zdCBTSUdOX0lOID0gJ1NJR05fSU4nO1xuZXhwb3J0IGNvbnN0IFNJR05fT1VUID0gJ1NJR05fT1VUJztcblxuZXhwb3J0IGZ1bmN0aW9uIHBhdGNoVXNlcihwYXRjaCkge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IFBBVENIX1VTRVIsXG4gICAgcGF0Y2hcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNpZ25Jbih1c2VyKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogU0lHTl9JTixcbiAgICB1c2VyXG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzaWduT3V0KHNvZnQ9ZmFsc2UpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBTSUdOX09VVCxcbiAgICBzb2Z0XG4gIH07XG59XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGF1dGgoc3RhdGU9aW5pdGlhbFN0YXRlLCBhY3Rpb249bnVsbCkge1xuICBzd2l0Y2ggKGFjdGlvbi50eXBlKSB7XG4gICAgY2FzZSBQQVRDSF9VU0VSOlxuICAgICAgICBsZXQgbmV3U3RhdGUgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSk7XG4gICAgICAgIG5ld1N0YXRlLnVzZXIgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZS51c2VyLCBhY3Rpb24ucGF0Y2gpO1xuICAgICAgICByZXR1cm4gbmV3U3RhdGU7XG5cbiAgICBjYXNlIFNJR05fSU46XG4gICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgc2lnbmVkSW46IGFjdGlvbi51c2VyXG4gICAgICB9KTtcblxuICAgIGNhc2UgU0lHTl9PVVQ6XG4gICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgaXNBdXRoZW50aWNhdGVkOiBmYWxzZSxcbiAgICAgICAgaXNBbm9ueW1vdXM6IHRydWUsXG4gICAgICAgIHNpZ25lZE91dDogIWFjdGlvbi5zb2Z0XG4gICAgICB9KTtcblxuICAgIGNhc2UgVVBEQVRFX0FWQVRBUjpcbiAgICAgIGlmIChzdGF0ZS5pc0F1dGhlbnRpY2F0ZWQgJiYgc3RhdGUudXNlci5pZCA9PT0gYWN0aW9uLnVzZXJJZCkge1xuICAgICAgICBsZXQgbmV3U3RhdGUgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSk7XG4gICAgICAgIG5ld1N0YXRlLnVzZXIgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZS51c2VyLCB7XG4gICAgICAgICAgJ2F2YXRhcl9oYXNoJzogYWN0aW9uLmF2YXRhckhhc2hcbiAgICAgICAgfSk7XG4gICAgICAgIHJldHVybiBuZXdTdGF0ZTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBzdGF0ZTtcblxuICAgIGNhc2UgVVBEQVRFX1VTRVJOQU1FOlxuICAgICAgaWYgKHN0YXRlLmlzQXV0aGVudGljYXRlZCAmJiBzdGF0ZS51c2VyLmlkID09PSBhY3Rpb24udXNlcklkKSB7XG4gICAgICAgIGxldCBuZXdTdGF0ZSA9IE9iamVjdC5hc3NpZ24oe30sIHN0YXRlKTtcbiAgICAgICAgbmV3U3RhdGUudXNlciA9IE9iamVjdC5hc3NpZ24oe30sIHN0YXRlLnVzZXIsIHtcbiAgICAgICAgICB1c2VybmFtZTogYWN0aW9uLnVzZXJuYW1lLFxuICAgICAgICAgIHNsdWc6IGFjdGlvbi5zbHVnXG4gICAgICAgIH0pO1xuICAgICAgICByZXR1cm4gbmV3U3RhdGU7XG4gICAgICB9XG4gICAgICByZXR1cm4gc3RhdGU7XG5cbiAgICBkZWZhdWx0OlxuICAgICAgcmV0dXJuIHN0YXRlO1xuICB9XG59XG4iLCJleHBvcnQgdmFyIGluaXRpYWxTdGF0ZSA9IHtcbiAgdHlwZTogJ2luZm8nLFxuICBtZXNzYWdlOiAnJyxcbiAgaXNWaXNpYmxlOiBmYWxzZVxufTtcblxuZXhwb3J0IGNvbnN0IFNIT1dfU05BQ0tCQVIgPSAnU0hPV19TTkFDS0JBUic7XG5leHBvcnQgY29uc3QgSElERV9TTkFDS0JBUiA9ICdISURFX1NOQUNLQkFSJztcblxuZXhwb3J0IGZ1bmN0aW9uIHNob3dTbmFja2JhcihtZXNzYWdlLCB0eXBlKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogU0hPV19TTkFDS0JBUixcbiAgICBtZXNzYWdlLFxuICAgIG1lc3NhZ2VUeXBlOiB0eXBlXG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoaWRlU25hY2tiYXIoKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogSElERV9TTkFDS0JBUlxuICB9O1xufVxuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBzbmFja2JhcihzdGF0ZT1pbml0aWFsU3RhdGUsIGFjdGlvbj1udWxsKSB7XG4gIGlmIChhY3Rpb24udHlwZSA9PT0gU0hPV19TTkFDS0JBUikge1xuICAgIHJldHVybiB7XG4gICAgICB0eXBlOiBhY3Rpb24ubWVzc2FnZVR5cGUsXG4gICAgICBtZXNzYWdlOiBhY3Rpb24ubWVzc2FnZSxcbiAgICAgIGlzVmlzaWJsZTogdHJ1ZVxuICAgIH07XG4gIH0gZWxzZSBpZiAoYWN0aW9uLnR5cGUgPT09IEhJREVfU05BQ0tCQVIpIHtcbiAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgaXNWaXNpYmxlOiBmYWxzZVxuICAgIH0pO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBzdGF0ZTtcbiAgfVxufVxuIiwiZXhwb3J0IHZhciBpbml0aWFsU3RhdGUgPSB7XG4gIHRpY2s6IDBcbn07XG5cbmV4cG9ydCBjb25zdCBUSUNLID0gJ1RJQ0snO1xuXG5leHBvcnQgZnVuY3Rpb24gZG9UaWNrKCkge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IFRJQ0tcbiAgfTtcbn1cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gdGljayhzdGF0ZT1pbml0aWFsU3RhdGUsIGFjdGlvbj1udWxsKSB7XG4gIGlmIChhY3Rpb24udHlwZSA9PT0gVElDSykge1xuICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSwge1xuICAgICAgICB0aWNrOiBzdGF0ZS50aWNrICsgMVxuICAgIH0pO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBzdGF0ZTtcbiAgfVxufVxuIiwiaW1wb3J0IHsgVVBEQVRFX0FWQVRBUiwgVVBEQVRFX1VTRVJOQU1FIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3VzZXJzJztcblxuaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuXG5leHBvcnQgY29uc3QgQUREX05BTUVfQ0hBTkdFID0gJ0FERF9OQU1FX0NIQU5HRSc7XG5leHBvcnQgY29uc3QgREVIWURSQVRFX1JFU1VMVCA9ICdERUhZRFJBVEVfUkVTVUxUJztcblxuZXhwb3J0IGZ1bmN0aW9uIGFkZE5hbWVDaGFuZ2UoY2hhbmdlLCB1c2VyLCBjaGFuZ2VkQnkpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBBRERfTkFNRV9DSEFOR0UsXG4gICAgY2hhbmdlLFxuICAgIHVzZXIsXG4gICAgY2hhbmdlZEJ5XG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBkZWh5ZHJhdGUoaXRlbXMpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBERUhZRFJBVEVfUkVTVUxULFxuICAgIGl0ZW1zOiBpdGVtc1xuICB9O1xufVxuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiB1c2VybmFtZShzdGF0ZT1bXSwgYWN0aW9uPW51bGwpIHtcbiAgc3dpdGNoIChhY3Rpb24udHlwZSkge1xuICAgIGNhc2UgQUREX05BTUVfQ0hBTkdFOlxuICAgICAgbGV0IG5ld1N0YXRlID0gc3RhdGUuc2xpY2UoKTtcbiAgICAgIG5ld1N0YXRlLnVuc2hpZnQoe1xuICAgICAgICBpZDogTWF0aC5mbG9vcihEYXRlLm5vdygpIC8gMTAwMCksIC8vIGp1c3Qgc21hbGwgaGF4IGZvciBnZXR0aW5nIGlkXG4gICAgICAgIGNoYW5nZWRfYnk6IGFjdGlvbi5jaGFuZ2VkQnksXG4gICAgICAgIGNoYW5nZWRfYnlfdXNlcm5hbWU6IGFjdGlvbi5jaGFuZ2VkQnkudXNlcm5hbWUsXG4gICAgICAgIGNoYW5nZWRfb246IG1vbWVudCgpLFxuICAgICAgICBuZXdfdXNlcm5hbWU6IGFjdGlvbi5jaGFuZ2UudXNlcm5hbWUsXG4gICAgICAgIG9sZF91c2VybmFtZTogYWN0aW9uLnVzZXIudXNlcm5hbWVcbiAgICAgIH0pO1xuICAgICAgcmV0dXJuIG5ld1N0YXRlO1xuXG4gICAgY2FzZSBERUhZRFJBVEVfUkVTVUxUOlxuICAgICAgcmV0dXJuIGFjdGlvbi5pdGVtcy5tYXAoZnVuY3Rpb24oaXRlbSkge1xuICAgICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgaXRlbSwge1xuICAgICAgICAgIGNoYW5nZWRfb246IG1vbWVudChpdGVtLmNoYW5nZWRfb24pXG4gICAgICAgIH0pO1xuICAgICAgfSk7XG5cbiAgICBjYXNlIFVQREFURV9BVkFUQVI6XG4gICAgICByZXR1cm4gc3RhdGUubWFwKGZ1bmN0aW9uKGl0ZW0pIHtcbiAgICAgICAgaXRlbSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0pO1xuICAgICAgICBpZiAoaXRlbS5jaGFuZ2VkX2J5ICYmIGl0ZW0uY2hhbmdlZF9ieS5pZCA9PT0gYWN0aW9uLnVzZXJJZCkge1xuICAgICAgICAgIGl0ZW0uY2hhbmdlZF9ieSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0uY2hhbmdlZF9ieSwge1xuICAgICAgICAgICAgJ2F2YXRhcl9oYXNoJzogYWN0aW9uLmF2YXRhckhhc2hcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBpdGVtKTtcbiAgICAgIH0pO1xuXG4gICAgY2FzZSBVUERBVEVfVVNFUk5BTUU6XG4gICAgICByZXR1cm4gc3RhdGUubWFwKGZ1bmN0aW9uKGl0ZW0pIHtcbiAgICAgICAgaXRlbSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0pO1xuICAgICAgICBpZiAoaXRlbS5jaGFuZ2VkX2J5ICYmIGl0ZW0uY2hhbmdlZF9ieS5pZCA9PT0gYWN0aW9uLnVzZXJJZCkge1xuICAgICAgICAgIGl0ZW0uY2hhbmdlZF9ieSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0uY2hhbmdlZF9ieSwge1xuICAgICAgICAgICAgJ3VzZXJuYW1lJzogYWN0aW9uLnVzZXJuYW1lLFxuICAgICAgICAgICAgJ3NsdWcnOiBhY3Rpb24uc2x1Z1xuICAgICAgICAgIH0pO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIE9iamVjdC5hc3NpZ24oe30sIGl0ZW0pO1xuICAgICAgfSk7XG5cbiAgICBkZWZhdWx0OlxuICAgICAgcmV0dXJuIHN0YXRlO1xuICB9XG59IiwiZXhwb3J0IGNvbnN0IERFSFlEUkFURV9SRVNVTFQgPSAnREVIWURSQVRFX1JFU1VMVCc7XG5leHBvcnQgY29uc3QgVVBEQVRFX0FWQVRBUiA9ICdVUERBVEVfQVZBVEFSJztcbmV4cG9ydCBjb25zdCBVUERBVEVfVVNFUk5BTUUgPSAnVVBEQVRFX1VTRVJOQU1FJztcblxuZXhwb3J0IGZ1bmN0aW9uIGRlaHlkcmF0ZShpdGVtcykge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IERFSFlEUkFURV9SRVNVTFQsXG4gICAgaXRlbXM6IGl0ZW1zXG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1cGRhdGVBdmF0YXIodXNlciwgYXZhdGFySGFzaCkge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IFVQREFURV9BVkFUQVIsXG4gICAgdXNlcklkOiB1c2VyLmlkLFxuICAgIGF2YXRhckhhc2hcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVwZGF0ZVVzZXJuYW1lKHVzZXIsIHVzZXJuYW1lLCBzbHVnKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogVVBEQVRFX1VTRVJOQU1FLFxuICAgIHVzZXJJZDogdXNlci5pZCxcbiAgICB1c2VybmFtZSxcbiAgICBzbHVnXG4gIH07XG59XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIHVzZXIoc3RhdGU9W10sIGFjdGlvbj1udWxsKSB7XG4gIHN3aXRjaCAoYWN0aW9uLnR5cGUpIHtcbiAgICBjYXNlIERFSFlEUkFURV9SRVNVTFQ6XG4gICAgICByZXR1cm4gYWN0aW9uLml0ZW1zLm1hcChmdW5jdGlvbihpdGVtKSB7XG4gICAgICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBpdGVtLCB7XG5cbiAgICAgICAgfSk7XG4gICAgICB9KTtcblxuICAgIGRlZmF1bHQ6XG4gICAgICByZXR1cm4gc3RhdGU7XG4gIH1cbn0iLCJleHBvcnQgY2xhc3MgQWpheCB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2Nvb2tpZU5hbWUgPSBudWxsO1xuICAgIHRoaXMuX2NzcmZUb2tlbiA9IG51bGw7XG4gIH1cblxuICBpbml0KGNvb2tpZU5hbWUpIHtcbiAgICB0aGlzLl9jb29raWVOYW1lID0gY29va2llTmFtZTtcbiAgICB0aGlzLl9jc3JmVG9rZW4gPSB0aGlzLmdldENzcmZUb2tlbigpO1xuICB9XG5cbiAgZ2V0Q3NyZlRva2VuKCkge1xuICAgIGlmIChkb2N1bWVudC5jb29raWUuaW5kZXhPZih0aGlzLl9jb29raWVOYW1lKSAhPT0gLTEpIHtcbiAgICAgIGxldCBjb29raWVSZWdleCA9IG5ldyBSZWdFeHAodGhpcy5fY29va2llTmFtZSArICdcXD0oW147XSopJyk7XG4gICAgICBsZXQgY29va2llID0gZG9jdW1lbnQuY29va2llLm1hdGNoKGNvb2tpZVJlZ2V4KVswXTtcbiAgICAgIHJldHVybiBjb29raWUgPyBjb29raWUuc3BsaXQoJz0nKVsxXSA6IG51bGw7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlcXVlc3QobWV0aG9kLCB1cmwsIGRhdGEpIHtcbiAgICBsZXQgc2VsZiA9IHRoaXM7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUsIHJlamVjdCkge1xuICAgICAgbGV0IHhociA9IHtcbiAgICAgICAgdXJsOiB1cmwsXG4gICAgICAgIG1ldGhvZDogbWV0aG9kLFxuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgJ1gtQ1NSRlRva2VuJzogc2VsZi5fY3NyZlRva2VuXG4gICAgICAgIH0sXG5cbiAgICAgICAgZGF0YTogKGRhdGEgPyBKU09OLnN0cmluZ2lmeShkYXRhKSA6IG51bGwpLFxuICAgICAgICBjb250ZW50VHlwZTogXCJhcHBsaWNhdGlvbi9qc29uOyBjaGFyc2V0PXV0Zi04XCIsXG4gICAgICAgIGRhdGFUeXBlOiAnanNvbicsXG5cbiAgICAgICAgc3VjY2VzczogZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICAgIHJlc29sdmUoZGF0YSk7XG4gICAgICAgIH0sXG5cbiAgICAgICAgZXJyb3I6IGZ1bmN0aW9uKGpxWEhSKSB7XG4gICAgICAgICAgbGV0IHJlamVjdGlvbiA9IGpxWEhSLnJlc3BvbnNlSlNPTiB8fCB7fTtcblxuICAgICAgICAgIHJlamVjdGlvbi5zdGF0dXMgPSBqcVhIUi5zdGF0dXM7XG5cbiAgICAgICAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gMCkge1xuICAgICAgICAgICAgcmVqZWN0aW9uLmRldGFpbCA9IGdldHRleHQoXCJMb3N0IGNvbm5lY3Rpb24gd2l0aCBhcHBsaWNhdGlvbi5cIik7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgcmVqZWN0aW9uLnN0YXR1c1RleHQgPSBqcVhIUi5zdGF0dXNUZXh0O1xuXG4gICAgICAgICAgcmVqZWN0KHJlamVjdGlvbik7XG4gICAgICAgIH1cbiAgICAgIH07XG5cbiAgICAgICQuYWpheCh4aHIpO1xuICAgIH0pO1xuICB9XG5cbiAgZ2V0KHVybCwgcGFyYW1zKSB7XG4gICAgaWYgKHBhcmFtcykge1xuICAgICAgdXJsICs9ICc/JyArICQucGFyYW0ocGFyYW1zKTtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnR0VUJywgdXJsKTtcbiAgfVxuXG4gIHBvc3QodXJsLCBkYXRhKSB7XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnUE9TVCcsIHVybCwgZGF0YSk7XG4gIH1cblxuICBwYXRjaCh1cmwsIGRhdGEpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdQQVRDSCcsIHVybCwgZGF0YSk7XG4gIH1cblxuICBwdXQodXJsLCBkYXRhKSB7XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnUFVUJywgdXJsLCBkYXRhKTtcbiAgfVxuXG4gIGRlbGV0ZSh1cmwpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdERUxFVEUnLCB1cmwpO1xuICB9XG5cbiAgdXBsb2FkKHVybCwgZGF0YSwgcHJvZ3Jlc3MpIHtcbiAgICBsZXQgc2VsZiA9IHRoaXM7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUsIHJlamVjdCkge1xuICAgICAgbGV0IHhociA9IHtcbiAgICAgICAgdXJsOiB1cmwsXG4gICAgICAgIG1ldGhvZDogJ1BPU1QnLFxuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgJ1gtQ1NSRlRva2VuJzogc2VsZi5fY3NyZlRva2VuXG4gICAgICAgIH0sXG5cbiAgICAgICAgZGF0YTogZGF0YSxcbiAgICAgICAgY29udGVudFR5cGU6IGZhbHNlLFxuICAgICAgICBwcm9jZXNzRGF0YTogZmFsc2UsXG5cbiAgICAgICAgeGhyOiBmdW5jdGlvbigpIHtcbiAgICAgICAgICBsZXQgeGhyID0gbmV3IHdpbmRvdy5YTUxIdHRwUmVxdWVzdCgpO1xuICAgICAgICAgIHhoci51cGxvYWQuYWRkRXZlbnRMaXN0ZW5lcihcInByb2dyZXNzXCIsIGZ1bmN0aW9uKGV2dCkge1xuICAgICAgICAgICAgaWYgKGV2dC5sZW5ndGhDb21wdXRhYmxlKSB7XG4gICAgICAgICAgICAgIHByb2dyZXNzKE1hdGgucm91bmQoZXZ0LmxvYWRlZCAvIGV2dC50b3RhbCAqIDEwMCkpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0sIGZhbHNlKTtcbiAgICAgICAgICByZXR1cm4geGhyO1xuICAgICAgICB9LFxuXG4gICAgICAgIHN1Y2Nlc3M6IGZ1bmN0aW9uKHJlc3BvbnNlKSB7XG4gICAgICAgICAgcmVzb2x2ZShyZXNwb25zZSk7XG4gICAgICAgIH0sXG5cbiAgICAgICAgZXJyb3I6IGZ1bmN0aW9uKGpxWEhSKSB7XG4gICAgICAgICAgbGV0IHJlamVjdGlvbiA9IGpxWEhSLnJlc3BvbnNlSlNPTiB8fCB7fTtcblxuICAgICAgICAgIHJlamVjdGlvbi5zdGF0dXMgPSBqcVhIUi5zdGF0dXM7XG5cbiAgICAgICAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gMCkge1xuICAgICAgICAgICAgcmVqZWN0aW9uLmRldGFpbCA9IGdldHRleHQoXCJMb3N0IGNvbm5lY3Rpb24gd2l0aCBhcHBsaWNhdGlvbi5cIik7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgcmVqZWN0aW9uLnN0YXR1c1RleHQgPSBqcVhIUi5zdGF0dXNUZXh0O1xuXG4gICAgICAgICAgcmVqZWN0KHJlamVjdGlvbik7XG4gICAgICAgIH1cbiAgICAgIH07XG5cbiAgICAgICQuYWpheCh4aHIpO1xuICAgIH0pO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBBamF4KCk7XG4iLCJpbXBvcnQgeyBzaWduSW4sIHNpZ25PdXQgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvYXV0aCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgQXV0aCB7XG4gIGluaXQoc3RvcmUsIGxvY2FsLCBtb2RhbCkge1xuICAgIHRoaXMuX3N0b3JlID0gc3RvcmU7XG4gICAgdGhpcy5fbG9jYWwgPSBsb2NhbDtcbiAgICB0aGlzLl9tb2RhbCA9IG1vZGFsO1xuXG4gICAgLy8gdGVsbCBvdGhlciB0YWJzIHdoYXQgYXV0aCBzdGF0ZSBpcyBiZWNhdXNlIHdlIGFyZSBtb3N0IGN1cnJlbnQgd2l0aCBpdFxuICAgIHRoaXMuc3luY1Nlc3Npb24oKTtcblxuICAgIC8vIGxpc3RlbiBmb3Igb3RoZXIgdGFicyB0byB0ZWxsIHVzIHRoYXQgc3RhdGUgY2hhbmdlZFxuICAgIHRoaXMud2F0Y2hTdGF0ZSgpO1xuICB9XG5cbiAgc3luY1Nlc3Npb24oKSB7XG4gICAgbGV0IHN0YXRlID0gdGhpcy5fc3RvcmUuZ2V0U3RhdGUoKS5hdXRoO1xuICAgIGlmIChzdGF0ZS5pc0F1dGhlbnRpY2F0ZWQpIHtcbiAgICAgIHRoaXMuX2xvY2FsLnNldCgnYXV0aCcsIHtcbiAgICAgICAgaXNBdXRoZW50aWNhdGVkOiB0cnVlLFxuICAgICAgICB1c2VybmFtZTogc3RhdGUudXNlci51c2VybmFtZVxuICAgICAgfSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2xvY2FsLnNldCgnYXV0aCcsIHtcbiAgICAgICAgaXNBdXRoZW50aWNhdGVkOiBmYWxzZVxuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgd2F0Y2hTdGF0ZSgpIHtcbiAgICB0aGlzLl9sb2NhbC53YXRjaCgnYXV0aCcsIChuZXdTdGF0ZSkgPT4ge1xuICAgICAgaWYgKG5ld1N0YXRlLmlzQXV0aGVudGljYXRlZCkge1xuICAgICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaWduSW4oe1xuICAgICAgICAgIHVzZXJuYW1lOiBuZXdTdGF0ZS51c2VybmFtZVxuICAgICAgICB9KSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaWduT3V0KCkpO1xuICAgICAgfVxuICAgIH0pO1xuICAgIHRoaXMuX21vZGFsLmhpZGUoKTtcbiAgfVxuXG4gIHNpZ25Jbih1c2VyKSB7XG4gICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goc2lnbkluKHVzZXIpKTtcbiAgICB0aGlzLl9sb2NhbC5zZXQoJ2F1dGgnLCB7XG4gICAgICBpc0F1dGhlbnRpY2F0ZWQ6IHRydWUsXG4gICAgICB1c2VybmFtZTogdXNlci51c2VybmFtZVxuICAgIH0pO1xuICAgIHRoaXMuX21vZGFsLmhpZGUoKTtcbiAgfVxuXG4gIHNpZ25PdXQoKSB7XG4gICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goc2lnbk91dCgpKTtcbiAgICB0aGlzLl9sb2NhbC5zZXQoJ2F1dGgnLCB7XG4gICAgICBpc0F1dGhlbnRpY2F0ZWQ6IGZhbHNlXG4gICAgfSk7XG4gICAgdGhpcy5fbW9kYWwuaGlkZSgpO1xuICB9XG5cbiAgc29mdFNpZ25PdXQoKSB7XG4gICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goc2lnbk91dCh0cnVlKSk7XG4gICAgdGhpcy5fbG9jYWwuc2V0KCdhdXRoJywge1xuICAgICAgaXNBdXRoZW50aWNhdGVkOiBmYWxzZVxuICAgIH0pO1xuICAgIHRoaXMuX21vZGFsLmhpZGUoKTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgQXV0aCgpOyIsIi8qIGdsb2JhbCBncmVjYXB0Y2hhICovXG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtR3JvdXAgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybS1ncm91cCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgQmFzZUNhcHRjaGEge1xuICBpbml0KGNvbnRleHQsIGFqYXgsIGluY2x1ZGUsIHNuYWNrYmFyKSB7XG4gICAgdGhpcy5fY29udGV4dCA9IGNvbnRleHQ7XG4gICAgdGhpcy5fYWpheCA9IGFqYXg7XG4gICAgdGhpcy5faW5jbHVkZSA9IGluY2x1ZGU7XG4gICAgdGhpcy5fc25hY2tiYXIgPSBzbmFja2JhcjtcbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgTm9DYXB0Y2hhIGV4dGVuZHMgQmFzZUNhcHRjaGEge1xuICBsb2FkKCkge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZShmdW5jdGlvbihyZXNvbHZlKSB7XG4gICAgICAvLyBpbW1lZGlhdGVseSByZXNvbHZlIGFzIHdlIGRvbid0IGhhdmUgYW55dGhpbmcgdG8gdmFsaWRhdGVcbiAgICAgIHJlc29sdmUoKTtcbiAgICB9KTtcbiAgfVxuXG4gIHZhbGlkYXRvcigpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIGNvbXBvbmVudCgpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgUUFDYXB0Y2hhIGV4dGVuZHMgQmFzZUNhcHRjaGEge1xuICBsb2FkKCkge1xuICAgIHZhciBzZWxmID0gdGhpcztcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgc2VsZi5fYWpheC5nZXQoc2VsZi5fY29udGV4dC5nZXQoJ0NBUFRDSEFfQVBJX1VSTCcpKS50aGVuKFxuICAgICAgZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICBzZWxmLnF1ZXN0aW9uID0gZGF0YS5xdWVzdGlvbjtcbiAgICAgICAgc2VsZi5oZWxwVGV4dCA9IGRhdGEuaGVscF90ZXh0O1xuICAgICAgICByZXNvbHZlKCk7XG4gICAgICB9LCBmdW5jdGlvbigpIHtcbiAgICAgICAgc2VsZi5fc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZhaWxlZCB0byBsb2FkIENBUFRDSEEuXCIpKTtcbiAgICAgICAgcmVqZWN0KCk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfVxuXG4gIHZhbGlkYXRvcigpIHtcbiAgICByZXR1cm4gW107XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBvbmVudChrd2FyZ3MpIHtcbiAgICByZXR1cm4gPEZvcm1Hcm91cCBsYWJlbD17dGhpcy5xdWVzdGlvbn0gZm9yPVwiaWRfY2FwdGNoYVwiXG4gICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz17a3dhcmdzLmxhYmVsQ2xhc3MgfHwgXCJjb2wtc20tNFwifVxuICAgICAgICAgICAgICAgICAgICAgIGNvbnRyb2xDbGFzcz17a3dhcmdzLmNvbnRyb2xDbGFzcyB8fCBcImNvbC1zbS04XCJ9XG4gICAgICAgICAgICAgICAgICAgICAgdmFsaWRhdGlvbj17a3dhcmdzLmZvcm0uc3RhdGUuZXJyb3JzLmNhcHRjaGF9XG4gICAgICAgICAgICAgICAgICAgICAgaGVscFRleHQ9e3RoaXMuaGVscFRleHQgfHwgbnVsbH0+XG4gICAgICA8aW5wdXQgdHlwZT1cInRleHRcIiBpZD1cImlkX2NhcHRjaGFcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgIGFyaWEtZGVzY3JpYmVkYnk9XCJpZF9jYXB0Y2hhX3N0YXR1c1wiXG4gICAgICAgICAgICAgZGlzYWJsZWQ9e2t3YXJncy5mb3JtLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICBvbkNoYW5nZT17a3dhcmdzLmZvcm0uYmluZElucHV0KCdjYXB0Y2hhJyl9XG4gICAgICAgICAgICAgdmFsdWU9e2t3YXJncy5mb3JtLnN0YXRlLmNhcHRjaGF9IC8+XG4gICAgPC9Gb3JtR3JvdXA+O1xuICB9XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG59XG5cblxuZXhwb3J0IGNsYXNzIFJlQ2FwdGNoYUNvbXBvbmVudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIGdyZWNhcHRjaGEucmVuZGVyKCdyZWNhcHRjaGEnLCB7XG4gICAgICAnc2l0ZWtleSc6IHRoaXMucHJvcHMuc2l0ZUtleSxcbiAgICAgICdjYWxsYmFjayc6IChyZXNwb25zZSkgPT4ge1xuICAgICAgICAvLyBmaXJlIGZha2V5IGV2ZW50IHRvIGJpbmRpbmdcbiAgICAgICAgdGhpcy5wcm9wcy5iaW5kaW5nKHtcbiAgICAgICAgICB0YXJnZXQ6IHtcbiAgICAgICAgICAgIHZhbHVlOiByZXNwb25zZVxuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGlkPVwicmVjYXB0Y2hhXCIgLz47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgUmVDYXB0Y2hhIGV4dGVuZHMgQmFzZUNhcHRjaGEge1xuICBsb2FkKCkge1xuICAgIHRoaXMuX2luY2x1ZGUuaW5jbHVkZSgnaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9yZWNhcHRjaGEvYXBpLmpzJywgdHJ1ZSk7XG5cbiAgICByZXR1cm4gbmV3IFByb21pc2UoZnVuY3Rpb24ocmVzb2x2ZSkge1xuICAgICAgdmFyIHdhaXQgPSBmdW5jdGlvbigpIHtcbiAgICAgICAgaWYgKHR5cGVvZiBncmVjYXB0Y2hhID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgICAgICAgd2luZG93LnNldFRpbWVvdXQoZnVuY3Rpb24oKSB7XG4gICAgICAgICAgICB3YWl0KCk7XG4gICAgICAgICAgfSwgMjAwKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgIH1cbiAgICAgIH07XG4gICAgICB3YWl0KCk7XG4gICAgfSk7XG4gIH1cblxuICB2YWxpZGF0b3IoKSB7XG4gICAgcmV0dXJuIFtdO1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBjb21wb25lbnQoa3dhcmdzKSB7XG4gICAgcmV0dXJuIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJDYXB0Y2hhXCIpfSBmb3I9XCJpZF9jYXB0Y2hhXCJcbiAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPXtrd2FyZ3MubGFiZWxDbGFzcyB8fCBcImNvbC1zbS00XCJ9XG4gICAgICAgICAgICAgICAgICAgICAgY29udHJvbENsYXNzPXtrd2FyZ3MuY29udHJvbENsYXNzIHx8IFwiY29sLXNtLThcIn1cbiAgICAgICAgICAgICAgICAgICAgICB2YWxpZGF0aW9uPXtrd2FyZ3MuZm9ybS5zdGF0ZS5lcnJvcnMuY2FwdGNoYX1cbiAgICAgICAgICAgICAgICAgICAgICBoZWxwVGV4dD17Z2V0dGV4dChcIlBsZWFzZSBzb2x2ZSB0aGUgcXVpY2sgdGVzdC5cIil9PlxuICAgICAgPFJlQ2FwdGNoYUNvbXBvbmVudCBzaXRlS2V5PXt0aGlzLl9jb250ZXh0LmdldCgnU0VUVElOR1MnKS5yZWNhcHRjaGFfc2l0ZV9rZXl9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIGJpbmRpbmc9e2t3YXJncy5mb3JtLmJpbmRJbnB1dCgnY2FwdGNoYScpfSAvPlxuICAgIDwvRm9ybUdyb3VwPjtcbiAgfVxuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xufVxuXG5leHBvcnQgY2xhc3MgQ2FwdGNoYSB7XG4gIGluaXQoY29udGV4dCwgYWpheCwgaW5jbHVkZSwgc25hY2tiYXIpIHtcbiAgICBzd2l0Y2goY29udGV4dC5nZXQoJ1NFVFRJTkdTJykuY2FwdGNoYV90eXBlKSB7XG4gICAgICBjYXNlICdubyc6XG4gICAgICAgIHRoaXMuX2NhcHRjaGEgPSBuZXcgTm9DYXB0Y2hhKCk7XG4gICAgICAgIGJyZWFrO1xuXG4gICAgICBjYXNlICdxYSc6XG4gICAgICAgIHRoaXMuX2NhcHRjaGEgPSBuZXcgUUFDYXB0Y2hhKCk7XG4gICAgICAgIGJyZWFrO1xuXG4gICAgICBjYXNlICdyZSc6XG4gICAgICAgIHRoaXMuX2NhcHRjaGEgPSBuZXcgUmVDYXB0Y2hhKCk7XG4gICAgICAgIGJyZWFrO1xuICAgIH1cblxuICAgIHRoaXMuX2NhcHRjaGEuaW5pdChjb250ZXh0LCBhamF4LCBpbmNsdWRlLCBzbmFja2Jhcik7XG4gIH1cblxuICAvLyBhY2Nlc3NvcnMgZm9yIHVuZGVybHlpbmcgc3RyYXRlZ3lcblxuICBsb2FkKCkge1xuICAgIHJldHVybiB0aGlzLl9jYXB0Y2hhLmxvYWQoKTtcbiAgfVxuXG4gIHZhbGlkYXRvcigpIHtcbiAgICByZXR1cm4gdGhpcy5fY2FwdGNoYS52YWxpZGF0b3IoKTtcbiAgfVxuXG4gIGNvbXBvbmVudChrd2FyZ3MpIHtcbiAgICByZXR1cm4gdGhpcy5fY2FwdGNoYS5jb21wb25lbnQoa3dhcmdzKTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgQ2FwdGNoYSgpOyIsImV4cG9ydCBjbGFzcyBJbmNsdWRlIHtcbiAgaW5pdChzdGF0aWNVcmwpIHtcbiAgICB0aGlzLl9zdGF0aWNVcmwgPSBzdGF0aWNVcmw7XG4gICAgdGhpcy5faW5jbHVkZWQgPSBbXTtcbiAgfVxuXG4gIGluY2x1ZGUoc2NyaXB0LCByZW1vdGU9ZmFsc2UpIHtcbiAgICBpZiAodGhpcy5faW5jbHVkZWQuaW5kZXhPZihzY3JpcHQpID09PSAtMSkge1xuICAgICAgdGhpcy5faW5jbHVkZWQucHVzaChzY3JpcHQpO1xuICAgICAgdGhpcy5faW5jbHVkZShzY3JpcHQsIHJlbW90ZSk7XG4gICAgfVxuICB9XG5cbiAgX2luY2x1ZGUoc2NyaXB0LCByZW1vdGUpIHtcbiAgICAkLmFqYXgoe1xuICAgICAgdXJsOiAoIXJlbW90ZSA/IHRoaXMuX3N0YXRpY1VybCA6ICcnKSArIHNjcmlwdCxcbiAgICAgIGNhY2hlOiB0cnVlLFxuICAgICAgZGF0YVR5cGU6ICdzY3JpcHQnXG4gICAgfSk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IEluY2x1ZGUoKTsiLCJsZXQgc3RvcmFnZSA9IHdpbmRvdy5sb2NhbFN0b3JhZ2U7XG5cbmV4cG9ydCBjbGFzcyBMb2NhbFN0b3JhZ2Uge1xuICBpbml0KHByZWZpeCkge1xuICAgIHRoaXMuX3ByZWZpeCA9IHByZWZpeDtcbiAgICB0aGlzLl93YXRjaGVycyA9IFtdO1xuXG4gICAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ3N0b3JhZ2UnLCAoZSkgPT4ge1xuICAgICAgbGV0IG5ld1ZhbHVlSnNvbiA9IEpTT04ucGFyc2UoZS5uZXdWYWx1ZSk7XG4gICAgICB0aGlzLl93YXRjaGVycy5mb3JFYWNoKGZ1bmN0aW9uKHdhdGNoZXIpIHtcbiAgICAgICAgaWYgKHdhdGNoZXIua2V5ID09PSBlLmtleSAmJiBlLm9sZFZhbHVlICE9PSBlLm5ld1ZhbHVlKSB7XG4gICAgICAgICAgd2F0Y2hlci5jYWxsYmFjayhuZXdWYWx1ZUpzb24pO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfVxuXG4gIHNldChrZXksIHZhbHVlKSB7XG4gICAgc3RvcmFnZS5zZXRJdGVtKHRoaXMuX3ByZWZpeCArIGtleSwgSlNPTi5zdHJpbmdpZnkodmFsdWUpKTtcbiAgfVxuXG4gIGdldChrZXkpIHtcbiAgICBsZXQgaXRlbVN0cmluZyA9IHN0b3JhZ2UuZ2V0SXRlbSh0aGlzLl9wcmVmaXggKyBrZXkpO1xuICAgIGlmIChpdGVtU3RyaW5nKSB7XG4gICAgICByZXR1cm4gSlNPTi5wYXJzZShpdGVtU3RyaW5nKTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgd2F0Y2goa2V5LCBjYWxsYmFjaykge1xuICAgIHRoaXMuX3dhdGNoZXJzLnB1c2goe1xuICAgICAga2V5OiB0aGlzLl9wcmVmaXggKyBrZXksXG4gICAgICBjYWxsYmFjazogY2FsbGJhY2tcbiAgICB9KTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgTG9jYWxTdG9yYWdlKCk7IiwiaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgY2xhc3MgTW9iaWxlTmF2YmFyRHJvcGRvd24ge1xuICBpbml0KGVsZW1lbnQpIHtcbiAgICB0aGlzLl9lbGVtZW50ID0gZWxlbWVudDtcbiAgICB0aGlzLl9jb21wb25lbnQgPSBudWxsO1xuICB9XG5cbiAgc2hvdyhjb21wb25lbnQpIHtcbiAgICBpZiAodGhpcy5fY29tcG9uZW50ID09PSBjb21wb25lbnQpIHtcbiAgICAgIHRoaXMuaGlkZSgpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9jb21wb25lbnQgPSBjb21wb25lbnQ7XG4gICAgICBtb3VudChjb21wb25lbnQsIHRoaXMuX2VsZW1lbnQuaWQpO1xuICAgICAgJCh0aGlzLl9lbGVtZW50KS5hZGRDbGFzcygnb3BlbicpO1xuICAgIH1cbiAgfVxuXG4gIHNob3dDb25uZWN0ZWQobmFtZSwgY29tcG9uZW50KSB7XG4gICAgaWYgKHRoaXMuX2NvbXBvbmVudCA9PT0gbmFtZSkge1xuICAgICAgdGhpcy5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2NvbXBvbmVudCA9IG5hbWU7XG4gICAgICBtb3VudChjb21wb25lbnQsIHRoaXMuX2VsZW1lbnQuaWQsIHRydWUpO1xuICAgICAgJCh0aGlzLl9lbGVtZW50KS5hZGRDbGFzcygnb3BlbicpO1xuICAgIH1cbiAgfVxuXG4gIGhpZGUoKSB7XG4gICAgJCh0aGlzLl9lbGVtZW50KS5yZW1vdmVDbGFzcygnb3BlbicpO1xuICAgIHRoaXMuX2NvbXBvbmVudCA9IG51bGw7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IE1vYmlsZU5hdmJhckRyb3Bkb3duKCk7XG4iLCJpbXBvcnQgUmVhY3RET00gZnJvbSAncmVhY3QtZG9tJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGNsYXNzIE1vZGFsIHtcbiAgaW5pdChlbGVtZW50KSB7XG4gICAgdGhpcy5fZWxlbWVudCA9IGVsZW1lbnQ7XG5cbiAgICB0aGlzLl9tb2RhbCA9ICQoZWxlbWVudCkubW9kYWwoe3Nob3c6IGZhbHNlfSk7XG5cbiAgICB0aGlzLl9tb2RhbC5vbignaGlkZGVuLmJzLm1vZGFsJywgKCkgPT4ge1xuICAgICAgUmVhY3RET00udW5tb3VudENvbXBvbmVudEF0Tm9kZSh0aGlzLl9lbGVtZW50KTtcbiAgICB9KTtcbiAgfVxuXG4gIHNob3coY29tcG9uZW50KSB7XG4gICAgbW91bnQoY29tcG9uZW50LCB0aGlzLl9lbGVtZW50LmlkKTtcbiAgICB0aGlzLl9tb2RhbC5tb2RhbCgnc2hvdycpO1xuICB9XG5cbiAgaGlkZSgpIHtcbiAgICB0aGlzLl9tb2RhbC5tb2RhbCgnaGlkZScpO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBNb2RhbCgpO1xuIiwiZXhwb3J0IGNsYXNzIFBhZ2VUaXRsZSB7XG4gIGluaXQoZm9ydW1OYW1lKSB7XG4gICAgdGhpcy5fZm9ydW1OYW1lID0gZm9ydW1OYW1lO1xuICB9XG5cbiAgc2V0KHRpdGxlKSB7XG4gICAgaWYgKHR5cGVvZiB0aXRsZSA9PT0gJ3N0cmluZycpIHtcbiAgICAgIHRpdGxlID0ge3RpdGxlOiB0aXRsZX07XG4gICAgfVxuXG4gICAgbGV0IGZpbmFsVGl0bGUgPSB0aXRsZS50aXRsZTtcblxuICAgIGlmICh0aXRsZS5wYWdlKSB7XG4gICAgICBsZXQgcGFnZUxhYmVsID0gaW50ZXJwb2xhdGUoZ2V0dGV4dCgncGFnZSAlKHBhZ2UpcycpLCB7XG4gICAgICAgIHBhZ2U6IHRpdGxlLnBhZ2VcbiAgICAgIH0sIHRydWUpO1xuXG4gICAgICBmaW5hbFRpdGxlICs9ICcgKCcgKyBwYWdlTGFiZWwgKyAnKSc7XG4gICAgfVxuXG4gICAgaWYgKHRpdGxlLnBhcmVudCkge1xuICAgICAgZmluYWxUaXRsZSArPSAnIHwgJyArIHRpdGxlLnBhcmVudDtcbiAgICB9XG5cbiAgICBkb2N1bWVudC50aXRsZSA9IGZpbmFsVGl0bGUgKyAnIHwgJyArIHRoaXMuX2ZvcnVtTmFtZTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgUGFnZVRpdGxlKCk7XG4iLCJpbXBvcnQgeyBzaG93U25hY2tiYXIsIGhpZGVTbmFja2JhciB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9zbmFja2Jhcic7XG5cbmNvbnN0IEhJREVfQU5JTUFUSU9OX0xFTkdUSCA9IDMwMDtcbmNvbnN0IE1FU1NBR0VfU0hPV19MRU5HVEggPSA1MDAwO1xuXG5leHBvcnQgY2xhc3MgU25hY2tiYXIge1xuICBpbml0KHN0b3JlKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBzdG9yZTtcbiAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgfVxuXG4gIGFsZXJ0KG1lc3NhZ2UsIHR5cGUpIHtcbiAgICBpZiAodGhpcy5fdGltZW91dCkge1xuICAgICAgd2luZG93LmNsZWFyVGltZW91dCh0aGlzLl90aW1lb3V0KTtcbiAgICAgIHRoaXMuX3N0b3JlLmRpc3BhdGNoKGhpZGVTbmFja2JhcigpKTtcblxuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fdGltZW91dCA9IG51bGw7XG4gICAgICAgIHRoaXMuYWxlcnQobWVzc2FnZSwgdHlwZSk7XG4gICAgICB9LCBISURFX0FOSU1BVElPTl9MRU5HVEgpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaG93U25hY2tiYXIobWVzc2FnZSwgdHlwZSkpO1xuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goaGlkZVNuYWNrYmFyKCkpO1xuICAgICAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgICAgIH0sIE1FU1NBR0VfU0hPV19MRU5HVEgpO1xuICAgIH1cbiAgfVxuXG4gIC8vIHNob3J0aGFuZHMgZm9yIG1lc3NhZ2UgdHlwZXNcblxuICBpbmZvKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdpbmZvJyk7XG4gIH1cblxuICBzdWNjZXNzKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdzdWNjZXNzJyk7XG4gIH1cblxuICB3YXJuaW5nKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICd3YXJuaW5nJyk7XG4gIH1cblxuICBlcnJvcihtZXNzYWdlKSB7XG4gICAgdGhpcy5hbGVydChtZXNzYWdlLCAnZXJyb3InKTtcbiAgfVxuXG4gIC8vIHNob3J0aGFuZCBmb3IgYXBpIGVycm9yc1xuXG4gIGFwaUVycm9yKHJlamVjdGlvbikge1xuICAgIGxldCBtZXNzYWdlID0gZ2V0dGV4dChcIlVua25vd24gZXJyb3IgaGFzIG9jY3VyZWQuXCIpO1xuXG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDApIHtcbiAgICAgIG1lc3NhZ2UgPSByZWplY3Rpb24uZGV0YWlsO1xuICAgIH1cblxuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDAgJiYgcmVqZWN0aW9uLmRldGFpbCkge1xuICAgICAgbWVzc2FnZSA9IHJlamVjdGlvbi5kZXRhaWw7XG4gICAgfVxuXG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMykge1xuICAgICAgbWVzc2FnZSA9IHJlamVjdGlvbi5kZXRhaWw7XG4gICAgICBpZiAobWVzc2FnZSA9PT0gXCJQZXJtaXNzaW9uIGRlbmllZFwiKSB7XG4gICAgICAgIG1lc3NhZ2UgPSBnZXR0ZXh0KFxuICAgICAgICAgIFwiWW91IGRvbid0IGhhdmUgcGVybWlzc2lvbiB0byBwZXJmb3JtIHRoaXMgYWN0aW9uLlwiKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDA0KSB7XG4gICAgICBtZXNzYWdlID0gZ2V0dGV4dChcIkFjdGlvbiBsaW5rIGlzIGludmFsaWQuXCIpO1xuICAgIH1cblxuICAgIHRoaXMuZXJyb3IobWVzc2FnZSk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IFNuYWNrYmFyKCk7XG4iLCJpbXBvcnQgeyBjb21iaW5lUmVkdWNlcnMsIGNyZWF0ZVN0b3JlIH0gZnJvbSAncmVkdXgnO1xuXG5leHBvcnQgY2xhc3MgU3RvcmVXcmFwcGVyIHtcbiAgY29uc3RydWN0b3IoKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBudWxsO1xuICAgIHRoaXMuX3JlZHVjZXJzID0ge307XG4gICAgdGhpcy5faW5pdGlhbFN0YXRlID0ge307XG4gIH1cblxuICBhZGRSZWR1Y2VyKG5hbWUsIHJlZHVjZXIsIGluaXRpYWxTdGF0ZSkge1xuICAgIHRoaXMuX3JlZHVjZXJzW25hbWVdID0gcmVkdWNlcjtcbiAgICB0aGlzLl9pbml0aWFsU3RhdGVbbmFtZV0gPSBpbml0aWFsU3RhdGU7XG4gIH1cblxuICBpbml0KCkge1xuICAgIHRoaXMuX3N0b3JlID0gY3JlYXRlU3RvcmUoXG4gICAgICBjb21iaW5lUmVkdWNlcnModGhpcy5fcmVkdWNlcnMpLCB0aGlzLl9pbml0aWFsU3RhdGUpO1xuICB9XG5cbiAgZ2V0U3RvcmUoKSB7XG4gICAgcmV0dXJuIHRoaXMuX3N0b3JlO1xuICB9XG5cbiAgLy8gU3RvcmUgQVBJXG5cbiAgZ2V0U3RhdGUoKSB7XG4gICAgcmV0dXJuIHRoaXMuX3N0b3JlLmdldFN0YXRlKCk7XG4gIH1cblxuICBkaXNwYXRjaChhY3Rpb24pIHtcbiAgICByZXR1cm4gdGhpcy5fc3RvcmUuZGlzcGF0Y2goYWN0aW9uKTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgU3RvcmVXcmFwcGVyKCk7XG4iLCIvKiBnbG9iYWwgenhjdmJuICovXG5leHBvcnQgY2xhc3MgWnhjdmJuIHtcbiAgaW5pdChpbmNsdWRlKSB7XG4gICAgdGhpcy5faW5jbHVkZSA9IGluY2x1ZGU7XG4gIH1cblxuICBzY29yZVBhc3N3b3JkKHBhc3N3b3JkLCBpbnB1dHMpIHtcbiAgICAvLyAwLTQgc2NvcmUsIHRoZSBtb3JlIHRoZSBzdHJvbmdlciBwYXNzd29yZFxuICAgIHJldHVybiB6eGN2Ym4ocGFzc3dvcmQsIGlucHV0cykuc2NvcmU7XG4gIH1cblxuICBsb2FkKCkge1xuICAgIGlmICh0eXBlb2YgenhjdmJuID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgICB0aGlzLl9pbmNsdWRlLmluY2x1ZGUoJ21pc2Fnby9qcy96eGN2Ym4uanMnKTtcbiAgICAgIHJldHVybiB0aGlzLl9sb2FkaW5nUHJvbWlzZSgpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gdGhpcy5fbG9hZGVkUHJvbWlzZSgpO1xuICAgIH1cbiAgfVxuXG4gIF9sb2FkaW5nUHJvbWlzZSgpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoZnVuY3Rpb24ocmVzb2x2ZSkge1xuICAgICAgdmFyIHdhaXQgPSBmdW5jdGlvbigpIHtcbiAgICAgICAgaWYgKHR5cGVvZiB6eGN2Ym4gPT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICB3aW5kb3cuc2V0VGltZW91dChmdW5jdGlvbigpIHtcbiAgICAgICAgICAgIHdhaXQoKTtcbiAgICAgICAgICB9LCAyMDApO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJlc29sdmUoKTtcbiAgICAgICAgfVxuICAgICAgfTtcbiAgICAgIHdhaXQoKTtcbiAgICB9KTtcbiAgfVxuXG4gIF9sb2FkZWRQcm9taXNlKCkge1xuICAgIC8vIHdlIGhhdmUgYWxyZWFkeSBsb2FkZWQgenhjdmJuLmpzLCByZXNvbHZlIGF3YXkhXG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUpIHtcbiAgICAgIHJlc29sdmUoKTtcbiAgICB9KTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgWnhjdmJuKCk7IiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5pbXBvcnQgeyBQcm92aWRlciwgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQmFubmVkUGFnZSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9iYW5uZWQtcGFnZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG4vKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG5sZXQgc2VsZWN0ID0gZnVuY3Rpb24oc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLnRpY2s7XG59O1xuXG5sZXQgUmVkcmF3ZWRCYW5uZWRQYWdlID0gY29ubmVjdChzZWxlY3QpKEJhbm5lZFBhZ2UpO1xuLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24oYmFuLCBjaGFuZ2VTdGF0ZSkge1xuICBSZWFjdERPTS5yZW5kZXIoXG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIDxQcm92aWRlciBzdG9yZT17c3RvcmUuZ2V0U3RvcmUoKX0+XG4gICAgICA8UmVkcmF3ZWRCYW5uZWRQYWdlIG1lc3NhZ2U9e2Jhbi5tZXNzYWdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICBleHBpcmVzPXtiYW4uZXhwaXJlc19vbiA/IG1vbWVudChiYW4uZXhwaXJlc19vbikgOiBudWxsfSAvPlxuICAgIDwvUHJvdmlkZXI+LFxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3BhZ2UtbW91bnQnKVxuICApO1xuXG4gIGlmICh0eXBlb2YgY2hhbmdlU3RhdGUgPT09ICd1bmRlZmluZWQnIHx8IGNoYW5nZVN0YXRlKSB7XG4gICAgbGV0IGZvcnVtTmFtZSA9IG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykuZm9ydW1fbmFtZTtcbiAgICBkb2N1bWVudC50aXRsZSA9IGdldHRleHQoXCJZb3UgYXJlIGJhbm5lZFwiKSArICcgfCAnICsgZm9ydW1OYW1lO1xuICAgIHdpbmRvdy5oaXN0b3J5LnB1c2hTdGF0ZSh7fSwgXCJcIiwgbWlzYWdvLmdldCgnQkFOTkVEX1VSTCcpKTtcbiAgfVxufSIsImV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uKGxpc3QsIHJvd1dpZHRoLCBwYWRkaW5nPWZhbHNlKSB7XG4gIGxldCByb3dzID0gW107XG4gIGxldCByb3cgPSBbXTtcblxuICBsaXN0LmZvckVhY2goZnVuY3Rpb24oZWxlbWVudCkge1xuICAgIHJvdy5wdXNoKGVsZW1lbnQpO1xuICAgIGlmIChyb3cubGVuZ3RoID09PSByb3dXaWR0aCkge1xuICAgICAgcm93cy5wdXNoKHJvdyk7XG4gICAgICByb3cgPSBbXTtcbiAgICB9XG4gIH0pO1xuXG4gIC8vIHBhZCByb3cgdG8gcmVxdWlyZWQgbGVuZ3RoP1xuICBpZiAocGFkZGluZyAhPT0gZmFsc2UgJiYgcm93Lmxlbmd0aCA+IDAgJiYgcm93Lmxlbmd0aCA8IHJvd1dpZHRoKSB7XG4gICAgZm9yIChsZXQgaSA9IHJvdy5sZW5ndGg7IGkgPCByb3dXaWR0aDsgaSArKykge1xuICAgICAgcm93LnB1c2gocGFkZGluZyk7XG4gICAgfVxuICB9XG5cbiAgaWYgKHJvdy5sZW5ndGgpIHtcbiAgICByb3dzLnB1c2gocm93KTtcbiAgfVxuXG4gIHJldHVybiByb3dzO1xufSIsImV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uKGJ5dGVzKSB7XG4gIGlmIChieXRlcyA+IDEwMDAgKiAxMDAwICogMTAwMCkge1xuICAgIHJldHVybiAoTWF0aC5yb3VuZChieXRlcyAqIDEwMCAvICgxMDAwICogMTAwMCAqIDEwMDApKSAvIDEwMCkgKyAnIEdCJztcbiAgfSBlbHNlIGlmIChieXRlcyA+IDEwMDAgKiAxMDAwKSB7XG4gICAgcmV0dXJuIChNYXRoLnJvdW5kKGJ5dGVzICogMTAwIC8gKDEwMDAgKiAxMDAwKSkgLyAxMDApICsgJyBNQic7XG4gIH0gZWxzZSBpZiAoYnl0ZXMgPiAxMDAwKSB7XG4gICAgcmV0dXJuIChNYXRoLnJvdW5kKGJ5dGVzICogMTAwIC8gMTAwMCkgLyAxMDApICsgJyBLQic7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIChNYXRoLnJvdW5kKGJ5dGVzICogMTAwKSAvIDEwMCkgKyAnIEInO1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgUmVhY3RET00gZnJvbSAncmVhY3QtZG9tJztcbmltcG9ydCB7IFByb3ZpZGVyIH0gZnJvbSAncmVhY3QtcmVkdXgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24oQ29tcG9uZW50LCByb290RWxlbWVudElkLCBjb25uZWN0ZWQ9dHJ1ZSkge1xuICBsZXQgcm9vdEVsZW1lbnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChyb290RWxlbWVudElkKTtcblxuICBpZiAocm9vdEVsZW1lbnQpIHtcbiAgICBpZiAoY29ubmVjdGVkKSB7XG4gICAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgICAgPFByb3ZpZGVyIHN0b3JlPXtzdG9yZS5nZXRTdG9yZSgpfT5cbiAgICAgICAgICA8Q29tcG9uZW50IC8+XG4gICAgICAgIDwvUHJvdmlkZXI+LFxuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgICByb290RWxlbWVudFxuICAgICAgKTtcbiAgICB9IGVsc2Uge1xuICAgICAgUmVhY3RET00ucmVuZGVyKFxuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIDxDb21wb25lbnQgLz4sXG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgICAgIHJvb3RFbGVtZW50XG4gICAgICApO1xuICAgIH1cbiAgfVxufVxuIiwiY2xhc3MgT3JkZXJlZExpc3Qge1xuICAgIGNvbnN0cnVjdG9yKGl0ZW1zKSB7XG4gICAgICB0aGlzLmlzT3JkZXJlZCA9IGZhbHNlO1xuICAgICAgdGhpcy5faXRlbXMgPSBpdGVtcyB8fCBbXTtcbiAgICB9XG5cbiAgICBhZGQoa2V5LCBpdGVtLCBvcmRlcikge1xuICAgICAgdGhpcy5faXRlbXMucHVzaCh7XG4gICAgICAgIGtleToga2V5LFxuICAgICAgICBpdGVtOiBpdGVtLFxuXG4gICAgICAgIGFmdGVyOiBvcmRlciA/IG9yZGVyLmFmdGVyIHx8IG51bGwgOiBudWxsLFxuICAgICAgICBiZWZvcmU6IG9yZGVyID8gb3JkZXIuYmVmb3JlIHx8IG51bGwgOiBudWxsXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBnZXQoa2V5LCB2YWx1ZSkge1xuICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLl9pdGVtcy5sZW5ndGg7IGkrKykge1xuICAgICAgICBpZiAodGhpcy5faXRlbXNbaV0ua2V5ID09PSBrZXkpIHtcbiAgICAgICAgICByZXR1cm4gdGhpcy5faXRlbXNbaV0uaXRlbTtcbiAgICAgICAgfVxuICAgICAgfVxuXG4gICAgICByZXR1cm4gdmFsdWU7XG4gICAgfVxuXG4gICAgaGFzKGtleSkge1xuICAgICAgcmV0dXJuIHRoaXMuZ2V0KGtleSkgIT09IHVuZGVmaW5lZDtcbiAgICB9XG5cbiAgICB2YWx1ZXMoKSB7XG4gICAgICB2YXIgdmFsdWVzID0gW107XG4gICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMuX2l0ZW1zLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIHZhbHVlcy5wdXNoKHRoaXMuX2l0ZW1zW2ldLml0ZW0pO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHZhbHVlcztcbiAgICB9XG5cbiAgICBvcmRlcih2YWx1ZXNfb25seSkge1xuICAgICAgaWYgKCF0aGlzLmlzT3JkZXJlZCkge1xuICAgICAgICB0aGlzLl9pdGVtcyA9IHRoaXMuX29yZGVyKHRoaXMuX2l0ZW1zKTtcbiAgICAgICAgdGhpcy5pc09yZGVyZWQgPSB0cnVlO1xuICAgICAgfVxuXG4gICAgICBpZiAodmFsdWVzX29ubHkgfHwgdHlwZW9mIHZhbHVlc19vbmx5ID09PSAndW5kZWZpbmVkJykge1xuICAgICAgICByZXR1cm4gdGhpcy52YWx1ZXMoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9pdGVtcztcbiAgICAgIH1cbiAgICB9XG5cbiAgICBvcmRlcmVkVmFsdWVzKCkge1xuICAgICAgcmV0dXJuIHRoaXMub3JkZXIodHJ1ZSk7XG4gICAgfVxuXG4gICAgX29yZGVyKHVub3JkZXJlZCkge1xuICAgICAgLy8gSW5kZXggb2YgdW5vcmRlcmVkIGl0ZW1zXG4gICAgICB2YXIgaW5kZXggPSBbXTtcbiAgICAgIHVub3JkZXJlZC5mb3JFYWNoKGZ1bmN0aW9uIChpdGVtKSB7XG4gICAgICAgIGluZGV4LnB1c2goaXRlbS5rZXkpO1xuICAgICAgfSk7XG5cbiAgICAgIC8vIE9yZGVyZWQgaXRlbXNcbiAgICAgIHZhciBvcmRlcmVkID0gW107XG4gICAgICB2YXIgb3JkZXJpbmcgPSBbXTtcblxuICAgICAgLy8gRmlyc3QgcGFzczogcmVnaXN0ZXIgaXRlbXMgdGhhdFxuICAgICAgLy8gZG9uJ3Qgc3BlY2lmeSB0aGVpciBvcmRlclxuICAgICAgdW5vcmRlcmVkLmZvckVhY2goZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICAgICAgaWYgKCFpdGVtLmFmdGVyICYmICFpdGVtLmJlZm9yZSkge1xuICAgICAgICAgIG9yZGVyZWQucHVzaChpdGVtKTtcbiAgICAgICAgICBvcmRlcmluZy5wdXNoKGl0ZW0ua2V5KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIC8vIFNlY29uZCBwYXNzOiByZWdpc3RlciBpdGVtcyB0aGF0XG4gICAgICAvLyBzcGVjaWZ5IHRoZWlyIGJlZm9yZSB0byBcIl9lbmRcIlxuICAgICAgdW5vcmRlcmVkLmZvckVhY2goZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICAgICAgaWYgKGl0ZW0uYmVmb3JlID09PSBcIl9lbmRcIikge1xuICAgICAgICAgIG9yZGVyZWQucHVzaChpdGVtKTtcbiAgICAgICAgICBvcmRlcmluZy5wdXNoKGl0ZW0ua2V5KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIC8vIFRoaXJkIHBhc3M6IGtlZXAgaXRlcmF0aW5nIGl0ZW1zXG4gICAgICAvLyB1bnRpbCB3ZSBoaXQgaXRlcmF0aW9ucyBsaW1pdCBvciBmaW5pc2hcbiAgICAgIC8vIG9yZGVyaW5nIGxpc3RcbiAgICAgIGZ1bmN0aW9uIGluc2VydEl0ZW0oaXRlbSkge1xuICAgICAgICB2YXIgaW5zZXJ0QXQgPSAtMTtcbiAgICAgICAgaWYgKG9yZGVyaW5nLmluZGV4T2YoaXRlbS5rZXkpID09PSAtMSkge1xuICAgICAgICAgIGlmIChpdGVtLmFmdGVyKSB7XG4gICAgICAgICAgICBpbnNlcnRBdCA9IG9yZGVyaW5nLmluZGV4T2YoaXRlbS5hZnRlcik7XG4gICAgICAgICAgICBpZiAoaW5zZXJ0QXQgIT09IC0xKSB7XG4gICAgICAgICAgICAgIGluc2VydEF0ICs9IDE7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSBlbHNlIGlmIChpdGVtLmJlZm9yZSkge1xuICAgICAgICAgICAgaW5zZXJ0QXQgPSBvcmRlcmluZy5pbmRleE9mKGl0ZW0uYmVmb3JlKTtcbiAgICAgICAgICB9XG5cbiAgICAgICAgICBpZiAoaW5zZXJ0QXQgIT09IC0xKSB7XG4gICAgICAgICAgICBvcmRlcmVkLnNwbGljZShpbnNlcnRBdCwgMCwgaXRlbSk7XG4gICAgICAgICAgICBvcmRlcmluZy5zcGxpY2UoaW5zZXJ0QXQsIDAsIGl0ZW0ua2V5KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgdmFyIGl0ZXJhdGlvbnMgPSAyMDA7XG4gICAgICB3aGlsZSAoaXRlcmF0aW9ucyA+IDAgJiYgaW5kZXgubGVuZ3RoICE9PSBvcmRlcmluZy5sZW5ndGgpIHtcbiAgICAgICAgaXRlcmF0aW9ucyAtPSAxO1xuICAgICAgICB1bm9yZGVyZWQuZm9yRWFjaChpbnNlcnRJdGVtKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIG9yZGVyZWQ7XG4gICAgfVxuICB9XG5cbiAgZXhwb3J0IGRlZmF1bHQgT3JkZXJlZExpc3Q7XG4iLCJleHBvcnQgZnVuY3Rpb24gaW50KG1pbiwgbWF4KSB7XG4gIHJldHVybiBNYXRoLmZsb29yKChNYXRoLnJhbmRvbSgpICogKG1heCArIDEpKSkgKyBtaW47XG59XG5cbmV4cG9ydCBmdW5jdGlvbiByYW5nZShtaW4sIG1heCkge1xuICBsZXQgYXJyYXkgPSBuZXcgQXJyYXkoaW50KG1pbiwgbWF4KSk7XG4gIGZvcihsZXQgaT0wOyBpPGFycmF5Lmxlbmd0aDsgaSsrKXtcbiAgICBhcnJheVtpXSA9IGk7XG4gIH1cblxuICByZXR1cm4gYXJyYXk7XG59IiwiLy8ganNoaW50IGlnbm9yZTpzdGFydFxuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IHsgUHJvdmlkZXIgfSBmcm9tICdyZWFjdC1yZWR1eCc7XG5pbXBvcnQgeyBSb3V0ZXIgfSBmcm9tICdyZWFjdC1yb3V0ZXInO1xuaW1wb3J0IGNyZWF0ZUhpc3RvcnkgZnJvbSAnaGlzdG9yeS9saWIvY3JlYXRlQnJvd3Nlckhpc3RvcnknO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmNvbnN0IHJvb3RFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3BhZ2UtbW91bnQnKTtcbmNvbnN0IGhpc3RvcnkgPSBuZXcgY3JlYXRlSGlzdG9yeSgpO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbihvcHRpb25zKSB7XG4gIGxldCByb3V0ZXMgPSB7XG4gICAgY29tcG9uZW50OiBvcHRpb25zLmNvbXBvbmVudCxcbiAgICBjaGlsZFJvdXRlczogW1xuICAgICAge1xuICAgICAgICBwYXRoOiBvcHRpb25zLnJvb3QsXG4gICAgICAgIG9uRW50ZXI6IGZ1bmN0aW9uKG5leHRTdGF0ZSwgcmVwbGFjZVN0YXRlKSB7XG4gICAgICAgICAgcmVwbGFjZVN0YXRlKG51bGwsIG9wdGlvbnMucGF0aHNbMF0ucGF0aCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICBdLmNvbmNhdChvcHRpb25zLnBhdGhzLm1hcChmdW5jdGlvbihwYXRoKSB7XG4gICAgICByZXR1cm4gcGF0aDtcbiAgICB9KSlcbiAgfTtcblxuICBSZWFjdERPTS5yZW5kZXIoXG4gICAgPFByb3ZpZGVyIHN0b3JlPXtzdG9yZS5nZXRTdG9yZSgpfT5cbiAgICAgIDxSb3V0ZXIgcm91dGVzPXtyb3V0ZXN9IGhpc3Rvcnk9e2hpc3Rvcnl9IC8+XG4gICAgPC9Qcm92aWRlcj4sXG4gICAgcm9vdEVsZW1lbnRcbiAgKTtcbn1cbiIsImNvbnN0IEVNQUlMID0gL14oKFtePD4oKVtcXF1cXC4sOzpcXHNAXFxcIl0rKFxcLltePD4oKVtcXF1cXC4sOzpcXHNAXFxcIl0rKSopfChcXFwiLitcXFwiKSlAKChbXjw+KClbXFxdXFwuLDs6XFxzQFxcXCJdK1xcLikrW148PigpW1xcXVxcLiw7Olxcc0BcXFwiXXsyLH0pJC9pO1xuY29uc3QgVVNFUk5BTUUgPSBuZXcgUmVnRXhwKCdeWzAtOWEtel0rJCcsICdpJyk7XG5cbmV4cG9ydCBmdW5jdGlvbiByZXF1aXJlZCgpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgaWYgKCQudHJpbSh2YWx1ZSkubGVuZ3RoID09PSAwKSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIlRoaXMgZmllbGQgaXMgcmVxdWlyZWQuXCIpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGVtYWlsKG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgaWYgKCFFTUFJTC50ZXN0KHZhbHVlKSkge1xuICAgICAgcmV0dXJuIG1lc3NhZ2UgfHwgZ2V0dGV4dChcIkVudGVyIGEgdmFsaWQgZW1haWwgYWRkcmVzcy5cIik7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gbWluTGVuZ3RoKGxpbWl0VmFsdWUsIG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgdmFyIHJldHVybk1lc3NhZ2UgPSAnJztcbiAgICB2YXIgbGVuZ3RoID0gJC50cmltKHZhbHVlKS5sZW5ndGg7XG5cbiAgICBpZiAobGVuZ3RoIDwgbGltaXRWYWx1ZSkge1xuICAgICAgaWYgKG1lc3NhZ2UpIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG1lc3NhZ2UobGltaXRWYWx1ZSwgbGVuZ3RoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybk1lc3NhZ2UgPSBuZ2V0dGV4dChcbiAgICAgICAgICBcIkVuc3VyZSB0aGlzIHZhbHVlIGhhcyBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIChpdCBoYXMgJShzaG93X3ZhbHVlKXMpLlwiLFxuICAgICAgICAgIFwiRW5zdXJlIHRoaXMgdmFsdWUgaGFzIGF0IGxlYXN0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXJzIChpdCBoYXMgJShzaG93X3ZhbHVlKXMpLlwiLFxuICAgICAgICAgIGxpbWl0VmFsdWUpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGludGVycG9sYXRlKHJldHVybk1lc3NhZ2UsIHtcbiAgICAgICAgbGltaXRfdmFsdWU6IGxpbWl0VmFsdWUsXG4gICAgICAgIHNob3dfdmFsdWU6IGxlbmd0aFxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gbWF4TGVuZ3RoKGxpbWl0VmFsdWUsIG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgdmFyIHJldHVybk1lc3NhZ2UgPSAnJztcbiAgICB2YXIgbGVuZ3RoID0gJC50cmltKHZhbHVlKS5sZW5ndGg7XG5cbiAgICBpZiAobGVuZ3RoID4gbGltaXRWYWx1ZSkge1xuICAgICAgaWYgKG1lc3NhZ2UpIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG1lc3NhZ2UobGltaXRWYWx1ZSwgbGVuZ3RoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybk1lc3NhZ2UgPSBuZ2V0dGV4dChcbiAgICAgICAgICBcIkVuc3VyZSB0aGlzIHZhbHVlIGhhcyBhdCBtb3N0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXIgKGl0IGhhcyAlKHNob3dfdmFsdWUpcykuXCIsXG4gICAgICAgICAgXCJFbnN1cmUgdGhpcyB2YWx1ZSBoYXMgYXQgbW9zdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVycyAoaXQgaGFzICUoc2hvd192YWx1ZSlzKS5cIixcbiAgICAgICAgICBsaW1pdFZhbHVlKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBpbnRlcnBvbGF0ZShyZXR1cm5NZXNzYWdlLCB7XG4gICAgICAgIGxpbWl0X3ZhbHVlOiBsaW1pdFZhbHVlLFxuICAgICAgICBzaG93X3ZhbHVlOiBsZW5ndGhcbiAgICAgIH0sIHRydWUpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVzZXJuYW1lTWluTGVuZ3RoKHNldHRpbmdzKSB7XG4gIHZhciBtZXNzYWdlID0gZnVuY3Rpb24obGltaXRWYWx1ZSkge1xuICAgIHJldHVybiBuZ2V0dGV4dChcbiAgICAgIFwiVXNlcm5hbWUgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIGxvbmcuXCIsXG4gICAgICBcIlVzZXJuYW1lIG11c3QgYmUgYXQgbGVhc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMgbG9uZy5cIixcbiAgICAgIGxpbWl0VmFsdWUpO1xuICB9O1xuICByZXR1cm4gdGhpcy5taW5MZW5ndGgoc2V0dGluZ3MudXNlcm5hbWVfbGVuZ3RoX21pbiwgbWVzc2FnZSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VybmFtZU1heExlbmd0aChzZXR0aW5ncykge1xuICB2YXIgbWVzc2FnZSA9IGZ1bmN0aW9uKGxpbWl0VmFsdWUpIHtcbiAgICByZXR1cm4gbmdldHRleHQoXG4gICAgICBcIlVzZXJuYW1lIGNhbm5vdCBiZSBsb25nZXIgdGhhbiAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyLlwiLFxuICAgICAgXCJVc2VybmFtZSBjYW5ub3QgYmUgbG9uZ2VyIHRoYW4gJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMuXCIsXG4gICAgICBsaW1pdFZhbHVlKTtcbiAgfTtcbiAgcmV0dXJuIHRoaXMubWF4TGVuZ3RoKHNldHRpbmdzLnVzZXJuYW1lX2xlbmd0aF9tYXgsIG1lc3NhZ2UpO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlcm5hbWVDb250ZW50KCkge1xuICByZXR1cm4gZnVuY3Rpb24odmFsdWUpIHtcbiAgICBpZiAoIVVTRVJOQU1FLnRlc3QoJC50cmltKHZhbHVlKSkpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiVXNlcm5hbWUgY2FuIG9ubHkgY29udGFpbiBsYXRpbiBhbHBoYWJldCBsZXR0ZXJzIGFuZCBkaWdpdHMuXCIpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHBhc3N3b3JkTWluTGVuZ3RoKHNldHRpbmdzKSB7XG4gIHZhciBtZXNzYWdlID0gZnVuY3Rpb24obGltaXRWYWx1ZSkge1xuICAgIHJldHVybiBuZ2V0dGV4dChcbiAgICAgIFwiVmFsaWQgcGFzc3dvcmQgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIGxvbmcuXCIsXG4gICAgICBcIlZhbGlkIHBhc3N3b3JkIG11c3QgYmUgYXQgbGVhc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMgbG9uZy5cIixcbiAgICAgIGxpbWl0VmFsdWUpO1xuICB9O1xuICByZXR1cm4gdGhpcy5taW5MZW5ndGgoc2V0dGluZ3MucGFzc3dvcmRfbGVuZ3RoX21pbiwgbWVzc2FnZSk7XG59Il19
