(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

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

var _class = (function (_React$Component) {
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
})(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],2:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

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

var _class = (function (_React$Component) {
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
          return interpolate(gettext('This ban expires %(expires_on)s.'), { 'expires_on': this.props.expires.fromNow() }, true);
        } else {
          return gettext('This ban has expired.');
        }
      } else {
        return gettext('This ban is permanent.');
      }
    }
  }, {
    key: 'render',
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement(
        'div',
        { className: 'page page-error page-error-baned' },
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
                null,
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
})(_react2.default.Component);

exports.default = _class;

},{"moment":"moment","react":"react"}],3:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

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

var Button = (function (_React$Component) {
  _inherits(Button, _React$Component);

  function Button() {
    _classCallCheck(this, Button);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(Button).apply(this, arguments));
  }

  _createClass(Button, [{
    key: 'render',
    value: function render() {
      var content = null;
      var className = 'btn ' + this.props.className;
      var disabled = this.props.disabled;

      if (this.props.loading) {
        /* jshint ignore:start */
        content = _react2.default.createElement(_loader2.default, null);
        /* jshint ignore:end */
        className += ' btn-loading';
        disabled = true;
      } else {
        content = this.props.children;
      }

      /* jshint ignore:start */
      return _react2.default.createElement(
        'button',
        { type: this.props.onClick ? 'button' : 'submit',
          className: className,
          disabled: disabled,
          onClick: this.props.onClick },
        content
      );
      /* jshint ignore:end */
    }
  }]);

  return Button;
})(_react2.default.Component);

exports.default = Button;

Button.defaultProps = {
  className: "btn-default",

  type: "submit",

  loading: false,
  disabled: false,

  onClick: null
};

},{"./loader":5,"react":"react"}],4:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

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

var _class = (function (_React$Component) {
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
            _this.handleSuccess(success);
            _this.setState({ 'isLoading': false });
          }, function (rejection) {
            _this.handleError(rejection);
            _this.setState({ 'isLoading': false });
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
      var isValid = true;
      var errors = {};

      for (var key in this.state.validators) {
        if (this.state.validators.hasOwnProperty(key)) {
          var value = this.state[key];
          errors[key] = this.validateField(value, this.state.validators[key]);
          if (errors[key] !== null) {
            isValid = false;
          }
        }
      }

      return isValid ? null : errors;
    }
  }, {
    key: 'validateField',
    value: function validateField(value, validators) {
      var result = (0, _validators.required)()(value);
      var errors = [];

      if (result) {
        return [result];
      } else {
        for (var i in validators) {
          result = validators[i](value);
          if (result) {
            errors.push(result);
          }
        }
      }

      return errors.length ? errors : null;
    }
  }, {
    key: 'changeValue',
    value: function changeValue(name, value) {
      var errors = null;
      if (this.state.validators.name) {
        errors = this.validateField(name, value);
      }
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
})(_react2.default.Component);

exports.default = _class;

},{"../utils/validators":36,"react":"react"}],5:[function(require,module,exports){
"use strict";

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = (function (_React$Component) {
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
        { className: "loader-compact" },
        _react2.default.createElement("div", { className: "loader-spinning-wheel" })
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
})(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],6:[function(require,module,exports){
"use strict";

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _class = (function (_React$Component) {
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
        { className: "modal-dialog modal-register" },
        _react2.default.createElement(
          "div",
          { className: "modal-content" },
          _react2.default.createElement(
            "div",
            { className: "modal-header" },
            _react2.default.createElement(
              "button",
              { type: "button", className: "close", "data-dismiss": "modal", "aria-label": "Close" },
              _react2.default.createElement(
                "span",
                { "aria-hidden": "true" },
                "×"
              )
            ),
            _react2.default.createElement(
              "h4",
              { className: "modal-title" },
              gettext("Register")
            )
          ),
          _react2.default.createElement(
            "div",
            { className: "modal-body" },
            _react2.default.createElement(
              "p",
              null,
              "This will be registration form!"
            )
          ),
          _react2.default.createElement(
            "div",
            { className: "modal-footer" },
            _react2.default.createElement(
              "button",
              { type: "button", className: "btn btn-default", "data-dismiss": "modal" },
              "Close"
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return _class;
})(_react2.default.Component);

exports.default = _class;

},{"react":"react"}],7:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

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

var _class = (function (_Form) {
  _inherits(_class, _Form);

  function _class(props) {
    _classCallCheck(this, _class);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(_class).call(this, props));

    _this.state = {
      'isLoading': false,
      'showActivation': false,

      'username': '',
      'password': '',

      validators: {
        'username': [],
        'password': []
      }
    };
    return _this;
  }

  _createClass(_class, [{
    key: 'clean',
    value: function clean() {
      if (this.validate()) {
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
      _modal2.default.hide();

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
        { className: 'modal-dialog modal-sm modal-sign-in' },
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
})(_form2.default);

exports.default = _class;

},{"../index":12,"../services/ajax":28,"../services/modal":30,"../services/snackbar":31,"../utils/banned-page":33,"./button":3,"./form":4,"react":"react"}],8:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

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

var Snackbar = exports.Snackbar = (function (_React$Component) {
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
})(_react2.default.Component);

function select(state) {
  return state.snackbar;
}

},{"react":"react"}],9:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.CompactGuestNav = exports.GuestNav = exports.GuestMenu = undefined;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _button = require('../button');

var _button2 = _interopRequireDefault(_button);

var _modal = require('../../services/modal');

var _modal2 = _interopRequireDefault(_modal);

var _mobileNavbarDropdown = require('../../services/mobile-navbar-dropdown');

var _mobileNavbarDropdown2 = _interopRequireDefault(_mobileNavbarDropdown);

var _avatar = require('../avatar');

var _avatar2 = _interopRequireDefault(_avatar);

var _signIn = require('../sign-in.js');

var _signIn2 = _interopRequireDefault(_signIn);

var _root = require('../register/root.js');

var _root2 = _interopRequireDefault(_root);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line

// jshint ignore:line

var GuestMenu = exports.GuestMenu = (function (_React$Component) {
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
    key: 'showRegisterModal',
    value: function showRegisterModal() {
      _modal2.default.show(_root2.default);
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
                { type: 'button', className: 'btn btn-default btn-block' },
                'Thy Sign In'
              )
            ),
            _react2.default.createElement(
              'div',
              { className: 'col-xs-6' },
              _react2.default.createElement(
                'button',
                { type: 'button', className: 'btn btn-primary btn-block' },
                'Thy Registry'
              )
            )
          )
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return GuestMenu;
})(_react2.default.Component);

var GuestNav = exports.GuestNav = (function (_GuestMenu) {
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
          _button2.default,
          { type: 'button',
            className: 'navbar-btn btn-default',
            onClick: this.showSignInModal },
          'Sign in'
        ),
        _react2.default.createElement(
          _button2.default,
          { type: 'button',
            className: 'navbar-btn btn-primary',
            onClick: this.showRegisterModal },
          'Register'
        )
      );
      /* jshint ignore:end */
    }
  }]);

  return GuestNav;
})(GuestMenu);

var CompactGuestNav = exports.CompactGuestNav = (function (_React$Component2) {
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
})(_react2.default.Component);

},{"../../services/mobile-navbar-dropdown":29,"../../services/modal":30,"../avatar":1,"../button":3,"../register/root.js":6,"../sign-in.js":7,"react":"react"}],10:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.CompactUserMenu = exports.UserMenu = undefined;
exports.select = select;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _guestNav = require('./guest-nav');

var _userNav = require('./user-nav');

var _userNav2 = _interopRequireDefault(_userNav);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // jshint ignore:line

// jshint ignore:line

var UserMenu = exports.UserMenu = (function (_React$Component) {
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
        return _react2.default.createElement(_userNav2.default, { user: this.props.user });
      } else {
        return _react2.default.createElement(_guestNav.GuestNav, null);
      }
      /* jshint ignore:end */
    }
  }]);

  return UserMenu;
})(_react2.default.Component);

var CompactUserMenu = exports.CompactUserMenu = (function (_React$Component2) {
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
        return _react2.default.createElement(_userNav2.default, { user: this.props.user });
      } else {
        return _react2.default.createElement(_guestNav.CompactGuestNav, null);
      }
      /* jshint ignore:end */
    }
  }]);

  return CompactUserMenu;
})(_react2.default.Component);

function select(state) {
  return state.auth;
}

},{"./guest-nav":9,"./user-nav":11,"react":"react"}],11:[function(require,module,exports){
"use strict";

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var UserNav = (function (_React$Component) {
  _inherits(UserNav, _React$Component);

  function UserNav() {
    _classCallCheck(this, UserNav);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(UserNav).apply(this, arguments));
  }

  _createClass(UserNav, [{
    key: "render",
    value: function render() {
      /* jshint ignore:start */
      return _react2.default.createElement("ul", { "class": "ul nav navbar-nav nav-user" });
      /* jshint ignore:end */
    }
  }]);

  return UserNav;
})(_react2.default.Component);

exports.default = UserNav;

},{"react":"react"}],12:[function(require,module,exports){
(function (global){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Misago = undefined;

var _orderedList = require('./utils/ordered-list');

var _orderedList2 = _interopRequireDefault(_orderedList);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Misago = exports.Misago = (function () {
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
})();

// create  singleton

var misago = new Misago();

// expose it globally
global.misago = misago;

// and export it for tests and stuff
exports.default = misago;

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{"./utils/ordered-list":35}],13:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _ajax = require('../services/ajax');

var _ajax2 = _interopRequireDefault(_ajax);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _ajax2.default.init(_index2.default.get('CSRF_COOKIE_NAME'));
}

_index2.default.addInitializer({
  name: 'ajax',
  initializer: initializer
});

},{"../index":12,"../services/ajax":28}],14:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _auth = require('../reducers/auth');

var _auth2 = _interopRequireDefault(_auth);

var _store = require('../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer(context) {
  _store2.default.addReducer('auth', _auth2.default, {
    'isAuthenticated': context.get('isAuthenticated'),
    'isAnonymous': !context.get('isAuthenticated'),

    'user': context.get('user')
  });
}

_index2.default.addInitializer({
  name: 'reducer:auth',
  initializer: initializer,
  before: 'store'
});

},{"../index":12,"../reducers/auth":25,"../services/store":32}],15:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _mobileNavbarDropdown = require('../services/mobile-navbar-dropdown');

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

},{"../index":12,"../services/mobile-navbar-dropdown":29}],16:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _modal = require('../services/modal');

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

},{"../index":12,"../services/modal":30}],17:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function initializer() {
  _moment2.default.locale($('html').attr('lang'));
}

_index2.default.addInitializer({
  name: 'moment',
  initializer: initializer
});

},{"../index":12,"moment":"moment"}],18:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _reactRedux = require('react-redux');

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _snackbar = require('../components/snackbar');

var _mountComponent = require('../utils/mount-component');

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

},{"../components/snackbar":8,"../index":12,"../utils/mount-component":34,"react-redux":"react-redux"}],19:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _snackbar = require('../reducers/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _store = require('../services/store');

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

},{"../index":12,"../reducers/snackbar":26,"../services/store":32}],20:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _snackbar = require('../services/snackbar');

var _snackbar2 = _interopRequireDefault(_snackbar);

var _store = require('../services/store');

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

},{"../index":12,"../services/snackbar":31,"../services/store":32}],21:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _store = require('../services/store');

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

},{"../index":12,"../services/store":32}],22:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _tick = require('../reducers/tick');

var _tick2 = _interopRequireDefault(_tick);

var _store = require('../services/store');

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

},{"../index":12,"../reducers/tick":27,"../services/store":32}],23:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _tick = require('../reducers/tick');

var _store = require('../services/store');

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

},{"../index":12,"../reducers/tick":27,"../services/store":32}],24:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = initializer;

var _reactRedux = require('react-redux');

var _index = require('../index');

var _index2 = _interopRequireDefault(_index);

var _root = require('../components/user-menu/root');

