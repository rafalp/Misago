(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
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
      return this._context.hasOwnProperty(key);
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

},{"../../../../documents/misago/frontend/src/utils/ordered-list":62}],2:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/ajax":50}],3:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/auth-message":24,"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/utils/mount-component":61,"react-redux":"react-redux"}],4:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/reducers/auth":46,"../../../../../documents/misago/frontend/src/services/store":58}],5:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/auth":51,"../../../../../documents/misago/frontend/src/services/local-storage":54,"../../../../../documents/misago/frontend/src/services/modal":56,"../../../../../documents/misago/frontend/src/services/store":58}],6:[function(require,module,exports){
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
  if (context.get('BAN_MESSAGE')) {
    (0, _bannedPage2.default)(context.get('BAN_MESSAGE'), false);
  }
}

_index2.default.addInitializer({
  name: 'component:baned-page',
  initializer: initializer,
  after: 'store'
});

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/utils/banned-page":60}],7:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/ajax":50,"../../../../../documents/misago/frontend/src/services/captcha":52,"../../../../../documents/misago/frontend/src/services/include":53,"../../../../../documents/misago/frontend/src/services/snackbar":57}],8:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/include":53}],9:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/local-storage":54}],10:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/mobile-navbar-dropdown":55}],11:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/modal":56}],12:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"moment":"moment"}],13:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/request-activation-link":37,"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/utils/mount-component":61}],14:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/request-password-reset":38,"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/utils/mount-component":61}],15:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/reset-password-form":39,"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/utils/mount-component":61}],16:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/snackbar":41,"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/utils/mount-component":61,"react-redux":"react-redux"}],17:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/reducers/snackbar":47,"../../../../../documents/misago/frontend/src/services/store":58}],18:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/snackbar":57,"../../../../../documents/misago/frontend/src/services/store":58}],19:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/store":58}],20:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/reducers/tick":48,"../../../../../documents/misago/frontend/src/services/store":58}],21:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/reducers/tick":48,"../../../../../documents/misago/frontend/src/services/store":58}],22:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/components/user-menu/root":43,"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/utils/mount-component":61,"react-redux":"react-redux"}],23:[function(require,module,exports){
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

},{"../../../../../documents/misago/frontend/src/index":45,"../../../../../documents/misago/frontend/src/services/include":53,"../../../../../documents/misago/frontend/src/services/zxcvbn":59}],24:[function(require,module,exports){
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

},{"react":"react"}],25:[function(require,module,exports){
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

},{"react":"react"}],26:[function(require,module,exports){
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

},{"moment":"moment","react":"react"}],27:[function(require,module,exports){
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

},{"./loader":32,"react":"react"}],28:[function(require,module,exports){
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

      _ajax2.default.post(this.props.user.avatar_api_url, {
        avatar: avatarType
      }).then(function (response) {
        _snackbar2.default.success(response.detail);
        _this2.props.updateAvatar(response.avatar_hash, response.options);

        _this2.setState({
          'isLoading': false
        });
      }, function (rejection) {
        if (rejection.status === 400) {
          _snackbar2.default.error(rejection.detail);
        } else {
          _snackbar2.default.showError(rejection);
        }

        _this2.setState({
          'isLoading': false
        });
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
            className: 'btn-default btn-block' },
          gettext("Download my Gravatar")
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
                className: 'btn-default btn-block' },
              gettext("Generate my individual avatar")
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

},{"../../services/ajax":50,"../../services/snackbar":57,"../avatar":25,"../button":27,"../loader":32,"react":"react"}],29:[function(require,module,exports){
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

var _modalLoader = require('../modal-loader');

var _modalLoader2 = _interopRequireDefault(_modalLoader);

var _index3 = require('../../index');

var _index4 = _interopRequireDefault(_index3);

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
    }, _this2.updateAvatar = function (avatarHash, options) {
      _store2.default.dispatch((0, _users.updateAvatar)(_this2.props.user, avatarHash));

      _this2.setState({
        'component': _index2.default,
        options: options
      });
    }, _this2.showIndex = function () {
      _this2.setState({
        'component': _index2.default
      });
    }, _temp), _possibleConstructorReturn(_this2, _ret);
  }

  _createClass(_class, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      var _this3 = this;

      Promise.all([_ajax2.default.get(_index4.default.get('user').avatar_api_url)]).then(function (resolutions) {
        _this3.setState({
          'component': _index2.default,
          'options': resolutions[0]
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
              updateAvatar: this.updateAvatar,
              showIndex: this.showIndex });
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

},{"../../index":45,"../../reducers/users":49,"../../services/ajax":50,"../../services/store":58,"../modal-loader":33,"./index":28,"react":"react"}],30:[function(require,module,exports){
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
          this.props.label,
          ':'
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

},{"react":"react"}],31:[function(require,module,exports){
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _validators = require('../utils/validators');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

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
        var newState = {};
        newState[name] = event.target.value;

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
        _this.setState({ 'isLoading': true });
        var promise = _this.send();

        if (promise) {
          promise.then(function (success) {
            _this.setState({ 'isLoading': false });
            _this.handleSuccess(success);
          }, function (rejection) {
            _this.setState({ 'isLoading': false });
            _this.handleError(rejection);
          });
        } else {
          _this.setState({ 'isLoading': false });
        }
      }
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(_class, [{
    key: 'validate',
    value: function validate() {
      var errors = {};

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

},{"../utils/validators":63,"react":"react"}],32:[function(require,module,exports){
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
        { className: "loader" },
        _react2.default.createElement("div", { className: "loader-spinning-wheel" })
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
}(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],33:[function(require,module,exports){
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

},{"./loader":32,"react":"react"}],34:[function(require,module,exports){
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

},{"../services/zxcvbn":59,"react":"react"}],35:[function(require,module,exports){
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

},{"../services/captcha":52,"../services/modal":56,"../services/snackbar":57,"../services/zxcvbn":59,"./loader":32,"./register.js":36,"react":"react"}],36:[function(require,module,exports){
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

},{"../index":45,"../services/ajax":50,"../services/auth":51,"../services/captcha":52,"../services/modal":56,"../services/snackbar":57,"../utils/banned-page":60,"../utils/validators":63,"./button":27,"./form":31,"./form-group":30,"./password-strength":34,"react":"react"}],37:[function(require,module,exports){
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

},{"../index":45,"../services/ajax":50,"../services/snackbar":57,"../utils/banned-page":60,"../utils/validators":63,"./button":27,"./form":31,"react":"react"}],38:[function(require,module,exports){
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

},{"../index":45,"../services/ajax":50,"../services/snackbar":57,"../utils/banned-page":60,"../utils/validators":63,"./button":27,"./form":31,"react":"react","react-dom":"react-dom"}],39:[function(require,module,exports){
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

},{"../index":45,"../services/ajax":50,"../services/auth":51,"../services/modal":56,"../services/snackbar":57,"../utils/banned-page":60,"../utils/validators":63,"./button":27,"./form":31,"./sign-in.js":40,"react":"react","react-dom":"react-dom"}],40:[function(require,module,exports){
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

},{"../index":45,"../services/ajax":50,"../services/modal":56,"../services/snackbar":57,"../utils/banned-page":60,"./button":27,"./form":31,"react":"react"}],41:[function(require,module,exports){
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

},{"react":"react"}],42:[function(require,module,exports){
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

},{"../../services/mobile-navbar-dropdown":55,"../../services/modal":56,"../avatar":25,"../register-button":35,"../sign-in.js":40,"react":"react"}],43:[function(require,module,exports){
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

},{"./guest-nav":42,"./user-nav":44,"react":"react"}],44:[function(require,module,exports){
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
              'face'
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
  console.log(state);
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

},{"../../index":45,"../../services/mobile-navbar-dropdown":55,"../../services/modal":56,"../avatar":25,"../change-avatar/root":29,"react":"react","react-redux":"react-redux"}],45:[function(require,module,exports){
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
      return this._context.hasOwnProperty(key);
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

},{"./utils/ordered-list":62}],46:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.SIGN_OUT = exports.SIGN_IN = exports.initialState = undefined;
exports.signIn = signIn;
exports.signOut = signOut;
exports.default = auth;

var _users = require('./users');

var initialState = exports.initialState = {
  signedIn: false,
  signedOut: false
};

var SIGN_IN = exports.SIGN_IN = 'SIGN_IN';
var SIGN_OUT = exports.SIGN_OUT = 'SIGN_OUT';

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
        var newState = Object.assign({}, state);
        newState.user = Object.assign({}, state.user, {
          'avatar_hash': action.avatarHash
        });
        return newState;
      }
      return state;

    default:
      return state;
  }
}

},{"./users":49}],47:[function(require,module,exports){
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

},{}],48:[function(require,module,exports){
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

},{}],49:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.updateAvatar = updateAvatar;
var UPDATE_AVATAR = exports.UPDATE_AVATAR = 'UPDATE_AVATAR';

function updateAvatar(user, avatarHash) {
  return {
    type: UPDATE_AVATAR,
    userId: user.id,
    avatarHash: avatarHash
  };
}

},{}],50:[function(require,module,exports){
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

          data: data || {},
          dataType: 'json',

          success: function success(data) {
            resolve(data);
          },

          error: function error(jqXHR) {
            var rejection = jqXHR.responseJSON || {};

            rejection.status = jqXHR.status;
            rejection.statusText = jqXHR.statusText;

            reject(rejection);
          }
        };

        $.ajax(xhr);
      });
    }
  }, {
    key: 'get',
    value: function get(url) {
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
  }]);

  return Ajax;
}();

