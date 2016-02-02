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

},{"../../../../documents/misago/frontend/src/utils/ordered-list":105}],3:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/ajax":90}],4:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/auth-message":48,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/utils/mount-component":104,"react-redux":"react-redux"}],5:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/reducers/auth":85,"../../../../../documents/misago/frontend/src/services/store":99}],6:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/auth":91,"../../../../../documents/misago/frontend/src/services/local-storage":94,"../../../../../documents/misago/frontend/src/services/modal":96,"../../../../../documents/misago/frontend/src/services/store":99}],7:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/utils/banned-page":101}],8:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/ajax":90,"../../../../../documents/misago/frontend/src/services/captcha":92,"../../../../../documents/misago/frontend/src/services/include":93,"../../../../../documents/misago/frontend/src/services/snackbar":98}],9:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/include":93}],10:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/local-storage":94}],11:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/mobile-navbar-dropdown":95}],12:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/modal":96}],13:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"moment":"moment"}],14:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/options/root":65,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/store":99,"../../../../../documents/misago/frontend/src/utils/routed-component":107}],15:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/page-title":97}],16:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/request-activation-link":70,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/utils/mount-component":104}],17:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/request-password-reset":71,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/utils/mount-component":104}],18:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/reset-password-form":72,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/utils/mount-component":104}],19:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/snackbar":75,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/utils/mount-component":104,"react-redux":"react-redux"}],20:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/reducers/snackbar":86,"../../../../../documents/misago/frontend/src/services/store":99}],21:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/snackbar":98,"../../../../../documents/misago/frontend/src/services/store":99}],22:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/store":99}],23:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/reducers/tick":87,"../../../../../documents/misago/frontend/src/services/store":99}],24:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/reducers/tick":87,"../../../../../documents/misago/frontend/src/services/store":99}],25:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/user-menu/root":77,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/utils/mount-component":104,"react-redux":"react-redux"}],26:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/reducers/username-history":88,"../../../../../documents/misago/frontend/src/services/store":99}],27:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/users/root":82,"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/store":99,"../../../../../documents/misago/frontend/src/utils/routed-component":107}],28:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/reducers/users":89,"../../../../../documents/misago/frontend/src/services/store":99}],29:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":84,"../../../../../documents/misago/frontend/src/services/include":93,"../../../../../documents/misago/frontend/src/services/zxcvbn":100}],30:[function(require,module,exports){
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

},{"../../services/ajax":90,"../../services/snackbar":98,"../avatar":49,"../button":51,"react":"react"}],53:[function(require,module,exports){
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

},{"../../index":84,"../../services/ajax":90,"../../services/snackbar":98,"../../utils/batch":102,"../button":51,"react":"react"}],54:[function(require,module,exports){
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

},{"../../services/ajax":90,"../../services/snackbar":98,"../avatar":49,"../button":51,"../loader":60,"react":"react"}],55:[function(require,module,exports){
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

},{"../../reducers/users":89,"../../services/ajax":90,"../../services/store":99,"../modal-loader":61,"./crop":52,"./gallery":53,"./index":54,"./upload":56,"react":"react"}],56:[function(require,module,exports){
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

},{"../../services/ajax":90,"../../services/snackbar":98,"../../utils/file-size":103,"../button":51,"./crop":52,"react":"react"}],57:[function(require,module,exports){
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

},{"../utils/validators":108,"react":"react"}],59:[function(require,module,exports){
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

},{"../../index":84,"../../reducers/username-history":88,"../../reducers/users":89,"../../services/ajax":90,"../../services/page-title":97,"../../services/snackbar":98,"../../services/store":99,"../../utils/random":106,"../../utils/validators":108,"../avatar":49,"../button":51,"../form":58,"../form-group":57,"../loader":60,"moment":"moment","react":"react"}],63:[function(require,module,exports){
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

},{"../../reducers/auth":85,"../../services/ajax":90,"../../services/page-title":97,"../../services/snackbar":98,"../../services/store":99,"../button":51,"../form":58,"../form-group":57,"../select":73,"../yes-no-switch":83,"react":"react"}],64:[function(require,module,exports){
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

},{"../../index":84,"../li":59,"react":"react","react-router":"react-router"}],65:[function(require,module,exports){
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

},{"../../index":84,"./change-username":62,"./forum-options":63,"./navs":64,"./sign-in-credentials":66,"react":"react","react-redux":"react-redux"}],66:[function(require,module,exports){
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

},{"../../index":84,"../../services/ajax":90,"../../services/page-title":97,"../../services/snackbar":98,"../../utils/validators":108,"../button":51,"../form":58,"../form-group":57,"react":"react"}],67:[function(require,module,exports){
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

},{"../services/zxcvbn":100,"react":"react"}],68:[function(require,module,exports){
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

},{"../services/captcha":92,"../services/modal":96,"../services/snackbar":98,"../services/zxcvbn":100,"./loader":60,"./register.js":69,"react":"react"}],69:[function(require,module,exports){
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

},{"../index":84,"../services/ajax":90,"../services/auth":91,"../services/captcha":92,"../services/modal":96,"../services/snackbar":98,"../utils/banned-page":101,"../utils/validators":108,"./button":51,"./form":58,"./form-group":57,"./password-strength":67,"react":"react"}],70:[function(require,module,exports){
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

},{"../index":84,"../services/ajax":90,"../services/snackbar":98,"../utils/banned-page":101,"../utils/validators":108,"./button":51,"./form":58,"react":"react"}],71:[function(require,module,exports){
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

},{"../index":84,"../services/ajax":90,"../services/snackbar":98,"../utils/banned-page":101,"../utils/validators":108,"./button":51,"./form":58,"react":"react","react-dom":"react-dom"}],72:[function(require,module,exports){
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

},{"../index":84,"../services/ajax":90,"../services/auth":91,"../services/modal":96,"../services/snackbar":98,"../utils/banned-page":101,"../utils/validators":108,"./button":51,"./form":58,"./sign-in.js":74,"react":"react","react-dom":"react-dom"}],73:[function(require,module,exports){
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

},{"../index":84,"../services/ajax":90,"../services/modal":96,"../services/snackbar":98,"../utils/banned-page":101,"./button":51,"./form":58,"react":"react"}],75:[function(require,module,exports){
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

},{"../../services/mobile-navbar-dropdown":95,"../../services/modal":96,"../avatar":49,"../register-button":68,"../sign-in.js":74,"react":"react"}],77:[function(require,module,exports){
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

},{"../../index":84,"../../services/mobile-navbar-dropdown":95,"../../services/modal":96,"../avatar":49,"../change-avatar/root":55,"react":"react","react-redux":"react-redux"}],79:[function(require,module,exports){
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
          { className: 'user-title' },
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

},{"../../index":84,"../../reducers/users":89,"../../services/page-title":97,"../../services/store":99,"../avatar":49,"react":"react","react-router":"react-router"}],80:[function(require,module,exports){
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

},{"../../index":84,"../li":59,"react":"react","react-router":"react-router"}],81:[function(require,module,exports){
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

},{"../../services/page-title":97,"react":"react"}],82:[function(require,module,exports){
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

},{"../../index":84,"./active-posters":79,"./navs":80,"./rank":81,"react":"react","react-redux":"react-redux"}],83:[function(require,module,exports){
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

},{"react":"react"}],84:[function(require,module,exports){
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

},{"./utils/ordered-list":105}],85:[function(require,module,exports){
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

},{"./users":89}],86:[function(require,module,exports){
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

},{}],87:[function(require,module,exports){
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

},{}],88:[function(require,module,exports){
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

},{"./users":89,"moment":"moment"}],89:[function(require,module,exports){
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

},{}],90:[function(require,module,exports){
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

},{}],91:[function(require,module,exports){
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

},{"../reducers/auth":85}],92:[function(require,module,exports){
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

},{"../components/form-group":57,"react":"react"}],93:[function(require,module,exports){
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

},{}],94:[function(require,module,exports){
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

},{}],95:[function(require,module,exports){
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

},{"../utils/mount-component":104}],96:[function(require,module,exports){
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

},{"../utils/mount-component":104,"react-dom":"react-dom"}],97:[function(require,module,exports){
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

},{}],98:[function(require,module,exports){
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

},{"../reducers/snackbar":86}],99:[function(require,module,exports){
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

},{"redux":"redux"}],100:[function(require,module,exports){
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

},{}],101:[function(require,module,exports){
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

},{"../components/banned-page":50,"../index":84,"../services/store":99,"moment":"moment","react":"react","react-dom":"react-dom","react-redux":"react-redux"}],102:[function(require,module,exports){
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

},{}],103:[function(require,module,exports){
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

},{}],104:[function(require,module,exports){
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

},{"../services/store":99,"react":"react","react-dom":"react-dom","react-redux":"react-redux"}],105:[function(require,module,exports){
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

},{}],106:[function(require,module,exports){
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

},{}],107:[function(require,module,exports){
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

},{"../services/store":99,"history/lib/createBrowserHistory":38,"react":"react","react-dom":"react-dom","react-redux":"react-redux","react-router":"react-router"}],108:[function(require,module,exports){
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJub2RlX21vZHVsZXMvcHJvY2Vzcy9icm93c2VyLmpzIiwic3JjL2luZGV4LmpzIiwic3JjL2luaXRpYWxpemVycy9hamF4LmpzIiwic3JjL2luaXRpYWxpemVycy9hdXRoLW1lc3NhZ2UtY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy9hdXRoLXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2F1dGguanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2Jhbm5lZC1wYWdlLWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvY2F0Y2hhLmpzIiwic3JjL2luaXRpYWxpemVycy9pbmNsdWRlLmpzIiwic3JjL2luaXRpYWxpemVycy9sb2NhbC1zdG9yYWdlLmpzIiwic3JjL2luaXRpYWxpemVycy9tb2JpbGUtbmF2YmFyLWRyb3Bkb3duLmpzIiwic3JjL2luaXRpYWxpemVycy9tb2RhbC5qcyIsInNyYy9pbml0aWFsaXplcnMvbW9tZW50LWxvY2FsZS5qcyIsInNyYy9pbml0aWFsaXplcnMvb3B0aW9ucy1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3BhZ2UtdGl0bGUuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rLWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvcmVxdWVzdC1wYXNzd29yZC1yZXNldC1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3Jlc2V0LXBhc3N3b3JkLWZvcm0tY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy9zbmFja2Jhci1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3NuYWNrYmFyLXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3NuYWNrYmFyLmpzIiwic3JjL2luaXRpYWxpemVycy9zdG9yZS5qcyIsInNyYy9pbml0aWFsaXplcnMvdGljay1yZWR1Y2VyLmpzIiwic3JjL2luaXRpYWxpemVycy90aWNrLXN0YXJ0LmpzIiwic3JjL2luaXRpYWxpemVycy91c2VyLW1lbnUtY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy91c2VybmFtZS1oaXN0b3J5LXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3VzZXJzLWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvdXNlcnMtcmVkdWNlci5qcyIsInNyYy9pbml0aWFsaXplcnMvenhjdmJuLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvZGVlcC1lcXVhbC9pbmRleC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2RlZXAtZXF1YWwvbGliL2lzX2FyZ3VtZW50cy5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2RlZXAtZXF1YWwvbGliL2tleXMuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9BY3Rpb25zLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaGlzdG9yeS9saWIvQXN5bmNVdGlscy5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL0RPTVN0YXRlU3RvcmFnZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL0RPTVV0aWxzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaGlzdG9yeS9saWIvRXhlY3V0aW9uRW52aXJvbm1lbnQuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9jcmVhdGVCcm93c2VySGlzdG9yeS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL2NyZWF0ZURPTUhpc3RvcnkuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9jcmVhdGVIaXN0b3J5LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaGlzdG9yeS9saWIvY3JlYXRlTG9jYXRpb24uanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9kZXByZWNhdGUuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy9oaXN0b3J5L2xpYi9leHRyYWN0UGF0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL3BhcnNlUGF0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvbm9kZV9tb2R1bGVzL2hpc3RvcnkvbGliL3J1blRyYW5zaXRpb25Ib29rLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9ub2RlX21vZHVsZXMvaW52YXJpYW50L2Jyb3dzZXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL25vZGVfbW9kdWxlcy93YXJuaW5nL2Jyb3dzZXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2F1dGgtbWVzc2FnZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvYXZhdGFyLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9iYW5uZWQtcGFnZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvYnV0dG9uLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL2Nyb3AuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2NoYW5nZS1hdmF0YXIvZ2FsbGVyeS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9pbmRleC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9yb290LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL3VwbG9hZC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvZm9ybS1ncm91cC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvZm9ybS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvbGkuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2xvYWRlci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvbW9kYWwtbG9hZGVyLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9vcHRpb25zL2NoYW5nZS11c2VybmFtZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvb3B0aW9ucy9mb3J1bS1vcHRpb25zLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9vcHRpb25zL25hdnMuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL29wdGlvbnMvcm9vdC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvb3B0aW9ucy9zaWduLWluLWNyZWRlbnRpYWxzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9wYXNzd29yZC1zdHJlbmd0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvcmVnaXN0ZXItYnV0dG9uLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9yZWdpc3Rlci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvcmVxdWVzdC1hY3RpdmF0aW9uLWxpbmsuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3JlcXVlc3QtcGFzc3dvcmQtcmVzZXQuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3Jlc2V0LXBhc3N3b3JkLWZvcm0uanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3NlbGVjdC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvc2lnbi1pbi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvc25hY2tiYXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3VzZXItbWVudS9ndWVzdC1uYXYuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3VzZXItbWVudS9yb290LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy91c2VyLW1lbnUvdXNlci1uYXYuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3VzZXJzL2FjdGl2ZS1wb3N0ZXJzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy91c2Vycy9uYXZzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy91c2Vycy9yYW5rLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy91c2Vycy9yb290LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy95ZXMtbm8tc3dpdGNoLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvaW5kZXguanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9yZWR1Y2Vycy9hdXRoLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvcmVkdWNlcnMvc25hY2tiYXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9yZWR1Y2Vycy90aWNrLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvcmVkdWNlcnMvdXNlcm5hbWUtaGlzdG9yeS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3JlZHVjZXJzL3VzZXJzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvYWpheC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL2F1dGguanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9jYXB0Y2hhLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvaW5jbHVkZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL2xvY2FsLXN0b3JhZ2UuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9tb2JpbGUtbmF2YmFyLWRyb3Bkb3duLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvbW9kYWwuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9wYWdlLXRpdGxlLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvc25hY2tiYXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9zdG9yZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL3p4Y3Zibi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3V0aWxzL2Jhbm5lZC1wYWdlLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvYmF0Y2guanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9maWxlLXNpemUuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9tb3VudC1jb21wb25lbnQuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9vcmRlcmVkLWxpc3QuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9yYW5kb20uanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9yb3V0ZWQtY29tcG9uZW50LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvdmFsaWRhdG9ycy5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtBQ0FBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0lDekZhLE1BQU0sV0FBTixNQUFNO0FBQ2pCLFdBRFcsTUFBTSxHQUNIOzBCQURILE1BQU07O0FBRWYsUUFBSSxDQUFDLGFBQWEsR0FBRyxFQUFFLENBQUM7QUFDeEIsUUFBSSxDQUFDLFFBQVEsR0FBRyxFQUFFLENB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QTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ3BCQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNUQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUM5QkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7O0FDekJBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7QUNuRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUMvRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7O0FDSkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7O0FDakxBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7O0FDdkNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNsU0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ3JEQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDZEE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7OztBQ1pBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7O0FDM0NBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtB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aUJBQWlCLENBQUMsUUFBUSxFQUFFO0FBQzFDLE1BQUksT0FBTyxHQUFHLFNBQVYsT0FBTyxDQUFZLFVBQVUsRUFBRTtBQUNqQyxXQUFPLFFBQVEsQ0FDYixpRUFBaUUsRUFDakUsa0VBQWtFLEVBQ2xFLFVBQVUsQ0FBQyxDQUFDO0dBQ2YsQ0FBQztBQUNGLFNBQU8sSUFBSSxDQUFDLFNBQVMsQ0FBQyxRQUFRLENBQUMsbUJBQW1CLEVBQUUsT0FBTyxDQUFDLENBQUM7Q0FDOUQiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiBlKHQsbixyKXtmdW5jdGlvbiBzKG8sdSl7aWYoIW5bb10pe2lmKCF0W29dKXt2YXIgYT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2lmKCF1JiZhKXJldHVybiBhKG8sITApO2lmKGkpcmV0dXJuIGkobywhMCk7dmFyIGY9bmV3IEVycm9yKFwiQ2Fubm90IGZpbmQgbW9kdWxlICdcIitvK1wiJ1wiKTt0aHJvdyBmLmNvZGU9XCJNT0RVTEVfTk9UX0ZPVU5EXCIsZn12YXIgbD1uW29dPXtleHBvcnRzOnt9fTt0W29dWzBdLmNhbGwobC5leHBvcnRzLGZ1bmN0aW9uKGUpe3ZhciBuPXRbb11bMV1bZV07cmV0dXJuIHMobj9uOmUpfSxsLGwuZXhwb3J0cyxlLHQsbixyKX1yZXR1cm4gbltvXS5leHBvcnRzfXZhciBpPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7Zm9yKHZhciBvPTA7bzxyLmxlbmd0aDtvKyspcyhyW29dKTtyZXR1cm4gc30pIiwiLy8gc2hpbSBmb3IgdXNpbmcgcHJvY2VzcyBpbiBicm93c2VyXG5cbnZhciBwcm9jZXNzID0gbW9kdWxlLmV4cG9ydHMgPSB7fTtcbnZhciBxdWV1ZSA9IFtdO1xudmFyIGRyYWluaW5nID0gZmFsc2U7XG52YXIgY3VycmVudFF1ZXVlO1xudmFyIHF1ZXVlSW5kZXggPSAtMTtcblxuZnVuY3Rpb24gY2xlYW5VcE5leHRUaWNrKCkge1xuICAgIGRyYWluaW5nID0gZmFsc2U7XG4gICAgaWYgKGN1cnJlbnRRdWV1ZS5sZW5ndGgpIHtcbiAgICAgICAgcXVldWUgPSBjdXJyZW50UXVldWUuY29uY2F0KHF1ZXVlKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICBxdWV1ZUluZGV4ID0gLTE7XG4gICAgfVxuICAgIGlmIChxdWV1ZS5sZW5ndGgpIHtcbiAgICAgICAgZHJhaW5RdWV1ZSgpO1xuICAgIH1cbn1cblxuZnVuY3Rpb24gZHJhaW5RdWV1ZSgpIHtcbiAgICBpZiAoZHJhaW5pbmcpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB2YXIgdGltZW91dCA9IHNldFRpbWVvdXQoY2xlYW5VcE5leHRUaWNrKTtcbiAgICBkcmFpbmluZyA9IHRydWU7XG5cbiAgICB2YXIgbGVuID0gcXVldWUubGVuZ3RoO1xuICAgIHdoaWxlKGxlbikge1xuICAgICAgICBjdXJyZW50UXVldWUgPSBxdWV1ZTtcbiAgICAgICAgcXVldWUgPSBbXTtcbiAgICAgICAgd2hpbGUgKCsrcXVldWVJbmRleCA8IGxlbikge1xuICAgICAgICAgICAgaWYgKGN1cnJlbnRRdWV1ZSkge1xuICAgICAgICAgICAgICAgIGN1cnJlbnRRdWV1ZVtxdWV1ZUluZGV4XS5ydW4oKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICBxdWV1ZUluZGV4ID0gLTE7XG4gICAgICAgIGxlbiA9IHF1ZXVlLmxlbmd0aDtcbiAgICB9XG4gICAgY3VycmVudFF1ZXVlID0gbnVsbDtcbiAgICBkcmFpbmluZyA9IGZhbHNlO1xuICAgIGNsZWFyVGltZW91dCh0aW1lb3V0KTtcbn1cblxucHJvY2Vzcy5uZXh0VGljayA9IGZ1bmN0aW9uIChmdW4pIHtcbiAgICB2YXIgYXJncyA9IG5ldyBBcnJheShhcmd1bWVudHMubGVuZ3RoIC0gMSk7XG4gICAgaWYgKGFyZ3VtZW50cy5sZW5ndGggPiAxKSB7XG4gICAgICAgIGZvciAodmFyIGkgPSAxOyBpIDwgYXJndW1lbnRzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBhcmdzW2kgLSAxXSA9IGFyZ3VtZW50c1tpXTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBxdWV1ZS5wdXNoKG5ldyBJdGVtKGZ1biwgYXJncykpO1xuICAgIGlmIChxdWV1ZS5sZW5ndGggPT09IDEgJiYgIWRyYWluaW5nKSB7XG4gICAgICAgIHNldFRpbWVvdXQoZHJhaW5RdWV1ZSwgMCk7XG4gICAgfVxufTtcblxuLy8gdjggbGlrZXMgcHJlZGljdGlibGUgb2JqZWN0c1xuZnVuY3Rpb24gSXRlbShmdW4sIGFycmF5KSB7XG4gICAgdGhpcy5mdW4gPSBmdW47XG4gICAgdGhpcy5hcnJheSA9IGFycmF5O1xufVxuSXRlbS5wcm90b3R5cGUucnVuID0gZnVuY3Rpb24gKCkge1xuICAgIHRoaXMuZnVuLmFwcGx5KG51bGwsIHRoaXMuYXJyYXkpO1xufTtcbnByb2Nlc3MudGl0bGUgPSAnYnJvd3Nlcic7XG5wcm9jZXNzLmJyb3dzZXIgPSB0cnVlO1xucHJvY2Vzcy5lbnYgPSB7fTtcbnByb2Nlc3MuYXJndiA9IFtdO1xucHJvY2Vzcy52ZXJzaW9uID0gJyc7IC8vIGVtcHR5IHN0cmluZyB0byBhdm9pZCByZWdleHAgaXNzdWVzXG5wcm9jZXNzLnZlcnNpb25zID0ge307XG5cbmZ1bmN0aW9uIG5vb3AoKSB7fVxuXG5wcm9jZXNzLm9uID0gbm9vcDtcbnByb2Nlc3MuYWRkTGlzdGVuZXIgPSBub29wO1xucHJvY2Vzcy5vbmNlID0gbm9vcDtcbnByb2Nlc3Mub2ZmID0gbm9vcDtcbnByb2Nlc3MucmVtb3ZlTGlzdGVuZXIgPSBub29wO1xucHJvY2Vzcy5yZW1vdmVBbGxMaXN0ZW5lcnMgPSBub29wO1xucHJvY2Vzcy5lbWl0ID0gbm9vcDtcblxucHJvY2Vzcy5iaW5kaW5nID0gZnVuY3Rpb24gKG5hbWUpIHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ3Byb2Nlc3MuYmluZGluZyBpcyBub3Qgc3VwcG9ydGVkJyk7XG59O1xuXG5wcm9jZXNzLmN3ZCA9IGZ1bmN0aW9uICgpIHsgcmV0dXJuICcvJyB9O1xucHJvY2Vzcy5jaGRpciA9IGZ1bmN0aW9uIChkaXIpIHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ3Byb2Nlc3MuY2hkaXIgaXMgbm90IHN1cHBvcnRlZCcpO1xufTtcbnByb2Nlc3MudW1hc2sgPSBmdW5jdGlvbigpIHsgcmV0dXJuIDA7IH07XG4iLCJpbXBvcnQgT3JkZXJlZExpc3QgZnJvbSAnbWlzYWdvL3V0aWxzL29yZGVyZWQtbGlzdCc7XG5cbmV4cG9ydCBjbGFzcyBNaXNhZ28ge1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICB0aGlzLl9pbml0aWFsaXplcnMgPSBbXTtcbiAgICB0aGlzLl9jb250ZXh0ID0ge307XG4gIH1cblxuICBhZGRJbml0aWFsaXplcihpbml0aWFsaXplcikge1xuICAgIHRoaXMuX2luaXRpYWxpemVycy5wdXNoKHtcbiAgICAgIGtleTogaW5pdGlhbGl6ZXIubmFtZSxcblxuICAgICAgaXRlbTogaW5pdGlhbGl6ZXIuaW5pdGlhbGl6ZXIsXG5cbiAgICAgIGFmdGVyOiBpbml0aWFsaXplci5hZnRlcixcbiAgICAgIGJlZm9yZTogaW5pdGlhbGl6ZXIuYmVmb3JlXG4gICAgfSk7XG4gIH1cblxuICBpbml0KGNvbnRleHQpIHtcbiAgICB0aGlzLl9jb250ZXh0ID0gY29udGV4dDtcblxuICAgIHZhciBpbml0T3JkZXIgPSBuZXcgT3JkZXJlZExpc3QodGhpcy5faW5pdGlhbGl6ZXJzKS5vcmRlcmVkVmFsdWVzKCk7XG4gICAgaW5pdE9yZGVyLmZvckVhY2goaW5pdGlhbGl6ZXIgPT4ge1xuICAgICAgaW5pdGlhbGl6ZXIodGhpcyk7XG4gICAgfSk7XG4gIH1cblxuICAvLyBjb250ZXh0IGFjY2Vzc29yc1xuICBoYXMoa2V5KSB7XG4gICAgcmV0dXJuICEhdGhpcy5fY29udGV4dFtrZXldO1xuICB9XG5cbiAgZ2V0KGtleSwgZmFsbGJhY2spIHtcbiAgICBpZiAodGhpcy5oYXMoa2V5KSkge1xuICAgICAgcmV0dXJuIHRoaXMuX2NvbnRleHRba2V5XTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIGZhbGxiYWNrIHx8IHVuZGVmaW5lZDtcbiAgICB9XG4gIH1cblxuICBwb3Aoa2V5KSB7XG4gICAgaWYgKHRoaXMuaGFzKGtleSkpIHtcbiAgICAgIGxldCB2YWx1ZSA9IHRoaXMuX2NvbnRleHRba2V5XTtcbiAgICAgIHRoaXMuX2NvbnRleHRba2V5XSA9IG51bGw7XG4gICAgICByZXR1cm4gdmFsdWU7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB1bmRlZmluZWQ7XG4gICAgfVxuICB9XG59XG5cbi8vIGNyZWF0ZSAgc2luZ2xldG9uXG52YXIgbWlzYWdvID0gbmV3IE1pc2FnbygpO1xuXG4vLyBleHBvc2UgaXQgZ2xvYmFsbHlcbmdsb2JhbC5taXNhZ28gPSBtaXNhZ287XG5cbi8vIGFuZCBleHBvcnQgaXQgZm9yIHRlc3RzIGFuZCBzdHVmZlxuZXhwb3J0IGRlZmF1bHQgbWlzYWdvO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgYWpheC5pbml0KG1pc2Fnby5nZXQoJ0NTUkZfQ09PS0lFX05BTUUnKSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdhamF4JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCB7IGNvbm5lY3QgfSBmcm9tICdyZWFjdC1yZWR1eCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgQXV0aE1lc3NhZ2UsIHsgc2VsZWN0IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYXV0aC1tZXNzYWdlJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIG1vdW50KGNvbm5lY3Qoc2VsZWN0KShBdXRoTWVzc2FnZSksICdhdXRoLW1lc3NhZ2UtbW91bnQnKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NvbXBvbmVudDphdXRoLW1lc3NhZ2UnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCByZWR1Y2VyLCB7IGluaXRpYWxTdGF0ZSB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9hdXRoJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcihjb250ZXh0KSB7XG4gIHN0b3JlLmFkZFJlZHVjZXIoJ2F1dGgnLCByZWR1Y2VyLCBPYmplY3QuYXNzaWduKHtcbiAgICAnaXNBdXRoZW50aWNhdGVkJzogY29udGV4dC5nZXQoJ2lzQXV0aGVudGljYXRlZCcpLFxuICAgICdpc0Fub255bW91cyc6ICFjb250ZXh0LmdldCgnaXNBdXRoZW50aWNhdGVkJyksXG5cbiAgICAndXNlcic6IGNvbnRleHQuZ2V0KCd1c2VyJylcbiAgfSwgaW5pdGlhbFN0YXRlKSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOmF1dGgnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgYXV0aCBmcm9tICdtaXNhZ28vc2VydmljZXMvYXV0aCc7XG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuaW1wb3J0IHN0b3JhZ2UgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2xvY2FsLXN0b3JhZ2UnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgYXV0aC5pbml0KHN0b3JlLCBzdG9yYWdlLCBtb2RhbCk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdhdXRoJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7IiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHNob3dCYW5uZWRQYWdlIGZyb20gJ21pc2Fnby91dGlscy9iYW5uZWQtcGFnZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKGNvbnRleHQpIHtcbiAgaWYgKGNvbnRleHQuaGFzKCdCQU5fTUVTU0FHRScpKSB7XG4gICAgc2hvd0Jhbm5lZFBhZ2UoY29udGV4dC5nZXQoJ0JBTl9NRVNTQUdFJyksIGZhbHNlKTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OmJhbmVkLXBhZ2UnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBjYXB0Y2hhIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9jYXB0Y2hhJztcbmltcG9ydCBpbmNsdWRlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9pbmNsdWRlJztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcihjb250ZXh0KSB7XG4gIGNhcHRjaGEuaW5pdChjb250ZXh0LCBhamF4LCBpbmNsdWRlLCBzbmFja2Jhcik7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjYXB0Y2hhJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBpbmNsdWRlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9pbmNsdWRlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoY29udGV4dCkge1xuICBpbmNsdWRlLmluaXQoY29udGV4dC5nZXQoJ1NUQVRJQ19VUkwnKSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdpbmNsdWRlJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBzdG9yYWdlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9sb2NhbC1zdG9yYWdlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHN0b3JhZ2UuaW5pdCgnbWlzYWdvXycpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnbG9jYWwtc3RvcmFnZScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplclxufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgZHJvcGRvd24gZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vYmlsZS1uYXZiYXItZHJvcGRvd24nO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbGV0IGVsZW1lbnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnbW9iaWxlLW5hdmJhci1kcm9wZG93bi1tb3VudCcpO1xuICBpZiAoZWxlbWVudCkge1xuICAgIGRyb3Bkb3duLmluaXQoZWxlbWVudCk7XG4gIH1cbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2Ryb3Bkb3duJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IG1vZGFsIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2RhbCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBsZXQgZWxlbWVudCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdtb2RhbC1tb3VudCcpO1xuICBpZiAoZWxlbWVudCkge1xuICAgIG1vZGFsLmluaXQoZWxlbWVudCk7XG4gIH1cbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ21vZGFsJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbW9tZW50LmxvY2FsZSgkKCdodG1sJykuYXR0cignbGFuZycpKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ21vbWVudCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplclxufSk7XG4iLCJpbXBvcnQgT3B0aW9ucywgeyBwYXRocyB9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL29wdGlvbnMvcm9vdCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvcm91dGVkLWNvbXBvbmVudCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKGNvbnRleHQpIHtcbiAgaWYgKGNvbnRleHQuaGFzKCdVU0VSX09QVElPTlMnKSkge1xuICAgIG1vdW50KHtcbiAgICAgIHJvb3Q6IG1pc2Fnby5nZXQoJ1VTRVJDUF9VUkwnKSxcbiAgICAgIGNvbXBvbmVudDogT3B0aW9ucyxcbiAgICAgIHBhdGhzOiBwYXRocyhzdG9yZSlcbiAgICB9KTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50Om9wdGlvbnMnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCB0aXRsZSBmcm9tICdtaXNhZ28vc2VydmljZXMvcGFnZS10aXRsZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKGNvbnRleHQpIHtcbiAgdGl0bGUuaW5pdChjb250ZXh0LmdldCgnU0VUVElOR1MnKS5mb3J1bV9uYW1lKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3BhZ2UtdGl0bGUnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXJcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IFJlcXVlc3RBY3RpdmF0aW9uTGluayBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9yZXF1ZXN0LWFjdGl2YXRpb24tbGluayc7XG5pbXBvcnQgbW91bnQgZnJvbSAnbWlzYWdvL3V0aWxzL21vdW50LWNvbXBvbmVudCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBpZiAoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rLW1vdW50JykpIHtcbiAgICBtb3VudChSZXF1ZXN0QWN0aXZhdGlvbkxpbmssICdyZXF1ZXN0LWFjdGl2YXRpb24tbGluay1tb3VudCcsIGZhbHNlKTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OnJlcXVlc3QtYWN0aXZhdGlvbi1saW5rJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgUmVxdWVzdFBhc3N3b3JkUmVzZXQgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvcmVxdWVzdC1wYXNzd29yZC1yZXNldCc7XG5pbXBvcnQgbW91bnQgZnJvbSAnbWlzYWdvL3V0aWxzL21vdW50LWNvbXBvbmVudCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBpZiAoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlcXVlc3QtcGFzc3dvcmQtcmVzZXQtbW91bnQnKSkge1xuICAgIG1vdW50KFJlcXVlc3RQYXNzd29yZFJlc2V0LCAncmVxdWVzdC1wYXNzd29yZC1yZXNldC1tb3VudCcsIGZhbHNlKTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OnJlcXVlc3QtcGFzc3dvcmQtcmVzZXQnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBSZXNldFBhc3N3b3JkRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9yZXNldC1wYXNzd29yZC1mb3JtJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGlmIChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVzZXQtcGFzc3dvcmQtZm9ybS1tb3VudCcpKSB7XG4gICAgbW91bnQoUmVzZXRQYXNzd29yZEZvcm0sICdyZXNldC1wYXNzd29yZC1mb3JtLW1vdW50JywgZmFsc2UpO1xuICB9XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6cmVzZXQtcGFzc3dvcmQtZm9ybScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCB7IFNuYWNrYmFyLCBzZWxlY3QgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9zbmFja2Jhcic7XG5pbXBvcnQgbW91bnQgZnJvbSAnbWlzYWdvL3V0aWxzL21vdW50LWNvbXBvbmVudCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBtb3VudChjb25uZWN0KHNlbGVjdCkoU25hY2tiYXIpLCAnc25hY2tiYXItbW91bnQnKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NvbXBvbmVudDpzbmFja2JhcicsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzbmFja2Jhcidcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHJlZHVjZXIsIHsgaW5pdGlhbFN0YXRlIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3NuYWNrYmFyJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc3RvcmUuYWRkUmVkdWNlcignc25hY2tiYXInLCByZWR1Y2VyLCBpbml0aWFsU3RhdGUpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAncmVkdWNlcjpzbmFja2JhcicsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYmVmb3JlOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBzbmFja2Jhci5pbml0KHN0b3JlKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3NuYWNrYmFyJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHN0b3JlLmluaXQoKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3N0b3JlJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdfZW5kJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgcmVkdWNlciwgeyBpbml0aWFsU3RhdGUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdGljayc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHN0b3JlLmFkZFJlZHVjZXIoJ3RpY2snLCByZWR1Y2VyLCBpbml0aWFsU3RhdGUpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAncmVkdWNlcjp0aWNrJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHsgZG9UaWNrIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3RpY2snO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmNvbnN0IFRJQ0tfUEVSSU9EID0gNTAgKiAxMDAwOyAvL2RvIHRoZSB0aWNrIGV2ZXJ5IDUwc1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgd2luZG93LnNldEludGVydmFsKGZ1bmN0aW9uKCkge1xuICAgIHN0b3JlLmRpc3BhdGNoKGRvVGljaygpKTtcbiAgfSwgVElDS19QRVJJT0QpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAndGljay1zdGFydCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCB7IFVzZXJNZW51LCBDb21wYWN0VXNlck1lbnUsIHNlbGVjdCB9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3VzZXItbWVudS9yb290JztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIG1vdW50KGNvbm5lY3Qoc2VsZWN0KShVc2VyTWVudSksICd1c2VyLW1lbnUtbW91bnQnKTtcbiAgbW91bnQoY29ubmVjdChzZWxlY3QpKENvbXBhY3RVc2VyTWVudSksICd1c2VyLW1lbnUtY29tcGFjdC1tb3VudCcpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OnVzZXItbWVudScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHJlZHVjZXIgZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3VzZXJuYW1lLWhpc3RvcnknO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBzdG9yZS5hZGRSZWR1Y2VyKCd1c2VybmFtZS1oaXN0b3J5JywgcmVkdWNlciwgW10pO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAncmVkdWNlcjp1c2VybmFtZS1oaXN0b3J5JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IFVzZXJzLCB7IHBhdGhzIH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvdXNlcnMvcm9vdCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvcm91dGVkLWNvbXBvbmVudCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKGNvbnRleHQpIHtcbiAgaWYgKGNvbnRleHQuaGFzKCdVU0VSU19MSVNUUycpKSB7XG4gICAgbW91bnQoe1xuICAgICAgcm9vdDogbWlzYWdvLmdldCgnVVNFUlNfTElTVF9VUkwnKSxcbiAgICAgIGNvbXBvbmVudDogVXNlcnMsXG4gICAgICBwYXRoczogcGF0aHMoc3RvcmUpXG4gICAgfSk7XG4gIH1cbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NvbXBvbmVudDp1c2VycycsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHJlZHVjZXIgZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3VzZXJzJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc3RvcmUuYWRkUmVkdWNlcigndXNlcnMnLCByZWR1Y2VyLCBbXSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOnVzZXJzJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGluY2x1ZGUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2luY2x1ZGUnO1xuaW1wb3J0IHp4Y3ZibiBmcm9tICdtaXNhZ28vc2VydmljZXMvenhjdmJuJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHp4Y3Zibi5pbml0KGluY2x1ZGUpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnenhjdmJuJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsInZhciBwU2xpY2UgPSBBcnJheS5wcm90b3R5cGUuc2xpY2U7XG52YXIgb2JqZWN0S2V5cyA9IHJlcXVpcmUoJy4vbGliL2tleXMuanMnKTtcbnZhciBpc0FyZ3VtZW50cyA9IHJlcXVpcmUoJy4vbGliL2lzX2FyZ3VtZW50cy5qcycpO1xuXG52YXIgZGVlcEVxdWFsID0gbW9kdWxlLmV4cG9ydHMgPSBmdW5jdGlvbiAoYWN0dWFsLCBleHBlY3RlZCwgb3B0cykge1xuICBpZiAoIW9wdHMpIG9wdHMgPSB7fTtcbiAgLy8gNy4xLiBBbGwgaWRlbnRpY2FsIHZhbHVlcyBhcmUgZXF1aXZhbGVudCwgYXMgZGV0ZXJtaW5lZCBieSA9PT0uXG4gIGlmIChhY3R1YWwgPT09IGV4cGVjdGVkKSB7XG4gICAgcmV0dXJuIHRydWU7XG5cbiAgfSBlbHNlIGlmIChhY3R1YWwgaW5zdGFuY2VvZiBEYXRlICYmIGV4cGVjdGVkIGluc3RhbmNlb2YgRGF0ZSkge1xuICAgIHJldHVybiBhY3R1YWwuZ2V0VGltZSgpID09PSBleHBlY3RlZC5nZXRUaW1lKCk7XG5cbiAgLy8gNy4zLiBPdGhlciBwYWlycyB0aGF0IGRvIG5vdCBib3RoIHBhc3MgdHlwZW9mIHZhbHVlID09ICdvYmplY3QnLFxuICAvLyBlcXVpdmFsZW5jZSBpcyBkZXRlcm1pbmVkIGJ5ID09LlxuICB9IGVsc2UgaWYgKCFhY3R1YWwgfHwgIWV4cGVjdGVkIHx8IHR5cGVvZiBhY3R1YWwgIT0gJ29iamVjdCcgJiYgdHlwZW9mIGV4cGVjdGVkICE9ICdvYmplY3QnKSB7XG4gICAgcmV0dXJuIG9wdHMuc3RyaWN0ID8gYWN0dWFsID09PSBleHBlY3RlZCA6IGFjdHVhbCA9PSBleHBlY3RlZDtcblxuICAvLyA3LjQuIEZvciBhbGwgb3RoZXIgT2JqZWN0IHBhaXJzLCBpbmNsdWRpbmcgQXJyYXkgb2JqZWN0cywgZXF1aXZhbGVuY2UgaXNcbiAgLy8gZGV0ZXJtaW5lZCBieSBoYXZpbmcgdGhlIHNhbWUgbnVtYmVyIG9mIG93bmVkIHByb3BlcnRpZXMgKGFzIHZlcmlmaWVkXG4gIC8vIHdpdGggT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKSwgdGhlIHNhbWUgc2V0IG9mIGtleXNcbiAgLy8gKGFsdGhvdWdoIG5vdCBuZWNlc3NhcmlseSB0aGUgc2FtZSBvcmRlciksIGVxdWl2YWxlbnQgdmFsdWVzIGZvciBldmVyeVxuICAvLyBjb3JyZXNwb25kaW5nIGtleSwgYW5kIGFuIGlkZW50aWNhbCAncHJvdG90eXBlJyBwcm9wZXJ0eS4gTm90ZTogdGhpc1xuICAvLyBhY2NvdW50cyBmb3IgYm90aCBuYW1lZCBhbmQgaW5kZXhlZCBwcm9wZXJ0aWVzIG9uIEFycmF5cy5cbiAgfSBlbHNlIHtcbiAgICByZXR1cm4gb2JqRXF1aXYoYWN0dWFsLCBleHBlY3RlZCwgb3B0cyk7XG4gIH1cbn1cblxuZnVuY3Rpb24gaXNVbmRlZmluZWRPck51bGwodmFsdWUpIHtcbiAgcmV0dXJuIHZhbHVlID09PSBudWxsIHx8IHZhbHVlID09PSB1bmRlZmluZWQ7XG59XG5cbmZ1bmN0aW9uIGlzQnVmZmVyICh4KSB7XG4gIGlmICgheCB8fCB0eXBlb2YgeCAhPT0gJ29iamVjdCcgfHwgdHlwZW9mIHgubGVuZ3RoICE9PSAnbnVtYmVyJykgcmV0dXJuIGZhbHNlO1xuICBpZiAodHlwZW9mIHguY29weSAhPT0gJ2Z1bmN0aW9uJyB8fCB0eXBlb2YgeC5zbGljZSAhPT0gJ2Z1bmN0aW9uJykge1xuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuICBpZiAoeC5sZW5ndGggPiAwICYmIHR5cGVvZiB4WzBdICE9PSAnbnVtYmVyJykgcmV0dXJuIGZhbHNlO1xuICByZXR1cm4gdHJ1ZTtcbn1cblxuZnVuY3Rpb24gb2JqRXF1aXYoYSwgYiwgb3B0cykge1xuICB2YXIgaSwga2V5O1xuICBpZiAoaXNVbmRlZmluZWRPck51bGwoYSkgfHwgaXNVbmRlZmluZWRPck51bGwoYikpXG4gICAgcmV0dXJuIGZhbHNlO1xuICAvLyBhbiBpZGVudGljYWwgJ3Byb3RvdHlwZScgcHJvcGVydHkuXG4gIGlmIChhLnByb3RvdHlwZSAhPT0gYi5wcm90b3R5cGUpIHJldHVybiBmYWxzZTtcbiAgLy9+fn5JJ3ZlIG1hbmFnZWQgdG8gYnJlYWsgT2JqZWN0LmtleXMgdGhyb3VnaCBzY3Jld3kgYXJndW1lbnRzIHBhc3NpbmcuXG4gIC8vICAgQ29udmVydGluZyB0byBhcnJheSBzb2x2ZXMgdGhlIHByb2JsZW0uXG4gIGlmIChpc0FyZ3VtZW50cyhhKSkge1xuICAgIGlmICghaXNBcmd1bWVudHMoYikpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gICAgYSA9IHBTbGljZS5jYWxsKGEpO1xuICAgIGIgPSBwU2xpY2UuY2FsbChiKTtcbiAgICByZXR1cm4gZGVlcEVxdWFsKGEsIGIsIG9wdHMpO1xuICB9XG4gIGlmIChpc0J1ZmZlcihhKSkge1xuICAgIGlmICghaXNCdWZmZXIoYikpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gICAgaWYgKGEubGVuZ3RoICE9PSBiLmxlbmd0aCkgcmV0dXJuIGZhbHNlO1xuICAgIGZvciAoaSA9IDA7IGkgPCBhLmxlbmd0aDsgaSsrKSB7XG4gICAgICBpZiAoYVtpXSAhPT0gYltpXSkgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuICB0cnkge1xuICAgIHZhciBrYSA9IG9iamVjdEtleXMoYSksXG4gICAgICAgIGtiID0gb2JqZWN0S2V5cyhiKTtcbiAgfSBjYXRjaCAoZSkgey8vaGFwcGVucyB3aGVuIG9uZSBpcyBhIHN0cmluZyBsaXRlcmFsIGFuZCB0aGUgb3RoZXIgaXNuJ3RcbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cbiAgLy8gaGF2aW5nIHRoZSBzYW1lIG51bWJlciBvZiBvd25lZCBwcm9wZXJ0aWVzIChrZXlzIGluY29ycG9yYXRlc1xuICAvLyBoYXNPd25Qcm9wZXJ0eSlcbiAgaWYgKGthLmxlbmd0aCAhPSBrYi5sZW5ndGgpXG4gICAgcmV0dXJuIGZhbHNlO1xuICAvL3RoZSBzYW1lIHNldCBvZiBrZXlzIChhbHRob3VnaCBub3QgbmVjZXNzYXJpbHkgdGhlIHNhbWUgb3JkZXIpLFxuICBrYS5zb3J0KCk7XG4gIGtiLnNvcnQoKTtcbiAgLy9+fn5jaGVhcCBrZXkgdGVzdFxuICBmb3IgKGkgPSBrYS5sZW5ndGggLSAxOyBpID49IDA7IGktLSkge1xuICAgIGlmIChrYVtpXSAhPSBrYltpXSlcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgfVxuICAvL2VxdWl2YWxlbnQgdmFsdWVzIGZvciBldmVyeSBjb3JyZXNwb25kaW5nIGtleSwgYW5kXG4gIC8vfn5+cG9zc2libHkgZXhwZW5zaXZlIGRlZXAgdGVzdFxuICBmb3IgKGkgPSBrYS5sZW5ndGggLSAxOyBpID49IDA7IGktLSkge1xuICAgIGtleSA9IGthW2ldO1xuICAgIGlmICghZGVlcEVxdWFsKGFba2V5XSwgYltrZXldLCBvcHRzKSkgcmV0dXJuIGZhbHNlO1xuICB9XG4gIHJldHVybiB0eXBlb2YgYSA9PT0gdHlwZW9mIGI7XG59XG4iLCJ2YXIgc3VwcG9ydHNBcmd1bWVudHNDbGFzcyA9IChmdW5jdGlvbigpe1xuICByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS50b1N0cmluZy5jYWxsKGFyZ3VtZW50cylcbn0pKCkgPT0gJ1tvYmplY3QgQXJndW1lbnRzXSc7XG5cbmV4cG9ydHMgPSBtb2R1bGUuZXhwb3J0cyA9IHN1cHBvcnRzQXJndW1lbnRzQ2xhc3MgPyBzdXBwb3J0ZWQgOiB1bnN1cHBvcnRlZDtcblxuZXhwb3J0cy5zdXBwb3J0ZWQgPSBzdXBwb3J0ZWQ7XG5mdW5jdGlvbiBzdXBwb3J0ZWQob2JqZWN0KSB7XG4gIHJldHVybiBPYmplY3QucHJvdG90eXBlLnRvU3RyaW5nLmNhbGwob2JqZWN0KSA9PSAnW29iamVjdCBBcmd1bWVudHNdJztcbn07XG5cbmV4cG9ydHMudW5zdXBwb3J0ZWQgPSB1bnN1cHBvcnRlZDtcbmZ1bmN0aW9uIHVuc3VwcG9ydGVkKG9iamVjdCl7XG4gIHJldHVybiBvYmplY3QgJiZcbiAgICB0eXBlb2Ygb2JqZWN0ID09ICdvYmplY3QnICYmXG4gICAgdHlwZW9mIG9iamVjdC5sZW5ndGggPT0gJ251bWJlcicgJiZcbiAgICBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwob2JqZWN0LCAnY2FsbGVlJykgJiZcbiAgICAhT2JqZWN0LnByb3RvdHlwZS5wcm9wZXJ0eUlzRW51bWVyYWJsZS5jYWxsKG9iamVjdCwgJ2NhbGxlZScpIHx8XG4gICAgZmFsc2U7XG59O1xuIiwiZXhwb3J0cyA9IG1vZHVsZS5leHBvcnRzID0gdHlwZW9mIE9iamVjdC5rZXlzID09PSAnZnVuY3Rpb24nXG4gID8gT2JqZWN0LmtleXMgOiBzaGltO1xuXG5leHBvcnRzLnNoaW0gPSBzaGltO1xuZnVuY3Rpb24gc2hpbSAob2JqKSB7XG4gIHZhciBrZXlzID0gW107XG4gIGZvciAodmFyIGtleSBpbiBvYmopIGtleXMucHVzaChrZXkpO1xuICByZXR1cm4ga2V5cztcbn1cbiIsIi8qKlxuICogSW5kaWNhdGVzIHRoYXQgbmF2aWdhdGlvbiB3YXMgY2F1c2VkIGJ5IGEgY2FsbCB0byBoaXN0b3J5LnB1c2guXG4gKi9cbid1c2Ugc3RyaWN0JztcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcbnZhciBQVVNIID0gJ1BVU0gnO1xuXG5leHBvcnRzLlBVU0ggPSBQVVNIO1xuLyoqXG4gKiBJbmRpY2F0ZXMgdGhhdCBuYXZpZ2F0aW9uIHdhcyBjYXVzZWQgYnkgYSBjYWxsIHRvIGhpc3RvcnkucmVwbGFjZS5cbiAqL1xudmFyIFJFUExBQ0UgPSAnUkVQTEFDRSc7XG5cbmV4cG9ydHMuUkVQTEFDRSA9IFJFUExBQ0U7XG4vKipcbiAqIEluZGljYXRlcyB0aGF0IG5hdmlnYXRpb24gd2FzIGNhdXNlZCBieSBzb21lIG90aGVyIGFjdGlvbiBzdWNoXG4gKiBhcyB1c2luZyBhIGJyb3dzZXIncyBiYWNrL2ZvcndhcmQgYnV0dG9ucyBhbmQvb3IgbWFudWFsbHkgbWFuaXB1bGF0aW5nXG4gKiB0aGUgVVJMIGluIGEgYnJvd3NlcidzIGxvY2F0aW9uIGJhci4gVGhpcyBpcyB0aGUgZGVmYXVsdC5cbiAqXG4gKiBTZWUgaHR0cHM6Ly9kZXZlbG9wZXIubW96aWxsYS5vcmcvZW4tVVMvZG9jcy9XZWIvQVBJL1dpbmRvd0V2ZW50SGFuZGxlcnMvb25wb3BzdGF0ZVxuICogZm9yIG1vcmUgaW5mb3JtYXRpb24uXG4gKi9cbnZhciBQT1AgPSAnUE9QJztcblxuZXhwb3J0cy5QT1AgPSBQT1A7XG5leHBvcnRzWydkZWZhdWx0J10gPSB7XG4gIFBVU0g6IFBVU0gsXG4gIFJFUExBQ0U6IFJFUExBQ0UsXG4gIFBPUDogUE9QXG59OyIsIlwidXNlIHN0cmljdFwiO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuZXhwb3J0cy5sb29wQXN5bmMgPSBsb29wQXN5bmM7XG5cbmZ1bmN0aW9uIGxvb3BBc3luYyh0dXJucywgd29yaywgY2FsbGJhY2spIHtcbiAgdmFyIGN1cnJlbnRUdXJuID0gMDtcbiAgdmFyIGlzRG9uZSA9IGZhbHNlO1xuXG4gIGZ1bmN0aW9uIGRvbmUoKSB7XG4gICAgaXNEb25lID0gdHJ1ZTtcbiAgICBjYWxsYmFjay5hcHBseSh0aGlzLCBhcmd1bWVudHMpO1xuICB9XG5cbiAgZnVuY3Rpb24gbmV4dCgpIHtcbiAgICBpZiAoaXNEb25lKSByZXR1cm47XG5cbiAgICBpZiAoY3VycmVudFR1cm4gPCB0dXJucykge1xuICAgICAgd29yay5jYWxsKHRoaXMsIGN1cnJlbnRUdXJuKyssIG5leHQsIGRvbmUpO1xuICAgIH0gZWxzZSB7XG4gICAgICBkb25lLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XG4gICAgfVxuICB9XG5cbiAgbmV4dCgpO1xufSIsIi8qZXNsaW50LWRpc2FibGUgbm8tZW1wdHkgKi9cbid1c2Ugc3RyaWN0JztcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcbmV4cG9ydHMuc2F2ZVN0YXRlID0gc2F2ZVN0YXRlO1xuZXhwb3J0cy5yZWFkU3RhdGUgPSByZWFkU3RhdGU7XG5cbmZ1bmN0aW9uIF9pbnRlcm9wUmVxdWlyZURlZmF1bHQob2JqKSB7IHJldHVybiBvYmogJiYgb2JqLl9fZXNNb2R1bGUgPyBvYmogOiB7ICdkZWZhdWx0Jzogb2JqIH07IH1cblxudmFyIF93YXJuaW5nID0gcmVxdWlyZSgnd2FybmluZycpO1xuXG52YXIgX3dhcm5pbmcyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfd2FybmluZyk7XG5cbnZhciBLZXlQcmVmaXggPSAnQEBIaXN0b3J5Lyc7XG52YXIgUXVvdGFFeGNlZWRlZEVycm9yID0gJ1F1b3RhRXhjZWVkZWRFcnJvcic7XG52YXIgU2VjdXJpdHlFcnJvciA9ICdTZWN1cml0eUVycm9yJztcblxuZnVuY3Rpb24gY3JlYXRlS2V5KGtleSkge1xuICByZXR1cm4gS2V5UHJlZml4ICsga2V5O1xufVxuXG5mdW5jdGlvbiBzYXZlU3RhdGUoa2V5LCBzdGF0ZSkge1xuICB0cnkge1xuICAgIHdpbmRvdy5zZXNzaW9uU3RvcmFnZS5zZXRJdGVtKGNyZWF0ZUtleShrZXkpLCBKU09OLnN0cmluZ2lmeShzdGF0ZSkpO1xuICB9IGNhdGNoIChlcnJvcikge1xuICAgIGlmIChlcnJvci5uYW1lID09PSBTZWN1cml0eUVycm9yKSB7XG4gICAgICAvLyBCbG9ja2luZyBjb29raWVzIGluIENocm9tZS9GaXJlZm94L1NhZmFyaSB0aHJvd3MgU2VjdXJpdHlFcnJvciBvbiBhbnlcbiAgICAgIC8vIGF0dGVtcHQgdG8gYWNjZXNzIHdpbmRvdy5zZXNzaW9uU3RvcmFnZS5cbiAgICAgIHByb2Nlc3MuZW52Lk5PREVfRU5WICE9PSAncHJvZHVjdGlvbicgPyBfd2FybmluZzJbJ2RlZmF1bHQnXShmYWxzZSwgJ1toaXN0b3J5XSBVbmFibGUgdG8gc2F2ZSBzdGF0ZTsgc2Vzc2lvblN0b3JhZ2UgaXMgbm90IGF2YWlsYWJsZSBkdWUgdG8gc2VjdXJpdHkgc2V0dGluZ3MnKSA6IHVuZGVmaW5lZDtcblxuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGlmIChlcnJvci5uYW1lID09PSBRdW90YUV4Y2VlZGVkRXJyb3IgJiYgd2luZG93LnNlc3Npb25TdG9yYWdlLmxlbmd0aCA9PT0gMCkge1xuICAgICAgLy8gU2FmYXJpIFwicHJpdmF0ZSBtb2RlXCIgdGhyb3dzIFF1b3RhRXhjZWVkZWRFcnJvci5cbiAgICAgIHByb2Nlc3MuZW52Lk5PREVfRU5WICE9PSAncHJvZHVjdGlvbicgPyBfd2FybmluZzJbJ2RlZmF1bHQnXShmYWxzZSwgJ1toaXN0b3J5XSBVbmFibGUgdG8gc2F2ZSBzdGF0ZTsgc2Vzc2lvblN0b3JhZ2UgaXMgbm90IGF2YWlsYWJsZSBpbiBTYWZhcmkgcHJpdmF0ZSBtb2RlJykgOiB1bmRlZmluZWQ7XG5cbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aHJvdyBlcnJvcjtcbiAgfVxufVxuXG5mdW5jdGlvbiByZWFkU3RhdGUoa2V5KSB7XG4gIHZhciBqc29uID0gdW5kZWZpbmVkO1xuICB0cnkge1xuICAgIGpzb24gPSB3aW5kb3cuc2Vzc2lvblN0b3JhZ2UuZ2V0SXRlbShjcmVhdGVLZXkoa2V5KSk7XG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgaWYgKGVycm9yLm5hbWUgPT09IFNlY3VyaXR5RXJyb3IpIHtcbiAgICAgIC8vIEJsb2NraW5nIGNvb2tpZXMgaW4gQ2hyb21lL0ZpcmVmb3gvU2FmYXJpIHRocm93cyBTZWN1cml0eUVycm9yIG9uIGFueVxuICAgICAgLy8gYXR0ZW1wdCB0byBhY2Nlc3Mgd2luZG93LnNlc3Npb25TdG9yYWdlLlxuICAgICAgcHJvY2Vzcy5lbnYuTk9ERV9FTlYgIT09ICdwcm9kdWN0aW9uJyA/IF93YXJuaW5nMlsnZGVmYXVsdCddKGZhbHNlLCAnW2hpc3RvcnldIFVuYWJsZSB0byByZWFkIHN0YXRlOyBzZXNzaW9uU3RvcmFnZSBpcyBub3QgYXZhaWxhYmxlIGR1ZSB0byBzZWN1cml0eSBzZXR0aW5ncycpIDogdW5kZWZpbmVkO1xuXG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICBpZiAoanNvbikge1xuICAgIHRyeSB7XG4gICAgICByZXR1cm4gSlNPTi5wYXJzZShqc29uKTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgLy8gSWdub3JlIGludmFsaWQgSlNPTi5cbiAgICB9XG4gIH1cblxuICByZXR1cm4gbnVsbDtcbn0iLCIndXNlIHN0cmljdCc7XG5cbmV4cG9ydHMuX19lc01vZHVsZSA9IHRydWU7XG5leHBvcnRzLmFkZEV2ZW50TGlzdGVuZXIgPSBhZGRFdmVudExpc3RlbmVyO1xuZXhwb3J0cy5yZW1vdmVFdmVudExpc3RlbmVyID0gcmVtb3ZlRXZlbnRMaXN0ZW5lcjtcbmV4cG9ydHMuZ2V0SGFzaFBhdGggPSBnZXRIYXNoUGF0aDtcbmV4cG9ydHMucmVwbGFjZUhhc2hQYXRoID0gcmVwbGFjZUhhc2hQYXRoO1xuZXhwb3J0cy5nZXRXaW5kb3dQYXRoID0gZ2V0V2luZG93UGF0aDtcbmV4cG9ydHMuZ28gPSBnbztcbmV4cG9ydHMuZ2V0VXNlckNvbmZpcm1hdGlvbiA9IGdldFVzZXJDb25maXJtYXRpb247XG5leHBvcnRzLnN1cHBvcnRzSGlzdG9yeSA9IHN1cHBvcnRzSGlzdG9yeTtcbmV4cG9ydHMuc3VwcG9ydHNHb1dpdGhvdXRSZWxvYWRVc2luZ0hhc2ggPSBzdXBwb3J0c0dvV2l0aG91dFJlbG9hZFVzaW5nSGFzaDtcblxuZnVuY3Rpb24gYWRkRXZlbnRMaXN0ZW5lcihub2RlLCBldmVudCwgbGlzdGVuZXIpIHtcbiAgaWYgKG5vZGUuYWRkRXZlbnRMaXN0ZW5lcikge1xuICAgIG5vZGUuYWRkRXZlbnRMaXN0ZW5lcihldmVudCwgbGlzdGVuZXIsIGZhbHNlKTtcbiAgfSBlbHNlIHtcbiAgICBub2RlLmF0dGFjaEV2ZW50KCdvbicgKyBldmVudCwgbGlzdGVuZXIpO1xuICB9XG59XG5cbmZ1bmN0aW9uIHJlbW92ZUV2ZW50TGlzdGVuZXIobm9kZSwgZXZlbnQsIGxpc3RlbmVyKSB7XG4gIGlmIChub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIpIHtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoZXZlbnQsIGxpc3RlbmVyLCBmYWxzZSk7XG4gIH0gZWxzZSB7XG4gICAgbm9kZS5kZXRhY2hFdmVudCgnb24nICsgZXZlbnQsIGxpc3RlbmVyKTtcbiAgfVxufVxuXG5mdW5jdGlvbiBnZXRIYXNoUGF0aCgpIHtcbiAgLy8gV2UgY2FuJ3QgdXNlIHdpbmRvdy5sb2NhdGlvbi5oYXNoIGhlcmUgYmVjYXVzZSBpdCdzIG5vdFxuICAvLyBjb25zaXN0ZW50IGFjcm9zcyBicm93c2VycyAtIEZpcmVmb3ggd2lsbCBwcmUtZGVjb2RlIGl0IVxuICByZXR1cm4gd2luZG93LmxvY2F0aW9uLmhyZWYuc3BsaXQoJyMnKVsxXSB8fCAnJztcbn1cblxuZnVuY3Rpb24gcmVwbGFjZUhhc2hQYXRoKHBhdGgpIHtcbiAgd2luZG93LmxvY2F0aW9uLnJlcGxhY2Uod2luZG93LmxvY2F0aW9uLnBhdGhuYW1lICsgd2luZG93LmxvY2F0aW9uLnNlYXJjaCArICcjJyArIHBhdGgpO1xufVxuXG5mdW5jdGlvbiBnZXRXaW5kb3dQYXRoKCkge1xuICByZXR1cm4gd2luZG93LmxvY2F0aW9uLnBhdGhuYW1lICsgd2luZG93LmxvY2F0aW9uLnNlYXJjaCArIHdpbmRvdy5sb2NhdGlvbi5oYXNoO1xufVxuXG5mdW5jdGlvbiBnbyhuKSB7XG4gIGlmIChuKSB3aW5kb3cuaGlzdG9yeS5nbyhuKTtcbn1cblxuZnVuY3Rpb24gZ2V0VXNlckNvbmZpcm1hdGlvbihtZXNzYWdlLCBjYWxsYmFjaykge1xuICBjYWxsYmFjayh3aW5kb3cuY29uZmlybShtZXNzYWdlKSk7XG59XG5cbi8qKlxuICogUmV0dXJucyB0cnVlIGlmIHRoZSBIVE1MNSBoaXN0b3J5IEFQSSBpcyBzdXBwb3J0ZWQuIFRha2VuIGZyb20gTW9kZXJuaXpyLlxuICpcbiAqIGh0dHBzOi8vZ2l0aHViLmNvbS9Nb2Rlcm5penIvTW9kZXJuaXpyL2Jsb2IvbWFzdGVyL0xJQ0VOU0VcbiAqIGh0dHBzOi8vZ2l0aHViLmNvbS9Nb2Rlcm5penIvTW9kZXJuaXpyL2Jsb2IvbWFzdGVyL2ZlYXR1cmUtZGV0ZWN0cy9oaXN0b3J5LmpzXG4gKiBjaGFuZ2VkIHRvIGF2b2lkIGZhbHNlIG5lZ2F0aXZlcyBmb3IgV2luZG93cyBQaG9uZXM6IGh0dHBzOi8vZ2l0aHViLmNvbS9yYWNrdC9yZWFjdC1yb3V0ZXIvaXNzdWVzLzU4NlxuICovXG5cbmZ1bmN0aW9uIHN1cHBvcnRzSGlzdG9yeSgpIHtcbiAgdmFyIHVhID0gbmF2aWdhdG9yLnVzZXJBZ2VudDtcbiAgaWYgKCh1YS5pbmRleE9mKCdBbmRyb2lkIDIuJykgIT09IC0xIHx8IHVhLmluZGV4T2YoJ0FuZHJvaWQgNC4wJykgIT09IC0xKSAmJiB1YS5pbmRleE9mKCdNb2JpbGUgU2FmYXJpJykgIT09IC0xICYmIHVhLmluZGV4T2YoJ0Nocm9tZScpID09PSAtMSAmJiB1YS5pbmRleE9mKCdXaW5kb3dzIFBob25lJykgPT09IC0xKSB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG4gIC8vIEZJWE1FOiBXb3JrIGFyb3VuZCBvdXIgYnJvd3NlciBoaXN0b3J5IG5vdCB3b3JraW5nIGNvcnJlY3RseSBvbiBDaHJvbWVcbiAgLy8gaU9TOiBodHRwczovL2dpdGh1Yi5jb20vcmFja3QvcmVhY3Qtcm91dGVyL2lzc3Vlcy8yNTY1XG4gIGlmICh1YS5pbmRleE9mKCdDcmlPUycpICE9PSAtMSkge1xuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuICByZXR1cm4gd2luZG93Lmhpc3RvcnkgJiYgJ3B1c2hTdGF0ZScgaW4gd2luZG93Lmhpc3Rvcnk7XG59XG5cbi8qKlxuICogUmV0dXJucyBmYWxzZSBpZiB1c2luZyBnbyhuKSB3aXRoIGhhc2ggaGlzdG9yeSBjYXVzZXMgYSBmdWxsIHBhZ2UgcmVsb2FkLlxuICovXG5cbmZ1bmN0aW9uIHN1cHBvcnRzR29XaXRob3V0UmVsb2FkVXNpbmdIYXNoKCkge1xuICB2YXIgdWEgPSBuYXZpZ2F0b3IudXNlckFnZW50O1xuICByZXR1cm4gdWEuaW5kZXhPZignRmlyZWZveCcpID09PSAtMTtcbn0iLCIndXNlIHN0cmljdCc7XG5cbmV4cG9ydHMuX19lc01vZHVsZSA9IHRydWU7XG52YXIgY2FuVXNlRE9NID0gISEodHlwZW9mIHdpbmRvdyAhPT0gJ3VuZGVmaW5lZCcgJiYgd2luZG93LmRvY3VtZW50ICYmIHdpbmRvdy5kb2N1bWVudC5jcmVhdGVFbGVtZW50KTtcbmV4cG9ydHMuY2FuVXNlRE9NID0gY2FuVXNlRE9NOyIsIid1c2Ugc3RyaWN0JztcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcblxudmFyIF9leHRlbmRzID0gT2JqZWN0LmFzc2lnbiB8fCBmdW5jdGlvbiAodGFyZ2V0KSB7IGZvciAodmFyIGkgPSAxOyBpIDwgYXJndW1lbnRzLmxlbmd0aDsgaSsrKSB7IHZhciBzb3VyY2UgPSBhcmd1bWVudHNbaV07IGZvciAodmFyIGtleSBpbiBzb3VyY2UpIHsgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChzb3VyY2UsIGtleSkpIHsgdGFyZ2V0W2tleV0gPSBzb3VyY2Vba2V5XTsgfSB9IH0gcmV0dXJuIHRhcmdldDsgfTtcblxuZnVuY3Rpb24gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChvYmopIHsgcmV0dXJuIG9iaiAmJiBvYmouX19lc01vZHVsZSA/IG9iaiA6IHsgJ2RlZmF1bHQnOiBvYmogfTsgfVxuXG52YXIgX2ludmFyaWFudCA9IHJlcXVpcmUoJ2ludmFyaWFudCcpO1xuXG52YXIgX2ludmFyaWFudDIgPSBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KF9pbnZhcmlhbnQpO1xuXG52YXIgX0FjdGlvbnMgPSByZXF1aXJlKCcuL0FjdGlvbnMnKTtcblxudmFyIF9FeGVjdXRpb25FbnZpcm9ubWVudCA9IHJlcXVpcmUoJy4vRXhlY3V0aW9uRW52aXJvbm1lbnQnKTtcblxudmFyIF9ET01VdGlscyA9IHJlcXVpcmUoJy4vRE9NVXRpbHMnKTtcblxudmFyIF9ET01TdGF0ZVN0b3JhZ2UgPSByZXF1aXJlKCcuL0RPTVN0YXRlU3RvcmFnZScpO1xuXG52YXIgX2NyZWF0ZURPTUhpc3RvcnkgPSByZXF1aXJlKCcuL2NyZWF0ZURPTUhpc3RvcnknKTtcblxudmFyIF9jcmVhdGVET01IaXN0b3J5MiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX2NyZWF0ZURPTUhpc3RvcnkpO1xuXG52YXIgX3BhcnNlUGF0aCA9IHJlcXVpcmUoJy4vcGFyc2VQYXRoJyk7XG5cbnZhciBfcGFyc2VQYXRoMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX3BhcnNlUGF0aCk7XG5cbi8qKlxuICogQ3JlYXRlcyBhbmQgcmV0dXJucyBhIGhpc3Rvcnkgb2JqZWN0IHRoYXQgdXNlcyBIVE1MNSdzIGhpc3RvcnkgQVBJXG4gKiAocHVzaFN0YXRlLCByZXBsYWNlU3RhdGUsIGFuZCB0aGUgcG9wc3RhdGUgZXZlbnQpIHRvIG1hbmFnZSBoaXN0b3J5LlxuICogVGhpcyBpcyB0aGUgcmVjb21tZW5kZWQgbWV0aG9kIG9mIG1hbmFnaW5nIGhpc3RvcnkgaW4gYnJvd3NlcnMgYmVjYXVzZVxuICogaXQgcHJvdmlkZXMgdGhlIGNsZWFuZXN0IFVSTHMuXG4gKlxuICogTm90ZTogSW4gYnJvd3NlcnMgdGhhdCBkbyBub3Qgc3VwcG9ydCB0aGUgSFRNTDUgaGlzdG9yeSBBUEkgZnVsbFxuICogcGFnZSByZWxvYWRzIHdpbGwgYmUgdXNlZCB0byBwcmVzZXJ2ZSBVUkxzLlxuICovXG5mdW5jdGlvbiBjcmVhdGVCcm93c2VySGlzdG9yeSgpIHtcbiAgdmFyIG9wdGlvbnMgPSBhcmd1bWVudHMubGVuZ3RoIDw9IDAgfHwgYXJndW1lbnRzWzBdID09PSB1bmRlZmluZWQgPyB7fSA6IGFyZ3VtZW50c1swXTtcblxuICAhX0V4ZWN1dGlvbkVudmlyb25tZW50LmNhblVzZURPTSA/IHByb2Nlc3MuZW52Lk5PREVfRU5WICE9PSAncHJvZHVjdGlvbicgPyBfaW52YXJpYW50MlsnZGVmYXVsdCddKGZhbHNlLCAnQnJvd3NlciBoaXN0b3J5IG5lZWRzIGEgRE9NJykgOiBfaW52YXJpYW50MlsnZGVmYXVsdCddKGZhbHNlKSA6IHVuZGVmaW5lZDtcblxuICB2YXIgZm9yY2VSZWZyZXNoID0gb3B0aW9ucy5mb3JjZVJlZnJlc2g7XG5cbiAgdmFyIGlzU3VwcG9ydGVkID0gX0RPTVV0aWxzLnN1cHBvcnRzSGlzdG9yeSgpO1xuICB2YXIgdXNlUmVmcmVzaCA9ICFpc1N1cHBvcnRlZCB8fCBmb3JjZVJlZnJlc2g7XG5cbiAgZnVuY3Rpb24gZ2V0Q3VycmVudExvY2F0aW9uKGhpc3RvcnlTdGF0ZSkge1xuICAgIGhpc3RvcnlTdGF0ZSA9IGhpc3RvcnlTdGF0ZSB8fCB3aW5kb3cuaGlzdG9yeS5zdGF0ZSB8fCB7fTtcblxuICAgIHZhciBwYXRoID0gX0RPTVV0aWxzLmdldFdpbmRvd1BhdGgoKTtcbiAgICB2YXIgX2hpc3RvcnlTdGF0ZSA9IGhpc3RvcnlTdGF0ZTtcbiAgICB2YXIga2V5ID0gX2hpc3RvcnlTdGF0ZS5rZXk7XG5cbiAgICB2YXIgc3RhdGUgPSB1bmRlZmluZWQ7XG4gICAgaWYgKGtleSkge1xuICAgICAgc3RhdGUgPSBfRE9NU3RhdGVTdG9yYWdlLnJlYWRTdGF0ZShrZXkpO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdGF0ZSA9IG51bGw7XG4gICAgICBrZXkgPSBoaXN0b3J5LmNyZWF0ZUtleSgpO1xuXG4gICAgICBpZiAoaXNTdXBwb3J0ZWQpIHdpbmRvdy5oaXN0b3J5LnJlcGxhY2VTdGF0ZShfZXh0ZW5kcyh7fSwgaGlzdG9yeVN0YXRlLCB7IGtleToga2V5IH0pLCBudWxsLCBwYXRoKTtcbiAgICB9XG5cbiAgICB2YXIgbG9jYXRpb24gPSBfcGFyc2VQYXRoMlsnZGVmYXVsdCddKHBhdGgpO1xuXG4gICAgcmV0dXJuIGhpc3RvcnkuY3JlYXRlTG9jYXRpb24oX2V4dGVuZHMoe30sIGxvY2F0aW9uLCB7IHN0YXRlOiBzdGF0ZSB9KSwgdW5kZWZpbmVkLCBrZXkpO1xuICB9XG5cbiAgZnVuY3Rpb24gc3RhcnRQb3BTdGF0ZUxpc3RlbmVyKF9yZWYpIHtcbiAgICB2YXIgdHJhbnNpdGlvblRvID0gX3JlZi50cmFuc2l0aW9uVG87XG5cbiAgICBmdW5jdGlvbiBwb3BTdGF0ZUxpc3RlbmVyKGV2ZW50KSB7XG4gICAgICBpZiAoZXZlbnQuc3RhdGUgPT09IHVuZGVmaW5lZCkgcmV0dXJuOyAvLyBJZ25vcmUgZXh0cmFuZW91cyBwb3BzdGF0ZSBldmVudHMgaW4gV2ViS2l0LlxuXG4gICAgICB0cmFuc2l0aW9uVG8oZ2V0Q3VycmVudExvY2F0aW9uKGV2ZW50LnN0YXRlKSk7XG4gICAgfVxuXG4gICAgX0RPTVV0aWxzLmFkZEV2ZW50TGlzdGVuZXIod2luZG93LCAncG9wc3RhdGUnLCBwb3BTdGF0ZUxpc3RlbmVyKTtcblxuICAgIHJldHVybiBmdW5jdGlvbiAoKSB7XG4gICAgICBfRE9NVXRpbHMucmVtb3ZlRXZlbnRMaXN0ZW5lcih3aW5kb3csICdwb3BzdGF0ZScsIHBvcFN0YXRlTGlzdGVuZXIpO1xuICAgIH07XG4gIH1cblxuICBmdW5jdGlvbiBmaW5pc2hUcmFuc2l0aW9uKGxvY2F0aW9uKSB7XG4gICAgdmFyIGJhc2VuYW1lID0gbG9jYXRpb24uYmFzZW5hbWU7XG4gICAgdmFyIHBhdGhuYW1lID0gbG9jYXRpb24ucGF0aG5hbWU7XG4gICAgdmFyIHNlYXJjaCA9IGxvY2F0aW9uLnNlYXJjaDtcbiAgICB2YXIgaGFzaCA9IGxvY2F0aW9uLmhhc2g7XG4gICAgdmFyIHN0YXRlID0gbG9jYXRpb24uc3RhdGU7XG4gICAgdmFyIGFjdGlvbiA9IGxvY2F0aW9uLmFjdGlvbjtcbiAgICB2YXIga2V5ID0gbG9jYXRpb24ua2V5O1xuXG4gICAgaWYgKGFjdGlvbiA9PT0gX0FjdGlvbnMuUE9QKSByZXR1cm47IC8vIE5vdGhpbmcgdG8gZG8uXG5cbiAgICBfRE9NU3RhdGVTdG9yYWdlLnNhdmVTdGF0ZShrZXksIHN0YXRlKTtcblxuICAgIHZhciBwYXRoID0gKGJhc2VuYW1lIHx8ICcnKSArIHBhdGhuYW1lICsgc2VhcmNoICsgaGFzaDtcbiAgICB2YXIgaGlzdG9yeVN0YXRlID0ge1xuICAgICAga2V5OiBrZXlcbiAgICB9O1xuXG4gICAgaWYgKGFjdGlvbiA9PT0gX0FjdGlvbnMuUFVTSCkge1xuICAgICAgaWYgKHVzZVJlZnJlc2gpIHtcbiAgICAgICAgd2luZG93LmxvY2F0aW9uLmhyZWYgPSBwYXRoO1xuICAgICAgICByZXR1cm4gZmFsc2U7IC8vIFByZXZlbnQgbG9jYXRpb24gdXBkYXRlLlxuICAgICAgfSBlbHNlIHtcbiAgICAgICAgICB3aW5kb3cuaGlzdG9yeS5wdXNoU3RhdGUoaGlzdG9yeVN0YXRlLCBudWxsLCBwYXRoKTtcbiAgICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICAvLyBSRVBMQUNFXG4gICAgICBpZiAodXNlUmVmcmVzaCkge1xuICAgICAgICB3aW5kb3cubG9jYXRpb24ucmVwbGFjZShwYXRoKTtcbiAgICAgICAgcmV0dXJuIGZhbHNlOyAvLyBQcmV2ZW50IGxvY2F0aW9uIHVwZGF0ZS5cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgd2luZG93Lmhpc3RvcnkucmVwbGFjZVN0YXRlKGhpc3RvcnlTdGF0ZSwgbnVsbCwgcGF0aCk7XG4gICAgICAgIH1cbiAgICB9XG4gIH1cblxuICB2YXIgaGlzdG9yeSA9IF9jcmVhdGVET01IaXN0b3J5MlsnZGVmYXVsdCddKF9leHRlbmRzKHt9LCBvcHRpb25zLCB7XG4gICAgZ2V0Q3VycmVudExvY2F0aW9uOiBnZXRDdXJyZW50TG9jYXRpb24sXG4gICAgZmluaXNoVHJhbnNpdGlvbjogZmluaXNoVHJhbnNpdGlvbixcbiAgICBzYXZlU3RhdGU6IF9ET01TdGF0ZVN0b3JhZ2Uuc2F2ZVN0YXRlXG4gIH0pKTtcblxuICB2YXIgbGlzdGVuZXJDb3VudCA9IDAsXG4gICAgICBzdG9wUG9wU3RhdGVMaXN0ZW5lciA9IHVuZGVmaW5lZDtcblxuICBmdW5jdGlvbiBsaXN0ZW5CZWZvcmUobGlzdGVuZXIpIHtcbiAgICBpZiAoKytsaXN0ZW5lckNvdW50ID09PSAxKSBzdG9wUG9wU3RhdGVMaXN0ZW5lciA9IHN0YXJ0UG9wU3RhdGVMaXN0ZW5lcihoaXN0b3J5KTtcblxuICAgIHZhciB1bmxpc3RlbiA9IGhpc3RvcnkubGlzdGVuQmVmb3JlKGxpc3RlbmVyKTtcblxuICAgIHJldHVybiBmdW5jdGlvbiAoKSB7XG4gICAgICB1bmxpc3RlbigpO1xuXG4gICAgICBpZiAoLS1saXN0ZW5lckNvdW50ID09PSAwKSBzdG9wUG9wU3RhdGVMaXN0ZW5lcigpO1xuICAgIH07XG4gIH1cblxuICBmdW5jdGlvbiBsaXN0ZW4obGlzdGVuZXIpIHtcbiAgICBpZiAoKytsaXN0ZW5lckNvdW50ID09PSAxKSBzdG9wUG9wU3RhdGVMaXN0ZW5lciA9IHN0YXJ0UG9wU3RhdGVMaXN0ZW5lcihoaXN0b3J5KTtcblxuICAgIHZhciB1bmxpc3RlbiA9IGhpc3RvcnkubGlzdGVuKGxpc3RlbmVyKTtcblxuICAgIHJldHVybiBmdW5jdGlvbiAoKSB7XG4gICAgICB1bmxpc3RlbigpO1xuXG4gICAgICBpZiAoLS1saXN0ZW5lckNvdW50ID09PSAwKSBzdG9wUG9wU3RhdGVMaXN0ZW5lcigpO1xuICAgIH07XG4gIH1cblxuICAvLyBkZXByZWNhdGVkXG4gIGZ1bmN0aW9uIHJlZ2lzdGVyVHJhbnNpdGlvbkhvb2soaG9vaykge1xuICAgIGlmICgrK2xpc3RlbmVyQ291bnQgPT09IDEpIHN0b3BQb3BTdGF0ZUxpc3RlbmVyID0gc3RhcnRQb3BTdGF0ZUxpc3RlbmVyKGhpc3RvcnkpO1xuXG4gICAgaGlzdG9yeS5yZWdpc3RlclRyYW5zaXRpb25Ib29rKGhvb2spO1xuICB9XG5cbiAgLy8gZGVwcmVjYXRlZFxuICBmdW5jdGlvbiB1bnJlZ2lzdGVyVHJhbnNpdGlvbkhvb2soaG9vaykge1xuICAgIGhpc3RvcnkudW5yZWdpc3RlclRyYW5zaXRpb25Ib29rKGhvb2spO1xuXG4gICAgaWYgKC0tbGlzdGVuZXJDb3VudCA9PT0gMCkgc3RvcFBvcFN0YXRlTGlzdGVuZXIoKTtcbiAgfVxuXG4gIHJldHVybiBfZXh0ZW5kcyh7fSwgaGlzdG9yeSwge1xuICAgIGxpc3RlbkJlZm9yZTogbGlzdGVuQmVmb3JlLFxuICAgIGxpc3RlbjogbGlzdGVuLFxuICAgIHJlZ2lzdGVyVHJhbnNpdGlvbkhvb2s6IHJlZ2lzdGVyVHJhbnNpdGlvbkhvb2ssXG4gICAgdW5yZWdpc3RlclRyYW5zaXRpb25Ib29rOiB1bnJlZ2lzdGVyVHJhbnNpdGlvbkhvb2tcbiAgfSk7XG59XG5cbmV4cG9ydHNbJ2RlZmF1bHQnXSA9IGNyZWF0ZUJyb3dzZXJIaXN0b3J5O1xubW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzWydkZWZhdWx0J107IiwiJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuXG52YXIgX2V4dGVuZHMgPSBPYmplY3QuYXNzaWduIHx8IGZ1bmN0aW9uICh0YXJnZXQpIHsgZm9yICh2YXIgaSA9IDE7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyBpKyspIHsgdmFyIHNvdXJjZSA9IGFyZ3VtZW50c1tpXTsgZm9yICh2YXIga2V5IGluIHNvdXJjZSkgeyBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKHNvdXJjZSwga2V5KSkgeyB0YXJnZXRba2V5XSA9IHNvdXJjZVtrZXldOyB9IH0gfSByZXR1cm4gdGFyZ2V0OyB9O1xuXG5mdW5jdGlvbiBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KG9iaikgeyByZXR1cm4gb2JqICYmIG9iai5fX2VzTW9kdWxlID8gb2JqIDogeyAnZGVmYXVsdCc6IG9iaiB9OyB9XG5cbnZhciBfaW52YXJpYW50ID0gcmVxdWlyZSgnaW52YXJpYW50Jyk7XG5cbnZhciBfaW52YXJpYW50MiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX2ludmFyaWFudCk7XG5cbnZhciBfRXhlY3V0aW9uRW52aXJvbm1lbnQgPSByZXF1aXJlKCcuL0V4ZWN1dGlvbkVudmlyb25tZW50Jyk7XG5cbnZhciBfRE9NVXRpbHMgPSByZXF1aXJlKCcuL0RPTVV0aWxzJyk7XG5cbnZhciBfY3JlYXRlSGlzdG9yeSA9IHJlcXVpcmUoJy4vY3JlYXRlSGlzdG9yeScpO1xuXG52YXIgX2NyZWF0ZUhpc3RvcnkyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfY3JlYXRlSGlzdG9yeSk7XG5cbmZ1bmN0aW9uIGNyZWF0ZURPTUhpc3Rvcnkob3B0aW9ucykge1xuICB2YXIgaGlzdG9yeSA9IF9jcmVhdGVIaXN0b3J5MlsnZGVmYXVsdCddKF9leHRlbmRzKHtcbiAgICBnZXRVc2VyQ29uZmlybWF0aW9uOiBfRE9NVXRpbHMuZ2V0VXNlckNvbmZpcm1hdGlvblxuICB9LCBvcHRpb25zLCB7XG4gICAgZ286IF9ET01VdGlscy5nb1xuICB9KSk7XG5cbiAgZnVuY3Rpb24gbGlzdGVuKGxpc3RlbmVyKSB7XG4gICAgIV9FeGVjdXRpb25FbnZpcm9ubWVudC5jYW5Vc2VET00gPyBwcm9jZXNzLmVudi5OT0RFX0VOViAhPT0gJ3Byb2R1Y3Rpb24nID8gX2ludmFyaWFudDJbJ2RlZmF1bHQnXShmYWxzZSwgJ0RPTSBoaXN0b3J5IG5lZWRzIGEgRE9NJykgOiBfaW52YXJpYW50MlsnZGVmYXVsdCddKGZhbHNlKSA6IHVuZGVmaW5lZDtcblxuICAgIHJldHVybiBoaXN0b3J5Lmxpc3RlbihsaXN0ZW5lcik7XG4gIH1cblxuICByZXR1cm4gX2V4dGVuZHMoe30sIGhpc3RvcnksIHtcbiAgICBsaXN0ZW46IGxpc3RlblxuICB9KTtcbn1cblxuZXhwb3J0c1snZGVmYXVsdCddID0gY3JlYXRlRE9NSGlzdG9yeTtcbm1vZHVsZS5leHBvcnRzID0gZXhwb3J0c1snZGVmYXVsdCddOyIsIi8vaW1wb3J0IHdhcm5pbmcgZnJvbSAnd2FybmluZydcbid1c2Ugc3RyaWN0JztcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcblxudmFyIF9leHRlbmRzID0gT2JqZWN0LmFzc2lnbiB8fCBmdW5jdGlvbiAodGFyZ2V0KSB7IGZvciAodmFyIGkgPSAxOyBpIDwgYXJndW1lbnRzLmxlbmd0aDsgaSsrKSB7IHZhciBzb3VyY2UgPSBhcmd1bWVudHNbaV07IGZvciAodmFyIGtleSBpbiBzb3VyY2UpIHsgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChzb3VyY2UsIGtleSkpIHsgdGFyZ2V0W2tleV0gPSBzb3VyY2Vba2V5XTsgfSB9IH0gcmV0dXJuIHRhcmdldDsgfTtcblxuZnVuY3Rpb24gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChvYmopIHsgcmV0dXJuIG9iaiAmJiBvYmouX19lc01vZHVsZSA/IG9iaiA6IHsgJ2RlZmF1bHQnOiBvYmogfTsgfVxuXG52YXIgX2RlZXBFcXVhbCA9IHJlcXVpcmUoJ2RlZXAtZXF1YWwnKTtcblxudmFyIF9kZWVwRXF1YWwyID0gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChfZGVlcEVxdWFsKTtcblxudmFyIF9Bc3luY1V0aWxzID0gcmVxdWlyZSgnLi9Bc3luY1V0aWxzJyk7XG5cbnZhciBfQWN0aW9ucyA9IHJlcXVpcmUoJy4vQWN0aW9ucycpO1xuXG52YXIgX2NyZWF0ZUxvY2F0aW9uMiA9IHJlcXVpcmUoJy4vY3JlYXRlTG9jYXRpb24nKTtcblxudmFyIF9jcmVhdGVMb2NhdGlvbjMgPSBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KF9jcmVhdGVMb2NhdGlvbjIpO1xuXG52YXIgX3J1blRyYW5zaXRpb25Ib29rID0gcmVxdWlyZSgnLi9ydW5UcmFuc2l0aW9uSG9vaycpO1xuXG52YXIgX3J1blRyYW5zaXRpb25Ib29rMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX3J1blRyYW5zaXRpb25Ib29rKTtcblxudmFyIF9wYXJzZVBhdGggPSByZXF1aXJlKCcuL3BhcnNlUGF0aCcpO1xuXG52YXIgX3BhcnNlUGF0aDIgPSBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KF9wYXJzZVBhdGgpO1xuXG52YXIgX2RlcHJlY2F0ZSA9IHJlcXVpcmUoJy4vZGVwcmVjYXRlJyk7XG5cbnZhciBfZGVwcmVjYXRlMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX2RlcHJlY2F0ZSk7XG5cbmZ1bmN0aW9uIGNyZWF0ZVJhbmRvbUtleShsZW5ndGgpIHtcbiAgcmV0dXJuIE1hdGgucmFuZG9tKCkudG9TdHJpbmcoMzYpLnN1YnN0cigyLCBsZW5ndGgpO1xufVxuXG5mdW5jdGlvbiBsb2NhdGlvbnNBcmVFcXVhbChhLCBiKSB7XG4gIHJldHVybiBhLnBhdGhuYW1lID09PSBiLnBhdGhuYW1lICYmIGEuc2VhcmNoID09PSBiLnNlYXJjaCAmJlxuICAvL2EuYWN0aW9uID09PSBiLmFjdGlvbiAmJiAvLyBEaWZmZXJlbnQgYWN0aW9uICE9PSBsb2NhdGlvbiBjaGFuZ2UuXG4gIGEua2V5ID09PSBiLmtleSAmJiBfZGVlcEVxdWFsMlsnZGVmYXVsdCddKGEuc3RhdGUsIGIuc3RhdGUpO1xufVxuXG52YXIgRGVmYXVsdEtleUxlbmd0aCA9IDY7XG5cbmZ1bmN0aW9uIGNyZWF0ZUhpc3RvcnkoKSB7XG4gIHZhciBvcHRpb25zID0gYXJndW1lbnRzLmxlbmd0aCA8PSAwIHx8IGFyZ3VtZW50c1swXSA9PT0gdW5kZWZpbmVkID8ge30gOiBhcmd1bWVudHNbMF07XG4gIHZhciBnZXRDdXJyZW50TG9jYXRpb24gPSBvcHRpb25zLmdldEN1cnJlbnRMb2NhdGlvbjtcbiAgdmFyIGZpbmlzaFRyYW5zaXRpb24gPSBvcHRpb25zLmZpbmlzaFRyYW5zaXRpb247XG4gIHZhciBzYXZlU3RhdGUgPSBvcHRpb25zLnNhdmVTdGF0ZTtcbiAgdmFyIGdvID0gb3B0aW9ucy5nbztcbiAgdmFyIGtleUxlbmd0aCA9IG9wdGlvbnMua2V5TGVuZ3RoO1xuICB2YXIgZ2V0VXNlckNvbmZpcm1hdGlvbiA9IG9wdGlvbnMuZ2V0VXNlckNvbmZpcm1hdGlvbjtcblxuICBpZiAodHlwZW9mIGtleUxlbmd0aCAhPT0gJ251bWJlcicpIGtleUxlbmd0aCA9IERlZmF1bHRLZXlMZW5ndGg7XG5cbiAgdmFyIHRyYW5zaXRpb25Ib29rcyA9IFtdO1xuXG4gIGZ1bmN0aW9uIGxpc3RlbkJlZm9yZShob29rKSB7XG4gICAgdHJhbnNpdGlvbkhvb2tzLnB1c2goaG9vayk7XG5cbiAgICByZXR1cm4gZnVuY3Rpb24gKCkge1xuICAgICAgdHJhbnNpdGlvbkhvb2tzID0gdHJhbnNpdGlvbkhvb2tzLmZpbHRlcihmdW5jdGlvbiAoaXRlbSkge1xuICAgICAgICByZXR1cm4gaXRlbSAhPT0gaG9vaztcbiAgICAgIH0pO1xuICAgIH07XG4gIH1cblxuICB2YXIgYWxsS2V5cyA9IFtdO1xuICB2YXIgY2hhbmdlTGlzdGVuZXJzID0gW107XG4gIHZhciBsb2NhdGlvbiA9IHVuZGVmaW5lZDtcblxuICBmdW5jdGlvbiBnZXRDdXJyZW50KCkge1xuICAgIGlmIChwZW5kaW5nTG9jYXRpb24gJiYgcGVuZGluZ0xvY2F0aW9uLmFjdGlvbiA9PT0gX0FjdGlvbnMuUE9QKSB7XG4gICAgICByZXR1cm4gYWxsS2V5cy5pbmRleE9mKHBlbmRpbmdMb2NhdGlvbi5rZXkpO1xuICAgIH0gZWxzZSBpZiAobG9jYXRpb24pIHtcbiAgICAgIHJldHVybiBhbGxLZXlzLmluZGV4T2YobG9jYXRpb24ua2V5KTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIC0xO1xuICAgIH1cbiAgfVxuXG4gIGZ1bmN0aW9uIHVwZGF0ZUxvY2F0aW9uKG5ld0xvY2F0aW9uKSB7XG4gICAgdmFyIGN1cnJlbnQgPSBnZXRDdXJyZW50KCk7XG5cbiAgICBsb2NhdGlvbiA9IG5ld0xvY2F0aW9uO1xuXG4gICAgaWYgKGxvY2F0aW9uLmFjdGlvbiA9PT0gX0FjdGlvbnMuUFVTSCkge1xuICAgICAgYWxsS2V5cyA9IFtdLmNvbmNhdChhbGxLZXlzLnNsaWNlKDAsIGN1cnJlbnQgKyAxKSwgW2xvY2F0aW9uLmtleV0pO1xuICAgIH0gZWxzZSBpZiAobG9jYXRpb24uYWN0aW9uID09PSBfQWN0aW9ucy5SRVBMQUNFKSB7XG4gICAgICBhbGxLZXlzW2N1cnJlbnRdID0gbG9jYXRpb24ua2V5O1xuICAgIH1cblxuICAgIGNoYW5nZUxpc3RlbmVycy5mb3JFYWNoKGZ1bmN0aW9uIChsaXN0ZW5lcikge1xuICAgICAgbGlzdGVuZXIobG9jYXRpb24pO1xuICAgIH0pO1xuICB9XG5cbiAgZnVuY3Rpb24gbGlzdGVuKGxpc3RlbmVyKSB7XG4gICAgY2hhbmdlTGlzdGVuZXJzLnB1c2gobGlzdGVuZXIpO1xuXG4gICAgaWYgKGxvY2F0aW9uKSB7XG4gICAgICBsaXN0ZW5lcihsb2NhdGlvbik7XG4gICAgfSBlbHNlIHtcbiAgICAgIHZhciBfbG9jYXRpb24gPSBnZXRDdXJyZW50TG9jYXRpb24oKTtcbiAgICAgIGFsbEtleXMgPSBbX2xvY2F0aW9uLmtleV07XG4gICAgICB1cGRhdGVMb2NhdGlvbihfbG9jYXRpb24pO1xuICAgIH1cblxuICAgIHJldHVybiBmdW5jdGlvbiAoKSB7XG4gICAgICBjaGFuZ2VMaXN0ZW5lcnMgPSBjaGFuZ2VMaXN0ZW5lcnMuZmlsdGVyKGZ1bmN0aW9uIChpdGVtKSB7XG4gICAgICAgIHJldHVybiBpdGVtICE9PSBsaXN0ZW5lcjtcbiAgICAgIH0pO1xuICAgIH07XG4gIH1cblxuICBmdW5jdGlvbiBjb25maXJtVHJhbnNpdGlvblRvKGxvY2F0aW9uLCBjYWxsYmFjaykge1xuICAgIF9Bc3luY1V0aWxzLmxvb3BBc3luYyh0cmFuc2l0aW9uSG9va3MubGVuZ3RoLCBmdW5jdGlvbiAoaW5kZXgsIG5leHQsIGRvbmUpIHtcbiAgICAgIF9ydW5UcmFuc2l0aW9uSG9vazJbJ2RlZmF1bHQnXSh0cmFuc2l0aW9uSG9va3NbaW5kZXhdLCBsb2NhdGlvbiwgZnVuY3Rpb24gKHJlc3VsdCkge1xuICAgICAgICBpZiAocmVzdWx0ICE9IG51bGwpIHtcbiAgICAgICAgICBkb25lKHJlc3VsdCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgbmV4dCgpO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9LCBmdW5jdGlvbiAobWVzc2FnZSkge1xuICAgICAgaWYgKGdldFVzZXJDb25maXJtYXRpb24gJiYgdHlwZW9mIG1lc3NhZ2UgPT09ICdzdHJpbmcnKSB7XG4gICAgICAgIGdldFVzZXJDb25maXJtYXRpb24obWVzc2FnZSwgZnVuY3Rpb24gKG9rKSB7XG4gICAgICAgICAgY2FsbGJhY2sob2sgIT09IGZhbHNlKTtcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjYWxsYmFjayhtZXNzYWdlICE9PSBmYWxzZSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICB2YXIgcGVuZGluZ0xvY2F0aW9uID0gdW5kZWZpbmVkO1xuXG4gIGZ1bmN0aW9uIHRyYW5zaXRpb25UbyhuZXh0TG9jYXRpb24pIHtcbiAgICBpZiAobG9jYXRpb24gJiYgbG9jYXRpb25zQXJlRXF1YWwobG9jYXRpb24sIG5leHRMb2NhdGlvbikpIHJldHVybjsgLy8gTm90aGluZyB0byBkby5cblxuICAgIHBlbmRpbmdMb2NhdGlvbiA9IG5leHRMb2NhdGlvbjtcblxuICAgIGNvbmZpcm1UcmFuc2l0aW9uVG8obmV4dExvY2F0aW9uLCBmdW5jdGlvbiAob2spIHtcbiAgICAgIGlmIChwZW5kaW5nTG9jYXRpb24gIT09IG5leHRMb2NhdGlvbikgcmV0dXJuOyAvLyBUcmFuc2l0aW9uIHdhcyBpbnRlcnJ1cHRlZC5cblxuICAgICAgaWYgKG9rKSB7XG4gICAgICAgIC8vIHRyZWF0IFBVU0ggdG8gY3VycmVudCBwYXRoIGxpa2UgUkVQTEFDRSB0byBiZSBjb25zaXN0ZW50IHdpdGggYnJvd3NlcnNcbiAgICAgICAgaWYgKG5leHRMb2NhdGlvbi5hY3Rpb24gPT09IF9BY3Rpb25zLlBVU0gpIHtcbiAgICAgICAgICB2YXIgcHJldlBhdGggPSBjcmVhdGVQYXRoKGxvY2F0aW9uKTtcbiAgICAgICAgICB2YXIgbmV4dFBhdGggPSBjcmVhdGVQYXRoKG5leHRMb2NhdGlvbik7XG5cbiAgICAgICAgICBpZiAobmV4dFBhdGggPT09IHByZXZQYXRoKSBuZXh0TG9jYXRpb24uYWN0aW9uID0gX0FjdGlvbnMuUkVQTEFDRTtcbiAgICAgICAgfVxuXG4gICAgICAgIGlmIChmaW5pc2hUcmFuc2l0aW9uKG5leHRMb2NhdGlvbikgIT09IGZhbHNlKSB1cGRhdGVMb2NhdGlvbihuZXh0TG9jYXRpb24pO1xuICAgICAgfSBlbHNlIGlmIChsb2NhdGlvbiAmJiBuZXh0TG9jYXRpb24uYWN0aW9uID09PSBfQWN0aW9ucy5QT1ApIHtcbiAgICAgICAgdmFyIHByZXZJbmRleCA9IGFsbEtleXMuaW5kZXhPZihsb2NhdGlvbi5rZXkpO1xuICAgICAgICB2YXIgbmV4dEluZGV4ID0gYWxsS2V5cy5pbmRleE9mKG5leHRMb2NhdGlvbi5rZXkpO1xuXG4gICAgICAgIGlmIChwcmV2SW5kZXggIT09IC0xICYmIG5leHRJbmRleCAhPT0gLTEpIGdvKHByZXZJbmRleCAtIG5leHRJbmRleCk7IC8vIFJlc3RvcmUgdGhlIFVSTC5cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIGZ1bmN0aW9uIHB1c2gobG9jYXRpb24pIHtcbiAgICB0cmFuc2l0aW9uVG8oY3JlYXRlTG9jYXRpb24obG9jYXRpb24sIF9BY3Rpb25zLlBVU0gsIGNyZWF0ZUtleSgpKSk7XG4gIH1cblxuICBmdW5jdGlvbiByZXBsYWNlKGxvY2F0aW9uKSB7XG4gICAgdHJhbnNpdGlvblRvKGNyZWF0ZUxvY2F0aW9uKGxvY2F0aW9uLCBfQWN0aW9ucy5SRVBMQUNFLCBjcmVhdGVLZXkoKSkpO1xuICB9XG5cbiAgZnVuY3Rpb24gZ29CYWNrKCkge1xuICAgIGdvKC0xKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIGdvRm9yd2FyZCgpIHtcbiAgICBnbygxKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIGNyZWF0ZUtleSgpIHtcbiAgICByZXR1cm4gY3JlYXRlUmFuZG9tS2V5KGtleUxlbmd0aCk7XG4gIH1cblxuICBmdW5jdGlvbiBjcmVhdGVQYXRoKGxvY2F0aW9uKSB7XG4gICAgaWYgKGxvY2F0aW9uID09IG51bGwgfHwgdHlwZW9mIGxvY2F0aW9uID09PSAnc3RyaW5nJykgcmV0dXJuIGxvY2F0aW9uO1xuXG4gICAgdmFyIHBhdGhuYW1lID0gbG9jYXRpb24ucGF0aG5hbWU7XG4gICAgdmFyIHNlYXJjaCA9IGxvY2F0aW9uLnNlYXJjaDtcbiAgICB2YXIgaGFzaCA9IGxvY2F0aW9uLmhhc2g7XG5cbiAgICB2YXIgcmVzdWx0ID0gcGF0aG5hbWU7XG5cbiAgICBpZiAoc2VhcmNoKSByZXN1bHQgKz0gc2VhcmNoO1xuXG4gICAgaWYgKGhhc2gpIHJlc3VsdCArPSBoYXNoO1xuXG4gICAgcmV0dXJuIHJlc3VsdDtcbiAgfVxuXG4gIGZ1bmN0aW9uIGNyZWF0ZUhyZWYobG9jYXRpb24pIHtcbiAgICByZXR1cm4gY3JlYXRlUGF0aChsb2NhdGlvbik7XG4gIH1cblxuICBmdW5jdGlvbiBjcmVhdGVMb2NhdGlvbihsb2NhdGlvbiwgYWN0aW9uKSB7XG4gICAgdmFyIGtleSA9IGFyZ3VtZW50cy5sZW5ndGggPD0gMiB8fCBhcmd1bWVudHNbMl0gPT09IHVuZGVmaW5lZCA/IGNyZWF0ZUtleSgpIDogYXJndW1lbnRzWzJdO1xuXG4gICAgaWYgKHR5cGVvZiBhY3Rpb24gPT09ICdvYmplY3QnKSB7XG4gICAgICAvL3dhcm5pbmcoXG4gICAgICAvLyAgZmFsc2UsXG4gICAgICAvLyAgJ1RoZSBzdGF0ZSAoMm5kKSBhcmd1bWVudCB0byBoaXN0b3J5LmNyZWF0ZUxvY2F0aW9uIGlzIGRlcHJlY2F0ZWQ7IHVzZSBhICcgK1xuICAgICAgLy8gICdsb2NhdGlvbiBkZXNjcmlwdG9yIGluc3RlYWQnXG4gICAgICAvLylcblxuICAgICAgaWYgKHR5cGVvZiBsb2NhdGlvbiA9PT0gJ3N0cmluZycpIGxvY2F0aW9uID0gX3BhcnNlUGF0aDJbJ2RlZmF1bHQnXShsb2NhdGlvbik7XG5cbiAgICAgIGxvY2F0aW9uID0gX2V4dGVuZHMoe30sIGxvY2F0aW9uLCB7IHN0YXRlOiBhY3Rpb24gfSk7XG5cbiAgICAgIGFjdGlvbiA9IGtleTtcbiAgICAgIGtleSA9IGFyZ3VtZW50c1szXSB8fCBjcmVhdGVLZXkoKTtcbiAgICB9XG5cbiAgICByZXR1cm4gX2NyZWF0ZUxvY2F0aW9uM1snZGVmYXVsdCddKGxvY2F0aW9uLCBhY3Rpb24sIGtleSk7XG4gIH1cblxuICAvLyBkZXByZWNhdGVkXG4gIGZ1bmN0aW9uIHNldFN0YXRlKHN0YXRlKSB7XG4gICAgaWYgKGxvY2F0aW9uKSB7XG4gICAgICB1cGRhdGVMb2NhdGlvblN0YXRlKGxvY2F0aW9uLCBzdGF0ZSk7XG4gICAgICB1cGRhdGVMb2NhdGlvbihsb2NhdGlvbik7XG4gICAgfSBlbHNlIHtcbiAgICAgIHVwZGF0ZUxvY2F0aW9uU3RhdGUoZ2V0Q3VycmVudExvY2F0aW9uKCksIHN0YXRlKTtcbiAgICB9XG4gIH1cblxuICBmdW5jdGlvbiB1cGRhdGVMb2NhdGlvblN0YXRlKGxvY2F0aW9uLCBzdGF0ZSkge1xuICAgIGxvY2F0aW9uLnN0YXRlID0gX2V4dGVuZHMoe30sIGxvY2F0aW9uLnN0YXRlLCBzdGF0ZSk7XG4gICAgc2F2ZVN0YXRlKGxvY2F0aW9uLmtleSwgbG9jYXRpb24uc3RhdGUpO1xuICB9XG5cbiAgLy8gZGVwcmVjYXRlZFxuICBmdW5jdGlvbiByZWdpc3RlclRyYW5zaXRpb25Ib29rKGhvb2spIHtcbiAgICBpZiAodHJhbnNpdGlvbkhvb2tzLmluZGV4T2YoaG9vaykgPT09IC0xKSB0cmFuc2l0aW9uSG9va3MucHVzaChob29rKTtcbiAgfVxuXG4gIC8vIGRlcHJlY2F0ZWRcbiAgZnVuY3Rpb24gdW5yZWdpc3RlclRyYW5zaXRpb25Ib29rKGhvb2spIHtcbiAgICB0cmFuc2l0aW9uSG9va3MgPSB0cmFuc2l0aW9uSG9va3MuZmlsdGVyKGZ1bmN0aW9uIChpdGVtKSB7XG4gICAgICByZXR1cm4gaXRlbSAhPT0gaG9vaztcbiAgICB9KTtcbiAgfVxuXG4gIC8vIGRlcHJlY2F0ZWRcbiAgZnVuY3Rpb24gcHVzaFN0YXRlKHN0YXRlLCBwYXRoKSB7XG4gICAgaWYgKHR5cGVvZiBwYXRoID09PSAnc3RyaW5nJykgcGF0aCA9IF9wYXJzZVBhdGgyWydkZWZhdWx0J10ocGF0aCk7XG5cbiAgICBwdXNoKF9leHRlbmRzKHsgc3RhdGU6IHN0YXRlIH0sIHBhdGgpKTtcbiAgfVxuXG4gIC8vIGRlcHJlY2F0ZWRcbiAgZnVuY3Rpb24gcmVwbGFjZVN0YXRlKHN0YXRlLCBwYXRoKSB7XG4gICAgaWYgKHR5cGVvZiBwYXRoID09PSAnc3RyaW5nJykgcGF0aCA9IF9wYXJzZVBhdGgyWydkZWZhdWx0J10ocGF0aCk7XG5cbiAgICByZXBsYWNlKF9leHRlbmRzKHsgc3RhdGU6IHN0YXRlIH0sIHBhdGgpKTtcbiAgfVxuXG4gIHJldHVybiB7XG4gICAgbGlzdGVuQmVmb3JlOiBsaXN0ZW5CZWZvcmUsXG4gICAgbGlzdGVuOiBsaXN0ZW4sXG4gICAgdHJhbnNpdGlvblRvOiB0cmFuc2l0aW9uVG8sXG4gICAgcHVzaDogcHVzaCxcbiAgICByZXBsYWNlOiByZXBsYWNlLFxuICAgIGdvOiBnbyxcbiAgICBnb0JhY2s6IGdvQmFjayxcbiAgICBnb0ZvcndhcmQ6IGdvRm9yd2FyZCxcbiAgICBjcmVhdGVLZXk6IGNyZWF0ZUtleSxcbiAgICBjcmVhdGVQYXRoOiBjcmVhdGVQYXRoLFxuICAgIGNyZWF0ZUhyZWY6IGNyZWF0ZUhyZWYsXG4gICAgY3JlYXRlTG9jYXRpb246IGNyZWF0ZUxvY2F0aW9uLFxuXG4gICAgc2V0U3RhdGU6IF9kZXByZWNhdGUyWydkZWZhdWx0J10oc2V0U3RhdGUsICdzZXRTdGF0ZSBpcyBkZXByZWNhdGVkOyB1c2UgbG9jYXRpb24ua2V5IHRvIHNhdmUgc3RhdGUgaW5zdGVhZCcpLFxuICAgIHJlZ2lzdGVyVHJhbnNpdGlvbkhvb2s6IF9kZXByZWNhdGUyWydkZWZhdWx0J10ocmVnaXN0ZXJUcmFuc2l0aW9uSG9vaywgJ3JlZ2lzdGVyVHJhbnNpdGlvbkhvb2sgaXMgZGVwcmVjYXRlZDsgdXNlIGxpc3RlbkJlZm9yZSBpbnN0ZWFkJyksXG4gICAgdW5yZWdpc3RlclRyYW5zaXRpb25Ib29rOiBfZGVwcmVjYXRlMlsnZGVmYXVsdCddKHVucmVnaXN0ZXJUcmFuc2l0aW9uSG9vaywgJ3VucmVnaXN0ZXJUcmFuc2l0aW9uSG9vayBpcyBkZXByZWNhdGVkOyB1c2UgdGhlIGNhbGxiYWNrIHJldHVybmVkIGZyb20gbGlzdGVuQmVmb3JlIGluc3RlYWQnKSxcbiAgICBwdXNoU3RhdGU6IF9kZXByZWNhdGUyWydkZWZhdWx0J10ocHVzaFN0YXRlLCAncHVzaFN0YXRlIGlzIGRlcHJlY2F0ZWQ7IHVzZSBwdXNoIGluc3RlYWQnKSxcbiAgICByZXBsYWNlU3RhdGU6IF9kZXByZWNhdGUyWydkZWZhdWx0J10ocmVwbGFjZVN0YXRlLCAncmVwbGFjZVN0YXRlIGlzIGRlcHJlY2F0ZWQ7IHVzZSByZXBsYWNlIGluc3RlYWQnKVxuICB9O1xufVxuXG5leHBvcnRzWydkZWZhdWx0J10gPSBjcmVhdGVIaXN0b3J5O1xubW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzWydkZWZhdWx0J107IiwiLy9pbXBvcnQgd2FybmluZyBmcm9tICd3YXJuaW5nJ1xuJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuXG52YXIgX2V4dGVuZHMgPSBPYmplY3QuYXNzaWduIHx8IGZ1bmN0aW9uICh0YXJnZXQpIHsgZm9yICh2YXIgaSA9IDE7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyBpKyspIHsgdmFyIHNvdXJjZSA9IGFyZ3VtZW50c1tpXTsgZm9yICh2YXIga2V5IGluIHNvdXJjZSkgeyBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKHNvdXJjZSwga2V5KSkgeyB0YXJnZXRba2V5XSA9IHNvdXJjZVtrZXldOyB9IH0gfSByZXR1cm4gdGFyZ2V0OyB9O1xuXG5mdW5jdGlvbiBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KG9iaikgeyByZXR1cm4gb2JqICYmIG9iai5fX2VzTW9kdWxlID8gb2JqIDogeyAnZGVmYXVsdCc6IG9iaiB9OyB9XG5cbnZhciBfQWN0aW9ucyA9IHJlcXVpcmUoJy4vQWN0aW9ucycpO1xuXG52YXIgX3BhcnNlUGF0aCA9IHJlcXVpcmUoJy4vcGFyc2VQYXRoJyk7XG5cbnZhciBfcGFyc2VQYXRoMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX3BhcnNlUGF0aCk7XG5cbmZ1bmN0aW9uIGNyZWF0ZUxvY2F0aW9uKCkge1xuICB2YXIgbG9jYXRpb24gPSBhcmd1bWVudHMubGVuZ3RoIDw9IDAgfHwgYXJndW1lbnRzWzBdID09PSB1bmRlZmluZWQgPyAnLycgOiBhcmd1bWVudHNbMF07XG4gIHZhciBhY3Rpb24gPSBhcmd1bWVudHMubGVuZ3RoIDw9IDEgfHwgYXJndW1lbnRzWzFdID09PSB1bmRlZmluZWQgPyBfQWN0aW9ucy5QT1AgOiBhcmd1bWVudHNbMV07XG4gIHZhciBrZXkgPSBhcmd1bWVudHMubGVuZ3RoIDw9IDIgfHwgYXJndW1lbnRzWzJdID09PSB1bmRlZmluZWQgPyBudWxsIDogYXJndW1lbnRzWzJdO1xuXG4gIHZhciBfZm91cnRoQXJnID0gYXJndW1lbnRzLmxlbmd0aCA8PSAzIHx8IGFyZ3VtZW50c1szXSA9PT0gdW5kZWZpbmVkID8gbnVsbCA6IGFyZ3VtZW50c1szXTtcblxuICBpZiAodHlwZW9mIGxvY2F0aW9uID09PSAnc3RyaW5nJykgbG9jYXRpb24gPSBfcGFyc2VQYXRoMlsnZGVmYXVsdCddKGxvY2F0aW9uKTtcblxuICBpZiAodHlwZW9mIGFjdGlvbiA9PT0gJ29iamVjdCcpIHtcbiAgICAvL3dhcm5pbmcoXG4gICAgLy8gIGZhbHNlLFxuICAgIC8vICAnVGhlIHN0YXRlICgybmQpIGFyZ3VtZW50IHRvIGNyZWF0ZUxvY2F0aW9uIGlzIGRlcHJlY2F0ZWQ7IHVzZSBhICcgK1xuICAgIC8vICAnbG9jYXRpb24gZGVzY3JpcHRvciBpbnN0ZWFkJ1xuICAgIC8vKVxuXG4gICAgbG9jYXRpb24gPSBfZXh0ZW5kcyh7fSwgbG9jYXRpb24sIHsgc3RhdGU6IGFjdGlvbiB9KTtcblxuICAgIGFjdGlvbiA9IGtleSB8fCBfQWN0aW9ucy5QT1A7XG4gICAga2V5ID0gX2ZvdXJ0aEFyZztcbiAgfVxuXG4gIHZhciBwYXRobmFtZSA9IGxvY2F0aW9uLnBhdGhuYW1lIHx8ICcvJztcbiAgdmFyIHNlYXJjaCA9IGxvY2F0aW9uLnNlYXJjaCB8fCAnJztcbiAgdmFyIGhhc2ggPSBsb2NhdGlvbi5oYXNoIHx8ICcnO1xuICB2YXIgc3RhdGUgPSBsb2NhdGlvbi5zdGF0ZSB8fCBudWxsO1xuXG4gIHJldHVybiB7XG4gICAgcGF0aG5hbWU6IHBhdGhuYW1lLFxuICAgIHNlYXJjaDogc2VhcmNoLFxuICAgIGhhc2g6IGhhc2gsXG4gICAgc3RhdGU6IHN0YXRlLFxuICAgIGFjdGlvbjogYWN0aW9uLFxuICAgIGtleToga2V5XG4gIH07XG59XG5cbmV4cG9ydHNbJ2RlZmF1bHQnXSA9IGNyZWF0ZUxvY2F0aW9uO1xubW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzWydkZWZhdWx0J107IiwiLy9pbXBvcnQgd2FybmluZyBmcm9tICd3YXJuaW5nJ1xuXG5cInVzZSBzdHJpY3RcIjtcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcbmZ1bmN0aW9uIGRlcHJlY2F0ZShmbikge1xuICByZXR1cm4gZm47XG4gIC8vcmV0dXJuIGZ1bmN0aW9uICgpIHtcbiAgLy8gIHdhcm5pbmcoZmFsc2UsICdbaGlzdG9yeV0gJyArIG1lc3NhZ2UpXG4gIC8vICByZXR1cm4gZm4uYXBwbHkodGhpcywgYXJndW1lbnRzKVxuICAvL31cbn1cblxuZXhwb3J0c1tcImRlZmF1bHRcIl0gPSBkZXByZWNhdGU7XG5tb2R1bGUuZXhwb3J0cyA9IGV4cG9ydHNbXCJkZWZhdWx0XCJdOyIsIlwidXNlIHN0cmljdFwiO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuZnVuY3Rpb24gZXh0cmFjdFBhdGgoc3RyaW5nKSB7XG4gIHZhciBtYXRjaCA9IHN0cmluZy5tYXRjaCgvXmh0dHBzPzpcXC9cXC9bXlxcL10qLyk7XG5cbiAgaWYgKG1hdGNoID09IG51bGwpIHJldHVybiBzdHJpbmc7XG5cbiAgcmV0dXJuIHN0cmluZy5zdWJzdHJpbmcobWF0Y2hbMF0ubGVuZ3RoKTtcbn1cblxuZXhwb3J0c1tcImRlZmF1bHRcIl0gPSBleHRyYWN0UGF0aDtcbm1vZHVsZS5leHBvcnRzID0gZXhwb3J0c1tcImRlZmF1bHRcIl07IiwiJ3VzZSBzdHJpY3QnO1xuXG5leHBvcnRzLl9fZXNNb2R1bGUgPSB0cnVlO1xuXG5mdW5jdGlvbiBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KG9iaikgeyByZXR1cm4gb2JqICYmIG9iai5fX2VzTW9kdWxlID8gb2JqIDogeyAnZGVmYXVsdCc6IG9iaiB9OyB9XG5cbnZhciBfd2FybmluZyA9IHJlcXVpcmUoJ3dhcm5pbmcnKTtcblxudmFyIF93YXJuaW5nMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX3dhcm5pbmcpO1xuXG52YXIgX2V4dHJhY3RQYXRoID0gcmVxdWlyZSgnLi9leHRyYWN0UGF0aCcpO1xuXG52YXIgX2V4dHJhY3RQYXRoMiA9IF9pbnRlcm9wUmVxdWlyZURlZmF1bHQoX2V4dHJhY3RQYXRoKTtcblxuZnVuY3Rpb24gcGFyc2VQYXRoKHBhdGgpIHtcbiAgdmFyIHBhdGhuYW1lID0gX2V4dHJhY3RQYXRoMlsnZGVmYXVsdCddKHBhdGgpO1xuICB2YXIgc2VhcmNoID0gJyc7XG4gIHZhciBoYXNoID0gJyc7XG5cbiAgcHJvY2Vzcy5lbnYuTk9ERV9FTlYgIT09ICdwcm9kdWN0aW9uJyA/IF93YXJuaW5nMlsnZGVmYXVsdCddKHBhdGggPT09IHBhdGhuYW1lLCAnQSBwYXRoIG11c3QgYmUgcGF0aG5hbWUgKyBzZWFyY2ggKyBoYXNoIG9ubHksIG5vdCBhIGZ1bGx5IHF1YWxpZmllZCBVUkwgbGlrZSBcIiVzXCInLCBwYXRoKSA6IHVuZGVmaW5lZDtcblxuICB2YXIgaGFzaEluZGV4ID0gcGF0aG5hbWUuaW5kZXhPZignIycpO1xuICBpZiAoaGFzaEluZGV4ICE9PSAtMSkge1xuICAgIGhhc2ggPSBwYXRobmFtZS5zdWJzdHJpbmcoaGFzaEluZGV4KTtcbiAgICBwYXRobmFtZSA9IHBhdGhuYW1lLnN1YnN0cmluZygwLCBoYXNoSW5kZXgpO1xuICB9XG5cbiAgdmFyIHNlYXJjaEluZGV4ID0gcGF0aG5hbWUuaW5kZXhPZignPycpO1xuICBpZiAoc2VhcmNoSW5kZXggIT09IC0xKSB7XG4gICAgc2VhcmNoID0gcGF0aG5hbWUuc3Vic3RyaW5nKHNlYXJjaEluZGV4KTtcbiAgICBwYXRobmFtZSA9IHBhdGhuYW1lLnN1YnN0cmluZygwLCBzZWFyY2hJbmRleCk7XG4gIH1cblxuICBpZiAocGF0aG5hbWUgPT09ICcnKSBwYXRobmFtZSA9ICcvJztcblxuICByZXR1cm4ge1xuICAgIHBhdGhuYW1lOiBwYXRobmFtZSxcbiAgICBzZWFyY2g6IHNlYXJjaCxcbiAgICBoYXNoOiBoYXNoXG4gIH07XG59XG5cbmV4cG9ydHNbJ2RlZmF1bHQnXSA9IHBhcnNlUGF0aDtcbm1vZHVsZS5leHBvcnRzID0gZXhwb3J0c1snZGVmYXVsdCddOyIsIid1c2Ugc3RyaWN0JztcblxuZXhwb3J0cy5fX2VzTW9kdWxlID0gdHJ1ZTtcblxuZnVuY3Rpb24gX2ludGVyb3BSZXF1aXJlRGVmYXVsdChvYmopIHsgcmV0dXJuIG9iaiAmJiBvYmouX19lc01vZHVsZSA/IG9iaiA6IHsgJ2RlZmF1bHQnOiBvYmogfTsgfVxuXG52YXIgX3dhcm5pbmcgPSByZXF1aXJlKCd3YXJuaW5nJyk7XG5cbnZhciBfd2FybmluZzIgPSBfaW50ZXJvcFJlcXVpcmVEZWZhdWx0KF93YXJuaW5nKTtcblxuZnVuY3Rpb24gcnVuVHJhbnNpdGlvbkhvb2soaG9vaywgbG9jYXRpb24sIGNhbGxiYWNrKSB7XG4gIHZhciByZXN1bHQgPSBob29rKGxvY2F0aW9uLCBjYWxsYmFjayk7XG5cbiAgaWYgKGhvb2subGVuZ3RoIDwgMikge1xuICAgIC8vIEFzc3VtZSB0aGUgaG9vayBydW5zIHN5bmNocm9ub3VzbHkgYW5kIGF1dG9tYXRpY2FsbHlcbiAgICAvLyBjYWxsIHRoZSBjYWxsYmFjayB3aXRoIHRoZSByZXR1cm4gdmFsdWUuXG4gICAgY2FsbGJhY2socmVzdWx0KTtcbiAgfSBlbHNlIHtcbiAgICBwcm9jZXNzLmVudi5OT0RFX0VOViAhPT0gJ3Byb2R1Y3Rpb24nID8gX3dhcm5pbmcyWydkZWZhdWx0J10ocmVzdWx0ID09PSB1bmRlZmluZWQsICdZb3Ugc2hvdWxkIG5vdCBcInJldHVyblwiIGluIGEgdHJhbnNpdGlvbiBob29rIHdpdGggYSBjYWxsYmFjayBhcmd1bWVudDsgY2FsbCB0aGUgY2FsbGJhY2sgaW5zdGVhZCcpIDogdW5kZWZpbmVkO1xuICB9XG59XG5cbmV4cG9ydHNbJ2RlZmF1bHQnXSA9IHJ1blRyYW5zaXRpb25Ib29rO1xubW9kdWxlLmV4cG9ydHMgPSBleHBvcnRzWydkZWZhdWx0J107IiwiLyoqXG4gKiBDb3B5cmlnaHQgMjAxMy0yMDE1LCBGYWNlYm9vaywgSW5jLlxuICogQWxsIHJpZ2h0cyByZXNlcnZlZC5cbiAqXG4gKiBUaGlzIHNvdXJjZSBjb2RlIGlzIGxpY2Vuc2VkIHVuZGVyIHRoZSBCU0Qtc3R5bGUgbGljZW5zZSBmb3VuZCBpbiB0aGVcbiAqIExJQ0VOU0UgZmlsZSBpbiB0aGUgcm9vdCBkaXJlY3Rvcnkgb2YgdGhpcyBzb3VyY2UgdHJlZS4gQW4gYWRkaXRpb25hbCBncmFudFxuICogb2YgcGF0ZW50IHJpZ2h0cyBjYW4gYmUgZm91bmQgaW4gdGhlIFBBVEVOVFMgZmlsZSBpbiB0aGUgc2FtZSBkaXJlY3RvcnkuXG4gKi9cblxuJ3VzZSBzdHJpY3QnO1xuXG4vKipcbiAqIFVzZSBpbnZhcmlhbnQoKSB0byBhc3NlcnQgc3RhdGUgd2hpY2ggeW91ciBwcm9ncmFtIGFzc3VtZXMgdG8gYmUgdHJ1ZS5cbiAqXG4gKiBQcm92aWRlIHNwcmludGYtc3R5bGUgZm9ybWF0IChvbmx5ICVzIGlzIHN1cHBvcnRlZCkgYW5kIGFyZ3VtZW50c1xuICogdG8gcHJvdmlkZSBpbmZvcm1hdGlvbiBhYm91dCB3aGF0IGJyb2tlIGFuZCB3aGF0IHlvdSB3ZXJlXG4gKiBleHBlY3RpbmcuXG4gKlxuICogVGhlIGludmFyaWFudCBtZXNzYWdlIHdpbGwgYmUgc3RyaXBwZWQgaW4gcHJvZHVjdGlvbiwgYnV0IHRoZSBpbnZhcmlhbnRcbiAqIHdpbGwgcmVtYWluIHRvIGVuc3VyZSBsb2dpYyBkb2VzIG5vdCBkaWZmZXIgaW4gcHJvZHVjdGlvbi5cbiAqL1xuXG52YXIgaW52YXJpYW50ID0gZnVuY3Rpb24oY29uZGl0aW9uLCBmb3JtYXQsIGEsIGIsIGMsIGQsIGUsIGYpIHtcbiAgaWYgKHByb2Nlc3MuZW52Lk5PREVfRU5WICE9PSAncHJvZHVjdGlvbicpIHtcbiAgICBpZiAoZm9ybWF0ID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignaW52YXJpYW50IHJlcXVpcmVzIGFuIGVycm9yIG1lc3NhZ2UgYXJndW1lbnQnKTtcbiAgICB9XG4gIH1cblxuICBpZiAoIWNvbmRpdGlvbikge1xuICAgIHZhciBlcnJvcjtcbiAgICBpZiAoZm9ybWF0ID09PSB1bmRlZmluZWQpIHtcbiAgICAgIGVycm9yID0gbmV3IEVycm9yKFxuICAgICAgICAnTWluaWZpZWQgZXhjZXB0aW9uIG9jY3VycmVkOyB1c2UgdGhlIG5vbi1taW5pZmllZCBkZXYgZW52aXJvbm1lbnQgJyArXG4gICAgICAgICdmb3IgdGhlIGZ1bGwgZXJyb3IgbWVzc2FnZSBhbmQgYWRkaXRpb25hbCBoZWxwZnVsIHdhcm5pbmdzLidcbiAgICAgICk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHZhciBhcmdzID0gW2EsIGIsIGMsIGQsIGUsIGZdO1xuICAgICAgdmFyIGFyZ0luZGV4ID0gMDtcbiAgICAgIGVycm9yID0gbmV3IEVycm9yKFxuICAgICAgICBmb3JtYXQucmVwbGFjZSgvJXMvZywgZnVuY3Rpb24oKSB7IHJldHVybiBhcmdzW2FyZ0luZGV4KytdOyB9KVxuICAgICAgKTtcbiAgICAgIGVycm9yLm5hbWUgPSAnSW52YXJpYW50IFZpb2xhdGlvbic7XG4gICAgfVxuXG4gICAgZXJyb3IuZnJhbWVzVG9Qb3AgPSAxOyAvLyB3ZSBkb24ndCBjYXJlIGFib3V0IGludmFyaWFudCdzIG93biBmcmFtZVxuICAgIHRocm93IGVycm9yO1xuICB9XG59O1xuXG5tb2R1bGUuZXhwb3J0cyA9IGludmFyaWFudDtcbiIsIi8qKlxuICogQ29weXJpZ2h0IDIwMTQtMjAxNSwgRmFjZWJvb2ssIEluYy5cbiAqIEFsbCByaWdodHMgcmVzZXJ2ZWQuXG4gKlxuICogVGhpcyBzb3VyY2UgY29kZSBpcyBsaWNlbnNlZCB1bmRlciB0aGUgQlNELXN0eWxlIGxpY2Vuc2UgZm91bmQgaW4gdGhlXG4gKiBMSUNFTlNFIGZpbGUgaW4gdGhlIHJvb3QgZGlyZWN0b3J5IG9mIHRoaXMgc291cmNlIHRyZWUuIEFuIGFkZGl0aW9uYWwgZ3JhbnRcbiAqIG9mIHBhdGVudCByaWdodHMgY2FuIGJlIGZvdW5kIGluIHRoZSBQQVRFTlRTIGZpbGUgaW4gdGhlIHNhbWUgZGlyZWN0b3J5LlxuICovXG5cbid1c2Ugc3RyaWN0JztcblxuLyoqXG4gKiBTaW1pbGFyIHRvIGludmFyaWFudCBidXQgb25seSBsb2dzIGEgd2FybmluZyBpZiB0aGUgY29uZGl0aW9uIGlzIG5vdCBtZXQuXG4gKiBUaGlzIGNhbiBiZSB1c2VkIHRvIGxvZyBpc3N1ZXMgaW4gZGV2ZWxvcG1lbnQgZW52aXJvbm1lbnRzIGluIGNyaXRpY2FsXG4gKiBwYXRocy4gUmVtb3ZpbmcgdGhlIGxvZ2dpbmcgY29kZSBmb3IgcHJvZHVjdGlvbiBlbnZpcm9ubWVudHMgd2lsbCBrZWVwIHRoZVxuICogc2FtZSBsb2dpYyBhbmQgZm9sbG93IHRoZSBzYW1lIGNvZGUgcGF0aHMuXG4gKi9cblxudmFyIHdhcm5pbmcgPSBmdW5jdGlvbigpIHt9O1xuXG5pZiAocHJvY2Vzcy5lbnYuTk9ERV9FTlYgIT09ICdwcm9kdWN0aW9uJykge1xuICB3YXJuaW5nID0gZnVuY3Rpb24oY29uZGl0aW9uLCBmb3JtYXQsIGFyZ3MpIHtcbiAgICB2YXIgbGVuID0gYXJndW1lbnRzLmxlbmd0aDtcbiAgICBhcmdzID0gbmV3IEFycmF5KGxlbiA+IDIgPyBsZW4gLSAyIDogMCk7XG4gICAgZm9yICh2YXIga2V5ID0gMjsga2V5IDwgbGVuOyBrZXkrKykge1xuICAgICAgYXJnc1trZXkgLSAyXSA9IGFyZ3VtZW50c1trZXldO1xuICAgIH1cbiAgICBpZiAoZm9ybWF0ID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihcbiAgICAgICAgJ2B3YXJuaW5nKGNvbmRpdGlvbiwgZm9ybWF0LCAuLi5hcmdzKWAgcmVxdWlyZXMgYSB3YXJuaW5nICcgK1xuICAgICAgICAnbWVzc2FnZSBhcmd1bWVudCdcbiAgICAgICk7XG4gICAgfVxuXG4gICAgaWYgKGZvcm1hdC5sZW5ndGggPCAxMCB8fCAoL15bc1xcV10qJC8pLnRlc3QoZm9ybWF0KSkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFxuICAgICAgICAnVGhlIHdhcm5pbmcgZm9ybWF0IHNob3VsZCBiZSBhYmxlIHRvIHVuaXF1ZWx5IGlkZW50aWZ5IHRoaXMgJyArXG4gICAgICAgICd3YXJuaW5nLiBQbGVhc2UsIHVzZSBhIG1vcmUgZGVzY3JpcHRpdmUgZm9ybWF0IHRoYW46ICcgKyBmb3JtYXRcbiAgICAgICk7XG4gICAgfVxuXG4gICAgaWYgKCFjb25kaXRpb24pIHtcbiAgICAgIHZhciBhcmdJbmRleCA9IDA7XG4gICAgICB2YXIgbWVzc2FnZSA9ICdXYXJuaW5nOiAnICtcbiAgICAgICAgZm9ybWF0LnJlcGxhY2UoLyVzL2csIGZ1bmN0aW9uKCkge1xuICAgICAgICAgIHJldHVybiBhcmdzW2FyZ0luZGV4KytdO1xuICAgICAgICB9KTtcbiAgICAgIGlmICh0eXBlb2YgY29uc29sZSAhPT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgICAgY29uc29sZS5lcnJvcihtZXNzYWdlKTtcbiAgICAgIH1cbiAgICAgIHRyeSB7XG4gICAgICAgIC8vIFRoaXMgZXJyb3Igd2FzIHRocm93biBhcyBhIGNvbnZlbmllbmNlIHNvIHRoYXQgeW91IGNhbiB1c2UgdGhpcyBzdGFja1xuICAgICAgICAvLyB0byBmaW5kIHRoZSBjYWxsc2l0ZSB0aGF0IGNhdXNlZCB0aGlzIHdhcm5pbmcgdG8gZmlyZS5cbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKG1lc3NhZ2UpO1xuICAgICAgfSBjYXRjaCh4KSB7fVxuICAgIH1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSB3YXJuaW5nO1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZWZyZXNoKCkge1xuICAgIHdpbmRvdy5sb2NhdGlvbi5yZWxvYWQoKTtcbiAgfVxuXG4gIGdldE1lc3NhZ2UoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuc2lnbmVkSW4pIHtcbiAgICAgIHJldHVybiBpbnRlcnBvbGF0ZShcbiAgICAgICAgZ2V0dGV4dChcIllvdSBoYXZlIHNpZ25lZCBpbiBhcyAlKHVzZXJuYW1lKXMuIFBsZWFzZSByZWZyZXNoIHRoZSBwYWdlIGJlZm9yZSBjb250aW51aW5nLlwiKSxcbiAgICAgICAge3VzZXJuYW1lOiB0aGlzLnByb3BzLnNpZ25lZEluLnVzZXJuYW1lfSwgdHJ1ZSk7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnNpZ25lZE91dCkge1xuICAgICAgcmV0dXJuIGludGVycG9sYXRlKFxuICAgICAgICBnZXR0ZXh0KFwiJSh1c2VybmFtZSlzLCB5b3UgaGF2ZSBiZWVuIHNpZ25lZCBvdXQuIFBsZWFzZSByZWZyZXNoIHRoZSBwYWdlIGJlZm9yZSBjb250aW51aW5nLlwiKSxcbiAgICAgICAge3VzZXJuYW1lOiB0aGlzLnByb3BzLnVzZXIudXNlcm5hbWV9LCB0cnVlKTtcbiAgICB9XG4gIH1cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuc2lnbmVkSW4gfHwgdGhpcy5wcm9wcy5zaWduZWRPdXQpIHtcbiAgICAgIHJldHVybiBcImF1dGgtbWVzc2FnZSBzaG93XCI7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBcImF1dGgtbWVzc2FnZVwiO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPXt0aGlzLmdldENsYXNzTmFtZSgpfT5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj57dGhpcy5nZXRNZXNzYWdlKCl9PC9wPlxuICAgICAgICA8cD5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLWRlZmF1bHRcIlxuICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5yZWZyZXNofT5cbiAgICAgICAgICAgIHtnZXR0ZXh0KFwiUmVsb2FkIHBhZ2VcIil9XG4gICAgICAgICAgPC9idXR0b24+IDxzcGFuIGNsYXNzTmFtZT1cImhpZGRlbi14cyBoaWRkZW4tc20gdGV4dC1tdXRlZFwiPlxuICAgICAgICAgICAge2dldHRleHQoXCJvciBwcmVzcyBGNSBrZXkuXCIpfVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9wPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4ge1xuICAgIHVzZXI6IHN0YXRlLmF1dGgudXNlcixcbiAgICBzaWduZWRJbjogc3RhdGUuYXV0aC5zaWduZWRJbixcbiAgICBzaWduZWRPdXQ6IHN0YXRlLmF1dGguc2lnbmVkT3V0XG4gIH07XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuY29uc3QgQkFTRV9VUkwgPSAkKCdiYXNlJykuYXR0cignaHJlZicpICsgJ3VzZXItYXZhdGFyLyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0U3JjKCkge1xuICAgIGxldCBzaXplID0gdGhpcy5wcm9wcy5zaXplIHx8IDEwMDsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG4gICAgbGV0IHVybCA9IEJBU0VfVVJMO1xuXG4gICAgaWYgKHRoaXMucHJvcHMudXNlciAmJiB0aGlzLnByb3BzLnVzZXIuaWQpIHtcbiAgICAgIC8vIGp1c3QgYXZhdGFyIGhhc2gsIHNpemUgYW5kIHVzZXIgaWRcbiAgICAgIHVybCArPSB0aGlzLnByb3BzLnVzZXIuYXZhdGFyX2hhc2ggKyAnLycgKyBzaXplICsgJy8nICsgdGhpcy5wcm9wcy51c2VyLmlkICsgJy5wbmcnO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBqdXN0IGFwcGVuZCBhdmF0YXIgc2l6ZSB0byBmaWxlIHRvIHByb2R1Y2Ugbm8tYXZhdGFyIHBsYWNlaG9sZGVyXG4gICAgICB1cmwgKz0gc2l6ZSArICcucG5nJztcbiAgICB9XG5cbiAgICByZXR1cm4gdXJsO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGltZyBzcmM9e3RoaXMuZ2V0U3JjKCl9XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lPXt0aGlzLnByb3BzLmNsYXNzTmFtZSB8fCAndXNlci1hdmF0YXInfVxuICAgICAgICAgICAgICAgIHRpdGxlPXtnZXR0ZXh0KFwiVXNlciBhdmF0YXJcIil9Lz47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRSZWFzb25NZXNzYWdlKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBpZiAodGhpcy5wcm9wcy5tZXNzYWdlLmh0bWwpIHtcbiAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImxlYWRcIlxuICAgICAgICAgICAgICAgICAgZGFuZ2Vyb3VzbHlTZXRJbm5lckhUTUw9e3tfX2h0bWw6IHRoaXMucHJvcHMubWVzc2FnZS5odG1sfX0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8cCBjbGFzc05hbWU9XCJsZWFkXCI+e3RoaXMucHJvcHMubWVzc2FnZS5wbGFpbn08L3A+O1xuICAgIH1cbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG5cbiAgZ2V0RXhwaXJhdGlvbk1lc3NhZ2UoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuZXhwaXJlcykge1xuICAgICAgaWYgKHRoaXMucHJvcHMuZXhwaXJlcy5pc0FmdGVyKG1vbWVudCgpKSkge1xuICAgICAgICByZXR1cm4gaW50ZXJwb2xhdGUoXG4gICAgICAgICAgZ2V0dGV4dChcIlRoaXMgYmFuIGV4cGlyZXMgJShleHBpcmVzX29uKXMuXCIpLFxuICAgICAgICAgIHsnZXhwaXJlc19vbic6IHRoaXMucHJvcHMuZXhwaXJlcy5mcm9tTm93KCl9LFxuICAgICAgICAgIHRydWUpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIGdldHRleHQoXCJUaGlzIGJhbiBoYXMgZXhwaXJlZC5cIik7XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiVGhpcyBiYW4gaXMgcGVybWFuZW50LlwiKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UgcGFnZS1lcnJvciBwYWdlLWVycm9yLWJhbm5lZFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLXBhbmVsXCI+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPmhpZ2hsaWdodF9vZmY8L3NwYW4+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWJvZHlcIj5cbiAgICAgICAgICAgIHt0aGlzLmdldFJlYXNvbk1lc3NhZ2UoKX1cbiAgICAgICAgICAgIDxwIGNsYXNzTmFtZT1cIm1lc3NhZ2UtZm9vdG5vdGVcIj5cbiAgICAgICAgICAgICAge3RoaXMuZ2V0RXhwaXJhdGlvbk1lc3NhZ2UoKX1cbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBMb2FkZXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvbG9hZGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIEJ1dHRvbiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICBsZXQgY2xhc3NOYW1lID0gJ2J0biAnICsgdGhpcy5wcm9wcy5jbGFzc05hbWU7XG4gICAgbGV0IGRpc2FibGVkID0gdGhpcy5wcm9wcy5kaXNhYmxlZDtcblxuICAgIGlmICh0aGlzLnByb3BzLmxvYWRpbmcpIHtcbiAgICAgIGNsYXNzTmFtZSArPSAnIGJ0bi1sb2FkaW5nJztcbiAgICAgIGRpc2FibGVkID0gdHJ1ZTtcbiAgICB9XG5cbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxidXR0b24gdHlwZT17dGhpcy5wcm9wcy5vbkNsaWNrID8gJ2J1dHRvbicgOiAnc3VibWl0J31cbiAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9e2NsYXNzTmFtZX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17ZGlzYWJsZWR9XG4gICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5wcm9wcy5vbkNsaWNrfT5cbiAgICAgIHt0aGlzLnByb3BzLmNoaWxkcmVufVxuICAgICAge3RoaXMucHJvcHMubG9hZGluZyA/IDxMb2FkZXIgLz4gOiBudWxsfVxuICAgIDwvYnV0dG9uPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cblxuQnV0dG9uLmRlZmF1bHRQcm9wcyA9IHtcbiAgY2xhc3NOYW1lOiBcImJ0bi1kZWZhdWx0XCIsXG5cbiAgdHlwZTogXCJzdWJtaXRcIixcblxuICBsb2FkaW5nOiBmYWxzZSxcbiAgZGlzYWJsZWQ6IGZhbHNlLFxuXG4gIG9uQ2xpY2s6IG51bGxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEF2YXRhciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdmF0YXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5jb25zdCBCQVNFX1VSTCA9ICQoJ2Jhc2UnKS5hdHRyKCdocmVmJykgKyAndXNlci1hdmF0YXInO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICBnZXRBdmF0YXJTaXplKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnVwbG9hZCkge1xuICAgICAgcmV0dXJuIHRoaXMucHJvcHMub3B0aW9ucy5jcm9wX3RtcC5zaXplO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gdGhpcy5wcm9wcy5vcHRpb25zLmNyb3Bfb3JnLnNpemU7XG4gICAgfVxuICB9XG5cbiAgZ2V0QXZhdGFyU2VjcmV0KCkge1xuICAgIGlmICh0aGlzLnByb3BzLnVwbG9hZCkge1xuICAgICAgcmV0dXJuIHRoaXMucHJvcHMub3B0aW9ucy5jcm9wX3RtcC5zZWNyZXQ7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLnByb3BzLm9wdGlvbnMuY3JvcF9vcmcuc2VjcmV0O1xuICAgIH1cbiAgfVxuXG4gIGdldEF2YXRhckhhc2goKSB7XG4gICAgcmV0dXJuIHRoaXMucHJvcHMudXBsb2FkIHx8IHRoaXMucHJvcHMudXNlci5hdmF0YXJfaGFzaDtcbiAgfVxuXG4gIGdldEltYWdlUGF0aCgpIHtcbiAgICByZXR1cm4gW1xuICAgICAgQkFTRV9VUkwsXG4gICAgICB0aGlzLmdldEF2YXRhclNlY3JldCgpICsgJzonICsgdGhpcy5nZXRBdmF0YXJIYXNoKCksXG4gICAgICB0aGlzLnByb3BzLnVzZXIuaWQgKyAnLnBuZydcbiAgICBdLmpvaW4oJy8nKTtcbiAgfVxuXG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIGxldCBjcm9waXQgPSAkKCcuY3JvcC1mb3JtJyk7XG4gICAgY3JvcGl0LndpZHRoKHRoaXMuZ2V0QXZhdGFyU2l6ZSgpKTtcblxuICAgIGNyb3BpdC5jcm9waXQoe1xuICAgICAgJ3dpZHRoJzogdGhpcy5nZXRBdmF0YXJTaXplKCksXG4gICAgICAnaGVpZ2h0JzogdGhpcy5nZXRBdmF0YXJTaXplKCksXG4gICAgICAnaW1hZ2VTdGF0ZSc6IHtcbiAgICAgICAgJ3NyYyc6IHRoaXMuZ2V0SW1hZ2VQYXRoKClcbiAgICAgIH0sXG4gICAgICBvbkltYWdlTG9hZGVkOiAoKSA9PiB7XG4gICAgICAgIGlmICh0aGlzLnByb3BzLnVwbG9hZCkge1xuICAgICAgICAgIC8vIGNlbnRlciB1cGxvYWRlZCBpbWFnZVxuICAgICAgICAgIGxldCB6b29tTGV2ZWwgPSBjcm9waXQuY3JvcGl0KCd6b29tJyk7XG4gICAgICAgICAgbGV0IGltYWdlU2l6ZSA9IGNyb3BpdC5jcm9waXQoJ2ltYWdlU2l6ZScpO1xuXG4gICAgICAgICAgLy8gaXMgaXQgd2lkZXIgdGhhbiB0YWxsZXI/XG4gICAgICAgICAgaWYgKGltYWdlU2l6ZS53aWR0aCA+IGltYWdlU2l6ZS5oZWlnaHQpIHtcbiAgICAgICAgICAgIGxldCBkaXNwbGF5ZWRXaWR0aCA9IChpbWFnZVNpemUud2lkdGggKiB6b29tTGV2ZWwpO1xuICAgICAgICAgICAgbGV0IG9mZnNldFggPSAoZGlzcGxheWVkV2lkdGggLSB0aGlzLmdldEF2YXRhclNpemUoKSkgLyAtMjtcblxuICAgICAgICAgICAgY3JvcGl0LmNyb3BpdCgnb2Zmc2V0Jywge1xuICAgICAgICAgICAgICAneCc6IG9mZnNldFgsXG4gICAgICAgICAgICAgICd5JzogMFxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfSBlbHNlIGlmIChpbWFnZVNpemUud2lkdGggPCBpbWFnZVNpemUuaGVpZ2h0KSB7XG4gICAgICAgICAgICBsZXQgZGlzcGxheWVkSGVpZ2h0ID0gKGltYWdlU2l6ZS5oZWlnaHQgKiB6b29tTGV2ZWwpO1xuICAgICAgICAgICAgbGV0IG9mZnNldFkgPSAoZGlzcGxheWVkSGVpZ2h0IC0gdGhpcy5nZXRBdmF0YXJTaXplKCkpIC8gLTI7XG5cbiAgICAgICAgICAgIGNyb3BpdC5jcm9waXQoJ29mZnNldCcsIHtcbiAgICAgICAgICAgICAgJ3gnOiAwLFxuICAgICAgICAgICAgICAneSc6IG9mZnNldFlcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAvLyB1c2UgcHJlc2VydmVkIGNyb3BcbiAgICAgICAgICBsZXQgY3JvcCA9IHRoaXMucHJvcHMub3B0aW9ucy5jcm9wX29yZy5jcm9wO1xuICAgICAgICAgIGlmIChjcm9wKSB7XG4gICAgICAgICAgICBjcm9waXQuY3JvcGl0KCd6b29tJywgY3JvcC56b29tKTtcbiAgICAgICAgICAgIGNyb3BpdC5jcm9waXQoJ29mZnNldCcsIHtcbiAgICAgICAgICAgICAgJ3gnOiBjcm9wLngsXG4gICAgICAgICAgICAgICd5JzogY3JvcC55XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIGNvbXBvbmVudFdpbGxVbm1vdW50KCkge1xuICAgICQoJy5jcm9wLWZvcm0nKS5jcm9waXQoJ2Rpc2FibGUnKTtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgY3JvcEF2YXRhciA9ICgpID0+IHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRpbmcpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdpc0xvYWRpbmcnOiB0cnVlXG4gICAgfSk7XG5cbiAgICBsZXQgYXZhdGFyVHlwZSA9IHRoaXMucHJvcHMudXBsb2FkID8gJ2Nyb3BfdG1wJyA6ICdjcm9wX29yZyc7XG4gICAgbGV0IGNyb3BpdCA9ICQoJy5jcm9wLWZvcm0nKTtcblxuICAgIGFqYXgucG9zdCh0aGlzLnByb3BzLnVzZXIuYXBpX3VybC5hdmF0YXIsIHtcbiAgICAgICdhdmF0YXInOiBhdmF0YXJUeXBlLFxuICAgICAgJ2Nyb3AnOiB7XG4gICAgICAgICdvZmZzZXQnOiBjcm9waXQuY3JvcGl0KCdvZmZzZXQnKSxcbiAgICAgICAgJ3pvb20nOiBjcm9waXQuY3JvcGl0KCd6b29tJylcbiAgICAgIH1cbiAgICB9KS50aGVuKChkYXRhKSA9PiB7XG4gICAgICB0aGlzLnByb3BzLm9uQ29tcGxldGUoZGF0YS5hdmF0YXJfaGFzaCwgZGF0YS5vcHRpb25zKTtcbiAgICAgIHNuYWNrYmFyLnN1Y2Nlc3MoZGF0YS5kZXRhaWwpO1xuICAgIH0sIChyZWplY3Rpb24pID0+IHtcbiAgICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMucHJvcHMuc2hvd0Vycm9yKHJlamVjdGlvbik7XG4gICAgICB9XG4gICAgfSk7XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keSBtb2RhbC1hdmF0YXItY3JvcFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNyb3AtZm9ybVwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY3JvcGl0LWltYWdlLXByZXZpZXdcIj48L2Rpdj5cbiAgICAgICAgICA8aW5wdXQgdHlwZT1cInJhbmdlXCIgY2xhc3NOYW1lPVwiY3JvcGl0LWltYWdlLXpvb20taW5wdXRcIiAvPlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1mb290ZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wtbWQtNiBjb2wtbWQtb2Zmc2V0LTNcIj5cblxuICAgICAgICAgIDxCdXR0b24gb25DbGljaz17dGhpcy5jcm9wQXZhdGFyfVxuICAgICAgICAgICAgICAgICAgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIj5cbiAgICAgICAgICAgIHt0aGlzLnByb3BzLnVwbG9hZCA/IGdldHRleHQoXCJTZXQgYXZhdGFyXCIpXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgOiBnZXR0ZXh0KFwiQ3JvcCBpbWFnZVwiKX1cbiAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICAgIDxCdXR0b24gb25DbGljaz17dGhpcy5wcm9wcy5zaG93SW5kZXh9XG4gICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4tZGVmYXVsdCBidG4tYmxvY2tcIj5cbiAgICAgICAgICAgIHtnZXR0ZXh0KFwiQ2FuY2VsXCIpfVxuICAgICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGJhdGNoIGZyb20gJ21pc2Fnby91dGlscy9iYXRjaCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgR2FsbGVyeUl0ZW0gZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHNlbGVjdCA9ICgpID0+IHtcbiAgICB0aGlzLnByb3BzLnNlbGVjdCh0aGlzLnByb3BzLmltYWdlKTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuc2VsZWN0aW9uID09PSB0aGlzLnByb3BzLmltYWdlKSB7XG4gICAgICBpZiAodGhpcy5wcm9wcy5kaXNhYmxlZCkge1xuICAgICAgICByZXR1cm4gJ2J0biBidG4tYXZhdGFyIGJ0bi1kaXNhYmxlZCBhdmF0YXItc2VsZWN0ZWQnO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuICdidG4gYnRuLWF2YXRhciBhdmF0YXItc2VsZWN0ZWQnO1xuICAgICAgfVxuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5kaXNhYmxlZCkge1xuICAgICAgcmV0dXJuICdidG4gYnRuLWF2YXRhciBidG4tZGlzYWJsZWQnO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gJ2J0biBidG4tYXZhdGFyJztcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8YnV0dG9uIHR5cGU9XCJidXR0b25cIlxuICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzc05hbWUoKX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5wcm9wcy5kaXNhYmxlZH1cbiAgICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnNlbGVjdH0+XG4gICAgICA8aW1nIHNyYz17bWlzYWdvLmdldCgnTUVESUFfVVJMJykgKyB0aGlzLnByb3BzLmltYWdlfSAvPlxuICAgIDwvYnV0dG9uPlxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIEdhbGxlcnkgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImF2YXRhcnMtZ2FsbGVyeVwiPlxuICAgICAgPGgzPnt0aGlzLnByb3BzLm5hbWV9PC9oMz5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJhdmF0YXJzLWdhbGxlcnktaW1hZ2VzXCI+XG4gICAgICAgIHtiYXRjaCh0aGlzLnByb3BzLmltYWdlcywgNCwgbnVsbCkubWFwKChyb3csIGkpID0+IHtcbiAgICAgICAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJyb3dcIiBrZXk9e2l9PlxuICAgICAgICAgICAge3Jvdy5tYXAoKGl0ZW0sIGkpID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiY29sLXhzLTNcIiBrZXk9e2l9PlxuICAgICAgICAgICAgICAgIHtpdGVtID8gPEdhbGxlcnlJdGVtIGltYWdlPXtpdGVtfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnByb3BzLmRpc2FibGVkfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNlbGVjdD17dGhpcy5wcm9wcy5zZWxlY3R9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc2VsZWN0aW9uPXt0aGlzLnByb3BzLnNlbGVjdGlvbn0gLz5cbiAgICAgICAgICAgICAgICAgICAgICA6IDxkaXYgY2xhc3NOYW1lPVwiYmxhbmstYXZhdGFyXCIgLz59XG4gICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgfSl9XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIH0pfVxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnc2VsZWN0aW9uJzogbnVsbCxcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHNlbGVjdCA9IChpbWFnZSkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgc2VsZWN0aW9uOiBpbWFnZVxuICAgIH0pO1xuICB9O1xuXG4gIHNhdmUgPSAoKSA9PiB7XG4gICAgaWYgKHRoaXMuc3RhdGUuaXNMb2FkaW5nKSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAnaXNMb2FkaW5nJzogdHJ1ZVxuICAgIH0pO1xuXG4gICAgYWpheC5wb3N0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLmF2YXRhciwge1xuICAgICAgYXZhdGFyOiAnZ2FsbGVyaWVzJyxcbiAgICAgIGltYWdlOiB0aGlzLnN0YXRlLnNlbGVjdGlvblxuICAgIH0pLnRoZW4oKHJlc3BvbnNlKSA9PiB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlXG4gICAgICB9KTtcblxuICAgICAgc25hY2tiYXIuc3VjY2VzcyhyZXNwb25zZS5kZXRhaWwpO1xuICAgICAgdGhpcy5wcm9wcy5vbkNvbXBsZXRlKHJlc3BvbnNlLmF2YXRhcl9oYXNoLCByZXNwb25zZS5vcHRpb25zKTtcbiAgICB9LCAocmVqZWN0aW9uKSA9PiB7XG4gICAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAwKSB7XG4gICAgICAgIHNuYWNrYmFyLmVycm9yKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgICAnaXNMb2FkaW5nJzogZmFsc2VcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLnByb3BzLnNob3dFcnJvcihyZWplY3Rpb24pO1xuICAgICAgfVxuICAgIH0pO1xuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHkgbW9kYWwtYXZhdGFyLWdhbGxlcnlcIj5cblxuICAgICAgICB7dGhpcy5wcm9wcy5vcHRpb25zLmdhbGxlcmllcy5tYXAoKGl0ZW0sIGkpID0+IHtcbiAgICAgICAgICByZXR1cm4gPEdhbGxlcnkgbmFtZT17aXRlbS5uYW1lfVxuICAgICAgICAgICAgICAgICAgICAgICAgICBpbWFnZXM9e2l0ZW0uaW1hZ2VzfVxuICAgICAgICAgICAgICAgICAgICAgICAgICBzZWxlY3Rpb249e3RoaXMuc3RhdGUuc2VsZWN0aW9ufVxuICAgICAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHNlbGVjdD17dGhpcy5zZWxlY3R9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIGtleT17aX0gLz47XG4gICAgICAgIH0pfVxuXG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtZm9vdGVyXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicm93XCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wtbWQtNiBjb2wtbWQtb2Zmc2V0LTNcIj5cblxuICAgICAgICAgICAgPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnNhdmV9XG4gICAgICAgICAgICAgICAgICAgIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17IXRoaXMuc3RhdGUuc2VsZWN0aW9ufVxuICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIj5cbiAgICAgICAgICAgICAge3RoaXMuc3RhdGUuc2VsZWN0aW9uID8gZ2V0dGV4dChcIlNhdmUgY2hvaWNlXCIpXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA6IGdldHRleHQoXCJTZWxlY3QgYXZhdGFyXCIpfVxuICAgICAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgICAgICAgIDxCdXR0b24gb25DbGljaz17dGhpcy5wcm9wcy5zaG93SW5kZXh9XG4gICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuLWRlZmF1bHQgYnRuLWJsb2NrXCI+XG4gICAgICAgICAgICAgIHtnZXR0ZXh0KFwiQ2FuY2VsXCIpfVxuICAgICAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgQXZhdGFyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2F2YXRhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBMb2FkZXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvbG9hZGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnaXNMb2FkaW5nJzogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgY2FsbEFwaShhdmF0YXJUeXBlKSB7XG4gICAgaWYgKHRoaXMuc3RhdGUuaXNMb2FkaW5nKSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAnaXNMb2FkaW5nJzogdHJ1ZVxuICAgIH0pO1xuXG4gICAgYWpheC5wb3N0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLmF2YXRhciwge1xuICAgICAgYXZhdGFyOiBhdmF0YXJUeXBlXG4gICAgfSkudGhlbigocmVzcG9uc2UpID0+IHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnaXNMb2FkaW5nJzogZmFsc2VcbiAgICAgIH0pO1xuXG4gICAgICBzbmFja2Jhci5zdWNjZXNzKHJlc3BvbnNlLmRldGFpbCk7XG4gICAgICB0aGlzLnByb3BzLm9uQ29tcGxldGUocmVzcG9uc2UuYXZhdGFyX2hhc2gsIHJlc3BvbnNlLm9wdGlvbnMpO1xuICAgIH0sIChyZWplY3Rpb24pID0+IHtcbiAgICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMucHJvcHMuc2hvd0Vycm9yKHJlamVjdGlvbik7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHNldEdyYXZhdGFyID0gKCkgPT4ge1xuICAgIHRoaXMuY2FsbEFwaSgnZ3JhdmF0YXInKTtcbiAgfTtcblxuICBzZXRHZW5lcmF0ZWQgPSAoKSA9PiB7XG4gICAgdGhpcy5jYWxsQXBpKCdnZW5lcmF0ZWQnKTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRHcmF2YXRhckJ1dHRvbigpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5vcHRpb25zLmdyYXZhdGFyKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnNldEdyYXZhdGFyfVxuICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9jayBidG4tYXZhdGFyLWdyYXZhdGFyXCI+XG4gICAgICAgIHtnZXR0ZXh0KFwiRG93bmxvYWQgbXkgR3JhdmF0YXJcIil9XG4gICAgICA8L0J1dHRvbj47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICBnZXRDcm9wQnV0dG9uKCkge1xuICAgIGlmICh0aGlzLnByb3BzLm9wdGlvbnMuY3JvcF9vcmcpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8QnV0dG9uIG9uQ2xpY2s9e3RoaXMucHJvcHMuc2hvd0Nyb3B9XG4gICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuLWRlZmF1bHQgYnRuLWJsb2NrIGJ0bi1hdmF0YXItY3JvcFwiPlxuICAgICAgICB7Z2V0dGV4dChcIlJlLWNyb3AgdXBsb2FkZWQgaW1hZ2VcIil9XG4gICAgICA8L0J1dHRvbj47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICBnZXRVcGxvYWRCdXR0b24oKSB7XG4gICAgaWYgKHRoaXMucHJvcHMub3B0aW9ucy51cGxvYWQpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8QnV0dG9uIG9uQ2xpY2s9e3RoaXMucHJvcHMuc2hvd1VwbG9hZH1cbiAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4tZGVmYXVsdCBidG4tYmxvY2sgYnRuLWF2YXRhci11cGxvYWRcIj5cbiAgICAgICAge2dldHRleHQoXCJVcGxvYWQgbmV3IGltYWdlXCIpfVxuICAgICAgPC9CdXR0b24+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgZ2V0R2FsbGVyeUJ1dHRvbigpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5vcHRpb25zLmdhbGxlcmllcykge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxCdXR0b24gb25DbGljaz17dGhpcy5wcm9wcy5zaG93R2FsbGVyeX1cbiAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4tZGVmYXVsdCBidG4tYmxvY2sgYnRuLWF2YXRhci1nYWxsZXJ5XCI+XG4gICAgICAgIHtnZXR0ZXh0KFwiUGljayBhdmF0YXIgZnJvbSBnYWxsZXJ5XCIpfVxuICAgICAgPC9CdXR0b24+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgZ2V0QXZhdGFyUHJldmlldygpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRpbmcpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImF2YXRhci1wcmV2aWV3IHByZXZpZXctbG9hZGluZ1wiPlxuICAgICAgICA8QXZhdGFyIHVzZXI9e3RoaXMucHJvcHMudXNlcn0gc2l6ZT1cIjIwMFwiIC8+XG4gICAgICAgIDxMb2FkZXIgLz5cbiAgICAgIDwvZGl2PjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImF2YXRhci1wcmV2aWV3XCI+XG4gICAgICAgIDxBdmF0YXIgdXNlcj17dGhpcy5wcm9wcy51c2VyfSBzaXplPVwiMjAwXCIgLz5cbiAgICAgIDwvZGl2PjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5IG1vZGFsLWF2YXRhci1pbmRleFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wtbWQtNVwiPlxuXG4gICAgICAgICAge3RoaXMuZ2V0QXZhdGFyUHJldmlldygpfVxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1tZC03XCI+XG5cbiAgICAgICAgICB7dGhpcy5nZXRHcmF2YXRhckJ1dHRvbigpfVxuXG4gICAgICAgICAgPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnNldEdlbmVyYXRlZH1cbiAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9jayBidG4tYXZhdGFyLWdlbmVyYXRlXCI+XG4gICAgICAgICAgICB7Z2V0dGV4dChcIkdlbmVyYXRlIG15IGluZGl2aWR1YWwgYXZhdGFyXCIpfVxuICAgICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICAgICAge3RoaXMuZ2V0Q3JvcEJ1dHRvbigpfVxuICAgICAgICAgIHt0aGlzLmdldFVwbG9hZEJ1dHRvbigpfVxuICAgICAgICAgIHt0aGlzLmdldEdhbGxlcnlCdXR0b24oKX1cblxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBBdmF0YXJJbmRleCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL2luZGV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQXZhdGFyQ3JvcCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL2Nyb3AnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBBdmF0YXJVcGxvYWQgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci91cGxvYWQnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBBdmF0YXJHYWxsZXJ5IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2NoYW5nZS1hdmF0YXIvZ2FsbGVyeSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IExvYWRlciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9tb2RhbC1sb2FkZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCB7IHVwZGF0ZUF2YXRhciB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy91c2Vycyc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgQ2hhbmdlQXZhdGFyRXJyb3IgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRFcnJvclJlYXNvbigpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5yZWFzb24pIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8cCBkYW5nZXJvdXNseVNldElubmVySFRNTD17e19faHRtbDogdGhpcy5wcm9wcy5yZWFzb259fSAvPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keVwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWljb25cIj5cbiAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgIHJlbW92ZV9jaXJjbGVfb3V0bGluZVxuICAgICAgICA8L3NwYW4+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1ib2R5XCI+XG4gICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICB7dGhpcy5wcm9wcy5tZXNzYWdlfVxuICAgICAgICA8L3A+XG4gICAgICAgIHt0aGlzLmdldEVycm9yUmVhc29uKCl9XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIGFqYXguZ2V0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLmF2YXRhcikudGhlbigob3B0aW9ucykgPT4ge1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICdjb21wb25lbnQnOiBBdmF0YXJJbmRleCxcbiAgICAgICAgJ29wdGlvbnMnOiBvcHRpb25zLFxuICAgICAgICAnZXJyb3InOiBudWxsXG4gICAgICB9KTtcbiAgICB9LCAocmVqZWN0aW9uKSA9PiB7XG4gICAgICB0aGlzLnNob3dFcnJvcihyZWplY3Rpb24pO1xuICAgIH0pO1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBzaG93RXJyb3IgPSAoZXJyb3IpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIGVycm9yXG4gICAgfSk7XG4gIH07XG5cbiAgc2hvd0luZGV4ID0gKCkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ2NvbXBvbmVudCc6IEF2YXRhckluZGV4XG4gICAgfSk7XG4gIH07XG5cbiAgc2hvd1VwbG9hZCA9ICgpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdjb21wb25lbnQnOiBBdmF0YXJVcGxvYWRcbiAgICB9KTtcbiAgfTtcblxuICBzaG93Q3JvcCA9ICgpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdjb21wb25lbnQnOiBBdmF0YXJDcm9wXG4gICAgfSk7XG4gIH07XG5cbiAgc2hvd0dhbGxlcnkgPSAoKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAnY29tcG9uZW50JzogQXZhdGFyR2FsbGVyeVxuICAgIH0pO1xuICB9O1xuXG4gIGNvbXBsZXRlRmxvdyA9IChhdmF0YXJIYXNoLCBvcHRpb25zKSA9PiB7XG4gICAgc3RvcmUuZGlzcGF0Y2godXBkYXRlQXZhdGFyKHRoaXMucHJvcHMudXNlciwgYXZhdGFySGFzaCkpO1xuXG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAnY29tcG9uZW50JzogQXZhdGFySW5kZXgsXG4gICAgICBvcHRpb25zXG4gICAgfSk7XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgZ2V0Qm9keSgpIHtcbiAgICBpZiAodGhpcy5zdGF0ZSkge1xuICAgICAgaWYgKHRoaXMuc3RhdGUuZXJyb3IpIHtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgICByZXR1cm4gPENoYW5nZUF2YXRhckVycm9yIG1lc3NhZ2U9e3RoaXMuc3RhdGUuZXJyb3IuZGV0YWlsfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJlYXNvbj17dGhpcy5zdGF0ZS5lcnJvci5yZWFzb259IC8+O1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgICByZXR1cm4gPHRoaXMuc3RhdGUuY29tcG9uZW50IG9wdGlvbnM9e3RoaXMuc3RhdGUub3B0aW9uc31cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgb25Db21wbGV0ZT17dGhpcy5jb21wbGV0ZUZsb3d9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc2hvd0Vycm9yPXt0aGlzLnNob3dFcnJvcn1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzaG93SW5kZXg9e3RoaXMuc2hvd0luZGV4fVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNob3dDcm9wPXt0aGlzLnNob3dDcm9wfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNob3dVcGxvYWQ9e3RoaXMuc2hvd1VwbG9hZH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzaG93R2FsbGVyeT17dGhpcy5zaG93R2FsbGVyeX0gLz47XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8TG9hZGVyIC8+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICBpZiAodGhpcy5zdGF0ZSAmJiB0aGlzLnN0YXRlLmVycm9yKSB7XG4gICAgICByZXR1cm4gXCJtb2RhbC1kaWFsb2cgbW9kYWwtbWVzc2FnZSBtb2RhbC1jaGFuZ2UtYXZhdGFyXCI7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBcIm1vZGFsLWRpYWxvZyBtb2RhbC1jaGFuZ2UtYXZhdGFyXCI7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9e3RoaXMuZ2V0Q2xhc3NOYW1lKCl9XG4gICAgICAgICAgICAgICAgcm9sZT1cImRvY3VtZW50XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWNvbnRlbnRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1oZWFkZXJcIj5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJjbG9zZVwiIGRhdGEtZGlzbWlzcz1cIm1vZGFsXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtbGFiZWw9e2dldHRleHQoXCJDbG9zZVwiKX0+XG4gICAgICAgICAgICA8c3BhbiBhcmlhLWhpZGRlbj1cInRydWVcIj4mdGltZXM7PC9zcGFuPlxuICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgIDxoNCBjbGFzc05hbWU9XCJtb2RhbC10aXRsZVwiPntnZXR0ZXh0KFwiQ2hhbmdlIHlvdXIgYXZhdGFyXCIpfTwvaDQ+XG4gICAgICAgIDwvZGl2PlxuXG4gICAgICAgIHt0aGlzLmdldEJvZHkoKX1cblxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4ge1xuICAgICd1c2VyJzogc3RhdGUuYXV0aC51c2VyXG4gIH07XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEF2YXRhckNyb3AgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9jcm9wJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQnV0dG9uIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2J1dHRvbic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBmaWxlU2l6ZSBmcm9tICdtaXNhZ28vdXRpbHMvZmlsZS1zaXplJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnaW1hZ2UnOiBudWxsLFxuICAgICAgJ3ByZXZpZXcnOiBudWxsLFxuICAgICAgJ3Byb2dyZXNzJzogMCxcbiAgICAgICd1cGxvYWRlZCc6IG51bGwsXG4gICAgfTtcbiAgfVxuXG4gIHZhbGlkYXRlRmlsZShpbWFnZSkge1xuICAgIGlmIChpbWFnZS5zaXplID4gdGhpcy5wcm9wcy5vcHRpb25zLnVwbG9hZC5saW1pdCkge1xuICAgICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCJTZWxlY3RlZCBmaWxlIGlzIHRvbyBiaWcuICglKGZpbGVzaXplKXMpXCIpLCB7XG4gICAgICAgICdmaWxlc2l6ZSc6IGZpbGVTaXplKGltYWdlLnNpemUpXG4gICAgICB9LCB0cnVlKTtcbiAgICB9XG5cbiAgICBsZXQgaW52YWxpZFR5cGVNc2cgPSBnZXR0ZXh0KFwiU2VsZWN0ZWQgZmlsZSB0eXBlIGlzIG5vdCBzdXBwb3J0ZWQuXCIpO1xuICAgIGlmICh0aGlzLnByb3BzLm9wdGlvbnMudXBsb2FkLmFsbG93ZWRfbWltZV90eXBlcy5pbmRleE9mKGltYWdlLnR5cGUpID09PSAtMSkge1xuICAgICAgcmV0dXJuIGludmFsaWRUeXBlTXNnO1xuICAgIH1cblxuICAgIGxldCBleHRlbnNpb25Gb3VuZCA9IGZhbHNlO1xuICAgIGxldCBsb3dlcmVkRmlsZW5hbWUgPSBpbWFnZS5uYW1lLnRvTG93ZXJDYXNlKCk7XG4gICAgdGhpcy5wcm9wcy5vcHRpb25zLnVwbG9hZC5hbGxvd2VkX2V4dGVuc2lvbnMubWFwKGZ1bmN0aW9uKGV4dGVuc2lvbikge1xuICAgICAgaWYgKGxvd2VyZWRGaWxlbmFtZS5zdWJzdHIoZXh0ZW5zaW9uLmxlbmd0aCAqIC0xKSA9PT0gZXh0ZW5zaW9uKSB7XG4gICAgICAgIGV4dGVuc2lvbkZvdW5kID0gdHJ1ZTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGlmICghZXh0ZW5zaW9uRm91bmQpIHtcbiAgICAgIHJldHVybiBpbnZhbGlkVHlwZU1zZztcbiAgICB9XG5cbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHBpY2tGaWxlID0gKCkgPT4ge1xuICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdhdmF0YXItaGlkZGVuLXVwbG9hZCcpLmNsaWNrKCk7XG4gIH07XG5cbiAgdXBsb2FkRmlsZSA9ICgpID0+IHtcbiAgICBsZXQgaW1hZ2UgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnYXZhdGFyLWhpZGRlbi11cGxvYWQnKS5maWxlc1swXTtcblxuICAgIGxldCB2YWxpZGF0aW9uRXJyb3IgPSB0aGlzLnZhbGlkYXRlRmlsZShpbWFnZSk7XG4gICAgaWYgKHZhbGlkYXRpb25FcnJvcikge1xuICAgICAgc25hY2tiYXIuZXJyb3IodmFsaWRhdGlvbkVycm9yKTtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIGltYWdlLFxuICAgICAgJ3ByZXZpZXcnOiBVUkwuY3JlYXRlT2JqZWN0VVJMKGltYWdlKSxcbiAgICAgICdwcm9ncmVzcyc6IDBcbiAgICB9KTtcblxuICAgIGxldCBkYXRhID0gbmV3IEZvcm1EYXRhKCk7XG4gICAgZGF0YS5hcHBlbmQoJ2F2YXRhcicsICd1cGxvYWQnKTtcbiAgICBkYXRhLmFwcGVuZCgnaW1hZ2UnLCBpbWFnZSk7XG5cbiAgICBhamF4LnVwbG9hZCh0aGlzLnByb3BzLnVzZXIuYXBpX3VybC5hdmF0YXIsIGRhdGEsIChwcm9ncmVzcykgPT4ge1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgIHByb2dyZXNzXG4gICAgICB9KTtcbiAgICB9KS50aGVuKChkYXRhKSA9PiB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ29wdGlvbnMnOiBkYXRhLm9wdGlvbnMsXG4gICAgICAgICd1cGxvYWRlZCc6IGRhdGEuZGV0YWlsXG4gICAgICB9KTtcbiAgICAgIHNuYWNrYmFyLmluZm8oZ2V0dGV4dChcIllvdXIgaW1hZ2UgaGFzIGJlZW4gdXBsb2FkZWQgYW5kIHlvdSBtYXkgbm93IGNyb3AgaXQuXCIpKTtcbiAgICB9LCAocmVqZWN0aW9uKSA9PiB7XG4gICAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAwKSB7XG4gICAgICAgIHNuYWNrYmFyLmVycm9yKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG4gICAgICAgICAgJ2ltYWdlJzogbnVsbCxcbiAgICAgICAgICAncHJvZ3Jlc3MnOiAwXG4gICAgICAgIH0pXG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLnByb3BzLnNob3dFcnJvcihyZWplY3Rpb24pO1xuICAgICAgfVxuICAgIH0pO1xuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIGdldFVwbG9hZFJlcXVpcmVtZW50cyhvcHRpb25zKSB7XG4gICAgbGV0IGV4dGVuc2lvbnMgPSBvcHRpb25zLmFsbG93ZWRfZXh0ZW5zaW9ucy5tYXAoZnVuY3Rpb24oZXh0ZW5zaW9uKSB7XG4gICAgICByZXR1cm4gZXh0ZW5zaW9uLnN1YnN0cigxKTtcbiAgICB9KTtcblxuICAgIHJldHVybiBpbnRlcnBvbGF0ZShnZXR0ZXh0KFwiJShmaWxlcylzIGZpbGVzIHNtYWxsZXIgdGhhbiAlKGxpbWl0KXNcIiksIHtcbiAgICAgICAgJ2ZpbGVzJzogZXh0ZW5zaW9ucy5qb2luKCcsICcpLFxuICAgICAgICAnbGltaXQnOiBmaWxlU2l6ZShvcHRpb25zLmxpbWl0KVxuICAgICAgfSwgdHJ1ZSk7XG4gIH1cblxuICBnZXRVcGxvYWRCdXR0b24oKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHkgbW9kYWwtYXZhdGFyLXVwbG9hZFwiPlxuICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1waWNrLWZpbGVcIlxuICAgICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMucGlja0ZpbGV9PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgaW5wdXRcbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICB7Z2V0dGV4dChcIlNlbGVjdCBmaWxlXCIpfVxuICAgICAgICA8L0J1dHRvbj5cbiAgICAgICAgPHAgY2xhc3NOYW1lPVwidGV4dC1tdXRlZFwiPlxuICAgICAgICAgIHt0aGlzLmdldFVwbG9hZFJlcXVpcmVtZW50cyh0aGlzLnByb3BzLm9wdGlvbnMudXBsb2FkKX1cbiAgICAgICAgPC9wPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG5cbiAgZ2V0VXBsb2FkUHJvZ3Jlc3NMYWJlbCgpIHtcbiAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIiUocHJvZ3Jlc3MpcyAlIGNvbXBsZXRlXCIpLCB7XG4gICAgICAgICdwcm9ncmVzcyc6IHRoaXMuc3RhdGUucHJvZ3Jlc3NcbiAgICAgIH0sIHRydWUpO1xuICB9XG5cbiAgZ2V0VXBsb2FkUHJvZ3Jlc3MoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHkgbW9kYWwtYXZhdGFyLXVwbG9hZFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVwbG9hZC1wcm9ncmVzc1wiPlxuICAgICAgICAgIDxpbWcgc3JjPXt0aGlzLnN0YXRlLnByZXZpZXd9IC8+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInByb2dyZXNzXCI+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInByb2dyZXNzLWJhclwiIHJvbGU9XCJwcm9ncmVzc2JhclwiXG4gICAgICAgICAgICAgICAgIGFyaWEtdmFsdWVub3c9XCJ7dGhpcy5zdGF0ZS5wcm9ncmVzc31cIlxuICAgICAgICAgICAgICAgICBhcmlhLXZhbHVlbWluPVwiMFwiIGFyaWEtdmFsdWVtYXg9XCIxMDBcIlxuICAgICAgICAgICAgICAgICBzdHlsZT17e3dpZHRoOiB0aGlzLnN0YXRlLnByb2dyZXNzICsgJyUnfX0+XG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInNyLW9ubHlcIj57dGhpcy5nZXRVcGxvYWRQcm9ncmVzc0xhYmVsKCl9PC9zcGFuPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG5cbiAgcmVuZGVyVXBsb2FkKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdj5cbiAgICAgIDxpbnB1dCB0eXBlPVwiZmlsZVwiXG4gICAgICAgICAgICAgaWQ9XCJhdmF0YXItaGlkZGVuLXVwbG9hZFwiXG4gICAgICAgICAgICAgY2xhc3NOYW1lPVwiaGlkZGVuLWZpbGUtdXBsb2FkXCJcbiAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy51cGxvYWRGaWxlfSAvPlxuICAgICAge3RoaXMuc3RhdGUuaW1hZ2UgPyB0aGlzLmdldFVwbG9hZFByb2dyZXNzKClcbiAgICAgICAgICAgICAgICAgICAgICAgIDogdGhpcy5nZXRVcGxvYWRCdXR0b24oKX1cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtZm9vdGVyXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLW1kLTYgY29sLW1kLW9mZnNldC0zXCI+XG5cbiAgICAgICAgICA8QnV0dG9uIG9uQ2xpY2s9e3RoaXMucHJvcHMuc2hvd0luZGV4fVxuICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9eyEhdGhpcy5zdGF0ZS5pbWFnZX1cbiAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAge2dldHRleHQoXCJDYW5jZWxcIil9XG4gICAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxuXG4gIHJlbmRlckNyb3AoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8QXZhdGFyQ3JvcCBvcHRpb25zPXt0aGlzLnN0YXRlLm9wdGlvbnN9XG4gICAgICAgICAgICAgICAgICAgICAgIHVzZXI9e3RoaXMucHJvcHMudXNlcn1cbiAgICAgICAgICAgICAgICAgICAgICAgdXBsb2FkPXt0aGlzLnN0YXRlLnVwbG9hZGVkfVxuICAgICAgICAgICAgICAgICAgICAgICBvbkNvbXBsZXRlPXt0aGlzLnByb3BzLm9uQ29tcGxldGV9XG4gICAgICAgICAgICAgICAgICAgICAgIHNob3dFcnJvcj17dGhpcy5wcm9wcy5zaG93RXJyb3J9XG4gICAgICAgICAgICAgICAgICAgICAgIHNob3dJbmRleD17dGhpcy5wcm9wcy5zaG93SW5kZXh9IC8+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiAodGhpcy5zdGF0ZS51cGxvYWRlZCA/IHRoaXMucmVuZGVyQ3JvcCgpXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDogdGhpcy5yZW5kZXJVcGxvYWQoKSk7XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgaXNWYWxpZGF0ZWQoKSB7XG4gICAgcmV0dXJuIHR5cGVvZiB0aGlzLnByb3BzLnZhbGlkYXRpb24gIT09IFwidW5kZWZpbmVkXCI7XG4gIH1cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICAgbGV0IGNsYXNzTmFtZSA9ICdmb3JtLWdyb3VwJztcbiAgICBpZiAodGhpcy5pc1ZhbGlkYXRlZCgpKSB7XG4gICAgICBjbGFzc05hbWUgKz0gJyBoYXMtZmVlZGJhY2snO1xuICAgICAgaWYgKHRoaXMucHJvcHMudmFsaWRhdGlvbiA9PT0gbnVsbCkge1xuICAgICAgICBjbGFzc05hbWUgKz0gJyBoYXMtc3VjY2Vzcyc7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjbGFzc05hbWUgKz0gJyBoYXMtZXJyb3InO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gY2xhc3NOYW1lO1xuICB9XG5cbiAgZ2V0RmVlZGJhY2soKSB7XG4gICAgaWYgKHRoaXMucHJvcHMudmFsaWRhdGlvbikge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiaGVscC1ibG9jayBlcnJvcnNcIj5cbiAgICAgICAge3RoaXMucHJvcHMudmFsaWRhdGlvbi5tYXAoKGVycm9yLCBpKSA9PiB7XG4gICAgICAgICAgcmV0dXJuIDxwIGtleT17dGhpcy5wcm9wcy5mb3IgKyAnRmVlZGJhY2tJdGVtJyArIGl9PntlcnJvcn08L3A+O1xuICAgICAgICB9KX1cbiAgICAgIDwvZGl2PjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIGdldEZlZWRiYWNrSWNvbigpIHtcbiAgICBpZiAodGhpcy5pc1ZhbGlkYXRlZCgpKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvbiBmb3JtLWNvbnRyb2wtZmVlZGJhY2tcIlxuICAgICAgICAgICAgICAgICAgIGFyaWEtaGlkZGVuPVwidHJ1ZVwiIGtleT17dGhpcy5wcm9wcy5mb3IgKyAnRmVlZGJhY2tJY29uJ30+XG4gICAgICAgIHt0aGlzLnByb3BzLnZhbGlkYXRpb24gPyAnY2xlYXInIDogJ2NoZWNrJ31cbiAgICAgIDwvc3Bhbj47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICBnZXRGZWVkYmFja0Rlc2NyaXB0aW9uKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWRhdGVkKCkpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8c3BhbiBpZD17dGhpcy5wcm9wcy5mb3IgKyAnX3N0YXR1cyd9IGNsYXNzTmFtZT1cInNyLW9ubHlcIj5cbiAgICAgICAge3RoaXMucHJvcHMudmFsaWRhdGlvbiA/IGdldHRleHQoJyhlcnJvciknKSA6IGdldHRleHQoJyhzdWNjZXNzKScpfVxuICAgICAgPC9zcGFuPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIGdldEhlbHBUZXh0KCkge1xuICAgIGlmICh0aGlzLnByb3BzLmhlbHBUZXh0KSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPHAgY2xhc3NOYW1lPVwiaGVscC1ibG9ja1wiPnt0aGlzLnByb3BzLmhlbHBUZXh0fTwvcD47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzc05hbWUoKX0+XG4gICAgICA8bGFiZWwgY2xhc3NOYW1lPXsnY29udHJvbC1sYWJlbCAnICsgKHRoaXMucHJvcHMubGFiZWxDbGFzcyB8fCAnJyl9XG4gICAgICAgICAgICAgaHRtbEZvcj17dGhpcy5wcm9wcy5mb3IgfHwgJyd9PlxuICAgICAgICB7dGhpcy5wcm9wcy5sYWJlbCArICc6J31cbiAgICAgIDwvbGFiZWw+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT17dGhpcy5wcm9wcy5jb250cm9sQ2xhc3MgfHwgJyd9PlxuICAgICAgICB7dGhpcy5wcm9wcy5jaGlsZHJlbn1cbiAgICAgICAge3RoaXMuZ2V0RmVlZGJhY2tJY29uKCl9XG4gICAgICAgIHt0aGlzLmdldEZlZWRiYWNrRGVzY3JpcHRpb24oKX1cbiAgICAgICAge3RoaXMuZ2V0RmVlZGJhY2soKX1cbiAgICAgICAge3RoaXMuZ2V0SGVscFRleHQoKX1cbiAgICAgICAge3RoaXMucHJvcHMuZXh0cmEgfHwgbnVsbH1cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyByZXF1aXJlZCB9IGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcblxubGV0IHZhbGlkYXRlUmVxdWlyZWQgPSByZXF1aXJlZCgpO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHZhbGlkYXRlKCkge1xuICAgIGxldCBlcnJvcnMgPSB7fTtcbiAgICBpZiAoIXRoaXMuc3RhdGUudmFsaWRhdG9ycykge1xuICAgICAgcmV0dXJuIGVycm9ycztcbiAgICB9XG5cbiAgICBsZXQgdmFsaWRhdG9ycyA9IHtcbiAgICAgIHJlcXVpcmVkOiB0aGlzLnN0YXRlLnZhbGlkYXRvcnMucmVxdWlyZWQgfHwgdGhpcy5zdGF0ZS52YWxpZGF0b3JzLFxuICAgICAgb3B0aW9uYWw6IHRoaXMuc3RhdGUudmFsaWRhdG9ycy5vcHRpb25hbCB8fCB7fVxuICAgIH07XG5cbiAgICBsZXQgdmFsaWRhdGVkRmllbGRzID0gW107XG5cbiAgICAvLyBhZGQgcmVxdWlyZWQgZmllbGRzIHRvIHZhbGlkYXRpb25cbiAgICBmb3IgKGxldCBuYW1lIGluIHZhbGlkYXRvcnMucmVxdWlyZWQpIHtcbiAgICAgIGlmICh2YWxpZGF0b3JzLnJlcXVpcmVkLmhhc093blByb3BlcnR5KG5hbWUpICYmXG4gICAgICAgICAgdmFsaWRhdG9ycy5yZXF1aXJlZFtuYW1lXSkge1xuICAgICAgICB2YWxpZGF0ZWRGaWVsZHMucHVzaChuYW1lKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBhZGQgb3B0aW9uYWwgZmllbGRzIHRvIHZhbGlkYXRpb25cbiAgICBmb3IgKGxldCBuYW1lIGluIHZhbGlkYXRvcnMub3B0aW9uYWwpIHtcbiAgICAgIGlmICh2YWxpZGF0b3JzLm9wdGlvbmFsLmhhc093blByb3BlcnR5KG5hbWUpICYmXG4gICAgICAgICAgdmFsaWRhdG9ycy5vcHRpb25hbFtuYW1lXSkge1xuICAgICAgICB2YWxpZGF0ZWRGaWVsZHMucHVzaChuYW1lKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyB2YWxpZGF0ZSBmaWVsZHMgdmFsdWVzXG4gICAgZm9yIChsZXQgaSBpbiB2YWxpZGF0ZWRGaWVsZHMpIHtcbiAgICAgIGxldCBuYW1lID0gdmFsaWRhdGVkRmllbGRzW2ldO1xuICAgICAgbGV0IGZpZWxkRXJyb3JzID0gdGhpcy52YWxpZGF0ZUZpZWxkKG5hbWUsIHRoaXMuc3RhdGVbbmFtZV0pO1xuXG4gICAgICBpZiAoZmllbGRFcnJvcnMgPT09IG51bGwpIHtcbiAgICAgICAgZXJyb3JzW25hbWVdID0gbnVsbDtcbiAgICAgIH0gZWxzZSBpZiAoZmllbGRFcnJvcnMpIHtcbiAgICAgICAgZXJyb3JzW25hbWVdID0gZmllbGRFcnJvcnM7XG4gICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIGVycm9ycztcbiAgfVxuXG4gIGlzVmFsaWQoKSB7XG4gICAgbGV0IGVycm9ycyA9IHRoaXMudmFsaWRhdGUoKTtcbiAgICBmb3IgKGxldCBmaWVsZCBpbiBlcnJvcnMpIHtcbiAgICAgIGlmIChlcnJvcnMuaGFzT3duUHJvcGVydHkoZmllbGQpKSB7XG4gICAgICAgIGlmIChlcnJvcnNbZmllbGRdICE9PSBudWxsKSB7XG4gICAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICB2YWxpZGF0ZUZpZWxkKG5hbWUsIHZhbHVlKSB7XG4gICAgbGV0IGVycm9ycyA9IFtdO1xuICAgIGlmICghdGhpcy5zdGF0ZS52YWxpZGF0b3JzKSB7XG4gICAgICByZXR1cm4gZXJyb3JzO1xuICAgIH1cblxuICAgIGxldCB2YWxpZGF0b3JzID0ge1xuICAgICAgcmVxdWlyZWQ6ICh0aGlzLnN0YXRlLnZhbGlkYXRvcnMucmVxdWlyZWQgfHwgdGhpcy5zdGF0ZS52YWxpZGF0b3JzKVtuYW1lXSxcbiAgICAgIG9wdGlvbmFsOiAodGhpcy5zdGF0ZS52YWxpZGF0b3JzLm9wdGlvbmFsIHx8IHt9KVtuYW1lXVxuICAgIH07XG5cbiAgICBsZXQgcmVxdWlyZWRFcnJvciA9IHZhbGlkYXRlUmVxdWlyZWQodmFsdWUpIHx8IGZhbHNlO1xuXG4gICAgaWYgKHZhbGlkYXRvcnMucmVxdWlyZWQpIHtcbiAgICAgIGlmIChyZXF1aXJlZEVycm9yKSB7XG4gICAgICAgIGVycm9ycyA9IFtyZXF1aXJlZEVycm9yXTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGZvciAobGV0IGkgaW4gdmFsaWRhdG9ycy5yZXF1aXJlZCkge1xuICAgICAgICAgIGxldCB2YWxpZGF0aW9uRXJyb3IgPSB2YWxpZGF0b3JzLnJlcXVpcmVkW2ldKHZhbHVlKTtcbiAgICAgICAgICBpZiAodmFsaWRhdGlvbkVycm9yKSB7XG4gICAgICAgICAgICBlcnJvcnMucHVzaCh2YWxpZGF0aW9uRXJyb3IpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuXG4gICAgICByZXR1cm4gZXJyb3JzLmxlbmd0aCA/IGVycm9ycyA6IG51bGw7XG4gICAgfSBlbHNlIGlmIChyZXF1aXJlZEVycm9yID09PSBmYWxzZSAmJiB2YWxpZGF0b3JzLm9wdGlvbmFsKSB7XG4gICAgICBmb3IgKGxldCBpIGluIHZhbGlkYXRvcnMub3B0aW9uYWwpIHtcbiAgICAgICAgbGV0IHZhbGlkYXRpb25FcnJvciA9IHZhbGlkYXRvcnMub3B0aW9uYWxbaV0odmFsdWUpO1xuICAgICAgICBpZiAodmFsaWRhdGlvbkVycm9yKSB7XG4gICAgICAgICAgZXJyb3JzLnB1c2godmFsaWRhdGlvbkVycm9yKTtcbiAgICAgICAgfVxuICAgICAgfVxuXG4gICAgICByZXR1cm4gZXJyb3JzLmxlbmd0aCA/IGVycm9ycyA6IG51bGw7XG4gICAgfVxuXG4gICAgcmV0dXJuIGZhbHNlOyAvLyBmYWxzZSA9PT0gZmllbGQgd2Fzbid0IHZhbGlkYXRlZFxuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBiaW5kSW5wdXQgPSAobmFtZSkgPT4ge1xuICAgIHJldHVybiAoZXZlbnQpID0+IHtcbiAgICAgIGxldCBuZXdTdGF0ZSA9IHtcbiAgICAgICAgW25hbWVdOiBldmVudC50YXJnZXQudmFsdWVcbiAgICAgIH07XG5cbiAgICAgIGxldCBmb3JtRXJyb3JzID0gdGhpcy5zdGF0ZS5lcnJvcnMgfHwge307XG4gICAgICBmb3JtRXJyb3JzW25hbWVdID0gdGhpcy52YWxpZGF0ZUZpZWxkKG5hbWUsIG5ld1N0YXRlW25hbWVdKTtcbiAgICAgIG5ld1N0YXRlLmVycm9ycyA9IGZvcm1FcnJvcnM7XG5cbiAgICAgIHRoaXMuc2V0U3RhdGUobmV3U3RhdGUpO1xuICAgIH1cbiAgfTtcblxuICBjbGVhbigpIHtcbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICBoYW5kbGVTdWNjZXNzKHN1Y2Nlc3MpIHtcbiAgICByZXR1cm47XG4gIH1cblxuICBoYW5kbGVFcnJvcihyZWplY3Rpb24pIHtcbiAgICByZXR1cm47XG4gIH1cblxuICBoYW5kbGVTdWJtaXQgPSAoZXZlbnQpID0+IHtcbiAgICAvLyB3ZSBkb24ndCByZWxvYWQgcGFnZSBvbiBzdWJtaXNzaW9uc1xuICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KClcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRpbmcpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBpZiAodGhpcy5jbGVhbigpKSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtpc0xvYWRpbmc6IHRydWV9KTtcbiAgICAgIGxldCBwcm9taXNlID0gdGhpcy5zZW5kKCk7XG5cbiAgICAgIGlmIChwcm9taXNlKSB7XG4gICAgICAgIHByb21pc2UudGhlbigoc3VjY2VzcykgPT4ge1xuICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe2lzTG9hZGluZzogZmFsc2V9KTtcbiAgICAgICAgICB0aGlzLmhhbmRsZVN1Y2Nlc3Moc3VjY2Vzcyk7XG4gICAgICAgIH0sIChyZWplY3Rpb24pID0+IHtcbiAgICAgICAgICB0aGlzLnNldFN0YXRlKHtpc0xvYWRpbmc6IGZhbHNlfSk7XG4gICAgICAgICAgdGhpcy5oYW5kbGVFcnJvcihyZWplY3Rpb24pO1xuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoe2lzTG9hZGluZzogZmFsc2V9KTtcbiAgICAgIH1cbiAgICB9XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBpc0FjdGl2ZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5wYXRoKSB7XG4gICAgICByZXR1cm4gZG9jdW1lbnQubG9jYXRpb24ucGF0aG5hbWUuaW5kZXhPZih0aGlzLnByb3BzLnBhdGgpID09PSAwO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgZ2V0Q2xhc3NOYW1lKCkge1xuICAgIGlmICh0aGlzLmlzQWN0aXZlKCkpIHtcbiAgICAgIHJldHVybiAodGhpcy5wcm9wcy5jbGFzc05hbWUgfHwgJycpICsgJyAnKyAodGhpcy5wcm9wcy5hY3RpdmVDbGFzc05hbWUgfHwgJ2FjdGl2ZScpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gdGhpcy5wcm9wcy5jbGFzc05hbWUgfHwgJyc7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8vIGpzaGludCBpZ25vcmU6c3RhcnRcbiAgICByZXR1cm4gPGxpIGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzc05hbWUoKX0+XG4gICAgICB7dGhpcy5wcm9wcy5jaGlsZHJlbn1cbiAgICA8L2xpPjtcbiAgICAvLyBqc2hpbnQgaWdub3JlOmVuZFxuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT17dGhpcy5wcm9wcy5jbGFzc05hbWUgfHwgXCJsb2FkZXJcIn0+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImxvYWRlci1zcGlubmluZy13aGVlbFwiPjwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IExvYWRlciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9sb2FkZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHkgbW9kYWwtbG9hZGVyXCI+XG4gICAgICA8TG9hZGVyIC8+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuIiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBBdmF0YXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYXZhdGFyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQnV0dG9uIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2J1dHRvbic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEZvcm0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybSc7XG5pbXBvcnQgRm9ybUdyb3VwIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0tZ3JvdXAnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBMb2FkZXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvbG9hZGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgeyBkZWh5ZHJhdGUsIGFkZE5hbWVDaGFuZ2UgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcm5hbWUtaGlzdG9yeSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHsgdXBkYXRlVXNlcm5hbWUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcnMnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCB0aXRsZSBmcm9tICdtaXNhZ28vc2VydmljZXMvcGFnZS10aXRsZSc7XG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuaW1wb3J0ICogYXMgcmFuZG9tIGZyb20gJ21pc2Fnby91dGlscy9yYW5kb20nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCAqIGFzIHZhbGlkYXRvcnMgZnJvbSAnbWlzYWdvL3V0aWxzL3ZhbGlkYXRvcnMnO1xuXG5leHBvcnQgY2xhc3MgQ2hhbmdlVXNlcm5hbWUgZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgdXNlcm5hbWU6ICcnLFxuXG4gICAgICB2YWxpZGF0b3JzOiB7XG4gICAgICAgIHVzZXJuYW1lOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy51c2VybmFtZUNvbnRlbnQoKSxcbiAgICAgICAgICB2YWxpZGF0b3JzLnVzZXJuYW1lTWluTGVuZ3RoKHtcbiAgICAgICAgICAgIHVzZXJuYW1lX2xlbmd0aF9taW46IHByb3BzLm9wdGlvbnMubGVuZ3RoX21pblxuICAgICAgICAgIH0pLFxuICAgICAgICAgIHZhbGlkYXRvcnMudXNlcm5hbWVNYXhMZW5ndGgoe1xuICAgICAgICAgICAgdXNlcm5hbWVfbGVuZ3RoX21heDogcHJvcHMub3B0aW9ucy5sZW5ndGhfbWF4XG4gICAgICAgICAgfSlcbiAgICAgICAgXVxuICAgICAgfSxcblxuICAgICAgaXNMb2FkaW5nOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICBnZXRIZWxwVGV4dCgpIHtcbiAgICBsZXQgcGhyYXNlcyA9IFtdO1xuXG4gICAgaWYgKHRoaXMucHJvcHMub3B0aW9ucy5jaGFuZ2VzX2xlZnQgPiAwKSB7XG4gICAgICBsZXQgbWVzc2FnZSA9IG5nZXR0ZXh0KFxuICAgICAgICBcIllvdSBjYW4gY2hhbmdlIHlvdXIgdXNlcm5hbWUgJShjaGFuZ2VzX2xlZnQpcyBtb3JlIHRpbWUuXCIsXG4gICAgICAgIFwiWW91IGNhbiBjaGFuZ2UgeW91ciB1c2VybmFtZSAlKGNoYW5nZXNfbGVmdClzIG1vcmUgdGltZXMuXCIsXG4gICAgICAgIHRoaXMucHJvcHMub3B0aW9ucy5jaGFuZ2VzX2xlZnQpO1xuXG4gICAgICBwaHJhc2VzLnB1c2goaW50ZXJwb2xhdGUobWVzc2FnZSwge1xuICAgICAgICAnY2hhbmdlc19sZWZ0JzogdGhpcy5wcm9wcy5vcHRpb25zLmNoYW5nZXNfbGVmdFxuICAgICAgfSwgdHJ1ZSkpO1xuICAgIH1cblxuICAgIGlmICh0aGlzLnByb3BzLnVzZXIuYWNsLm5hbWVfY2hhbmdlc19leHBpcmUgPiAwKSB7XG4gICAgICBsZXQgbWVzc2FnZSA9IG5nZXR0ZXh0KFxuICAgICAgICBcIlVzZWQgY2hhbmdlcyByZWRlZW0gYWZ0ZXIgJShuYW1lX2NoYW5nZXNfZXhwaXJlKXMgZGF5LlwiLFxuICAgICAgICBcIlVzZWQgY2hhbmdlcyByZWRlZW0gYWZ0ZXIgJShuYW1lX2NoYW5nZXNfZXhwaXJlKXMgZGF5cy5cIixcbiAgICAgICAgdGhpcy5wcm9wcy51c2VyLmFjbC5uYW1lX2NoYW5nZXNfZXhwaXJlKTtcblxuICAgICAgcGhyYXNlcy5wdXNoKGludGVycG9sYXRlKG1lc3NhZ2UsIHtcbiAgICAgICAgJ25hbWVfY2hhbmdlc19leHBpcmUnOiB0aGlzLnByb3BzLnVzZXIuYWNsLm5hbWVfY2hhbmdlc19leHBpcmVcbiAgICAgIH0sIHRydWUpKTtcbiAgICB9XG5cbiAgICByZXR1cm4gcGhyYXNlcy5sZW5ndGggPyBwaHJhc2VzLmpvaW4oJyAnKSA6IG51bGw7XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBsZXQgZXJyb3JzID0gdGhpcy52YWxpZGF0ZSgpO1xuICAgIGlmIChlcnJvcnMudXNlcm5hbWUpIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGVycm9ycy51c2VybmFtZVswXSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfSBpZiAodGhpcy5zdGF0ZS51c2VybmFtZS50cmltKCkgPT09IHRoaXMucHJvcHMudXNlci51c2VybmFtZSkge1xuICAgICAgc25hY2tiYXIuaW5mbyhnZXR0ZXh0KFwiWW91ciBuZXcgdXNlcm5hbWUgaXMgc2FtZSBhcyBjdXJyZW50IG9uZS5cIikpO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBhamF4LnBvc3QodGhpcy5wcm9wcy51c2VyLmFwaV91cmwudXNlcm5hbWUsIHtcbiAgICAgICd1c2VybmFtZSc6IHRoaXMuc3RhdGUudXNlcm5hbWVcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3Moc3VjY2Vzcykge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ3VzZXJuYW1lJzogJydcbiAgICB9KTtcblxuICAgIHRoaXMucHJvcHMuY29tcGxldGUoc3VjY2Vzcy51c2VybmFtZSwgc3VjY2Vzcy5zbHVnLCBzdWNjZXNzLm9wdGlvbnMpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxmb3JtIG9uU3VibWl0PXt0aGlzLmhhbmRsZVN1Ym1pdH0gY2xhc3NOYW1lPVwiZm9ybS1ob3Jpem9udGFsXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsIHBhbmVsLWRlZmF1bHQgcGFuZWwtZm9ybVwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWhlYWRpbmdcIj5cbiAgICAgICAgICA8aDMgY2xhc3NOYW1lPVwicGFuZWwtdGl0bGVcIj57Z2V0dGV4dChcIkNoYW5nZSB1c2VybmFtZVwiKX08L2gzPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1ib2R5XCI+XG5cbiAgICAgICAgICA8Rm9ybUdyb3VwIGxhYmVsPXtnZXR0ZXh0KFwiTmV3IHVzZXJuYW1lXCIpfSBmb3I9XCJpZF91c2VybmFtZVwiXG4gICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiXG4gICAgICAgICAgICAgICAgICAgICBoZWxwVGV4dD17dGhpcy5nZXRIZWxwVGV4dCgpfT5cbiAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwidGV4dFwiIGlkPVwiaWRfdXNlcm5hbWVcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3VzZXJuYW1lJyl9XG4gICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUudXNlcm5hbWV9IC8+XG4gICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtZm9vdGVyXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLXNtLTggY29sLXNtLW9mZnNldC00XCI+XG5cbiAgICAgICAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeVwiIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICAgICAgICB7Z2V0dGV4dChcIkNoYW5nZSB1c2VybmFtZVwiKX1cbiAgICAgICAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZm9ybT47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgTm9DaGFuZ2VzTGVmdCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldEhlbHBUZXh0KCkge1xuICAgIGlmICh0aGlzLnByb3BzLm9wdGlvbnMubmV4dF9vbikge1xuICAgICAgcmV0dXJuIGludGVycG9sYXRlKFxuICAgICAgICAgIGdldHRleHQoXCJZb3Ugd2lsbCBiZSBhYmxlIHRvIGNoYW5nZSB5b3VyIHVzZXJuYW1lICUobmV4dF9jaGFuZ2Upcy5cIiksXG4gICAgICAgICAgeyduZXh0X2NoYW5nZSc6IHRoaXMucHJvcHMub3B0aW9ucy5uZXh0X29uLmZyb21Ob3coKX0sIHRydWUpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIllvdSBoYXZlIHVzZWQgdXAgYXZhaWxhYmxlIG5hbWUgY2hhbmdlcy5cIik7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJwYW5lbCBwYW5lbC1kZWZhdWx0IHBhbmVsLWZvcm1cIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtaGVhZGluZ1wiPlxuICAgICAgICA8aDMgY2xhc3NOYW1lPVwicGFuZWwtdGl0bGVcIj57Z2V0dGV4dChcIkNoYW5nZSB1c2VybmFtZVwiKX08L2gzPlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWJvZHkgcGFuZWwtbWVzc2FnZS1ib2R5XCI+XG5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWljb25cIj5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICBpbmZvX291dGxpbmVcbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICAgIHtnZXR0ZXh0KFwiWW91IGNhbid0IGNoYW5nZSB5b3VyIHVzZXJuYW1lIGF0IHRoZSBtb21lbnQuXCIpfVxuICAgICAgICAgIDwvcD5cbiAgICAgICAgICA8cCBjbGFzc05hbWU9XCJoZWxwLWJsb2NrXCI+XG4gICAgICAgICAgICB7dGhpcy5nZXRIZWxwVGV4dCgpfVxuICAgICAgICAgIDwvcD5cbiAgICAgICAgPC9kaXY+XG5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBDaGFuZ2VVc2VybmFtZUxvYWRpbmcgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsIHBhbmVsLWRlZmF1bHQgcGFuZWwtZm9ybVwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1oZWFkaW5nXCI+XG4gICAgICAgIDxoMyBjbGFzc05hbWU9XCJwYW5lbC10aXRsZVwiPntnZXR0ZXh0KFwiQ2hhbmdlIHVzZXJuYW1lXCIpfTwvaDM+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtYm9keSBwYW5lbC1ib2R5LWxvYWRpbmdcIj5cblxuICAgICAgICA8TG9hZGVyIGNsYXNzTmFtZT1cImxvYWRlciBsb2FkZXItc3BhY2VkXCIgLz5cblxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFVzZXJuYW1lSGlzdG9yeSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlclVzZXJBdmF0YXIoaXRlbSkge1xuICAgIGlmIChpdGVtLmNoYW5nZWRfYnkpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8YSBocmVmPXtpdGVtLmNoYW5nZWRfYnkuYWJzb2x1dGVfdXJsfSBjbGFzc05hbWU9XCJ1c2VyLWF2YXRhclwiPlxuICAgICAgICA8QXZhdGFyIHVzZXI9e2l0ZW0uY2hhbmdlZF9ieX0gc2l6ZT1cIjEwMFwiIC8+XG4gICAgICA8L2E+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxzcGFuIGNsYXNzTmFtZT1cInVzZXItYXZhdGFyXCI+XG4gICAgICAgIDxBdmF0YXIgc2l6ZT1cIjEwMFwiIC8+XG4gICAgICA8L3NwYW4+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cblxuICByZW5kZXJVc2VybmFtZShpdGVtKSB7XG4gICAgaWYgKGl0ZW0uY2hhbmdlZF9ieSkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxhIGhyZWY9e2l0ZW0uY2hhbmdlZF9ieS5hYnNvbHV0ZV91cmx9IGNsYXNzTmFtZT1cIml0ZW0tdGl0bGVcIj5cbiAgICAgICAge2l0ZW0uY2hhbmdlZF9ieS51c2VybmFtZX1cbiAgICAgIDwvYT47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPHNwYW4gY2xhc3NOYW1lPVwiaXRlbS10aXRsZVwiPlxuICAgICAgICB7aXRlbS5jaGFuZ2VkX2J5X3VzZXJuYW1lfVxuICAgICAgPC9zcGFuPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfVxuICB9XG5cbiAgcmVuZGVySGlzdG9yeSgpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtaGlzdG9yeSB1aS1yZWFkeVwiPlxuICAgICAgPHVsIGNsYXNzTmFtZT1cImxpc3QtZ3JvdXBcIj5cbiAgICAgICAge3RoaXMucHJvcHMuY2hhbmdlcy5tYXAoKGl0ZW0pID0+IHtcbiAgICAgICAgICByZXR1cm4gPGxpIGNsYXNzTmFtZT1cImxpc3QtZ3JvdXAtaXRlbVwiIGtleT17aXRlbS5pZH0+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVzZXJuYW1lLWNoYW5nZS1hdmF0YXJcIj5cbiAgICAgICAgICAgICAge3RoaXMucmVuZGVyVXNlckF2YXRhcihpdGVtKX1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ1c2VybmFtZS1jaGFuZ2UtYXV0aG9yXCI+XG4gICAgICAgICAgICAgIHt0aGlzLnJlbmRlclVzZXJuYW1lKGl0ZW0pfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVzZXJuYW1lLWNoYW5nZVwiPlxuICAgICAgICAgICAgICB7aXRlbS5vbGRfdXNlcm5hbWV9XG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgICAgICBhcnJvd19mb3J3YXJkXG4gICAgICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICAgICAge2l0ZW0ubmV3X3VzZXJuYW1lfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVzZXJuYW1lLWNoYW5nZS1kYXRlXCI+XG4gICAgICAgICAgICAgIDxhYmJyIHRpdGxlPXtpdGVtLmNoYW5nZWRfb24uZm9ybWF0KCdMTEwnKX0+XG4gICAgICAgICAgICAgICAge2l0ZW0uY2hhbmdlZF9vbi5mcm9tTm93KCl9XG4gICAgICAgICAgICAgIDwvYWJicj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvbGk+O1xuICAgICAgICB9KX1cbiAgICAgIDwvdWw+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cblxuICByZW5kZXJFbXB0eUhpc3RvcnkoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInVzZXJuYW1lLWhpc3RvcnkgdWktcmVhZHlcIj5cbiAgICAgIDx1bCBjbGFzc05hbWU9XCJsaXN0LWdyb3VwXCI+XG4gICAgICAgIDxsaSBjbGFzc05hbWU9XCJsaXN0LWdyb3VwLWl0ZW0gZW1wdHktbWVzc2FnZVwiPlxuICAgICAgICAgIHtnZXR0ZXh0KFwiTm8gbmFtZSBjaGFuZ2VzIGhhdmUgYmVlbiByZWNvcmRlZCBmb3IgeW91ciBhY2NvdW50LlwiKX1cbiAgICAgICAgPC9saT5cbiAgICAgIDwvdWw+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cblxuICByZW5kZXJIaXN0b3J5UHJldmlldygpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtaGlzdG9yeSB1aS1wcmV2aWV3XCI+XG4gICAgICA8dWwgY2xhc3NOYW1lPVwibGlzdC1ncm91cFwiPlxuICAgICAgICB7cmFuZG9tLnJhbmdlKDMsIDUpLm1hcCgoaSkgPT4ge1xuICAgICAgICAgIHJldHVybiA8bGkgY2xhc3NOYW1lPVwibGlzdC1ncm91cC1pdGVtXCIga2V5PXtpfT5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtY2hhbmdlLWF2YXRhclwiPlxuICAgICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJ1c2VyLWF2YXRhclwiPlxuICAgICAgICAgICAgICAgIDxBdmF0YXIgc2l6ZT1cIjEwMFwiIC8+XG4gICAgICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ1c2VybmFtZS1jaGFuZ2UtYXV0aG9yXCI+XG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInVpLXByZXZpZXctdGV4dFwiIHN0eWxlPXt7d2lkdGg6IHJhbmRvbS5pbnQoMzAsIDEwMCkgKyBcInB4XCJ9fT4mbmJzcDs8L3NwYW4+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtY2hhbmdlXCI+XG4gICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInVpLXByZXZpZXctdGV4dFwiIHN0eWxlPXt7d2lkdGg6IHJhbmRvbS5pbnQoMzAsIDUwKSArIFwicHhcIn19PiZuYnNwOzwvc3Bhbj5cbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgICAgIGFycm93X2ZvcndhcmRcbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJ1aS1wcmV2aWV3LXRleHRcIiBzdHlsZT17e3dpZHRoOiByYW5kb20uaW50KDMwLCA1MCkgKyBcInB4XCJ9fT4mbmJzcDs8L3NwYW4+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidXNlcm5hbWUtY2hhbmdlLWRhdGVcIj5cbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwidWktcHJldmlldy10ZXh0XCIgc3R5bGU9e3t3aWR0aDogcmFuZG9tLmludCg1MCwgMTAwKSArIFwicHhcIn19PiZuYnNwOzwvc3Bhbj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvbGk+XG4gICAgICAgIH0pfVxuICAgICAgPC91bD5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5pc0xvYWRlZCkge1xuICAgICAgaWYgKHRoaXMucHJvcHMuY2hhbmdlcy5sZW5ndGgpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMucmVuZGVySGlzdG9yeSgpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIHRoaXMucmVuZGVyRW1wdHlIaXN0b3J5KCk7XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLnJlbmRlckhpc3RvcnlQcmV2aWV3KCk7XG4gICAgfVxuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgaXNMb2FkZWQ6IGZhbHNlLFxuICAgICAgb3B0aW9uczogbnVsbFxuICAgIH07XG4gIH1cblxuICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICB0aXRsZS5zZXQoe1xuICAgICAgdGl0bGU6IGdldHRleHQoXCJDaGFuZ2UgdXNlcm5hbWVcIiksXG4gICAgICBwYXJlbnQ6IGdldHRleHQoXCJDaGFuZ2UgeW91ciBvcHRpb25zXCIpXG4gICAgfSk7XG5cbiAgICBQcm9taXNlLmFsbChbXG4gICAgICBhamF4LmdldCh0aGlzLnByb3BzLnVzZXIuYXBpX3VybC51c2VybmFtZSksXG4gICAgICBhamF4LmdldChtaXNhZ28uZ2V0KCdVU0VSTkFNRV9DSEFOR0VTX0FQSScpLCB7dXNlcjogdGhpcy5wcm9wcy51c2VyLmlkfSlcbiAgICBdKS50aGVuKChkYXRhKSA9PiB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgaXNMb2FkZWQ6IHRydWUsXG4gICAgICAgIG9wdGlvbnM6IHtcbiAgICAgICAgICBjaGFuZ2VzX2xlZnQ6IGRhdGFbMF0uY2hhbmdlc19sZWZ0LFxuICAgICAgICAgIGxlbmd0aF9taW46IGRhdGFbMF0ubGVuZ3RoX21pbixcbiAgICAgICAgICBsZW5ndGhfbWF4OiBkYXRhWzBdLmxlbmd0aF9tYXgsXG4gICAgICAgICAgbmV4dF9vbjogZGF0YVswXS5uZXh0X29uID8gbW9tZW50KGRhdGFbMF0ubmV4dF9vbikgOiBudWxsLFxuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgc3RvcmUuZGlzcGF0Y2goZGVoeWRyYXRlKGRhdGFbMV0ucmVzdWx0cykpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBvbkNvbXBsZXRlID0gKHVzZXJuYW1lLCBzbHVnLCBvcHRpb25zKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBvcHRpb25zXG4gICAgfSk7XG5cbiAgICBzdG9yZS5kaXNwYXRjaChcbiAgICAgIGFkZE5hbWVDaGFuZ2UoeyB1c2VybmFtZSwgc2x1ZyB9LCB0aGlzLnByb3BzLnVzZXIsIHRoaXMucHJvcHMudXNlcikpO1xuICAgIHN0b3JlLmRpc3BhdGNoKFxuICAgICAgdXBkYXRlVXNlcm5hbWUodGhpcy5wcm9wcy51c2VyLCB1c2VybmFtZSwgc2x1ZykpO1xuXG4gICAgc25hY2tiYXIuc3VjY2VzcyhnZXR0ZXh0KFwiWW91ciB1c2VybmFtZSBoYXMgYmVlbiBjaGFuZ2VkIHN1Y2Nlc3NmdWxseS5cIikpO1xuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIGdldENoYW5nZUZvcm0oKSB7XG4gICAgaWYgKHRoaXMuc3RhdGUuaXNMb2FkZWQpIHtcbiAgICAgIGlmICh0aGlzLnN0YXRlLm9wdGlvbnMuY2hhbmdlc19sZWZ0ID4gMCkge1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIHJldHVybiA8Q2hhbmdlVXNlcm5hbWUgdXNlcj17dGhpcy5wcm9wcy51c2VyfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9wdGlvbnM9e3RoaXMuc3RhdGUub3B0aW9uc31cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb21wbGV0ZT17dGhpcy5vbkNvbXBsZXRlfSAvPjtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgICAgcmV0dXJuIDxOb0NoYW5nZXNMZWZ0IG9wdGlvbnM9e3RoaXMuc3RhdGUub3B0aW9uc30gLz47XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8Q2hhbmdlVXNlcm5hbWVMb2FkaW5nIC8+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2PlxuICAgICAge3RoaXMuZ2V0Q2hhbmdlRm9ybSgpfVxuICAgICAgPFVzZXJuYW1lSGlzdG9yeSBpc0xvYWRlZD17dGhpcy5zdGF0ZS5pc0xvYWRlZH1cbiAgICAgICAgICAgICAgICAgICAgICAgY2hhbmdlcz17dGhpcy5wcm9wc1sndXNlcm5hbWUtaGlzdG9yeSddfSAvPlxuICAgIDwvZGl2PlxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBGb3JtR3JvdXAgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybS1ncm91cCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFNlbGVjdCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9zZWxlY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBZZXNOb1N3aXRjaCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy95ZXMtbm8tc3dpdGNoJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgeyBwYXRjaFVzZXIgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvYXV0aCc7XG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5pbXBvcnQgdGl0bGUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3BhZ2UtdGl0bGUnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuXG4gICAgICAnaXNfaGlkaW5nX3ByZXNlbmNlJzogcHJvcHMudXNlci5pc19oaWRpbmdfcHJlc2VuY2UsXG4gICAgICAnbGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG8nOiBwcm9wcy51c2VyLmxpbWl0c19wcml2YXRlX3RocmVhZF9pbnZpdGVzX3RvLFxuICAgICAgJ3N1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHMnOiBwcm9wcy51c2VyLnN1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHMsXG4gICAgICAnc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkcyc6IHByb3BzLnVzZXIuc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkcyxcblxuICAgICAgJ2Vycm9ycyc6IHt9XG4gICAgfTtcblxuICAgIHRoaXMucHJpdmF0ZVRocmVhZEludml0ZXNDaG9pY2VzID0gW1xuICAgICAge1xuICAgICAgICAndmFsdWUnOiAwLFxuICAgICAgICAnaWNvbic6ICdoZWxwX291dGxpbmUnLFxuICAgICAgICAnbGFiZWwnOiBnZXR0ZXh0KCdFdmVyeWJvZHknKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgJ3ZhbHVlJzogMSxcbiAgICAgICAgJ2ljb24nOiAnZG9uZV9hbGwnLFxuICAgICAgICAnbGFiZWwnOiBnZXR0ZXh0KCdVc2VycyBJIGZvbGxvdycpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAndmFsdWUnOiAyLFxuICAgICAgICAnaWNvbic6ICdoaWdobGlnaHRfb2ZmJyxcbiAgICAgICAgJ2xhYmVsJzogZ2V0dGV4dCgnTm9ib2R5JylcbiAgICAgIH1cbiAgICBdO1xuXG4gICAgdGhpcy5zdWJzY3JpYmVUb0Nob2ljZXMgPSBbXG4gICAgICB7XG4gICAgICAgICd2YWx1ZSc6IDAsXG4gICAgICAgICdpY29uJzogJ2Jvb2ttYXJrX2JvcmRlcicsXG4gICAgICAgICdsYWJlbCc6IGdldHRleHQoJ05vJylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgICd2YWx1ZSc6IDEsXG4gICAgICAgICdpY29uJzogJ2Jvb2ttYXJrJyxcbiAgICAgICAgJ2xhYmVsJzogZ2V0dGV4dCgnQm9va21hcmsnKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgJ3ZhbHVlJzogMixcbiAgICAgICAgJ2ljb24nOiAnbWFpbCcsXG4gICAgICAgICdsYWJlbCc6IGdldHRleHQoJ0Jvb2ttYXJrIHdpdGggZS1tYWlsIG5vdGlmaWNhdGlvbicpXG4gICAgICB9XG4gICAgXTtcbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdCh0aGlzLnByb3BzLnVzZXIuYXBpX3VybC5vcHRpb25zLCB7XG4gICAgICAnaXNfaGlkaW5nX3ByZXNlbmNlJzogdGhpcy5zdGF0ZS5pc19oaWRpbmdfcHJlc2VuY2UsXG4gICAgICAnbGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG8nOiB0aGlzLnN0YXRlLmxpbWl0c19wcml2YXRlX3RocmVhZF9pbnZpdGVzX3RvLFxuICAgICAgJ3N1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHMnOiB0aGlzLnN0YXRlLnN1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHMsXG4gICAgICAnc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkcyc6IHRoaXMuc3RhdGUuc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkc1xuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcygpIHtcbiAgICBzdG9yZS5kaXNwYXRjaChwYXRjaFVzZXIoe1xuICAgICAgJ2lzX2hpZGluZ19wcmVzZW5jZSc6IHRoaXMuc3RhdGUuaXNfaGlkaW5nX3ByZXNlbmNlLFxuICAgICAgJ2xpbWl0c19wcml2YXRlX3RocmVhZF9pbnZpdGVzX3RvJzogdGhpcy5zdGF0ZS5saW1pdHNfcHJpdmF0ZV90aHJlYWRfaW52aXRlc190byxcbiAgICAgICdzdWJzY3JpYmVfdG9fc3RhcnRlZF90aHJlYWRzJzogdGhpcy5zdGF0ZS5zdWJzY3JpYmVfdG9fc3RhcnRlZF90aHJlYWRzLFxuICAgICAgJ3N1YnNjcmliZV90b19yZXBsaWVkX3RocmVhZHMnOiB0aGlzLnN0YXRlLnN1YnNjcmliZV90b19yZXBsaWVkX3RocmVhZHNcbiAgICB9KSk7XG4gICAgc25hY2tiYXIuc3VjY2VzcyhnZXR0ZXh0KFwiWW91ciBmb3J1bSBvcHRpb25zIGhhdmUgYmVlbiBjaGFuZ2VkLlwiKSk7XG4gIH1cblxuICBoYW5kbGVFcnJvcihyZWplY3Rpb24pIHtcbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAwKSB7XG4gICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiUGxlYXNlIHJlbG9hZCBwYWdlIGFuZCB0cnkgYWdhaW4uXCIpKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgICB9XG4gIH1cblxuICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICB0aXRsZS5zZXQoe1xuICAgICAgdGl0bGU6IGdldHRleHQoXCJGb3J1bSBvcHRpb25zXCIpLFxuICAgICAgcGFyZW50OiBnZXR0ZXh0KFwiQ2hhbmdlIHlvdXIgb3B0aW9uc1wiKVxuICAgIH0pO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fSBjbGFzc05hbWU9XCJmb3JtLWhvcml6b250YWxcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwgcGFuZWwtZGVmYXVsdCBwYW5lbC1mb3JtXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtaGVhZGluZ1wiPlxuICAgICAgICAgIDxoMyBjbGFzc05hbWU9XCJwYW5lbC10aXRsZVwiPntnZXR0ZXh0KFwiQ2hhbmdlIGZvcnVtIG9wdGlvbnNcIil9PC9oMz5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtYm9keVwiPlxuXG4gICAgICAgICAgPGZpZWxkc2V0PlxuICAgICAgICAgICAgPGxlZ2VuZD57Z2V0dGV4dChcIlByaXZhY3kgc2V0dGluZ3NcIil9PC9sZWdlbmQ+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJIaWRlIG15IHByZXNlbmNlXCIpfVxuICAgICAgICAgICAgICAgICAgICAgICBoZWxwVGV4dD17Z2V0dGV4dChcIklmIHlvdSBoaWRlIHlvdXIgcHJlc2VuY2UsIG9ubHkgbWVtYmVycyB3aXRoIHBlcm1pc3Npb24gdG8gc2VlIGhpZGRlbiB1c2VycyB3aWxsIHNlZSB3aGVuIHlvdSBhcmUgb25saW5lLlwiKX1cbiAgICAgICAgICAgICAgICAgICAgICAgZm9yPVwiaWRfaXNfaGlkaW5nX3ByZXNlbmNlXCJcbiAgICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz1cImNvbC1zbS00XCIgY29udHJvbENsYXNzPVwiY29sLXNtLThcIj5cbiAgICAgICAgICAgICAgPFllc05vU3dpdGNoIGlkPVwiaWRfaXNfaGlkaW5nX3ByZXNlbmNlXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgICAgICAgIGljb25Pbj1cInZpc2liaWxpdHlcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgaWNvbk9mZj1cInZpc2liaWxpdHlfb2ZmXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgIGxhYmVsT249e2dldHRleHQoXCJTaG93IG15IHByZXNlbmNlIHRvIG90aGVyIHVzZXJzXCIpfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgbGFiZWxPZmY9e2dldHRleHQoXCJIaWRlIG15IHByZXNlbmNlIGZyb20gb3RoZXIgdXNlcnNcIil9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ2lzX2hpZGluZ19wcmVzZW5jZScpfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUuaXNfaGlkaW5nX3ByZXNlbmNlfSAvPlxuICAgICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJQcml2YXRlIHRocmVhZCBpbnZpdGF0aW9uc1wiKX1cbiAgICAgICAgICAgICAgICAgICAgICAgZm9yPVwiaWRfbGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG9cIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiPlxuICAgICAgICAgICAgICA8U2VsZWN0IGlkPVwiaWRfbGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG9cIlxuICAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ2xpbWl0c19wcml2YXRlX3RocmVhZF9pbnZpdGVzX3RvJyl9XG4gICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUubGltaXRzX3ByaXZhdGVfdGhyZWFkX2ludml0ZXNfdG99XG4gICAgICAgICAgICAgICAgICAgICAgY2hvaWNlcz17dGhpcy5wcml2YXRlVGhyZWFkSW52aXRlc0Nob2ljZXN9IC8+XG4gICAgICAgICAgICA8L0Zvcm1Hcm91cD5cbiAgICAgICAgICA8L2ZpZWxkc2V0PlxuXG4gICAgICAgICAgPGZpZWxkc2V0PlxuICAgICAgICAgICAgPGxlZ2VuZD57Z2V0dGV4dChcIkF1dG9tYXRpYyBzdWJzY3JpcHRpb25zXCIpfTwvbGVnZW5kPlxuXG4gICAgICAgICAgICA8Rm9ybUdyb3VwIGxhYmVsPXtnZXR0ZXh0KFwiVGhyZWFkcyBJIHN0YXJ0XCIpfVxuICAgICAgICAgICAgICAgICAgICAgICBmb3I9XCJpZF9zdWJzY3JpYmVfdG9fc3RhcnRlZF90aHJlYWRzXCJcbiAgICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz1cImNvbC1zbS00XCIgY29udHJvbENsYXNzPVwiY29sLXNtLThcIj5cbiAgICAgICAgICAgICAgPFNlbGVjdCBpZD1cImlkX3N1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHNcIlxuICAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3N1YnNjcmliZV90b19zdGFydGVkX3RocmVhZHMnKX1cbiAgICAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5zdWJzY3JpYmVfdG9fc3RhcnRlZF90aHJlYWRzfVxuICAgICAgICAgICAgICAgICAgICAgIGNob2ljZXM9e3RoaXMuc3Vic2NyaWJlVG9DaG9pY2VzfSAvPlxuICAgICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJUaHJlYWRzIEkgcmVwbHkgdG9cIil9XG4gICAgICAgICAgICAgICAgICAgICAgIGZvcj1cImlkX3N1YnNjcmliZV90b19yZXBsaWVkX3RocmVhZHNcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiPlxuICAgICAgICAgICAgICA8U2VsZWN0IGlkPVwiaWRfc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkc1wiXG4gICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnc3Vic2NyaWJlX3RvX3JlcGxpZWRfdGhyZWFkcycpfVxuICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnN1YnNjcmliZV90b19yZXBsaWVkX3RocmVhZHN9XG4gICAgICAgICAgICAgICAgICAgICAgY2hvaWNlcz17dGhpcy5zdWJzY3JpYmVUb0Nob2ljZXN9IC8+XG4gICAgICAgICAgICA8L0Zvcm1Hcm91cD5cbiAgICAgICAgICA8L2ZpZWxkc2V0PlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWZvb3RlclwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicm93XCI+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1zbS04IGNvbC1zbS1vZmZzZXQtNFwiPlxuXG4gICAgICAgICAgICAgIDxCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXByaW1hcnlcIiBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAgICAgICAge2dldHRleHQoXCJTYXZlIGNoYW5nZXNcIil9XG4gICAgICAgICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Zvcm0+XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBMaW5rIH0gZnJvbSAncmVhY3Qtcm91dGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgTGkgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvbGknOyAvL2pzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnOyAvL2pzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgU2lkZU5hdiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvLyBqc2hpbnQgaWdub3JlOnN0YXJ0XG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibGlzdC1ncm91cCBuYXYtc2lkZVwiPlxuICAgICAge3RoaXMucHJvcHMub3B0aW9ucy5tYXAoKG9wdGlvbikgPT4ge1xuICAgICAgICByZXR1cm4gPExpbmsgdG89e3RoaXMucHJvcHMuYmFzZVVybCArIG9wdGlvbi5jb21wb25lbnQgKyAnLyd9XG4gICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJsaXN0LWdyb3VwLWl0ZW1cIlxuICAgICAgICAgICAgICAgICAgICAgYWN0aXZlQ2xhc3NOYW1lPVwiYWN0aXZlXCJcbiAgICAgICAgICAgICAgICAgICAgIGtleT17b3B0aW9uLmNvbXBvbmVudH0+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAge29wdGlvbi5pY29ufVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICB7b3B0aW9uLm5hbWV9XG4gICAgICAgIDwvTGluaz47XG4gICAgICB9KX1cbiAgICA8L2Rpdj47XG4gICAgLy8ganNoaW50IGlnbm9yZTplbmRcbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgQ29tcGFjdE5hdiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvLyBqc2hpbnQgaWdub3JlOnN0YXJ0XG4gICAgcmV0dXJuIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51XCIgcm9sZT1cIm1lbnVcIj5cbiAgICAgIHt0aGlzLnByb3BzLm9wdGlvbnMubWFwKChvcHRpb24pID0+IHtcbiAgICAgICAgcmV0dXJuIDxMaSBwYXRoPXt0aGlzLnByb3BzLmJhc2VVcmwgKyBvcHRpb24uY29tcG9uZW50ICsgJy8nfVxuICAgICAgICAgICAgICAgICAgIGtleT17b3B0aW9uLmNvbXBvbmVudH0+XG4gICAgICAgICAgPExpbmsgdG89e3RoaXMucHJvcHMuYmFzZVVybCArIG9wdGlvbi5jb21wb25lbnQgKyAnLyd9PlxuICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgICB7b3B0aW9uLmljb259XG4gICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgICB7b3B0aW9uLm5hbWV9XG4gICAgICAgICAgPC9MaW5rPlxuICAgICAgICA8L0xpPjtcbiAgICAgIH0pfVxuICAgIDwvdWw+O1xuICAgIC8vIGpzaGludCBpZ25vcmU6ZW5kXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCB7IFNpZGVOYXYsIENvbXBhY3ROYXYgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9vcHRpb25zL25hdnMnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBDaGFuZ2VGb3J1bU9wdGlvbnMgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvb3B0aW9ucy9mb3J1bS1vcHRpb25zJztcbmltcG9ydCBDaGFuZ2VVc2VybmFtZSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9vcHRpb25zL2NoYW5nZS11c2VybmFtZSc7XG5pbXBvcnQgQ2hhbmdlU2lnbkluQ3JlZGVudGlhbHMgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvb3B0aW9ucy9zaWduLWluLWNyZWRlbnRpYWxzJztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBkcm9wZG93bjogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICB0b2dnbGVOYXYgPSAoKSA9PiB7XG4gICAgaWYgKHRoaXMuc3RhdGUuZHJvcGRvd24pIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICBkcm9wZG93bjogZmFsc2VcbiAgICAgIH0pO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgZHJvcGRvd246IHRydWVcbiAgICAgIH0pO1xuICAgIH1cbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRUb2dnbGVOYXZDbGFzc05hbWUoKSB7XG4gICAgaWYgKHRoaXMuc3RhdGUuZHJvcGRvd24pIHtcbiAgICAgIHJldHVybiAnYnRuIGJ0bi1kZWZhdWx0IGJ0bi1pY29uIG9wZW4nO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gJ2J0biBidG4tZGVmYXVsdCBidG4taWNvbic7XG4gICAgfVxuICB9XG5cbiAgZ2V0Q29tcGFjdE5hdkNsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5kcm9wZG93bikge1xuICAgICAgcmV0dXJuICdjb21wYWN0LW5hdiBvcGVuJztcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuICdjb21wYWN0LW5hdic7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJwYWdlIHBhZ2Utb3B0aW9uc1wiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYWdlLWhlYWRlclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuXG4gICAgICAgICAgPGgxIGNsYXNzTmFtZT1cInB1bGwtbGVmdFwiPntnZXR0ZXh0KFwiQ2hhbmdlIHlvdXIgb3B0aW9uc1wiKX08L2gxPlxuXG4gICAgICAgICAgPGJ1dHRvbiBjbGFzc05hbWU9XCJidG4gYnRuLWRlZmF1bHQgYnRuLWljb24gYnRuLWRyb3Bkb3duLXRvZ2dsZSBoaWRkZW4tbWQgaGlkZGVuLWxnXCJcbiAgICAgICAgICAgICAgICAgIHR5cGU9XCJidXR0b25cIlxuICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy50b2dnbGVOYXZ9XG4gICAgICAgICAgICAgICAgICBhcmlhLWhhc3BvcHVwPVwidHJ1ZVwiXG4gICAgICAgICAgICAgICAgICBhcmlhLWV4cGFuZGVkPXt0aGlzLnN0YXRlLmRyb3Bkb3duID8gJ3RydWUnIDogJ2ZhbHNlJ30+XG4gICAgICAgICAgICA8aSBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgIG1lbnVcbiAgICAgICAgICAgIDwvaT5cbiAgICAgICAgICA8L2J1dHRvbj5cblxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9e3RoaXMuZ2V0Q29tcGFjdE5hdkNsYXNzTmFtZSgpfT5cblxuICAgICAgICA8Q29tcGFjdE5hdiBvcHRpb25zPXttaXNhZ28uZ2V0KCdVU0VSX09QVElPTlMnKX1cbiAgICAgICAgICAgICAgICAgICAgYmFzZVVybD17bWlzYWdvLmdldCgnVVNFUkNQX1VSTCcpfSAvPlxuXG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1tZC0zIGhpZGRlbi14cyBoaWRkZW4tc21cIj5cblxuICAgICAgICAgICAgPFNpZGVOYXYgb3B0aW9ucz17bWlzYWdvLmdldCgnVVNFUl9PUFRJT05TJyl9XG4gICAgICAgICAgICAgICAgICAgICBiYXNlVXJsPXttaXNhZ28uZ2V0KCdVU0VSQ1BfVVJMJyl9IC8+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1tZC05XCI+XG5cbiAgICAgICAgICAgIHt0aGlzLnByb3BzLmNoaWxkcmVufVxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuXG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0KHN0b3JlKSB7XG4gIHJldHVybiB7XG4gICAgJ3RpY2snOiBzdG9yZS50aWNrLnRpY2ssXG4gICAgJ3VzZXInOiBzdG9yZS5hdXRoLnVzZXIsXG4gICAgJ3VzZXJuYW1lLWhpc3RvcnknOiBzdG9yZVsndXNlcm5hbWUtaGlzdG9yeSddXG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBwYXRocygpIHtcbiAgcmV0dXJuIFtcbiAgICB7XG4gICAgICBwYXRoOiBtaXNhZ28uZ2V0KCdVU0VSQ1BfVVJMJykgKyAnZm9ydW0tb3B0aW9ucy8nLFxuICAgICAgY29tcG9uZW50OiBjb25uZWN0KHNlbGVjdCkoQ2hhbmdlRm9ydW1PcHRpb25zKVxuICAgIH0sXG4gICAge1xuICAgICAgcGF0aDogbWlzYWdvLmdldCgnVVNFUkNQX1VSTCcpICsgJ2NoYW5nZS11c2VybmFtZS8nLFxuICAgICAgY29tcG9uZW50OiBjb25uZWN0KHNlbGVjdCkoQ2hhbmdlVXNlcm5hbWUpXG4gICAgfSxcbiAgICB7XG4gICAgICBwYXRoOiBtaXNhZ28uZ2V0KCdVU0VSQ1BfVVJMJykgKyAnc2lnbi1pbi1jcmVkZW50aWFscy8nLFxuICAgICAgY29tcG9uZW50OiBjb25uZWN0KHNlbGVjdCkoQ2hhbmdlU2lnbkluQ3JlZGVudGlhbHMpXG4gICAgfVxuICBdO1xufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBGb3JtR3JvdXAgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybS1ncm91cCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IHRpdGxlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9wYWdlLXRpdGxlJztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuaW1wb3J0ICogYXMgdmFsaWRhdG9ycyBmcm9tICdtaXNhZ28vdXRpbHMvdmFsaWRhdG9ycyc7XG5cbmV4cG9ydCBjbGFzcyBDaGFuZ2VFbWFpbCBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBuZXdfZW1haWw6ICcnLFxuICAgICAgcGFzc3dvcmQ6ICcnLFxuXG4gICAgICB2YWxpZGF0b3JzOiB7XG4gICAgICAgIG5ld19lbWFpbDogW1xuICAgICAgICAgIHZhbGlkYXRvcnMuZW1haWwoKVxuICAgICAgICBdLFxuICAgICAgICBwYXNzd29yZDogW11cbiAgICAgIH0sXG5cbiAgICAgIGlzTG9hZGluZzogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgY2xlYW4oKSB7XG4gICAgbGV0IGVycm9ycyA9IHRoaXMudmFsaWRhdGUoKTtcbiAgICBsZXQgbGVuZ3RocyA9IFtcbiAgICAgIHRoaXMuc3RhdGUubmV3X2VtYWlsLnRyaW0oKS5sZW5ndGgsXG4gICAgICB0aGlzLnN0YXRlLnBhc3N3b3JkLnRyaW0oKS5sZW5ndGhcbiAgICBdO1xuXG4gICAgaWYgKGxlbmd0aHMuaW5kZXhPZigwKSAhPT0gLTEpIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJGaWxsIG91dCBhbGwgZmllbGRzLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgaWYgKGVycm9ycy5uZXdfZW1haWwpIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGVycm9ycy5uZXdfZW1haWxbMF0pO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLmNoYW5nZV9lbWFpbCwge1xuICAgICAgbmV3X2VtYWlsOiB0aGlzLnN0YXRlLm5ld19lbWFpbCxcbiAgICAgIHBhc3N3b3JkOiB0aGlzLnN0YXRlLnBhc3N3b3JkLFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhyZXNwb25zZSkge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgbmV3X2VtYWlsOiAnJyxcbiAgICAgIHBhc3N3b3JkOiAnJ1xuICAgIH0pO1xuXG4gICAgc25hY2tiYXIuc3VjY2VzcyhyZXNwb25zZS5kZXRhaWwpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMCkge1xuICAgICAgaWYgKHJlamVjdGlvbi5uZXdfZW1haWwpIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLm5ld19lbWFpbCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24ucGFzc3dvcmQpO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxmb3JtIG9uU3VibWl0PXt0aGlzLmhhbmRsZVN1Ym1pdH0gY2xhc3NOYW1lPVwiZm9ybS1ob3Jpem9udGFsXCI+XG4gICAgICA8aW5wdXQgdHlwZT1cInR5cGVcIiBzdHlsZT17e2Rpc3BsYXk6ICdub25lJ319IC8+XG4gICAgICA8aW5wdXQgdHlwZT1cInBhc3N3b3JkXCIgc3R5bGU9e3tkaXNwbGF5OiAnbm9uZSd9fSAvPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbCBwYW5lbC1kZWZhdWx0IHBhbmVsLWZvcm1cIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1oZWFkaW5nXCI+XG4gICAgICAgICAgPGgzIGNsYXNzTmFtZT1cInBhbmVsLXRpdGxlXCI+e2dldHRleHQoXCJDaGFuZ2UgZS1tYWlsIGFkZHJlc3NcIil9PC9oMz5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtYm9keVwiPlxuXG4gICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIk5ldyBlLW1haWxcIil9IGZvcj1cImlkX25ld19lbWFpbFwiXG4gICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiPlxuICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgaWQ9XCJpZF9uZXdfZW1haWxcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ25ld19lbWFpbCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLm5ld19lbWFpbH0gLz5cbiAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgIDxociAvPlxuXG4gICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIllvdXIgY3VycmVudCBwYXNzd29yZFwiKX0gZm9yPVwiaWRfcGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz1cImNvbC1zbS00XCIgY29udHJvbENsYXNzPVwiY29sLXNtLThcIj5cbiAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBpZD1cImlkX3Bhc3N3b3JkXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdwYXNzd29yZCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnBhc3N3b3JkfSAvPlxuICAgICAgICAgIDwvRm9ybUdyb3VwPlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhbmVsLWZvb3RlclwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicm93XCI+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1zbS04IGNvbC1zbS1vZmZzZXQtNFwiPlxuXG4gICAgICAgICAgICAgIDxCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXByaW1hcnlcIiBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAgICAgICAge2dldHRleHQoXCJDaGFuZ2UgZS1tYWlsXCIpfVxuICAgICAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9mb3JtPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBDaGFuZ2VQYXNzd29yZCBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBuZXdfcGFzc3dvcmQ6ICcnLFxuICAgICAgcmVwZWF0X3Bhc3N3b3JkOiAnJyxcbiAgICAgIHBhc3N3b3JkOiAnJyxcblxuICAgICAgdmFsaWRhdG9yczoge1xuICAgICAgICBuZXdfcGFzc3dvcmQ6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnBhc3N3b3JkTWluTGVuZ3RoKG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykpXG4gICAgICAgIF0sXG4gICAgICAgIHJlcGVhdF9wYXNzd29yZDogW10sXG4gICAgICAgIHBhc3N3b3JkOiBbXVxuICAgICAgfSxcblxuICAgICAgaXNMb2FkaW5nOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBsZXQgZXJyb3JzID0gdGhpcy52YWxpZGF0ZSgpO1xuICAgIGxldCBsZW5ndGhzID0gW1xuICAgICAgdGhpcy5zdGF0ZS5uZXdfcGFzc3dvcmQudHJpbSgpLmxlbmd0aCxcbiAgICAgIHRoaXMuc3RhdGUucmVwZWF0X3Bhc3N3b3JkLnRyaW0oKS5sZW5ndGgsXG4gICAgICB0aGlzLnN0YXRlLnBhc3N3b3JkLnRyaW0oKS5sZW5ndGhcbiAgICBdO1xuXG4gICAgaWYgKGxlbmd0aHMuaW5kZXhPZigwKSAhPT0gLTEpIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJGaWxsIG91dCBhbGwgZmllbGRzLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgaWYgKGVycm9ycy5uZXdfcGFzc3dvcmQpIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGVycm9ycy5uZXdfcGFzc3dvcmRbMF0pO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIGlmICh0aGlzLnN0YXRlLm5ld19wYXNzd29yZC50cmltKCkgIT09IHRoaXMuc3RhdGUucmVwZWF0X3Bhc3N3b3JkLnRyaW0oKSkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIk5ldyBwYXNzd29yZHMgYXJlIGRpZmZlcmVudC5cIikpO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KHRoaXMucHJvcHMudXNlci5hcGlfdXJsLmNoYW5nZV9wYXNzd29yZCwge1xuICAgICAgbmV3X3Bhc3N3b3JkOiB0aGlzLnN0YXRlLm5ld19wYXNzd29yZCxcbiAgICAgIHBhc3N3b3JkOiB0aGlzLnN0YXRlLnBhc3N3b3JkXG4gICAgfSk7XG4gIH1cblxuICBoYW5kbGVTdWNjZXNzKHJlc3BvbnNlKSB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBuZXdfcGFzc3dvcmQ6ICcnLFxuICAgICAgcmVwZWF0X3Bhc3N3b3JkOiAnJyxcbiAgICAgIHBhc3N3b3JkOiAnJ1xuICAgIH0pO1xuXG4gICAgc25hY2tiYXIuc3VjY2VzcyhyZXNwb25zZS5kZXRhaWwpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMCkge1xuICAgICAgaWYgKHJlamVjdGlvbi5uZXdfcGFzc3dvcmQpIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLm5ld19wYXNzd29yZCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24ucGFzc3dvcmQpO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxmb3JtIG9uU3VibWl0PXt0aGlzLmhhbmRsZVN1Ym1pdH0gY2xhc3NOYW1lPVwiZm9ybS1ob3Jpem9udGFsXCI+XG4gICAgICA8aW5wdXQgdHlwZT1cInR5cGVcIiBzdHlsZT17e2Rpc3BsYXk6ICdub25lJ319IC8+XG4gICAgICA8aW5wdXQgdHlwZT1cInBhc3N3b3JkXCIgc3R5bGU9e3tkaXNwbGF5OiAnbm9uZSd9fSAvPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbCBwYW5lbC1kZWZhdWx0IHBhbmVsLWZvcm1cIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1oZWFkaW5nXCI+XG4gICAgICAgICAgPGgzIGNsYXNzTmFtZT1cInBhbmVsLXRpdGxlXCI+e2dldHRleHQoXCJDaGFuZ2UgcGFzc3dvcmRcIil9PC9oMz5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicGFuZWwtYm9keVwiPlxuXG4gICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIk5ldyBwYXNzd29yZFwiKX0gZm9yPVwiaWRfbmV3X3Bhc3N3b3JkXCJcbiAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCI+XG4gICAgICAgICAgICA8aW5wdXQgdHlwZT1cInBhc3N3b3JkXCIgaWQ9XCJpZF9uZXdfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ25ld19wYXNzd29yZCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLm5ld19wYXNzd29yZH0gLz5cbiAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJSZXBlYXQgcGFzc3dvcmRcIil9IGZvcj1cImlkX3JlcGVhdF9wYXNzd29yZFwiXG4gICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiPlxuICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJwYXNzd29yZFwiIGlkPVwiaWRfcmVwZWF0X3Bhc3N3b3JkXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdyZXBlYXRfcGFzc3dvcmQnKX1cbiAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5yZXBlYXRfcGFzc3dvcmR9IC8+XG4gICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgICA8aHIgLz5cblxuICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJZb3VyIGN1cnJlbnQgcGFzc3dvcmRcIil9IGZvcj1cImlkX3Bhc3N3b3JkXCJcbiAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCI+XG4gICAgICAgICAgICA8aW5wdXQgdHlwZT1cInBhc3N3b3JkXCIgaWQ9XCJpZF9wYXNzd29yZFwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgncGFzc3dvcmQnKX1cbiAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5wYXNzd29yZH0gLz5cbiAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYW5lbC1mb290ZXJcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInJvd1wiPlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wtc20tOCBjb2wtc20tb2Zmc2V0LTRcIj5cblxuICAgICAgICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5XCIgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9PlxuICAgICAgICAgICAgICAgIHtnZXR0ZXh0KFwiQ2hhbmdlIHBhc3N3b3JkXCIpfVxuICAgICAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9mb3JtPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgdGl0bGUuc2V0KHtcbiAgICAgIHRpdGxlOiBnZXR0ZXh0KFwiQ2hhbmdlIGVtYWlsIG9yIHBhc3N3b3JkXCIpLFxuICAgICAgcGFyZW50OiBnZXR0ZXh0KFwiQ2hhbmdlIHlvdXIgb3B0aW9uc1wiKVxuICAgIH0pO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdj5cbiAgICAgIDxDaGFuZ2VFbWFpbCB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IC8+XG4gICAgICA8Q2hhbmdlUGFzc3dvcmQgdXNlcj17dGhpcy5wcm9wcy51c2VyfSAvPlxuXG4gICAgICA8cCBjbGFzc05hbWU9XCJtZXNzYWdlLWxpbmVcIj5cbiAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgIHdhcm5pbmdcbiAgICAgICAgPC9zcGFuPlxuICAgICAgICA8YSBocmVmPXttaXNhZ28uZ2V0KCdGT1JHT1RURU5fUEFTU1dPUkRfVVJMJyl9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiQ2hhbmdlIGZvcmdvdHRlbiBwYXNzd29yZFwiKX1cbiAgICAgICAgPC9hPlxuICAgICAgPC9wPlxuICAgIDwvZGl2PlxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHp4Y3ZibiBmcm9tICdtaXNhZ28vc2VydmljZXMvenhjdmJuJztcblxuZXhwb3J0IGNvbnN0IFNUWUxFUyA9IFtcbiAgJ3Byb2dyZXNzLWJhci1kYW5nZXInLFxuICAncHJvZ3Jlc3MtYmFyLXdhcm5pbmcnLFxuICAncHJvZ3Jlc3MtYmFyLXdhcm5pbmcnLFxuICAncHJvZ3Jlc3MtYmFyLXByaW1hcnknLFxuICAncHJvZ3Jlc3MtYmFyLXN1Y2Nlc3MnXG5dO1xuXG5leHBvcnQgY29uc3QgTEFCRUxTID0gW1xuICBnZXR0ZXh0KFwiRW50ZXJlZCBwYXNzd29yZCBpcyB2ZXJ5IHdlYWsuXCIpLFxuICBnZXR0ZXh0KFwiRW50ZXJlZCBwYXNzd29yZCBpcyB3ZWFrLlwiKSxcbiAgZ2V0dGV4dChcIkVudGVyZWQgcGFzc3dvcmQgaXMgYXZlcmFnZS5cIiksXG4gIGdldHRleHQoXCJFbnRlcmVkIHBhc3N3b3JkIGlzIHN0cm9uZy5cIiksXG4gIGdldHRleHQoXCJFbnRlcmVkIHBhc3N3b3JkIGlzIHZlcnkgc3Ryb25nLlwiKVxuXTtcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuX3Njb3JlID0gMDtcbiAgICB0aGlzLl9wYXNzd29yZCA9IG51bGw7XG4gICAgdGhpcy5faW5wdXRzID0gW107XG4gIH1cblxuICBnZXRTY29yZShwYXNzd29yZCwgaW5wdXRzKSB7XG4gICAgbGV0IGNhY2hlU3RhbGUgPSBmYWxzZTtcblxuICAgIGlmIChwYXNzd29yZC50cmltKCkgIT09IHRoaXMuX3Bhc3N3b3JkKSB7XG4gICAgICBjYWNoZVN0YWxlID0gdHJ1ZTtcbiAgICB9XG5cbiAgICBpZiAoaW5wdXRzLmxlbmd0aCAhPT0gdGhpcy5faW5wdXRzLmxlbmd0aCkge1xuICAgICAgY2FjaGVTdGFsZSA9IHRydWU7XG4gICAgfSBlbHNlIHtcbiAgICAgIGlucHV0cy5tYXAoKHZhbHVlLCBpKSA9PiB7XG4gICAgICAgIGlmICh2YWx1ZS50cmltKCkgIT09IHRoaXMuX2lucHV0c1tpXSkge1xuICAgICAgICAgIGNhY2hlU3RhbGUgPSB0cnVlO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBpZiAoY2FjaGVTdGFsZSkge1xuICAgICAgdGhpcy5fc2NvcmUgPSB6eGN2Ym4uc2NvcmVQYXNzd29yZChwYXNzd29yZCwgaW5wdXRzKTtcbiAgICAgIHRoaXMuX3Bhc3N3b3JkID0gcGFzc3dvcmQudHJpbSgpO1xuICAgICAgdGhpcy5faW5wdXRzID0gaW5wdXRzLm1hcChmdW5jdGlvbih2YWx1ZSkge1xuICAgICAgICByZXR1cm4gdmFsdWUudHJpbSgpO1xuICAgICAgfSk7XG4gICAgfVxuXG4gICAgcmV0dXJuIHRoaXMuX3Njb3JlO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBsZXQgc2NvcmUgPSB0aGlzLmdldFNjb3JlKHRoaXMucHJvcHMucGFzc3dvcmQsIHRoaXMucHJvcHMuaW5wdXRzKTtcblxuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImhlbHAtYmxvY2sgcGFzc3dvcmQtc3RyZW5ndGhcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwicHJvZ3Jlc3NcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9e1wicHJvZ3Jlc3MtYmFyIFwiICsgU1RZTEVTW3Njb3JlXX1cbiAgICAgICAgICAgICBzdHlsZT17e3dpZHRoOiAoMjAgKyAoMjAgKiBzY29yZSkpICsgJyUnfX1cbiAgICAgICAgICAgICByb2xlPVwicHJvZ3Jlc3MtYmFyXCJcbiAgICAgICAgICAgICBhcmlhLXZhbHVlbm93PXtzY29yZX1cbiAgICAgICAgICAgICBhcmlhLXZhbHVlbWluPVwiMFwiXG4gICAgICAgICAgICAgYXJpYS12YWx1ZW1heD1cIjRcIj5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJzci1vbmx5XCI+XG4gICAgICAgICAgICB7TEFCRUxTW3Njb3JlXX1cbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgICA8cCBjbGFzc05hbWU9XCJ0ZXh0LXNtYWxsXCI+XG4gICAgICAgIHtMQUJFTFNbc2NvcmVdfVxuICAgICAgPC9wPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBMb2FkZXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvbG9hZGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgUmVnaXN0ZXJNb2RhbCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9yZWdpc3Rlci5qcyc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGNhcHRjaGEgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2NhcHRjaGEnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCB6eGN2Ym4gZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3p4Y3Zibic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZSxcbiAgICAgICdpc0xvYWRlZCc6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgc2hvd1JlZ2lzdGVyTW9kYWwgPSAoKSA9PiB7XG4gICAgaWYgKG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykuYWNjb3VudF9hY3RpdmF0aW9uID09PSAnY2xvc2VkJykge1xuICAgICAgc25hY2tiYXIuaW5mbyhnZXR0ZXh0KFwiTmV3IHJlZ2lzdHJhdGlvbnMgYXJlIGN1cnJlbnRseSBkaXNhYmxlZC5cIikpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5zdGF0ZS5pc0xvYWRlZCkge1xuICAgICAgbW9kYWwuc2hvdyhSZWdpc3Rlck1vZGFsKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICdpc0xvYWRpbmcnOiB0cnVlXG4gICAgICB9KTtcblxuICAgICAgUHJvbWlzZS5hbGwoW1xuICAgICAgICBjYXB0Y2hhLmxvYWQoKSxcbiAgICAgICAgenhjdmJuLmxvYWQoKVxuICAgICAgXSkudGhlbigoKSA9PiB7XG4gICAgICAgIGlmICghdGhpcy5zdGF0ZS5pc0xvYWRlZCkge1xuICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuICAgICAgICAgICAgJ2lzTG9hZGVkJzogZmFsc2VcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuXG4gICAgICAgIG1vZGFsLnNob3coUmVnaXN0ZXJNb2RhbCk7XG4gICAgICB9KTtcbiAgICB9XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgZ2V0Q2xhc3NOYW1lKCkge1xuICAgIHJldHVybiB0aGlzLnByb3BzLmNsYXNzTmFtZSArICh0aGlzLnN0YXRlLmlzTG9hZGluZyA/ICcgYnRuLWxvYWRpbmcnIDogJycpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgb25DbGljaz17dGhpcy5zaG93UmVnaXN0ZXJNb2RhbH1cbiAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9eydidG4gJyArIHRoaXMuZ2V0Q2xhc3NOYW1lKCl9XG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkZWR9PlxuICAgICAge2dldHRleHQoXCJSZWdpc3RlclwiKX1cbiAgICAgIHt0aGlzLnN0YXRlLmlzTG9hZGluZyA/IDxMb2FkZXIgLz4gOiBudWxsIH1cbiAgICA8L2J1dHRvbj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBGb3JtR3JvdXAgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybS1ncm91cCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFBhc3N3b3JkU3RyZW5ndGggZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvcGFzc3dvcmQtc3RyZW5ndGgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBhdXRoIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hdXRoJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgY2FwdGNoYSBmcm9tICdtaXNhZ28vc2VydmljZXMvY2FwdGNoYSc7XG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuaW1wb3J0IHNob3dCYW5uZWRQYWdlIGZyb20gJ21pc2Fnby91dGlscy9iYW5uZWQtcGFnZSc7XG5pbXBvcnQgKiBhcyB2YWxpZGF0b3JzIGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcblxuZXhwb3J0IGNsYXNzIFJlZ2lzdGVyRm9ybSBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG5cbiAgICAgICd1c2VybmFtZSc6ICcnLFxuICAgICAgJ2VtYWlsJzogJycsXG4gICAgICAncGFzc3dvcmQnOiAnJyxcbiAgICAgICdjYXB0Y2hhJzogJycsXG5cbiAgICAgICd2YWxpZGF0b3JzJzoge1xuICAgICAgICAndXNlcm5hbWUnOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy51c2VybmFtZUNvbnRlbnQoKSxcbiAgICAgICAgICB2YWxpZGF0b3JzLnVzZXJuYW1lTWluTGVuZ3RoKG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykpLFxuICAgICAgICAgIHZhbGlkYXRvcnMudXNlcm5hbWVNYXhMZW5ndGgobWlzYWdvLmdldCgnU0VUVElOR1MnKSlcbiAgICAgICAgXSxcbiAgICAgICAgJ2VtYWlsJzogW1xuICAgICAgICAgIHZhbGlkYXRvcnMuZW1haWwoKVxuICAgICAgICBdLFxuICAgICAgICAncGFzc3dvcmQnOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy5wYXNzd29yZE1pbkxlbmd0aChtaXNhZ28uZ2V0KCdTRVRUSU5HUycpKVxuICAgICAgICBdLFxuICAgICAgICAnY2FwdGNoYSc6IGNhcHRjaGEudmFsaWRhdG9yKClcbiAgICAgIH0sXG5cbiAgICAgICdlcnJvcnMnOiB7fVxuICAgIH07XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBpZiAodGhpcy5pc1ZhbGlkKCkpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRm9ybSBjb250YWlucyBlcnJvcnMuXCIpKTtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnZXJyb3JzJzogdGhpcy52YWxpZGF0ZSgpXG4gICAgICB9KTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBhamF4LnBvc3QobWlzYWdvLmdldCgnVVNFUlNfQVBJJyksIHtcbiAgICAgICd1c2VybmFtZSc6IHRoaXMuc3RhdGUudXNlcm5hbWUsXG4gICAgICAnZW1haWwnOiB0aGlzLnN0YXRlLmVtYWlsLFxuICAgICAgJ3Bhc3N3b3JkJzogdGhpcy5zdGF0ZS5wYXNzd29yZCxcbiAgICAgICdjYXB0Y2hhJzogdGhpcy5zdGF0ZS5jYXB0Y2hhXG4gICAgfSk7XG4gIH1cblxuICBoYW5kbGVTdWNjZXNzKGFwaVJlc3BvbnNlKSB7XG4gICAgdGhpcy5wcm9wcy5jYWxsYmFjayhhcGlSZXNwb25zZSk7XG4gIH1cblxuICBoYW5kbGVFcnJvcihyZWplY3Rpb24pIHtcbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAwKSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ2Vycm9ycyc6IE9iamVjdC5hc3NpZ24oe30sIHRoaXMuc3RhdGUuZXJyb3JzLCByZWplY3Rpb24pXG4gICAgICB9KTtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJGb3JtIGNvbnRhaW5zIGVycm9ycy5cIikpO1xuICAgIH0gZWxzZSBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAzICYmIHJlamVjdGlvbi5iYW4pIHtcbiAgICAgIHNob3dCYW5uZWRQYWdlKHJlamVjdGlvbi5iYW4pO1xuICAgICAgbW9kYWwuaGlkZSgpO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIGdldExlZ2FsRm9vdE5vdGUoKSB7XG4gICAgaWYgKG1pc2Fnby5nZXQoJ1RFUk1TX09GX1NFUlZJQ0VfVVJMJykpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8YSBocmVmPXttaXNhZ28uZ2V0KCdURVJNU19PRl9TRVJWSUNFX1VSTCcpfVxuICAgICAgICAgICAgICAgIHRhcmdldD1cIl9ibGFua1wiPlxuICAgICAgICB7Z2V0dGV4dChcIkJ5IHJlZ2lzdGVyaW5nIHlvdSBhZ3JlZSB0byBzaXRlJ3MgdGVybXMgYW5kIGNvbmRpdGlvbnMuXCIpfVxuICAgICAgPC9hPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtZGlhbG9nIG1vZGFsLXJlZ2lzdGVyXCIgcm9sZT1cImRvY3VtZW50XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWNvbnRlbnRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1oZWFkZXJcIj5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJjbG9zZVwiIGRhdGEtZGlzbWlzcz1cIm1vZGFsXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtbGFiZWw9e2dldHRleHQoXCJDbG9zZVwiKX0+XG4gICAgICAgICAgICA8c3BhbiBhcmlhLWhpZGRlbj1cInRydWVcIj4mdGltZXM7PC9zcGFuPlxuICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgIDxoNCBjbGFzc05hbWU9XCJtb2RhbC10aXRsZVwiPntnZXR0ZXh0KFwiUmVnaXN0ZXJcIil9PC9oND5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxmb3JtIG9uU3VibWl0PXt0aGlzLmhhbmRsZVN1Ym1pdH0gY2xhc3NOYW1lPVwiZm9ybS1ob3Jpem9udGFsXCI+XG4gICAgICAgICAgPGlucHV0IHR5cGU9XCJ0eXBlXCIgc3R5bGU9e3tkaXNwbGF5OiAnbm9uZSd9fSAvPlxuICAgICAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBzdHlsZT17e2Rpc3BsYXk6ICdub25lJ319IC8+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5XCI+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJVc2VybmFtZVwiKX0gZm9yPVwiaWRfdXNlcm5hbWVcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiXG4gICAgICAgICAgICAgICAgICAgICAgIHZhbGlkYXRpb249e3RoaXMuc3RhdGUuZXJyb3JzLnVzZXJuYW1lfT5cbiAgICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgaWQ9XCJpZF91c2VybmFtZVwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgICBhcmlhLWRlc2NyaWJlZGJ5PVwiaWRfdXNlcm5hbWVfc3RhdHVzXCJcbiAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgndXNlcm5hbWUnKX1cbiAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnVzZXJuYW1lfSAvPlxuICAgICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJFLW1haWxcIil9IGZvcj1cImlkX2VtYWlsXCJcbiAgICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz1cImNvbC1zbS00XCIgY29udHJvbENsYXNzPVwiY29sLXNtLThcIlxuICAgICAgICAgICAgICAgICAgICAgICB2YWxpZGF0aW9uPXt0aGlzLnN0YXRlLmVycm9ycy5lbWFpbH0+XG4gICAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwidGV4dFwiIGlkPVwiaWRfZW1haWxcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgICAgYXJpYS1kZXNjcmliZWRieT1cImlkX2VtYWlsX3N0YXR1c1wiXG4gICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ2VtYWlsJyl9XG4gICAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5lbWFpbH0gLz5cbiAgICAgICAgICAgIDwvRm9ybUdyb3VwPlxuXG4gICAgICAgICAgICA8Rm9ybUdyb3VwIGxhYmVsPXtnZXR0ZXh0KFwiUGFzc3dvcmRcIil9IGZvcj1cImlkX3Bhc3N3b3JkXCJcbiAgICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz1cImNvbC1zbS00XCIgY29udHJvbENsYXNzPVwiY29sLXNtLThcIlxuICAgICAgICAgICAgICAgICAgICAgICB2YWxpZGF0aW9uPXt0aGlzLnN0YXRlLmVycm9ycy5wYXNzd29yZH1cbiAgICAgICAgICAgICAgICAgICAgICAgZXh0cmE9ezxQYXNzd29yZFN0cmVuZ3RoIHBhc3N3b3JkPXt0aGlzLnN0YXRlLnBhc3N3b3JkfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaW5wdXRzPXtbXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc3RhdGUudXNlcm5hbWUsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc3RhdGUuZW1haWxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF19IC8+fSA+XG4gICAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBpZD1cImlkX3Bhc3N3b3JkXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICAgIGFyaWEtZGVzY3JpYmVkYnk9XCJpZF9wYXNzd29yZF9zdGF0dXNcIlxuICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdwYXNzd29yZCcpfVxuICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUucGFzc3dvcmR9IC8+XG4gICAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgICAge2NhcHRjaGEuY29tcG9uZW50KHtcbiAgICAgICAgICAgICAgZm9ybTogdGhpcyxcbiAgICAgICAgICAgICAgbGFiZWxDbGFzczogXCJjb2wtc20tNFwiLFxuICAgICAgICAgICAgICBjb250cm9sQ2xhc3M6IFwiY29sLXNtLThcIlxuICAgICAgICAgICAgfSl9XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWZvb3RlclwiPlxuICAgICAgICAgICAge3RoaXMuZ2V0TGVnYWxGb290Tm90ZSgpfVxuICAgICAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeVwiIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICAgICAge2dldHRleHQoXCJSZWdpc3RlciBhY2NvdW50XCIpfVxuICAgICAgICAgICAgPC9CdXR0b24+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZm9ybT5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBSZWdpc3RlckNvbXBsZXRlIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0TGVhZCgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5hY3RpdmF0aW9uID09PSAndXNlcicpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiJSh1c2VybmFtZSlzLCB5b3VyIGFjY291bnQgaGFzIGJlZW4gY3JlYXRlZCBidXQgeW91IG5lZWQgdG8gYWN0aXZhdGUgaXQgYmVmb3JlIHlvdSB3aWxsIGJlIGFibGUgdG8gc2lnbiBpbi5cIik7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICdhZG1pbicpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiJSh1c2VybmFtZSlzLCB5b3VyIGFjY291bnQgaGFzIGJlZW4gY3JlYXRlZCBidXQgYm9hcmQgYWRtaW5pc3RyYXRvciB3aWxsIGhhdmUgdG8gYWN0aXZhdGUgaXQgYmVmb3JlIHlvdSB3aWxsIGJlIGFibGUgdG8gc2lnbiBpbi5cIik7XG4gICAgfVxuICB9XG5cbiAgZ2V0U3Vic2NyaXB0KCkge1xuICAgIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICd1c2VyJykge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCJXZSBoYXZlIHNlbnQgYW4gZS1tYWlsIHRvICUoZW1haWwpcyB3aXRoIGxpbmsgdGhhdCB5b3UgaGF2ZSB0byBjbGljayB0byBhY3RpdmF0ZSB5b3VyIGFjY291bnQuXCIpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5wcm9wcy5hY3RpdmF0aW9uID09PSAnYWRtaW4nKSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIldlIHdpbGwgc2VuZCBhbiBlLW1haWwgdG8gJShlbWFpbClzIHdoZW4gdGhpcyB0YWtlcyBwbGFjZS5cIik7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1kaWFsb2cgbW9kYWwtbWVzc2FnZSBtb2RhbC1yZWdpc3RlclwiXG4gICAgICAgICAgICAgICAgcm9sZT1cImRvY3VtZW50XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWNvbnRlbnRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1oZWFkZXJcIj5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJjbG9zZVwiIGRhdGEtZGlzbWlzcz1cIm1vZGFsXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtbGFiZWw9e2dldHRleHQoXCJDbG9zZVwiKX0+XG4gICAgICAgICAgICA8c3BhbiBhcmlhLWhpZGRlbj1cInRydWVcIj4mdGltZXM7PC9zcGFuPlxuICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgIDxoNCBjbGFzc05hbWU9XCJtb2RhbC10aXRsZVwiPntnZXR0ZXh0KFwiUmVnaXN0cmF0aW9uIGNvbXBsZXRlXCIpfTwvaDQ+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHlcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgICBpbmZvX291dGxpbmVcbiAgICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgICAgICB7aW50ZXJwb2xhdGUoXG4gICAgICAgICAgICAgICAgdGhpcy5nZXRMZWFkKCksXG4gICAgICAgICAgICAgICAgeyd1c2VybmFtZSc6IHRoaXMucHJvcHMudXNlcm5hbWV9LCB0cnVlKX1cbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICAgIDxwPlxuICAgICAgICAgICAgICB7aW50ZXJwb2xhdGUoXG4gICAgICAgICAgICAgICAgdGhpcy5nZXRTdWJzY3JpcHQoKSxcbiAgICAgICAgICAgICAgICB7J2VtYWlsJzogdGhpcy5wcm9wcy5lbWFpbH0sIHRydWUpfVxuICAgICAgICAgICAgPC9wPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2NvbXBsZXRlJzogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBjb21wbGV0ZVJlZ2lzdHJhdGlvbiA9IChhcGlSZXNwb25zZSkgPT4ge1xuICAgIGlmIChhcGlSZXNwb25zZS5hY3RpdmF0aW9uID09PSAnYWN0aXZlJykge1xuICAgICAgbW9kYWwuaGlkZSgpO1xuICAgICAgYXV0aC5zaWduSW4oYXBpUmVzcG9uc2UpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ2NvbXBsZXRlJzogYXBpUmVzcG9uc2VcbiAgICAgIH0pO1xuICAgIH1cbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGlmICh0aGlzLnN0YXRlLmNvbXBsZXRlKSB7XG4gICAgICByZXR1cm4gPFJlZ2lzdGVyQ29tcGxldGUgYWN0aXZhdGlvbj17dGhpcy5zdGF0ZS5jb21wbGV0ZS5hY3RpdmF0aW9ufVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVzZXJuYW1lPXt0aGlzLnN0YXRlLmNvbXBsZXRlLnVzZXJuYW1lfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVtYWlsPXt0aGlzLnN0YXRlLmNvbXBsZXRlLmVtYWlsfSAvPjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIDxSZWdpc3RlckZvcm0gY2FsbGJhY2s9e3RoaXMuY29tcGxldGVSZWdpc3RyYXRpb259Lz47XG4gICAgfVxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgKiBhcyB2YWxpZGF0b3JzIGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcbmltcG9ydCBzaG93QmFubmVkUGFnZSBmcm9tICdtaXNhZ28vdXRpbHMvYmFubmVkLXBhZ2UnO1xuXG5leHBvcnQgY2xhc3MgUmVxdWVzdExpbmtGb3JtIGV4dGVuZHMgRm9ybSB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZSxcblxuICAgICAgJ2VtYWlsJzogJycsXG5cbiAgICAgICd2YWxpZGF0b3JzJzoge1xuICAgICAgICAnZW1haWwnOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy5lbWFpbCgpXG4gICAgICAgIF1cbiAgICAgIH1cbiAgICB9O1xuICB9XG5cbiAgY2xlYW4oKSB7XG4gICAgaWYgKHRoaXMuaXNWYWxpZCgpKSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkVudGVyIGEgdmFsaWQgZW1haWwgYWRkcmVzcy5cIikpO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdChtaXNhZ28uZ2V0KCdTRU5EX0FDVElWQVRJT05fQVBJJyksIHtcbiAgICAgICdlbWFpbCc6IHRoaXMuc3RhdGUuZW1haWxcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3MoYXBpUmVzcG9uc2UpIHtcbiAgICB0aGlzLnByb3BzLmNhbGxiYWNrKGFwaVJlc3BvbnNlKTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChbJ2FscmVhZHlfYWN0aXZlJywgJ2luYWN0aXZlX2FkbWluJ10uaW5kZXhPZihyZWplY3Rpb24uY29kZSkgPiAtMSkge1xuICAgICAgc25hY2tiYXIuaW5mbyhyZWplY3Rpb24uZGV0YWlsKTtcbiAgICB9IGVsc2UgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMyAmJiByZWplY3Rpb24uYmFuKSB7XG4gICAgICBzaG93QmFubmVkUGFnZShyZWplY3Rpb24uYmFuKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXF1ZXN0LWFjdGl2YXRpb24tbGlua1wiPlxuICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fT5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJmb3JtLWdyb3VwXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250cm9sLWlucHV0XCI+XG5cbiAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwidGV4dFwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9e2dldHRleHQoXCJZb3VyIGUtbWFpbCBhZGRyZXNzXCIpfVxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ2VtYWlsJyl9XG4gICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUuZW1haWx9IC8+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICB7Z2V0dGV4dChcIlNlbmQgbGlua1wiKX1cbiAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgIDwvZm9ybT5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgTGlua1NlbnQgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRNZXNzYWdlKCkge1xuICAgIHJldHVybiBpbnRlcnBvbGF0ZShnZXR0ZXh0KFwiQWN0aXZhdGlvbiBsaW5rIHdhcyBzZW50IHRvICUoZW1haWwpc1wiKSwge1xuICAgICAgZW1haWw6IHRoaXMucHJvcHMudXNlci5lbWFpbFxuICAgIH0sIHRydWUpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJ3ZWxsIHdlbGwtZm9ybSB3ZWxsLWZvcm0tcmVxdWVzdC1hY3RpdmF0aW9uLWxpbmsgd2VsbC1kb25lXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImRvbmUtbWVzc2FnZVwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgIGNoZWNrXG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWJvZHlcIj5cbiAgICAgICAgICA8cD5cbiAgICAgICAgICAgIHt0aGlzLmdldE1lc3NhZ2UoKX1cbiAgICAgICAgICA8L3A+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLXByaW1hcnkgYnRuLWJsb2NrXCJcbiAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnByb3BzLmNhbGxiYWNrfT5cbiAgICAgICAgICB7Z2V0dGV4dChcIlJlcXVlc3QgYW5vdGhlciBsaW5rXCIpfVxuICAgICAgICA8L2J1dHRvbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgY29tcGxldGU6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgY29tcGxldGUgPSAoYXBpUmVzcG9uc2UpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIGNvbXBsZXRlOiBhcGlSZXNwb25zZVxuICAgIH0pO1xuICB9O1xuXG4gIHJlc2V0ID0gKCkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgY29tcGxldGU6IGZhbHNlXG4gICAgfSk7XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBpZiAodGhpcy5zdGF0ZS5jb21wbGV0ZSkge1xuICAgICAgcmV0dXJuIDxMaW5rU2VudCB1c2VyPXt0aGlzLnN0YXRlLmNvbXBsZXRlfSBjYWxsYmFjaz17dGhpcy5yZXNldH0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8UmVxdWVzdExpbmtGb3JtIGNhbGxiYWNrPXt0aGlzLmNvbXBsZXRlfSAvPjtcbiAgICB9O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuaW1wb3J0ICogYXMgdmFsaWRhdG9ycyBmcm9tICdtaXNhZ28vdXRpbHMvdmFsaWRhdG9ycyc7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcblxuZXhwb3J0IGNsYXNzIFJlcXVlc3RSZXNldEZvcm0gZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuXG4gICAgICAnZW1haWwnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICdlbWFpbCc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLmVtYWlsKClcbiAgICAgICAgXVxuICAgICAgfVxuICAgIH07XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBpZiAodGhpcy5pc1ZhbGlkKCkpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRW50ZXIgYSB2YWxpZCBlbWFpbCBhZGRyZXNzLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KG1pc2Fnby5nZXQoJ1NFTkRfUEFTU1dPUkRfUkVTRVRfQVBJJyksIHtcbiAgICAgICdlbWFpbCc6IHRoaXMuc3RhdGUuZW1haWxcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3MoYXBpUmVzcG9uc2UpIHtcbiAgICB0aGlzLnByb3BzLmNhbGxiYWNrKGFwaVJlc3BvbnNlKTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChbJ2luYWN0aXZlX3VzZXInLCAnaW5hY3RpdmVfYWRtaW4nXS5pbmRleE9mKHJlamVjdGlvbi5jb2RlKSA+IC0xKSB7XG4gICAgICB0aGlzLnByb3BzLnNob3dJbmFjdGl2ZVBhZ2UocmVqZWN0aW9uKTtcbiAgICB9IGVsc2UgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMyAmJiByZWplY3Rpb24uYmFuKSB7XG4gICAgICBzaG93QmFubmVkUGFnZShyZWplY3Rpb24uYmFuKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXF1ZXN0LXBhc3N3b3JkLXJlc2V0XCI+XG4gICAgICA8Zm9ybSBvblN1Ym1pdD17dGhpcy5oYW5kbGVTdWJtaXR9PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXBcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRyb2wtaW5wdXRcIj5cblxuICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICBwbGFjZWhvbGRlcj17Z2V0dGV4dChcIllvdXIgZS1tYWlsIGFkZHJlc3NcIil9XG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnZW1haWwnKX1cbiAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5lbWFpbH0gLz5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cblxuICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiU2VuZCBsaW5rXCIpfVxuICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgPC9mb3JtPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBMaW5rU2VudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldE1lc3NhZ2UoKSB7XG4gICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCJSZXNldCBwYXNzd29yZCBsaW5rIHdhcyBzZW50IHRvICUoZW1haWwpc1wiKSwge1xuICAgICAgZW1haWw6IHRoaXMucHJvcHMudXNlci5lbWFpbFxuICAgIH0sIHRydWUpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJ3ZWxsIHdlbGwtZm9ybSB3ZWxsLWZvcm0tcmVxdWVzdC1wYXNzd29yZC1yZXNldCB3ZWxsLWRvbmVcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZG9uZS1tZXNzYWdlXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgY2hlY2tcbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgIDxwPlxuICAgICAgICAgICAge3RoaXMuZ2V0TWVzc2FnZSgpfVxuICAgICAgICAgIDwvcD5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMucHJvcHMuY2FsbGJhY2t9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiUmVxdWVzdCBhbm90aGVyIGxpbmtcIil9XG4gICAgICAgIDwvYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIEFjY291bnRJbmFjdGl2ZVBhZ2UgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRBY3RpdmF0ZUJ1dHRvbigpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5hY3RpdmF0aW9uID09PSAnaW5hY3RpdmVfdXNlcicpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8cD5cbiAgICAgICAgPGEgaHJlZj17bWlzYWdvLmdldCgnUkVRVUVTVF9BQ1RJVkFUSU9OX1VSTCcpfT5cbiAgICAgICAgICB7Z2V0dGV4dChcIkFjdGl2YXRlIHlvdXIgYWNjb3VudC5cIil9XG4gICAgICAgIDwvYT5cbiAgICAgIDwvcD47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UgcGFnZS1tZXNzYWdlIHBhZ2UtbWVzc2FnZS1pbmZvIHBhZ2UtZm9yZ290dGVuLXBhc3N3b3JkLWluYWN0aXZlXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtcGFuZWxcIj5cblxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgIGluZm9fb3V0bGluZVxuICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDwvZGl2PlxuXG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWJvZHlcIj5cbiAgICAgICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICAgICAge2dldHRleHQoXCJZb3VyIGFjY291bnQgaXMgaW5hY3RpdmUuXCIpfVxuICAgICAgICAgICAgPC9wPlxuICAgICAgICAgICAgPHA+XG4gICAgICAgICAgICAgIHt0aGlzLnByb3BzLm1lc3NhZ2V9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgICB7dGhpcy5nZXRBY3RpdmF0ZUJ1dHRvbigpfVxuICAgICAgICAgIDwvZGl2PlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBjb21wbGV0ZTogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBjb21wbGV0ZSA9IChhcGlSZXNwb25zZSkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgY29tcGxldGU6IGFwaVJlc3BvbnNlXG4gICAgfSk7XG4gIH07XG5cbiAgcmVzZXQgPSAoKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBjb21wbGV0ZTogZmFsc2VcbiAgICB9KTtcbiAgfTtcblxuICBzaG93SW5hY3RpdmVQYWdlKGFwaVJlc3BvbnNlKSB7XG4gICAgUmVhY3RET00ucmVuZGVyKFxuICAgICAgPEFjY291bnRJbmFjdGl2ZVBhZ2UgYWN0aXZhdGlvbj17YXBpUmVzcG9uc2UuY29kZX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgIG1lc3NhZ2U9e2FwaVJlc3BvbnNlLmRldGFpbH0gLz4sXG4gICAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncGFnZS1tb3VudCcpXG4gICAgKTtcbiAgfVxuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgaWYgKHRoaXMuc3RhdGUuY29tcGxldGUpIHtcbiAgICAgIHJldHVybiA8TGlua1NlbnQgdXNlcj17dGhpcy5zdGF0ZS5jb21wbGV0ZX0gY2FsbGJhY2s9e3RoaXMucmVzZXR9IC8+O1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gPFJlcXVlc3RSZXNldEZvcm0gY2FsbGJhY2s9e3RoaXMuY29tcGxldGV9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc2hvd0luYWN0aXZlUGFnZT17dGhpcy5zaG93SW5hY3RpdmVQYWdlfSAvPjtcbiAgICB9O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBTaWduSW5Nb2RhbCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9zaWduLWluLmpzJztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBhdXRoIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hdXRoJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuaW1wb3J0ICogYXMgdmFsaWRhdG9ycyBmcm9tICdtaXNhZ28vdXRpbHMvdmFsaWRhdG9ycyc7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcblxuZXhwb3J0IGNsYXNzIFJlc2V0UGFzc3dvcmRGb3JtIGV4dGVuZHMgRm9ybSB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZSxcblxuICAgICAgJ3Bhc3N3b3JkJzogJycsXG5cbiAgICAgICd2YWxpZGF0b3JzJzoge1xuICAgICAgICAncGFzc3dvcmQnOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy5wYXNzd29yZE1pbkxlbmd0aChtaXNhZ28uZ2V0KCdTRVRUSU5HUycpKVxuICAgICAgICBdXG4gICAgICB9XG4gICAgfTtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWQoKSkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSBlbHNlIHtcbiAgICAgIGlmICh0aGlzLnN0YXRlLnBhc3N3b3JkLnRyaW0oKS5sZW5ndGgpIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IodGhpcy5zdGF0ZS5lcnJvcnMucGFzc3dvcmRbMF0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkVudGVyIG5ldyBwYXNzd29yZC5cIikpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdChtaXNhZ28uZ2V0KCdDSEFOR0VfUEFTU1dPUkRfQVBJJyksIHtcbiAgICAgICdwYXNzd29yZCc6IHRoaXMuc3RhdGUucGFzc3dvcmRcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3MoYXBpUmVzcG9uc2UpIHtcbiAgICB0aGlzLnByb3BzLmNhbGxiYWNrKGFwaVJlc3BvbnNlKTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDMgJiYgcmVqZWN0aW9uLmJhbikge1xuICAgICAgc2hvd0Jhbm5lZFBhZ2UocmVqZWN0aW9uLmJhbik7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmFwaUVycm9yKHJlamVjdGlvbik7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJ3ZWxsIHdlbGwtZm9ybSB3ZWxsLWZvcm0tcmVzZXQtcGFzc3dvcmRcIj5cbiAgICAgIDxmb3JtIG9uU3VibWl0PXt0aGlzLmhhbmRsZVN1Ym1pdH0+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZm9ybS1ncm91cFwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udHJvbC1pbnB1dFwiPlxuXG4gICAgICAgICAgICA8aW5wdXQgdHlwZT1cInBhc3N3b3JkXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICBwbGFjZWhvbGRlcj17Z2V0dGV4dChcIkVudGVyIG5ldyBwYXNzd29yZFwiKX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdwYXNzd29yZCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnBhc3N3b3JkfSAvPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuXG4gICAgICAgIDxCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXByaW1hcnkgYnRuLWJsb2NrXCJcbiAgICAgICAgICAgICAgICBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAge2dldHRleHQoXCJDaGFuZ2UgcGFzc3dvcmRcIil9XG4gICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICA8L2Zvcm0+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFBhc3N3b3JkQ2hhbmdlZFBhZ2UgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRNZXNzYWdlKCkge1xuICAgIHJldHVybiBpbnRlcnBvbGF0ZShnZXR0ZXh0KFwiJSh1c2VybmFtZSlzLCB5b3VyIHBhc3N3b3JkIGhhcyBiZWVuIGNoYW5nZWQgc3VjY2Vzc2Z1bGx5LlwiKSwge1xuICAgICAgdXNlcm5hbWU6IHRoaXMucHJvcHMudXNlci51c2VybmFtZVxuICAgIH0sIHRydWUpO1xuICB9XG5cbiAgc2hvd1NpZ25JbigpIHtcbiAgICBtb2RhbC5zaG93KFNpZ25Jbk1vZGFsKTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwicGFnZSBwYWdlLW1lc3NhZ2UgcGFnZS1tZXNzYWdlLXN1Y2Nlc3MgcGFnZS1mb3Jnb3R0ZW4tcGFzc3dvcmQtY2hhbmdlZFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLXBhbmVsXCI+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgICBjaGVja1xuICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDwvZGl2PlxuXG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWJvZHlcIj5cbiAgICAgICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICAgICAge3RoaXMuZ2V0TWVzc2FnZSgpfVxuICAgICAgICAgICAgPC9wPlxuICAgICAgICAgICAgPHA+XG4gICAgICAgICAgICAgIHtnZXR0ZXh0KFwiWW91IHdpbGwgaGF2ZSB0byBzaWduIGluIHVzaW5nIG5ldyBwYXNzd29yZCBiZWZvcmUgY29udGludWluZy5cIil9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgICA8cD5cbiAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIGJ0bi1wcmltYXJ5XCIgb25DbGljaz17dGhpcy5zaG93U2lnbklufT5cbiAgICAgICAgICAgICAgICB7Z2V0dGV4dChcIlNpZ24gaW5cIil9XG4gICAgICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgICAgPC9wPlxuICAgICAgICAgIDwvZGl2PlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBsZXRlID0gKGFwaVJlc3BvbnNlKSA9PiB7XG4gICAgYXV0aC5zb2Z0U2lnbk91dCgpO1xuXG4gICAgLy8gbnVrZSBcInJlZGlyZWN0X3RvXCIgZmllbGQgc28gd2UgZG9uJ3QgZW5kXG4gICAgLy8gY29taW5nIGJhY2sgdG8gZXJyb3IgcGFnZSBhZnRlciBzaWduIGluXG4gICAgJCgnI2hpZGRlbi1sb2dpbi1mb3JtIGlucHV0W25hbWU9XCJyZWRpcmVjdF90b1wiXScpLnJlbW92ZSgpO1xuXG4gICAgUmVhY3RET00ucmVuZGVyKFxuICAgICAgPFBhc3N3b3JkQ2hhbmdlZFBhZ2UgdXNlcj17YXBpUmVzcG9uc2V9IC8+LFxuICAgICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3BhZ2UtbW91bnQnKVxuICAgICk7XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPFJlc2V0UGFzc3dvcmRGb3JtIGNhbGxiYWNrPXt0aGlzLmNvbXBsZXRlfSAvPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRDaG9pY2UoKSB7XG4gICAgbGV0IGNob2ljZSA9IG51bGw7XG4gICAgdGhpcy5wcm9wcy5jaG9pY2VzLm1hcCgoaXRlbSkgPT4ge1xuICAgICAgaWYgKGl0ZW0udmFsdWUgPT09IHRoaXMucHJvcHMudmFsdWUpIHtcbiAgICAgICAgY2hvaWNlID0gaXRlbTtcbiAgICAgIH1cbiAgICB9KTtcbiAgICByZXR1cm4gY2hvaWNlO1xuICB9XG5cbiAgZ2V0SWNvbigpIHtcbiAgICByZXR1cm4gdGhpcy5nZXRDaG9pY2UoKS5pY29uO1xuICB9XG5cbiAgZ2V0TGFiZWwoKSB7XG4gICAgcmV0dXJuIHRoaXMuZ2V0Q2hvaWNlKCkubGFiZWw7XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNoYW5nZSA9ICh2YWx1ZSkgPT4ge1xuICAgIHJldHVybiAoKSA9PiB7XG4gICAgICB0aGlzLnByb3BzLm9uQ2hhbmdlKHtcbiAgICAgICAgdGFyZ2V0OiB7XG4gICAgICAgICAgdmFsdWU6IHZhbHVlXG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH07XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJidG4tZ3JvdXAgYnRuLXNlbGVjdC1ncm91cFwiPlxuICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCJcbiAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuIGJ0bi1zZWxlY3QgZHJvcGRvd24tdG9nZ2xlXCJcbiAgICAgICAgICAgICAgaWQ9e3RoaXMucHJvcHMuaWQgfHwgbnVsbH1cbiAgICAgICAgICAgICAgZGF0YS10b2dnbGU9XCJkcm9wZG93blwiXG4gICAgICAgICAgICAgIGFyaWEtaGFzcG9wdXA9XCJ0cnVlXCJcbiAgICAgICAgICAgICAgYXJpYS1leHBhbmRlZD1cImZhbHNlXCJcbiAgICAgICAgICAgICAgYXJpYS1kZXNjcmliZWRieT17dGhpcy5wcm9wc1snYXJpYS1kZXNjcmliZWRieSddIHx8IG51bGx9XG4gICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnByb3BzLmRpc2FibGVkIHx8IGZhbHNlfT5cbiAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgIHt0aGlzLmdldEljb24oKX1cbiAgICAgICAgPC9zcGFuPlxuICAgICAgICB7dGhpcy5nZXRMYWJlbCgpfVxuICAgICAgPC9idXR0b24+XG4gICAgICA8dWwgY2xhc3NOYW1lPVwiZHJvcGRvd24tbWVudVwiPlxuICAgICAgICB7dGhpcy5wcm9wcy5jaG9pY2VzLm1hcCgoaXRlbSwgaSkgPT4ge1xuICAgICAgICAgIHJldHVybiA8bGkga2V5PXtpfT5cbiAgICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0bi1saW5rXCJcbiAgICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5jaGFuZ2UoaXRlbS52YWx1ZSl9PlxuICAgICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgICAge2l0ZW0uaWNvbn1cbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgICB7aXRlbS5sYWJlbH1cbiAgICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgIDwvbGk+O1xuICAgICAgICB9KX1cbiAgICAgIDwvdWw+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuICAgICAgJ3Nob3dBY3RpdmF0aW9uJzogZmFsc2UsXG5cbiAgICAgICd1c2VybmFtZSc6ICcnLFxuICAgICAgJ3Bhc3N3b3JkJzogJycsXG5cbiAgICAgICd2YWxpZGF0b3JzJzoge1xuICAgICAgICAndXNlcm5hbWUnOiBbXSxcbiAgICAgICAgJ3Bhc3N3b3JkJzogW11cbiAgICAgIH1cbiAgICB9O1xuICB9XG5cbiAgY2xlYW4oKSB7XG4gICAgaWYgKCF0aGlzLmlzVmFsaWQoKSkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZpbGwgb3V0IGJvdGggZmllbGRzLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdChtaXNhZ28uZ2V0KCdBVVRIX0FQSScpLCB7XG4gICAgICAndXNlcm5hbWUnOiB0aGlzLnN0YXRlLnVzZXJuYW1lLFxuICAgICAgJ3Bhc3N3b3JkJzogdGhpcy5zdGF0ZS5wYXNzd29yZFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcygpIHtcbiAgICBsZXQgZm9ybSA9ICQoJyNoaWRkZW4tbG9naW4tZm9ybScpO1xuXG4gICAgZm9ybS5hcHBlbmQoJzxpbnB1dCB0eXBlPVwidGV4dFwiIG5hbWU9XCJ1c2VybmFtZVwiIC8+Jyk7XG4gICAgZm9ybS5hcHBlbmQoJzxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBuYW1lPVwicGFzc3dvcmRcIiAvPicpO1xuXG4gICAgLy8gZmlsbCBvdXQgZm9ybSB3aXRoIHVzZXIgY3JlZGVudGlhbHMgYW5kIHN1Ym1pdCBpdCwgdGhpcyB3aWxsIHRlbGxcbiAgICAvLyBNaXNhZ28gdG8gcmVkaXJlY3QgdXNlciBiYWNrIHRvIHJpZ2h0IHBhZ2UsIGFuZCB3aWxsIHRyaWdnZXIgYnJvd3NlcidzXG4gICAgLy8ga2V5IHJpbmcgZmVhdHVyZVxuICAgIGZvcm0uZmluZCgnaW5wdXRbdHlwZT1cImhpZGRlblwiXScpLnZhbChhamF4LmdldENzcmZUb2tlbigpKTtcbiAgICBmb3JtLmZpbmQoJ2lucHV0W25hbWU9XCJyZWRpcmVjdF90b1wiXScpLnZhbCh3aW5kb3cubG9jYXRpb24ucGF0aG5hbWUpO1xuICAgIGZvcm0uZmluZCgnaW5wdXRbbmFtZT1cInVzZXJuYW1lXCJdJykudmFsKHRoaXMuc3RhdGUudXNlcm5hbWUpO1xuICAgIGZvcm0uZmluZCgnaW5wdXRbbmFtZT1cInBhc3N3b3JkXCJdJykudmFsKHRoaXMuc3RhdGUucGFzc3dvcmQpO1xuICAgIGZvcm0uc3VibWl0KCk7XG5cbiAgICAvLyBrZWVwIGZvcm0gbG9hZGluZ1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ2lzTG9hZGluZyc6IHRydWVcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgIGlmIChyZWplY3Rpb24uY29kZSA9PT0gJ2luYWN0aXZlX2FkbWluJykge1xuICAgICAgICBzbmFja2Jhci5pbmZvKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgICAgfSBlbHNlIGlmIChyZWplY3Rpb24uY29kZSA9PT0gJ2luYWN0aXZlX3VzZXInKSB7XG4gICAgICAgIHNuYWNrYmFyLmluZm8ocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICdzaG93QWN0aXZhdGlvbic6IHRydWVcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2UgaWYgKHJlamVjdGlvbi5jb2RlID09PSAnYmFubmVkJykge1xuICAgICAgICBzaG93QmFubmVkUGFnZShyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgICAgbW9kYWwuaGlkZSgpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDMgJiYgcmVqZWN0aW9uLmJhbikge1xuICAgICAgc2hvd0Jhbm5lZFBhZ2UocmVqZWN0aW9uLmJhbik7XG4gICAgICBtb2RhbC5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmFwaUVycm9yKHJlamVjdGlvbik7XG4gICAgfVxuICB9XG5cbiAgZ2V0QWN0aXZhdGlvbkJ1dHRvbigpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5zaG93QWN0aXZhdGlvbikge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxhIGhyZWY9e21pc2Fnby5nZXQoJ1JFUVVFU1RfQUNUSVZBVElPTl9VUkwnKX1cbiAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4gYnRuLXN1Y2Nlc3MgYnRuLWJsb2NrXCI+XG4gICAgICAgICB7Z2V0dGV4dChcIkFjdGl2YXRlIGFjY291bnRcIil9XG4gICAgICA8L2E+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1kaWFsb2cgbW9kYWwtc20gbW9kYWwtc2lnbi1pblwiXG4gICAgICAgICAgICAgICAgcm9sZT1cImRvY3VtZW50XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWNvbnRlbnRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1oZWFkZXJcIj5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJjbG9zZVwiIGRhdGEtZGlzbWlzcz1cIm1vZGFsXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtbGFiZWw9e2dldHRleHQoXCJDbG9zZVwiKX0+XG4gICAgICAgICAgICA8c3BhbiBhcmlhLWhpZGRlbj1cInRydWVcIj4mdGltZXM7PC9zcGFuPlxuICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgIDxoNCBjbGFzc05hbWU9XCJtb2RhbC10aXRsZVwiPntnZXR0ZXh0KFwiU2lnbiBpblwiKX08L2g0PlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fT5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHlcIj5cblxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJmb3JtLWdyb3VwXCI+XG4gICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udHJvbC1pbnB1dFwiPlxuICAgICAgICAgICAgICAgIDxpbnB1dCBpZD1cImlkX3VzZXJuYW1lXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCIgdHlwZT1cInRleHRcIlxuICAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiVXNlcm5hbWUgb3IgZS1tYWlsXCIpfVxuICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3VzZXJuYW1lJyl9XG4gICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnVzZXJuYW1lfSAvPlxuICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDwvZGl2PlxuXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXBcIj5cbiAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250cm9sLWlucHV0XCI+XG4gICAgICAgICAgICAgICAgPGlucHV0IGlkPVwiaWRfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIiB0eXBlPVwicGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiUGFzc3dvcmRcIil9XG4gICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgncGFzc3dvcmQnKX1cbiAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUucGFzc3dvcmR9IC8+XG4gICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWZvb3RlclwiPlxuICAgICAgICAgICAge3RoaXMuZ2V0QWN0aXZhdGlvbkJ1dHRvbigpfVxuICAgICAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgICAgICBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAgICAgIHtnZXR0ZXh0KFwiU2lnbiBpblwiKX1cbiAgICAgICAgICAgIDwvQnV0dG9uPlxuICAgICAgICAgICAgPGEgaHJlZj17bWlzYWdvLmdldCgnRk9SR09UVEVOX1BBU1NXT1JEX1VSTCcpfVxuICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuIGJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAgICAge2dldHRleHQoXCJGb3Jnb3QgcGFzc3dvcmQ/XCIpfVxuICAgICAgICAgICAgPC9hPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Zvcm0+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuY29uc3QgVFlQRVNfQ0xBU1NFUyA9IHtcbiAgJ2luZm8nOiAnYWxlcnQtaW5mbycsXG4gICdzdWNjZXNzJzogJ2FsZXJ0LXN1Y2Nlc3MnLFxuICAnd2FybmluZyc6ICdhbGVydC13YXJuaW5nJyxcbiAgJ2Vycm9yJzogJ2FsZXJ0LWRhbmdlcidcbn07XG4vKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG5leHBvcnQgY2xhc3MgU25hY2tiYXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRTbmFja2JhckNsYXNzKCkge1xuICAgIGxldCBzbmFja2JhckNsYXNzID0gJ2FsZXJ0cy1zbmFja2Jhcic7XG4gICAgaWYgKHRoaXMucHJvcHMuaXNWaXNpYmxlKSB7XG4gICAgICBzbmFja2JhckNsYXNzICs9ICcgaW4nO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2JhckNsYXNzICs9ICcgb3V0JztcbiAgICB9XG4gICAgcmV0dXJuIHNuYWNrYmFyQ2xhc3M7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRTbmFja2JhckNsYXNzKCl9PlxuICAgICAgPHAgY2xhc3NOYW1lPXsnYWxlcnQgJyArIFRZUEVTX0NMQVNTRVNbdGhpcy5wcm9wcy50eXBlXX0+XG4gICAgICAgIHt0aGlzLnByb3BzLm1lc3NhZ2V9XG4gICAgICA8L3A+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4gc3RhdGUuc25hY2tiYXI7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEF2YXRhciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdmF0YXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWdpc3RlckJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9yZWdpc3Rlci1idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBTaWduSW5Nb2RhbCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9zaWduLWluLmpzJztcbmltcG9ydCBkcm9wZG93biBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9iaWxlLW5hdmJhci1kcm9wZG93bic7XG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcblxuZXhwb3J0IGNsYXNzIEd1ZXN0TWVudSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHNob3dTaWduSW5Nb2RhbCgpIHtcbiAgICBtb2RhbC5zaG93KFNpZ25Jbk1vZGFsKTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51IHVzZXItZHJvcGRvd24gZHJvcGRvd24tbWVudS1yaWdodFwiXG4gICAgICAgICAgICAgICByb2xlPVwibWVudVwiPlxuICAgICAgPGxpIGNsYXNzTmFtZT1cImd1ZXN0LXByZXZpZXdcIj5cbiAgICAgICAgPGg0PntnZXR0ZXh0KFwiWW91IGFyZSBicm93c2luZyBhcyBndWVzdC5cIil9PC9oND5cbiAgICAgICAgPHA+XG4gICAgICAgICAge2dldHRleHQoJ1NpZ24gaW4gb3IgcmVnaXN0ZXIgdG8gc3RhcnQgYW5kIHBhcnRpY2lwYXRlIGluIGRpc2N1c3Npb25zLicpfVxuICAgICAgICA8L3A+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicm93XCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wteHMtNlwiPlxuXG4gICAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLWRlZmF1bHQgYnRuLWJsb2NrXCJcbiAgICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5zaG93U2lnbkluTW9kYWx9PlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIlNpZ24gaW5cIil9XG4gICAgICAgICAgICA8L2J1dHRvbj5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLXhzLTZcIj5cblxuICAgICAgICAgICAgPFJlZ2lzdGVyQnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIlJlZ2lzdGVyXCIpfVxuICAgICAgICAgICAgPC9SZWdpc3RlckJ1dHRvbj5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvbGk+XG4gICAgPC91bD47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgR3Vlc3ROYXYgZXh0ZW5kcyBHdWVzdE1lbnUge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm5hdiBuYXYtZ3Vlc3RcIj5cbiAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBuYXZiYXItYnRuIGJ0bi1kZWZhdWx0XCJcbiAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5zaG93U2lnbkluTW9kYWx9PlxuICAgICAgICB7Z2V0dGV4dChcIlNpZ24gaW5cIil9XG4gICAgICA8L2J1dHRvbj5cbiAgICAgIDxSZWdpc3RlckJ1dHRvbiBjbGFzc05hbWU9XCJuYXZiYXItYnRuIGJ0bi1wcmltYXJ5XCI+XG4gICAgICAgIHtnZXR0ZXh0KFwiUmVnaXN0ZXJcIil9XG4gICAgICA8L1JlZ2lzdGVyQnV0dG9uPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBDb21wYWN0R3Vlc3ROYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBzaG93R3Vlc3RNZW51KCkge1xuICAgIGRyb3Bkb3duLnNob3coR3Vlc3RNZW51KTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIG9uQ2xpY2s9e3RoaXMuc2hvd0d1ZXN0TWVudX0+XG4gICAgICA8QXZhdGFyIHNpemU9XCI2NFwiIC8+XG4gICAgPC9idXR0b24+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBHdWVzdE5hdiwgQ29tcGFjdEd1ZXN0TmF2IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvdXNlci1tZW51L2d1ZXN0LW5hdic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHsgVXNlck5hdiwgQ29tcGFjdFVzZXJOYXZ9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3VzZXItbWVudS91c2VyLW5hdic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgVXNlck1lbnUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGlmICh0aGlzLnByb3BzLmlzQXV0aGVudGljYXRlZCkge1xuICAgICAgcmV0dXJuIDxVc2VyTmF2IHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8R3Vlc3ROYXYgLz47XG4gICAgfVxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIENvbXBhY3RVc2VyTWVudSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgaWYgKHRoaXMucHJvcHMuaXNBdXRoZW50aWNhdGVkKSB7XG4gICAgICByZXR1cm4gPENvbXBhY3RVc2VyTmF2IHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8Q29tcGFjdEd1ZXN0TmF2IC8+O1xuICAgIH1cbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzZWxlY3Qoc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLmF1dGg7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCBBdmF0YXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYXZhdGFyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQ2hhbmdlQXZhdGFyTW9kYWwsIHsgc2VsZWN0IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9yb290JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGRyb3Bkb3duIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2JpbGUtbmF2YmFyLWRyb3Bkb3duJztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuXG5leHBvcnQgY2xhc3MgVXNlck1lbnUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBsb2dvdXQoKSB7XG4gICAgbGV0IGRlY2lzaW9uID0gY29uZmlybShnZXR0ZXh0KFwiQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIHNpZ24gb3V0P1wiKSk7XG4gICAgaWYgKGRlY2lzaW9uKSB7XG4gICAgICAkKCcjaGlkZGVuLWxvZ291dC1mb3JtJykuc3VibWl0KCk7XG4gICAgfVxuICB9XG5cbiAgY2hhbmdlQXZhdGFyKCkge1xuICAgIG1vZGFsLnNob3coY29ubmVjdChzZWxlY3QpKENoYW5nZUF2YXRhck1vZGFsKSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8dWwgY2xhc3NOYW1lPVwiZHJvcGRvd24tbWVudSB1c2VyLWRyb3Bkb3duIGRyb3Bkb3duLW1lbnUtcmlnaHRcIlxuICAgICAgICAgICAgICAgcm9sZT1cIm1lbnVcIj5cbiAgICAgIDxsaSBjbGFzc05hbWU9XCJkcm9wZG93bi1oZWFkZXJcIj5cbiAgICAgICAgPHN0cm9uZz57dGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lfTwvc3Ryb25nPlxuICAgICAgPC9saT5cbiAgICAgIDxsaSBjbGFzc05hbWU9XCJkaXZpZGVyXCIgLz5cbiAgICAgIDxsaT5cbiAgICAgICAgPGEgaHJlZj17dGhpcy5wcm9wcy51c2VyLmFic29sdXRlX3VybH0+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPmFjY291bnRfY2lyY2xlPC9zcGFuPlxuICAgICAgICAgIHtnZXR0ZXh0KFwiU2VlIHlvdXIgcHJvZmlsZVwiKX1cbiAgICAgICAgPC9hPlxuICAgICAgPC9saT5cbiAgICAgIDxsaT5cbiAgICAgICAgPGEgaHJlZj17bWlzYWdvLmdldCgnVVNFUkNQX1VSTCcpfT5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+ZG9uZV9hbGw8L3NwYW4+XG4gICAgICAgICAge2dldHRleHQoXCJDaGFuZ2Ugb3B0aW9uc1wiKX1cbiAgICAgICAgPC9hPlxuICAgICAgPC9saT5cbiAgICAgIDxsaT5cbiAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuLWxpbmtcIiBvbkNsaWNrPXt0aGlzLmNoYW5nZUF2YXRhcn0+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPnBvcnRyYWl0PC9zcGFuPlxuICAgICAgICAgIHtnZXR0ZXh0KFwiQ2hhbmdlIGF2YXRhclwiKX1cbiAgICAgICAgPC9idXR0b24+XG4gICAgICA8L2xpPlxuICAgICAgPGxpIGNsYXNzTmFtZT1cImRpdmlkZXJcIiAvPlxuICAgICAgPGxpIGNsYXNzTmFtZT1cImRyb3Bkb3duLWZvb3RlclwiPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBidG4tZGVmYXVsdCBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5sb2dvdXR9PlxuICAgICAgICAgICAge2dldHRleHQoXCJMb2cgb3V0XCIpfVxuICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgPC9saT5cbiAgICA8L3VsPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBVc2VyTmF2IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPHVsIGNsYXNzTmFtZT1cInVsIG5hdiBuYXZiYXItbmF2IG5hdi11c2VyXCI+XG4gICAgICA8bGkgY2xhc3NOYW1lPVwiZHJvcGRvd25cIj5cbiAgICAgICAgPGEgaHJlZj17dGhpcy5wcm9wcy51c2VyLmFic29sdXRlX3VybH0gY2xhc3NOYW1lPVwiZHJvcGRvd24tdG9nZ2xlXCJcbiAgICAgICAgICAgZGF0YS10b2dnbGU9XCJkcm9wZG93blwiIGFyaWEtaGFzcG9wdXA9XCJ0cnVlXCIgYXJpYS1leHBhbmRlZD1cImZhbHNlXCJcbiAgICAgICAgICAgcm9sZT1cImJ1dHRvblwiPlxuICAgICAgICAgIDxBdmF0YXIgdXNlcj17dGhpcy5wcm9wcy51c2VyfSBzaXplPVwiNjRcIiAvPlxuICAgICAgICA8L2E+XG4gICAgICAgIDxVc2VyTWVudSB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IC8+XG4gICAgICA8L2xpPlxuICAgIDwvdWw+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdFVzZXJNZW51KHN0YXRlKSB7XG4gIHJldHVybiB7dXNlcjogc3RhdGUuYXV0aC51c2VyfTtcbn1cblxuZXhwb3J0IGNsYXNzIENvbXBhY3RVc2VyTmF2IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgc2hvd1VzZXJNZW51KCkge1xuICAgIGRyb3Bkb3duLnNob3dDb25uZWN0ZWQoJ3VzZXItbWVudScsIGNvbm5lY3Qoc2VsZWN0VXNlck1lbnUpKFVzZXJNZW51KSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBvbkNsaWNrPXt0aGlzLnNob3dVc2VyTWVudX0+XG4gICAgICA8QXZhdGFyIHVzZXI9e3RoaXMucHJvcHMudXNlcn0gc2l6ZT1cIjY0XCIgLz5cbiAgICA8L2J1dHRvbj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IExpbmsgfSBmcm9tICdyZWFjdC1yb3V0ZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBBdmF0YXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYXZhdGFyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgeyBkZWh5ZHJhdGUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcnMnO1xuaW1wb3J0IHRpdGxlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9wYWdlLXRpdGxlJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgY2xhc3MgQWN0aXZlUG9zdGVyIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0Q2xhc3NOYW1lKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnJhbmsuY3NzX2NsYXNzKSB7XG4gICAgICByZXR1cm4gXCJsaXN0LWdyb3VwLWl0ZW0gbGlzdC1ncm91cC1yYW5rLVwiICsgdGhpcy5wcm9wcy5yYW5rLmNzc19jbGFzcztcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIFwibGlzdC1ncm91cC1pdGVtXCI7XG4gICAgfVxuICB9XG5cbiAgZ2V0UmFua05hbWUoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMucmFuay5pc190YWIpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIGxldCByYW5rVXJsID0gbWlzYWdvLmdldCgnVVNFUlNfTElTVF9VUkwnKSArIHRoaXMucHJvcHMucmFuay5zbHVnICsgJy8nO1xuICAgICAgcmV0dXJuIDxMaW5rIHRvPXtyYW5rVXJsfSBjbGFzc05hbWU9XCJyYW5rLW5hbWVcIj5cbiAgICAgICAge3RoaXMucHJvcHMucmFuay5uYW1lfVxuICAgICAgPC9MaW5rPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8c3BhbiBjbGFzc05hbWU9XCJyYW5rLW5hbWVcIj5cbiAgICAgICAge3RoaXMucHJvcHMucmFuay5uYW1lfVxuICAgICAgPC9zcGFuPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfVxuICB9XG5cbiAgZ2V0VXNlclRpdGxlKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnVzZXIudGl0bGUpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8c3BhbiBjbGFzc05hbWU9XCJ1c2VyLXRpdGxlXCI+XG4gICAgICAgIHt0aGlzLnByb3BzLnVzZXIudGl0bGV9XG4gICAgICA8L3NwYW4+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGxpIGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzc05hbWUoKX0+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInJhbmstdXNlci1hdmF0YXJcIj5cbiAgICAgICAgPGEgaHJlZj17dGhpcy5wcm9wcy51c2VyLmFic29sdXRlX3VybH0+XG4gICAgICAgICAgPEF2YXRhciB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IHNpemU9XCI1MFwiIC8+XG4gICAgICAgIDwvYT5cbiAgICAgIDwvZGl2PlxuXG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInJhbmstdXNlclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVzZXItbmFtZVwiPlxuICAgICAgICAgIDxhIGhyZWY9e3RoaXMucHJvcHMudXNlci5hYnNvbHV0ZV91cmx9IGNsYXNzTmFtZT1cIml0ZW0tdGl0bGVcIj5cbiAgICAgICAgICAgIHt0aGlzLnByb3BzLnVzZXIudXNlcm5hbWV9XG4gICAgICAgICAgPC9hPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAge3RoaXMuZ2V0UmFua05hbWUoKX1cbiAgICAgICAge3RoaXMuZ2V0VXNlclRpdGxlKCl9XG4gICAgICA8L2Rpdj5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyYW5rLXBvc2l0aW9uXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwic3RhdC12YWx1ZVwiPiN7dGhpcy5wcm9wcy5jb3VudGVyfTwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInRleHQtbXV0ZWRcIj57Z2V0dGV4dChcIlJhbmtcIil9PC9kaXY+XG4gICAgICA8L2Rpdj5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyYW5rLXBvc3RzLWNvdW50ZWRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJzdGF0LXZhbHVlXCI+e3RoaXMucHJvcHMudXNlci5tZXRhLnNjb3JlfTwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInRleHQtbXV0ZWRcIj57Z2V0dGV4dChcIlJhbmtlZCBwb3N0c1wiKX08L2Rpdj5cbiAgICAgIDwvZGl2PlxuXG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cInJhbmstcG9zdHMtdG90YWxcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJzdGF0LXZhbHVlXCI+e3RoaXMucHJvcHMudXNlci5wb3N0c308L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ0ZXh0LW11dGVkXCI+e2dldHRleHQoXCJUb3RhbCBwb3N0c1wiKX08L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvbGk+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIEFjdGl2ZVBvc3RlcnMgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRMZWFkTWVzc2FnZSgpIHtcbiAgICBsZXQgbWVzc2FnZSA9IG5nZXR0ZXh0KFxuICAgICAgICBcIiUocG9zdGVycylzIG1vc3QgYWN0aXZlIHBvc3RlciBmcm9tIGxhc3QgJShkYXlzKXMgZGF5cy5cIixcbiAgICAgICAgXCIlKHBvc3RlcnMpcyBtb3N0IGFjdGl2ZSBwb3N0ZXJzIGZyb20gbGFzdCAlKGRheXMpcyBkYXlzLlwiLFxuICAgICAgICB0aGlzLnByb3BzLmNvdW50KTtcblxuICAgIHJldHVybiBpbnRlcnBvbGF0ZShtZXNzYWdlLCB7XG4gICAgICAgIHBvc3RlcnM6IHRoaXMucHJvcHMuY291bnQsXG4gICAgICAgIGRheXM6IHRoaXMucHJvcHMudHJhY2tlZFBlcmlvZFxuICAgICAgfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImFjdGl2ZS1wb3N0ZXJzLWxpc3RcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICB7dGhpcy5nZXRMZWFkTWVzc2FnZSgpfVxuICAgICAgICA8L3A+XG5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJhY3RpdmUtcG9zdGVycyB1aS1yZWFkeVwiPlxuICAgICAgICAgIDx1bCBjbGFzc05hbWU9XCJsaXN0LWdyb3VwXCI+XG4gICAgICAgICAgICB7dGhpcy5wcm9wcy51c2Vycy5tYXAoKHVzZXIsIGkpID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIDxBY3RpdmVQb3N0ZXIgdXNlcj17dXNlcn1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmFuaz17dXNlci5yYW5rfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb3VudGVyPXtpICsgMX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAga2V5PXt1c2VyLmlkfSAvPjtcbiAgICAgICAgICAgIH0pfVxuICAgICAgICAgIDwvdWw+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIEFjdGl2ZVBvc3RlcnNMb2FkaW5nIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJhY3RpdmUtcG9zdGVycy1saXN0XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgICBUaGlzIGlzIFVJIHByZXZpZXchXG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgTm9BY3RpdmVQb3N0ZXJzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0RW1wdHlNZXNzYWdlKCkge1xuICAgIHJldHVybiBpbnRlcnBvbGF0ZShcbiAgICAgIGdldHRleHQoXCJObyB1c2VycyBoYXZlIHBvc3RlZCBhbnkgbmV3IG1lc3NhZ2VzIGR1cmluZyBsYXN0ICUoZGF5cylzIGRheXMuXCIpLFxuICAgICAgeydkYXlzJzogdGhpcy5wcm9wcy50cmFja2VkUGVyaW9kfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImFjdGl2ZS1wb3N0ZXJzLWxpc3RcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj5cbiAgICAgICAgICB7dGhpcy5nZXRFbXB0eU1lc3NhZ2UoKX1cbiAgICAgICAgPC9wPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIGlmIChtaXNhZ28uaGFzKCdVU0VSUycpKSB7XG4gICAgICB0aGlzLmluaXRXaXRoUHJlbG9hZGVkRGF0YShtaXNhZ28ucG9wKCdVU0VSUycpKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5pbml0V2l0aG91dFByZWxvYWRlZERhdGEoKTtcbiAgICB9XG4gIH1cblxuICBpbml0V2l0aFByZWxvYWRlZERhdGEoZGF0YSkge1xuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBpc0xvYWRlZDogdHJ1ZSxcblxuICAgICAgdHJhY2tlZFBlcmlvZDogZGF0YS50cmFja2VkX3BlcmlvZCxcbiAgICAgIGNvdW50OiBkYXRhLmNvdW50XG4gICAgfTtcblxuICAgIHN0b3JlLmRpc3BhdGNoKGRlaHlkcmF0ZShkYXRhLnJlc3VsdHMpKTtcbiAgfVxuXG4gIGluaXRXaXRob3V0UHJlbG9hZGVkRGF0YSgpIHtcbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgaXNMb2FkZWQ6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIHRpdGxlLnNldCh7XG4gICAgICB0aXRsZTogdGhpcy5wcm9wcy5yb3V0ZS5leHRyYS5uYW1lLFxuICAgICAgcGFyZW50OiBnZXR0ZXh0KFwiVXNlcnNcIilcbiAgICB9KTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRlZCkge1xuICAgICAgaWYgKHRoaXMuc3RhdGUuY291bnQgPiAwKSB7XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgICAgcmV0dXJuIDxBY3RpdmVQb3N0ZXJzIHVzZXJzPXt0aGlzLnByb3BzLnVzZXJzfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdHJhY2tlZFBlcmlvZD17dGhpcy5zdGF0ZS50cmFja2VkUGVyaW9kfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY291bnQ9e3RoaXMuc3RhdGUuY291bnR9IC8+O1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgICByZXR1cm4gPE5vQWN0aXZlUG9zdGVycyB0cmFja2VkUGVyaW9kPXt0aGlzLnN0YXRlLnRyYWNrZWRQZXJpb2R9IC8+O1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPEFjdGl2ZVBvc3RlcnNMb2FkaW5nIC8+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9XG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgTGluayB9IGZyb20gJ3JlYWN0LXJvdXRlcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IExpIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2xpJzsgLy9qc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JzsgLy9qc2hpbnQgaWdub3JlOmxpbmVcblxuLy8ganNoaW50IGlnbm9yZTpzdGFydFxubGV0IGxpc3RVcmwgPSBmdW5jdGlvbihiYXNlVXJsLCBsaXN0KSB7XG4gIGxldCB1cmwgPSBiYXNlVXJsO1xuICBpZiAobGlzdC5jb21wb25lbnQgPT09ICdyYW5rJykge1xuICAgIHVybCArPSBsaXN0LnNsdWc7XG4gIH0gZWxzZSB7XG4gICAgdXJsICs9IGxpc3QuY29tcG9uZW50O1xuICB9XG4gIHJldHVybiB1cmwgKyAnLyc7XG59O1xuXG5sZXQgbmF2TGlua3MgPSBmdW5jdGlvbihiYXNlVXJsLCBsaXN0cykge1xuICAgIHJldHVybiBsaXN0cy5tYXAoZnVuY3Rpb24obGlzdCkge1xuICAgICAgbGV0IHVybCA9IGxpc3RVcmwoYmFzZVVybCwgbGlzdCk7XG4gICAgICByZXR1cm4gPExpIHBhdGg9e3VybH1cbiAgICAgICAgICAgICAgICAga2V5PXt1cmx9PlxuICAgICAgICA8TGluayB0bz17dXJsfT5cbiAgICAgICAgICB7bGlzdC5uYW1lfVxuICAgICAgICA8L0xpbms+XG4gICAgICA8L0xpPjtcbiAgfSk7XG59O1xuLy8ganNoaW50IGlnbm9yZTplbmRcblxuZXhwb3J0IGNsYXNzIFRhYnNOYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLy8ganNoaW50IGlnbm9yZTpzdGFydFxuICAgIHJldHVybiA8dWwgY2xhc3NOYW1lPVwibmF2IG5hdi1waWxsc1wiPlxuICAgICAge25hdkxpbmtzKHRoaXMucHJvcHMuYmFzZVVybCwgdGhpcy5wcm9wcy5saXN0cyl9XG4gICAgPC91bD47XG4gICAgLy8ganNoaW50IGlnbm9yZTplbmRcbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgQ29tcGFjdE5hdiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvLyBqc2hpbnQgaWdub3JlOnN0YXJ0XG4gICAgcmV0dXJuIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51XCIgcm9sZT1cIm1lbnVcIj5cbiAgICAgIHtuYXZMaW5rcyh0aGlzLnByb3BzLmJhc2VVcmwsIHRoaXMucHJvcHMubGlzdHMpfVxuICAgIDwvdWw+O1xuICAgIC8vIGpzaGludCBpZ25vcmU6ZW5kXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHRpdGxlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9wYWdlLXRpdGxlJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICB0aXRsZS5zZXQoe1xuICAgICAgdGl0bGU6IHRoaXMucHJvcHMucm91dGUucmFuay5uYW1lLFxuICAgICAgcGFyZW50OiBnZXR0ZXh0KFwiVXNlcnNcIilcbiAgICB9KTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgIEhlbGxvLCB0aGlzIGlzIHVzZXJzIHdpdGggcmFuayBsaXN0IVxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCB7IFRhYnNOYXYsIENvbXBhY3ROYXYgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2Vycy9uYXZzJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQWN0aXZlUG9zdGVycyBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2Vycy9hY3RpdmUtcG9zdGVycyc7XG5pbXBvcnQgUmFuayBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2Vycy9yYW5rJztcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBkcm9wZG93bjogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICB0b2dnbGVOYXYgPSAoKSA9PiB7XG4gICAgaWYgKHRoaXMuc3RhdGUuZHJvcGRvd24pIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICBkcm9wZG93bjogZmFsc2VcbiAgICAgIH0pO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgZHJvcGRvd246IHRydWVcbiAgICAgIH0pO1xuICAgIH1cbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRUb2dnbGVOYXZDbGFzc05hbWUoKSB7XG4gICAgaWYgKHRoaXMuc3RhdGUuZHJvcGRvd24pIHtcbiAgICAgIHJldHVybiAnYnRuIGJ0bi1kZWZhdWx0IGJ0bi1pY29uIG9wZW4nO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gJ2J0biBidG4tZGVmYXVsdCBidG4taWNvbic7XG4gICAgfVxuICB9XG5cbiAgZ2V0Q29tcGFjdE5hdkNsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5kcm9wZG93bikge1xuICAgICAgcmV0dXJuICdjb21wYWN0LW5hdiBvcGVuJztcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuICdjb21wYWN0LW5hdic7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJwYWdlIHBhZ2UtdXNlcnMtbGlzdHNcIj5cblxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwYWdlLWhlYWRlciB0YWJiZWRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cblxuICAgICAgICAgIDxoMT57Z2V0dGV4dChcIlVzZXJzXCIpfTwvaDE+XG5cbiAgICAgICAgICA8YnV0dG9uIGNsYXNzTmFtZT1cImJ0biBidG4tZGVmYXVsdCBidG4taWNvbiBidG4tZHJvcGRvd24tdG9nZ2xlIGhpZGRlbi1tZCBoaWRkZW4tbGdcIlxuICAgICAgICAgICAgICAgICAgdHlwZT1cImJ1dHRvblwiXG4gICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLnRvZ2dsZU5hdn1cbiAgICAgICAgICAgICAgICAgIGFyaWEtaGFzcG9wdXA9XCJ0cnVlXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtZXhwYW5kZWQ9e3RoaXMuc3RhdGUuZHJvcGRvd24gPyAndHJ1ZScgOiAnZmFsc2UnfT5cbiAgICAgICAgICAgIDxpIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgICAgbWVudVxuICAgICAgICAgICAgPC9pPlxuICAgICAgICAgIDwvYnV0dG9uPlxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UtdGFicyBoaWRkZW4teHMgaGlkZGVuLXNtXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cblxuICAgICAgICAgICAgPFRhYnNOYXYgbGlzdHM9e21pc2Fnby5nZXQoJ1VTRVJTX0xJU1RTJyl9XG4gICAgICAgICAgICAgICAgICAgICBiYXNlVXJsPXttaXNhZ28uZ2V0KCdVU0VSU19MSVNUX1VSTCcpfSAvPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRDb21wYWN0TmF2Q2xhc3NOYW1lKCl9PlxuXG4gICAgICAgIDxDb21wYWN0TmF2IGxpc3RzPXttaXNhZ28uZ2V0KCdVU0VSU19MSVNUUycpfVxuICAgICAgICAgICAgICAgICAgICBiYXNlVXJsPXttaXNhZ28uZ2V0KCdVU0VSU19MSVNUX1VSTCcpfSAvPlxuXG4gICAgICA8L2Rpdj5cblxuICAgICAge3RoaXMucHJvcHMuY2hpbGRyZW59XG5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0KHN0b3JlKSB7XG4gIHJldHVybiB7XG4gICAgJ3RpY2snOiBzdG9yZS50aWNrLnRpY2ssXG4gICAgJ3VzZXInOiBzdG9yZS5hdXRoLnVzZXIsXG4gICAgJ3VzZXJzJzogc3RvcmUudXNlcnNcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHBhdGhzKCkge1xuICBsZXQgcGF0aHMgPSBbXTtcblxuICBtaXNhZ28uZ2V0KCdVU0VSU19MSVNUUycpLmZvckVhY2goZnVuY3Rpb24oaXRlbSkge1xuICAgIGlmIChpdGVtLmNvbXBvbmVudCA9PT0gJ3JhbmsnKSB7XG4gICAgICBwYXRocy5wdXNoKHtcbiAgICAgICAgcGF0aDogbWlzYWdvLmdldCgnVVNFUlNfTElTVF9VUkwnKSArIGl0ZW0uc2x1ZyArICcvJyxcbiAgICAgICAgY29tcG9uZW50OiBjb25uZWN0KHNlbGVjdCkoUmFuayksXG4gICAgICAgIHJhbms6IHtcbiAgICAgICAgICBuYW1lOiBpdGVtLm5hbWUsXG4gICAgICAgICAgc2x1ZzogaXRlbS5zbHVnLFxuICAgICAgICAgIGNzc19jbGFzczogaXRlbS5jc3NfY2xhc3MsXG4gICAgICAgICAgZGVzY3JpcHRpb246IGl0ZW0uZGVzY3JpcHRpb25cbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfSBlbHNlIGlmIChpdGVtLmNvbXBvbmVudCA9PT0gJ2FjdGl2ZS1wb3N0ZXJzJyl7XG4gICAgICBwYXRocy5wdXNoKHtcbiAgICAgICAgcGF0aDogbWlzYWdvLmdldCgnVVNFUlNfTElTVF9VUkwnKSArIGl0ZW0uY29tcG9uZW50ICsgJy8nLFxuICAgICAgICBjb21wb25lbnQ6IGNvbm5lY3Qoc2VsZWN0KShBY3RpdmVQb3N0ZXJzKSxcbiAgICAgICAgZXh0cmE6IHtcbiAgICAgICAgICBuYW1lOiBpdGVtLm5hbWVcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICB9KTtcblxuICByZXR1cm4gcGF0aHM7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldENsYXNzTmFtZSgpIHtcbiAgICBpZiAodGhpcy5wcm9wcy52YWx1ZSkge1xuICAgICAgcmV0dXJuIFwiYnRuIGJ0bi15ZXMtbm8gYnRuLXllcy1uby1vblwiO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gXCJidG4gYnRuLXllcy1ubyBidG4teWVzLW5vLW9mZlwiO1xuICAgIH1cbiAgfVxuXG4gIGdldEljb24oKSB7XG4gICAgaWYgKHRoaXMucHJvcHMudmFsdWUpIHtcbiAgICAgIHJldHVybiB0aGlzLnByb3BzLmljb25PbiB8fCAnY2hlY2tfYm94JztcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHRoaXMucHJvcHMuaWNvbk9mZiB8fCAnY2hlY2tfYm94X291dGxpbmVfYmxhbmsnO1xuICAgIH1cbiAgfVxuXG4gIGdldExhYmVsKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnZhbHVlKSB7XG4gICAgICByZXR1cm4gdGhpcy5wcm9wcy5sYWJlbE9uIHx8IGdldHRleHQoXCJ5ZXNcIik7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLnByb3BzLmxhYmVsT2ZmIHx8IGdldHRleHQoXCJub1wiKTtcbiAgICB9XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHRvZ2dsZSA9ICgpID0+IHtcbiAgICB0aGlzLnByb3BzLm9uQ2hhbmdlKHtcbiAgICAgIHRhcmdldDoge1xuICAgICAgICB2YWx1ZTogIXRoaXMucHJvcHMudmFsdWVcbiAgICAgIH1cbiAgICB9KTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8YnV0dG9uIHR5cGU9XCJidXR0b25cIlxuICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMudG9nZ2xlfVxuICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17dGhpcy5nZXRDbGFzc05hbWUoKX1cbiAgICAgICAgICAgICAgICAgICBpZD17dGhpcy5wcm9wcy5pZCB8fCBudWxsfVxuICAgICAgICAgICAgICAgICAgIGFyaWEtZGVzY3JpYmVkYnk9e3RoaXMucHJvcHNbJ2FyaWEtZGVzY3JpYmVkYnknXSB8fCBudWxsfVxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnByb3BzLmRpc2FibGVkIHx8IGZhbHNlfT5cbiAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAge3RoaXMuZ2V0SWNvbigpfVxuICAgICAgPC9zcGFuPlxuICAgICAge3RoaXMuZ2V0TGFiZWwoKX1cbiAgICA8L2J1dHRvbj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBPcmRlcmVkTGlzdCBmcm9tICdtaXNhZ28vdXRpbHMvb3JkZXJlZC1saXN0JztcblxuZXhwb3J0IGNsYXNzIE1pc2FnbyB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2luaXRpYWxpemVycyA9IFtdO1xuICAgIHRoaXMuX2NvbnRleHQgPSB7fTtcbiAgfVxuXG4gIGFkZEluaXRpYWxpemVyKGluaXRpYWxpemVyKSB7XG4gICAgdGhpcy5faW5pdGlhbGl6ZXJzLnB1c2goe1xuICAgICAga2V5OiBpbml0aWFsaXplci5uYW1lLFxuXG4gICAgICBpdGVtOiBpbml0aWFsaXplci5pbml0aWFsaXplcixcblxuICAgICAgYWZ0ZXI6IGluaXRpYWxpemVyLmFmdGVyLFxuICAgICAgYmVmb3JlOiBpbml0aWFsaXplci5iZWZvcmVcbiAgICB9KTtcbiAgfVxuXG4gIGluaXQoY29udGV4dCkge1xuICAgIHRoaXMuX2NvbnRleHQgPSBjb250ZXh0O1xuXG4gICAgdmFyIGluaXRPcmRlciA9IG5ldyBPcmRlcmVkTGlzdCh0aGlzLl9pbml0aWFsaXplcnMpLm9yZGVyZWRWYWx1ZXMoKTtcbiAgICBpbml0T3JkZXIuZm9yRWFjaChpbml0aWFsaXplciA9PiB7XG4gICAgICBpbml0aWFsaXplcih0aGlzKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8vIGNvbnRleHQgYWNjZXNzb3JzXG4gIGhhcyhrZXkpIHtcbiAgICByZXR1cm4gISF0aGlzLl9jb250ZXh0W2tleV07XG4gIH1cblxuICBnZXQoa2V5LCBmYWxsYmFjaykge1xuICAgIGlmICh0aGlzLmhhcyhrZXkpKSB7XG4gICAgICByZXR1cm4gdGhpcy5fY29udGV4dFtrZXldO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gZmFsbGJhY2sgfHwgdW5kZWZpbmVkO1xuICAgIH1cbiAgfVxuXG4gIHBvcChrZXkpIHtcbiAgICBpZiAodGhpcy5oYXMoa2V5KSkge1xuICAgICAgbGV0IHZhbHVlID0gdGhpcy5fY29udGV4dFtrZXldO1xuICAgICAgdGhpcy5fY29udGV4dFtrZXldID0gbnVsbDtcbiAgICAgIHJldHVybiB2YWx1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG4gIH1cbn1cblxuLy8gY3JlYXRlICBzaW5nbGV0b25cbnZhciBtaXNhZ28gPSBuZXcgTWlzYWdvKCk7XG5cbi8vIGV4cG9zZSBpdCBnbG9iYWxseVxuZ2xvYmFsLm1pc2FnbyA9IG1pc2FnbztcblxuLy8gYW5kIGV4cG9ydCBpdCBmb3IgdGVzdHMgYW5kIHN0dWZmXG5leHBvcnQgZGVmYXVsdCBtaXNhZ287XG4iLCJpbXBvcnQgeyBVUERBVEVfQVZBVEFSLCBVUERBVEVfVVNFUk5BTUUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdXNlcnMnO1xuXG5leHBvcnQgdmFyIGluaXRpYWxTdGF0ZSA9IHtcbiAgc2lnbmVkSW46IGZhbHNlLFxuICBzaWduZWRPdXQ6IGZhbHNlXG59O1xuXG5leHBvcnQgY29uc3QgUEFUQ0hfVVNFUiA9ICdQQVRDSF9VU0VSJztcbmV4cG9ydCBjb25zdCBTSUdOX0lOID0gJ1NJR05fSU4nO1xuZXhwb3J0IGNvbnN0IFNJR05fT1VUID0gJ1NJR05fT1VUJztcblxuZXhwb3J0IGZ1bmN0aW9uIHBhdGNoVXNlcihwYXRjaCkge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IFBBVENIX1VTRVIsXG4gICAgcGF0Y2hcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNpZ25Jbih1c2VyKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogU0lHTl9JTixcbiAgICB1c2VyXG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzaWduT3V0KHNvZnQ9ZmFsc2UpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBTSUdOX09VVCxcbiAgICBzb2Z0XG4gIH07XG59XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGF1dGgoc3RhdGU9aW5pdGlhbFN0YXRlLCBhY3Rpb249bnVsbCkge1xuICBzd2l0Y2ggKGFjdGlvbi50eXBlKSB7XG4gICAgY2FzZSBQQVRDSF9VU0VSOlxuICAgICAgICBsZXQgbmV3U3RhdGUgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSk7XG4gICAgICAgIG5ld1N0YXRlLnVzZXIgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZS51c2VyLCBhY3Rpb24ucGF0Y2gpO1xuICAgICAgICByZXR1cm4gbmV3U3RhdGU7XG5cbiAgICBjYXNlIFNJR05fSU46XG4gICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgc2lnbmVkSW46IGFjdGlvbi51c2VyXG4gICAgICB9KTtcblxuICAgIGNhc2UgU0lHTl9PVVQ6XG4gICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgaXNBdXRoZW50aWNhdGVkOiBmYWxzZSxcbiAgICAgICAgaXNBbm9ueW1vdXM6IHRydWUsXG4gICAgICAgIHNpZ25lZE91dDogIWFjdGlvbi5zb2Z0XG4gICAgICB9KTtcblxuICAgIGNhc2UgVVBEQVRFX0FWQVRBUjpcbiAgICAgIGlmIChzdGF0ZS5pc0F1dGhlbnRpY2F0ZWQgJiYgc3RhdGUudXNlci5pZCA9PT0gYWN0aW9uLnVzZXJJZCkge1xuICAgICAgICBsZXQgbmV3U3RhdGUgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSk7XG4gICAgICAgIG5ld1N0YXRlLnVzZXIgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZS51c2VyLCB7XG4gICAgICAgICAgJ2F2YXRhcl9oYXNoJzogYWN0aW9uLmF2YXRhckhhc2hcbiAgICAgICAgfSk7XG4gICAgICAgIHJldHVybiBuZXdTdGF0ZTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBzdGF0ZTtcblxuICAgIGNhc2UgVVBEQVRFX1VTRVJOQU1FOlxuICAgICAgaWYgKHN0YXRlLmlzQXV0aGVudGljYXRlZCAmJiBzdGF0ZS51c2VyLmlkID09PSBhY3Rpb24udXNlcklkKSB7XG4gICAgICAgIGxldCBuZXdTdGF0ZSA9IE9iamVjdC5hc3NpZ24oe30sIHN0YXRlKTtcbiAgICAgICAgbmV3U3RhdGUudXNlciA9IE9iamVjdC5hc3NpZ24oe30sIHN0YXRlLnVzZXIsIHtcbiAgICAgICAgICB1c2VybmFtZTogYWN0aW9uLnVzZXJuYW1lLFxuICAgICAgICAgIHNsdWc6IGFjdGlvbi5zbHVnXG4gICAgICAgIH0pO1xuICAgICAgICByZXR1cm4gbmV3U3RhdGU7XG4gICAgICB9XG4gICAgICByZXR1cm4gc3RhdGU7XG5cbiAgICBkZWZhdWx0OlxuICAgICAgcmV0dXJuIHN0YXRlO1xuICB9XG59XG4iLCJleHBvcnQgdmFyIGluaXRpYWxTdGF0ZSA9IHtcbiAgdHlwZTogJ2luZm8nLFxuICBtZXNzYWdlOiAnJyxcbiAgaXNWaXNpYmxlOiBmYWxzZVxufTtcblxuZXhwb3J0IGNvbnN0IFNIT1dfU05BQ0tCQVIgPSAnU0hPV19TTkFDS0JBUic7XG5leHBvcnQgY29uc3QgSElERV9TTkFDS0JBUiA9ICdISURFX1NOQUNLQkFSJztcblxuZXhwb3J0IGZ1bmN0aW9uIHNob3dTbmFja2JhcihtZXNzYWdlLCB0eXBlKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogU0hPV19TTkFDS0JBUixcbiAgICBtZXNzYWdlLFxuICAgIG1lc3NhZ2VUeXBlOiB0eXBlXG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoaWRlU25hY2tiYXIoKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogSElERV9TTkFDS0JBUlxuICB9O1xufVxuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBzbmFja2JhcihzdGF0ZT1pbml0aWFsU3RhdGUsIGFjdGlvbj1udWxsKSB7XG4gIGlmIChhY3Rpb24udHlwZSA9PT0gU0hPV19TTkFDS0JBUikge1xuICAgIHJldHVybiB7XG4gICAgICB0eXBlOiBhY3Rpb24ubWVzc2FnZVR5cGUsXG4gICAgICBtZXNzYWdlOiBhY3Rpb24ubWVzc2FnZSxcbiAgICAgIGlzVmlzaWJsZTogdHJ1ZVxuICAgIH07XG4gIH0gZWxzZSBpZiAoYWN0aW9uLnR5cGUgPT09IEhJREVfU05BQ0tCQVIpIHtcbiAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgaXNWaXNpYmxlOiBmYWxzZVxuICAgIH0pO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBzdGF0ZTtcbiAgfVxufVxuIiwiZXhwb3J0IHZhciBpbml0aWFsU3RhdGUgPSB7XG4gIHRpY2s6IDBcbn07XG5cbmV4cG9ydCBjb25zdCBUSUNLID0gJ1RJQ0snO1xuXG5leHBvcnQgZnVuY3Rpb24gZG9UaWNrKCkge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IFRJQ0tcbiAgfTtcbn1cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gdGljayhzdGF0ZT1pbml0aWFsU3RhdGUsIGFjdGlvbj1udWxsKSB7XG4gIGlmIChhY3Rpb24udHlwZSA9PT0gVElDSykge1xuICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSwge1xuICAgICAgICB0aWNrOiBzdGF0ZS50aWNrICsgMVxuICAgIH0pO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBzdGF0ZTtcbiAgfVxufVxuIiwiaW1wb3J0IHsgVVBEQVRFX0FWQVRBUiwgVVBEQVRFX1VTRVJOQU1FIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3VzZXJzJztcblxuaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuXG5leHBvcnQgY29uc3QgQUREX05BTUVfQ0hBTkdFID0gJ0FERF9OQU1FX0NIQU5HRSc7XG5leHBvcnQgY29uc3QgREVIWURSQVRFX1JFU1VMVCA9ICdERUhZRFJBVEVfUkVTVUxUJztcblxuZXhwb3J0IGZ1bmN0aW9uIGFkZE5hbWVDaGFuZ2UoY2hhbmdlLCB1c2VyLCBjaGFuZ2VkQnkpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBBRERfTkFNRV9DSEFOR0UsXG4gICAgY2hhbmdlLFxuICAgIHVzZXIsXG4gICAgY2hhbmdlZEJ5XG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBkZWh5ZHJhdGUoaXRlbXMpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBERUhZRFJBVEVfUkVTVUxULFxuICAgIGl0ZW1zOiBpdGVtc1xuICB9O1xufVxuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiB1c2VybmFtZShzdGF0ZT1bXSwgYWN0aW9uPW51bGwpIHtcbiAgc3dpdGNoIChhY3Rpb24udHlwZSkge1xuICAgIGNhc2UgQUREX05BTUVfQ0hBTkdFOlxuICAgICAgbGV0IG5ld1N0YXRlID0gc3RhdGUuc2xpY2UoKTtcbiAgICAgIG5ld1N0YXRlLnVuc2hpZnQoe1xuICAgICAgICBpZDogTWF0aC5mbG9vcihEYXRlLm5vdygpIC8gMTAwMCksIC8vIGp1c3Qgc21hbGwgaGF4IGZvciBnZXR0aW5nIGlkXG4gICAgICAgIGNoYW5nZWRfYnk6IGFjdGlvbi5jaGFuZ2VkQnksXG4gICAgICAgIGNoYW5nZWRfYnlfdXNlcm5hbWU6IGFjdGlvbi5jaGFuZ2VkQnkudXNlcm5hbWUsXG4gICAgICAgIGNoYW5nZWRfb246IG1vbWVudCgpLFxuICAgICAgICBuZXdfdXNlcm5hbWU6IGFjdGlvbi5jaGFuZ2UudXNlcm5hbWUsXG4gICAgICAgIG9sZF91c2VybmFtZTogYWN0aW9uLnVzZXIudXNlcm5hbWVcbiAgICAgIH0pO1xuICAgICAgcmV0dXJuIG5ld1N0YXRlO1xuXG4gICAgY2FzZSBERUhZRFJBVEVfUkVTVUxUOlxuICAgICAgcmV0dXJuIGFjdGlvbi5pdGVtcy5tYXAoZnVuY3Rpb24oaXRlbSkge1xuICAgICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgaXRlbSwge1xuICAgICAgICAgIGNoYW5nZWRfb246IG1vbWVudChpdGVtLmNoYW5nZWRfb24pXG4gICAgICAgIH0pO1xuICAgICAgfSk7XG5cbiAgICBjYXNlIFVQREFURV9BVkFUQVI6XG4gICAgICByZXR1cm4gc3RhdGUubWFwKGZ1bmN0aW9uKGl0ZW0pIHtcbiAgICAgICAgaXRlbSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0pO1xuICAgICAgICBpZiAoaXRlbS5jaGFuZ2VkX2J5ICYmIGl0ZW0uY2hhbmdlZF9ieS5pZCA9PT0gYWN0aW9uLnVzZXJJZCkge1xuICAgICAgICAgIGl0ZW0uY2hhbmdlZF9ieSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0uY2hhbmdlZF9ieSwge1xuICAgICAgICAgICAgJ2F2YXRhcl9oYXNoJzogYWN0aW9uLmF2YXRhckhhc2hcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBpdGVtKTtcbiAgICAgIH0pO1xuXG4gICAgY2FzZSBVUERBVEVfVVNFUk5BTUU6XG4gICAgICByZXR1cm4gc3RhdGUubWFwKGZ1bmN0aW9uKGl0ZW0pIHtcbiAgICAgICAgaXRlbSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0pO1xuICAgICAgICBpZiAoaXRlbS5jaGFuZ2VkX2J5ICYmIGl0ZW0uY2hhbmdlZF9ieS5pZCA9PT0gYWN0aW9uLnVzZXJJZCkge1xuICAgICAgICAgIGl0ZW0uY2hhbmdlZF9ieSA9IE9iamVjdC5hc3NpZ24oe30sIGl0ZW0uY2hhbmdlZF9ieSwge1xuICAgICAgICAgICAgJ3VzZXJuYW1lJzogYWN0aW9uLnVzZXJuYW1lLFxuICAgICAgICAgICAgJ3NsdWcnOiBhY3Rpb24uc2x1Z1xuICAgICAgICAgIH0pO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIE9iamVjdC5hc3NpZ24oe30sIGl0ZW0pO1xuICAgICAgfSk7XG5cbiAgICBkZWZhdWx0OlxuICAgICAgcmV0dXJuIHN0YXRlO1xuICB9XG59IiwiZXhwb3J0IGNvbnN0IERFSFlEUkFURV9SRVNVTFQgPSAnREVIWURSQVRFX1JFU1VMVCc7XG5leHBvcnQgY29uc3QgVVBEQVRFX0FWQVRBUiA9ICdVUERBVEVfQVZBVEFSJztcbmV4cG9ydCBjb25zdCBVUERBVEVfVVNFUk5BTUUgPSAnVVBEQVRFX1VTRVJOQU1FJztcblxuZXhwb3J0IGZ1bmN0aW9uIGRlaHlkcmF0ZShpdGVtcykge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IERFSFlEUkFURV9SRVNVTFQsXG4gICAgaXRlbXM6IGl0ZW1zXG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1cGRhdGVBdmF0YXIodXNlciwgYXZhdGFySGFzaCkge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IFVQREFURV9BVkFUQVIsXG4gICAgdXNlcklkOiB1c2VyLmlkLFxuICAgIGF2YXRhckhhc2hcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVwZGF0ZVVzZXJuYW1lKHVzZXIsIHVzZXJuYW1lLCBzbHVnKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogVVBEQVRFX1VTRVJOQU1FLFxuICAgIHVzZXJJZDogdXNlci5pZCxcbiAgICB1c2VybmFtZSxcbiAgICBzbHVnXG4gIH07XG59XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIHVzZXIoc3RhdGU9W10sIGFjdGlvbj1udWxsKSB7XG4gIHN3aXRjaCAoYWN0aW9uLnR5cGUpIHtcbiAgICBjYXNlIERFSFlEUkFURV9SRVNVTFQ6XG4gICAgICByZXR1cm4gYWN0aW9uLml0ZW1zLm1hcChmdW5jdGlvbihpdGVtKSB7XG4gICAgICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBpdGVtLCB7XG5cbiAgICAgICAgfSk7XG4gICAgICB9KTtcblxuICAgIGRlZmF1bHQ6XG4gICAgICByZXR1cm4gc3RhdGU7XG4gIH1cbn0iLCJleHBvcnQgY2xhc3MgQWpheCB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2Nvb2tpZU5hbWUgPSBudWxsO1xuICAgIHRoaXMuX2NzcmZUb2tlbiA9IG51bGw7XG4gIH1cblxuICBpbml0KGNvb2tpZU5hbWUpIHtcbiAgICB0aGlzLl9jb29raWVOYW1lID0gY29va2llTmFtZTtcbiAgICB0aGlzLl9jc3JmVG9rZW4gPSB0aGlzLmdldENzcmZUb2tlbigpO1xuICB9XG5cbiAgZ2V0Q3NyZlRva2VuKCkge1xuICAgIGlmIChkb2N1bWVudC5jb29raWUuaW5kZXhPZih0aGlzLl9jb29raWVOYW1lKSAhPT0gLTEpIHtcbiAgICAgIGxldCBjb29raWVSZWdleCA9IG5ldyBSZWdFeHAodGhpcy5fY29va2llTmFtZSArICdcXD0oW147XSopJyk7XG4gICAgICBsZXQgY29va2llID0gZG9jdW1lbnQuY29va2llLm1hdGNoKGNvb2tpZVJlZ2V4KVswXTtcbiAgICAgIHJldHVybiBjb29raWUgPyBjb29raWUuc3BsaXQoJz0nKVsxXSA6IG51bGw7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlcXVlc3QobWV0aG9kLCB1cmwsIGRhdGEpIHtcbiAgICBsZXQgc2VsZiA9IHRoaXM7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUsIHJlamVjdCkge1xuICAgICAgbGV0IHhociA9IHtcbiAgICAgICAgdXJsOiB1cmwsXG4gICAgICAgIG1ldGhvZDogbWV0aG9kLFxuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgJ1gtQ1NSRlRva2VuJzogc2VsZi5fY3NyZlRva2VuXG4gICAgICAgIH0sXG5cbiAgICAgICAgZGF0YTogKGRhdGEgPyBKU09OLnN0cmluZ2lmeShkYXRhKSA6IG51bGwpLFxuICAgICAgICBjb250ZW50VHlwZTogXCJhcHBsaWNhdGlvbi9qc29uOyBjaGFyc2V0PXV0Zi04XCIsXG4gICAgICAgIGRhdGFUeXBlOiAnanNvbicsXG5cbiAgICAgICAgc3VjY2VzczogZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICAgIHJlc29sdmUoZGF0YSk7XG4gICAgICAgIH0sXG5cbiAgICAgICAgZXJyb3I6IGZ1bmN0aW9uKGpxWEhSKSB7XG4gICAgICAgICAgbGV0IHJlamVjdGlvbiA9IGpxWEhSLnJlc3BvbnNlSlNPTiB8fCB7fTtcblxuICAgICAgICAgIHJlamVjdGlvbi5zdGF0dXMgPSBqcVhIUi5zdGF0dXM7XG5cbiAgICAgICAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gMCkge1xuICAgICAgICAgICAgcmVqZWN0aW9uLmRldGFpbCA9IGdldHRleHQoXCJMb3N0IGNvbm5lY3Rpb24gd2l0aCBhcHBsaWNhdGlvbi5cIik7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgcmVqZWN0aW9uLnN0YXR1c1RleHQgPSBqcVhIUi5zdGF0dXNUZXh0O1xuXG4gICAgICAgICAgcmVqZWN0KHJlamVjdGlvbik7XG4gICAgICAgIH1cbiAgICAgIH07XG5cbiAgICAgICQuYWpheCh4aHIpO1xuICAgIH0pO1xuICB9XG5cbiAgZ2V0KHVybCwgcGFyYW1zKSB7XG4gICAgaWYgKHBhcmFtcykge1xuICAgICAgdXJsICs9ICc/JyArICQucGFyYW0ocGFyYW1zKTtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnR0VUJywgdXJsKTtcbiAgfVxuXG4gIHBvc3QodXJsLCBkYXRhKSB7XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnUE9TVCcsIHVybCwgZGF0YSk7XG4gIH1cblxuICBwYXRjaCh1cmwsIGRhdGEpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdQQVRDSCcsIHVybCwgZGF0YSk7XG4gIH1cblxuICBwdXQodXJsLCBkYXRhKSB7XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnUFVUJywgdXJsLCBkYXRhKTtcbiAgfVxuXG4gIGRlbGV0ZSh1cmwpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdERUxFVEUnLCB1cmwpO1xuICB9XG5cbiAgdXBsb2FkKHVybCwgZGF0YSwgcHJvZ3Jlc3MpIHtcbiAgICBsZXQgc2VsZiA9IHRoaXM7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUsIHJlamVjdCkge1xuICAgICAgbGV0IHhociA9IHtcbiAgICAgICAgdXJsOiB1cmwsXG4gICAgICAgIG1ldGhvZDogJ1BPU1QnLFxuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgJ1gtQ1NSRlRva2VuJzogc2VsZi5fY3NyZlRva2VuXG4gICAgICAgIH0sXG5cbiAgICAgICAgZGF0YTogZGF0YSxcbiAgICAgICAgY29udGVudFR5cGU6IGZhbHNlLFxuICAgICAgICBwcm9jZXNzRGF0YTogZmFsc2UsXG5cbiAgICAgICAgeGhyOiBmdW5jdGlvbigpIHtcbiAgICAgICAgICBsZXQgeGhyID0gbmV3IHdpbmRvdy5YTUxIdHRwUmVxdWVzdCgpO1xuICAgICAgICAgIHhoci51cGxvYWQuYWRkRXZlbnRMaXN0ZW5lcihcInByb2dyZXNzXCIsIGZ1bmN0aW9uKGV2dCkge1xuICAgICAgICAgICAgaWYgKGV2dC5sZW5ndGhDb21wdXRhYmxlKSB7XG4gICAgICAgICAgICAgIHByb2dyZXNzKE1hdGgucm91bmQoZXZ0LmxvYWRlZCAvIGV2dC50b3RhbCAqIDEwMCkpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0sIGZhbHNlKTtcbiAgICAgICAgICByZXR1cm4geGhyO1xuICAgICAgICB9LFxuXG4gICAgICAgIHN1Y2Nlc3M6IGZ1bmN0aW9uKHJlc3BvbnNlKSB7XG4gICAgICAgICAgcmVzb2x2ZShyZXNwb25zZSk7XG4gICAgICAgIH0sXG5cbiAgICAgICAgZXJyb3I6IGZ1bmN0aW9uKGpxWEhSKSB7XG4gICAgICAgICAgbGV0IHJlamVjdGlvbiA9IGpxWEhSLnJlc3BvbnNlSlNPTiB8fCB7fTtcblxuICAgICAgICAgIHJlamVjdGlvbi5zdGF0dXMgPSBqcVhIUi5zdGF0dXM7XG5cbiAgICAgICAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gMCkge1xuICAgICAgICAgICAgcmVqZWN0aW9uLmRldGFpbCA9IGdldHRleHQoXCJMb3N0IGNvbm5lY3Rpb24gd2l0aCBhcHBsaWNhdGlvbi5cIik7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgcmVqZWN0aW9uLnN0YXR1c1RleHQgPSBqcVhIUi5zdGF0dXNUZXh0O1xuXG4gICAgICAgICAgcmVqZWN0KHJlamVjdGlvbik7XG4gICAgICAgIH1cbiAgICAgIH07XG5cbiAgICAgICQuYWpheCh4aHIpO1xuICAgIH0pO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBBamF4KCk7XG4iLCJpbXBvcnQgeyBzaWduSW4sIHNpZ25PdXQgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvYXV0aCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgQXV0aCB7XG4gIGluaXQoc3RvcmUsIGxvY2FsLCBtb2RhbCkge1xuICAgIHRoaXMuX3N0b3JlID0gc3RvcmU7XG4gICAgdGhpcy5fbG9jYWwgPSBsb2NhbDtcbiAgICB0aGlzLl9tb2RhbCA9IG1vZGFsO1xuXG4gICAgLy8gdGVsbCBvdGhlciB0YWJzIHdoYXQgYXV0aCBzdGF0ZSBpcyBiZWNhdXNlIHdlIGFyZSBtb3N0IGN1cnJlbnQgd2l0aCBpdFxuICAgIHRoaXMuc3luY1Nlc3Npb24oKTtcblxuICAgIC8vIGxpc3RlbiBmb3Igb3RoZXIgdGFicyB0byB0ZWxsIHVzIHRoYXQgc3RhdGUgY2hhbmdlZFxuICAgIHRoaXMud2F0Y2hTdGF0ZSgpO1xuICB9XG5cbiAgc3luY1Nlc3Npb24oKSB7XG4gICAgbGV0IHN0YXRlID0gdGhpcy5fc3RvcmUuZ2V0U3RhdGUoKS5hdXRoO1xuICAgIGlmIChzdGF0ZS5pc0F1dGhlbnRpY2F0ZWQpIHtcbiAgICAgIHRoaXMuX2xvY2FsLnNldCgnYXV0aCcsIHtcbiAgICAgICAgaXNBdXRoZW50aWNhdGVkOiB0cnVlLFxuICAgICAgICB1c2VybmFtZTogc3RhdGUudXNlci51c2VybmFtZVxuICAgICAgfSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2xvY2FsLnNldCgnYXV0aCcsIHtcbiAgICAgICAgaXNBdXRoZW50aWNhdGVkOiBmYWxzZVxuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgd2F0Y2hTdGF0ZSgpIHtcbiAgICB0aGlzLl9sb2NhbC53YXRjaCgnYXV0aCcsIChuZXdTdGF0ZSkgPT4ge1xuICAgICAgaWYgKG5ld1N0YXRlLmlzQXV0aGVudGljYXRlZCkge1xuICAgICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaWduSW4oe1xuICAgICAgICAgIHVzZXJuYW1lOiBuZXdTdGF0ZS51c2VybmFtZVxuICAgICAgICB9KSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaWduT3V0KCkpO1xuICAgICAgfVxuICAgIH0pO1xuICAgIHRoaXMuX21vZGFsLmhpZGUoKTtcbiAgfVxuXG4gIHNpZ25Jbih1c2VyKSB7XG4gICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goc2lnbkluKHVzZXIpKTtcbiAgICB0aGlzLl9sb2NhbC5zZXQoJ2F1dGgnLCB7XG4gICAgICBpc0F1dGhlbnRpY2F0ZWQ6IHRydWUsXG4gICAgICB1c2VybmFtZTogdXNlci51c2VybmFtZVxuICAgIH0pO1xuICAgIHRoaXMuX21vZGFsLmhpZGUoKTtcbiAgfVxuXG4gIHNpZ25PdXQoKSB7XG4gICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goc2lnbk91dCgpKTtcbiAgICB0aGlzLl9sb2NhbC5zZXQoJ2F1dGgnLCB7XG4gICAgICBpc0F1dGhlbnRpY2F0ZWQ6IGZhbHNlXG4gICAgfSk7XG4gICAgdGhpcy5fbW9kYWwuaGlkZSgpO1xuICB9XG5cbiAgc29mdFNpZ25PdXQoKSB7XG4gICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goc2lnbk91dCh0cnVlKSk7XG4gICAgdGhpcy5fbG9jYWwuc2V0KCdhdXRoJywge1xuICAgICAgaXNBdXRoZW50aWNhdGVkOiBmYWxzZVxuICAgIH0pO1xuICAgIHRoaXMuX21vZGFsLmhpZGUoKTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgQXV0aCgpOyIsIi8qIGdsb2JhbCBncmVjYXB0Y2hhICovXG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtR3JvdXAgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybS1ncm91cCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgQmFzZUNhcHRjaGEge1xuICBpbml0KGNvbnRleHQsIGFqYXgsIGluY2x1ZGUsIHNuYWNrYmFyKSB7XG4gICAgdGhpcy5fY29udGV4dCA9IGNvbnRleHQ7XG4gICAgdGhpcy5fYWpheCA9IGFqYXg7XG4gICAgdGhpcy5faW5jbHVkZSA9IGluY2x1ZGU7XG4gICAgdGhpcy5fc25hY2tiYXIgPSBzbmFja2JhcjtcbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgTm9DYXB0Y2hhIGV4dGVuZHMgQmFzZUNhcHRjaGEge1xuICBsb2FkKCkge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZShmdW5jdGlvbihyZXNvbHZlKSB7XG4gICAgICAvLyBpbW1lZGlhdGVseSByZXNvbHZlIGFzIHdlIGRvbid0IGhhdmUgYW55dGhpbmcgdG8gdmFsaWRhdGVcbiAgICAgIHJlc29sdmUoKTtcbiAgICB9KTtcbiAgfVxuXG4gIHZhbGlkYXRvcigpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIGNvbXBvbmVudCgpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgUUFDYXB0Y2hhIGV4dGVuZHMgQmFzZUNhcHRjaGEge1xuICBsb2FkKCkge1xuICAgIHZhciBzZWxmID0gdGhpcztcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgc2VsZi5fYWpheC5nZXQoc2VsZi5fY29udGV4dC5nZXQoJ0NBUFRDSEFfQVBJX1VSTCcpKS50aGVuKFxuICAgICAgZnVuY3Rpb24oZGF0YSkge1xuICAgICAgICBzZWxmLnF1ZXN0aW9uID0gZGF0YS5xdWVzdGlvbjtcbiAgICAgICAgc2VsZi5oZWxwVGV4dCA9IGRhdGEuaGVscF90ZXh0O1xuICAgICAgICByZXNvbHZlKCk7XG4gICAgICB9LCBmdW5jdGlvbigpIHtcbiAgICAgICAgc2VsZi5fc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZhaWxlZCB0byBsb2FkIENBUFRDSEEuXCIpKTtcbiAgICAgICAgcmVqZWN0KCk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfVxuXG4gIHZhbGlkYXRvcigpIHtcbiAgICByZXR1cm4gW107XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBvbmVudChrd2FyZ3MpIHtcbiAgICByZXR1cm4gPEZvcm1Hcm91cCBsYWJlbD17dGhpcy5xdWVzdGlvbn0gZm9yPVwiaWRfY2FwdGNoYVwiXG4gICAgICAgICAgICAgICAgICAgICAgbGFiZWxDbGFzcz17a3dhcmdzLmxhYmVsQ2xhc3MgfHwgXCJjb2wtc20tNFwifVxuICAgICAgICAgICAgICAgICAgICAgIGNvbnRyb2xDbGFzcz17a3dhcmdzLmNvbnRyb2xDbGFzcyB8fCBcImNvbC1zbS04XCJ9XG4gICAgICAgICAgICAgICAgICAgICAgdmFsaWRhdGlvbj17a3dhcmdzLmZvcm0uc3RhdGUuZXJyb3JzLmNhcHRjaGF9XG4gICAgICAgICAgICAgICAgICAgICAgaGVscFRleHQ9e3RoaXMuaGVscFRleHQgfHwgbnVsbH0+XG4gICAgICA8aW5wdXQgdHlwZT1cInRleHRcIiBpZD1cImlkX2NhcHRjaGFcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgIGFyaWEtZGVzY3JpYmVkYnk9XCJpZF9jYXB0Y2hhX3N0YXR1c1wiXG4gICAgICAgICAgICAgZGlzYWJsZWQ9e2t3YXJncy5mb3JtLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICBvbkNoYW5nZT17a3dhcmdzLmZvcm0uYmluZElucHV0KCdjYXB0Y2hhJyl9XG4gICAgICAgICAgICAgdmFsdWU9e2t3YXJncy5mb3JtLnN0YXRlLmNhcHRjaGF9IC8+XG4gICAgPC9Gb3JtR3JvdXA+O1xuICB9XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG59XG5cblxuZXhwb3J0IGNsYXNzIFJlQ2FwdGNoYUNvbXBvbmVudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIGdyZWNhcHRjaGEucmVuZGVyKCdyZWNhcHRjaGEnLCB7XG4gICAgICAnc2l0ZWtleSc6IHRoaXMucHJvcHMuc2l0ZUtleSxcbiAgICAgICdjYWxsYmFjayc6IChyZXNwb25zZSkgPT4ge1xuICAgICAgICAvLyBmaXJlIGZha2V5IGV2ZW50IHRvIGJpbmRpbmdcbiAgICAgICAgdGhpcy5wcm9wcy5iaW5kaW5nKHtcbiAgICAgICAgICB0YXJnZXQ6IHtcbiAgICAgICAgICAgIHZhbHVlOiByZXNwb25zZVxuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGlkPVwicmVjYXB0Y2hhXCIgLz47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgUmVDYXB0Y2hhIGV4dGVuZHMgQmFzZUNhcHRjaGEge1xuICBsb2FkKCkge1xuICAgIHRoaXMuX2luY2x1ZGUuaW5jbHVkZSgnaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9yZWNhcHRjaGEvYXBpLmpzJywgdHJ1ZSk7XG5cbiAgICByZXR1cm4gbmV3IFByb21pc2UoZnVuY3Rpb24ocmVzb2x2ZSkge1xuICAgICAgdmFyIHdhaXQgPSBmdW5jdGlvbigpIHtcbiAgICAgICAgaWYgKHR5cGVvZiBncmVjYXB0Y2hhID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgICAgICAgd2luZG93LnNldFRpbWVvdXQoZnVuY3Rpb24oKSB7XG4gICAgICAgICAgICB3YWl0KCk7XG4gICAgICAgICAgfSwgMjAwKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgIH1cbiAgICAgIH07XG4gICAgICB3YWl0KCk7XG4gICAgfSk7XG4gIH1cblxuICB2YWxpZGF0b3IoKSB7XG4gICAgcmV0dXJuIFtdO1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBjb21wb25lbnQoa3dhcmdzKSB7XG4gICAgcmV0dXJuIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJDYXB0Y2hhXCIpfSBmb3I9XCJpZF9jYXB0Y2hhXCJcbiAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPXtrd2FyZ3MubGFiZWxDbGFzcyB8fCBcImNvbC1zbS00XCJ9XG4gICAgICAgICAgICAgICAgICAgICAgY29udHJvbENsYXNzPXtrd2FyZ3MuY29udHJvbENsYXNzIHx8IFwiY29sLXNtLThcIn1cbiAgICAgICAgICAgICAgICAgICAgICB2YWxpZGF0aW9uPXtrd2FyZ3MuZm9ybS5zdGF0ZS5lcnJvcnMuY2FwdGNoYX1cbiAgICAgICAgICAgICAgICAgICAgICBoZWxwVGV4dD17Z2V0dGV4dChcIlBsZWFzZSBzb2x2ZSB0aGUgcXVpY2sgdGVzdC5cIil9PlxuICAgICAgPFJlQ2FwdGNoYUNvbXBvbmVudCBzaXRlS2V5PXt0aGlzLl9jb250ZXh0LmdldCgnU0VUVElOR1MnKS5yZWNhcHRjaGFfc2l0ZV9rZXl9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIGJpbmRpbmc9e2t3YXJncy5mb3JtLmJpbmRJbnB1dCgnY2FwdGNoYScpfSAvPlxuICAgIDwvRm9ybUdyb3VwPjtcbiAgfVxuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xufVxuXG5leHBvcnQgY2xhc3MgQ2FwdGNoYSB7XG4gIGluaXQoY29udGV4dCwgYWpheCwgaW5jbHVkZSwgc25hY2tiYXIpIHtcbiAgICBzd2l0Y2goY29udGV4dC5nZXQoJ1NFVFRJTkdTJykuY2FwdGNoYV90eXBlKSB7XG4gICAgICBjYXNlICdubyc6XG4gICAgICAgIHRoaXMuX2NhcHRjaGEgPSBuZXcgTm9DYXB0Y2hhKCk7XG4gICAgICAgIGJyZWFrO1xuXG4gICAgICBjYXNlICdxYSc6XG4gICAgICAgIHRoaXMuX2NhcHRjaGEgPSBuZXcgUUFDYXB0Y2hhKCk7XG4gICAgICAgIGJyZWFrO1xuXG4gICAgICBjYXNlICdyZSc6XG4gICAgICAgIHRoaXMuX2NhcHRjaGEgPSBuZXcgUmVDYXB0Y2hhKCk7XG4gICAgICAgIGJyZWFrO1xuICAgIH1cblxuICAgIHRoaXMuX2NhcHRjaGEuaW5pdChjb250ZXh0LCBhamF4LCBpbmNsdWRlLCBzbmFja2Jhcik7XG4gIH1cblxuICAvLyBhY2Nlc3NvcnMgZm9yIHVuZGVybHlpbmcgc3RyYXRlZ3lcblxuICBsb2FkKCkge1xuICAgIHJldHVybiB0aGlzLl9jYXB0Y2hhLmxvYWQoKTtcbiAgfVxuXG4gIHZhbGlkYXRvcigpIHtcbiAgICByZXR1cm4gdGhpcy5fY2FwdGNoYS52YWxpZGF0b3IoKTtcbiAgfVxuXG4gIGNvbXBvbmVudChrd2FyZ3MpIHtcbiAgICByZXR1cm4gdGhpcy5fY2FwdGNoYS5jb21wb25lbnQoa3dhcmdzKTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgQ2FwdGNoYSgpOyIsImV4cG9ydCBjbGFzcyBJbmNsdWRlIHtcbiAgaW5pdChzdGF0aWNVcmwpIHtcbiAgICB0aGlzLl9zdGF0aWNVcmwgPSBzdGF0aWNVcmw7XG4gICAgdGhpcy5faW5jbHVkZWQgPSBbXTtcbiAgfVxuXG4gIGluY2x1ZGUoc2NyaXB0LCByZW1vdGU9ZmFsc2UpIHtcbiAgICBpZiAodGhpcy5faW5jbHVkZWQuaW5kZXhPZihzY3JpcHQpID09PSAtMSkge1xuICAgICAgdGhpcy5faW5jbHVkZWQucHVzaChzY3JpcHQpO1xuICAgICAgdGhpcy5faW5jbHVkZShzY3JpcHQsIHJlbW90ZSk7XG4gICAgfVxuICB9XG5cbiAgX2luY2x1ZGUoc2NyaXB0LCByZW1vdGUpIHtcbiAgICAkLmFqYXgoe1xuICAgICAgdXJsOiAoIXJlbW90ZSA/IHRoaXMuX3N0YXRpY1VybCA6ICcnKSArIHNjcmlwdCxcbiAgICAgIGNhY2hlOiB0cnVlLFxuICAgICAgZGF0YVR5cGU6ICdzY3JpcHQnXG4gICAgfSk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IEluY2x1ZGUoKTsiLCJsZXQgc3RvcmFnZSA9IHdpbmRvdy5sb2NhbFN0b3JhZ2U7XG5cbmV4cG9ydCBjbGFzcyBMb2NhbFN0b3JhZ2Uge1xuICBpbml0KHByZWZpeCkge1xuICAgIHRoaXMuX3ByZWZpeCA9IHByZWZpeDtcbiAgICB0aGlzLl93YXRjaGVycyA9IFtdO1xuXG4gICAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ3N0b3JhZ2UnLCAoZSkgPT4ge1xuICAgICAgbGV0IG5ld1ZhbHVlSnNvbiA9IEpTT04ucGFyc2UoZS5uZXdWYWx1ZSk7XG4gICAgICB0aGlzLl93YXRjaGVycy5mb3JFYWNoKGZ1bmN0aW9uKHdhdGNoZXIpIHtcbiAgICAgICAgaWYgKHdhdGNoZXIua2V5ID09PSBlLmtleSAmJiBlLm9sZFZhbHVlICE9PSBlLm5ld1ZhbHVlKSB7XG4gICAgICAgICAgd2F0Y2hlci5jYWxsYmFjayhuZXdWYWx1ZUpzb24pO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfVxuXG4gIHNldChrZXksIHZhbHVlKSB7XG4gICAgc3RvcmFnZS5zZXRJdGVtKHRoaXMuX3ByZWZpeCArIGtleSwgSlNPTi5zdHJpbmdpZnkodmFsdWUpKTtcbiAgfVxuXG4gIGdldChrZXkpIHtcbiAgICBsZXQgaXRlbVN0cmluZyA9IHN0b3JhZ2UuZ2V0SXRlbSh0aGlzLl9wcmVmaXggKyBrZXkpO1xuICAgIGlmIChpdGVtU3RyaW5nKSB7XG4gICAgICByZXR1cm4gSlNPTi5wYXJzZShpdGVtU3RyaW5nKTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgd2F0Y2goa2V5LCBjYWxsYmFjaykge1xuICAgIHRoaXMuX3dhdGNoZXJzLnB1c2goe1xuICAgICAga2V5OiB0aGlzLl9wcmVmaXggKyBrZXksXG4gICAgICBjYWxsYmFjazogY2FsbGJhY2tcbiAgICB9KTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgTG9jYWxTdG9yYWdlKCk7IiwiaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgY2xhc3MgTW9iaWxlTmF2YmFyRHJvcGRvd24ge1xuICBpbml0KGVsZW1lbnQpIHtcbiAgICB0aGlzLl9lbGVtZW50ID0gZWxlbWVudDtcbiAgICB0aGlzLl9jb21wb25lbnQgPSBudWxsO1xuICB9XG5cbiAgc2hvdyhjb21wb25lbnQpIHtcbiAgICBpZiAodGhpcy5fY29tcG9uZW50ID09PSBjb21wb25lbnQpIHtcbiAgICAgIHRoaXMuaGlkZSgpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9jb21wb25lbnQgPSBjb21wb25lbnQ7XG4gICAgICBtb3VudChjb21wb25lbnQsIHRoaXMuX2VsZW1lbnQuaWQpO1xuICAgICAgJCh0aGlzLl9lbGVtZW50KS5hZGRDbGFzcygnb3BlbicpO1xuICAgIH1cbiAgfVxuXG4gIHNob3dDb25uZWN0ZWQobmFtZSwgY29tcG9uZW50KSB7XG4gICAgaWYgKHRoaXMuX2NvbXBvbmVudCA9PT0gbmFtZSkge1xuICAgICAgdGhpcy5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2NvbXBvbmVudCA9IG5hbWU7XG4gICAgICBtb3VudChjb21wb25lbnQsIHRoaXMuX2VsZW1lbnQuaWQsIHRydWUpO1xuICAgICAgJCh0aGlzLl9lbGVtZW50KS5hZGRDbGFzcygnb3BlbicpO1xuICAgIH1cbiAgfVxuXG4gIGhpZGUoKSB7XG4gICAgJCh0aGlzLl9lbGVtZW50KS5yZW1vdmVDbGFzcygnb3BlbicpO1xuICAgIHRoaXMuX2NvbXBvbmVudCA9IG51bGw7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IE1vYmlsZU5hdmJhckRyb3Bkb3duKCk7XG4iLCJpbXBvcnQgUmVhY3RET00gZnJvbSAncmVhY3QtZG9tJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGNsYXNzIE1vZGFsIHtcbiAgaW5pdChlbGVtZW50KSB7XG4gICAgdGhpcy5fZWxlbWVudCA9IGVsZW1lbnQ7XG5cbiAgICB0aGlzLl9tb2RhbCA9ICQoZWxlbWVudCkubW9kYWwoe3Nob3c6IGZhbHNlfSk7XG5cbiAgICB0aGlzLl9tb2RhbC5vbignaGlkZGVuLmJzLm1vZGFsJywgKCkgPT4ge1xuICAgICAgUmVhY3RET00udW5tb3VudENvbXBvbmVudEF0Tm9kZSh0aGlzLl9lbGVtZW50KTtcbiAgICB9KTtcbiAgfVxuXG4gIHNob3coY29tcG9uZW50KSB7XG4gICAgbW91bnQoY29tcG9uZW50LCB0aGlzLl9lbGVtZW50LmlkKTtcbiAgICB0aGlzLl9tb2RhbC5tb2RhbCgnc2hvdycpO1xuICB9XG5cbiAgaGlkZSgpIHtcbiAgICB0aGlzLl9tb2RhbC5tb2RhbCgnaGlkZScpO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBNb2RhbCgpO1xuIiwiZXhwb3J0IGNsYXNzIFBhZ2VUaXRsZSB7XG4gIGluaXQoZm9ydW1OYW1lKSB7XG4gICAgdGhpcy5fZm9ydW1OYW1lID0gZm9ydW1OYW1lO1xuICB9XG5cbiAgc2V0KHRpdGxlKSB7XG4gICAgaWYgKHR5cGVvZiB0aXRsZSA9PT0gJ3N0cmluZycpIHtcbiAgICAgIHRpdGxlID0ge3RpdGxlOiB0aXRsZX07XG4gICAgfVxuXG4gICAgbGV0IGZpbmFsVGl0bGUgPSB0aXRsZS50aXRsZTtcblxuICAgIGlmICh0aXRsZS5wYWdlKSB7XG4gICAgICBsZXQgcGFnZUxhYmVsID0gaW50ZXJwb2xhdGUoZ2V0dGV4dCgncGFnZSAlKHBhZ2UpcycpLCB7XG4gICAgICAgIHBhZ2U6IHRpdGxlLnBhZ2VcbiAgICAgIH0sIHRydWUpO1xuXG4gICAgICBmaW5hbFRpdGxlICs9ICcgKCcgKyBwYWdlTGFiZWwgKyAnKSc7XG4gICAgfVxuXG4gICAgaWYgKHRpdGxlLnBhcmVudCkge1xuICAgICAgZmluYWxUaXRsZSArPSAnIHwgJyArIHRpdGxlLnBhcmVudDtcbiAgICB9XG5cbiAgICBkb2N1bWVudC50aXRsZSA9IGZpbmFsVGl0bGUgKyAnIHwgJyArIHRoaXMuX2ZvcnVtTmFtZTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgUGFnZVRpdGxlKCk7XG4iLCJpbXBvcnQgeyBzaG93U25hY2tiYXIsIGhpZGVTbmFja2JhciB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9zbmFja2Jhcic7XG5cbmNvbnN0IEhJREVfQU5JTUFUSU9OX0xFTkdUSCA9IDMwMDtcbmNvbnN0IE1FU1NBR0VfU0hPV19MRU5HVEggPSA1MDAwO1xuXG5leHBvcnQgY2xhc3MgU25hY2tiYXIge1xuICBpbml0KHN0b3JlKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBzdG9yZTtcbiAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgfVxuXG4gIGFsZXJ0KG1lc3NhZ2UsIHR5cGUpIHtcbiAgICBpZiAodGhpcy5fdGltZW91dCkge1xuICAgICAgd2luZG93LmNsZWFyVGltZW91dCh0aGlzLl90aW1lb3V0KTtcbiAgICAgIHRoaXMuX3N0b3JlLmRpc3BhdGNoKGhpZGVTbmFja2JhcigpKTtcblxuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fdGltZW91dCA9IG51bGw7XG4gICAgICAgIHRoaXMuYWxlcnQobWVzc2FnZSwgdHlwZSk7XG4gICAgICB9LCBISURFX0FOSU1BVElPTl9MRU5HVEgpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaG93U25hY2tiYXIobWVzc2FnZSwgdHlwZSkpO1xuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goaGlkZVNuYWNrYmFyKCkpO1xuICAgICAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgICAgIH0sIE1FU1NBR0VfU0hPV19MRU5HVEgpO1xuICAgIH1cbiAgfVxuXG4gIC8vIHNob3J0aGFuZHMgZm9yIG1lc3NhZ2UgdHlwZXNcblxuICBpbmZvKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdpbmZvJyk7XG4gIH1cblxuICBzdWNjZXNzKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdzdWNjZXNzJyk7XG4gIH1cblxuICB3YXJuaW5nKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICd3YXJuaW5nJyk7XG4gIH1cblxuICBlcnJvcihtZXNzYWdlKSB7XG4gICAgdGhpcy5hbGVydChtZXNzYWdlLCAnZXJyb3InKTtcbiAgfVxuXG4gIC8vIHNob3J0aGFuZCBmb3IgYXBpIGVycm9yc1xuXG4gIGFwaUVycm9yKHJlamVjdGlvbikge1xuICAgIGxldCBtZXNzYWdlID0gZ2V0dGV4dChcIlVua25vd24gZXJyb3IgaGFzIG9jY3VyZWQuXCIpO1xuXG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDApIHtcbiAgICAgIG1lc3NhZ2UgPSByZWplY3Rpb24uZGV0YWlsO1xuICAgIH1cblxuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDAgJiYgcmVqZWN0aW9uLmRldGFpbCkge1xuICAgICAgbWVzc2FnZSA9IHJlamVjdGlvbi5kZXRhaWw7XG4gICAgfVxuXG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMykge1xuICAgICAgbWVzc2FnZSA9IHJlamVjdGlvbi5kZXRhaWw7XG4gICAgICBpZiAobWVzc2FnZSA9PT0gXCJQZXJtaXNzaW9uIGRlbmllZFwiKSB7XG4gICAgICAgIG1lc3NhZ2UgPSBnZXR0ZXh0KFxuICAgICAgICAgIFwiWW91IGRvbid0IGhhdmUgcGVybWlzc2lvbiB0byBwZXJmb3JtIHRoaXMgYWN0aW9uLlwiKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDA0KSB7XG4gICAgICBtZXNzYWdlID0gZ2V0dGV4dChcIkFjdGlvbiBsaW5rIGlzIGludmFsaWQuXCIpO1xuICAgIH1cblxuICAgIHRoaXMuZXJyb3IobWVzc2FnZSk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IFNuYWNrYmFyKCk7XG4iLCJpbXBvcnQgeyBjb21iaW5lUmVkdWNlcnMsIGNyZWF0ZVN0b3JlIH0gZnJvbSAncmVkdXgnO1xuXG5leHBvcnQgY2xhc3MgU3RvcmVXcmFwcGVyIHtcbiAgY29uc3RydWN0b3IoKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBudWxsO1xuICAgIHRoaXMuX3JlZHVjZXJzID0ge307XG4gICAgdGhpcy5faW5pdGlhbFN0YXRlID0ge307XG4gIH1cblxuICBhZGRSZWR1Y2VyKG5hbWUsIHJlZHVjZXIsIGluaXRpYWxTdGF0ZSkge1xuICAgIHRoaXMuX3JlZHVjZXJzW25hbWVdID0gcmVkdWNlcjtcbiAgICB0aGlzLl9pbml0aWFsU3RhdGVbbmFtZV0gPSBpbml0aWFsU3RhdGU7XG4gIH1cblxuICBpbml0KCkge1xuICAgIHRoaXMuX3N0b3JlID0gY3JlYXRlU3RvcmUoXG4gICAgICBjb21iaW5lUmVkdWNlcnModGhpcy5fcmVkdWNlcnMpLCB0aGlzLl9pbml0aWFsU3RhdGUpO1xuICB9XG5cbiAgZ2V0U3RvcmUoKSB7XG4gICAgcmV0dXJuIHRoaXMuX3N0b3JlO1xuICB9XG5cbiAgLy8gU3RvcmUgQVBJXG5cbiAgZ2V0U3RhdGUoKSB7XG4gICAgcmV0dXJuIHRoaXMuX3N0b3JlLmdldFN0YXRlKCk7XG4gIH1cblxuICBkaXNwYXRjaChhY3Rpb24pIHtcbiAgICByZXR1cm4gdGhpcy5fc3RvcmUuZGlzcGF0Y2goYWN0aW9uKTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgU3RvcmVXcmFwcGVyKCk7XG4iLCIvKiBnbG9iYWwgenhjdmJuICovXG5leHBvcnQgY2xhc3MgWnhjdmJuIHtcbiAgaW5pdChpbmNsdWRlKSB7XG4gICAgdGhpcy5faW5jbHVkZSA9IGluY2x1ZGU7XG4gIH1cblxuICBzY29yZVBhc3N3b3JkKHBhc3N3b3JkLCBpbnB1dHMpIHtcbiAgICAvLyAwLTQgc2NvcmUsIHRoZSBtb3JlIHRoZSBzdHJvbmdlciBwYXNzd29yZFxuICAgIHJldHVybiB6eGN2Ym4ocGFzc3dvcmQsIGlucHV0cykuc2NvcmU7XG4gIH1cblxuICBsb2FkKCkge1xuICAgIGlmICh0eXBlb2YgenhjdmJuID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgICB0aGlzLl9pbmNsdWRlLmluY2x1ZGUoJ21pc2Fnby9qcy96eGN2Ym4uanMnKTtcbiAgICAgIHJldHVybiB0aGlzLl9sb2FkaW5nUHJvbWlzZSgpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gdGhpcy5fbG9hZGVkUHJvbWlzZSgpO1xuICAgIH1cbiAgfVxuXG4gIF9sb2FkaW5nUHJvbWlzZSgpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoZnVuY3Rpb24ocmVzb2x2ZSkge1xuICAgICAgdmFyIHdhaXQgPSBmdW5jdGlvbigpIHtcbiAgICAgICAgaWYgKHR5cGVvZiB6eGN2Ym4gPT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICB3aW5kb3cuc2V0VGltZW91dChmdW5jdGlvbigpIHtcbiAgICAgICAgICAgIHdhaXQoKTtcbiAgICAgICAgICB9LCAyMDApO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJlc29sdmUoKTtcbiAgICAgICAgfVxuICAgICAgfTtcbiAgICAgIHdhaXQoKTtcbiAgICB9KTtcbiAgfVxuXG4gIF9sb2FkZWRQcm9taXNlKCkge1xuICAgIC8vIHdlIGhhdmUgYWxyZWFkeSBsb2FkZWQgenhjdmJuLmpzLCByZXNvbHZlIGF3YXkhXG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUpIHtcbiAgICAgIHJlc29sdmUoKTtcbiAgICB9KTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgWnhjdmJuKCk7IiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5pbXBvcnQgeyBQcm92aWRlciwgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQmFubmVkUGFnZSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9iYW5uZWQtcGFnZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG4vKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG5sZXQgc2VsZWN0ID0gZnVuY3Rpb24oc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLnRpY2s7XG59O1xuXG5sZXQgUmVkcmF3ZWRCYW5uZWRQYWdlID0gY29ubmVjdChzZWxlY3QpKEJhbm5lZFBhZ2UpO1xuLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24oYmFuLCBjaGFuZ2VTdGF0ZSkge1xuICBSZWFjdERPTS5yZW5kZXIoXG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIDxQcm92aWRlciBzdG9yZT17c3RvcmUuZ2V0U3RvcmUoKX0+XG4gICAgICA8UmVkcmF3ZWRCYW5uZWRQYWdlIG1lc3NhZ2U9e2Jhbi5tZXNzYWdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICBleHBpcmVzPXtiYW4uZXhwaXJlc19vbiA/IG1vbWVudChiYW4uZXhwaXJlc19vbikgOiBudWxsfSAvPlxuICAgIDwvUHJvdmlkZXI+LFxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3BhZ2UtbW91bnQnKVxuICApO1xuXG4gIGlmICh0eXBlb2YgY2hhbmdlU3RhdGUgPT09ICd1bmRlZmluZWQnIHx8IGNoYW5nZVN0YXRlKSB7XG4gICAgbGV0IGZvcnVtTmFtZSA9IG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykuZm9ydW1fbmFtZTtcbiAgICBkb2N1bWVudC50aXRsZSA9IGdldHRleHQoXCJZb3UgYXJlIGJhbm5lZFwiKSArICcgfCAnICsgZm9ydW1OYW1lO1xuICAgIHdpbmRvdy5oaXN0b3J5LnB1c2hTdGF0ZSh7fSwgXCJcIiwgbWlzYWdvLmdldCgnQkFOTkVEX1VSTCcpKTtcbiAgfVxufSIsImV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uKGxpc3QsIHJvd1dpZHRoLCBwYWRkaW5nPWZhbHNlKSB7XG4gIGxldCByb3dzID0gW107XG4gIGxldCByb3cgPSBbXTtcblxuICBsaXN0LmZvckVhY2goZnVuY3Rpb24oZWxlbWVudCkge1xuICAgIHJvdy5wdXNoKGVsZW1lbnQpO1xuICAgIGlmIChyb3cubGVuZ3RoID09PSByb3dXaWR0aCkge1xuICAgICAgcm93cy5wdXNoKHJvdyk7XG4gICAgICByb3cgPSBbXTtcbiAgICB9XG4gIH0pO1xuXG4gIC8vIHBhZCByb3cgdG8gcmVxdWlyZWQgbGVuZ3RoP1xuICBpZiAocGFkZGluZyAhPT0gZmFsc2UgJiYgcm93Lmxlbmd0aCA+IDAgJiYgcm93Lmxlbmd0aCA8IHJvd1dpZHRoKSB7XG4gICAgZm9yIChsZXQgaSA9IHJvdy5sZW5ndGg7IGkgPCByb3dXaWR0aDsgaSArKykge1xuICAgICAgcm93LnB1c2gocGFkZGluZyk7XG4gICAgfVxuICB9XG5cbiAgaWYgKHJvdy5sZW5ndGgpIHtcbiAgICByb3dzLnB1c2gocm93KTtcbiAgfVxuXG4gIHJldHVybiByb3dzO1xufSIsImV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uKGJ5dGVzKSB7XG4gIGlmIChieXRlcyA+IDEwMDAgKiAxMDAwICogMTAwMCkge1xuICAgIHJldHVybiAoTWF0aC5yb3VuZChieXRlcyAqIDEwMCAvICgxMDAwICogMTAwMCAqIDEwMDApKSAvIDEwMCkgKyAnIEdCJztcbiAgfSBlbHNlIGlmIChieXRlcyA+IDEwMDAgKiAxMDAwKSB7XG4gICAgcmV0dXJuIChNYXRoLnJvdW5kKGJ5dGVzICogMTAwIC8gKDEwMDAgKiAxMDAwKSkgLyAxMDApICsgJyBNQic7XG4gIH0gZWxzZSBpZiAoYnl0ZXMgPiAxMDAwKSB7XG4gICAgcmV0dXJuIChNYXRoLnJvdW5kKGJ5dGVzICogMTAwIC8gMTAwMCkgLyAxMDApICsgJyBLQic7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIChNYXRoLnJvdW5kKGJ5dGVzICogMTAwKSAvIDEwMCkgKyAnIEInO1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgUmVhY3RET00gZnJvbSAncmVhY3QtZG9tJztcbmltcG9ydCB7IFByb3ZpZGVyIH0gZnJvbSAncmVhY3QtcmVkdXgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24oQ29tcG9uZW50LCByb290RWxlbWVudElkLCBjb25uZWN0ZWQ9dHJ1ZSkge1xuICBsZXQgcm9vdEVsZW1lbnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChyb290RWxlbWVudElkKTtcblxuICBpZiAocm9vdEVsZW1lbnQpIHtcbiAgICBpZiAoY29ubmVjdGVkKSB7XG4gICAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgICAgPFByb3ZpZGVyIHN0b3JlPXtzdG9yZS5nZXRTdG9yZSgpfT5cbiAgICAgICAgICA8Q29tcG9uZW50IC8+XG4gICAgICAgIDwvUHJvdmlkZXI+LFxuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgICByb290RWxlbWVudFxuICAgICAgKTtcbiAgICB9IGVsc2Uge1xuICAgICAgUmVhY3RET00ucmVuZGVyKFxuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIDxDb21wb25lbnQgLz4sXG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgICAgIHJvb3RFbGVtZW50XG4gICAgICApO1xuICAgIH1cbiAgfVxufVxuIiwiY2xhc3MgT3JkZXJlZExpc3Qge1xuICAgIGNvbnN0cnVjdG9yKGl0ZW1zKSB7XG4gICAgICB0aGlzLmlzT3JkZXJlZCA9IGZhbHNlO1xuICAgICAgdGhpcy5faXRlbXMgPSBpdGVtcyB8fCBbXTtcbiAgICB9XG5cbiAgICBhZGQoa2V5LCBpdGVtLCBvcmRlcikge1xuICAgICAgdGhpcy5faXRlbXMucHVzaCh7XG4gICAgICAgIGtleToga2V5LFxuICAgICAgICBpdGVtOiBpdGVtLFxuXG4gICAgICAgIGFmdGVyOiBvcmRlciA/IG9yZGVyLmFmdGVyIHx8IG51bGwgOiBudWxsLFxuICAgICAgICBiZWZvcmU6IG9yZGVyID8gb3JkZXIuYmVmb3JlIHx8IG51bGwgOiBudWxsXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBnZXQoa2V5LCB2YWx1ZSkge1xuICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLl9pdGVtcy5sZW5ndGg7IGkrKykge1xuICAgICAgICBpZiAodGhpcy5faXRlbXNbaV0ua2V5ID09PSBrZXkpIHtcbiAgICAgICAgICByZXR1cm4gdGhpcy5faXRlbXNbaV0uaXRlbTtcbiAgICAgICAgfVxuICAgICAgfVxuXG4gICAgICByZXR1cm4gdmFsdWU7XG4gICAgfVxuXG4gICAgaGFzKGtleSkge1xuICAgICAgcmV0dXJuIHRoaXMuZ2V0KGtleSkgIT09IHVuZGVmaW5lZDtcbiAgICB9XG5cbiAgICB2YWx1ZXMoKSB7XG4gICAgICB2YXIgdmFsdWVzID0gW107XG4gICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMuX2l0ZW1zLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIHZhbHVlcy5wdXNoKHRoaXMuX2l0ZW1zW2ldLml0ZW0pO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHZhbHVlcztcbiAgICB9XG5cbiAgICBvcmRlcih2YWx1ZXNfb25seSkge1xuICAgICAgaWYgKCF0aGlzLmlzT3JkZXJlZCkge1xuICAgICAgICB0aGlzLl9pdGVtcyA9IHRoaXMuX29yZGVyKHRoaXMuX2l0ZW1zKTtcbiAgICAgICAgdGhpcy5pc09yZGVyZWQgPSB0cnVlO1xuICAgICAgfVxuXG4gICAgICBpZiAodmFsdWVzX29ubHkgfHwgdHlwZW9mIHZhbHVlc19vbmx5ID09PSAndW5kZWZpbmVkJykge1xuICAgICAgICByZXR1cm4gdGhpcy52YWx1ZXMoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9pdGVtcztcbiAgICAgIH1cbiAgICB9XG5cbiAgICBvcmRlcmVkVmFsdWVzKCkge1xuICAgICAgcmV0dXJuIHRoaXMub3JkZXIodHJ1ZSk7XG4gICAgfVxuXG4gICAgX29yZGVyKHVub3JkZXJlZCkge1xuICAgICAgLy8gSW5kZXggb2YgdW5vcmRlcmVkIGl0ZW1zXG4gICAgICB2YXIgaW5kZXggPSBbXTtcbiAgICAgIHVub3JkZXJlZC5mb3JFYWNoKGZ1bmN0aW9uIChpdGVtKSB7XG4gICAgICAgIGluZGV4LnB1c2goaXRlbS5rZXkpO1xuICAgICAgfSk7XG5cbiAgICAgIC8vIE9yZGVyZWQgaXRlbXNcbiAgICAgIHZhciBvcmRlcmVkID0gW107XG4gICAgICB2YXIgb3JkZXJpbmcgPSBbXTtcblxuICAgICAgLy8gRmlyc3QgcGFzczogcmVnaXN0ZXIgaXRlbXMgdGhhdFxuICAgICAgLy8gZG9uJ3Qgc3BlY2lmeSB0aGVpciBvcmRlclxuICAgICAgdW5vcmRlcmVkLmZvckVhY2goZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICAgICAgaWYgKCFpdGVtLmFmdGVyICYmICFpdGVtLmJlZm9yZSkge1xuICAgICAgICAgIG9yZGVyZWQucHVzaChpdGVtKTtcbiAgICAgICAgICBvcmRlcmluZy5wdXNoKGl0ZW0ua2V5KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIC8vIFNlY29uZCBwYXNzOiByZWdpc3RlciBpdGVtcyB0aGF0XG4gICAgICAvLyBzcGVjaWZ5IHRoZWlyIGJlZm9yZSB0byBcIl9lbmRcIlxuICAgICAgdW5vcmRlcmVkLmZvckVhY2goZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICAgICAgaWYgKGl0ZW0uYmVmb3JlID09PSBcIl9lbmRcIikge1xuICAgICAgICAgIG9yZGVyZWQucHVzaChpdGVtKTtcbiAgICAgICAgICBvcmRlcmluZy5wdXNoKGl0ZW0ua2V5KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIC8vIFRoaXJkIHBhc3M6IGtlZXAgaXRlcmF0aW5nIGl0ZW1zXG4gICAgICAvLyB1bnRpbCB3ZSBoaXQgaXRlcmF0aW9ucyBsaW1pdCBvciBmaW5pc2hcbiAgICAgIC8vIG9yZGVyaW5nIGxpc3RcbiAgICAgIGZ1bmN0aW9uIGluc2VydEl0ZW0oaXRlbSkge1xuICAgICAgICB2YXIgaW5zZXJ0QXQgPSAtMTtcbiAgICAgICAgaWYgKG9yZGVyaW5nLmluZGV4T2YoaXRlbS5rZXkpID09PSAtMSkge1xuICAgICAgICAgIGlmIChpdGVtLmFmdGVyKSB7XG4gICAgICAgICAgICBpbnNlcnRBdCA9IG9yZGVyaW5nLmluZGV4T2YoaXRlbS5hZnRlcik7XG4gICAgICAgICAgICBpZiAoaW5zZXJ0QXQgIT09IC0xKSB7XG4gICAgICAgICAgICAgIGluc2VydEF0ICs9IDE7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSBlbHNlIGlmIChpdGVtLmJlZm9yZSkge1xuICAgICAgICAgICAgaW5zZXJ0QXQgPSBvcmRlcmluZy5pbmRleE9mKGl0ZW0uYmVmb3JlKTtcbiAgICAgICAgICB9XG5cbiAgICAgICAgICBpZiAoaW5zZXJ0QXQgIT09IC0xKSB7XG4gICAgICAgICAgICBvcmRlcmVkLnNwbGljZShpbnNlcnRBdCwgMCwgaXRlbSk7XG4gICAgICAgICAgICBvcmRlcmluZy5zcGxpY2UoaW5zZXJ0QXQsIDAsIGl0ZW0ua2V5KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgdmFyIGl0ZXJhdGlvbnMgPSAyMDA7XG4gICAgICB3aGlsZSAoaXRlcmF0aW9ucyA+IDAgJiYgaW5kZXgubGVuZ3RoICE9PSBvcmRlcmluZy5sZW5ndGgpIHtcbiAgICAgICAgaXRlcmF0aW9ucyAtPSAxO1xuICAgICAgICB1bm9yZGVyZWQuZm9yRWFjaChpbnNlcnRJdGVtKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIG9yZGVyZWQ7XG4gICAgfVxuICB9XG5cbiAgZXhwb3J0IGRlZmF1bHQgT3JkZXJlZExpc3Q7XG4iLCJleHBvcnQgZnVuY3Rpb24gaW50KG1pbiwgbWF4KSB7XG4gIHJldHVybiBNYXRoLmZsb29yKChNYXRoLnJhbmRvbSgpICogKG1heCArIDEpKSkgKyBtaW47XG59XG5cbmV4cG9ydCBmdW5jdGlvbiByYW5nZShtaW4sIG1heCkge1xuICBsZXQgYXJyYXkgPSBuZXcgQXJyYXkoaW50KG1pbiwgbWF4KSk7XG4gIGZvcihsZXQgaT0wOyBpPGFycmF5Lmxlbmd0aDsgaSsrKXtcbiAgICBhcnJheVtpXSA9IGk7XG4gIH1cblxuICByZXR1cm4gYXJyYXk7XG59IiwiLy8ganNoaW50IGlnbm9yZTpzdGFydFxuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IHsgUHJvdmlkZXIgfSBmcm9tICdyZWFjdC1yZWR1eCc7XG5pbXBvcnQgeyBSb3V0ZXIgfSBmcm9tICdyZWFjdC1yb3V0ZXInO1xuaW1wb3J0IGNyZWF0ZUhpc3RvcnkgZnJvbSAnaGlzdG9yeS9saWIvY3JlYXRlQnJvd3Nlckhpc3RvcnknO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmNvbnN0IHJvb3RFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3BhZ2UtbW91bnQnKTtcbmNvbnN0IGhpc3RvcnkgPSBuZXcgY3JlYXRlSGlzdG9yeSgpO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbihvcHRpb25zKSB7XG4gIGxldCByb3V0ZXMgPSB7XG4gICAgY29tcG9uZW50OiBvcHRpb25zLmNvbXBvbmVudCxcbiAgICBjaGlsZFJvdXRlczogW1xuICAgICAge1xuICAgICAgICBwYXRoOiBvcHRpb25zLnJvb3QsXG4gICAgICAgIG9uRW50ZXI6IGZ1bmN0aW9uKG5leHRTdGF0ZSwgcmVwbGFjZVN0YXRlKSB7XG4gICAgICAgICAgcmVwbGFjZVN0YXRlKG51bGwsIG9wdGlvbnMucGF0aHNbMF0ucGF0aCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICBdLmNvbmNhdChvcHRpb25zLnBhdGhzLm1hcChmdW5jdGlvbihwYXRoKSB7XG4gICAgICByZXR1cm4gcGF0aDtcbiAgICB9KSlcbiAgfTtcblxuICBSZWFjdERPTS5yZW5kZXIoXG4gICAgPFByb3ZpZGVyIHN0b3JlPXtzdG9yZS5nZXRTdG9yZSgpfT5cbiAgICAgIDxSb3V0ZXIgcm91dGVzPXtyb3V0ZXN9IGhpc3Rvcnk9e2hpc3Rvcnl9IC8+XG4gICAgPC9Qcm92aWRlcj4sXG4gICAgcm9vdEVsZW1lbnRcbiAgKTtcbn1cbiIsImNvbnN0IEVNQUlMID0gL14oKFtePD4oKVtcXF1cXC4sOzpcXHNAXFxcIl0rKFxcLltePD4oKVtcXF1cXC4sOzpcXHNAXFxcIl0rKSopfChcXFwiLitcXFwiKSlAKChbXjw+KClbXFxdXFwuLDs6XFxzQFxcXCJdK1xcLikrW148PigpW1xcXVxcLiw7Olxcc0BcXFwiXXsyLH0pJC9pO1xuY29uc3QgVVNFUk5BTUUgPSBuZXcgUmVnRXhwKCdeWzAtOWEtel0rJCcsICdpJyk7XG5cbmV4cG9ydCBmdW5jdGlvbiByZXF1aXJlZCgpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgaWYgKCQudHJpbSh2YWx1ZSkubGVuZ3RoID09PSAwKSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIlRoaXMgZmllbGQgaXMgcmVxdWlyZWQuXCIpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGVtYWlsKG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgaWYgKCFFTUFJTC50ZXN0KHZhbHVlKSkge1xuICAgICAgcmV0dXJuIG1lc3NhZ2UgfHwgZ2V0dGV4dChcIkVudGVyIGEgdmFsaWQgZW1haWwgYWRkcmVzcy5cIik7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gbWluTGVuZ3RoKGxpbWl0VmFsdWUsIG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgdmFyIHJldHVybk1lc3NhZ2UgPSAnJztcbiAgICB2YXIgbGVuZ3RoID0gJC50cmltKHZhbHVlKS5sZW5ndGg7XG5cbiAgICBpZiAobGVuZ3RoIDwgbGltaXRWYWx1ZSkge1xuICAgICAgaWYgKG1lc3NhZ2UpIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG1lc3NhZ2UobGltaXRWYWx1ZSwgbGVuZ3RoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybk1lc3NhZ2UgPSBuZ2V0dGV4dChcbiAgICAgICAgICBcIkVuc3VyZSB0aGlzIHZhbHVlIGhhcyBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIChpdCBoYXMgJShzaG93X3ZhbHVlKXMpLlwiLFxuICAgICAgICAgIFwiRW5zdXJlIHRoaXMgdmFsdWUgaGFzIGF0IGxlYXN0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXJzIChpdCBoYXMgJShzaG93X3ZhbHVlKXMpLlwiLFxuICAgICAgICAgIGxpbWl0VmFsdWUpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGludGVycG9sYXRlKHJldHVybk1lc3NhZ2UsIHtcbiAgICAgICAgbGltaXRfdmFsdWU6IGxpbWl0VmFsdWUsXG4gICAgICAgIHNob3dfdmFsdWU6IGxlbmd0aFxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gbWF4TGVuZ3RoKGxpbWl0VmFsdWUsIG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgdmFyIHJldHVybk1lc3NhZ2UgPSAnJztcbiAgICB2YXIgbGVuZ3RoID0gJC50cmltKHZhbHVlKS5sZW5ndGg7XG5cbiAgICBpZiAobGVuZ3RoID4gbGltaXRWYWx1ZSkge1xuICAgICAgaWYgKG1lc3NhZ2UpIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG1lc3NhZ2UobGltaXRWYWx1ZSwgbGVuZ3RoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybk1lc3NhZ2UgPSBuZ2V0dGV4dChcbiAgICAgICAgICBcIkVuc3VyZSB0aGlzIHZhbHVlIGhhcyBhdCBtb3N0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXIgKGl0IGhhcyAlKHNob3dfdmFsdWUpcykuXCIsXG4gICAgICAgICAgXCJFbnN1cmUgdGhpcyB2YWx1ZSBoYXMgYXQgbW9zdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVycyAoaXQgaGFzICUoc2hvd192YWx1ZSlzKS5cIixcbiAgICAgICAgICBsaW1pdFZhbHVlKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBpbnRlcnBvbGF0ZShyZXR1cm5NZXNzYWdlLCB7XG4gICAgICAgIGxpbWl0X3ZhbHVlOiBsaW1pdFZhbHVlLFxuICAgICAgICBzaG93X3ZhbHVlOiBsZW5ndGhcbiAgICAgIH0sIHRydWUpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVzZXJuYW1lTWluTGVuZ3RoKHNldHRpbmdzKSB7XG4gIHZhciBtZXNzYWdlID0gZnVuY3Rpb24obGltaXRWYWx1ZSkge1xuICAgIHJldHVybiBuZ2V0dGV4dChcbiAgICAgIFwiVXNlcm5hbWUgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIGxvbmcuXCIsXG4gICAgICBcIlVzZXJuYW1lIG11c3QgYmUgYXQgbGVhc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMgbG9uZy5cIixcbiAgICAgIGxpbWl0VmFsdWUpO1xuICB9O1xuICByZXR1cm4gdGhpcy5taW5MZW5ndGgoc2V0dGluZ3MudXNlcm5hbWVfbGVuZ3RoX21pbiwgbWVzc2FnZSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VybmFtZU1heExlbmd0aChzZXR0aW5ncykge1xuICB2YXIgbWVzc2FnZSA9IGZ1bmN0aW9uKGxpbWl0VmFsdWUpIHtcbiAgICByZXR1cm4gbmdldHRleHQoXG4gICAgICBcIlVzZXJuYW1lIGNhbm5vdCBiZSBsb25nZXIgdGhhbiAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyLlwiLFxuICAgICAgXCJVc2VybmFtZSBjYW5ub3QgYmUgbG9uZ2VyIHRoYW4gJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMuXCIsXG4gICAgICBsaW1pdFZhbHVlKTtcbiAgfTtcbiAgcmV0dXJuIHRoaXMubWF4TGVuZ3RoKHNldHRpbmdzLnVzZXJuYW1lX2xlbmd0aF9tYXgsIG1lc3NhZ2UpO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlcm5hbWVDb250ZW50KCkge1xuICByZXR1cm4gZnVuY3Rpb24odmFsdWUpIHtcbiAgICBpZiAoIVVTRVJOQU1FLnRlc3QoJC50cmltKHZhbHVlKSkpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiVXNlcm5hbWUgY2FuIG9ubHkgY29udGFpbiBsYXRpbiBhbHBoYWJldCBsZXR0ZXJzIGFuZCBkaWdpdHMuXCIpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHBhc3N3b3JkTWluTGVuZ3RoKHNldHRpbmdzKSB7XG4gIHZhciBtZXNzYWdlID0gZnVuY3Rpb24obGltaXRWYWx1ZSkge1xuICAgIHJldHVybiBuZ2V0dGV4dChcbiAgICAgIFwiVmFsaWQgcGFzc3dvcmQgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIGxvbmcuXCIsXG4gICAgICBcIlZhbGlkIHBhc3N3b3JkIG11c3QgYmUgYXQgbGVhc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMgbG9uZy5cIixcbiAgICAgIGxpbWl0VmFsdWUpO1xuICB9O1xuICByZXR1cm4gdGhpcy5taW5MZW5ndGgoc2V0dGluZ3MucGFzc3dvcmRfbGVuZ3RoX21pbiwgbWVzc2FnZSk7XG59Il19