var _mountComponent = require('../utils/mount-component');

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

},{"../components/user-menu/root":10,"../index":12,"../utils/mount-component":34,"react-redux":"react-redux"}],25:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = auth;
function auth() {
  var state = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];
  var action = arguments.length <= 1 || arguments[1] === undefined ? null : arguments[1];

  return state;
}

},{}],26:[function(require,module,exports){
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

},{}],27:[function(require,module,exports){
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

},{}],28:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Ajax = exports.Ajax = (function () {
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
})();

exports.default = new Ajax();

},{}],29:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.MobileNavbarDropdown = undefined;

var _mountComponent = require('../utils/mount-component');

var _mountComponent2 = _interopRequireDefault(_mountComponent);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var MobileNavbarDropdown = exports.MobileNavbarDropdown = (function () {
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
    key: 'hide',
    value: function hide() {
      $(this._element).removeClass('open');
      this._component = null;
    }
  }]);

  return MobileNavbarDropdown;
})();

exports.default = new MobileNavbarDropdown();

},{"../utils/mount-component":34}],30:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

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

var Modal = exports.Modal = (function () {
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
})();

exports.default = new Modal();

},{"../utils/mount-component":34,"react-dom":"react-dom"}],31:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Snackbar = undefined;

var _snackbar = require('../reducers/snackbar');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var HIDE_ANIMATION_LENGTH = 300;
var MESSAGE_SHOW_LENGTH = 5000;

var Snackbar = exports.Snackbar = (function () {
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
})();