exports.default = new Ajax();

},{}],51:[function(require,module,exports){
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

},{"../reducers/auth":46}],52:[function(require,module,exports){
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

},{"../components/form-group":30,"react":"react"}],53:[function(require,module,exports){
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

},{}],54:[function(require,module,exports){
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

},{}],55:[function(require,module,exports){
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

},{"../utils/mount-component":61}],56:[function(require,module,exports){
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

},{"../utils/mount-component":61,"react-dom":"react-dom"}],57:[function(require,module,exports){
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
        message = gettext("Lost connection with application.");
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

},{"../reducers/snackbar":47}],58:[function(require,module,exports){
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

},{"redux":"redux"}],59:[function(require,module,exports){
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

},{}],60:[function(require,module,exports){
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

},{"../components/banned-page":26,"../index":45,"../services/store":58,"moment":"moment","react":"react","react-dom":"react-dom","react-redux":"react-redux"}],61:[function(require,module,exports){
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

},{"../services/store":58,"react":"react","react-dom":"react-dom","react-redux":"react-redux"}],62:[function(require,module,exports){
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

},{}],63:[function(require,module,exports){
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

},{}]},{},[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzcmMvaW5kZXguanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2FqYXguanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2F1dGgtbWVzc2FnZS1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2F1dGgtcmVkdWNlci5qcyIsInNyYy9pbml0aWFsaXplcnMvYXV0aC5qcyIsInNyYy9pbml0aWFsaXplcnMvYmFubmVkLXBhZ2UtY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy9jYXRjaGEuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2luY2x1ZGUuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL2xvY2FsLXN0b3JhZ2UuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL21vYmlsZS1uYXZiYXItZHJvcGRvd24uanMiLCJzcmMvaW5pdGlhbGl6ZXJzL21vZGFsLmpzIiwic3JjL2luaXRpYWxpemVycy9tb21lbnQtbG9jYWxlLmpzIiwic3JjL2luaXRpYWxpemVycy9yZXF1ZXN0LWFjdGl2YXRpb24tbGluay1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3JlcXVlc3QtcGFzc3dvcmQtcmVzZXQtY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy9yZXNldC1wYXNzd29yZC1mb3JtLWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvc25hY2tiYXItY29tcG9uZW50LmpzIiwic3JjL2luaXRpYWxpemVycy9zbmFja2Jhci1yZWR1Y2VyLmpzIiwic3JjL2luaXRpYWxpemVycy9zbmFja2Jhci5qcyIsInNyYy9pbml0aWFsaXplcnMvc3RvcmUuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3RpY2stcmVkdWNlci5qcyIsInNyYy9pbml0aWFsaXplcnMvdGljay1zdGFydC5qcyIsInNyYy9pbml0aWFsaXplcnMvdXNlci1tZW51LWNvbXBvbmVudC5qcyIsInNyYy9pbml0aWFsaXplcnMvenhjdmJuLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9hdXRoLW1lc3NhZ2UuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2F2YXRhci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvYmFubmVkLXBhZ2UuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL2J1dHRvbi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9pbmRleC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9yb290LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9mb3JtLWdyb3VwLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9mb3JtLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9sb2FkZXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL21vZGFsLWxvYWRlci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvcGFzc3dvcmQtc3RyZW5ndGguanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3JlZ2lzdGVyLWJ1dHRvbi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvcmVnaXN0ZXIuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9yZXF1ZXN0LXBhc3N3b3JkLXJlc2V0LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9yZXNldC1wYXNzd29yZC1mb3JtLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9zaWduLWluLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvY29tcG9uZW50cy9zbmFja2Jhci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvdXNlci1tZW51L2d1ZXN0LW5hdi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2NvbXBvbmVudHMvdXNlci1tZW51L3Jvb3QuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9jb21wb25lbnRzL3VzZXItbWVudS91c2VyLW5hdi5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL2luZGV4LmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvcmVkdWNlcnMvYXV0aC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3JlZHVjZXJzL3NuYWNrYmFyLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvcmVkdWNlcnMvdGljay5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3JlZHVjZXJzL3VzZXJzLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvYWpheC5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL2F1dGguanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9jYXB0Y2hhLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvaW5jbHVkZS5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL2xvY2FsLXN0b3JhZ2UuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9tb2JpbGUtbmF2YmFyLWRyb3Bkb3duLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvbW9kYWwuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy9zZXJ2aWNlcy9zbmFja2Jhci5qcyIsIi4uLy4uLy4uL2RvY3VtZW50cy9taXNhZ28vZnJvbnRlbmQvc3JjL3NlcnZpY2VzL3N0b3JlLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvc2VydmljZXMvenhjdmJuLmpzIiwiLi4vLi4vLi4vZG9jdW1lbnRzL21pc2Fnby9mcm9udGVuZC9zcmMvdXRpbHMvYmFubmVkLXBhZ2UuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9tb3VudC1jb21wb25lbnQuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy9vcmRlcmVkLWxpc3QuanMiLCIuLi8uLi8uLi9kb2N1bWVudHMvbWlzYWdvL2Zyb250ZW5kL3NyYy91dGlscy92YWxpZGF0b3JzLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0lDRWEsTUFBTSxXQUFOLE1BQU07QUFDakIsV0FEVyxNQUFNLEdBQ0g7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LENBQUM7R0FDZixDQUFDO0FBQ0YsU0FBTyxJQUFJLENBQUMsU0FBUyxDQUFDLFFBQVEsQ0FBQyxtQkFBbUIsRUFBRSxPQUFPLENBQUMsQ0FBQztDQUM5RDs7QUFFTSxTQUFTLGlCQUFpQixDQUFDLFFBQVEsRUFBRTtBQUMxQyxNQUFJLE9BQU8sR0FBRyxTQUFWLE9BQU8sQ0FBWSxVQUFVLEVBQUU7QUFDakMsV0FBTyxRQUFRLENBQ2IsMkRBQTJELEVBQzNELDREQUE0RCxFQUM1RCxVQUFVLENBQUMsQ0FBQztHQUNmLENBQUM7QUFDRixTQUFPLElBQUksQ0FBQyxTQUFTLENBQUMsUUFBUSxDQUFDLG1CQUFtQixFQUFFLE9BQU8sQ0FBQyxDQUFDO0NBQzlEOztBQUVNLFNBQVMsZUFBZSxHQUFHO0FBQ2hDLFNBQU8sVUFBUyxLQUFLLEVBQUU7QUFDckIsUUFBSSxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQyxFQUFFO0FBQ2pDLGFBQU8sT0FBTyxDQUFDLDhEQUE4RCxDQUFDLENBQUM7S0FDaEY7R0FDRixDQUFDO0NBQ0g7O0FBRU0sU0FBUyxpQkFBaUIsQ0FBQyxRQUFRLEVBQUU7QUFDMUMsTUFBSSxPQUFPLEdBQUcsU0FBVixPQUFPLENBQVksVUFBVSxFQUFFO0FBQ2pDLFdBQU8sUUFBUSxDQUNiLGlFQUFpRSxFQUNqRSxrRUFBa0UsRUFDbEUsVUFBVSxDQUFDLENBQUM7R0FDZixDQUFDO0FBQ0YsU0FBTyxJQUFJLENBQUMsU0FBUyxDQUFDLFFBQVEsQ0FBQyxtQkFBbUIsRUFBRSxPQUFPLENBQUMsQ0FBQztDQUM5RCIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIGUodCxuLHIpe2Z1bmN0aW9uIHMobyx1KXtpZighbltvXSl7aWYoIXRbb10pe3ZhciBhPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7aWYoIXUmJmEpcmV0dXJuIGEobywhMCk7aWYoaSlyZXR1cm4gaShvLCEwKTt2YXIgZj1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK28rXCInXCIpO3Rocm93IGYuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixmfXZhciBsPW5bb109e2V4cG9ydHM6e319O3Rbb11bMF0uY2FsbChsLmV4cG9ydHMsZnVuY3Rpb24oZSl7dmFyIG49dFtvXVsxXVtlXTtyZXR1cm4gcyhuP246ZSl9LGwsbC5leHBvcnRzLGUsdCxuLHIpfXJldHVybiBuW29dLmV4cG9ydHN9dmFyIGk9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtmb3IodmFyIG89MDtvPHIubGVuZ3RoO28rKylzKHJbb10pO3JldHVybiBzfSkiLCJpbXBvcnQgT3JkZXJlZExpc3QgZnJvbSAnbWlzYWdvL3V0aWxzL29yZGVyZWQtbGlzdCc7XG5cbmV4cG9ydCBjbGFzcyBNaXNhZ28ge1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICB0aGlzLl9pbml0aWFsaXplcnMgPSBbXTtcbiAgICB0aGlzLl9jb250ZXh0ID0ge307XG4gIH1cblxuICBhZGRJbml0aWFsaXplcihpbml0aWFsaXplcikge1xuICAgIHRoaXMuX2luaXRpYWxpemVycy5wdXNoKHtcbiAgICAgIGtleTogaW5pdGlhbGl6ZXIubmFtZSxcblxuICAgICAgaXRlbTogaW5pdGlhbGl6ZXIuaW5pdGlhbGl6ZXIsXG5cbiAgICAgIGFmdGVyOiBpbml0aWFsaXplci5hZnRlcixcbiAgICAgIGJlZm9yZTogaW5pdGlhbGl6ZXIuYmVmb3JlXG4gICAgfSk7XG4gIH1cblxuICBpbml0KGNvbnRleHQpIHtcbiAgICB0aGlzLl9jb250ZXh0ID0gY29udGV4dDtcblxuICAgIHZhciBpbml0T3JkZXIgPSBuZXcgT3JkZXJlZExpc3QodGhpcy5faW5pdGlhbGl6ZXJzKS5vcmRlcmVkVmFsdWVzKCk7XG4gICAgaW5pdE9yZGVyLmZvckVhY2goaW5pdGlhbGl6ZXIgPT4ge1xuICAgICAgaW5pdGlhbGl6ZXIodGhpcyk7XG4gICAgfSk7XG4gIH1cblxuICAvLyBjb250ZXh0IGFjY2Vzc29yc1xuICBoYXMoa2V5KSB7XG4gICAgcmV0dXJuIHRoaXMuX2NvbnRleHQuaGFzT3duUHJvcGVydHkoa2V5KTtcbiAgfVxuXG4gIGdldChrZXksIGZhbGxiYWNrKSB7XG4gICAgaWYgKHRoaXMuaGFzKGtleSkpIHtcbiAgICAgIHJldHVybiB0aGlzLl9jb250ZXh0W2tleV07XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBmYWxsYmFjayB8fCB1bmRlZmluZWQ7XG4gICAgfVxuICB9XG59XG5cbi8vIGNyZWF0ZSAgc2luZ2xldG9uXG52YXIgbWlzYWdvID0gbmV3IE1pc2FnbygpO1xuXG4vLyBleHBvc2UgaXQgZ2xvYmFsbHlcbmdsb2JhbC5taXNhZ28gPSBtaXNhZ287XG5cbi8vIGFuZCBleHBvcnQgaXQgZm9yIHRlc3RzIGFuZCBzdHVmZlxuZXhwb3J0IGRlZmF1bHQgbWlzYWdvO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgYWpheC5pbml0KG1pc2Fnby5nZXQoJ0NTUkZfQ09PS0lFX05BTUUnKSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdhamF4JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCB7IGNvbm5lY3QgfSBmcm9tICdyZWFjdC1yZWR1eCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgQXV0aE1lc3NhZ2UsIHsgc2VsZWN0IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYXV0aC1tZXNzYWdlJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIG1vdW50KGNvbm5lY3Qoc2VsZWN0KShBdXRoTWVzc2FnZSksICdhdXRoLW1lc3NhZ2UtbW91bnQnKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NvbXBvbmVudDphdXRoLW1lc3NhZ2UnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCByZWR1Y2VyLCB7IGluaXRpYWxTdGF0ZSB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9hdXRoJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcihjb250ZXh0KSB7XG4gIHN0b3JlLmFkZFJlZHVjZXIoJ2F1dGgnLCByZWR1Y2VyLCBPYmplY3QuYXNzaWduKHtcbiAgICAnaXNBdXRoZW50aWNhdGVkJzogY29udGV4dC5nZXQoJ2lzQXV0aGVudGljYXRlZCcpLFxuICAgICdpc0Fub255bW91cyc6ICFjb250ZXh0LmdldCgnaXNBdXRoZW50aWNhdGVkJyksXG5cbiAgICAndXNlcic6IGNvbnRleHQuZ2V0KCd1c2VyJylcbiAgfSwgaW5pdGlhbFN0YXRlKSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOmF1dGgnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgYXV0aCBmcm9tICdtaXNhZ28vc2VydmljZXMvYXV0aCc7XG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuaW1wb3J0IHN0b3JhZ2UgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2xvY2FsLXN0b3JhZ2UnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgYXV0aC5pbml0KHN0b3JlLCBzdG9yYWdlLCBtb2RhbCk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdhdXRoJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7IiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHNob3dCYW5uZWRQYWdlIGZyb20gJ21pc2Fnby91dGlscy9iYW5uZWQtcGFnZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKGNvbnRleHQpIHtcbiAgaWYgKGNvbnRleHQuZ2V0KCdCQU5fTUVTU0FHRScpKSB7XG4gICAgc2hvd0Jhbm5lZFBhZ2UoY29udGV4dC5nZXQoJ0JBTl9NRVNTQUdFJyksIGZhbHNlKTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OmJhbmVkLXBhZ2UnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBjYXB0Y2hhIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9jYXB0Y2hhJztcbmltcG9ydCBpbmNsdWRlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9pbmNsdWRlJztcbmltcG9ydCBzbmFja2JhciBmcm9tICdtaXNhZ28vc2VydmljZXMvc25hY2tiYXInO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcihjb250ZXh0KSB7XG4gIGNhcHRjaGEuaW5pdChjb250ZXh0LCBhamF4LCBpbmNsdWRlLCBzbmFja2Jhcik7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjYXB0Y2hhJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBpbmNsdWRlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9pbmNsdWRlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoY29udGV4dCkge1xuICBpbmNsdWRlLmluaXQoY29udGV4dC5nZXQoJ1NUQVRJQ19VUkwnKSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdpbmNsdWRlJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBzdG9yYWdlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9sb2NhbC1zdG9yYWdlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHN0b3JhZ2UuaW5pdCgnbWlzYWdvXycpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnbG9jYWwtc3RvcmFnZScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplclxufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgZHJvcGRvd24gZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vYmlsZS1uYXZiYXItZHJvcGRvd24nO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbGV0IGVsZW1lbnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnbW9iaWxlLW5hdmJhci1kcm9wZG93bi1tb3VudCcpO1xuICBpZiAoZWxlbWVudCkge1xuICAgIGRyb3Bkb3duLmluaXQoZWxlbWVudCk7XG4gIH1cbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2Ryb3Bkb3duJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IG1vZGFsIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2RhbCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBsZXQgZWxlbWVudCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdtb2RhbC1tb3VudCcpO1xuICBpZiAoZWxlbWVudCkge1xuICAgIG1vZGFsLmluaXQoZWxlbWVudCk7XG4gIH1cbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ21vZGFsJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbW9tZW50LmxvY2FsZSgkKCdodG1sJykuYXR0cignbGFuZycpKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ21vbWVudCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplclxufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgUmVxdWVzdEFjdGl2YXRpb25MaW5rIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGlmIChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVxdWVzdC1hY3RpdmF0aW9uLWxpbmstbW91bnQnKSkge1xuICAgIG1vdW50KFJlcXVlc3RBY3RpdmF0aW9uTGluaywgJ3JlcXVlc3QtYWN0aXZhdGlvbi1saW5rLW1vdW50JywgZmFsc2UpO1xuICB9XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6cmVxdWVzdC1hY3RpdmF0aW9uLWxpbmsnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBSZXF1ZXN0UGFzc3dvcmRSZXNldCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9yZXF1ZXN0LXBhc3N3b3JkLXJlc2V0JztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGlmIChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVxdWVzdC1wYXNzd29yZC1yZXNldC1tb3VudCcpKSB7XG4gICAgbW91bnQoUmVxdWVzdFBhc3N3b3JkUmVzZXQsICdyZXF1ZXN0LXBhc3N3b3JkLXJlc2V0LW1vdW50JywgZmFsc2UpO1xuICB9XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6cmVxdWVzdC1wYXNzd29yZC1yZXNldCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IFJlc2V0UGFzc3dvcmRGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3Jlc2V0LXBhc3N3b3JkLWZvcm0nO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgaWYgKGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZXNldC1wYXNzd29yZC1mb3JtLW1vdW50JykpIHtcbiAgICBtb3VudChSZXNldFBhc3N3b3JkRm9ybSwgJ3Jlc2V0LXBhc3N3b3JkLWZvcm0tbW91bnQnLCBmYWxzZSk7XG4gIH1cbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NvbXBvbmVudDpyZXNldC1wYXNzd29yZC1mb3JtJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgeyBjb25uZWN0IH0gZnJvbSAncmVhY3QtcmVkdXgnO1xuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHsgU25hY2tiYXIsIHNlbGVjdCB9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3NuYWNrYmFyJztcbmltcG9ydCBtb3VudCBmcm9tICdtaXNhZ28vdXRpbHMvbW91bnQtY29tcG9uZW50JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIG1vdW50KGNvbm5lY3Qoc2VsZWN0KShTbmFja2JhciksICdzbmFja2Jhci1tb3VudCcpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnY29tcG9uZW50OnNuYWNrYmFyJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3NuYWNrYmFyJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgcmVkdWNlciwgeyBpbml0aWFsU3RhdGUgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvc25hY2tiYXInO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBzdG9yZS5hZGRSZWR1Y2VyKCdzbmFja2JhcicsIHJlZHVjZXIsIGluaXRpYWxTdGF0ZSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOnNuYWNrYmFyJyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBiZWZvcmU6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHNuYWNrYmFyLmluaXQoc3RvcmUpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnc25hY2tiYXInLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc3RvcmUuaW5pdCgpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnc3RvcmUnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ19lbmQnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCByZWR1Y2VyLCB7IGluaXRpYWxTdGF0ZSB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy90aWNrJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc3RvcmUuYWRkUmVkdWNlcigndGljaycsIHJlZHVjZXIsIGluaXRpYWxTdGF0ZSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdyZWR1Y2VyOnRpY2snLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgeyBkb1RpY2sgfSBmcm9tICdtaXNhZ28vcmVkdWNlcnMvdGljayc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuY29uc3QgVElDS19QRVJJT0QgPSA1MCAqIDEwMDA7IC8vZG8gdGhlIHRpY2sgZXZlcnkgNTBzXG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICB3aW5kb3cuc2V0SW50ZXJ2YWwoZnVuY3Rpb24oKSB7XG4gICAgc3RvcmUuZGlzcGF0Y2goZG9UaWNrKCkpO1xuICB9LCBUSUNLX1BFUklPRCk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICd0aWNrLXN0YXJ0JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgeyBjb25uZWN0IH0gZnJvbSAncmVhY3QtcmVkdXgnO1xuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHsgVXNlck1lbnUsIENvbXBhY3RVc2VyTWVudSwgc2VsZWN0IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvdXNlci1tZW51L3Jvb3QnO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbW91bnQoY29ubmVjdChzZWxlY3QpKFVzZXJNZW51KSwgJ3VzZXItbWVudS1tb3VudCcpO1xuICBtb3VudChjb25uZWN0KHNlbGVjdCkoQ29tcGFjdFVzZXJNZW51KSwgJ3VzZXItbWVudS1jb21wYWN0LW1vdW50Jyk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6dXNlci1tZW51JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyLFxuICBhZnRlcjogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgaW5jbHVkZSBmcm9tICdtaXNhZ28vc2VydmljZXMvaW5jbHVkZSc7XG5pbXBvcnQgenhjdmJuIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy96eGN2Ym4nO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgenhjdmJuLmluaXQoaW5jbHVkZSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICd6eGN2Ym4nLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXJcbn0pO1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZWZyZXNoKCkge1xuICAgIHdpbmRvdy5sb2NhdGlvbi5yZWxvYWQoKTtcbiAgfVxuXG4gIGdldE1lc3NhZ2UoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuc2lnbmVkSW4pIHtcbiAgICAgIHJldHVybiBpbnRlcnBvbGF0ZShcbiAgICAgICAgZ2V0dGV4dChcIllvdSBoYXZlIHNpZ25lZCBpbiBhcyAlKHVzZXJuYW1lKXMuIFBsZWFzZSByZWZyZXNoIHRoZSBwYWdlIGJlZm9yZSBjb250aW51aW5nLlwiKSxcbiAgICAgICAge3VzZXJuYW1lOiB0aGlzLnByb3BzLnNpZ25lZEluLnVzZXJuYW1lfSwgdHJ1ZSk7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLnNpZ25lZE91dCkge1xuICAgICAgcmV0dXJuIGludGVycG9sYXRlKFxuICAgICAgICBnZXR0ZXh0KFwiJSh1c2VybmFtZSlzLCB5b3UgaGF2ZSBiZWVuIHNpZ25lZCBvdXQuIFBsZWFzZSByZWZyZXNoIHRoZSBwYWdlIGJlZm9yZSBjb250aW51aW5nLlwiKSxcbiAgICAgICAge3VzZXJuYW1lOiB0aGlzLnByb3BzLnVzZXIudXNlcm5hbWV9LCB0cnVlKTtcbiAgICB9XG4gIH1cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuc2lnbmVkSW4gfHwgdGhpcy5wcm9wcy5zaWduZWRPdXQpIHtcbiAgICAgIHJldHVybiBcImF1dGgtbWVzc2FnZSBzaG93XCI7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBcImF1dGgtbWVzc2FnZVwiO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPXt0aGlzLmdldENsYXNzTmFtZSgpfT5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxwIGNsYXNzTmFtZT1cImxlYWRcIj57dGhpcy5nZXRNZXNzYWdlKCl9PC9wPlxuICAgICAgICA8cD5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLWRlZmF1bHRcIlxuICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5yZWZyZXNofT5cbiAgICAgICAgICAgIHtnZXR0ZXh0KFwiUmVsb2FkIHBhZ2VcIil9XG4gICAgICAgICAgPC9idXR0b24+IDxzcGFuIGNsYXNzTmFtZT1cImhpZGRlbi14cyBoaWRkZW4tc20gdGV4dC1tdXRlZFwiPlxuICAgICAgICAgICAge2dldHRleHQoXCJvciBwcmVzcyBGNSBrZXkuXCIpfVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9wPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4ge1xuICAgIHVzZXI6IHN0YXRlLmF1dGgudXNlcixcbiAgICBzaWduZWRJbjogc3RhdGUuYXV0aC5zaWduZWRJbixcbiAgICBzaWduZWRPdXQ6IHN0YXRlLmF1dGguc2lnbmVkT3V0XG4gIH07XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuY29uc3QgQkFTRV9VUkwgPSAkKCdiYXNlJykuYXR0cignaHJlZicpICsgJ3VzZXItYXZhdGFyLyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0U3JjKCkge1xuICAgIGxldCBzaXplID0gdGhpcy5wcm9wcy5zaXplIHx8IDEwMDsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG4gICAgbGV0IHVybCA9IEJBU0VfVVJMO1xuXG4gICAgaWYgKHRoaXMucHJvcHMudXNlciAmJiB0aGlzLnByb3BzLnVzZXIuaWQpIHtcbiAgICAgIC8vIGp1c3QgYXZhdGFyIGhhc2gsIHNpemUgYW5kIHVzZXIgaWRcbiAgICAgIHVybCArPSB0aGlzLnByb3BzLnVzZXIuYXZhdGFyX2hhc2ggKyAnLycgKyBzaXplICsgJy8nICsgdGhpcy5wcm9wcy51c2VyLmlkICsgJy5wbmcnO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBqdXN0IGFwcGVuZCBhdmF0YXIgc2l6ZSB0byBmaWxlIHRvIHByb2R1Y2Ugbm8tYXZhdGFyIHBsYWNlaG9sZGVyXG4gICAgICB1cmwgKz0gc2l6ZSArICcucG5nJztcbiAgICB9XG5cbiAgICByZXR1cm4gdXJsO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGltZyBzcmM9e3RoaXMuZ2V0U3JjKCl9XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lPXt0aGlzLnByb3BzLmNsYXNzTmFtZSB8fCAndXNlci1hdmF0YXInfVxuICAgICAgICAgICAgICAgIHRpdGxlPXtnZXR0ZXh0KFwiVXNlciBhdmF0YXJcIil9Lz47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRSZWFzb25NZXNzYWdlKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBpZiAodGhpcy5wcm9wcy5tZXNzYWdlLmh0bWwpIHtcbiAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImxlYWRcIlxuICAgICAgICAgICAgICAgICAgZGFuZ2Vyb3VzbHlTZXRJbm5lckhUTUw9e3tfX2h0bWw6IHRoaXMucHJvcHMubWVzc2FnZS5odG1sfX0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8cCBjbGFzc05hbWU9XCJsZWFkXCI+e3RoaXMucHJvcHMubWVzc2FnZS5wbGFpbn08L3A+O1xuICAgIH1cbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG5cbiAgZ2V0RXhwaXJhdGlvbk1lc3NhZ2UoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuZXhwaXJlcykge1xuICAgICAgaWYgKHRoaXMucHJvcHMuZXhwaXJlcy5pc0FmdGVyKG1vbWVudCgpKSkge1xuICAgICAgICByZXR1cm4gaW50ZXJwb2xhdGUoXG4gICAgICAgICAgZ2V0dGV4dChcIlRoaXMgYmFuIGV4cGlyZXMgJShleHBpcmVzX29uKXMuXCIpLFxuICAgICAgICAgIHsnZXhwaXJlc19vbic6IHRoaXMucHJvcHMuZXhwaXJlcy5mcm9tTm93KCl9LFxuICAgICAgICAgIHRydWUpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIGdldHRleHQoXCJUaGlzIGJhbiBoYXMgZXhwaXJlZC5cIik7XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiVGhpcyBiYW4gaXMgcGVybWFuZW50LlwiKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UgcGFnZS1lcnJvciBwYWdlLWVycm9yLWJhbm5lZFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250YWluZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLXBhbmVsXCI+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPmhpZ2hsaWdodF9vZmY8L3NwYW4+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWJvZHlcIj5cbiAgICAgICAgICAgIHt0aGlzLmdldFJlYXNvbk1lc3NhZ2UoKX1cbiAgICAgICAgICAgIDxwIGNsYXNzTmFtZT1cIm1lc3NhZ2UtZm9vdG5vdGVcIj5cbiAgICAgICAgICAgICAge3RoaXMuZ2V0RXhwaXJhdGlvbk1lc3NhZ2UoKX1cbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBMb2FkZXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvbG9hZGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIEJ1dHRvbiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICBsZXQgY2xhc3NOYW1lID0gJ2J0biAnICsgdGhpcy5wcm9wcy5jbGFzc05hbWU7XG4gICAgbGV0IGRpc2FibGVkID0gdGhpcy5wcm9wcy5kaXNhYmxlZDtcblxuICAgIGlmICh0aGlzLnByb3BzLmxvYWRpbmcpIHtcbiAgICAgIGNsYXNzTmFtZSArPSAnIGJ0bi1sb2FkaW5nJztcbiAgICAgIGRpc2FibGVkID0gdHJ1ZTtcbiAgICB9XG5cbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxidXR0b24gdHlwZT17dGhpcy5wcm9wcy5vbkNsaWNrID8gJ2J1dHRvbicgOiAnc3VibWl0J31cbiAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9e2NsYXNzTmFtZX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17ZGlzYWJsZWR9XG4gICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5wcm9wcy5vbkNsaWNrfT5cbiAgICAgIHt0aGlzLnByb3BzLmNoaWxkcmVufVxuICAgICAge3RoaXMucHJvcHMubG9hZGluZyA/IDxMb2FkZXIgLz4gOiBudWxsfVxuICAgIDwvYnV0dG9uPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cblxuQnV0dG9uLmRlZmF1bHRQcm9wcyA9IHtcbiAgY2xhc3NOYW1lOiBcImJ0bi1kZWZhdWx0XCIsXG5cbiAgdHlwZTogXCJzdWJtaXRcIixcblxuICBsb2FkaW5nOiBmYWxzZSxcbiAgZGlzYWJsZWQ6IGZhbHNlLFxuXG4gIG9uQ2xpY2s6IG51bGxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEF2YXRhciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdmF0YXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgTG9hZGVyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2xvYWRlcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIGNhbGxBcGkoYXZhdGFyVHlwZSkge1xuICAgIGlmICh0aGlzLnN0YXRlLmlzTG9hZGluZykge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ2lzTG9hZGluZyc6IHRydWVcbiAgICB9KTtcblxuICAgIGFqYXgucG9zdCh0aGlzLnByb3BzLnVzZXIuYXZhdGFyX2FwaV91cmwsIHtcbiAgICAgIGF2YXRhcjogYXZhdGFyVHlwZVxuICAgIH0pLnRoZW4oKHJlc3BvbnNlKSA9PiB7XG4gICAgICBzbmFja2Jhci5zdWNjZXNzKHJlc3BvbnNlLmRldGFpbCk7XG4gICAgICB0aGlzLnByb3BzLnVwZGF0ZUF2YXRhcihyZXNwb25zZS5hdmF0YXJfaGFzaCwgcmVzcG9uc2Uub3B0aW9ucyk7XG5cbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnaXNMb2FkaW5nJzogZmFsc2VcbiAgICAgIH0pO1xuICAgIH0sIChyZWplY3Rpb24pID0+IHtcbiAgICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzbmFja2Jhci5zaG93RXJyb3IocmVqZWN0aW9uKTtcbiAgICAgIH1cblxuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICdpc0xvYWRpbmcnOiBmYWxzZVxuICAgICAgfSk7XG4gICAgfSk7XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIHNldEdyYXZhdGFyID0gKCkgPT4ge1xuICAgIHRoaXMuY2FsbEFwaSgnZ3JhdmF0YXInKTtcbiAgfTtcblxuICBzZXRHZW5lcmF0ZWQgPSAoKSA9PiB7XG4gICAgdGhpcy5jYWxsQXBpKCdnZW5lcmF0ZWQnKTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRHcmF2YXRhckJ1dHRvbigpIHtcbiAgICBpZiAodGhpcy5wcm9wcy5vcHRpb25zLmdyYXZhdGFyKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnNldEdyYXZhdGFyfVxuICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiPlxuICAgICAgICB7Z2V0dGV4dChcIkRvd25sb2FkIG15IEdyYXZhdGFyXCIpfVxuICAgICAgPC9CdXR0b24+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgZ2V0QXZhdGFyUHJldmlldygpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRpbmcpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImF2YXRhci1wcmV2aWV3IHByZXZpZXctbG9hZGluZ1wiPlxuICAgICAgICA8QXZhdGFyIHVzZXI9e3RoaXMucHJvcHMudXNlcn0gc2l6ZT1cIjIwMFwiIC8+XG4gICAgICAgIDxMb2FkZXIgLz5cbiAgICAgIDwvZGl2PjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImF2YXRhci1wcmV2aWV3XCI+XG4gICAgICAgIDxBdmF0YXIgdXNlcj17dGhpcy5wcm9wcy51c2VyfSBzaXplPVwiMjAwXCIgLz5cbiAgICAgIDwvZGl2PjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5IG1vZGFsLWF2YXRhci1pbmRleFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJyb3dcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wtbWQtNVwiPlxuXG4gICAgICAgICAge3RoaXMuZ2V0QXZhdGFyUHJldmlldygpfVxuXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC1tZC03XCI+XG5cbiAgICAgICAgICB7dGhpcy5nZXRHcmF2YXRhckJ1dHRvbigpfVxuXG4gICAgICAgICAgPEJ1dHRvbiBvbkNsaWNrPXt0aGlzLnNldEdlbmVyYXRlZH1cbiAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAge2dldHRleHQoXCJHZW5lcmF0ZSBteSBpbmRpdmlkdWFsIGF2YXRhclwiKX1cbiAgICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBBdmF0YXJJbmRleCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9jaGFuZ2UtYXZhdGFyL2luZGV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgTG9hZGVyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL21vZGFsLWxvYWRlcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHsgdXBkYXRlQXZhdGFyIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3VzZXJzJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBjbGFzcyBDaGFuZ2VBdmF0YXJFcnJvciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldEVycm9yUmVhc29uKCkge1xuICAgIGlmICh0aGlzLnByb3BzLnJlYXNvbikge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxwIGRhbmdlcm91c2x5U2V0SW5uZXJIVE1MPXt7X19odG1sOiB0aGlzLnByb3BzLnJlYXNvbn19IC8+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtaWNvblwiPlxuICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgcmVtb3ZlX2NpcmNsZV9vdXRsaW5lXG4gICAgICAgIDwvc3Bhbj5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWJvZHlcIj5cbiAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgIHt0aGlzLnByb3BzLm1lc3NhZ2V9XG4gICAgICAgIDwvcD5cbiAgICAgICAge3RoaXMuZ2V0RXJyb3JSZWFzb24oKX1cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgUHJvbWlzZS5hbGwoW1xuICAgICAgYWpheC5nZXQobWlzYWdvLmdldCgndXNlcicpLmF2YXRhcl9hcGlfdXJsKVxuICAgIF0pLnRoZW4oKHJlc29sdXRpb25zKSA9PiB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ2NvbXBvbmVudCc6IEF2YXRhckluZGV4LFxuICAgICAgICAnb3B0aW9ucyc6IHJlc29sdXRpb25zWzBdXG4gICAgICB9KTtcbiAgICB9LCAocmVqZWN0aW9uKSA9PiB7XG4gICAgICB0aGlzLnNob3dFcnJvcihyZWplY3Rpb24pO1xuICAgIH0pO1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBzaG93RXJyb3IgPSAoZXJyb3IpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIGVycm9yXG4gICAgfSk7XG4gIH07XG5cbiAgdXBkYXRlQXZhdGFyID0gKGF2YXRhckhhc2gsIG9wdGlvbnMpID0+IHtcbiAgICBzdG9yZS5kaXNwYXRjaCh1cGRhdGVBdmF0YXIodGhpcy5wcm9wcy51c2VyLCBhdmF0YXJIYXNoKSk7XG5cbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICdjb21wb25lbnQnOiBBdmF0YXJJbmRleCxcbiAgICAgIG9wdGlvbnNcbiAgICB9KTtcbiAgfTtcblxuICBzaG93SW5kZXggPSAoKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAnY29tcG9uZW50JzogQXZhdGFySW5kZXhcbiAgICB9KTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRCb2R5KCkge1xuICAgIGlmICh0aGlzLnN0YXRlKSB7XG4gICAgICBpZiAodGhpcy5zdGF0ZS5lcnJvcikge1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIHJldHVybiA8Q2hhbmdlQXZhdGFyRXJyb3IgbWVzc2FnZT17dGhpcy5zdGF0ZS5lcnJvci5kZXRhaWx9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVhc29uPXt0aGlzLnN0YXRlLmVycm9yLnJlYXNvbn0gLz47XG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIHJldHVybiA8dGhpcy5zdGF0ZS5jb21wb25lbnQgb3B0aW9ucz17dGhpcy5zdGF0ZS5vcHRpb25zfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVzZXI9e3RoaXMucHJvcHMudXNlcn1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB1cGRhdGVBdmF0YXI9e3RoaXMudXBkYXRlQXZhdGFyfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNob3dJbmRleD17dGhpcy5zaG93SW5kZXh9IC8+O1xuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPExvYWRlciAvPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfVxuICB9XG5cbiAgZ2V0Q2xhc3NOYW1lKCkge1xuICAgaWYgKHRoaXMuc3RhdGUgJiYgdGhpcy5zdGF0ZS5lcnJvcikge1xuICAgICAgcmV0dXJuIFwibW9kYWwtZGlhbG9nIG1vZGFsLW1lc3NhZ2UgbW9kYWwtY2hhbmdlLWF2YXRhclwiO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gXCJtb2RhbC1kaWFsb2cgbW9kYWwtY2hhbmdlLWF2YXRhclwiO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPXt0aGlzLmdldENsYXNzTmFtZSgpfVxuICAgICAgICAgICAgICAgIHJvbGU9XCJkb2N1bWVudFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1jb250ZW50XCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtaGVhZGVyXCI+XG4gICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiY2xvc2VcIiBkYXRhLWRpc21pc3M9XCJtb2RhbFwiXG4gICAgICAgICAgICAgICAgICBhcmlhLWxhYmVsPXtnZXR0ZXh0KFwiQ2xvc2VcIil9PlxuICAgICAgICAgICAgPHNwYW4gYXJpYS1oaWRkZW49XCJ0cnVlXCI+JnRpbWVzOzwvc3Bhbj5cbiAgICAgICAgICA8L2J1dHRvbj5cbiAgICAgICAgICA8aDQgY2xhc3NOYW1lPVwibW9kYWwtdGl0bGVcIj57Z2V0dGV4dChcIkNoYW5nZSB5b3VyIGF2YXRhclwiKX08L2g0PlxuICAgICAgICA8L2Rpdj5cblxuICAgICAgICB7dGhpcy5nZXRCb2R5KCl9XG5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzZWxlY3Qoc3RhdGUpIHtcbiAgcmV0dXJuIHtcbiAgICAndXNlcic6IHN0YXRlLmF1dGgudXNlclxuICB9O1xufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBpc1ZhbGlkYXRlZCgpIHtcbiAgICByZXR1cm4gdHlwZW9mIHRoaXMucHJvcHMudmFsaWRhdGlvbiAhPT0gXCJ1bmRlZmluZWRcIjtcbiAgfVxuXG4gIGdldENsYXNzTmFtZSgpIHtcbiAgICBsZXQgY2xhc3NOYW1lID0gJ2Zvcm0tZ3JvdXAnO1xuICAgIGlmICh0aGlzLmlzVmFsaWRhdGVkKCkpIHtcbiAgICAgIGNsYXNzTmFtZSArPSAnIGhhcy1mZWVkYmFjayc7XG4gICAgICBpZiAodGhpcy5wcm9wcy52YWxpZGF0aW9uID09PSBudWxsKSB7XG4gICAgICAgIGNsYXNzTmFtZSArPSAnIGhhcy1zdWNjZXNzJztcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGNsYXNzTmFtZSArPSAnIGhhcy1lcnJvcic7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBjbGFzc05hbWU7XG4gIH1cblxuICBnZXRGZWVkYmFjaygpIHtcbiAgICBpZiAodGhpcy5wcm9wcy52YWxpZGF0aW9uKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJoZWxwLWJsb2NrIGVycm9yc1wiPlxuICAgICAgICB7dGhpcy5wcm9wcy52YWxpZGF0aW9uLm1hcCgoZXJyb3IsIGkpID0+IHtcbiAgICAgICAgICByZXR1cm4gPHAga2V5PXt0aGlzLnByb3BzLmZvciArICdGZWVkYmFja0l0ZW0nICsgaX0+e2Vycm9yfTwvcD47XG4gICAgICAgIH0pfVxuICAgICAgPC9kaXY+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgZ2V0RmVlZGJhY2tJY29uKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWRhdGVkKCkpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uIGZvcm0tY29udHJvbC1mZWVkYmFja1wiXG4gICAgICAgICAgICAgICAgICAgYXJpYS1oaWRkZW49XCJ0cnVlXCIga2V5PXt0aGlzLnByb3BzLmZvciArICdGZWVkYmFja0ljb24nfT5cbiAgICAgICAge3RoaXMucHJvcHMudmFsaWRhdGlvbiA/ICdjbGVhcicgOiAnY2hlY2snfVxuICAgICAgPC9zcGFuPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIGdldEZlZWRiYWNrRGVzY3JpcHRpb24oKSB7XG4gICAgaWYgKHRoaXMuaXNWYWxpZGF0ZWQoKSkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxzcGFuIGlkPXt0aGlzLnByb3BzLmZvciArICdfc3RhdHVzJ30gY2xhc3NOYW1lPVwic3Itb25seVwiPlxuICAgICAgICB7dGhpcy5wcm9wcy52YWxpZGF0aW9uID8gZ2V0dGV4dCgnKGVycm9yKScpIDogZ2V0dGV4dCgnKHN1Y2Nlc3MpJyl9XG4gICAgICA8L3NwYW4+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgZ2V0SGVscFRleHQoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuaGVscFRleHQpIHtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgIHJldHVybiA8cCBjbGFzc05hbWU9XCJoZWxwLWJsb2NrXCI+e3RoaXMucHJvcHMuaGVscFRleHR9PC9wPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPXt0aGlzLmdldENsYXNzTmFtZSgpfT5cbiAgICAgIDxsYWJlbCBjbGFzc05hbWU9eydjb250cm9sLWxhYmVsICcgKyAodGhpcy5wcm9wcy5sYWJlbENsYXNzIHx8ICcnKX1cbiAgICAgICAgICAgICBodG1sRm9yPXt0aGlzLnByb3BzLmZvciB8fCAnJ30+XG4gICAgICAgIHt0aGlzLnByb3BzLmxhYmVsfTpcbiAgICAgIDwvbGFiZWw+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT17dGhpcy5wcm9wcy5jb250cm9sQ2xhc3MgfHwgJyd9PlxuICAgICAgICB7dGhpcy5wcm9wcy5jaGlsZHJlbn1cbiAgICAgICAge3RoaXMuZ2V0RmVlZGJhY2tJY29uKCl9XG4gICAgICAgIHt0aGlzLmdldEZlZWRiYWNrRGVzY3JpcHRpb24oKX1cbiAgICAgICAge3RoaXMuZ2V0RmVlZGJhY2soKX1cbiAgICAgICAge3RoaXMuZ2V0SGVscFRleHQoKX1cbiAgICAgICAge3RoaXMucHJvcHMuZXh0cmEgfHwgbnVsbH1cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyByZXF1aXJlZCB9IGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcblxubGV0IHZhbGlkYXRlUmVxdWlyZWQgPSByZXF1aXJlZCgpO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHZhbGlkYXRlKCkge1xuICAgIGxldCBlcnJvcnMgPSB7fTtcblxuICAgIGxldCB2YWxpZGF0b3JzID0ge1xuICAgICAgcmVxdWlyZWQ6IHRoaXMuc3RhdGUudmFsaWRhdG9ycy5yZXF1aXJlZCB8fCB0aGlzLnN0YXRlLnZhbGlkYXRvcnMsXG4gICAgICBvcHRpb25hbDogdGhpcy5zdGF0ZS52YWxpZGF0b3JzLm9wdGlvbmFsIHx8IHt9XG4gICAgfTtcblxuICAgIGxldCB2YWxpZGF0ZWRGaWVsZHMgPSBbXTtcblxuICAgIC8vIGFkZCByZXF1aXJlZCBmaWVsZHMgdG8gdmFsaWRhdGlvblxuICAgIGZvciAobGV0IG5hbWUgaW4gdmFsaWRhdG9ycy5yZXF1aXJlZCkge1xuICAgICAgaWYgKHZhbGlkYXRvcnMucmVxdWlyZWQuaGFzT3duUHJvcGVydHkobmFtZSkgJiZcbiAgICAgICAgICB2YWxpZGF0b3JzLnJlcXVpcmVkW25hbWVdKSB7XG4gICAgICAgIHZhbGlkYXRlZEZpZWxkcy5wdXNoKG5hbWUpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIGFkZCBvcHRpb25hbCBmaWVsZHMgdG8gdmFsaWRhdGlvblxuICAgIGZvciAobGV0IG5hbWUgaW4gdmFsaWRhdG9ycy5vcHRpb25hbCkge1xuICAgICAgaWYgKHZhbGlkYXRvcnMub3B0aW9uYWwuaGFzT3duUHJvcGVydHkobmFtZSkgJiZcbiAgICAgICAgICB2YWxpZGF0b3JzLm9wdGlvbmFsW25hbWVdKSB7XG4gICAgICAgIHZhbGlkYXRlZEZpZWxkcy5wdXNoKG5hbWUpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIHZhbGlkYXRlIGZpZWxkcyB2YWx1ZXNcbiAgICBmb3IgKGxldCBpIGluIHZhbGlkYXRlZEZpZWxkcykge1xuICAgICAgbGV0IG5hbWUgPSB2YWxpZGF0ZWRGaWVsZHNbaV07XG4gICAgICBsZXQgZmllbGRFcnJvcnMgPSB0aGlzLnZhbGlkYXRlRmllbGQobmFtZSwgdGhpcy5zdGF0ZVtuYW1lXSk7XG5cbiAgICAgIGlmIChmaWVsZEVycm9ycyA9PT0gbnVsbCkge1xuICAgICAgICBlcnJvcnNbbmFtZV0gPSBudWxsO1xuICAgICAgfSBlbHNlIGlmIChmaWVsZEVycm9ycykge1xuICAgICAgICBlcnJvcnNbbmFtZV0gPSBmaWVsZEVycm9ycztcbiAgICAgIH1cbiAgICB9XG5cbiAgICByZXR1cm4gZXJyb3JzO1xuICB9XG5cbiAgaXNWYWxpZCgpIHtcbiAgICBsZXQgZXJyb3JzID0gdGhpcy52YWxpZGF0ZSgpO1xuICAgIGZvciAobGV0IGZpZWxkIGluIGVycm9ycykge1xuICAgICAgaWYgKGVycm9ycy5oYXNPd25Qcm9wZXJ0eShmaWVsZCkpIHtcbiAgICAgICAgaWYgKGVycm9yc1tmaWVsZF0gIT09IG51bGwpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG5cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIHZhbGlkYXRlRmllbGQobmFtZSwgdmFsdWUpIHtcbiAgICBsZXQgZXJyb3JzID0gW107XG5cbiAgICBsZXQgdmFsaWRhdG9ycyA9IHtcbiAgICAgIHJlcXVpcmVkOiAodGhpcy5zdGF0ZS52YWxpZGF0b3JzLnJlcXVpcmVkIHx8IHRoaXMuc3RhdGUudmFsaWRhdG9ycylbbmFtZV0sXG4gICAgICBvcHRpb25hbDogKHRoaXMuc3RhdGUudmFsaWRhdG9ycy5vcHRpb25hbCB8fCB7fSlbbmFtZV1cbiAgICB9O1xuXG4gICAgbGV0IHJlcXVpcmVkRXJyb3IgPSB2YWxpZGF0ZVJlcXVpcmVkKHZhbHVlKSB8fCBmYWxzZTtcblxuICAgIGlmICh2YWxpZGF0b3JzLnJlcXVpcmVkKSB7XG4gICAgICBpZiAocmVxdWlyZWRFcnJvcikge1xuICAgICAgICBlcnJvcnMgPSBbcmVxdWlyZWRFcnJvcl07XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBmb3IgKGxldCBpIGluIHZhbGlkYXRvcnMucmVxdWlyZWQpIHtcbiAgICAgICAgICBsZXQgdmFsaWRhdGlvbkVycm9yID0gdmFsaWRhdG9ycy5yZXF1aXJlZFtpXSh2YWx1ZSk7XG4gICAgICAgICAgaWYgKHZhbGlkYXRpb25FcnJvcikge1xuICAgICAgICAgICAgZXJyb3JzLnB1c2godmFsaWRhdGlvbkVycm9yKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgcmV0dXJuIGVycm9ycy5sZW5ndGggPyBlcnJvcnMgOiBudWxsO1xuICAgIH0gZWxzZSBpZiAocmVxdWlyZWRFcnJvciA9PT0gZmFsc2UgJiYgdmFsaWRhdG9ycy5vcHRpb25hbCkge1xuICAgICAgZm9yIChsZXQgaSBpbiB2YWxpZGF0b3JzLm9wdGlvbmFsKSB7XG4gICAgICAgIGxldCB2YWxpZGF0aW9uRXJyb3IgPSB2YWxpZGF0b3JzLm9wdGlvbmFsW2ldKHZhbHVlKTtcbiAgICAgICAgaWYgKHZhbGlkYXRpb25FcnJvcikge1xuICAgICAgICAgIGVycm9ycy5wdXNoKHZhbGlkYXRpb25FcnJvcik7XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgcmV0dXJuIGVycm9ycy5sZW5ndGggPyBlcnJvcnMgOiBudWxsO1xuICAgIH1cblxuICAgIHJldHVybiBmYWxzZTsgLy8gZmFsc2UgPT09IGZpZWxkIHdhc24ndCB2YWxpZGF0ZWRcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgYmluZElucHV0ID0gKG5hbWUpID0+IHtcbiAgICByZXR1cm4gKGV2ZW50KSA9PiB7XG4gICAgICBsZXQgbmV3U3RhdGUgPSB7fTtcbiAgICAgIG5ld1N0YXRlW25hbWVdID0gZXZlbnQudGFyZ2V0LnZhbHVlO1xuXG4gICAgICBsZXQgZm9ybUVycm9ycyA9IHRoaXMuc3RhdGUuZXJyb3JzIHx8IHt9O1xuICAgICAgZm9ybUVycm9yc1tuYW1lXSA9IHRoaXMudmFsaWRhdGVGaWVsZChuYW1lLCBuZXdTdGF0ZVtuYW1lXSk7XG4gICAgICBuZXdTdGF0ZS5lcnJvcnMgPSBmb3JtRXJyb3JzO1xuXG4gICAgICB0aGlzLnNldFN0YXRlKG5ld1N0YXRlKTtcbiAgICB9XG4gIH07XG5cbiAgY2xlYW4oKSB7XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhzdWNjZXNzKSB7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgaGFuZGxlU3VibWl0ID0gKGV2ZW50KSA9PiB7XG4gICAgLy8gd2UgZG9uJ3QgcmVsb2FkIHBhZ2Ugb24gc3VibWlzc2lvbnNcbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpXG4gICAgaWYgKHRoaXMuc3RhdGUuaXNMb2FkaW5nKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgaWYgKHRoaXMuY2xlYW4oKSkge1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7J2lzTG9hZGluZyc6IHRydWV9KTtcbiAgICAgIGxldCBwcm9taXNlID0gdGhpcy5zZW5kKCk7XG5cbiAgICAgIGlmIChwcm9taXNlKSB7XG4gICAgICAgIHByb21pc2UudGhlbigoc3VjY2VzcykgPT4ge1xuICAgICAgICAgIHRoaXMuc2V0U3RhdGUoeydpc0xvYWRpbmcnOiBmYWxzZX0pO1xuICAgICAgICAgIHRoaXMuaGFuZGxlU3VjY2VzcyhzdWNjZXNzKTtcbiAgICAgICAgfSwgKHJlamVjdGlvbikgPT4ge1xuICAgICAgICAgIHRoaXMuc2V0U3RhdGUoeydpc0xvYWRpbmcnOiBmYWxzZX0pO1xuICAgICAgICAgIHRoaXMuaGFuZGxlRXJyb3IocmVqZWN0aW9uKTtcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLnNldFN0YXRlKHsnaXNMb2FkaW5nJzogZmFsc2V9KTtcbiAgICAgIH1cbiAgICB9XG4gIH07XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG59IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImxvYWRlclwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJsb2FkZXItc3Bpbm5pbmctd2hlZWxcIj48L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBMb2FkZXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvbG9hZGVyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5IG1vZGFsLWxvYWRlclwiPlxuICAgICAgPExvYWRlciAvPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgenhjdmJuIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy96eGN2Ym4nO1xuXG5leHBvcnQgY29uc3QgU1RZTEVTID0gW1xuICAncHJvZ3Jlc3MtYmFyLWRhbmdlcicsXG4gICdwcm9ncmVzcy1iYXItd2FybmluZycsXG4gICdwcm9ncmVzcy1iYXItd2FybmluZycsXG4gICdwcm9ncmVzcy1iYXItcHJpbWFyeScsXG4gICdwcm9ncmVzcy1iYXItc3VjY2Vzcydcbl07XG5cbmV4cG9ydCBjb25zdCBMQUJFTFMgPSBbXG4gIGdldHRleHQoXCJFbnRlcmVkIHBhc3N3b3JkIGlzIHZlcnkgd2Vhay5cIiksXG4gIGdldHRleHQoXCJFbnRlcmVkIHBhc3N3b3JkIGlzIHdlYWsuXCIpLFxuICBnZXR0ZXh0KFwiRW50ZXJlZCBwYXNzd29yZCBpcyBhdmVyYWdlLlwiKSxcbiAgZ2V0dGV4dChcIkVudGVyZWQgcGFzc3dvcmQgaXMgc3Ryb25nLlwiKSxcbiAgZ2V0dGV4dChcIkVudGVyZWQgcGFzc3dvcmQgaXMgdmVyeSBzdHJvbmcuXCIpXG5dO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5fc2NvcmUgPSAwO1xuICAgIHRoaXMuX3Bhc3N3b3JkID0gbnVsbDtcbiAgICB0aGlzLl9pbnB1dHMgPSBbXTtcbiAgfVxuXG4gIGdldFNjb3JlKHBhc3N3b3JkLCBpbnB1dHMpIHtcbiAgICBsZXQgY2FjaGVTdGFsZSA9IGZhbHNlO1xuXG4gICAgaWYgKHBhc3N3b3JkLnRyaW0oKSAhPT0gdGhpcy5fcGFzc3dvcmQpIHtcbiAgICAgIGNhY2hlU3RhbGUgPSB0cnVlO1xuICAgIH1cblxuICAgIGlmIChpbnB1dHMubGVuZ3RoICE9PSB0aGlzLl9pbnB1dHMubGVuZ3RoKSB7XG4gICAgICBjYWNoZVN0YWxlID0gdHJ1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgaW5wdXRzLm1hcCgodmFsdWUsIGkpID0+IHtcbiAgICAgICAgaWYgKHZhbHVlLnRyaW0oKSAhPT0gdGhpcy5faW5wdXRzW2ldKSB7XG4gICAgICAgICAgY2FjaGVTdGFsZSA9IHRydWU7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGlmIChjYWNoZVN0YWxlKSB7XG4gICAgICB0aGlzLl9zY29yZSA9IHp4Y3Zibi5zY29yZVBhc3N3b3JkKHBhc3N3b3JkLCBpbnB1dHMpO1xuICAgICAgdGhpcy5fcGFzc3dvcmQgPSBwYXNzd29yZC50cmltKCk7XG4gICAgICB0aGlzLl9pbnB1dHMgPSBpbnB1dHMubWFwKGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgICAgIHJldHVybiB2YWx1ZS50cmltKCk7XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICByZXR1cm4gdGhpcy5fc2NvcmU7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGxldCBzY29yZSA9IHRoaXMuZ2V0U2NvcmUodGhpcy5wcm9wcy5wYXNzd29yZCwgdGhpcy5wcm9wcy5pbnB1dHMpO1xuXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiaGVscC1ibG9jayBwYXNzd29yZC1zdHJlbmd0aFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJwcm9ncmVzc1wiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT17XCJwcm9ncmVzcy1iYXIgXCIgKyBTVFlMRVNbc2NvcmVdfVxuICAgICAgICAgICAgIHN0eWxlPXt7d2lkdGg6ICgyMCArICgyMCAqIHNjb3JlKSkgKyAnJSd9fVxuICAgICAgICAgICAgIHJvbGU9XCJwcm9ncmVzcy1iYXJcIlxuICAgICAgICAgICAgIGFyaWEtdmFsdWVub3c9e3Njb3JlfVxuICAgICAgICAgICAgIGFyaWEtdmFsdWVtaW49XCIwXCJcbiAgICAgICAgICAgICBhcmlhLXZhbHVlbWF4PVwiNFwiPlxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInNyLW9ubHlcIj5cbiAgICAgICAgICAgIHtMQUJFTFNbc2NvcmVdfVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxwIGNsYXNzTmFtZT1cInRleHQtc21hbGxcIj5cbiAgICAgICAge0xBQkVMU1tzY29yZV19XG4gICAgICA8L3A+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IExvYWRlciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9sb2FkZXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWdpc3Rlck1vZGFsIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3JlZ2lzdGVyLmpzJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgY2FwdGNoYSBmcm9tICdtaXNhZ28vc2VydmljZXMvY2FwdGNoYSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1vZGFsIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2RhbCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHp4Y3ZibiBmcm9tICdtaXNhZ28vc2VydmljZXMvenhjdmJuJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuICAgICAgJ2lzTG9hZGVkJzogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBzaG93UmVnaXN0ZXJNb2RhbCA9ICgpID0+IHtcbiAgICBpZiAobWlzYWdvLmdldCgnU0VUVElOR1MnKS5hY2NvdW50X2FjdGl2YXRpb24gPT09ICdjbG9zZWQnKSB7XG4gICAgICBzbmFja2Jhci5pbmZvKGdldHRleHQoXCJOZXcgcmVnaXN0cmF0aW9ucyBhcmUgY3VycmVudGx5IGRpc2FibGVkLlwiKSk7XG4gICAgfSBlbHNlIGlmICh0aGlzLnN0YXRlLmlzTG9hZGVkKSB7XG4gICAgICBtb2RhbC5zaG93KFJlZ2lzdGVyTW9kYWwpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgJ2lzTG9hZGluZyc6IHRydWVcbiAgICAgIH0pO1xuXG4gICAgICBQcm9taXNlLmFsbChbXG4gICAgICAgIGNhcHRjaGEubG9hZCgpLFxuICAgICAgICB6eGN2Ym4ubG9hZCgpXG4gICAgICBdKS50aGVuKCgpID0+IHtcbiAgICAgICAgaWYgKCF0aGlzLnN0YXRlLmlzTG9hZGVkKSB7XG4gICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG4gICAgICAgICAgICAnaXNMb2FkZWQnOiBmYWxzZVxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG5cbiAgICAgICAgbW9kYWwuc2hvdyhSZWdpc3Rlck1vZGFsKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICBnZXRDbGFzc05hbWUoKSB7XG4gICAgcmV0dXJuIHRoaXMucHJvcHMuY2xhc3NOYW1lICsgKHRoaXMuc3RhdGUuaXNMb2FkaW5nID8gJyBidG4tbG9hZGluZycgOiAnJyk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBvbkNsaWNrPXt0aGlzLnNob3dSZWdpc3Rlck1vZGFsfVxuICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17J2J0biAnICsgdGhpcy5nZXRDbGFzc05hbWUoKX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRlZH0+XG4gICAgICB7Z2V0dGV4dChcIlJlZ2lzdGVyXCIpfVxuICAgICAge3RoaXMuc3RhdGUuaXNMb2FkaW5nID8gPExvYWRlciAvPiA6IG51bGwgfVxuICAgIDwvYnV0dG9uPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IEZvcm1Hcm91cCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtLWdyb3VwJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgUGFzc3dvcmRTdHJlbmd0aCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9wYXNzd29yZC1zdHJlbmd0aCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IGF1dGggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2F1dGgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBjYXB0Y2hhIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9jYXB0Y2hhJztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcbmltcG9ydCAqIGFzIHZhbGlkYXRvcnMgZnJvbSAnbWlzYWdvL3V0aWxzL3ZhbGlkYXRvcnMnO1xuXG5leHBvcnQgY2xhc3MgUmVnaXN0ZXJGb3JtIGV4dGVuZHMgRm9ybSB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICdpc0xvYWRpbmcnOiBmYWxzZSxcblxuICAgICAgJ3VzZXJuYW1lJzogJycsXG4gICAgICAnZW1haWwnOiAnJyxcbiAgICAgICdwYXNzd29yZCc6ICcnLFxuICAgICAgJ2NhcHRjaGEnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICd1c2VybmFtZSc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnVzZXJuYW1lQ29udGVudCgpLFxuICAgICAgICAgIHZhbGlkYXRvcnMudXNlcm5hbWVNaW5MZW5ndGgobWlzYWdvLmdldCgnU0VUVElOR1MnKSksXG4gICAgICAgICAgdmFsaWRhdG9ycy51c2VybmFtZU1heExlbmd0aChtaXNhZ28uZ2V0KCdTRVRUSU5HUycpKVxuICAgICAgICBdLFxuICAgICAgICAnZW1haWwnOiBbXG4gICAgICAgICAgdmFsaWRhdG9ycy5lbWFpbCgpXG4gICAgICAgIF0sXG4gICAgICAgICdwYXNzd29yZCc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnBhc3N3b3JkTWluTGVuZ3RoKG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykpXG4gICAgICAgIF0sXG4gICAgICAgICdjYXB0Y2hhJzogY2FwdGNoYS52YWxpZGF0b3IoKVxuICAgICAgfSxcblxuICAgICAgJ2Vycm9ycyc6IHt9XG4gICAgfTtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWQoKSkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJGb3JtIGNvbnRhaW5zIGVycm9ycy5cIikpO1xuICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICdlcnJvcnMnOiB0aGlzLnZhbGlkYXRlKClcbiAgICAgIH0pO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdChtaXNhZ28uZ2V0KCdVU0VSU19BUEknKSwge1xuICAgICAgJ3VzZXJuYW1lJzogdGhpcy5zdGF0ZS51c2VybmFtZSxcbiAgICAgICdlbWFpbCc6IHRoaXMuc3RhdGUuZW1haWwsXG4gICAgICAncGFzc3dvcmQnOiB0aGlzLnN0YXRlLnBhc3N3b3JkLFxuICAgICAgJ2NhcHRjaGEnOiB0aGlzLnN0YXRlLmNhcHRjaGFcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3MoYXBpUmVzcG9uc2UpIHtcbiAgICB0aGlzLnByb3BzLmNhbGxiYWNrKGFwaVJlc3BvbnNlKTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnZXJyb3JzJzogT2JqZWN0LmFzc2lnbih7fSwgdGhpcy5zdGF0ZS5lcnJvcnMsIHJlamVjdGlvbilcbiAgICAgIH0pO1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZvcm0gY29udGFpbnMgZXJyb3JzLlwiKSk7XG4gICAgfSBlbHNlIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDMgJiYgcmVqZWN0aW9uLmJhbikge1xuICAgICAgc2hvd0Jhbm5lZFBhZ2UocmVqZWN0aW9uLmJhbik7XG4gICAgICBtb2RhbC5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmFwaUVycm9yKHJlamVjdGlvbik7XG4gICAgfVxuICB9XG5cbiAgZ2V0TGVnYWxGb290Tm90ZSgpIHtcbiAgICBpZiAobWlzYWdvLmdldCgnVEVSTVNfT0ZfU0VSVklDRV9VUkwnKSkge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxhIGhyZWY9e21pc2Fnby5nZXQoJ1RFUk1TX09GX1NFUlZJQ0VfVVJMJyl9XG4gICAgICAgICAgICAgICAgdGFyZ2V0PVwiX2JsYW5rXCI+XG4gICAgICAgIHtnZXR0ZXh0KFwiQnkgcmVnaXN0ZXJpbmcgeW91IGFncmVlIHRvIHNpdGUncyB0ZXJtcyBhbmQgY29uZGl0aW9ucy5cIil9XG4gICAgICA8L2E+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1kaWFsb2cgbW9kYWwtcmVnaXN0ZXJcIiByb2xlPVwiZG9jdW1lbnRcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtY29udGVudFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWhlYWRlclwiPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImNsb3NlXCIgZGF0YS1kaXNtaXNzPVwibW9kYWxcIlxuICAgICAgICAgICAgICAgICAgYXJpYS1sYWJlbD17Z2V0dGV4dChcIkNsb3NlXCIpfT5cbiAgICAgICAgICAgIDxzcGFuIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPiZ0aW1lczs8L3NwYW4+XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgPGg0IGNsYXNzTmFtZT1cIm1vZGFsLXRpdGxlXCI+e2dldHRleHQoXCJSZWdpc3RlclwiKX08L2g0PlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fSBjbGFzc05hbWU9XCJmb3JtLWhvcml6b250YWxcIj5cbiAgICAgICAgICA8aW5wdXQgdHlwZT1cInR5cGVcIiBzdHlsZT17e2Rpc3BsYXk6ICdub25lJ319IC8+XG4gICAgICAgICAgPGlucHV0IHR5cGU9XCJwYXNzd29yZFwiIHN0eWxlPXt7ZGlzcGxheTogJ25vbmUnfX0gLz5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHlcIj5cblxuICAgICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIlVzZXJuYW1lXCIpfSBmb3I9XCJpZF91c2VybmFtZVwiXG4gICAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9XCJjb2wtc20tNFwiIGNvbnRyb2xDbGFzcz1cImNvbC1zbS04XCJcbiAgICAgICAgICAgICAgICAgICAgICAgdmFsaWRhdGlvbj17dGhpcy5zdGF0ZS5lcnJvcnMudXNlcm5hbWV9PlxuICAgICAgICAgICAgICA8aW5wdXQgdHlwZT1cInRleHRcIiBpZD1cImlkX3VzZXJuYW1lXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICAgIGFyaWEtZGVzY3JpYmVkYnk9XCJpZF91c2VybmFtZV9zdGF0dXNcIlxuICAgICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCd1c2VybmFtZScpfVxuICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUudXNlcm5hbWV9IC8+XG4gICAgICAgICAgICA8L0Zvcm1Hcm91cD5cblxuICAgICAgICAgICAgPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIkUtbWFpbFwiKX0gZm9yPVwiaWRfZW1haWxcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiXG4gICAgICAgICAgICAgICAgICAgICAgIHZhbGlkYXRpb249e3RoaXMuc3RhdGUuZXJyb3JzLmVtYWlsfT5cbiAgICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgaWQ9XCJpZF9lbWFpbFwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgICBhcmlhLWRlc2NyaWJlZGJ5PVwiaWRfZW1haWxfc3RhdHVzXCJcbiAgICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnZW1haWwnKX1cbiAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLmVtYWlsfSAvPlxuICAgICAgICAgICAgPC9Gb3JtR3JvdXA+XG5cbiAgICAgICAgICAgIDxGb3JtR3JvdXAgbGFiZWw9e2dldHRleHQoXCJQYXNzd29yZFwiKX0gZm9yPVwiaWRfcGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPVwiY29sLXNtLTRcIiBjb250cm9sQ2xhc3M9XCJjb2wtc20tOFwiXG4gICAgICAgICAgICAgICAgICAgICAgIHZhbGlkYXRpb249e3RoaXMuc3RhdGUuZXJyb3JzLnBhc3N3b3JkfVxuICAgICAgICAgICAgICAgICAgICAgICBleHRyYT17PFBhc3N3b3JkU3RyZW5ndGggcGFzc3dvcmQ9e3RoaXMuc3RhdGUucGFzc3dvcmR9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnB1dHM9e1tcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zdGF0ZS51c2VybmFtZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zdGF0ZS5lbWFpbFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgXX0gLz59ID5cbiAgICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJwYXNzd29yZFwiIGlkPVwiaWRfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgICAgYXJpYS1kZXNjcmliZWRieT1cImlkX3Bhc3N3b3JkX3N0YXR1c1wiXG4gICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3Bhc3N3b3JkJyl9XG4gICAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5wYXNzd29yZH0gLz5cbiAgICAgICAgICAgIDwvRm9ybUdyb3VwPlxuXG4gICAgICAgICAgICB7Y2FwdGNoYS5jb21wb25lbnQoe1xuICAgICAgICAgICAgICBmb3JtOiB0aGlzLFxuICAgICAgICAgICAgICBsYWJlbENsYXNzOiBcImNvbC1zbS00XCIsXG4gICAgICAgICAgICAgIGNvbnRyb2xDbGFzczogXCJjb2wtc20tOFwiXG4gICAgICAgICAgICB9KX1cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtZm9vdGVyXCI+XG4gICAgICAgICAgICB7dGhpcy5nZXRMZWdhbEZvb3ROb3RlKCl9XG4gICAgICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5XCIgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9PlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIlJlZ2lzdGVyIGFjY291bnRcIil9XG4gICAgICAgICAgICA8L0J1dHRvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9mb3JtPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFJlZ2lzdGVyQ29tcGxldGUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRMZWFkKCkge1xuICAgIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICd1c2VyJykge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCIlKHVzZXJuYW1lKXMsIHlvdXIgYWNjb3VudCBoYXMgYmVlbiBjcmVhdGVkIGJ1dCB5b3UgbmVlZCB0byBhY3RpdmF0ZSBpdCBiZWZvcmUgeW91IHdpbGwgYmUgYWJsZSB0byBzaWduIGluLlwiKTtcbiAgICB9IGVsc2UgaWYgKHRoaXMucHJvcHMuYWN0aXZhdGlvbiA9PT0gJ2FkbWluJykge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCIlKHVzZXJuYW1lKXMsIHlvdXIgYWNjb3VudCBoYXMgYmVlbiBjcmVhdGVkIGJ1dCBib2FyZCBhZG1pbmlzdHJhdG9yIHdpbGwgaGF2ZSB0byBhY3RpdmF0ZSBpdCBiZWZvcmUgeW91IHdpbGwgYmUgYWJsZSB0byBzaWduIGluLlwiKTtcbiAgICB9XG4gIH1cblxuICBnZXRTdWJzY3JpcHQoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuYWN0aXZhdGlvbiA9PT0gJ3VzZXInKSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIldlIGhhdmUgc2VudCBhbiBlLW1haWwgdG8gJShlbWFpbClzIHdpdGggbGluayB0aGF0IHlvdSBoYXZlIHRvIGNsaWNrIHRvIGFjdGl2YXRlIHlvdXIgYWNjb3VudC5cIik7XG4gICAgfSBlbHNlIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICdhZG1pbicpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiV2Ugd2lsbCBzZW5kIGFuIGUtbWFpbCB0byAlKGVtYWlsKXMgd2hlbiB0aGlzIHRha2VzIHBsYWNlLlwiKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWRpYWxvZyBtb2RhbC1tZXNzYWdlIG1vZGFsLXJlZ2lzdGVyXCJcbiAgICAgICAgICAgICAgICByb2xlPVwiZG9jdW1lbnRcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtY29udGVudFwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWhlYWRlclwiPlxuICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImNsb3NlXCIgZGF0YS1kaXNtaXNzPVwibW9kYWxcIlxuICAgICAgICAgICAgICAgICAgYXJpYS1sYWJlbD17Z2V0dGV4dChcIkNsb3NlXCIpfT5cbiAgICAgICAgICAgIDxzcGFuIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPiZ0aW1lczs8L3NwYW4+XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgPGg0IGNsYXNzTmFtZT1cIm1vZGFsLXRpdGxlXCI+e2dldHRleHQoXCJSZWdpc3RyYXRpb24gY29tcGxldGVcIil9PC9oND5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtYm9keVwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgIGluZm9fb3V0bGluZVxuICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1ib2R5XCI+XG4gICAgICAgICAgICA8cCBjbGFzc05hbWU9XCJsZWFkXCI+XG4gICAgICAgICAgICAgIHtpbnRlcnBvbGF0ZShcbiAgICAgICAgICAgICAgICB0aGlzLmdldExlYWQoKSxcbiAgICAgICAgICAgICAgICB7J3VzZXJuYW1lJzogdGhpcy5wcm9wcy51c2VybmFtZX0sIHRydWUpfVxuICAgICAgICAgICAgPC9wPlxuICAgICAgICAgICAgPHA+XG4gICAgICAgICAgICAgIHtpbnRlcnBvbGF0ZShcbiAgICAgICAgICAgICAgICB0aGlzLmdldFN1YnNjcmlwdCgpLFxuICAgICAgICAgICAgICAgIHsnZW1haWwnOiB0aGlzLnByb3BzLmVtYWlsfSwgdHJ1ZSl9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnY29tcGxldGUnOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBsZXRlUmVnaXN0cmF0aW9uID0gKGFwaVJlc3BvbnNlKSA9PiB7XG4gICAgaWYgKGFwaVJlc3BvbnNlLmFjdGl2YXRpb24gPT09ICdhY3RpdmUnKSB7XG4gICAgICBtb2RhbC5oaWRlKCk7XG4gICAgICBhdXRoLnNpZ25JbihhcGlSZXNwb25zZSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAnY29tcGxldGUnOiBhcGlSZXNwb25zZVxuICAgICAgfSk7XG4gICAgfVxuICB9O1xuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgaWYgKHRoaXMuc3RhdGUuY29tcGxldGUpIHtcbiAgICAgIHJldHVybiA8UmVnaXN0ZXJDb21wbGV0ZSBhY3RpdmF0aW9uPXt0aGlzLnN0YXRlLmNvbXBsZXRlLmFjdGl2YXRpb259XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdXNlcm5hbWU9e3RoaXMuc3RhdGUuY29tcGxldGUudXNlcm5hbWV9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZW1haWw9e3RoaXMuc3RhdGUuY29tcGxldGUuZW1haWx9IC8+O1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gPFJlZ2lzdGVyRm9ybSBjYWxsYmFjaz17dGhpcy5jb21wbGV0ZVJlZ2lzdHJhdGlvbn0vPjtcbiAgICB9XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgQnV0dG9uIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2J1dHRvbic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEZvcm0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvZm9ybSc7XG5pbXBvcnQgYWpheCBmcm9tICdtaXNhZ28vc2VydmljZXMvYWpheCc7XG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJztcbmltcG9ydCAqIGFzIHZhbGlkYXRvcnMgZnJvbSAnbWlzYWdvL3V0aWxzL3ZhbGlkYXRvcnMnO1xuaW1wb3J0IHNob3dCYW5uZWRQYWdlIGZyb20gJ21pc2Fnby91dGlscy9iYW5uZWQtcGFnZSc7XG5cbmV4cG9ydCBjbGFzcyBSZXF1ZXN0TGlua0Zvcm0gZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuXG4gICAgICAnZW1haWwnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICdlbWFpbCc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLmVtYWlsKClcbiAgICAgICAgXVxuICAgICAgfVxuICAgIH07XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICBpZiAodGhpcy5pc1ZhbGlkKCkpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRW50ZXIgYSB2YWxpZCBlbWFpbCBhZGRyZXNzLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KG1pc2Fnby5nZXQoJ1NFTkRfQUNUSVZBVElPTl9BUEknKSwge1xuICAgICAgJ2VtYWlsJzogdGhpcy5zdGF0ZS5lbWFpbFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhhcGlSZXNwb25zZSkge1xuICAgIHRoaXMucHJvcHMuY2FsbGJhY2soYXBpUmVzcG9uc2UpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKFsnYWxyZWFkeV9hY3RpdmUnLCAnaW5hY3RpdmVfYWRtaW4nXS5pbmRleE9mKHJlamVjdGlvbi5jb2RlKSA+IC0xKSB7XG4gICAgICBzbmFja2Jhci5pbmZvKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgIH0gZWxzZSBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAzICYmIHJlamVjdGlvbi5iYW4pIHtcbiAgICAgIHNob3dCYW5uZWRQYWdlKHJlamVjdGlvbi5iYW4pO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwid2VsbCB3ZWxsLWZvcm0gd2VsbC1mb3JtLXJlcXVlc3QtYWN0aXZhdGlvbi1saW5rXCI+XG4gICAgICA8Zm9ybSBvblN1Ym1pdD17dGhpcy5oYW5kbGVTdWJtaXR9PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXBcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRyb2wtaW5wdXRcIj5cblxuICAgICAgICAgICAgPGlucHV0IHR5cGU9XCJ0ZXh0XCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICBwbGFjZWhvbGRlcj17Z2V0dGV4dChcIllvdXIgZS1tYWlsIGFkZHJlc3NcIil9XG4gICAgICAgICAgICAgICAgICAgZGlzYWJsZWQ9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgnZW1haWwnKX1cbiAgICAgICAgICAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS5lbWFpbH0gLz5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cblxuICAgICAgICA8QnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgbG9hZGluZz17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiU2VuZCBsaW5rXCIpfVxuICAgICAgICA8L0J1dHRvbj5cblxuICAgICAgPC9mb3JtPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBMaW5rU2VudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldE1lc3NhZ2UoKSB7XG4gICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCJBY3RpdmF0aW9uIGxpbmsgd2FzIHNlbnQgdG8gJShlbWFpbClzXCIpLCB7XG4gICAgICBlbWFpbDogdGhpcy5wcm9wcy51c2VyLmVtYWlsXG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXF1ZXN0LWFjdGl2YXRpb24tbGluayB3ZWxsLWRvbmVcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZG9uZS1tZXNzYWdlXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPlxuICAgICAgICAgICAgY2hlY2tcbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgIDxwPlxuICAgICAgICAgICAge3RoaXMuZ2V0TWVzc2FnZSgpfVxuICAgICAgICAgIDwvcD5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMucHJvcHMuY2FsbGJhY2t9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiUmVxdWVzdCBhbm90aGVyIGxpbmtcIil9XG4gICAgICAgIDwvYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICBjb21wbGV0ZTogZmFsc2VcbiAgICB9O1xuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBjb21wbGV0ZSA9IChhcGlSZXNwb25zZSkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgY29tcGxldGU6IGFwaVJlc3BvbnNlXG4gICAgfSk7XG4gIH07XG5cbiAgcmVzZXQgPSAoKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBjb21wbGV0ZTogZmFsc2VcbiAgICB9KTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGlmICh0aGlzLnN0YXRlLmNvbXBsZXRlKSB7XG4gICAgICByZXR1cm4gPExpbmtTZW50IHVzZXI9e3RoaXMuc3RhdGUuY29tcGxldGV9IGNhbGxiYWNrPXt0aGlzLnJlc2V0fSAvPjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIDxSZXF1ZXN0TGlua0Zvcm0gY2FsbGJhY2s9e3RoaXMuY29tcGxldGV9IC8+O1xuICAgIH07XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgKiBhcyB2YWxpZGF0b3JzIGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcbmltcG9ydCBzaG93QmFubmVkUGFnZSBmcm9tICdtaXNhZ28vdXRpbHMvYmFubmVkLXBhZ2UnO1xuXG5leHBvcnQgY2xhc3MgUmVxdWVzdFJlc2V0Rm9ybSBleHRlbmRzIEZvcm0ge1xuICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcblxuICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAnaXNMb2FkaW5nJzogZmFsc2UsXG5cbiAgICAgICdlbWFpbCc6ICcnLFxuXG4gICAgICAndmFsaWRhdG9ycyc6IHtcbiAgICAgICAgJ2VtYWlsJzogW1xuICAgICAgICAgIHZhbGlkYXRvcnMuZW1haWwoKVxuICAgICAgICBdXG4gICAgICB9XG4gICAgfTtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGlmICh0aGlzLmlzVmFsaWQoKSkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJFbnRlciBhIHZhbGlkIGVtYWlsIGFkZHJlc3MuXCIpKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBhamF4LnBvc3QobWlzYWdvLmdldCgnU0VORF9QQVNTV09SRF9SRVNFVF9BUEknKSwge1xuICAgICAgJ2VtYWlsJzogdGhpcy5zdGF0ZS5lbWFpbFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhhcGlSZXNwb25zZSkge1xuICAgIHRoaXMucHJvcHMuY2FsbGJhY2soYXBpUmVzcG9uc2UpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKFsnaW5hY3RpdmVfdXNlcicsICdpbmFjdGl2ZV9hZG1pbiddLmluZGV4T2YocmVqZWN0aW9uLmNvZGUpID4gLTEpIHtcbiAgICAgIHRoaXMucHJvcHMuc2hvd0luYWN0aXZlUGFnZShyZWplY3Rpb24pO1xuICAgIH0gZWxzZSBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAzICYmIHJlamVjdGlvbi5iYW4pIHtcbiAgICAgIHNob3dCYW5uZWRQYWdlKHJlamVjdGlvbi5iYW4pO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2Jhci5hcGlFcnJvcihyZWplY3Rpb24pO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwid2VsbCB3ZWxsLWZvcm0gd2VsbC1mb3JtLXJlcXVlc3QtcGFzc3dvcmQtcmVzZXRcIj5cbiAgICAgIDxmb3JtIG9uU3VibWl0PXt0aGlzLmhhbmRsZVN1Ym1pdH0+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZm9ybS1ncm91cFwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udHJvbC1pbnB1dFwiPlxuXG4gICAgICAgICAgICA8aW5wdXQgdHlwZT1cInRleHRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiWW91ciBlLW1haWwgYWRkcmVzc1wiKX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuYmluZElucHV0KCdlbWFpbCcpfVxuICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLmVtYWlsfSAvPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuXG4gICAgICAgIDxCdXR0b24gY2xhc3NOYW1lPVwiYnRuLXByaW1hcnkgYnRuLWJsb2NrXCJcbiAgICAgICAgICAgICAgICBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAge2dldHRleHQoXCJTZW5kIGxpbmtcIil9XG4gICAgICAgIDwvQnV0dG9uPlxuXG4gICAgICA8L2Zvcm0+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIExpbmtTZW50IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0TWVzc2FnZSgpIHtcbiAgICByZXR1cm4gaW50ZXJwb2xhdGUoZ2V0dGV4dChcIlJlc2V0IHBhc3N3b3JkIGxpbmsgd2FzIHNlbnQgdG8gJShlbWFpbClzXCIpLCB7XG4gICAgICBlbWFpbDogdGhpcy5wcm9wcy51c2VyLmVtYWlsXG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXF1ZXN0LXBhc3N3b3JkLXJlc2V0IHdlbGwtZG9uZVwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJkb25lLW1lc3NhZ2VcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWljb25cIj5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICBjaGVja1xuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1ib2R5XCI+XG4gICAgICAgICAgPHA+XG4gICAgICAgICAgICB7dGhpcy5nZXRNZXNzYWdlKCl9XG4gICAgICAgICAgPC9wPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIGJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5wcm9wcy5jYWxsYmFja30+XG4gICAgICAgICAge2dldHRleHQoXCJSZXF1ZXN0IGFub3RoZXIgbGlua1wiKX1cbiAgICAgICAgPC9idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgQWNjb3VudEluYWN0aXZlUGFnZSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldEFjdGl2YXRlQnV0dG9uKCkge1xuICAgIGlmICh0aGlzLnByb3BzLmFjdGl2YXRpb24gPT09ICdpbmFjdGl2ZV91c2VyJykge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxwPlxuICAgICAgICA8YSBocmVmPXttaXNhZ28uZ2V0KCdSRVFVRVNUX0FDVElWQVRJT05fVVJMJyl9PlxuICAgICAgICAgIHtnZXR0ZXh0KFwiQWN0aXZhdGUgeW91ciBhY2NvdW50LlwiKX1cbiAgICAgICAgPC9hPlxuICAgICAgPC9wPjtcbiAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwicGFnZSBwYWdlLW1lc3NhZ2UgcGFnZS1tZXNzYWdlLWluZm8gcGFnZS1mb3Jnb3R0ZW4tcGFzc3dvcmQtaW5hY3RpdmVcIj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udGFpbmVyXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1wYW5lbFwiPlxuXG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtZXNzYWdlLWljb25cIj5cbiAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cIm1hdGVyaWFsLWljb25cIj5cbiAgICAgICAgICAgICAgaW5mb19vdXRsaW5lXG4gICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIllvdXIgYWNjb3VudCBpcyBpbmFjdGl2ZS5cIil9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgICA8cD5cbiAgICAgICAgICAgICAge3RoaXMucHJvcHMubWVzc2FnZX1cbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICAgIHt0aGlzLmdldEFjdGl2YXRlQnV0dG9uKCl9XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuXG4gICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgIGNvbXBsZXRlOiBmYWxzZVxuICAgIH07XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBsZXRlID0gKGFwaVJlc3BvbnNlKSA9PiB7XG4gICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICBjb21wbGV0ZTogYXBpUmVzcG9uc2VcbiAgICB9KTtcbiAgfTtcblxuICByZXNldCA9ICgpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgIGNvbXBsZXRlOiBmYWxzZVxuICAgIH0pO1xuICB9O1xuXG4gIHNob3dJbmFjdGl2ZVBhZ2UoYXBpUmVzcG9uc2UpIHtcbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICA8QWNjb3VudEluYWN0aXZlUGFnZSBhY3RpdmF0aW9uPXthcGlSZXNwb25zZS5jb2RlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZT17YXBpUmVzcG9uc2UuZGV0YWlsfSAvPixcbiAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdwYWdlLW1vdW50JylcbiAgICApO1xuICB9XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBpZiAodGhpcy5zdGF0ZS5jb21wbGV0ZSkge1xuICAgICAgcmV0dXJuIDxMaW5rU2VudCB1c2VyPXt0aGlzLnN0YXRlLmNvbXBsZXRlfSBjYWxsYmFjaz17dGhpcy5yZXNldH0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8UmVxdWVzdFJlc2V0Rm9ybSBjYWxsYmFjaz17dGhpcy5jb21wbGV0ZX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzaG93SW5hY3RpdmVQYWdlPXt0aGlzLnNob3dJbmFjdGl2ZVBhZ2V9IC8+O1xuICAgIH07XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBGb3JtIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2Zvcm0nO1xuaW1wb3J0IFNpZ25Jbk1vZGFsIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3NpZ24taW4uanMnO1xuaW1wb3J0IGFqYXggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2FqYXgnO1xuaW1wb3J0IGF1dGggZnJvbSAnbWlzYWdvL3NlcnZpY2VzL2F1dGgnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgKiBhcyB2YWxpZGF0b3JzIGZyb20gJ21pc2Fnby91dGlscy92YWxpZGF0b3JzJztcbmltcG9ydCBzaG93QmFubmVkUGFnZSBmcm9tICdtaXNhZ28vdXRpbHMvYmFubmVkLXBhZ2UnO1xuXG5leHBvcnQgY2xhc3MgUmVzZXRQYXNzd29yZEZvcm0gZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuXG4gICAgICAncGFzc3dvcmQnOiAnJyxcblxuICAgICAgJ3ZhbGlkYXRvcnMnOiB7XG4gICAgICAgICdwYXNzd29yZCc6IFtcbiAgICAgICAgICB2YWxpZGF0b3JzLnBhc3N3b3JkTWluTGVuZ3RoKG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykpXG4gICAgICAgIF1cbiAgICAgIH1cbiAgICB9O1xuICB9XG5cbiAgY2xlYW4oKSB7XG4gICAgaWYgKHRoaXMuaXNWYWxpZCgpKSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgaWYgKHRoaXMuc3RhdGUucGFzc3dvcmQudHJpbSgpLmxlbmd0aCkge1xuICAgICAgICBzbmFja2Jhci5lcnJvcih0aGlzLnN0YXRlLmVycm9ycy5wYXNzd29yZFswXSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRW50ZXIgbmV3IHBhc3N3b3JkLlwiKSk7XG4gICAgICB9XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgc2VuZCgpIHtcbiAgICByZXR1cm4gYWpheC5wb3N0KG1pc2Fnby5nZXQoJ0NIQU5HRV9QQVNTV09SRF9BUEknKSwge1xuICAgICAgJ3Bhc3N3b3JkJzogdGhpcy5zdGF0ZS5wYXNzd29yZFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcyhhcGlSZXNwb25zZSkge1xuICAgIHRoaXMucHJvcHMuY2FsbGJhY2soYXBpUmVzcG9uc2UpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMyAmJiByZWplY3Rpb24uYmFuKSB7XG4gICAgICBzaG93QmFubmVkUGFnZShyZWplY3Rpb24uYmFuKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIndlbGwgd2VsbC1mb3JtIHdlbGwtZm9ybS1yZXNldC1wYXNzd29yZFwiPlxuICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fT5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJmb3JtLWdyb3VwXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250cm9sLWlucHV0XCI+XG5cbiAgICAgICAgICAgIDxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiRW50ZXIgbmV3IHBhc3N3b3JkXCIpfVxuICAgICAgICAgICAgICAgICAgIGRpc2FibGVkPXt0aGlzLnN0YXRlLmlzTG9hZGluZ31cbiAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3Bhc3N3b3JkJyl9XG4gICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUucGFzc3dvcmR9IC8+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgIGxvYWRpbmc9e3RoaXMuc3RhdGUuaXNMb2FkaW5nfT5cbiAgICAgICAgICB7Z2V0dGV4dChcIkNoYW5nZSBwYXNzd29yZFwiKX1cbiAgICAgICAgPC9CdXR0b24+XG5cbiAgICAgIDwvZm9ybT5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgUGFzc3dvcmRDaGFuZ2VkUGFnZSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIGdldE1lc3NhZ2UoKSB7XG4gICAgcmV0dXJuIGludGVycG9sYXRlKGdldHRleHQoXCIlKHVzZXJuYW1lKXMsIHlvdXIgcGFzc3dvcmQgaGFzIGJlZW4gY2hhbmdlZCBzdWNjZXNzZnVsbHkuXCIpLCB7XG4gICAgICB1c2VybmFtZTogdGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lXG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxuICBzaG93U2lnbkluKCkge1xuICAgIG1vZGFsLnNob3coU2lnbkluTW9kYWwpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJwYWdlIHBhZ2UtbWVzc2FnZSBwYWdlLW1lc3NhZ2Utc3VjY2VzcyBwYWdlLWZvcmdvdHRlbi1wYXNzd29yZC1jaGFuZ2VkXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtcGFuZWxcIj5cblxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+XG4gICAgICAgICAgICAgIGNoZWNrXG4gICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgICAgPHAgY2xhc3NOYW1lPVwibGVhZFwiPlxuICAgICAgICAgICAgICB7dGhpcy5nZXRNZXNzYWdlKCl9XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgICA8cD5cbiAgICAgICAgICAgICAge2dldHRleHQoXCJZb3Ugd2lsbCBoYXZlIHRvIHNpZ24gaW4gdXNpbmcgbmV3IHBhc3N3b3JkIGJlZm9yZSBjb250aW51aW5nLlwiKX1cbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICAgIDxwPlxuICAgICAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLXByaW1hcnlcIiBvbkNsaWNrPXt0aGlzLnNob3dTaWduSW59PlxuICAgICAgICAgICAgICAgIHtnZXR0ZXh0KFwiU2lnbiBpblwiKX1cbiAgICAgICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgY29tcGxldGUgPSAoYXBpUmVzcG9uc2UpID0+IHtcbiAgICBhdXRoLnNvZnRTaWduT3V0KCk7XG5cbiAgICAvLyBudWtlIFwicmVkaXJlY3RfdG9cIiBmaWVsZCBzbyB3ZSBkb24ndCBlbmRcbiAgICAvLyBjb21pbmcgYmFjayB0byBlcnJvciBwYWdlIGFmdGVyIHNpZ24gaW5cbiAgICAkKCcjaGlkZGVuLWxvZ2luLWZvcm0gaW5wdXRbbmFtZT1cInJlZGlyZWN0X3RvXCJdJykucmVtb3ZlKCk7XG5cbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICA8UGFzc3dvcmRDaGFuZ2VkUGFnZSB1c2VyPXthcGlSZXNwb25zZX0gLz4sXG4gICAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncGFnZS1tb3VudCcpXG4gICAgKTtcbiAgfTtcbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8UmVzZXRQYXNzd29yZEZvcm0gY2FsbGJhY2s9e3RoaXMuY29tcGxldGV9IC8+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuICAgICAgJ3Nob3dBY3RpdmF0aW9uJzogZmFsc2UsXG5cbiAgICAgICd1c2VybmFtZSc6ICcnLFxuICAgICAgJ3Bhc3N3b3JkJzogJycsXG5cbiAgICAgICd2YWxpZGF0b3JzJzoge1xuICAgICAgICAndXNlcm5hbWUnOiBbXSxcbiAgICAgICAgJ3Bhc3N3b3JkJzogW11cbiAgICAgIH1cbiAgICB9O1xuICB9XG5cbiAgY2xlYW4oKSB7XG4gICAgaWYgKCF0aGlzLmlzVmFsaWQoKSkge1xuICAgICAgc25hY2tiYXIuZXJyb3IoZ2V0dGV4dChcIkZpbGwgb3V0IGJvdGggZmllbGRzLlwiKSk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIGFqYXgucG9zdChtaXNhZ28uZ2V0KCdBVVRIX0FQSScpLCB7XG4gICAgICAndXNlcm5hbWUnOiB0aGlzLnN0YXRlLnVzZXJuYW1lLFxuICAgICAgJ3Bhc3N3b3JkJzogdGhpcy5zdGF0ZS5wYXNzd29yZFxuICAgIH0pO1xuICB9XG5cbiAgaGFuZGxlU3VjY2VzcygpIHtcbiAgICBsZXQgZm9ybSA9ICQoJyNoaWRkZW4tbG9naW4tZm9ybScpO1xuXG4gICAgZm9ybS5hcHBlbmQoJzxpbnB1dCB0eXBlPVwidGV4dFwiIG5hbWU9XCJ1c2VybmFtZVwiIC8+Jyk7XG4gICAgZm9ybS5hcHBlbmQoJzxpbnB1dCB0eXBlPVwicGFzc3dvcmRcIiBuYW1lPVwicGFzc3dvcmRcIiAvPicpO1xuXG4gICAgLy8gZmlsbCBvdXQgZm9ybSB3aXRoIHVzZXIgY3JlZGVudGlhbHMgYW5kIHN1Ym1pdCBpdCwgdGhpcyB3aWxsIHRlbGxcbiAgICAvLyBNaXNhZ28gdG8gcmVkaXJlY3QgdXNlciBiYWNrIHRvIHJpZ2h0IHBhZ2UsIGFuZCB3aWxsIHRyaWdnZXIgYnJvd3NlcidzXG4gICAgLy8ga2V5IHJpbmcgZmVhdHVyZVxuICAgIGZvcm0uZmluZCgnaW5wdXRbdHlwZT1cImhpZGRlblwiXScpLnZhbChhamF4LmdldENzcmZUb2tlbigpKTtcbiAgICBmb3JtLmZpbmQoJ2lucHV0W25hbWU9XCJyZWRpcmVjdF90b1wiXScpLnZhbCh3aW5kb3cubG9jYXRpb24ucGF0aG5hbWUpO1xuICAgIGZvcm0uZmluZCgnaW5wdXRbbmFtZT1cInVzZXJuYW1lXCJdJykudmFsKHRoaXMuc3RhdGUudXNlcm5hbWUpO1xuICAgIGZvcm0uZmluZCgnaW5wdXRbbmFtZT1cInBhc3N3b3JkXCJdJykudmFsKHRoaXMuc3RhdGUucGFzc3dvcmQpO1xuICAgIGZvcm0uc3VibWl0KCk7XG5cbiAgICAvLyBrZWVwIGZvcm0gbG9hZGluZ1xuICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgJ2lzTG9hZGluZyc6IHRydWVcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZUVycm9yKHJlamVjdGlvbikge1xuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDApIHtcbiAgICAgIGlmIChyZWplY3Rpb24uY29kZSA9PT0gJ2luYWN0aXZlX2FkbWluJykge1xuICAgICAgICBzbmFja2Jhci5pbmZvKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgICAgfSBlbHNlIGlmIChyZWplY3Rpb24uY29kZSA9PT0gJ2luYWN0aXZlX3VzZXInKSB7XG4gICAgICAgIHNuYWNrYmFyLmluZm8ocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICdzaG93QWN0aXZhdGlvbic6IHRydWVcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2UgaWYgKHJlamVjdGlvbi5jb2RlID09PSAnYmFubmVkJykge1xuICAgICAgICBzaG93QmFubmVkUGFnZShyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgICAgbW9kYWwuaGlkZSgpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgc25hY2tiYXIuZXJyb3IocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDMgJiYgcmVqZWN0aW9uLmJhbikge1xuICAgICAgc2hvd0Jhbm5lZFBhZ2UocmVqZWN0aW9uLmJhbik7XG4gICAgICBtb2RhbC5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNuYWNrYmFyLmFwaUVycm9yKHJlamVjdGlvbik7XG4gICAgfVxuICB9XG5cbiAgZ2V0QWN0aXZhdGlvbkJ1dHRvbigpIHtcbiAgICBpZiAodGhpcy5zdGF0ZS5zaG93QWN0aXZhdGlvbikge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgcmV0dXJuIDxhIGhyZWY9e21pc2Fnby5nZXQoJ1JFUVVFU1RfQUNUSVZBVElPTl9VUkwnKX1cbiAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJidG4gYnRuLXN1Y2Nlc3MgYnRuLWJsb2NrXCI+XG4gICAgICAgICB7Z2V0dGV4dChcIkFjdGl2YXRlIGFjY291bnRcIil9XG4gICAgICA8L2E+O1xuICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1kaWFsb2cgbW9kYWwtc20gbW9kYWwtc2lnbi1pblwiXG4gICAgICAgICAgICAgICAgcm9sZT1cImRvY3VtZW50XCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWNvbnRlbnRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1oZWFkZXJcIj5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJjbG9zZVwiIGRhdGEtZGlzbWlzcz1cIm1vZGFsXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtbGFiZWw9e2dldHRleHQoXCJDbG9zZVwiKX0+XG4gICAgICAgICAgICA8c3BhbiBhcmlhLWhpZGRlbj1cInRydWVcIj4mdGltZXM7PC9zcGFuPlxuICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgIDxoNCBjbGFzc05hbWU9XCJtb2RhbC10aXRsZVwiPntnZXR0ZXh0KFwiU2lnbiBpblwiKX08L2g0PlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fT5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHlcIj5cblxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJmb3JtLWdyb3VwXCI+XG4gICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udHJvbC1pbnB1dFwiPlxuICAgICAgICAgICAgICAgIDxpbnB1dCBpZD1cImlkX3VzZXJuYW1lXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCIgdHlwZT1cInRleHRcIlxuICAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiVXNlcm5hbWUgb3IgZS1tYWlsXCIpfVxuICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3VzZXJuYW1lJyl9XG4gICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnVzZXJuYW1lfSAvPlxuICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDwvZGl2PlxuXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXBcIj5cbiAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250cm9sLWlucHV0XCI+XG4gICAgICAgICAgICAgICAgPGlucHV0IGlkPVwiaWRfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIiB0eXBlPVwicGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiUGFzc3dvcmRcIil9XG4gICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgncGFzc3dvcmQnKX1cbiAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUucGFzc3dvcmR9IC8+XG4gICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWZvb3RlclwiPlxuICAgICAgICAgICAge3RoaXMuZ2V0QWN0aXZhdGlvbkJ1dHRvbigpfVxuICAgICAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgICAgICBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAgICAgIHtnZXR0ZXh0KFwiU2lnbiBpblwiKX1cbiAgICAgICAgICAgIDwvQnV0dG9uPlxuICAgICAgICAgICAgPGEgaHJlZj17bWlzYWdvLmdldCgnRk9SR09UVEVOX1BBU1NXT1JEX1VSTCcpfVxuICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuIGJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAgICAge2dldHRleHQoXCJGb3Jnb3QgcGFzc3dvcmQ/XCIpfVxuICAgICAgICAgICAgPC9hPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Zvcm0+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuY29uc3QgVFlQRVNfQ0xBU1NFUyA9IHtcbiAgJ2luZm8nOiAnYWxlcnQtaW5mbycsXG4gICdzdWNjZXNzJzogJ2FsZXJ0LXN1Y2Nlc3MnLFxuICAnd2FybmluZyc6ICdhbGVydC13YXJuaW5nJyxcbiAgJ2Vycm9yJzogJ2FsZXJ0LWRhbmdlcidcbn07XG4vKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG5leHBvcnQgY2xhc3MgU25hY2tiYXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRTbmFja2JhckNsYXNzKCkge1xuICAgIGxldCBzbmFja2JhckNsYXNzID0gJ2FsZXJ0cy1zbmFja2Jhcic7XG4gICAgaWYgKHRoaXMucHJvcHMuaXNWaXNpYmxlKSB7XG4gICAgICBzbmFja2JhckNsYXNzICs9ICcgaW4nO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2JhckNsYXNzICs9ICcgb3V0JztcbiAgICB9XG4gICAgcmV0dXJuIHNuYWNrYmFyQ2xhc3M7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRTbmFja2JhckNsYXNzKCl9PlxuICAgICAgPHAgY2xhc3NOYW1lPXsnYWxlcnQgJyArIFRZUEVTX0NMQVNTRVNbdGhpcy5wcm9wcy50eXBlXX0+XG4gICAgICAgIHt0aGlzLnByb3BzLm1lc3NhZ2V9XG4gICAgICA8L3A+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4gc3RhdGUuc25hY2tiYXI7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEF2YXRhciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdmF0YXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWdpc3RlckJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9yZWdpc3Rlci1idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBTaWduSW5Nb2RhbCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9zaWduLWluLmpzJztcbmltcG9ydCBkcm9wZG93biBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9iaWxlLW5hdmJhci1kcm9wZG93bic7XG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcblxuZXhwb3J0IGNsYXNzIEd1ZXN0TWVudSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHNob3dTaWduSW5Nb2RhbCgpIHtcbiAgICBtb2RhbC5zaG93KFNpZ25Jbk1vZGFsKTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51IHVzZXItZHJvcGRvd24gZHJvcGRvd24tbWVudS1yaWdodFwiXG4gICAgICAgICAgICAgICByb2xlPVwibWVudVwiPlxuICAgICAgPGxpIGNsYXNzTmFtZT1cImd1ZXN0LXByZXZpZXdcIj5cbiAgICAgICAgPGg0PntnZXR0ZXh0KFwiWW91IGFyZSBicm93c2luZyBhcyBndWVzdC5cIil9PC9oND5cbiAgICAgICAgPHA+XG4gICAgICAgICAge2dldHRleHQoJ1NpZ24gaW4gb3IgcmVnaXN0ZXIgdG8gc3RhcnQgYW5kIHBhcnRpY2lwYXRlIGluIGRpc2N1c3Npb25zLicpfVxuICAgICAgICA8L3A+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicm93XCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb2wteHMtNlwiPlxuXG4gICAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLWRlZmF1bHQgYnRuLWJsb2NrXCJcbiAgICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5zaG93U2lnbkluTW9kYWx9PlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIlNpZ24gaW5cIil9XG4gICAgICAgICAgICA8L2J1dHRvbj5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLXhzLTZcIj5cblxuICAgICAgICAgICAgPFJlZ2lzdGVyQnV0dG9uIGNsYXNzTmFtZT1cImJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAgICB7Z2V0dGV4dChcIlJlZ2lzdGVyXCIpfVxuICAgICAgICAgICAgPC9SZWdpc3RlckJ1dHRvbj5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvbGk+XG4gICAgPC91bD47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgR3Vlc3ROYXYgZXh0ZW5kcyBHdWVzdE1lbnUge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm5hdiBuYXYtZ3Vlc3RcIj5cbiAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzTmFtZT1cImJ0biBuYXZiYXItYnRuIGJ0bi1kZWZhdWx0XCJcbiAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5zaG93U2lnbkluTW9kYWx9PlxuICAgICAgICB7Z2V0dGV4dChcIlNpZ24gaW5cIil9XG4gICAgICA8L2J1dHRvbj5cbiAgICAgIDxSZWdpc3RlckJ1dHRvbiBjbGFzc05hbWU9XCJuYXZiYXItYnRuIGJ0bi1wcmltYXJ5XCI+XG4gICAgICAgIHtnZXR0ZXh0KFwiUmVnaXN0ZXJcIil9XG4gICAgICA8L1JlZ2lzdGVyQnV0dG9uPlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBDb21wYWN0R3Vlc3ROYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBzaG93R3Vlc3RNZW51KCkge1xuICAgIGRyb3Bkb3duLnNob3coR3Vlc3RNZW51KTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIG9uQ2xpY2s9e3RoaXMuc2hvd0d1ZXN0TWVudX0+XG4gICAgICA8QXZhdGFyIHNpemU9XCI2NFwiIC8+XG4gICAgPC9idXR0b24+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBHdWVzdE5hdiwgQ29tcGFjdEd1ZXN0TmF2IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvdXNlci1tZW51L2d1ZXN0LW5hdic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHsgVXNlck5hdiwgQ29tcGFjdFVzZXJOYXZ9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3VzZXItbWVudS91c2VyLW5hdic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgVXNlck1lbnUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGlmICh0aGlzLnByb3BzLmlzQXV0aGVudGljYXRlZCkge1xuICAgICAgcmV0dXJuIDxVc2VyTmF2IHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8R3Vlc3ROYXYgLz47XG4gICAgfVxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIENvbXBhY3RVc2VyTWVudSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgaWYgKHRoaXMucHJvcHMuaXNBdXRoZW50aWNhdGVkKSB7XG4gICAgICByZXR1cm4gPENvbXBhY3RVc2VyTmF2IHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8Q29tcGFjdEd1ZXN0TmF2IC8+O1xuICAgIH1cbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzZWxlY3Qoc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLmF1dGg7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JztcbmltcG9ydCBBdmF0YXIgZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYXZhdGFyJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQ2hhbmdlQXZhdGFyTW9kYWwsIHsgc2VsZWN0IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvY2hhbmdlLWF2YXRhci9yb290JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IGRyb3Bkb3duIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2JpbGUtbmF2YmFyLWRyb3Bkb3duJztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuXG5leHBvcnQgY2xhc3MgVXNlck1lbnUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBsb2dvdXQoKSB7XG4gICAgbGV0IGRlY2lzaW9uID0gY29uZmlybShnZXR0ZXh0KFwiQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIHNpZ24gb3V0P1wiKSk7XG4gICAgaWYgKGRlY2lzaW9uKSB7XG4gICAgICAkKCcjaGlkZGVuLWxvZ291dC1mb3JtJykuc3VibWl0KCk7XG4gICAgfVxuICB9XG5cbiAgY2hhbmdlQXZhdGFyKCkge1xuICAgIG1vZGFsLnNob3coY29ubmVjdChzZWxlY3QpKENoYW5nZUF2YXRhck1vZGFsKSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8dWwgY2xhc3NOYW1lPVwiZHJvcGRvd24tbWVudSB1c2VyLWRyb3Bkb3duIGRyb3Bkb3duLW1lbnUtcmlnaHRcIlxuICAgICAgICAgICAgICAgcm9sZT1cIm1lbnVcIj5cbiAgICAgIDxsaSBjbGFzc05hbWU9XCJkcm9wZG93bi1oZWFkZXJcIj5cbiAgICAgICAgPHN0cm9uZz57dGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lfTwvc3Ryb25nPlxuICAgICAgPC9saT5cbiAgICAgIDxsaSBjbGFzc05hbWU9XCJkaXZpZGVyXCIgLz5cbiAgICAgIDxsaT5cbiAgICAgICAgPGEgaHJlZj17dGhpcy5wcm9wcy51c2VyLmFic29sdXRlX3VybH0+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPmFjY291bnRfY2lyY2xlPC9zcGFuPlxuICAgICAgICAgIHtnZXR0ZXh0KFwiU2VlIHlvdXIgcHJvZmlsZVwiKX1cbiAgICAgICAgPC9hPlxuICAgICAgPC9saT5cbiAgICAgIDxsaT5cbiAgICAgICAgPGEgaHJlZj17bWlzYWdvLmdldCgnVVNFUkNQX1VSTCcpfT5cbiAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+ZG9uZV9hbGw8L3NwYW4+XG4gICAgICAgICAge2dldHRleHQoXCJDaGFuZ2Ugb3B0aW9uc1wiKX1cbiAgICAgICAgPC9hPlxuICAgICAgPC9saT5cbiAgICAgIDxsaT5cbiAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuLWxpbmtcIiBvbkNsaWNrPXt0aGlzLmNoYW5nZUF2YXRhcn0+XG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwibWF0ZXJpYWwtaWNvblwiPmZhY2U8L3NwYW4+XG4gICAgICAgICAge2dldHRleHQoXCJDaGFuZ2UgYXZhdGFyXCIpfVxuICAgICAgICA8L2J1dHRvbj5cbiAgICAgIDwvbGk+XG4gICAgICA8bGkgY2xhc3NOYW1lPVwiZGl2aWRlclwiIC8+XG4gICAgICA8bGkgY2xhc3NOYW1lPVwiZHJvcGRvd24tZm9vdGVyXCI+XG4gICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIGJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiXG4gICAgICAgICAgICAgICAgICBvbkNsaWNrPXt0aGlzLmxvZ291dH0+XG4gICAgICAgICAgICB7Z2V0dGV4dChcIkxvZyBvdXRcIil9XG4gICAgICAgICAgPC9idXR0b24+XG4gICAgICA8L2xpPlxuICAgIDwvdWw+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFVzZXJOYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8dWwgY2xhc3NOYW1lPVwidWwgbmF2IG5hdmJhci1uYXYgbmF2LXVzZXJcIj5cbiAgICAgIDxsaSBjbGFzc05hbWU9XCJkcm9wZG93blwiPlxuICAgICAgICA8YSBocmVmPXt0aGlzLnByb3BzLnVzZXIuYWJzb2x1dGVfdXJsfSBjbGFzc05hbWU9XCJkcm9wZG93bi10b2dnbGVcIlxuICAgICAgICAgICBkYXRhLXRvZ2dsZT1cImRyb3Bkb3duXCIgYXJpYS1oYXNwb3B1cD1cInRydWVcIiBhcmlhLWV4cGFuZGVkPVwiZmFsc2VcIlxuICAgICAgICAgICByb2xlPVwiYnV0dG9uXCI+XG4gICAgICAgICAgPEF2YXRhciB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IHNpemU9XCI2NFwiIC8+XG4gICAgICAgIDwvYT5cbiAgICAgICAgPFVzZXJNZW51IHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz5cbiAgICAgIDwvbGk+XG4gICAgPC91bD47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2VsZWN0VXNlck1lbnUoc3RhdGUpIHtcbiAgY29uc29sZS5sb2coc3RhdGUpO1xuICByZXR1cm4ge3VzZXI6IHN0YXRlLmF1dGgudXNlcn07XG59XG5cbmV4cG9ydCBjbGFzcyBDb21wYWN0VXNlck5hdiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHNob3dVc2VyTWVudSgpIHtcbiAgICBkcm9wZG93bi5zaG93Q29ubmVjdGVkKCd1c2VyLW1lbnUnLCBjb25uZWN0KHNlbGVjdFVzZXJNZW51KShVc2VyTWVudSkpO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgb25DbGljaz17dGhpcy5zaG93VXNlck1lbnV9PlxuICAgICAgPEF2YXRhciB1c2VyPXt0aGlzLnByb3BzLnVzZXJ9IHNpemU9XCI2NFwiIC8+XG4gICAgPC9idXR0b24+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBPcmRlcmVkTGlzdCBmcm9tICdtaXNhZ28vdXRpbHMvb3JkZXJlZC1saXN0JztcblxuZXhwb3J0IGNsYXNzIE1pc2FnbyB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2luaXRpYWxpemVycyA9IFtdO1xuICAgIHRoaXMuX2NvbnRleHQgPSB7fTtcbiAgfVxuXG4gIGFkZEluaXRpYWxpemVyKGluaXRpYWxpemVyKSB7XG4gICAgdGhpcy5faW5pdGlhbGl6ZXJzLnB1c2goe1xuICAgICAga2V5OiBpbml0aWFsaXplci5uYW1lLFxuXG4gICAgICBpdGVtOiBpbml0aWFsaXplci5pbml0aWFsaXplcixcblxuICAgICAgYWZ0ZXI6IGluaXRpYWxpemVyLmFmdGVyLFxuICAgICAgYmVmb3JlOiBpbml0aWFsaXplci5iZWZvcmVcbiAgICB9KTtcbiAgfVxuXG4gIGluaXQoY29udGV4dCkge1xuICAgIHRoaXMuX2NvbnRleHQgPSBjb250ZXh0O1xuXG4gICAgdmFyIGluaXRPcmRlciA9IG5ldyBPcmRlcmVkTGlzdCh0aGlzLl9pbml0aWFsaXplcnMpLm9yZGVyZWRWYWx1ZXMoKTtcbiAgICBpbml0T3JkZXIuZm9yRWFjaChpbml0aWFsaXplciA9PiB7XG4gICAgICBpbml0aWFsaXplcih0aGlzKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8vIGNvbnRleHQgYWNjZXNzb3JzXG4gIGhhcyhrZXkpIHtcbiAgICByZXR1cm4gdGhpcy5fY29udGV4dC5oYXNPd25Qcm9wZXJ0eShrZXkpO1xuICB9XG5cbiAgZ2V0KGtleSwgZmFsbGJhY2spIHtcbiAgICBpZiAodGhpcy5oYXMoa2V5KSkge1xuICAgICAgcmV0dXJuIHRoaXMuX2NvbnRleHRba2V5XTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIGZhbGxiYWNrIHx8IHVuZGVmaW5lZDtcbiAgICB9XG4gIH1cbn1cblxuLy8gY3JlYXRlICBzaW5nbGV0b25cbnZhciBtaXNhZ28gPSBuZXcgTWlzYWdvKCk7XG5cbi8vIGV4cG9zZSBpdCBnbG9iYWxseVxuZ2xvYmFsLm1pc2FnbyA9IG1pc2FnbztcblxuLy8gYW5kIGV4cG9ydCBpdCBmb3IgdGVzdHMgYW5kIHN0dWZmXG5leHBvcnQgZGVmYXVsdCBtaXNhZ287XG4iLCJpbXBvcnQgeyBVUERBVEVfQVZBVEFSIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3VzZXJzJztcblxuZXhwb3J0IHZhciBpbml0aWFsU3RhdGUgPSB7XG4gIHNpZ25lZEluOiBmYWxzZSxcbiAgc2lnbmVkT3V0OiBmYWxzZVxufTtcblxuZXhwb3J0IGNvbnN0IFNJR05fSU4gPSAnU0lHTl9JTic7XG5leHBvcnQgY29uc3QgU0lHTl9PVVQgPSAnU0lHTl9PVVQnO1xuXG5leHBvcnQgZnVuY3Rpb24gc2lnbkluKHVzZXIpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBTSUdOX0lOLFxuICAgIHVzZXJcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNpZ25PdXQoc29mdD1mYWxzZSkge1xuICByZXR1cm4ge1xuICAgIHR5cGU6IFNJR05fT1VULFxuICAgIHNvZnRcbiAgfTtcbn1cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gYXV0aChzdGF0ZT1pbml0aWFsU3RhdGUsIGFjdGlvbj1udWxsKSB7XG4gIHN3aXRjaCAoYWN0aW9uLnR5cGUpIHtcbiAgICBjYXNlIFNJR05fSU46XG4gICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgc2lnbmVkSW46IGFjdGlvbi51c2VyXG4gICAgICB9KTtcblxuICAgIGNhc2UgU0lHTl9PVVQ6XG4gICAgICByZXR1cm4gT2JqZWN0LmFzc2lnbih7fSwgc3RhdGUsIHtcbiAgICAgICAgaXNBdXRoZW50aWNhdGVkOiBmYWxzZSxcbiAgICAgICAgaXNBbm9ueW1vdXM6IHRydWUsXG4gICAgICAgIHNpZ25lZE91dDogIWFjdGlvbi5zb2Z0XG4gICAgICB9KTtcblxuICAgIGNhc2UgVVBEQVRFX0FWQVRBUjpcbiAgICAgIGlmIChzdGF0ZS5pc0F1dGhlbnRpY2F0ZWQgJiYgc3RhdGUudXNlci5pZCA9PT0gYWN0aW9uLnVzZXJJZCkge1xuICAgICAgICBsZXQgbmV3U3RhdGUgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSk7XG4gICAgICAgIG5ld1N0YXRlLnVzZXIgPSBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZS51c2VyLCB7XG4gICAgICAgICAgJ2F2YXRhcl9oYXNoJzogYWN0aW9uLmF2YXRhckhhc2hcbiAgICAgICAgfSk7XG4gICAgICAgIHJldHVybiBuZXdTdGF0ZTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBzdGF0ZTtcblxuICAgIGRlZmF1bHQ6XG4gICAgICByZXR1cm4gc3RhdGU7XG4gIH1cbn1cbiIsImV4cG9ydCB2YXIgaW5pdGlhbFN0YXRlID0ge1xuICB0eXBlOiAnaW5mbycsXG4gIG1lc3NhZ2U6ICcnLFxuICBpc1Zpc2libGU6IGZhbHNlXG59O1xuXG5leHBvcnQgY29uc3QgU0hPV19TTkFDS0JBUiA9ICdTSE9XX1NOQUNLQkFSJztcbmV4cG9ydCBjb25zdCBISURFX1NOQUNLQkFSID0gJ0hJREVfU05BQ0tCQVInO1xuXG5leHBvcnQgZnVuY3Rpb24gc2hvd1NuYWNrYmFyKG1lc3NhZ2UsIHR5cGUpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBTSE9XX1NOQUNLQkFSLFxuICAgIG1lc3NhZ2UsXG4gICAgbWVzc2FnZVR5cGU6IHR5cGVcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGhpZGVTbmFja2JhcigpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBISURFX1NOQUNLQkFSXG4gIH07XG59XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIHNuYWNrYmFyKHN0YXRlPWluaXRpYWxTdGF0ZSwgYWN0aW9uPW51bGwpIHtcbiAgaWYgKGFjdGlvbi50eXBlID09PSBTSE9XX1NOQUNLQkFSKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHR5cGU6IGFjdGlvbi5tZXNzYWdlVHlwZSxcbiAgICAgIG1lc3NhZ2U6IGFjdGlvbi5tZXNzYWdlLFxuICAgICAgaXNWaXNpYmxlOiB0cnVlXG4gICAgfTtcbiAgfSBlbHNlIGlmIChhY3Rpb24udHlwZSA9PT0gSElERV9TTkFDS0JBUikge1xuICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSwge1xuICAgICAgICBpc1Zpc2libGU6IGZhbHNlXG4gICAgfSk7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIHN0YXRlO1xuICB9XG59XG4iLCJleHBvcnQgdmFyIGluaXRpYWxTdGF0ZSA9IHtcbiAgdGljazogMFxufTtcblxuZXhwb3J0IGNvbnN0IFRJQ0sgPSAnVElDSyc7XG5cbmV4cG9ydCBmdW5jdGlvbiBkb1RpY2soKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogVElDS1xuICB9O1xufVxuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiB0aWNrKHN0YXRlPWluaXRpYWxTdGF0ZSwgYWN0aW9uPW51bGwpIHtcbiAgaWYgKGFjdGlvbi50eXBlID09PSBUSUNLKSB7XG4gICAgcmV0dXJuIE9iamVjdC5hc3NpZ24oe30sIHN0YXRlLCB7XG4gICAgICAgIHRpY2s6IHN0YXRlLnRpY2sgKyAxXG4gICAgfSk7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIHN0YXRlO1xuICB9XG59XG4iLCJleHBvcnQgY29uc3QgVVBEQVRFX0FWQVRBUiA9ICdVUERBVEVfQVZBVEFSJztcblxuZXhwb3J0IGZ1bmN0aW9uIHVwZGF0ZUF2YXRhcih1c2VyLCBhdmF0YXJIYXNoKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogVVBEQVRFX0FWQVRBUixcbiAgICB1c2VySWQ6IHVzZXIuaWQsXG4gICAgYXZhdGFySGFzaFxuICB9O1xufSIsImV4cG9ydCBjbGFzcyBBamF4IHtcbiAgY29uc3RydWN0b3IoKSB7XG4gICAgdGhpcy5fY29va2llTmFtZSA9IG51bGw7XG4gICAgdGhpcy5fY3NyZlRva2VuID0gbnVsbDtcbiAgfVxuXG4gIGluaXQoY29va2llTmFtZSkge1xuICAgIHRoaXMuX2Nvb2tpZU5hbWUgPSBjb29raWVOYW1lO1xuICAgIHRoaXMuX2NzcmZUb2tlbiA9IHRoaXMuZ2V0Q3NyZlRva2VuKCk7XG4gIH1cblxuICBnZXRDc3JmVG9rZW4oKSB7XG4gICAgaWYgKGRvY3VtZW50LmNvb2tpZS5pbmRleE9mKHRoaXMuX2Nvb2tpZU5hbWUpICE9PSAtMSkge1xuICAgICAgdmFyIGNvb2tpZVJlZ2V4ID0gbmV3IFJlZ0V4cCh0aGlzLl9jb29raWVOYW1lICsgJ1xcPShbXjtdKiknKTtcbiAgICAgIHZhciBjb29raWUgPSBkb2N1bWVudC5jb29raWUubWF0Y2goY29va2llUmVnZXgpWzBdO1xuICAgICAgcmV0dXJuIGNvb2tpZSA/IGNvb2tpZS5zcGxpdCgnPScpWzFdIDogbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9XG5cbiAgcmVxdWVzdChtZXRob2QsIHVybCwgZGF0YSkge1xuICAgIHZhciBzZWxmID0gdGhpcztcbiAgICByZXR1cm4gbmV3IFByb21pc2UoZnVuY3Rpb24ocmVzb2x2ZSwgcmVqZWN0KSB7XG4gICAgICB2YXIgeGhyID0ge1xuICAgICAgICB1cmw6IHVybCxcbiAgICAgICAgbWV0aG9kOiBtZXRob2QsXG4gICAgICAgIGhlYWRlcnM6IHtcbiAgICAgICAgICAnWC1DU1JGVG9rZW4nOiBzZWxmLl9jc3JmVG9rZW5cbiAgICAgICAgfSxcblxuICAgICAgICBkYXRhOiBkYXRhIHx8IHt9LFxuICAgICAgICBkYXRhVHlwZTogJ2pzb24nLFxuXG4gICAgICAgIHN1Y2Nlc3M6IGZ1bmN0aW9uKGRhdGEpIHtcbiAgICAgICAgICByZXNvbHZlKGRhdGEpO1xuICAgICAgICB9LFxuXG4gICAgICAgIGVycm9yOiBmdW5jdGlvbihqcVhIUikge1xuICAgICAgICAgIHZhciByZWplY3Rpb24gPSBqcVhIUi5yZXNwb25zZUpTT04gfHwge307XG5cbiAgICAgICAgICByZWplY3Rpb24uc3RhdHVzID0ganFYSFIuc3RhdHVzO1xuICAgICAgICAgIHJlamVjdGlvbi5zdGF0dXNUZXh0ID0ganFYSFIuc3RhdHVzVGV4dDtcblxuICAgICAgICAgIHJlamVjdChyZWplY3Rpb24pO1xuICAgICAgICB9XG4gICAgICB9O1xuXG4gICAgICAkLmFqYXgoeGhyKTtcbiAgICB9KTtcbiAgfVxuXG4gIGdldCh1cmwpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdHRVQnLCB1cmwpO1xuICB9XG5cbiAgcG9zdCh1cmwsIGRhdGEpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdQT1NUJywgdXJsLCBkYXRhKTtcbiAgfVxuXG4gIHBhdGNoKHVybCwgZGF0YSkge1xuICAgIHJldHVybiB0aGlzLnJlcXVlc3QoJ1BBVENIJywgdXJsLCBkYXRhKTtcbiAgfVxuXG4gIHB1dCh1cmwsIGRhdGEpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdQVVQnLCB1cmwsIGRhdGEpO1xuICB9XG5cbiAgZGVsZXRlKHVybCkge1xuICAgIHJldHVybiB0aGlzLnJlcXVlc3QoJ0RFTEVURScsIHVybCk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IEFqYXgoKTtcbiIsImltcG9ydCB7IHNpZ25Jbiwgc2lnbk91dCB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9hdXRoJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBjbGFzcyBBdXRoIHtcbiAgaW5pdChzdG9yZSwgbG9jYWwsIG1vZGFsKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBzdG9yZTtcbiAgICB0aGlzLl9sb2NhbCA9IGxvY2FsO1xuICAgIHRoaXMuX21vZGFsID0gbW9kYWw7XG5cbiAgICAvLyB0ZWxsIG90aGVyIHRhYnMgd2hhdCBhdXRoIHN0YXRlIGlzIGJlY2F1c2Ugd2UgYXJlIG1vc3QgY3VycmVudCB3aXRoIGl0XG4gICAgdGhpcy5zeW5jU2Vzc2lvbigpO1xuXG4gICAgLy8gbGlzdGVuIGZvciBvdGhlciB0YWJzIHRvIHRlbGwgdXMgdGhhdCBzdGF0ZSBjaGFuZ2VkXG4gICAgdGhpcy53YXRjaFN0YXRlKCk7XG4gIH1cblxuICBzeW5jU2Vzc2lvbigpIHtcbiAgICBsZXQgc3RhdGUgPSB0aGlzLl9zdG9yZS5nZXRTdGF0ZSgpLmF1dGg7XG4gICAgaWYgKHN0YXRlLmlzQXV0aGVudGljYXRlZCkge1xuICAgICAgdGhpcy5fbG9jYWwuc2V0KCdhdXRoJywge1xuICAgICAgICBpc0F1dGhlbnRpY2F0ZWQ6IHRydWUsXG4gICAgICAgIHVzZXJuYW1lOiBzdGF0ZS51c2VyLnVzZXJuYW1lXG4gICAgICB9KTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5fbG9jYWwuc2V0KCdhdXRoJywge1xuICAgICAgICBpc0F1dGhlbnRpY2F0ZWQ6IGZhbHNlXG4gICAgICB9KTtcbiAgICB9XG4gIH1cblxuICB3YXRjaFN0YXRlKCkge1xuICAgIHRoaXMuX2xvY2FsLndhdGNoKCdhdXRoJywgKG5ld1N0YXRlKSA9PiB7XG4gICAgICBpZiAobmV3U3RhdGUuaXNBdXRoZW50aWNhdGVkKSB7XG4gICAgICAgIHRoaXMuX3N0b3JlLmRpc3BhdGNoKHNpZ25Jbih7XG4gICAgICAgICAgdXNlcm5hbWU6IG5ld1N0YXRlLnVzZXJuYW1lXG4gICAgICAgIH0pKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuX3N0b3JlLmRpc3BhdGNoKHNpZ25PdXQoKSk7XG4gICAgICB9XG4gICAgfSk7XG4gICAgdGhpcy5fbW9kYWwuaGlkZSgpO1xuICB9XG5cbiAgc2lnbkluKHVzZXIpIHtcbiAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaWduSW4odXNlcikpO1xuICAgIHRoaXMuX2xvY2FsLnNldCgnYXV0aCcsIHtcbiAgICAgIGlzQXV0aGVudGljYXRlZDogdHJ1ZSxcbiAgICAgIHVzZXJuYW1lOiB1c2VyLnVzZXJuYW1lXG4gICAgfSk7XG4gICAgdGhpcy5fbW9kYWwuaGlkZSgpO1xuICB9XG5cbiAgc2lnbk91dCgpIHtcbiAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaWduT3V0KCkpO1xuICAgIHRoaXMuX2xvY2FsLnNldCgnYXV0aCcsIHtcbiAgICAgIGlzQXV0aGVudGljYXRlZDogZmFsc2VcbiAgICB9KTtcbiAgICB0aGlzLl9tb2RhbC5oaWRlKCk7XG4gIH1cblxuICBzb2Z0U2lnbk91dCgpIHtcbiAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaWduT3V0KHRydWUpKTtcbiAgICB0aGlzLl9sb2NhbC5zZXQoJ2F1dGgnLCB7XG4gICAgICBpc0F1dGhlbnRpY2F0ZWQ6IGZhbHNlXG4gICAgfSk7XG4gICAgdGhpcy5fbW9kYWwuaGlkZSgpO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBBdXRoKCk7IiwiLyogZ2xvYmFsIGdyZWNhcHRjaGEgKi9cbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IEZvcm1Hcm91cCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtLWdyb3VwJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBjbGFzcyBCYXNlQ2FwdGNoYSB7XG4gIGluaXQoY29udGV4dCwgYWpheCwgaW5jbHVkZSwgc25hY2tiYXIpIHtcbiAgICB0aGlzLl9jb250ZXh0ID0gY29udGV4dDtcbiAgICB0aGlzLl9hamF4ID0gYWpheDtcbiAgICB0aGlzLl9pbmNsdWRlID0gaW5jbHVkZTtcbiAgICB0aGlzLl9zbmFja2JhciA9IHNuYWNrYmFyO1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBOb0NhcHRjaGEgZXh0ZW5kcyBCYXNlQ2FwdGNoYSB7XG4gIGxvYWQoKSB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUpIHtcbiAgICAgIC8vIGltbWVkaWF0ZWx5IHJlc29sdmUgYXMgd2UgZG9uJ3QgaGF2ZSBhbnl0aGluZyB0byB2YWxpZGF0ZVxuICAgICAgcmVzb2x2ZSgpO1xuICAgIH0pO1xuICB9XG5cbiAgdmFsaWRhdG9yKCkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG5cbiAgY29tcG9uZW50KCkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBRQUNhcHRjaGEgZXh0ZW5kcyBCYXNlQ2FwdGNoYSB7XG4gIGxvYWQoKSB7XG4gICAgdmFyIHNlbGYgPSB0aGlzO1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICBzZWxmLl9hamF4LmdldChzZWxmLl9jb250ZXh0LmdldCgnQ0FQVENIQV9BUElfVVJMJykpLnRoZW4oXG4gICAgICBmdW5jdGlvbihkYXRhKSB7XG4gICAgICAgIHNlbGYucXVlc3Rpb24gPSBkYXRhLnF1ZXN0aW9uO1xuICAgICAgICBzZWxmLmhlbHBUZXh0ID0gZGF0YS5oZWxwX3RleHQ7XG4gICAgICAgIHJlc29sdmUoKTtcbiAgICAgIH0sIGZ1bmN0aW9uKCkge1xuICAgICAgICBzZWxmLl9zbmFja2Jhci5lcnJvcihnZXR0ZXh0KFwiRmFpbGVkIHRvIGxvYWQgQ0FQVENIQS5cIikpO1xuICAgICAgICByZWplY3QoKTtcbiAgICAgIH0pO1xuICAgIH0pO1xuICB9XG5cbiAgdmFsaWRhdG9yKCkge1xuICAgIHJldHVybiBbXTtcbiAgfVxuXG4gIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgY29tcG9uZW50KGt3YXJncykge1xuICAgIHJldHVybiA8Rm9ybUdyb3VwIGxhYmVsPXt0aGlzLnF1ZXN0aW9ufSBmb3I9XCJpZF9jYXB0Y2hhXCJcbiAgICAgICAgICAgICAgICAgICAgICBsYWJlbENsYXNzPXtrd2FyZ3MubGFiZWxDbGFzcyB8fCBcImNvbC1zbS00XCJ9XG4gICAgICAgICAgICAgICAgICAgICAgY29udHJvbENsYXNzPXtrd2FyZ3MuY29udHJvbENsYXNzIHx8IFwiY29sLXNtLThcIn1cbiAgICAgICAgICAgICAgICAgICAgICB2YWxpZGF0aW9uPXtrd2FyZ3MuZm9ybS5zdGF0ZS5lcnJvcnMuY2FwdGNoYX1cbiAgICAgICAgICAgICAgICAgICAgICBoZWxwVGV4dD17dGhpcy5oZWxwVGV4dCB8fCBudWxsfT5cbiAgICAgIDxpbnB1dCB0eXBlPVwidGV4dFwiIGlkPVwiaWRfY2FwdGNoYVwiIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgYXJpYS1kZXNjcmliZWRieT1cImlkX2NhcHRjaGFfc3RhdHVzXCJcbiAgICAgICAgICAgICBkaXNhYmxlZD17a3dhcmdzLmZvcm0uc3RhdGUuaXNMb2FkaW5nfVxuICAgICAgICAgICAgIG9uQ2hhbmdlPXtrd2FyZ3MuZm9ybS5iaW5kSW5wdXQoJ2NhcHRjaGEnKX1cbiAgICAgICAgICAgICB2YWx1ZT17a3dhcmdzLmZvcm0uc3RhdGUuY2FwdGNoYX0gLz5cbiAgICA8L0Zvcm1Hcm91cD47XG4gIH1cbiAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbn1cblxuXG5leHBvcnQgY2xhc3MgUmVDYXB0Y2hhQ29tcG9uZW50IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgZ3JlY2FwdGNoYS5yZW5kZXIoJ3JlY2FwdGNoYScsIHtcbiAgICAgICdzaXRla2V5JzogdGhpcy5wcm9wcy5zaXRlS2V5LFxuICAgICAgJ2NhbGxiYWNrJzogKHJlc3BvbnNlKSA9PiB7XG4gICAgICAgIC8vIGZpcmUgZmFrZXkgZXZlbnQgdG8gYmluZGluZ1xuICAgICAgICB0aGlzLnByb3BzLmJpbmRpbmcoe1xuICAgICAgICAgIHRhcmdldDoge1xuICAgICAgICAgICAgdmFsdWU6IHJlc3BvbnNlXG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgaWQ9XCJyZWNhcHRjaGFcIiAvPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBSZUNhcHRjaGEgZXh0ZW5kcyBCYXNlQ2FwdGNoYSB7XG4gIGxvYWQoKSB7XG4gICAgdGhpcy5faW5jbHVkZS5pbmNsdWRlKCdodHRwczovL3d3dy5nb29nbGUuY29tL3JlY2FwdGNoYS9hcGkuanMnLCB0cnVlKTtcblxuICAgIHJldHVybiBuZXcgUHJvbWlzZShmdW5jdGlvbihyZXNvbHZlKSB7XG4gICAgICB2YXIgd2FpdCA9IGZ1bmN0aW9uKCkge1xuICAgICAgICBpZiAodHlwZW9mIGdyZWNhcHRjaGEgPT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICB3aW5kb3cuc2V0VGltZW91dChmdW5jdGlvbigpIHtcbiAgICAgICAgICAgIHdhaXQoKTtcbiAgICAgICAgICB9LCAyMDApO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJlc29sdmUoKTtcbiAgICAgICAgfVxuICAgICAgfTtcbiAgICAgIHdhaXQoKTtcbiAgICB9KTtcbiAgfVxuXG4gIHZhbGlkYXRvcigpIHtcbiAgICByZXR1cm4gW107XG4gIH1cblxuICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gIGNvbXBvbmVudChrd2FyZ3MpIHtcbiAgICByZXR1cm4gPEZvcm1Hcm91cCBsYWJlbD17Z2V0dGV4dChcIkNhcHRjaGFcIil9IGZvcj1cImlkX2NhcHRjaGFcIlxuICAgICAgICAgICAgICAgICAgICAgIGxhYmVsQ2xhc3M9e2t3YXJncy5sYWJlbENsYXNzIHx8IFwiY29sLXNtLTRcIn1cbiAgICAgICAgICAgICAgICAgICAgICBjb250cm9sQ2xhc3M9e2t3YXJncy5jb250cm9sQ2xhc3MgfHwgXCJjb2wtc20tOFwifVxuICAgICAgICAgICAgICAgICAgICAgIHZhbGlkYXRpb249e2t3YXJncy5mb3JtLnN0YXRlLmVycm9ycy5jYXB0Y2hhfVxuICAgICAgICAgICAgICAgICAgICAgIGhlbHBUZXh0PXtnZXR0ZXh0KFwiUGxlYXNlIHNvbHZlIHRoZSBxdWljayB0ZXN0LlwiKX0+XG4gICAgICA8UmVDYXB0Y2hhQ29tcG9uZW50IHNpdGVLZXk9e3RoaXMuX2NvbnRleHQuZ2V0KCdTRVRUSU5HUycpLnJlY2FwdGNoYV9zaXRlX2tleX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZz17a3dhcmdzLmZvcm0uYmluZElucHV0KCdjYXB0Y2hhJyl9IC8+XG4gICAgPC9Gb3JtR3JvdXA+O1xuICB9XG4gIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG59XG5cbmV4cG9ydCBjbGFzcyBDYXB0Y2hhIHtcbiAgaW5pdChjb250ZXh0LCBhamF4LCBpbmNsdWRlLCBzbmFja2Jhcikge1xuICAgIHN3aXRjaChjb250ZXh0LmdldCgnU0VUVElOR1MnKS5jYXB0Y2hhX3R5cGUpIHtcbiAgICAgIGNhc2UgJ25vJzpcbiAgICAgICAgdGhpcy5fY2FwdGNoYSA9IG5ldyBOb0NhcHRjaGEoKTtcbiAgICAgICAgYnJlYWs7XG5cbiAgICAgIGNhc2UgJ3FhJzpcbiAgICAgICAgdGhpcy5fY2FwdGNoYSA9IG5ldyBRQUNhcHRjaGEoKTtcbiAgICAgICAgYnJlYWs7XG5cbiAgICAgIGNhc2UgJ3JlJzpcbiAgICAgICAgdGhpcy5fY2FwdGNoYSA9IG5ldyBSZUNhcHRjaGEoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuXG4gICAgdGhpcy5fY2FwdGNoYS5pbml0KGNvbnRleHQsIGFqYXgsIGluY2x1ZGUsIHNuYWNrYmFyKTtcbiAgfVxuXG4gIC8vIGFjY2Vzc29ycyBmb3IgdW5kZXJseWluZyBzdHJhdGVneVxuXG4gIGxvYWQoKSB7XG4gICAgcmV0dXJuIHRoaXMuX2NhcHRjaGEubG9hZCgpO1xuICB9XG5cbiAgdmFsaWRhdG9yKCkge1xuICAgIHJldHVybiB0aGlzLl9jYXB0Y2hhLnZhbGlkYXRvcigpO1xuICB9XG5cbiAgY29tcG9uZW50KGt3YXJncykge1xuICAgIHJldHVybiB0aGlzLl9jYXB0Y2hhLmNvbXBvbmVudChrd2FyZ3MpO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBDYXB0Y2hhKCk7IiwiZXhwb3J0IGNsYXNzIEluY2x1ZGUge1xuICBpbml0KHN0YXRpY1VybCkge1xuICAgIHRoaXMuX3N0YXRpY1VybCA9IHN0YXRpY1VybDtcbiAgICB0aGlzLl9pbmNsdWRlZCA9IFtdO1xuICB9XG5cbiAgaW5jbHVkZShzY3JpcHQsIHJlbW90ZT1mYWxzZSkge1xuICAgIGlmICh0aGlzLl9pbmNsdWRlZC5pbmRleE9mKHNjcmlwdCkgPT09IC0xKSB7XG4gICAgICB0aGlzLl9pbmNsdWRlZC5wdXNoKHNjcmlwdCk7XG4gICAgICB0aGlzLl9pbmNsdWRlKHNjcmlwdCwgcmVtb3RlKTtcbiAgICB9XG4gIH1cblxuICBfaW5jbHVkZShzY3JpcHQsIHJlbW90ZSkge1xuICAgICQuYWpheCh7XG4gICAgICB1cmw6ICghcmVtb3RlID8gdGhpcy5fc3RhdGljVXJsIDogJycpICsgc2NyaXB0LFxuICAgICAgY2FjaGU6IHRydWUsXG4gICAgICBkYXRhVHlwZTogJ3NjcmlwdCdcbiAgICB9KTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgSW5jbHVkZSgpOyIsImxldCBzdG9yYWdlID0gd2luZG93LmxvY2FsU3RvcmFnZTtcblxuZXhwb3J0IGNsYXNzIExvY2FsU3RvcmFnZSB7XG4gIGluaXQocHJlZml4KSB7XG4gICAgdGhpcy5fcHJlZml4ID0gcHJlZml4O1xuICAgIHRoaXMuX3dhdGNoZXJzID0gW107XG5cbiAgICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignc3RvcmFnZScsIChlKSA9PiB7XG4gICAgICBsZXQgbmV3VmFsdWVKc29uID0gSlNPTi5wYXJzZShlLm5ld1ZhbHVlKTtcbiAgICAgIHRoaXMuX3dhdGNoZXJzLmZvckVhY2goZnVuY3Rpb24od2F0Y2hlcikge1xuICAgICAgICBpZiAod2F0Y2hlci5rZXkgPT09IGUua2V5ICYmIGUub2xkVmFsdWUgIT09IGUubmV3VmFsdWUpIHtcbiAgICAgICAgICB3YXRjaGVyLmNhbGxiYWNrKG5ld1ZhbHVlSnNvbik7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH0pO1xuICB9XG5cbiAgc2V0KGtleSwgdmFsdWUpIHtcbiAgICBzdG9yYWdlLnNldEl0ZW0odGhpcy5fcHJlZml4ICsga2V5LCBKU09OLnN0cmluZ2lmeSh2YWx1ZSkpO1xuICB9XG5cbiAgZ2V0KGtleSkge1xuICAgIGxldCBpdGVtU3RyaW5nID0gc3RvcmFnZS5nZXRJdGVtKHRoaXMuX3ByZWZpeCArIGtleSk7XG4gICAgaWYgKGl0ZW1TdHJpbmcpIHtcbiAgICAgIHJldHVybiBKU09OLnBhcnNlKGl0ZW1TdHJpbmcpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICB3YXRjaChrZXksIGNhbGxiYWNrKSB7XG4gICAgdGhpcy5fd2F0Y2hlcnMucHVzaCh7XG4gICAgICBrZXk6IHRoaXMuX3ByZWZpeCArIGtleSxcbiAgICAgIGNhbGxiYWNrOiBjYWxsYmFja1xuICAgIH0pO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBMb2NhbFN0b3JhZ2UoKTsiLCJpbXBvcnQgbW91bnQgZnJvbSAnbWlzYWdvL3V0aWxzL21vdW50LWNvbXBvbmVudCc7XG5cbmV4cG9ydCBjbGFzcyBNb2JpbGVOYXZiYXJEcm9wZG93biB7XG4gIGluaXQoZWxlbWVudCkge1xuICAgIHRoaXMuX2VsZW1lbnQgPSBlbGVtZW50O1xuICAgIHRoaXMuX2NvbXBvbmVudCA9IG51bGw7XG4gIH1cblxuICBzaG93KGNvbXBvbmVudCkge1xuICAgIGlmICh0aGlzLl9jb21wb25lbnQgPT09IGNvbXBvbmVudCkge1xuICAgICAgdGhpcy5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2NvbXBvbmVudCA9IGNvbXBvbmVudDtcbiAgICAgIG1vdW50KGNvbXBvbmVudCwgdGhpcy5fZWxlbWVudC5pZCk7XG4gICAgICAkKHRoaXMuX2VsZW1lbnQpLmFkZENsYXNzKCdvcGVuJyk7XG4gICAgfVxuICB9XG5cbiAgc2hvd0Nvbm5lY3RlZChuYW1lLCBjb21wb25lbnQpIHtcbiAgICBpZiAodGhpcy5fY29tcG9uZW50ID09PSBuYW1lKSB7XG4gICAgICB0aGlzLmhpZGUoKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5fY29tcG9uZW50ID0gbmFtZTtcbiAgICAgIG1vdW50KGNvbXBvbmVudCwgdGhpcy5fZWxlbWVudC5pZCwgdHJ1ZSk7XG4gICAgICAkKHRoaXMuX2VsZW1lbnQpLmFkZENsYXNzKCdvcGVuJyk7XG4gICAgfVxuICB9XG5cbiAgaGlkZSgpIHtcbiAgICAkKHRoaXMuX2VsZW1lbnQpLnJlbW92ZUNsYXNzKCdvcGVuJyk7XG4gICAgdGhpcy5fY29tcG9uZW50ID0gbnVsbDtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgTW9iaWxlTmF2YmFyRHJvcGRvd24oKTtcbiIsImltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgY2xhc3MgTW9kYWwge1xuICBpbml0KGVsZW1lbnQpIHtcbiAgICB0aGlzLl9lbGVtZW50ID0gZWxlbWVudDtcblxuICAgIHRoaXMuX21vZGFsID0gJChlbGVtZW50KS5tb2RhbCh7c2hvdzogZmFsc2V9KTtcblxuICAgIHRoaXMuX21vZGFsLm9uKCdoaWRkZW4uYnMubW9kYWwnLCAoKSA9PiB7XG4gICAgICBSZWFjdERPTS51bm1vdW50Q29tcG9uZW50QXROb2RlKHRoaXMuX2VsZW1lbnQpO1xuICAgIH0pO1xuICB9XG5cbiAgc2hvdyhjb21wb25lbnQpIHtcbiAgICBtb3VudChjb21wb25lbnQsIHRoaXMuX2VsZW1lbnQuaWQpO1xuICAgIHRoaXMuX21vZGFsLm1vZGFsKCdzaG93Jyk7XG4gIH1cblxuICBoaWRlKCkge1xuICAgIHRoaXMuX21vZGFsLm1vZGFsKCdoaWRlJyk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IE1vZGFsKCk7XG4iLCJpbXBvcnQgeyBzaG93U25hY2tiYXIsIGhpZGVTbmFja2JhciB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9zbmFja2Jhcic7XG5cbmNvbnN0IEhJREVfQU5JTUFUSU9OX0xFTkdUSCA9IDMwMDtcbmNvbnN0IE1FU1NBR0VfU0hPV19MRU5HVEggPSA1MDAwO1xuXG5leHBvcnQgY2xhc3MgU25hY2tiYXIge1xuICBpbml0KHN0b3JlKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBzdG9yZTtcbiAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgfVxuXG4gIGFsZXJ0KG1lc3NhZ2UsIHR5cGUpIHtcbiAgICBpZiAodGhpcy5fdGltZW91dCkge1xuICAgICAgd2luZG93LmNsZWFyVGltZW91dCh0aGlzLl90aW1lb3V0KTtcbiAgICAgIHRoaXMuX3N0b3JlLmRpc3BhdGNoKGhpZGVTbmFja2JhcigpKTtcblxuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fdGltZW91dCA9IG51bGw7XG4gICAgICAgIHRoaXMuYWxlcnQobWVzc2FnZSwgdHlwZSk7XG4gICAgICB9LCBISURFX0FOSU1BVElPTl9MRU5HVEgpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaG93U25hY2tiYXIobWVzc2FnZSwgdHlwZSkpO1xuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goaGlkZVNuYWNrYmFyKCkpO1xuICAgICAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgICAgIH0sIE1FU1NBR0VfU0hPV19MRU5HVEgpO1xuICAgIH1cbiAgfVxuXG4gIC8vIHNob3J0aGFuZHMgZm9yIG1lc3NhZ2UgdHlwZXNcblxuICBpbmZvKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdpbmZvJyk7XG4gIH1cblxuICBzdWNjZXNzKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdzdWNjZXNzJyk7XG4gIH1cblxuICB3YXJuaW5nKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICd3YXJuaW5nJyk7XG4gIH1cblxuICBlcnJvcihtZXNzYWdlKSB7XG4gICAgdGhpcy5hbGVydChtZXNzYWdlLCAnZXJyb3InKTtcbiAgfVxuXG4gIC8vIHNob3J0aGFuZCBmb3IgYXBpIGVycm9yc1xuXG4gIGFwaUVycm9yKHJlamVjdGlvbikge1xuICAgIGxldCBtZXNzYWdlID0gZ2V0dGV4dChcIlVua25vd24gZXJyb3IgaGFzIG9jY3VyZWQuXCIpO1xuXG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDApIHtcbiAgICAgIG1lc3NhZ2UgPSBnZXR0ZXh0KFwiTG9zdCBjb25uZWN0aW9uIHdpdGggYXBwbGljYXRpb24uXCIpO1xuICAgIH1cblxuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDAgJiYgcmVqZWN0aW9uLmRldGFpbCkge1xuICAgICAgbWVzc2FnZSA9IHJlamVjdGlvbi5kZXRhaWw7XG4gICAgfVxuXG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMykge1xuICAgICAgbWVzc2FnZSA9IHJlamVjdGlvbi5kZXRhaWw7XG4gICAgICBpZiAobWVzc2FnZSA9PT0gXCJQZXJtaXNzaW9uIGRlbmllZFwiKSB7XG4gICAgICAgIG1lc3NhZ2UgPSBnZXR0ZXh0KFxuICAgICAgICAgIFwiWW91IGRvbid0IGhhdmUgcGVybWlzc2lvbiB0byBwZXJmb3JtIHRoaXMgYWN0aW9uLlwiKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDA0KSB7XG4gICAgICBtZXNzYWdlID0gZ2V0dGV4dChcIkFjdGlvbiBsaW5rIGlzIGludmFsaWQuXCIpO1xuICAgIH1cblxuICAgIHRoaXMuZXJyb3IobWVzc2FnZSk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IFNuYWNrYmFyKCk7XG4iLCJpbXBvcnQgeyBjb21iaW5lUmVkdWNlcnMsIGNyZWF0ZVN0b3JlIH0gZnJvbSAncmVkdXgnO1xuXG5leHBvcnQgY2xhc3MgU3RvcmVXcmFwcGVyIHtcbiAgY29uc3RydWN0b3IoKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBudWxsO1xuICAgIHRoaXMuX3JlZHVjZXJzID0ge307XG4gICAgdGhpcy5faW5pdGlhbFN0YXRlID0ge307XG4gIH1cblxuICBhZGRSZWR1Y2VyKG5hbWUsIHJlZHVjZXIsIGluaXRpYWxTdGF0ZSkge1xuICAgIHRoaXMuX3JlZHVjZXJzW25hbWVdID0gcmVkdWNlcjtcbiAgICB0aGlzLl9pbml0aWFsU3RhdGVbbmFtZV0gPSBpbml0aWFsU3RhdGU7XG4gIH1cblxuICBpbml0KCkge1xuICAgIHRoaXMuX3N0b3JlID0gY3JlYXRlU3RvcmUoXG4gICAgICBjb21iaW5lUmVkdWNlcnModGhpcy5fcmVkdWNlcnMpLCB0aGlzLl9pbml0aWFsU3RhdGUpO1xuICB9XG5cbiAgZ2V0U3RvcmUoKSB7XG4gICAgcmV0dXJuIHRoaXMuX3N0b3JlO1xuICB9XG5cbiAgLy8gU3RvcmUgQVBJXG5cbiAgZ2V0U3RhdGUoKSB7XG4gICAgcmV0dXJuIHRoaXMuX3N0b3JlLmdldFN0YXRlKCk7XG4gIH1cblxuICBkaXNwYXRjaChhY3Rpb24pIHtcbiAgICByZXR1cm4gdGhpcy5fc3RvcmUuZGlzcGF0Y2goYWN0aW9uKTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgU3RvcmVXcmFwcGVyKCk7XG4iLCIvKiBnbG9iYWwgenhjdmJuICovXG5leHBvcnQgY2xhc3MgWnhjdmJuIHtcbiAgaW5pdChpbmNsdWRlKSB7XG4gICAgdGhpcy5faW5jbHVkZSA9IGluY2x1ZGU7XG4gIH1cblxuICBzY29yZVBhc3N3b3JkKHBhc3N3b3JkLCBpbnB1dHMpIHtcbiAgICAvLyAwLTQgc2NvcmUsIHRoZSBtb3JlIHRoZSBzdHJvbmdlciBwYXNzd29yZFxuICAgIHJldHVybiB6eGN2Ym4ocGFzc3dvcmQsIGlucHV0cykuc2NvcmU7XG4gIH1cblxuICBsb2FkKCkge1xuICAgIGlmICh0eXBlb2YgenhjdmJuID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgICB0aGlzLl9pbmNsdWRlLmluY2x1ZGUoJ21pc2Fnby9qcy96eGN2Ym4uanMnKTtcbiAgICAgIHJldHVybiB0aGlzLl9sb2FkaW5nUHJvbWlzZSgpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gdGhpcy5fbG9hZGVkUHJvbWlzZSgpO1xuICAgIH1cbiAgfVxuXG4gIF9sb2FkaW5nUHJvbWlzZSgpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoZnVuY3Rpb24ocmVzb2x2ZSkge1xuICAgICAgdmFyIHdhaXQgPSBmdW5jdGlvbigpIHtcbiAgICAgICAgaWYgKHR5cGVvZiB6eGN2Ym4gPT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICB3aW5kb3cuc2V0VGltZW91dChmdW5jdGlvbigpIHtcbiAgICAgICAgICAgIHdhaXQoKTtcbiAgICAgICAgICB9LCAyMDApO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJlc29sdmUoKTtcbiAgICAgICAgfVxuICAgICAgfTtcbiAgICAgIHdhaXQoKTtcbiAgICB9KTtcbiAgfVxuXG4gIF9sb2FkZWRQcm9taXNlKCkge1xuICAgIC8vIHdlIGhhdmUgYWxyZWFkeSBsb2FkZWQgenhjdmJuLmpzLCByZXNvbHZlIGF3YXkhXG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUpIHtcbiAgICAgIHJlc29sdmUoKTtcbiAgICB9KTtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgWnhjdmJuKCk7IiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5pbXBvcnQgeyBQcm92aWRlciwgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQmFubmVkUGFnZSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9iYW5uZWQtcGFnZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG4vKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG5sZXQgc2VsZWN0ID0gZnVuY3Rpb24oc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLnRpY2s7XG59O1xuXG5sZXQgUmVkcmF3ZWRCYW5uZWRQYWdlID0gY29ubmVjdChzZWxlY3QpKEJhbm5lZFBhZ2UpO1xuLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24oYmFuLCBjaGFuZ2VTdGF0ZSkge1xuICBSZWFjdERPTS5yZW5kZXIoXG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIDxQcm92aWRlciBzdG9yZT17c3RvcmUuZ2V0U3RvcmUoKX0+XG4gICAgICA8UmVkcmF3ZWRCYW5uZWRQYWdlIG1lc3NhZ2U9e2Jhbi5tZXNzYWdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICBleHBpcmVzPXtiYW4uZXhwaXJlc19vbiA/IG1vbWVudChiYW4uZXhwaXJlc19vbikgOiBudWxsfSAvPlxuICAgIDwvUHJvdmlkZXI+LFxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3BhZ2UtbW91bnQnKVxuICApO1xuXG4gIGlmICh0eXBlb2YgY2hhbmdlU3RhdGUgPT09ICd1bmRlZmluZWQnIHx8IGNoYW5nZVN0YXRlKSB7XG4gICAgbGV0IGZvcnVtTmFtZSA9IG1pc2Fnby5nZXQoJ1NFVFRJTkdTJykuZm9ydW1fbmFtZTtcbiAgICBkb2N1bWVudC50aXRsZSA9IGdldHRleHQoXCJZb3UgYXJlIGJhbm5lZFwiKSArICcgfCAnICsgZm9ydW1OYW1lO1xuICAgIHdpbmRvdy5oaXN0b3J5LnB1c2hTdGF0ZSh7fSwgXCJcIiwgbWlzYWdvLmdldCgnQkFOTkVEX1VSTCcpKTtcbiAgfVxufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5pbXBvcnQgeyBQcm92aWRlciB9IGZyb20gJ3JlYWN0LXJlZHV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uKENvbXBvbmVudCwgcm9vdEVsZW1lbnRJZCwgY29ubmVjdGVkPXRydWUpIHtcbiAgbGV0IHJvb3RFbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQocm9vdEVsZW1lbnRJZCk7XG5cbiAgaWYgKHJvb3RFbGVtZW50KSB7XG4gICAgaWYgKGNvbm5lY3RlZCkge1xuICAgICAgUmVhY3RET00ucmVuZGVyKFxuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICAgIDxQcm92aWRlciBzdG9yZT17c3RvcmUuZ2V0U3RvcmUoKX0+XG4gICAgICAgICAgPENvbXBvbmVudCAvPlxuICAgICAgICA8L1Byb3ZpZGVyPixcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICAgICAgcm9vdEVsZW1lbnRcbiAgICAgICk7XG4gICAgfSBlbHNlIHtcbiAgICAgIFJlYWN0RE9NLnJlbmRlcihcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgICA8Q29tcG9uZW50IC8+LFxuICAgICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgICByb290RWxlbWVudFxuICAgICAgKTtcbiAgICB9XG4gIH1cbn1cbiIsImNsYXNzIE9yZGVyZWRMaXN0IHtcbiAgICBjb25zdHJ1Y3RvcihpdGVtcykge1xuICAgICAgdGhpcy5pc09yZGVyZWQgPSBmYWxzZTtcbiAgICAgIHRoaXMuX2l0ZW1zID0gaXRlbXMgfHwgW107XG4gICAgfVxuXG4gICAgYWRkKGtleSwgaXRlbSwgb3JkZXIpIHtcbiAgICAgIHRoaXMuX2l0ZW1zLnB1c2goe1xuICAgICAgICBrZXk6IGtleSxcbiAgICAgICAgaXRlbTogaXRlbSxcblxuICAgICAgICBhZnRlcjogb3JkZXIgPyBvcmRlci5hZnRlciB8fCBudWxsIDogbnVsbCxcbiAgICAgICAgYmVmb3JlOiBvcmRlciA/IG9yZGVyLmJlZm9yZSB8fCBudWxsIDogbnVsbFxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgZ2V0KGtleSwgdmFsdWUpIHtcbiAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5faXRlbXMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgaWYgKHRoaXMuX2l0ZW1zW2ldLmtleSA9PT0ga2V5KSB7XG4gICAgICAgICAgcmV0dXJuIHRoaXMuX2l0ZW1zW2ldLml0ZW07XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHZhbHVlO1xuICAgIH1cblxuICAgIGhhcyhrZXkpIHtcbiAgICAgIHJldHVybiB0aGlzLmdldChrZXkpICE9PSB1bmRlZmluZWQ7XG4gICAgfVxuXG4gICAgdmFsdWVzKCkge1xuICAgICAgdmFyIHZhbHVlcyA9IFtdO1xuICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLl9pdGVtcy5sZW5ndGg7IGkrKykge1xuICAgICAgICB2YWx1ZXMucHVzaCh0aGlzLl9pdGVtc1tpXS5pdGVtKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiB2YWx1ZXM7XG4gICAgfVxuXG4gICAgb3JkZXIodmFsdWVzX29ubHkpIHtcbiAgICAgIGlmICghdGhpcy5pc09yZGVyZWQpIHtcbiAgICAgICAgdGhpcy5faXRlbXMgPSB0aGlzLl9vcmRlcih0aGlzLl9pdGVtcyk7XG4gICAgICAgIHRoaXMuaXNPcmRlcmVkID0gdHJ1ZTtcbiAgICAgIH1cblxuICAgICAgaWYgKHZhbHVlc19vbmx5IHx8IHR5cGVvZiB2YWx1ZXNfb25seSA9PT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMudmFsdWVzKCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gdGhpcy5faXRlbXM7XG4gICAgICB9XG4gICAgfVxuXG4gICAgb3JkZXJlZFZhbHVlcygpIHtcbiAgICAgIHJldHVybiB0aGlzLm9yZGVyKHRydWUpO1xuICAgIH1cblxuICAgIF9vcmRlcih1bm9yZGVyZWQpIHtcbiAgICAgIC8vIEluZGV4IG9mIHVub3JkZXJlZCBpdGVtc1xuICAgICAgdmFyIGluZGV4ID0gW107XG4gICAgICB1bm9yZGVyZWQuZm9yRWFjaChmdW5jdGlvbiAoaXRlbSkge1xuICAgICAgICBpbmRleC5wdXNoKGl0ZW0ua2V5KTtcbiAgICAgIH0pO1xuXG4gICAgICAvLyBPcmRlcmVkIGl0ZW1zXG4gICAgICB2YXIgb3JkZXJlZCA9IFtdO1xuICAgICAgdmFyIG9yZGVyaW5nID0gW107XG5cbiAgICAgIC8vIEZpcnN0IHBhc3M6IHJlZ2lzdGVyIGl0ZW1zIHRoYXRcbiAgICAgIC8vIGRvbid0IHNwZWNpZnkgdGhlaXIgb3JkZXJcbiAgICAgIHVub3JkZXJlZC5mb3JFYWNoKGZ1bmN0aW9uIChpdGVtKSB7XG4gICAgICAgIGlmICghaXRlbS5hZnRlciAmJiAhaXRlbS5iZWZvcmUpIHtcbiAgICAgICAgICBvcmRlcmVkLnB1c2goaXRlbSk7XG4gICAgICAgICAgb3JkZXJpbmcucHVzaChpdGVtLmtleSk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuXG4gICAgICAvLyBTZWNvbmQgcGFzczogcmVnaXN0ZXIgaXRlbXMgdGhhdFxuICAgICAgLy8gc3BlY2lmeSB0aGVpciBiZWZvcmUgdG8gXCJfZW5kXCJcbiAgICAgIHVub3JkZXJlZC5mb3JFYWNoKGZ1bmN0aW9uIChpdGVtKSB7XG4gICAgICAgIGlmIChpdGVtLmJlZm9yZSA9PT0gXCJfZW5kXCIpIHtcbiAgICAgICAgICBvcmRlcmVkLnB1c2goaXRlbSk7XG4gICAgICAgICAgb3JkZXJpbmcucHVzaChpdGVtLmtleSk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuXG4gICAgICAvLyBUaGlyZCBwYXNzOiBrZWVwIGl0ZXJhdGluZyBpdGVtc1xuICAgICAgLy8gdW50aWwgd2UgaGl0IGl0ZXJhdGlvbnMgbGltaXQgb3IgZmluaXNoXG4gICAgICAvLyBvcmRlcmluZyBsaXN0XG4gICAgICBmdW5jdGlvbiBpbnNlcnRJdGVtKGl0ZW0pIHtcbiAgICAgICAgdmFyIGluc2VydEF0ID0gLTE7XG4gICAgICAgIGlmIChvcmRlcmluZy5pbmRleE9mKGl0ZW0ua2V5KSA9PT0gLTEpIHtcbiAgICAgICAgICBpZiAoaXRlbS5hZnRlcikge1xuICAgICAgICAgICAgaW5zZXJ0QXQgPSBvcmRlcmluZy5pbmRleE9mKGl0ZW0uYWZ0ZXIpO1xuICAgICAgICAgICAgaWYgKGluc2VydEF0ICE9PSAtMSkge1xuICAgICAgICAgICAgICBpbnNlcnRBdCArPSAxO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0gZWxzZSBpZiAoaXRlbS5iZWZvcmUpIHtcbiAgICAgICAgICAgIGluc2VydEF0ID0gb3JkZXJpbmcuaW5kZXhPZihpdGVtLmJlZm9yZSk7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgaWYgKGluc2VydEF0ICE9PSAtMSkge1xuICAgICAgICAgICAgb3JkZXJlZC5zcGxpY2UoaW5zZXJ0QXQsIDAsIGl0ZW0pO1xuICAgICAgICAgICAgb3JkZXJpbmcuc3BsaWNlKGluc2VydEF0LCAwLCBpdGVtLmtleSk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIHZhciBpdGVyYXRpb25zID0gMjAwO1xuICAgICAgd2hpbGUgKGl0ZXJhdGlvbnMgPiAwICYmIGluZGV4Lmxlbmd0aCAhPT0gb3JkZXJpbmcubGVuZ3RoKSB7XG4gICAgICAgIGl0ZXJhdGlvbnMgLT0gMTtcbiAgICAgICAgdW5vcmRlcmVkLmZvckVhY2goaW5zZXJ0SXRlbSk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBvcmRlcmVkO1xuICAgIH1cbiAgfVxuXG4gIGV4cG9ydCBkZWZhdWx0IE9yZGVyZWRMaXN0O1xuIiwiY29uc3QgRU1BSUwgPSAvXigoW148PigpW1xcXVxcLiw7Olxcc0BcXFwiXSsoXFwuW148PigpW1xcXVxcLiw7Olxcc0BcXFwiXSspKil8KFxcXCIuK1xcXCIpKUAoKFtePD4oKVtcXF1cXC4sOzpcXHNAXFxcIl0rXFwuKStbXjw+KClbXFxdXFwuLDs6XFxzQFxcXCJdezIsfSkkL2k7XG5jb25zdCBVU0VSTkFNRSA9IG5ldyBSZWdFeHAoJ15bMC05YS16XSskJywgJ2knKTtcblxuZXhwb3J0IGZ1bmN0aW9uIHJlcXVpcmVkKCkge1xuICByZXR1cm4gZnVuY3Rpb24odmFsdWUpIHtcbiAgICBpZiAoJC50cmltKHZhbHVlKS5sZW5ndGggPT09IDApIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiVGhpcyBmaWVsZCBpcyByZXF1aXJlZC5cIik7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gZW1haWwobWVzc2FnZSkge1xuICByZXR1cm4gZnVuY3Rpb24odmFsdWUpIHtcbiAgICBpZiAoIUVNQUlMLnRlc3QodmFsdWUpKSB7XG4gICAgICByZXR1cm4gbWVzc2FnZSB8fCBnZXR0ZXh0KFwiRW50ZXIgYSB2YWxpZCBlbWFpbCBhZGRyZXNzLlwiKTtcbiAgICB9XG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBtaW5MZW5ndGgobGltaXRWYWx1ZSwgbWVzc2FnZSkge1xuICByZXR1cm4gZnVuY3Rpb24odmFsdWUpIHtcbiAgICB2YXIgcmV0dXJuTWVzc2FnZSA9ICcnO1xuICAgIHZhciBsZW5ndGggPSAkLnRyaW0odmFsdWUpLmxlbmd0aDtcblxuICAgIGlmIChsZW5ndGggPCBsaW1pdFZhbHVlKSB7XG4gICAgICBpZiAobWVzc2FnZSkge1xuICAgICAgICByZXR1cm5NZXNzYWdlID0gbWVzc2FnZShsaW1pdFZhbHVlLCBsZW5ndGgpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG5nZXR0ZXh0KFxuICAgICAgICAgIFwiRW5zdXJlIHRoaXMgdmFsdWUgaGFzIGF0IGxlYXN0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXIgKGl0IGhhcyAlKHNob3dfdmFsdWUpcykuXCIsXG4gICAgICAgICAgXCJFbnN1cmUgdGhpcyB2YWx1ZSBoYXMgYXQgbGVhc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMgKGl0IGhhcyAlKHNob3dfdmFsdWUpcykuXCIsXG4gICAgICAgICAgbGltaXRWYWx1ZSk7XG4gICAgICB9XG4gICAgICByZXR1cm4gaW50ZXJwb2xhdGUocmV0dXJuTWVzc2FnZSwge1xuICAgICAgICBsaW1pdF92YWx1ZTogbGltaXRWYWx1ZSxcbiAgICAgICAgc2hvd192YWx1ZTogbGVuZ3RoXG4gICAgICB9LCB0cnVlKTtcbiAgICB9XG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBtYXhMZW5ndGgobGltaXRWYWx1ZSwgbWVzc2FnZSkge1xuICByZXR1cm4gZnVuY3Rpb24odmFsdWUpIHtcbiAgICB2YXIgcmV0dXJuTWVzc2FnZSA9ICcnO1xuICAgIHZhciBsZW5ndGggPSAkLnRyaW0odmFsdWUpLmxlbmd0aDtcblxuICAgIGlmIChsZW5ndGggPiBsaW1pdFZhbHVlKSB7XG4gICAgICBpZiAobWVzc2FnZSkge1xuICAgICAgICByZXR1cm5NZXNzYWdlID0gbWVzc2FnZShsaW1pdFZhbHVlLCBsZW5ndGgpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG5nZXR0ZXh0KFxuICAgICAgICAgIFwiRW5zdXJlIHRoaXMgdmFsdWUgaGFzIGF0IG1vc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlciAoaXQgaGFzICUoc2hvd192YWx1ZSlzKS5cIixcbiAgICAgICAgICBcIkVuc3VyZSB0aGlzIHZhbHVlIGhhcyBhdCBtb3N0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXJzIChpdCBoYXMgJShzaG93X3ZhbHVlKXMpLlwiLFxuICAgICAgICAgIGxpbWl0VmFsdWUpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGludGVycG9sYXRlKHJldHVybk1lc3NhZ2UsIHtcbiAgICAgICAgbGltaXRfdmFsdWU6IGxpbWl0VmFsdWUsXG4gICAgICAgIHNob3dfdmFsdWU6IGxlbmd0aFxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlcm5hbWVNaW5MZW5ndGgoc2V0dGluZ3MpIHtcbiAgdmFyIG1lc3NhZ2UgPSBmdW5jdGlvbihsaW1pdFZhbHVlKSB7XG4gICAgcmV0dXJuIG5nZXR0ZXh0KFxuICAgICAgXCJVc2VybmFtZSBtdXN0IGJlIGF0IGxlYXN0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXIgbG9uZy5cIixcbiAgICAgIFwiVXNlcm5hbWUgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVycyBsb25nLlwiLFxuICAgICAgbGltaXRWYWx1ZSk7XG4gIH07XG4gIHJldHVybiB0aGlzLm1pbkxlbmd0aChzZXR0aW5ncy51c2VybmFtZV9sZW5ndGhfbWluLCBtZXNzYWdlKTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVzZXJuYW1lTWF4TGVuZ3RoKHNldHRpbmdzKSB7XG4gIHZhciBtZXNzYWdlID0gZnVuY3Rpb24obGltaXRWYWx1ZSkge1xuICAgIHJldHVybiBuZ2V0dGV4dChcbiAgICAgIFwiVXNlcm5hbWUgY2Fubm90IGJlIGxvbmdlciB0aGFuICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXIuXCIsXG4gICAgICBcIlVzZXJuYW1lIGNhbm5vdCBiZSBsb25nZXIgdGhhbiAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVycy5cIixcbiAgICAgIGxpbWl0VmFsdWUpO1xuICB9O1xuICByZXR1cm4gdGhpcy5tYXhMZW5ndGgoc2V0dGluZ3MudXNlcm5hbWVfbGVuZ3RoX21heCwgbWVzc2FnZSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VybmFtZUNvbnRlbnQoKSB7XG4gIHJldHVybiBmdW5jdGlvbih2YWx1ZSkge1xuICAgIGlmICghVVNFUk5BTUUudGVzdCgkLnRyaW0odmFsdWUpKSkge1xuICAgICAgcmV0dXJuIGdldHRleHQoXCJVc2VybmFtZSBjYW4gb25seSBjb250YWluIGxhdGluIGFscGhhYmV0IGxldHRlcnMgYW5kIGRpZ2l0cy5cIik7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcGFzc3dvcmRNaW5MZW5ndGgoc2V0dGluZ3MpIHtcbiAgdmFyIG1lc3NhZ2UgPSBmdW5jdGlvbihsaW1pdFZhbHVlKSB7XG4gICAgcmV0dXJuIG5nZXR0ZXh0KFxuICAgICAgXCJWYWxpZCBwYXNzd29yZCBtdXN0IGJlIGF0IGxlYXN0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXIgbG9uZy5cIixcbiAgICAgIFwiVmFsaWQgcGFzc3dvcmQgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVycyBsb25nLlwiLFxuICAgICAgbGltaXRWYWx1ZSk7XG4gIH07XG4gIHJldHVybiB0aGlzLm1pbkxlbmd0aChzZXR0aW5ncy5wYXNzd29yZF9sZW5ndGhfbWluLCBtZXNzYWdlKTtcbn0iXX0=