exports.default = new Snackbar();

},{"../reducers/snackbar":26}],32:[function(require,module,exports){
'use strict';

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.StoreWrapper = undefined;

var _redux = require('redux');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var StoreWrapper = exports.StoreWrapper = (function () {
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
})();

exports.default = new StoreWrapper();

},{"redux":"redux"}],33:[function(require,module,exports){
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

  if (typeof changeState === 'undefined' || !changeState) {
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

},{"../components/banned-page":2,"../index":12,"../services/store":32,"moment":"moment","react":"react","react-dom":"react-dom","react-redux":"react-redux"}],34:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = mount;

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _reactRedux = require('react-redux');

var _store = require('../services/store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// jshint ignore:line

function mount(Component, rootElementId) {
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
} // jshint ignore:line
// jshint ignore:line

},{"../services/store":32,"react":"react","react-dom":"react-dom","react-redux":"react-redux"}],35:[function(require,module,exports){
"use strict";

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

Object.defineProperty(exports, "__esModule", {
  value: true
});

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var OrderedList = (function () {
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
})();

exports.default = OrderedList;

},{}],36:[function(require,module,exports){
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

},{}]},{},[12,13,14,15,16,17,18,19,20,21,22,23,24])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzcmMvY29tcG9uZW50cy9hdmF0YXIuanMiLCJzcmMvY29tcG9uZW50cy9iYW5uZWQtcGFnZS5qcyIsInNyYy9jb21wb25lbnRzL2J1dHRvbi5qcyIsInNyYy9jb21wb25lbnRzL2Zvcm0uanMiLCJzcmMvY29tcG9uZW50cy9sb2FkZXIuanMiLCJzcmMvY29tcG9uZW50cy9yZWdpc3Rlci9yb290LmpzIiwic3JjL2NvbXBvbmVudHMvc2lnbi1pbi5qcyIsInNyYy9jb21wb25lbnRzL3NuYWNrYmFyLmpzIiwic3JjL2NvbXBvbmVudHMvdXNlci1tZW51L2d1ZXN0LW5hdi5qcyIsInNyYy9jb21wb25lbnRzL3VzZXItbWVudS9yb290LmpzIiwic3JjL2NvbXBvbmVudHMvdXNlci1tZW51L3VzZXItbmF2LmpzIiwic3JjL2luZGV4LmpzIiwic3JjL2luaXRpYWxpemVycy9hamF4LmpzIiwic3JjL2luaXRpYWxpemVycy9hdXRoLXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL21vYmlsZS1uYXZiYXItZHJvcGRvd24uanMiLCJzcmMvaW5pdGlhbGl6ZXJzL21vZGFsLmpzIiwic3JjL2luaXRpYWxpemVycy9tb21lbnQtbG9jYWxlLmpzIiwic3JjL2luaXRpYWxpemVycy9zbmFja2Jhci1jb21wb25lbnQuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3NuYWNrYmFyLXJlZHVjZXIuanMiLCJzcmMvaW5pdGlhbGl6ZXJzL3NuYWNrYmFyLmpzIiwic3JjL2luaXRpYWxpemVycy9zdG9yZS5qcyIsInNyYy9pbml0aWFsaXplcnMvdGljay1yZWR1Y2VyLmpzIiwic3JjL2luaXRpYWxpemVycy90aWNrLXN0YXJ0LmpzIiwic3JjL2luaXRpYWxpemVycy91c2VyLW1lbnUtY29tcG9uZW50LmpzIiwic3JjL3JlZHVjZXJzL2F1dGguanMiLCJzcmMvcmVkdWNlcnMvc25hY2tiYXIuanMiLCJzcmMvcmVkdWNlcnMvdGljay5qcyIsInNyYy9zZXJ2aWNlcy9hamF4LmpzIiwic3JjL3NlcnZpY2VzL21vYmlsZS1uYXZiYXItZHJvcGRvd24uanMiLCJzcmMvc2VydmljZXMvbW9kYWwuanMiLCJzcmMvc2VydmljZXMvc25hY2tiYXIuanMiLCJzcmMvc2VydmljZXMvc3RvcmUuanMiLCJzcmMvdXRpbHMvYmFubmVkLXBhZ2UuanMiLCJzcmMvdXRpbHMvbW91bnQtY29tcG9uZW50LmpzIiwic3JjL3V0aWxzL29yZGVyZWQtbGlzdC5qcyIsInNyYy91dGlscy92YWxpZGF0b3JzLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNFQSxJQUFNLFFBQVEsR0FBRyxDQUFDLENBQUMsTUFBTSxDQUFDLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxHQUFHLGNBQWMsQ0FBQzs7Ozs7Ozs7Ozs7Ozs2QkFHOUM7QUFDUCxVQUFJLElBQUksR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDLElBQUksSUFBSSxHQUFHO0FBQUMsQUFDbEMsVUFBSSxHQUFHLEdBQUcsUUFBUSxDQUFDOztBQUVuQixVQUFJLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxJQUFJLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLEVBQUUsRUFBRTs7QUFFekMsV0FBRyxJQUFJLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLFdBQVcsR0FBRyxHQUFHLEdBQUcsSUFBSSxHQUFHLEdBQUcsR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxFQUFFLEdBQUcsTUFBTSxDQUFDO09BQ3JGLE1BQU07O0FBRUwsV0FBRyxJQUFJLElBQUksR0FBRyxNQUFNLENBQUM7T0FDdEI7O0FBRUQsYUFBTyxHQUFHLENBQUM7S0FDWjs7OzZCQUVROztBQUVQLGFBQU8sdUNBQUssR0FBRyxFQUFFLElBQUksQ0FBQyxNQUFNLEVBQUUsQUFBQztBQUNuQixpQkFBUyxFQUFFLElBQUksQ0FBQyxLQUFLLENBQUMs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QW1CLEVBQUUsT0FBTyxDQUFDLENBQUM7Q0FDOUQiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiBlKHQsbixyKXtmdW5jdGlvbiBzKG8sdSl7aWYoIW5bb10pe2lmKCF0W29dKXt2YXIgYT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2lmKCF1JiZhKXJldHVybiBhKG8sITApO2lmKGkpcmV0dXJuIGkobywhMCk7dmFyIGY9bmV3IEVycm9yKFwiQ2Fubm90IGZpbmQgbW9kdWxlICdcIitvK1wiJ1wiKTt0aHJvdyBmLmNvZGU9XCJNT0RVTEVfTk9UX0ZPVU5EXCIsZn12YXIgbD1uW29dPXtleHBvcnRzOnt9fTt0W29dWzBdLmNhbGwobC5leHBvcnRzLGZ1bmN0aW9uKGUpe3ZhciBuPXRbb11bMV1bZV07cmV0dXJuIHMobj9uOmUpfSxsLGwuZXhwb3J0cyxlLHQsbixyKX1yZXR1cm4gbltvXS5leHBvcnRzfXZhciBpPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7Zm9yKHZhciBvPTA7bzxyLmxlbmd0aDtvKyspcyhyW29dKTtyZXR1cm4gc30pIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuY29uc3QgQkFTRV9VUkwgPSAkKCdiYXNlJykuYXR0cignaHJlZicpICsgJ3VzZXItYXZhdGFyLyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgZ2V0U3JjKCkge1xuICAgIGxldCBzaXplID0gdGhpcy5wcm9wcy5zaXplIHx8IDEwMDsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG4gICAgbGV0IHVybCA9IEJBU0VfVVJMO1xuXG4gICAgaWYgKHRoaXMucHJvcHMudXNlciAmJiB0aGlzLnByb3BzLnVzZXIuaWQpIHtcbiAgICAgIC8vIGp1c3QgYXZhdGFyIGhhc2gsIHNpemUgYW5kIHVzZXIgaWRcbiAgICAgIHVybCArPSB0aGlzLnByb3BzLnVzZXIuYXZhdGFyX2hhc2ggKyAnLycgKyBzaXplICsgJy8nICsgdGhpcy5wcm9wcy51c2VyLmlkICsgJy5wbmcnO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBqdXN0IGFwcGVuZCBhdmF0YXIgc2l6ZSB0byBmaWxlIHRvIHByb2R1Y2Ugbm8tYXZhdGFyIHBsYWNlaG9sZGVyXG4gICAgICB1cmwgKz0gc2l6ZSArICcucG5nJztcbiAgICB9XG5cbiAgICByZXR1cm4gdXJsO1xuICB9XG5cbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGltZyBzcmM9e3RoaXMuZ2V0U3JjKCl9XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lPXt0aGlzLnByb3BzLmNsYXNzTmFtZSB8fCAndXNlci1hdmF0YXInfVxuICAgICAgICAgICAgICAgIHRpdGxlPXtnZXR0ZXh0KFwiVXNlciBhdmF0YXJcIil9Lz47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRSZWFzb25NZXNzYWdlKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICBpZiAodGhpcy5wcm9wcy5tZXNzYWdlLmh0bWwpIHtcbiAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImxlYWRcIlxuICAgICAgICAgICAgICAgICAgZGFuZ2Vyb3VzbHlTZXRJbm5lckhUTUw9e3tfX2h0bWw6IHRoaXMucHJvcHMubWVzc2FnZS5odG1sfX0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8cCBjbGFzc05hbWU9XCJsZWFkXCI+e3RoaXMucHJvcHMubWVzc2FnZS5wbGFpbn08L3A+O1xuICAgIH1cbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG5cbiAgZ2V0RXhwaXJhdGlvbk1lc3NhZ2UoKSB7XG4gICAgaWYgKHRoaXMucHJvcHMuZXhwaXJlcykge1xuICAgICAgaWYgKHRoaXMucHJvcHMuZXhwaXJlcy5pc0FmdGVyKG1vbWVudCgpKSkge1xuICAgICAgICByZXR1cm4gaW50ZXJwb2xhdGUoXG4gICAgICAgICAgZ2V0dGV4dCgnVGhpcyBiYW4gZXhwaXJlcyAlKGV4cGlyZXNfb24pcy4nKSxcbiAgICAgICAgICB7J2V4cGlyZXNfb24nOiB0aGlzLnByb3BzLmV4cGlyZXMuZnJvbU5vdygpfSxcbiAgICAgICAgICB0cnVlKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBnZXR0ZXh0KCdUaGlzIGJhbiBoYXMgZXhwaXJlZC4nKTtcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIGdldHRleHQoJ1RoaXMgYmFuIGlzIHBlcm1hbmVudC4nKTtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cInBhZ2UgcGFnZS1lcnJvciBwYWdlLWVycm9yLWJhbmVkXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiPlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtcGFuZWxcIj5cblxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibWVzc2FnZS1pY29uXCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9XCJtYXRlcmlhbC1pY29uXCI+aGlnaGxpZ2h0X29mZjwvc3Bhbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1lc3NhZ2UtYm9keVwiPlxuICAgICAgICAgICAge3RoaXMuZ2V0UmVhc29uTWVzc2FnZSgpfVxuICAgICAgICAgICAgPHA+e3RoaXMuZ2V0RXhwaXJhdGlvbk1lc3NhZ2UoKX08L3A+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgTG9hZGVyIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL2xvYWRlcic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBCdXR0b24gZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgbGV0IGNvbnRlbnQgPSBudWxsO1xuICAgIGxldCBjbGFzc05hbWUgPSAnYnRuICcgKyB0aGlzLnByb3BzLmNsYXNzTmFtZTtcbiAgICBsZXQgZGlzYWJsZWQgPSB0aGlzLnByb3BzLmRpc2FibGVkO1xuXG4gICAgaWYgKHRoaXMucHJvcHMubG9hZGluZykge1xuICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgY29udGVudCA9IDxMb2FkZXIgLz47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgICAgY2xhc3NOYW1lICs9ICcgYnRuLWxvYWRpbmcnO1xuICAgICAgZGlzYWJsZWQgPSB0cnVlO1xuICAgIH0gZWxzZSB7XG4gICAgICBjb250ZW50ID0gdGhpcy5wcm9wcy5jaGlsZHJlbjtcbiAgICB9XG5cbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxidXR0b24gdHlwZT17dGhpcy5wcm9wcy5vbkNsaWNrID8gJ2J1dHRvbicgOiAnc3VibWl0J31cbiAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9e2NsYXNzTmFtZX1cbiAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17ZGlzYWJsZWR9XG4gICAgICAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5wcm9wcy5vbkNsaWNrfT5cbiAgICAgIHtjb250ZW50fVxuICAgIDwvYnV0dG9uPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cblxuQnV0dG9uLmRlZmF1bHRQcm9wcyA9IHtcbiAgY2xhc3NOYW1lOiBcImJ0bi1kZWZhdWx0XCIsXG5cbiAgdHlwZTogXCJzdWJtaXRcIixcblxuICBsb2FkaW5nOiBmYWxzZSxcbiAgZGlzYWJsZWQ6IGZhbHNlLFxuXG4gIG9uQ2xpY2s6IG51bGxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgcmVxdWlyZWQgfSBmcm9tICdtaXNhZ28vdXRpbHMvdmFsaWRhdG9ycyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgdmFsaWRhdGUoKSB7XG4gICAgbGV0IGlzVmFsaWQgPSB0cnVlO1xuICAgIGxldCBlcnJvcnMgPSB7fTtcblxuICAgIGZvciAodmFyIGtleSBpbiB0aGlzLnN0YXRlLnZhbGlkYXRvcnMpIHtcbiAgICAgIGlmICh0aGlzLnN0YXRlLnZhbGlkYXRvcnMuaGFzT3duUHJvcGVydHkoa2V5KSkge1xuICAgICAgICBsZXQgdmFsdWUgPSB0aGlzLnN0YXRlW2tleV07XG4gICAgICAgIGVycm9yc1trZXldID0gdGhpcy52YWxpZGF0ZUZpZWxkKHZhbHVlLCB0aGlzLnN0YXRlLnZhbGlkYXRvcnNba2V5XSk7XG4gICAgICAgIGlmIChlcnJvcnNba2V5XSAhPT0gbnVsbCkge1xuICAgICAgICAgIGlzVmFsaWQgPSBmYWxzZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cblxuICAgIHJldHVybiBpc1ZhbGlkID8gbnVsbCA6IGVycm9ycztcbiAgfVxuXG4gIHZhbGlkYXRlRmllbGQodmFsdWUsIHZhbGlkYXRvcnMpIHtcbiAgICBsZXQgcmVzdWx0ID0gcmVxdWlyZWQoKSh2YWx1ZSk7XG4gICAgbGV0IGVycm9ycyA9IFtdO1xuXG4gICAgaWYgKHJlc3VsdCkge1xuICAgICAgcmV0dXJuIFtyZXN1bHRdO1xuICAgIH0gZWxzZSB7XG4gICAgICBmb3IgKGxldCBpIGluIHZhbGlkYXRvcnMpIHtcbiAgICAgICAgcmVzdWx0ID0gdmFsaWRhdG9yc1tpXSh2YWx1ZSk7XG4gICAgICAgIGlmIChyZXN1bHQpIHtcbiAgICAgICAgICBlcnJvcnMucHVzaChyZXN1bHQpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIGVycm9ycy5sZW5ndGggPyBlcnJvcnMgOiBudWxsO1xuICB9XG5cbiAgY2hhbmdlVmFsdWUobmFtZSwgdmFsdWUpIHtcbiAgICBsZXQgZXJyb3JzID0gbnVsbDtcbiAgICBpZiAodGhpcy5zdGF0ZS52YWxpZGF0b3JzLm5hbWUpIHtcbiAgICAgIGVycm9ycyA9IHRoaXMudmFsaWRhdGVGaWVsZChuYW1lLCB2YWx1ZSk7XG4gICAgfVxuICB9XG5cbiAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICBiaW5kSW5wdXQgPSAobmFtZSkgPT4ge1xuICAgIHJldHVybiAoZXZlbnQpID0+IHtcbiAgICAgIGxldCBuZXdTdGF0ZSA9IHt9O1xuICAgICAgbmV3U3RhdGVbbmFtZV0gPSBldmVudC50YXJnZXQudmFsdWU7XG4gICAgICB0aGlzLnNldFN0YXRlKG5ld1N0YXRlKTtcbiAgICB9XG4gIH1cblxuICBjbGVhbigpIHtcbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIHNlbmQoKSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICBoYW5kbGVTdWNjZXNzKHN1Y2Nlc3MpIHtcbiAgICByZXR1cm47XG4gIH1cblxuICBoYW5kbGVFcnJvcihyZWplY3Rpb24pIHtcbiAgICByZXR1cm47XG4gIH1cblxuICBoYW5kbGVTdWJtaXQgPSAoZXZlbnQpID0+IHtcbiAgICAvLyB3ZSBkb24ndCByZWxvYWQgcGFnZSBvbiBzdWJtaXNzaW9uc1xuICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG5cbiAgICBpZiAodGhpcy5zdGF0ZS5pc0xvYWRpbmcpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBpZiAodGhpcy5jbGVhbigpKSB7XG4gICAgICB0aGlzLnNldFN0YXRlKHsnaXNMb2FkaW5nJzogdHJ1ZX0pO1xuICAgICAgbGV0IHByb21pc2UgPSB0aGlzLnNlbmQoKTtcblxuICAgICAgaWYgKHByb21pc2UpIHtcbiAgICAgICAgcHJvbWlzZS50aGVuKChzdWNjZXNzKSA9PiB7XG4gICAgICAgICAgdGhpcy5oYW5kbGVTdWNjZXNzKHN1Y2Nlc3MpO1xuICAgICAgICAgIHRoaXMuc2V0U3RhdGUoeydpc0xvYWRpbmcnOiBmYWxzZX0pO1xuICAgICAgICB9LCAocmVqZWN0aW9uKSA9PiB7XG4gICAgICAgICAgdGhpcy5oYW5kbGVFcnJvcihyZWplY3Rpb24pO1xuICAgICAgICAgIHRoaXMuc2V0U3RhdGUoeydpc0xvYWRpbmcnOiBmYWxzZX0pO1xuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuc2V0U3RhdGUoeydpc0xvYWRpbmcnOiBmYWxzZX0pO1xuICAgICAgfVxuICAgIH1cbiAgfVxuICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xufSIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgcmVuZGVyKCkge1xuICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJsb2FkZXItY29tcGFjdFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJsb2FkZXItc3Bpbm5pbmctd2hlZWxcIj48L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWRpYWxvZyBtb2RhbC1yZWdpc3RlclwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1jb250ZW50XCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtaGVhZGVyXCI+XG4gICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiY2xvc2VcIiBkYXRhLWRpc21pc3M9XCJtb2RhbFwiIGFyaWEtbGFiZWw9XCJDbG9zZVwiPjxzcGFuIGFyaWEtaGlkZGVuPVwidHJ1ZVwiPiZ0aW1lczs8L3NwYW4+PC9idXR0b24+XG4gICAgICAgICAgPGg0IGNsYXNzTmFtZT1cIm1vZGFsLXRpdGxlXCI+e2dldHRleHQoXCJSZWdpc3RlclwiKX08L2g0PlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1ib2R5XCI+XG4gICAgICAgICAgPHA+VGhpcyB3aWxsIGJlIHJlZ2lzdHJhdGlvbiBmb3JtITwvcD5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibW9kYWwtZm9vdGVyXCI+XG4gICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIGJ0bi1kZWZhdWx0XCIgZGF0YS1kaXNtaXNzPVwibW9kYWxcIj5DbG9zZTwvYnV0dG9uPlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBCdXR0b24gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvYnV0dG9uJzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgRm9ybSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9mb3JtJztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcbmltcG9ydCBtb2RhbCBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9kYWwnO1xuaW1wb3J0IHNuYWNrYmFyIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zbmFja2Jhcic7XG5pbXBvcnQgc2hvd0Jhbm5lZFBhZ2UgZnJvbSAnbWlzYWdvL3V0aWxzL2Jhbm5lZC1wYWdlJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgZXh0ZW5kcyBGb3JtIHtcbiAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICBzdXBlcihwcm9wcyk7XG5cbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgJ2lzTG9hZGluZyc6IGZhbHNlLFxuICAgICAgJ3Nob3dBY3RpdmF0aW9uJzogZmFsc2UsXG5cbiAgICAgICd1c2VybmFtZSc6ICcnLFxuICAgICAgJ3Bhc3N3b3JkJzogJycsXG5cbiAgICAgIHZhbGlkYXRvcnM6IHtcbiAgICAgICAgJ3VzZXJuYW1lJzogW10sXG4gICAgICAgICdwYXNzd29yZCc6IFtdXG4gICAgICB9XG4gICAgfTtcbiAgfVxuXG4gIGNsZWFuKCkge1xuICAgIGlmICh0aGlzLnZhbGlkYXRlKCkpIHtcbiAgICAgIHNuYWNrYmFyLmVycm9yKGdldHRleHQoXCJGaWxsIG91dCBib3RoIGZpZWxkcy5cIikpO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9XG4gIH1cblxuICBzZW5kKCkge1xuICAgIHJldHVybiBhamF4LnBvc3QobWlzYWdvLmdldCgnQVVUSF9BUEknKSwge1xuICAgICAgJ3VzZXJuYW1lJzogdGhpcy5zdGF0ZS51c2VybmFtZSxcbiAgICAgICdwYXNzd29yZCc6IHRoaXMuc3RhdGUucGFzc3dvcmRcbiAgICB9KTtcbiAgfVxuXG4gIGhhbmRsZVN1Y2Nlc3MoKSB7XG4gICAgbW9kYWwuaGlkZSgpO1xuXG4gICAgbGV0IGZvcm0gPSAkKCcjaGlkZGVuLWxvZ2luLWZvcm0nKTtcblxuICAgIGZvcm0uYXBwZW5kKCc8aW5wdXQgdHlwZT1cInRleHRcIiBuYW1lPVwidXNlcm5hbWVcIiAvPicpO1xuICAgIGZvcm0uYXBwZW5kKCc8aW5wdXQgdHlwZT1cInBhc3N3b3JkXCIgbmFtZT1cInBhc3N3b3JkXCIgLz4nKTtcblxuICAgIC8vIGZpbGwgb3V0IGZvcm0gd2l0aCB1c2VyIGNyZWRlbnRpYWxzIGFuZCBzdWJtaXQgaXQsIHRoaXMgd2lsbCB0ZWxsXG4gICAgLy8gTWlzYWdvIHRvIHJlZGlyZWN0IHVzZXIgYmFjayB0byByaWdodCBwYWdlLCBhbmQgd2lsbCB0cmlnZ2VyIGJyb3dzZXInc1xuICAgIC8vIGtleSByaW5nIGZlYXR1cmVcbiAgICBmb3JtLmZpbmQoJ2lucHV0W3R5cGU9XCJoaWRkZW5cIl0nKS52YWwoYWpheC5nZXRDc3JmVG9rZW4oKSk7XG4gICAgZm9ybS5maW5kKCdpbnB1dFtuYW1lPVwicmVkaXJlY3RfdG9cIl0nKS52YWwod2luZG93LmxvY2F0aW9uLnBhdGhuYW1lKTtcbiAgICBmb3JtLmZpbmQoJ2lucHV0W25hbWU9XCJ1c2VybmFtZVwiXScpLnZhbCh0aGlzLnN0YXRlLnVzZXJuYW1lKTtcbiAgICBmb3JtLmZpbmQoJ2lucHV0W25hbWU9XCJwYXNzd29yZFwiXScpLnZhbCh0aGlzLnN0YXRlLnBhc3N3b3JkKTtcbiAgICBmb3JtLnN1Ym1pdCgpO1xuICB9XG5cbiAgaGFuZGxlRXJyb3IocmVqZWN0aW9uKSB7XG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwMCkge1xuICAgICAgaWYgKHJlamVjdGlvbi5jb2RlID09PSAnaW5hY3RpdmVfYWRtaW4nKSB7XG4gICAgICAgIHNuYWNrYmFyLmluZm8ocmVqZWN0aW9uLmRldGFpbCk7XG4gICAgICB9IGVsc2UgaWYgKHJlamVjdGlvbi5jb2RlID09PSAnaW5hY3RpdmVfdXNlcicpIHtcbiAgICAgICAgc25hY2tiYXIuaW5mbyhyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgJ3Nob3dBY3RpdmF0aW9uJzogdHJ1ZVxuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSBpZiAocmVqZWN0aW9uLmNvZGUgPT09ICdiYW5uZWQnKSB7XG4gICAgICAgIHNob3dCYW5uZWRQYWdlKHJlamVjdGlvbi5kZXRhaWwpO1xuICAgICAgICBtb2RhbC5oaWRlKCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzbmFja2Jhci5lcnJvcihyZWplY3Rpb24uZGV0YWlsKTtcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgc25hY2tiYXIuYXBpRXJyb3IocmVqZWN0aW9uKTtcbiAgICB9XG4gIH1cblxuICBnZXRBY3RpdmF0aW9uQnV0dG9uKCkge1xuICAgIGlmICh0aGlzLnN0YXRlLnNob3dBY3RpdmF0aW9uKSB7XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgICByZXR1cm4gPGEgaHJlZj17bWlzYWdvLmdldCgnUkVRVUVTVF9BQ1RJVkFUSU9OX1VSTCcpfVxuICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImJ0biBidG4tc3VjY2VzcyBidG4tYmxvY2tcIj5cbiAgICAgICAgIHtnZXR0ZXh0KFwiQWN0aXZhdGUgYWNjb3VudFwiKX1cbiAgICAgIDwvYT47XG4gICAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWRpYWxvZyBtb2RhbC1zbSBtb2RhbC1zaWduLWluXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWNvbnRlbnRcIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJtb2RhbC1oZWFkZXJcIj5cbiAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJjbG9zZVwiIGRhdGEtZGlzbWlzcz1cIm1vZGFsXCJcbiAgICAgICAgICAgICAgICAgIGFyaWEtbGFiZWw9e2dldHRleHQoXCJDbG9zZVwiKX0+XG4gICAgICAgICAgICA8c3BhbiBhcmlhLWhpZGRlbj1cInRydWVcIj4mdGltZXM7PC9zcGFuPlxuICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgIDxoNCBjbGFzc05hbWU9XCJtb2RhbC10aXRsZVwiPntnZXR0ZXh0KFwiU2lnbiBpblwiKX08L2g0PlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGZvcm0gb25TdWJtaXQ9e3RoaXMuaGFuZGxlU3VibWl0fT5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWJvZHlcIj5cblxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJmb3JtLWdyb3VwXCI+XG4gICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29udHJvbC1pbnB1dFwiPlxuICAgICAgICAgICAgICAgIDxpbnB1dCBpZD1cImlkX3VzZXJuYW1lXCIgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCIgdHlwZT1cInRleHRcIlxuICAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiVXNlcm5hbWUgb3IgZS1tYWlsXCIpfVxuICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17dGhpcy5iaW5kSW5wdXQoJ3VzZXJuYW1lJyl9XG4gICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXt0aGlzLnN0YXRlLnVzZXJuYW1lfSAvPlxuICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDwvZGl2PlxuXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXBcIj5cbiAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJjb250cm9sLWlucHV0XCI+XG4gICAgICAgICAgICAgICAgPGlucHV0IGlkPVwiaWRfcGFzc3dvcmRcIiBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIiB0eXBlPVwicGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17dGhpcy5zdGF0ZS5pc0xvYWRpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtnZXR0ZXh0KFwiUGFzc3dvcmRcIil9XG4gICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmJpbmRJbnB1dCgncGFzc3dvcmQnKX1cbiAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUucGFzc3dvcmR9IC8+XG4gICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm1vZGFsLWZvb3RlclwiPlxuICAgICAgICAgICAge3RoaXMuZ2V0QWN0aXZhdGlvbkJ1dHRvbigpfVxuICAgICAgICAgICAgPEJ1dHRvbiBjbGFzc05hbWU9XCJidG4tcHJpbWFyeSBidG4tYmxvY2tcIlxuICAgICAgICAgICAgICAgICAgICBsb2FkaW5nPXt0aGlzLnN0YXRlLmlzTG9hZGluZ30+XG4gICAgICAgICAgICAgIHtnZXR0ZXh0KFwiU2lnbiBpblwiKX1cbiAgICAgICAgICAgIDwvQnV0dG9uPlxuICAgICAgICAgICAgPGEgaHJlZj17bWlzYWdvLmdldCgnRk9SR09UVEVOX1BBU1NXT1JEX1VSTCcpfVxuICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiYnRuIGJ0bi1kZWZhdWx0IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAgICAge2dldHRleHQoXCJGb3Jnb3QgcGFzc3dvcmQ/XCIpfVxuICAgICAgICAgICAgPC9hPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Zvcm0+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuY29uc3QgVFlQRVNfQ0xBU1NFUyA9IHtcbiAgJ2luZm8nOiAnYWxlcnQtaW5mbycsXG4gICdzdWNjZXNzJzogJ2FsZXJ0LXN1Y2Nlc3MnLFxuICAnd2FybmluZyc6ICdhbGVydC13YXJuaW5nJyxcbiAgJ2Vycm9yJzogJ2FsZXJ0LWRhbmdlcidcbn07XG4vKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuXG5leHBvcnQgY2xhc3MgU25hY2tiYXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICBnZXRTbmFja2JhckNsYXNzKCkge1xuICAgIGxldCBzbmFja2JhckNsYXNzID0gJ2FsZXJ0cy1zbmFja2Jhcic7XG4gICAgaWYgKHRoaXMucHJvcHMuaXNWaXNpYmxlKSB7XG4gICAgICBzbmFja2JhckNsYXNzICs9ICcgaW4nO1xuICAgIH0gZWxzZSB7XG4gICAgICBzbmFja2JhckNsYXNzICs9ICcgb3V0JztcbiAgICB9XG4gICAgcmV0dXJuIHNuYWNrYmFyQ2xhc3M7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT17dGhpcy5nZXRTbmFja2JhckNsYXNzKCl9PlxuICAgICAgPHAgY2xhc3NOYW1lPXsnYWxlcnQgJyArIFRZUEVTX0NMQVNTRVNbdGhpcy5wcm9wcy50eXBlXX0+XG4gICAgICAgIHt0aGlzLnByb3BzLm1lc3NhZ2V9XG4gICAgICA8L3A+XG4gICAgPC9kaXY+O1xuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4gc3RhdGUuc25hY2tiYXI7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEJ1dHRvbiBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9idXR0b24nOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcblxuaW1wb3J0IG1vZGFsIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9tb2RhbCc7XG5pbXBvcnQgZHJvcGRvd24gZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vYmlsZS1uYXZiYXItZHJvcGRvd24nO1xuaW1wb3J0IEF2YXRhciBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9hdmF0YXInOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBTaWduSW5Nb2RhbCBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9zaWduLWluLmpzJztcbmltcG9ydCBSZWdpc3Rlck1vZGFsIGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3JlZ2lzdGVyL3Jvb3QuanMnO1xuXG5leHBvcnQgY2xhc3MgR3Vlc3RNZW51IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgc2hvd1NpZ25Jbk1vZGFsKCkge1xuICAgIG1vZGFsLnNob3coU2lnbkluTW9kYWwpO1xuICB9XG5cbiAgc2hvd1JlZ2lzdGVyTW9kYWwoKSB7XG4gICAgbW9kYWwuc2hvdyhSZWdpc3Rlck1vZGFsKTtcbiAgfVxuXG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDx1bCBjbGFzc05hbWU9XCJkcm9wZG93bi1tZW51IHVzZXItZHJvcGRvd24gZHJvcGRvd24tbWVudS1yaWdodFwiXG4gICAgICAgICAgICAgICByb2xlPVwibWVudVwiPlxuICAgICAgPGxpIGNsYXNzTmFtZT1cImd1ZXN0LXByZXZpZXdcIj5cbiAgICAgICAgPGg0PntnZXR0ZXh0KFwiWW91IGFyZSBicm93c2luZyBhcyBndWVzdC5cIil9PC9oND5cbiAgICAgICAgPHA+XG4gICAgICAgICAge2dldHRleHQoJ1NpZ24gaW4gb3IgcmVnaXN0ZXIgdG8gc3RhcnQgYW5kIHBhcnRpY2lwYXRlIGluIGRpc2N1c3Npb25zLicpfVxuICAgICAgICA8L3A+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwicm93XCI+XG5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbC14cy02XCI+XG4gICAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBjbGFzc05hbWU9XCJidG4gYnRuLWRlZmF1bHQgYnRuLWJsb2NrXCI+XG4gICAgICAgICAgICAgIFRoeSBTaWduIEluXG4gICAgICAgICAgICA8L2J1dHRvbj5cblxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY29sLXhzLTZcIj5cblxuICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3NOYW1lPVwiYnRuIGJ0bi1wcmltYXJ5IGJ0bi1ibG9ja1wiPlxuICAgICAgICAgICAgICBUaHkgUmVnaXN0cnlcbiAgICAgICAgICAgIDwvYnV0dG9uPlxuXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9saT5cbiAgICA8L3VsPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG5cbmV4cG9ydCBjbGFzcyBHdWVzdE5hdiBleHRlbmRzIEd1ZXN0TWVudSB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwibmF2IG5hdi1ndWVzdFwiPlxuICAgICAgPEJ1dHRvbiB0eXBlPVwiYnV0dG9uXCJcbiAgICAgICAgICAgICAgY2xhc3NOYW1lPVwibmF2YmFyLWJ0biBidG4tZGVmYXVsdFwiXG4gICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMuc2hvd1NpZ25Jbk1vZGFsfT5cbiAgICAgICAgU2lnbiBpblxuICAgICAgPC9CdXR0b24+XG4gICAgICA8QnV0dG9uIHR5cGU9XCJidXR0b25cIlxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJuYXZiYXItYnRuIGJ0bi1wcmltYXJ5XCJcbiAgICAgICAgICAgICAgb25DbGljaz17dGhpcy5zaG93UmVnaXN0ZXJNb2RhbH0+XG4gICAgICAgIFJlZ2lzdGVyXG4gICAgICA8L0J1dHRvbj5cbiAgICA8L2Rpdj47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuXG5leHBvcnQgY2xhc3MgQ29tcGFjdEd1ZXN0TmF2IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgc2hvd0d1ZXN0TWVudSgpIHtcbiAgICBkcm9wZG93bi5zaG93KEd1ZXN0TWVudSk7XG4gIH1cblxuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8YnV0dG9uIHR5cGU9XCJidXR0b25cIiBvbkNsaWNrPXt0aGlzLnNob3dHdWVzdE1lbnV9PlxuICAgICAgPEF2YXRhciBzaXplPVwiNjRcIiAvPlxuICAgIDwvYnV0dG9uPjtcbiAgICAvKiBqc2hpbnQgaWdub3JlOmVuZCAqL1xuICB9XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgR3Vlc3ROYXYsIENvbXBhY3RHdWVzdE5hdiB9IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3VzZXItbWVudS9ndWVzdC1uYXYnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBVc2VyTmF2IGZyb20gJ21pc2Fnby9jb21wb25lbnRzL3VzZXItbWVudS91c2VyLW5hdic7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgY2xhc3MgVXNlck1lbnUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIGlmICh0aGlzLnByb3BzLmlzQXV0aGVudGljYXRlZCkge1xuICAgICAgcmV0dXJuIDxVc2VyTmF2IHVzZXI9e3RoaXMucHJvcHMudXNlcn0gLz47XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiA8R3Vlc3ROYXYgLz47XG4gICAgfVxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIENvbXBhY3RVc2VyTWVudSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gIHJlbmRlcigpIHtcbiAgICAvKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG4gICAgaWYgKHRoaXMucHJvcHMuaXNBdXRoZW50aWNhdGVkKSB7XG4gICAgICByZXR1cm4gPFVzZXJOYXYgdXNlcj17dGhpcy5wcm9wcy51c2VyfSAvPjtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIDxDb21wYWN0R3Vlc3ROYXYgLz47XG4gICAgfVxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNlbGVjdChzdGF0ZSkge1xuICByZXR1cm4gc3RhdGUuYXV0aDtcbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFVzZXJOYXYgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICByZW5kZXIoKSB7XG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIHJldHVybiA8dWwgY2xhc3M9XCJ1bCBuYXYgbmF2YmFyLW5hdiBuYXYtdXNlclwiPlxuXG4gICAgPC91bD47XG4gICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgfVxufVxuIiwiaW1wb3J0IE9yZGVyZWRMaXN0IGZyb20gJ21pc2Fnby91dGlscy9vcmRlcmVkLWxpc3QnO1xuXG5leHBvcnQgY2xhc3MgTWlzYWdvIHtcbiAgY29uc3RydWN0b3IoKSB7XG4gICAgdGhpcy5faW5pdGlhbGl6ZXJzID0gW107XG4gICAgdGhpcy5fY29udGV4dCA9IHt9O1xuICB9XG5cbiAgYWRkSW5pdGlhbGl6ZXIoaW5pdGlhbGl6ZXIpIHtcbiAgICB0aGlzLl9pbml0aWFsaXplcnMucHVzaCh7XG4gICAgICBrZXk6IGluaXRpYWxpemVyLm5hbWUsXG5cbiAgICAgIGl0ZW06IGluaXRpYWxpemVyLmluaXRpYWxpemVyLFxuXG4gICAgICBhZnRlcjogaW5pdGlhbGl6ZXIuYWZ0ZXIsXG4gICAgICBiZWZvcmU6IGluaXRpYWxpemVyLmJlZm9yZVxuICAgIH0pO1xuICB9XG5cbiAgaW5pdChjb250ZXh0KSB7XG4gICAgdGhpcy5fY29udGV4dCA9IGNvbnRleHQ7XG5cbiAgICB2YXIgaW5pdE9yZGVyID0gbmV3IE9yZGVyZWRMaXN0KHRoaXMuX2luaXRpYWxpemVycykub3JkZXJlZFZhbHVlcygpO1xuICAgIGluaXRPcmRlci5mb3JFYWNoKGluaXRpYWxpemVyID0+IHtcbiAgICAgIGluaXRpYWxpemVyKHRoaXMpO1xuICAgIH0pO1xuICB9XG5cbiAgLy8gY29udGV4dCBhY2Nlc3NvcnNcbiAgaGFzKGtleSkge1xuICAgIHJldHVybiB0aGlzLl9jb250ZXh0Lmhhc093blByb3BlcnR5KGtleSk7XG4gIH1cblxuICBnZXQoa2V5LCBmYWxsYmFjaykge1xuICAgIGlmICh0aGlzLmhhcyhrZXkpKSB7XG4gICAgICByZXR1cm4gdGhpcy5fY29udGV4dFtrZXldO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gZmFsbGJhY2sgfHwgdW5kZWZpbmVkO1xuICAgIH1cbiAgfVxufVxuXG4vLyBjcmVhdGUgIHNpbmdsZXRvblxudmFyIG1pc2FnbyA9IG5ldyBNaXNhZ28oKTtcblxuLy8gZXhwb3NlIGl0IGdsb2JhbGx5XG5nbG9iYWwubWlzYWdvID0gbWlzYWdvO1xuXG4vLyBhbmQgZXhwb3J0IGl0IGZvciB0ZXN0cyBhbmQgc3R1ZmZcbmV4cG9ydCBkZWZhdWx0IG1pc2FnbztcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBhamF4IGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9hamF4JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGFqYXguaW5pdChtaXNhZ28uZ2V0KCdDU1JGX0NPT0tJRV9OQU1FJykpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnYWpheCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplclxufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgcmVkdWNlciBmcm9tICdtaXNhZ28vcmVkdWNlcnMvYXV0aCc7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoY29udGV4dCkge1xuICBzdG9yZS5hZGRSZWR1Y2VyKCdhdXRoJywgcmVkdWNlciwge1xuICAgICdpc0F1dGhlbnRpY2F0ZWQnOiBjb250ZXh0LmdldCgnaXNBdXRoZW50aWNhdGVkJyksXG4gICAgJ2lzQW5vbnltb3VzJzogIWNvbnRleHQuZ2V0KCdpc0F1dGhlbnRpY2F0ZWQnKSxcblxuICAgICd1c2VyJzogY29udGV4dC5nZXQoJ3VzZXInKVxuICB9KTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3JlZHVjZXI6YXV0aCcsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYmVmb3JlOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCBkcm9wZG93biBmcm9tICdtaXNhZ28vc2VydmljZXMvbW9iaWxlLW5hdmJhci1kcm9wZG93bic7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBsZXQgZWxlbWVudCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdtb2JpbGUtbmF2YmFyLWRyb3Bkb3duLW1vdW50Jyk7XG4gIGlmIChlbGVtZW50KSB7XG4gICAgZHJvcGRvd24uaW5pdChlbGVtZW50KTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnZHJvcGRvd24nLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgbW9kYWwgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL21vZGFsJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIGxldCBlbGVtZW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ21vZGFsLW1vdW50Jyk7XG4gIGlmIChlbGVtZW50KSB7XG4gICAgbW9kYWwuaW5pdChlbGVtZW50KTtcbiAgfVxufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnbW9kYWwnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbW9tZW50IGZyb20gJ21vbWVudCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBtb21lbnQubG9jYWxlKCQoJ2h0bWwnKS5hdHRyKCdsYW5nJykpO1xufVxuXG5taXNhZ28uYWRkSW5pdGlhbGl6ZXIoe1xuICBuYW1lOiAnbW9tZW50JyxcbiAgaW5pdGlhbGl6ZXI6IGluaXRpYWxpemVyXG59KTtcbiIsImltcG9ydCB7IGNvbm5lY3QgfSBmcm9tICdyZWFjdC1yZWR1eCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgeyBTbmFja2Jhciwgc2VsZWN0IH0gZnJvbSAnbWlzYWdvL2NvbXBvbmVudHMvc25hY2tiYXInO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgbW91bnQoY29ubmVjdChzZWxlY3QpKFNuYWNrYmFyKSwgJ3NuYWNrYmFyLW1vdW50Jyk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdjb21wb25lbnQ6c25hY2tiYXInLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc25hY2tiYXInXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCByZWR1Y2VyLCB7IGluaXRpYWxTdGF0ZSB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9zbmFja2Jhcic7XG5pbXBvcnQgc3RvcmUgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3N0b3JlJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHN0b3JlLmFkZFJlZHVjZXIoJ3NuYWNrYmFyJywgcmVkdWNlciwgaW5pdGlhbFN0YXRlKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3JlZHVjZXI6c25hY2tiYXInLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGJlZm9yZTogJ3N0b3JlJ1xufSk7XG4iLCJpbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgc25hY2tiYXIgZnJvbSAnbWlzYWdvL3NlcnZpY2VzL3NuYWNrYmFyJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBpbml0aWFsaXplcigpIHtcbiAgc25hY2tiYXIuaW5pdChzdG9yZSk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdzbmFja2JhcicsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYWZ0ZXI6ICdzdG9yZSdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBzdG9yZS5pbml0KCk7XG59XG5cbm1pc2Fnby5hZGRJbml0aWFsaXplcih7XG4gIG5hbWU6ICdzdG9yZScsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYmVmb3JlOiAnX2VuZCdcbn0pO1xuIiwiaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHJlZHVjZXIsIHsgaW5pdGlhbFN0YXRlIH0gZnJvbSAnbWlzYWdvL3JlZHVjZXJzL3RpY2snO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBzdG9yZS5hZGRSZWR1Y2VyKCd0aWNrJywgcmVkdWNlciwgaW5pdGlhbFN0YXRlKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3JlZHVjZXI6dGljaycsXG4gIGluaXRpYWxpemVyOiBpbml0aWFsaXplcixcbiAgYmVmb3JlOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCBtaXNhZ28gZnJvbSAnbWlzYWdvL2luZGV4JztcbmltcG9ydCB7IGRvVGljayB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy90aWNrJztcbmltcG9ydCBzdG9yZSBmcm9tICdtaXNhZ28vc2VydmljZXMvc3RvcmUnO1xuXG5jb25zdCBUSUNLX1BFUklPRCA9IDUwICogMTAwMDsgLy9kbyB0aGUgdGljayBldmVyeSA1MHNcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaW5pdGlhbGl6ZXIoKSB7XG4gIHdpbmRvdy5zZXRJbnRlcnZhbChmdW5jdGlvbigpIHtcbiAgICBzdG9yZS5kaXNwYXRjaChkb1RpY2soKSk7XG4gIH0sIFRJQ0tfUEVSSU9EKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ3RpY2stc3RhcnQnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImltcG9ydCB7IGNvbm5lY3QgfSBmcm9tICdyZWFjdC1yZWR1eCc7XG5pbXBvcnQgbWlzYWdvIGZyb20gJ21pc2Fnby9pbmRleCc7XG5pbXBvcnQgeyBVc2VyTWVudSwgQ29tcGFjdFVzZXJNZW51LCBzZWxlY3QgfSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy91c2VyLW1lbnUvcm9vdCc7XG5pbXBvcnQgbW91bnQgZnJvbSAnbWlzYWdvL3V0aWxzL21vdW50LWNvbXBvbmVudCc7XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGluaXRpYWxpemVyKCkge1xuICBtb3VudChjb25uZWN0KHNlbGVjdCkoVXNlck1lbnUpLCAndXNlci1tZW51LW1vdW50Jyk7XG4gIG1vdW50KGNvbm5lY3Qoc2VsZWN0KShDb21wYWN0VXNlck1lbnUpLCAndXNlci1tZW51LWNvbXBhY3QtbW91bnQnKTtcbn1cblxubWlzYWdvLmFkZEluaXRpYWxpemVyKHtcbiAgbmFtZTogJ2NvbXBvbmVudDp1c2VyLW1lbnUnLFxuICBpbml0aWFsaXplcjogaW5pdGlhbGl6ZXIsXG4gIGFmdGVyOiAnc3RvcmUnXG59KTtcbiIsImV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIGF1dGgoc3RhdGU9e30sIGFjdGlvbj1udWxsKSB7XG4gIHJldHVybiBzdGF0ZTtcbn1cbiIsImV4cG9ydCB2YXIgaW5pdGlhbFN0YXRlID0ge1xuICB0eXBlOiAnaW5mbycsXG4gIG1lc3NhZ2U6ICcnLFxuICBpc1Zpc2libGU6IGZhbHNlXG59O1xuXG5leHBvcnQgY29uc3QgU0hPV19TTkFDS0JBUiA9ICdTSE9XX1NOQUNLQkFSJztcbmV4cG9ydCBjb25zdCBISURFX1NOQUNLQkFSID0gJ0hJREVfU05BQ0tCQVInO1xuXG5leHBvcnQgZnVuY3Rpb24gc2hvd1NuYWNrYmFyKG1lc3NhZ2UsIHR5cGUpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBTSE9XX1NOQUNLQkFSLFxuICAgIG1lc3NhZ2UsXG4gICAgbWVzc2FnZVR5cGU6IHR5cGVcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGhpZGVTbmFja2JhcigpIHtcbiAgcmV0dXJuIHtcbiAgICB0eXBlOiBISURFX1NOQUNLQkFSXG4gIH07XG59XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIHNuYWNrYmFyKHN0YXRlPWluaXRpYWxTdGF0ZSwgYWN0aW9uPW51bGwpIHtcbiAgaWYgKGFjdGlvbi50eXBlID09PSBTSE9XX1NOQUNLQkFSKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHR5cGU6IGFjdGlvbi5tZXNzYWdlVHlwZSxcbiAgICAgIG1lc3NhZ2U6IGFjdGlvbi5tZXNzYWdlLFxuICAgICAgaXNWaXNpYmxlOiB0cnVlXG4gICAgfTtcbiAgfSBlbHNlIGlmIChhY3Rpb24udHlwZSA9PT0gSElERV9TTkFDS0JBUikge1xuICAgIHJldHVybiBPYmplY3QuYXNzaWduKHt9LCBzdGF0ZSwge1xuICAgICAgICBpc1Zpc2libGU6IGZhbHNlXG4gICAgfSk7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIHN0YXRlO1xuICB9XG59XG4iLCJleHBvcnQgdmFyIGluaXRpYWxTdGF0ZSA9IHtcbiAgdGljazogMFxufTtcblxuZXhwb3J0IGNvbnN0IFRJQ0sgPSAnVElDSyc7XG5cbmV4cG9ydCBmdW5jdGlvbiBkb1RpY2soKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogVElDS1xuICB9O1xufVxuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiB0aWNrKHN0YXRlPWluaXRpYWxTdGF0ZSwgYWN0aW9uPW51bGwpIHtcbiAgaWYgKGFjdGlvbi50eXBlID09PSBUSUNLKSB7XG4gICAgcmV0dXJuIE9iamVjdC5hc3NpZ24oe30sIHN0YXRlLCB7XG4gICAgICAgIHRpY2s6IHN0YXRlLnRpY2sgKyAxXG4gICAgfSk7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIHN0YXRlO1xuICB9XG59XG4iLCJleHBvcnQgY2xhc3MgQWpheCB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2Nvb2tpZU5hbWUgPSBudWxsO1xuICAgIHRoaXMuX2NzcmZUb2tlbiA9IG51bGw7XG4gIH1cblxuICBpbml0KGNvb2tpZU5hbWUpIHtcbiAgICB0aGlzLl9jb29raWVOYW1lID0gY29va2llTmFtZTtcbiAgICB0aGlzLl9jc3JmVG9rZW4gPSB0aGlzLmdldENzcmZUb2tlbigpO1xuICB9XG5cbiAgZ2V0Q3NyZlRva2VuKCkge1xuICAgIGlmIChkb2N1bWVudC5jb29raWUuaW5kZXhPZih0aGlzLl9jb29raWVOYW1lKSAhPT0gLTEpIHtcbiAgICAgIHZhciBjb29raWVSZWdleCA9IG5ldyBSZWdFeHAodGhpcy5fY29va2llTmFtZSArICdcXD0oW147XSopJyk7XG4gICAgICB2YXIgY29va2llID0gZG9jdW1lbnQuY29va2llLm1hdGNoKGNvb2tpZVJlZ2V4KVswXTtcbiAgICAgIHJldHVybiBjb29raWUgPyBjb29raWUuc3BsaXQoJz0nKVsxXSA6IG51bGw7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHJlcXVlc3QobWV0aG9kLCB1cmwsIGRhdGEpIHtcbiAgICB2YXIgc2VsZiA9IHRoaXM7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uKHJlc29sdmUsIHJlamVjdCkge1xuICAgICAgdmFyIHhociA9IHtcbiAgICAgICAgdXJsOiB1cmwsXG4gICAgICAgIG1ldGhvZDogbWV0aG9kLFxuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgJ1gtQ1NSRlRva2VuJzogc2VsZi5fY3NyZlRva2VuXG4gICAgICAgIH0sXG5cbiAgICAgICAgZGF0YTogZGF0YSB8fCB7fSxcbiAgICAgICAgZGF0YVR5cGU6ICdqc29uJyxcblxuICAgICAgICBzdWNjZXNzOiBmdW5jdGlvbihkYXRhKSB7XG4gICAgICAgICAgcmVzb2x2ZShkYXRhKTtcbiAgICAgICAgfSxcblxuICAgICAgICBlcnJvcjogZnVuY3Rpb24oanFYSFIpIHtcbiAgICAgICAgICB2YXIgcmVqZWN0aW9uID0ganFYSFIucmVzcG9uc2VKU09OIHx8IHt9O1xuXG4gICAgICAgICAgcmVqZWN0aW9uLnN0YXR1cyA9IGpxWEhSLnN0YXR1cztcbiAgICAgICAgICByZWplY3Rpb24uc3RhdHVzVGV4dCA9IGpxWEhSLnN0YXR1c1RleHQ7XG5cbiAgICAgICAgICByZWplY3QocmVqZWN0aW9uKTtcbiAgICAgICAgfVxuICAgICAgfTtcblxuICAgICAgJC5hamF4KHhocik7XG4gICAgfSk7XG4gIH1cblxuICBnZXQodXJsKSB7XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnR0VUJywgdXJsKTtcbiAgfVxuXG4gIHBvc3QodXJsLCBkYXRhKSB7XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnUE9TVCcsIHVybCwgZGF0YSk7XG4gIH1cblxuICBwYXRjaCh1cmwsIGRhdGEpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdQQVRDSCcsIHVybCwgZGF0YSk7XG4gIH1cblxuICBwdXQodXJsLCBkYXRhKSB7XG4gICAgcmV0dXJuIHRoaXMucmVxdWVzdCgnUFVUJywgdXJsLCBkYXRhKTtcbiAgfVxuXG4gIGRlbGV0ZSh1cmwpIHtcbiAgICByZXR1cm4gdGhpcy5yZXF1ZXN0KCdERUxFVEUnLCB1cmwpO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBBamF4KCk7XG4iLCJpbXBvcnQgbW91bnQgZnJvbSAnbWlzYWdvL3V0aWxzL21vdW50LWNvbXBvbmVudCc7XG5cbmV4cG9ydCBjbGFzcyBNb2JpbGVOYXZiYXJEcm9wZG93biB7XG4gIGluaXQoZWxlbWVudCkge1xuICAgIHRoaXMuX2VsZW1lbnQgPSBlbGVtZW50O1xuICAgIHRoaXMuX2NvbXBvbmVudCA9IG51bGw7XG4gIH1cblxuICBzaG93KGNvbXBvbmVudCkge1xuICAgIGlmICh0aGlzLl9jb21wb25lbnQgPT09IGNvbXBvbmVudCkge1xuICAgICAgdGhpcy5oaWRlKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2NvbXBvbmVudCA9IGNvbXBvbmVudDtcbiAgICAgIG1vdW50KGNvbXBvbmVudCwgdGhpcy5fZWxlbWVudC5pZCk7XG4gICAgICAkKHRoaXMuX2VsZW1lbnQpLmFkZENsYXNzKCdvcGVuJyk7XG4gICAgfVxuICB9XG5cbiAgaGlkZSgpIHtcbiAgICAkKHRoaXMuX2VsZW1lbnQpLnJlbW92ZUNsYXNzKCdvcGVuJyk7XG4gICAgdGhpcy5fY29tcG9uZW50ID0gbnVsbDtcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBuZXcgTW9iaWxlTmF2YmFyRHJvcGRvd24oKTtcbiIsImltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IG1vdW50IGZyb20gJ21pc2Fnby91dGlscy9tb3VudC1jb21wb25lbnQnO1xuXG5leHBvcnQgY2xhc3MgTW9kYWwge1xuICBpbml0KGVsZW1lbnQpIHtcbiAgICB0aGlzLl9lbGVtZW50ID0gZWxlbWVudDtcblxuICAgIHRoaXMuX21vZGFsID0gJChlbGVtZW50KS5tb2RhbCh7c2hvdzogZmFsc2V9KTtcblxuICAgIHRoaXMuX21vZGFsLm9uKCdoaWRkZW4uYnMubW9kYWwnLCAoKSA9PiB7XG4gICAgICBSZWFjdERPTS51bm1vdW50Q29tcG9uZW50QXROb2RlKHRoaXMuX2VsZW1lbnQpO1xuICAgIH0pO1xuICB9XG5cbiAgc2hvdyhjb21wb25lbnQpIHtcbiAgICBtb3VudChjb21wb25lbnQsIHRoaXMuX2VsZW1lbnQuaWQpO1xuICAgIHRoaXMuX21vZGFsLm1vZGFsKCdzaG93Jyk7XG4gIH1cblxuICBoaWRlKCkge1xuICAgIHRoaXMuX21vZGFsLm1vZGFsKCdoaWRlJyk7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IE1vZGFsKCk7XG4iLCJpbXBvcnQgeyBzaG93U25hY2tiYXIsIGhpZGVTbmFja2JhciB9IGZyb20gJ21pc2Fnby9yZWR1Y2Vycy9zbmFja2Jhcic7XG5cbmNvbnN0IEhJREVfQU5JTUFUSU9OX0xFTkdUSCA9IDMwMDtcbmNvbnN0IE1FU1NBR0VfU0hPV19MRU5HVEggPSA1MDAwO1xuXG5leHBvcnQgY2xhc3MgU25hY2tiYXIge1xuICBpbml0KHN0b3JlKSB7XG4gICAgdGhpcy5fc3RvcmUgPSBzdG9yZTtcbiAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgfVxuXG4gIGFsZXJ0KG1lc3NhZ2UsIHR5cGUpIHtcbiAgICBpZiAodGhpcy5fdGltZW91dCkge1xuICAgICAgd2luZG93LmNsZWFyVGltZW91dCh0aGlzLl90aW1lb3V0KTtcbiAgICAgIHRoaXMuX3N0b3JlLmRpc3BhdGNoKGhpZGVTbmFja2JhcigpKTtcblxuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fdGltZW91dCA9IG51bGw7XG4gICAgICAgIHRoaXMuYWxlcnQobWVzc2FnZSwgdHlwZSk7XG4gICAgICB9LCBISURFX0FOSU1BVElPTl9MRU5HVEgpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9zdG9yZS5kaXNwYXRjaChzaG93U25hY2tiYXIobWVzc2FnZSwgdHlwZSkpO1xuICAgICAgdGhpcy5fdGltZW91dCA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgdGhpcy5fc3RvcmUuZGlzcGF0Y2goaGlkZVNuYWNrYmFyKCkpO1xuICAgICAgICB0aGlzLl90aW1lb3V0ID0gbnVsbDtcbiAgICAgIH0sIE1FU1NBR0VfU0hPV19MRU5HVEgpO1xuICAgIH1cbiAgfVxuXG4gIC8vIHNob3J0aGFuZHMgZm9yIG1lc3NhZ2UgdHlwZXNcblxuICBpbmZvKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdpbmZvJyk7XG4gIH1cblxuICBzdWNjZXNzKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICdzdWNjZXNzJyk7XG4gIH1cblxuICB3YXJuaW5nKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmFsZXJ0KG1lc3NhZ2UsICd3YXJuaW5nJyk7XG4gIH1cblxuICBlcnJvcihtZXNzYWdlKSB7XG4gICAgdGhpcy5hbGVydChtZXNzYWdlLCAnZXJyb3InKTtcbiAgfVxuXG4gIC8vIHNob3J0aGFuZCBmb3IgYXBpIGVycm9yc1xuICBhcGlFcnJvcihyZWplY3Rpb24pIHtcbiAgICBsZXQgbWVzc2FnZSA9IGdldHRleHQoXCJVbmtub3duIGVycm9yIGhhcyBvY2N1cmVkLlwiKTtcblxuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSAwKSB7XG4gICAgICBtZXNzYWdlID0gZ2V0dGV4dChcIkxvc3QgY29ubmVjdGlvbiB3aXRoIGFwcGxpY2F0aW9uLlwiKTtcbiAgICB9XG5cbiAgICBpZiAocmVqZWN0aW9uLnN0YXR1cyA9PT0gNDAwICYmIHJlamVjdGlvbi5kZXRhaWwpIHtcbiAgICAgIG1lc3NhZ2UgPSByZWplY3Rpb24uZGV0YWlsO1xuICAgIH1cblxuICAgIGlmIChyZWplY3Rpb24uc3RhdHVzID09PSA0MDMpIHtcbiAgICAgIG1lc3NhZ2UgPSByZWplY3Rpb24uZGV0YWlsO1xuICAgICAgaWYgKG1lc3NhZ2UgPT09IFwiUGVybWlzc2lvbiBkZW5pZWRcIikge1xuICAgICAgICBtZXNzYWdlID0gZ2V0dGV4dChcbiAgICAgICAgICBcIllvdSBkb24ndCBoYXZlIHBlcm1pc3Npb24gdG8gcGVyZm9ybSB0aGlzIGFjdGlvbi5cIik7XG4gICAgICB9XG4gICAgfVxuXG4gICAgaWYgKHJlamVjdGlvbi5zdGF0dXMgPT09IDQwNCkge1xuICAgICAgbWVzc2FnZSA9IGdldHRleHQoXCJBY3Rpb24gbGluayBpcyBpbnZhbGlkLlwiKTtcbiAgICB9XG5cbiAgICB0aGlzLmVycm9yKG1lc3NhZ2UpO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG5ldyBTbmFja2JhcigpO1xuIiwiaW1wb3J0IHsgY29tYmluZVJlZHVjZXJzLCBjcmVhdGVTdG9yZSB9IGZyb20gJ3JlZHV4JztcblxuZXhwb3J0IGNsYXNzIFN0b3JlV3JhcHBlciB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX3N0b3JlID0gbnVsbDtcbiAgICB0aGlzLl9yZWR1Y2VycyA9IHt9O1xuICAgIHRoaXMuX2luaXRpYWxTdGF0ZSA9IHt9O1xuICB9XG5cbiAgYWRkUmVkdWNlcihuYW1lLCByZWR1Y2VyLCBpbml0aWFsU3RhdGUpIHtcbiAgICB0aGlzLl9yZWR1Y2Vyc1tuYW1lXSA9IHJlZHVjZXI7XG4gICAgdGhpcy5faW5pdGlhbFN0YXRlW25hbWVdID0gaW5pdGlhbFN0YXRlO1xuICB9XG5cbiAgaW5pdCgpIHtcbiAgICB0aGlzLl9zdG9yZSA9IGNyZWF0ZVN0b3JlKFxuICAgICAgY29tYmluZVJlZHVjZXJzKHRoaXMuX3JlZHVjZXJzKSwgdGhpcy5faW5pdGlhbFN0YXRlKTtcbiAgfVxuXG4gIGdldFN0b3JlKCkge1xuICAgIHJldHVybiB0aGlzLl9zdG9yZTtcbiAgfVxuXG4gIC8vIFN0b3JlIEFQSVxuXG4gIGdldFN0YXRlKCkge1xuICAgIHJldHVybiB0aGlzLl9zdG9yZS5nZXRTdGF0ZSgpO1xuICB9XG5cbiAgZGlzcGF0Y2goYWN0aW9uKSB7XG4gICAgcmV0dXJuIHRoaXMuX3N0b3JlLmRpc3BhdGNoKGFjdGlvbik7XG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgbmV3IFN0b3JlV3JhcHBlcigpO1xuIiwiaW1wb3J0IG1vbWVudCBmcm9tICdtb21lbnQnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5pbXBvcnQgeyBQcm92aWRlciwgY29ubmVjdCB9IGZyb20gJ3JlYWN0LXJlZHV4JzsgLy8ganNoaW50IGlnbm9yZTpsaW5lXG5pbXBvcnQgQmFubmVkUGFnZSBmcm9tICdtaXNhZ28vY29tcG9uZW50cy9iYW5uZWQtcGFnZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IG1pc2FnbyBmcm9tICdtaXNhZ28vaW5kZXgnO1xuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG4vKiBqc2hpbnQgaWdub3JlOnN0YXJ0ICovXG5sZXQgc2VsZWN0ID0gZnVuY3Rpb24oc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLnRpY2s7XG59O1xuXG5sZXQgUmVkcmF3ZWRCYW5uZWRQYWdlID0gY29ubmVjdChzZWxlY3QpKEJhbm5lZFBhZ2UpO1xuLyoganNoaW50IGlnbm9yZTplbmQgKi9cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24oYmFuLCBjaGFuZ2VTdGF0ZSkge1xuICBSZWFjdERPTS5yZW5kZXIoXG4gICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgIDxQcm92aWRlciBzdG9yZT17c3RvcmUuZ2V0U3RvcmUoKX0+XG4gICAgICA8UmVkcmF3ZWRCYW5uZWRQYWdlIG1lc3NhZ2U9e2Jhbi5tZXNzYWdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICBleHBpcmVzPXtiYW4uZXhwaXJlc19vbiA/IG1vbWVudChiYW4uZXhwaXJlc19vbikgOiBudWxsfSAvPlxuICAgIDwvUHJvdmlkZXI+LFxuICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3BhZ2UtbW91bnQnKVxuICApO1xuXG4gIGlmICh0eXBlb2YgY2hhbmdlU3RhdGUgPT09ICd1bmRlZmluZWQnIHx8ICFjaGFuZ2VTdGF0ZSkge1xuICAgIGxldCBmb3J1bU5hbWUgPSBtaXNhZ28uZ2V0KCdTRVRUSU5HUycpLmZvcnVtX25hbWU7XG4gICAgZG9jdW1lbnQudGl0bGUgPSBnZXR0ZXh0KFwiWW91IGFyZSBiYW5uZWRcIikgKyAnIHwgJyArIGZvcnVtTmFtZTtcbiAgICB3aW5kb3cuaGlzdG9yeS5wdXNoU3RhdGUoe30sIFwiXCIsIG1pc2Fnby5nZXQoJ0JBTk5FRF9VUkwnKSk7XG4gIH1cbn0iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnOyAvLyBqc2hpbnQgaWdub3JlOmxpbmVcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IHsgUHJvdmlkZXIgfSBmcm9tICdyZWFjdC1yZWR1eCc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuaW1wb3J0IHN0b3JlIGZyb20gJ21pc2Fnby9zZXJ2aWNlcy9zdG9yZSc7IC8vIGpzaGludCBpZ25vcmU6bGluZVxuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBtb3VudChDb21wb25lbnQsIHJvb3RFbGVtZW50SWQsIGNvbm5lY3RlZD10cnVlKSB7XG4gIGxldCByb290RWxlbWVudCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKHJvb3RFbGVtZW50SWQpO1xuXG4gIGlmIChyb290RWxlbWVudCkge1xuICAgIGlmIChjb25uZWN0ZWQpIHtcbiAgICAgIFJlYWN0RE9NLnJlbmRlcihcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTpzdGFydCAqL1xuICAgICAgICA8UHJvdmlkZXIgc3RvcmU9e3N0b3JlLmdldFN0b3JlKCl9PlxuICAgICAgICAgIDxDb21wb25lbnQgLz5cbiAgICAgICAgPC9Qcm92aWRlcj4sXG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6ZW5kICovXG4gICAgICAgIHJvb3RFbGVtZW50XG4gICAgICApO1xuICAgIH0gZWxzZSB7XG4gICAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIC8qIGpzaGludCBpZ25vcmU6c3RhcnQgKi9cbiAgICAgICAgPENvbXBvbmVudCAvPixcbiAgICAgICAgLyoganNoaW50IGlnbm9yZTplbmQgKi9cbiAgICAgICAgcm9vdEVsZW1lbnRcbiAgICAgICk7XG4gICAgfVxuICB9XG59XG4iLCJjbGFzcyBPcmRlcmVkTGlzdCB7XG4gICAgY29uc3RydWN0b3IoaXRlbXMpIHtcbiAgICAgIHRoaXMuaXNPcmRlcmVkID0gZmFsc2U7XG4gICAgICB0aGlzLl9pdGVtcyA9IGl0ZW1zIHx8IFtdO1xuICAgIH1cblxuICAgIGFkZChrZXksIGl0ZW0sIG9yZGVyKSB7XG4gICAgICB0aGlzLl9pdGVtcy5wdXNoKHtcbiAgICAgICAga2V5OiBrZXksXG4gICAgICAgIGl0ZW06IGl0ZW0sXG5cbiAgICAgICAgYWZ0ZXI6IG9yZGVyID8gb3JkZXIuYWZ0ZXIgfHwgbnVsbCA6IG51bGwsXG4gICAgICAgIGJlZm9yZTogb3JkZXIgPyBvcmRlci5iZWZvcmUgfHwgbnVsbCA6IG51bGxcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGdldChrZXksIHZhbHVlKSB7XG4gICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMuX2l0ZW1zLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIGlmICh0aGlzLl9pdGVtc1tpXS5rZXkgPT09IGtleSkge1xuICAgICAgICAgIHJldHVybiB0aGlzLl9pdGVtc1tpXS5pdGVtO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIHJldHVybiB2YWx1ZTtcbiAgICB9XG5cbiAgICBoYXMoa2V5KSB7XG4gICAgICByZXR1cm4gdGhpcy5nZXQoa2V5KSAhPT0gdW5kZWZpbmVkO1xuICAgIH1cblxuICAgIHZhbHVlcygpIHtcbiAgICAgIHZhciB2YWx1ZXMgPSBbXTtcbiAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5faXRlbXMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgdmFsdWVzLnB1c2godGhpcy5faXRlbXNbaV0uaXRlbSk7XG4gICAgICB9XG4gICAgICByZXR1cm4gdmFsdWVzO1xuICAgIH1cblxuICAgIG9yZGVyKHZhbHVlc19vbmx5KSB7XG4gICAgICBpZiAoIXRoaXMuaXNPcmRlcmVkKSB7XG4gICAgICAgIHRoaXMuX2l0ZW1zID0gdGhpcy5fb3JkZXIodGhpcy5faXRlbXMpO1xuICAgICAgICB0aGlzLmlzT3JkZXJlZCA9IHRydWU7XG4gICAgICB9XG5cbiAgICAgIGlmICh2YWx1ZXNfb25seSB8fCB0eXBlb2YgdmFsdWVzX29ubHkgPT09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgIHJldHVybiB0aGlzLnZhbHVlcygpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuX2l0ZW1zO1xuICAgICAgfVxuICAgIH1cblxuICAgIG9yZGVyZWRWYWx1ZXMoKSB7XG4gICAgICByZXR1cm4gdGhpcy5vcmRlcih0cnVlKTtcbiAgICB9XG5cbiAgICBfb3JkZXIodW5vcmRlcmVkKSB7XG4gICAgICAvLyBJbmRleCBvZiB1bm9yZGVyZWQgaXRlbXNcbiAgICAgIHZhciBpbmRleCA9IFtdO1xuICAgICAgdW5vcmRlcmVkLmZvckVhY2goZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICAgICAgaW5kZXgucHVzaChpdGVtLmtleSk7XG4gICAgICB9KTtcblxuICAgICAgLy8gT3JkZXJlZCBpdGVtc1xuICAgICAgdmFyIG9yZGVyZWQgPSBbXTtcbiAgICAgIHZhciBvcmRlcmluZyA9IFtdO1xuXG4gICAgICAvLyBGaXJzdCBwYXNzOiByZWdpc3RlciBpdGVtcyB0aGF0XG4gICAgICAvLyBkb24ndCBzcGVjaWZ5IHRoZWlyIG9yZGVyXG4gICAgICB1bm9yZGVyZWQuZm9yRWFjaChmdW5jdGlvbiAoaXRlbSkge1xuICAgICAgICBpZiAoIWl0ZW0uYWZ0ZXIgJiYgIWl0ZW0uYmVmb3JlKSB7XG4gICAgICAgICAgb3JkZXJlZC5wdXNoKGl0ZW0pO1xuICAgICAgICAgIG9yZGVyaW5nLnB1c2goaXRlbS5rZXkpO1xuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgLy8gU2Vjb25kIHBhc3M6IHJlZ2lzdGVyIGl0ZW1zIHRoYXRcbiAgICAgIC8vIHNwZWNpZnkgdGhlaXIgYmVmb3JlIHRvIFwiX2VuZFwiXG4gICAgICB1bm9yZGVyZWQuZm9yRWFjaChmdW5jdGlvbiAoaXRlbSkge1xuICAgICAgICBpZiAoaXRlbS5iZWZvcmUgPT09IFwiX2VuZFwiKSB7XG4gICAgICAgICAgb3JkZXJlZC5wdXNoKGl0ZW0pO1xuICAgICAgICAgIG9yZGVyaW5nLnB1c2goaXRlbS5rZXkpO1xuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgLy8gVGhpcmQgcGFzczoga2VlcCBpdGVyYXRpbmcgaXRlbXNcbiAgICAgIC8vIHVudGlsIHdlIGhpdCBpdGVyYXRpb25zIGxpbWl0IG9yIGZpbmlzaFxuICAgICAgLy8gb3JkZXJpbmcgbGlzdFxuICAgICAgZnVuY3Rpb24gaW5zZXJ0SXRlbShpdGVtKSB7XG4gICAgICAgIHZhciBpbnNlcnRBdCA9IC0xO1xuICAgICAgICBpZiAob3JkZXJpbmcuaW5kZXhPZihpdGVtLmtleSkgPT09IC0xKSB7XG4gICAgICAgICAgaWYgKGl0ZW0uYWZ0ZXIpIHtcbiAgICAgICAgICAgIGluc2VydEF0ID0gb3JkZXJpbmcuaW5kZXhPZihpdGVtLmFmdGVyKTtcbiAgICAgICAgICAgIGlmIChpbnNlcnRBdCAhPT0gLTEpIHtcbiAgICAgICAgICAgICAgaW5zZXJ0QXQgKz0gMTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9IGVsc2UgaWYgKGl0ZW0uYmVmb3JlKSB7XG4gICAgICAgICAgICBpbnNlcnRBdCA9IG9yZGVyaW5nLmluZGV4T2YoaXRlbS5iZWZvcmUpO1xuICAgICAgICAgIH1cblxuICAgICAgICAgIGlmIChpbnNlcnRBdCAhPT0gLTEpIHtcbiAgICAgICAgICAgIG9yZGVyZWQuc3BsaWNlKGluc2VydEF0LCAwLCBpdGVtKTtcbiAgICAgICAgICAgIG9yZGVyaW5nLnNwbGljZShpbnNlcnRBdCwgMCwgaXRlbS5rZXkpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuXG4gICAgICB2YXIgaXRlcmF0aW9ucyA9IDIwMDtcbiAgICAgIHdoaWxlIChpdGVyYXRpb25zID4gMCAmJiBpbmRleC5sZW5ndGggIT09IG9yZGVyaW5nLmxlbmd0aCkge1xuICAgICAgICBpdGVyYXRpb25zIC09IDE7XG4gICAgICAgIHVub3JkZXJlZC5mb3JFYWNoKGluc2VydEl0ZW0pO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gb3JkZXJlZDtcbiAgICB9XG4gIH1cblxuICBleHBvcnQgZGVmYXVsdCBPcmRlcmVkTGlzdDtcbiIsImNvbnN0IEVNQUlMID0gL14oKFtePD4oKVtcXF1cXC4sOzpcXHNAXFxcIl0rKFxcLltePD4oKVtcXF1cXC4sOzpcXHNAXFxcIl0rKSopfChcXFwiLitcXFwiKSlAKChbXjw+KClbXFxdXFwuLDs6XFxzQFxcXCJdK1xcLikrW148PigpW1xcXVxcLiw7Olxcc0BcXFwiXXsyLH0pJC9pO1xuY29uc3QgVVNFUk5BTUUgPSBuZXcgUmVnRXhwKCdeWzAtOWEtel0rJCcsICdpJyk7XG5cbmV4cG9ydCBmdW5jdGlvbiByZXF1aXJlZCgpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgaWYgKCQudHJpbSh2YWx1ZSkubGVuZ3RoID09PSAwKSB7XG4gICAgICByZXR1cm4gZ2V0dGV4dChcIlRoaXMgZmllbGQgaXMgcmVxdWlyZWQuXCIpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGVtYWlsKG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgaWYgKCFFTUFJTC50ZXN0KHZhbHVlKSkge1xuICAgICAgcmV0dXJuIG1lc3NhZ2UgfHwgZ2V0dGV4dChcIkVudGVyIGEgdmFsaWQgZW1haWwgYWRkcmVzcy5cIik7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gbWluTGVuZ3RoKGxpbWl0VmFsdWUsIG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgdmFyIHJldHVybk1lc3NhZ2UgPSAnJztcbiAgICB2YXIgbGVuZ3RoID0gJC50cmltKHZhbHVlKS5sZW5ndGg7XG5cbiAgICBpZiAobGVuZ3RoIDwgbGltaXRWYWx1ZSkge1xuICAgICAgaWYgKG1lc3NhZ2UpIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG1lc3NhZ2UobGltaXRWYWx1ZSwgbGVuZ3RoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybk1lc3NhZ2UgPSBuZ2V0dGV4dChcbiAgICAgICAgICBcIkVuc3VyZSB0aGlzIHZhbHVlIGhhcyBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIChpdCBoYXMgJShzaG93X3ZhbHVlKXMpLlwiLFxuICAgICAgICAgIFwiRW5zdXJlIHRoaXMgdmFsdWUgaGFzIGF0IGxlYXN0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXJzIChpdCBoYXMgJShzaG93X3ZhbHVlKXMpLlwiLFxuICAgICAgICAgIGxpbWl0VmFsdWUpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGludGVycG9sYXRlKHJldHVybk1lc3NhZ2UsIHtcbiAgICAgICAgbGltaXRfdmFsdWU6IGxpbWl0VmFsdWUsXG4gICAgICAgIHNob3dfdmFsdWU6IGxlbmd0aFxuICAgICAgfSwgdHJ1ZSk7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gbWF4TGVuZ3RoKGxpbWl0VmFsdWUsIG1lc3NhZ2UpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uKHZhbHVlKSB7XG4gICAgdmFyIHJldHVybk1lc3NhZ2UgPSAnJztcbiAgICB2YXIgbGVuZ3RoID0gJC50cmltKHZhbHVlKS5sZW5ndGg7XG5cbiAgICBpZiAobGVuZ3RoID4gbGltaXRWYWx1ZSkge1xuICAgICAgaWYgKG1lc3NhZ2UpIHtcbiAgICAgICAgcmV0dXJuTWVzc2FnZSA9IG1lc3NhZ2UobGltaXRWYWx1ZSwgbGVuZ3RoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybk1lc3NhZ2UgPSBuZ2V0dGV4dChcbiAgICAgICAgICBcIkVuc3VyZSB0aGlzIHZhbHVlIGhhcyBhdCBtb3N0ICUobGltaXRfdmFsdWUpcyBjaGFyYWN0ZXIgKGl0IGhhcyAlKHNob3dfdmFsdWUpcykuXCIsXG4gICAgICAgICAgXCJFbnN1cmUgdGhpcyB2YWx1ZSBoYXMgYXQgbW9zdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVycyAoaXQgaGFzICUoc2hvd192YWx1ZSlzKS5cIixcbiAgICAgICAgICBsaW1pdFZhbHVlKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBpbnRlcnBvbGF0ZShyZXR1cm5NZXNzYWdlLCB7XG4gICAgICAgIGxpbWl0X3ZhbHVlOiBsaW1pdFZhbHVlLFxuICAgICAgICBzaG93X3ZhbHVlOiBsZW5ndGhcbiAgICAgIH0sIHRydWUpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVzZXJuYW1lTWluTGVuZ3RoKHNldHRpbmdzKSB7XG4gIHZhciBtZXNzYWdlID0gZnVuY3Rpb24obGltaXRWYWx1ZSkge1xuICAgIHJldHVybiBuZ2V0dGV4dChcbiAgICAgIFwiVXNlcm5hbWUgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIGxvbmcuXCIsXG4gICAgICBcIlVzZXJuYW1lIG11c3QgYmUgYXQgbGVhc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMgbG9uZy5cIixcbiAgICAgIGxpbWl0VmFsdWUpO1xuICB9O1xuICByZXR1cm4gdGhpcy5taW5MZW5ndGgoc2V0dGluZ3MudXNlcm5hbWVfbGVuZ3RoX21pbiwgbWVzc2FnZSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VybmFtZU1heExlbmd0aChzZXR0aW5ncykge1xuICB2YXIgbWVzc2FnZSA9IGZ1bmN0aW9uKGxpbWl0VmFsdWUpIHtcbiAgICByZXR1cm4gbmdldHRleHQoXG4gICAgICBcIlVzZXJuYW1lIGNhbm5vdCBiZSBsb25nZXIgdGhhbiAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyLlwiLFxuICAgICAgXCJVc2VybmFtZSBjYW5ub3QgYmUgbG9uZ2VyIHRoYW4gJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMuXCIsXG4gICAgICBsaW1pdFZhbHVlKTtcbiAgfTtcbiAgcmV0dXJuIHRoaXMubWF4TGVuZ3RoKHNldHRpbmdzLnVzZXJuYW1lX2xlbmd0aF9tYXgsIG1lc3NhZ2UpO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlcm5hbWVDb250ZW50KCkge1xuICByZXR1cm4gZnVuY3Rpb24odmFsdWUpIHtcbiAgICBpZiAoIVVTRVJOQU1FLnRlc3QoJC50cmltKHZhbHVlKSkpIHtcbiAgICAgIHJldHVybiBnZXR0ZXh0KFwiVXNlcm5hbWUgY2FuIG9ubHkgY29udGFpbiBsYXRpbiBhbHBoYWJldCBsZXR0ZXJzIGFuZCBkaWdpdHMuXCIpO1xuICAgIH1cbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHBhc3N3b3JkTWluTGVuZ3RoKHNldHRpbmdzKSB7XG4gIHZhciBtZXNzYWdlID0gZnVuY3Rpb24obGltaXRWYWx1ZSkge1xuICAgIHJldHVybiBuZ2V0dGV4dChcbiAgICAgIFwiVmFsaWQgcGFzc3dvcmQgbXVzdCBiZSBhdCBsZWFzdCAlKGxpbWl0X3ZhbHVlKXMgY2hhcmFjdGVyIGxvbmcuXCIsXG4gICAgICBcIlZhbGlkIHBhc3N3b3JkIG11c3QgYmUgYXQgbGVhc3QgJShsaW1pdF92YWx1ZSlzIGNoYXJhY3RlcnMgbG9uZy5cIixcbiAgICAgIGxpbWl0VmFsdWUpO1xuICB9O1xuICByZXR1cm4gdGhpcy5taW5MZW5ndGgoc2V0dGluZ3MucGFzc3dvcmRfbGVuZ3RoX21pbiwgbWVzc2FnZSk7XG59Il19
