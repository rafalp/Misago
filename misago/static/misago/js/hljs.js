"use strict";
(self["webpackChunkmisago"] = self["webpackChunkmisago"] || []).push([["hljs"],{

/***/ "./highlight/highlight.js":
/*!********************************!*\
  !*** ./highlight/highlight.js ***!
  \********************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _babel_runtime_helpers_wrapNativeSuper__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/wrapNativeSuper */ "./node_modules/@babel/runtime/helpers/esm/wrapNativeSuper.js");
/* harmony import */ var _babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime/helpers/slicedToArray */ "./node_modules/@babel/runtime/helpers/esm/slicedToArray.js");
/* harmony import */ var _babel_runtime_helpers_inherits__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @babel/runtime/helpers/inherits */ "./node_modules/@babel/runtime/helpers/esm/inherits.js");
/* harmony import */ var _babel_runtime_helpers_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @babel/runtime/helpers/possibleConstructorReturn */ "./node_modules/@babel/runtime/helpers/esm/possibleConstructorReturn.js");
/* harmony import */ var _babel_runtime_helpers_getPrototypeOf__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @babel/runtime/helpers/getPrototypeOf */ "./node_modules/@babel/runtime/helpers/esm/getPrototypeOf.js");
/* harmony import */ var _babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @babel/runtime/helpers/toConsumableArray */ "./node_modules/@babel/runtime/helpers/esm/toConsumableArray.js");
/* harmony import */ var _babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @babel/runtime/helpers/classCallCheck */ "./node_modules/@babel/runtime/helpers/esm/classCallCheck.js");
/* harmony import */ var _babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @babel/runtime/helpers/createClass */ "./node_modules/@babel/runtime/helpers/esm/createClass.js");
/* harmony import */ var _babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @babel/runtime/helpers/typeof */ "./node_modules/@babel/runtime/helpers/esm/typeof.js");
/* module decorator */ module = __webpack_require__.hmd(module);









function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e8) { throw _e8; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e9) { didErr = true; err = _e9; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }
function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }
function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }
function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = (0,_babel_runtime_helpers_getPrototypeOf__WEBPACK_IMPORTED_MODULE_4__["default"])(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = (0,_babel_runtime_helpers_getPrototypeOf__WEBPACK_IMPORTED_MODULE_4__["default"])(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return (0,_babel_runtime_helpers_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_3__["default"])(this, result); }; }
function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})); return true; } catch (e) { return false; } }
/*!
  Highlight.js v11.7.0 (git: 82688fad18)
  (c) 2006-2022 undefined and other contributors
  License: BSD-3-Clause
 */
var hljs = function () {
  "use strict";

  var e = {
    exports: {}
  };
  function t(e) {
    return e instanceof Map ? e.clear = e["delete"] = e.set = function () {
      throw Error("map is read-only");
    } : e instanceof Set && (e.add = e.clear = e["delete"] = function () {
      throw Error("set is read-only");
    }), Object.freeze(e), Object.getOwnPropertyNames(e).forEach(function (n) {
      var i = e[n];
      "object" != (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(i) || Object.isFrozen(i) || t(i);
    }), e;
  }
  e.exports = t, e.exports["default"] = t;
  var n = /*#__PURE__*/function () {
    function n(e) {
      (0,_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__["default"])(this, n);
      void 0 === e.data && (e.data = {}), this.data = e.data, this.isMatchIgnored = !1;
    }
    (0,_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__["default"])(n, [{
      key: "ignoreMatch",
      value: function ignoreMatch() {
        this.isMatchIgnored = !0;
      }
    }]);
    return n;
  }();
  function i(e) {
    return e.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
  }
  function r(e) {
    var n = Object.create(null);
    for (var _t in e) {
      n[_t] = e[_t];
    }
    for (var _len = arguments.length, t = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
      t[_key - 1] = arguments[_key];
    }
    return t.forEach(function (e) {
      for (var _t2 in e) {
        n[_t2] = e[_t2];
      }
    }), n;
  }
  var s = function s(e) {
    return !!e.scope || e.sublanguage && e.language;
  };
  var o = /*#__PURE__*/function () {
    function o(e, t) {
      (0,_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__["default"])(this, o);
      this.buffer = "", this.classPrefix = t.classPrefix, e.walk(this);
    }
    (0,_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__["default"])(o, [{
      key: "addText",
      value: function addText(e) {
        this.buffer += i(e);
      }
    }, {
      key: "openNode",
      value: function openNode(e) {
        if (!s(e)) return;
        var t = "";
        t = e.sublanguage ? "language-" + e.language : function (e, _ref) {
          var t = _ref.prefix;
          if (e.includes(".")) {
            var _n = e.split(".");
            return ["".concat(t).concat(_n.shift())].concat((0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(_n.map(function (e, t) {
              return "".concat(e).concat("_".repeat(t + 1));
            }))).join(" ");
          }
          return "".concat(t).concat(e);
        }(e.scope, {
          prefix: this.classPrefix
        }), this.span(t);
      }
    }, {
      key: "closeNode",
      value: function closeNode(e) {
        s(e) && (this.buffer += "</span>");
      }
    }, {
      key: "value",
      value: function value() {
        return this.buffer;
      }
    }, {
      key: "span",
      value: function span(e) {
        this.buffer += "<span class=\"".concat(e, "\">");
      }
    }]);
    return o;
  }();
  var a = function a() {
    var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var t = {
      children: []
    };
    return Object.assign(t, e), t;
  };
  var c = /*#__PURE__*/function () {
    function c() {
      (0,_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__["default"])(this, c);
      this.rootNode = a(), this.stack = [this.rootNode];
    }
    (0,_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__["default"])(c, [{
      key: "top",
      get: function get() {
        return this.stack[this.stack.length - 1];
      }
    }, {
      key: "root",
      get: function get() {
        return this.rootNode;
      }
    }, {
      key: "add",
      value: function add(e) {
        this.top.children.push(e);
      }
    }, {
      key: "openNode",
      value: function openNode(e) {
        var t = a({
          scope: e
        });
        this.add(t), this.stack.push(t);
      }
    }, {
      key: "closeNode",
      value: function closeNode() {
        if (this.stack.length > 1) return this.stack.pop();
      }
    }, {
      key: "closeAllNodes",
      value: function closeAllNodes() {
        for (; this.closeNode();) {
          ;
        }
      }
    }, {
      key: "toJSON",
      value: function toJSON() {
        return JSON.stringify(this.rootNode, null, 4);
      }
    }, {
      key: "walk",
      value: function walk(e) {
        return this.constructor._walk(e, this.rootNode);
      }
    }], [{
      key: "_walk",
      value: function _walk(e, t) {
        var _this = this;
        return "string" == typeof t ? e.addText(t) : t.children && (e.openNode(t), t.children.forEach(function (t) {
          return _this._walk(e, t);
        }), e.closeNode(t)), e;
      }
    }, {
      key: "_collapse",
      value: function _collapse(e) {
        "string" != typeof e && e.children && (e.children.every(function (e) {
          return "string" == typeof e;
        }) ? e.children = [e.children.join("")] : e.children.forEach(function (e) {
          c._collapse(e);
        }));
      }
    }]);
    return c;
  }();
  var l = /*#__PURE__*/function (_c) {
    (0,_babel_runtime_helpers_inherits__WEBPACK_IMPORTED_MODULE_2__["default"])(l, _c);
    var _super = _createSuper(l);
    function l(e) {
      var _this2;
      (0,_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__["default"])(this, l);
      _this2 = _super.call(this), _this2.options = e;
      return _this2;
    }
    (0,_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__["default"])(l, [{
      key: "addKeyword",
      value: function addKeyword(e, t) {
        "" !== e && (this.openNode(t), this.addText(e), this.closeNode());
      }
    }, {
      key: "addText",
      value: function addText(e) {
        "" !== e && this.add(e);
      }
    }, {
      key: "addSublanguage",
      value: function addSublanguage(e, t) {
        var n = e.root;
        n.sublanguage = !0, n.language = t, this.add(n);
      }
    }, {
      key: "toHTML",
      value: function toHTML() {
        return new o(this, this.options).value();
      }
    }, {
      key: "finalize",
      value: function finalize() {
        return !0;
      }
    }]);
    return l;
  }(c);
  function g(e) {
    return e ? "string" == typeof e ? e : e.source : null;
  }
  function d(e) {
    return p("(?=", e, ")");
  }
  function u(e) {
    return p("(?:", e, ")*");
  }
  function h(e) {
    return p("(?:", e, ")?");
  }
  function p() {
    for (var _len2 = arguments.length, e = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
      e[_key2] = arguments[_key2];
    }
    return e.map(function (e) {
      return g(e);
    }).join("");
  }
  function f() {
    for (var _len3 = arguments.length, e = new Array(_len3), _key3 = 0; _key3 < _len3; _key3++) {
      e[_key3] = arguments[_key3];
    }
    var t = function (e) {
      var t = e[e.length - 1];
      return "object" == (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(t) && t.constructor === Object ? (e.splice(e.length - 1, 1), t) : {};
    }(e);
    return "(" + (t.capture ? "" : "?:") + e.map(function (e) {
      return g(e);
    }).join("|") + ")";
  }
  function b(e) {
    return RegExp(e.toString() + "|").exec("").length - 1;
  }
  var m = /\[(?:[^\\\]]|\\.)*\]|\(\??|\\([1-9][0-9]*)|\\./;
  function E(e, _ref2) {
    var t = _ref2.joinWith;
    var n = 0;
    return e.map(function (e) {
      n += 1;
      var t = n;
      var i = g(e),
        r = "";
      for (; i.length > 0;) {
        var _e = m.exec(i);
        if (!_e) {
          r += i;
          break;
        }
        r += i.substring(0, _e.index), i = i.substring(_e.index + _e[0].length), "\\" === _e[0][0] && _e[1] ? r += "\\" + (Number(_e[1]) + t) : (r += _e[0], "(" === _e[0] && n++);
      }
      return r;
    }).map(function (e) {
      return "(".concat(e, ")");
    }).join(t);
  }
  var x = "[a-zA-Z]\\w*",
    w = "[a-zA-Z_]\\w*",
    y = "\\b\\d+(\\.\\d+)?",
    _ = "(-?)(\\b0[xX][a-fA-F0-9]+|(\\b\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]?\\d+)?)",
    O = "\\b(0b[01]+)",
    v = {
      begin: "\\\\[\\s\\S]",
      relevance: 0
    },
    N = {
      scope: "string",
      begin: "'",
      end: "'",
      illegal: "\\n",
      contains: [v]
    },
    k = {
      scope: "string",
      begin: '"',
      end: '"',
      illegal: "\\n",
      contains: [v]
    },
    M = function M(e, t) {
      var n = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
      var i = r({
        scope: "comment",
        begin: e,
        end: t,
        contains: []
      }, n);
      i.contains.push({
        scope: "doctag",
        begin: "[ ]*(?=(TODO|FIXME|NOTE|BUG|OPTIMIZE|HACK|XXX):)",
        end: /(TODO|FIXME|NOTE|BUG|OPTIMIZE|HACK|XXX):/,
        excludeBegin: !0,
        relevance: 0
      });
      var s = f("I", "a", "is", "so", "us", "to", "at", "if", "in", "it", "on", /[A-Za-z]+['](d|ve|re|ll|t|s|n)/, /[A-Za-z]+[-][a-z]+/, /[A-Za-z][a-z]{2,}/);
      return i.contains.push({
        begin: p(/[ ]+/, "(", s, /[.]?[:]?([.][ ]|[ ])/, "){3}")
      }), i;
    },
    S = M("//", "$"),
    R = M("/\\*", "\\*/"),
    j = M("#", "$");
  var A = Object.freeze({
    __proto__: null,
    MATCH_NOTHING_RE: /\b\B/,
    IDENT_RE: x,
    UNDERSCORE_IDENT_RE: w,
    NUMBER_RE: y,
    C_NUMBER_RE: _,
    BINARY_NUMBER_RE: O,
    RE_STARTERS_RE: "!|!=|!==|%|%=|&|&&|&=|\\*|\\*=|\\+|\\+=|,|-|-=|/=|/|:|;|<<|<<=|<=|<|===|==|=|>>>=|>>=|>=|>>>|>>|>|\\?|\\[|\\{|\\(|\\^|\\^=|\\||\\|=|\\|\\||~",
    SHEBANG: function SHEBANG() {
      var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      var t = /^#![ ]*\//;
      return e.binary && (e.begin = p(t, /.*\b/, e.binary, /\b.*/)), r({
        scope: "meta",
        begin: t,
        end: /$/,
        relevance: 0,
        "on:begin": function onBegin(e, t) {
          0 !== e.index && t.ignoreMatch();
        }
      }, e);
    },
    BACKSLASH_ESCAPE: v,
    APOS_STRING_MODE: N,
    QUOTE_STRING_MODE: k,
    PHRASAL_WORDS_MODE: {
      begin: /\b(a|an|the|are|I'm|isn't|don't|doesn't|won't|but|just|should|pretty|simply|enough|gonna|going|wtf|so|such|will|you|your|they|like|more)\b/
    },
    COMMENT: M,
    C_LINE_COMMENT_MODE: S,
    C_BLOCK_COMMENT_MODE: R,
    HASH_COMMENT_MODE: j,
    NUMBER_MODE: {
      scope: "number",
      begin: y,
      relevance: 0
    },
    C_NUMBER_MODE: {
      scope: "number",
      begin: _,
      relevance: 0
    },
    BINARY_NUMBER_MODE: {
      scope: "number",
      begin: O,
      relevance: 0
    },
    REGEXP_MODE: {
      begin: /(?=\/[^/\n]*\/)/,
      contains: [{
        scope: "regexp",
        begin: /\//,
        end: /\/[gimuy]*/,
        illegal: /\n/,
        contains: [v, {
          begin: /\[/,
          end: /\]/,
          relevance: 0,
          contains: [v]
        }]
      }]
    },
    TITLE_MODE: {
      scope: "title",
      begin: x,
      relevance: 0
    },
    UNDERSCORE_TITLE_MODE: {
      scope: "title",
      begin: w,
      relevance: 0
    },
    METHOD_GUARD: {
      begin: "\\.\\s*[a-zA-Z_]\\w*",
      relevance: 0
    },
    END_SAME_AS_BEGIN: function END_SAME_AS_BEGIN(e) {
      return Object.assign(e, {
        "on:begin": function onBegin(e, t) {
          t.data._beginMatch = e[1];
        },
        "on:end": function onEnd(e, t) {
          t.data._beginMatch !== e[1] && t.ignoreMatch();
        }
      });
    }
  });
  function I(e, t) {
    "." === e.input[e.index - 1] && t.ignoreMatch();
  }
  function T(e, t) {
    void 0 !== e.className && (e.scope = e.className, delete e.className);
  }
  function L(e, t) {
    t && e.beginKeywords && (e.begin = "\\b(" + e.beginKeywords.split(" ").join("|") + ")(?!\\.)(?=\\b|\\s)", e.__beforeBegin = I, e.keywords = e.keywords || e.beginKeywords, delete e.beginKeywords, void 0 === e.relevance && (e.relevance = 0));
  }
  function B(e, t) {
    Array.isArray(e.illegal) && (e.illegal = f.apply(void 0, (0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(e.illegal)));
  }
  function D(e, t) {
    if (e.match) {
      if (e.begin || e.end) throw Error("begin & end are not supported with match");
      e.begin = e.match, delete e.match;
    }
  }
  function H(e, t) {
    void 0 === e.relevance && (e.relevance = 1);
  }
  var P = function P(e, t) {
      if (!e.beforeMatch) return;
      if (e.starts) throw Error("beforeMatch cannot be used with starts");
      var n = Object.assign({}, e);
      Object.keys(e).forEach(function (t) {
        delete e[t];
      }), e.keywords = n.keywords, e.begin = p(n.beforeMatch, d(n.begin)), e.starts = {
        relevance: 0,
        contains: [Object.assign(n, {
          endsParent: !0
        })]
      }, e.relevance = 0, delete n.beforeMatch;
    },
    C = ["of", "and", "for", "in", "not", "or", "if", "then", "parent", "list", "value"];
  function $(e, t) {
    var n = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "keyword";
    var i = Object.create(null);
    return "string" == typeof e ? r(n, e.split(" ")) : Array.isArray(e) ? r(n, e) : Object.keys(e).forEach(function (n) {
      Object.assign(i, $(e[n], t, n));
    }), i;
    function r(e, n) {
      t && (n = n.map(function (e) {
        return e.toLowerCase();
      })), n.forEach(function (t) {
        var n = t.split("|");
        i[n[0]] = [e, U(n[0], n[1])];
      });
    }
  }
  function U(e, t) {
    return t ? Number(t) : function (e) {
      return C.includes(e.toLowerCase());
    }(e) ? 0 : 1;
  }
  var z = {},
    K = function K(e) {
      console.error(e);
    },
    W = function W(e) {
      var _console;
      for (var _len4 = arguments.length, t = new Array(_len4 > 1 ? _len4 - 1 : 0), _key4 = 1; _key4 < _len4; _key4++) {
        t[_key4 - 1] = arguments[_key4];
      }
      (_console = console).log.apply(_console, ["WARN: " + e].concat(t));
    },
    X = function X(e, t) {
      z["".concat(e, "/").concat(t)] || (console.log("Deprecated as of ".concat(e, ". ").concat(t)), z["".concat(e, "/").concat(t)] = !0);
    },
    G = Error();
  function Z(e, t, _ref3) {
    var n = _ref3.key;
    var i = 0;
    var r = e[n],
      s = {},
      o = {};
    for (var _e2 = 1; _e2 <= t.length; _e2++) {
      o[_e2 + i] = r[_e2], s[_e2 + i] = !0, i += b(t[_e2 - 1]);
    }
    e[n] = o, e[n]._emit = s, e[n]._multi = !0;
  }
  function F(e) {
    (function (e) {
      e.scope && "object" == (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(e.scope) && null !== e.scope && (e.beginScope = e.scope, delete e.scope);
    })(e), "string" == typeof e.beginScope && (e.beginScope = {
      _wrap: e.beginScope
    }), "string" == typeof e.endScope && (e.endScope = {
      _wrap: e.endScope
    }), function (e) {
      if (Array.isArray(e.begin)) {
        if (e.skip || e.excludeBegin || e.returnBegin) throw K("skip, excludeBegin, returnBegin not compatible with beginScope: {}"), G;
        if ("object" != (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(e.beginScope) || null === e.beginScope) throw K("beginScope must be object"), G;
        Z(e, e.begin, {
          key: "beginScope"
        }), e.begin = E(e.begin, {
          joinWith: ""
        });
      }
    }(e), function (e) {
      if (Array.isArray(e.end)) {
        if (e.skip || e.excludeEnd || e.returnEnd) throw K("skip, excludeEnd, returnEnd not compatible with endScope: {}"), G;
        if ("object" != (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(e.endScope) || null === e.endScope) throw K("endScope must be object"), G;
        Z(e, e.end, {
          key: "endScope"
        }), e.end = E(e.end, {
          joinWith: ""
        });
      }
    }(e);
  }
  function V(e) {
    function t(t, n) {
      return RegExp(g(t), "m" + (e.case_insensitive ? "i" : "") + (e.unicodeRegex ? "u" : "") + (n ? "g" : ""));
    }
    var n = /*#__PURE__*/function () {
      function n() {
        (0,_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__["default"])(this, n);
        this.matchIndexes = {}, this.regexes = [], this.matchAt = 1, this.position = 0;
      }
      (0,_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__["default"])(n, [{
        key: "addRule",
        value: function addRule(e, t) {
          t.position = this.position++, this.matchIndexes[this.matchAt] = t, this.regexes.push([t, e]), this.matchAt += b(e) + 1;
        }
      }, {
        key: "compile",
        value: function compile() {
          0 === this.regexes.length && (this.exec = function () {
            return null;
          });
          var e = this.regexes.map(function (e) {
            return e[1];
          });
          this.matcherRe = t(E(e, {
            joinWith: "|"
          }), !0), this.lastIndex = 0;
        }
      }, {
        key: "exec",
        value: function exec(e) {
          this.matcherRe.lastIndex = this.lastIndex;
          var t = this.matcherRe.exec(e);
          if (!t) return null;
          var _n2 = t.findIndex(function (e, t) {
              return t > 0 && void 0 !== e;
            }),
            i = this.matchIndexes[_n2];
          return t.splice(0, _n2), Object.assign(t, i);
        }
      }]);
      return n;
    }();
    var i = /*#__PURE__*/function () {
      function i() {
        (0,_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__["default"])(this, i);
        this.rules = [], this.multiRegexes = [], this.count = 0, this.lastIndex = 0, this.regexIndex = 0;
      }
      (0,_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__["default"])(i, [{
        key: "getMatcher",
        value: function getMatcher(e) {
          if (this.multiRegexes[e]) return this.multiRegexes[e];
          var t = new n();
          return this.rules.slice(e).forEach(function (_ref4) {
            var _ref5 = (0,_babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1__["default"])(_ref4, 2),
              e = _ref5[0],
              n = _ref5[1];
            return t.addRule(e, n);
          }), t.compile(), this.multiRegexes[e] = t, t;
        }
      }, {
        key: "resumingScanAtSamePosition",
        value: function resumingScanAtSamePosition() {
          return 0 !== this.regexIndex;
        }
      }, {
        key: "considerAll",
        value: function considerAll() {
          this.regexIndex = 0;
        }
      }, {
        key: "addRule",
        value: function addRule(e, t) {
          this.rules.push([e, t]), "begin" === t.type && this.count++;
        }
      }, {
        key: "exec",
        value: function exec(e) {
          var t = this.getMatcher(this.regexIndex);
          t.lastIndex = this.lastIndex;
          var n = t.exec(e);
          if (this.resumingScanAtSamePosition()) if (n && n.index === this.lastIndex) ;else {
            var _t3 = this.getMatcher(0);
            _t3.lastIndex = this.lastIndex + 1, n = _t3.exec(e);
          }
          return n && (this.regexIndex += n.position + 1, this.regexIndex === this.count && this.considerAll()), n;
        }
      }]);
      return i;
    }();
    if (e.compilerExtensions || (e.compilerExtensions = []), e.contains && e.contains.includes("self")) throw Error("ERR: contains `self` is not supported at the top-level of a language.  See documentation.");
    return e.classNameAliases = r(e.classNameAliases || {}), function n(s, o) {
      var _ref6;
      var a = s;
      if (s.isCompiled) return a;
      [T, D, F, P].forEach(function (e) {
        return e(s, o);
      }), e.compilerExtensions.forEach(function (e) {
        return e(s, o);
      }), s.__beforeBegin = null, [L, B, H].forEach(function (e) {
        return e(s, o);
      }), s.isCompiled = !0;
      var c = null;
      return "object" == (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(s.keywords) && s.keywords.$pattern && (s.keywords = Object.assign({}, s.keywords), c = s.keywords.$pattern, delete s.keywords.$pattern), c = c || /\w+/, s.keywords && (s.keywords = $(s.keywords, e.case_insensitive)), a.keywordPatternRe = t(c, !0), o && (s.begin || (s.begin = /\B|\b/), a.beginRe = t(a.begin), s.end || s.endsWithParent || (s.end = /\B|\b/), s.end && (a.endRe = t(a.end)), a.terminatorEnd = g(a.end) || "", s.endsWithParent && o.terminatorEnd && (a.terminatorEnd += (s.end ? "|" : "") + o.terminatorEnd)), s.illegal && (a.illegalRe = t(s.illegal)), s.contains || (s.contains = []), s.contains = (_ref6 = []).concat.apply(_ref6, (0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(s.contains.map(function (e) {
        return function (e) {
          return e.variants && !e.cachedVariants && (e.cachedVariants = e.variants.map(function (t) {
            return r(e, {
              variants: null
            }, t);
          })), e.cachedVariants ? e.cachedVariants : q(e) ? r(e, {
            starts: e.starts ? r(e.starts) : null
          }) : Object.isFrozen(e) ? r(e) : e;
        }("self" === e ? s : e);
      }))), s.contains.forEach(function (e) {
        n(e, a);
      }), s.starts && n(s.starts, o), a.matcher = function (e) {
        var t = new i();
        return e.contains.forEach(function (e) {
          return t.addRule(e.begin, {
            rule: e,
            type: "begin"
          });
        }), e.terminatorEnd && t.addRule(e.terminatorEnd, {
          type: "end"
        }), e.illegal && t.addRule(e.illegal, {
          type: "illegal"
        }), t;
      }(a), a;
    }(e);
  }
  function q(e) {
    return !!e && (e.endsWithParent || q(e.starts));
  }
  var J = /*#__PURE__*/function (_Error) {
    (0,_babel_runtime_helpers_inherits__WEBPACK_IMPORTED_MODULE_2__["default"])(J, _Error);
    var _super2 = _createSuper(J);
    function J(e, t) {
      var _this3;
      (0,_babel_runtime_helpers_classCallCheck__WEBPACK_IMPORTED_MODULE_6__["default"])(this, J);
      _this3 = _super2.call(this, e), _this3.name = "HTMLInjectionError", _this3.html = t;
      return _this3;
    }
    return (0,_babel_runtime_helpers_createClass__WEBPACK_IMPORTED_MODULE_7__["default"])(J);
  }( /*#__PURE__*/(0,_babel_runtime_helpers_wrapNativeSuper__WEBPACK_IMPORTED_MODULE_0__["default"])(Error));
  var Y = i,
    Q = r,
    ee = Symbol("nomatch");
  var te = function (t) {
    var i = Object.create(null),
      r = Object.create(null),
      s = [];
    var o = !0;
    var a = "Could not find the language '{}', did you forget to load/include a language module?",
      c = {
        disableAutodetect: !0,
        name: "Plain text",
        contains: []
      };
    var g = {
      ignoreUnescapedHTML: !1,
      throwUnescapedHTML: !1,
      noHighlightRe: /^(no-?highlight)$/i,
      languageDetectRe: /\blang(?:uage)?-([\w-]+)\b/i,
      classPrefix: "hljs-",
      cssSelector: "pre code",
      languages: null,
      __emitter: l
    };
    function b(e) {
      return g.noHighlightRe.test(e);
    }
    function m(e, t, n) {
      var i = "",
        r = "";
      "object" == (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(t) ? (i = e, n = t.ignoreIllegals, r = t.language) : (X("10.7.0", "highlight(lang, code, ...args) has been deprecated."), X("10.7.0", "Please use highlight(code, options) instead.\nhttps://github.com/highlightjs/highlight.js/issues/2277"), r = e, i = t), void 0 === n && (n = !0);
      var s = {
        code: i,
        language: r
      };
      k("before:highlight", s);
      var o = s.result ? s.result : E(s.language, s.code, n);
      return o.code = s.code, k("after:highlight", o), o;
    }
    function E(e, t, r, s) {
      var c = Object.create(null);
      function l() {
        if (!N.keywords) return void M.addText(S);
        var e = 0;
        N.keywordPatternRe.lastIndex = 0;
        var t = N.keywordPatternRe.exec(S),
          n = "";
        for (; t;) {
          n += S.substring(e, t.index);
          var _r = y.case_insensitive ? t[0].toLowerCase() : t[0],
            _s = (i = _r, N.keywords[i]);
          if (_s) {
            var _s2 = (0,_babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1__["default"])(_s, 2),
              _e3 = _s2[0],
              _i = _s2[1];
            if (M.addText(n), n = "", c[_r] = (c[_r] || 0) + 1, c[_r] <= 7 && (R += _i), _e3.startsWith("_")) n += t[0];else {
              var _n3 = y.classNameAliases[_e3] || _e3;
              M.addKeyword(t[0], _n3);
            }
          } else n += t[0];
          e = N.keywordPatternRe.lastIndex, t = N.keywordPatternRe.exec(S);
        }
        var i;
        n += S.substring(e), M.addText(n);
      }
      function d() {
        null != N.subLanguage ? function () {
          if ("" === S) return;
          var e = null;
          if ("string" == typeof N.subLanguage) {
            if (!i[N.subLanguage]) return void M.addText(S);
            e = E(N.subLanguage, S, !0, k[N.subLanguage]), k[N.subLanguage] = e._top;
          } else e = x(S, N.subLanguage.length ? N.subLanguage : null);
          N.relevance > 0 && (R += e.relevance), M.addSublanguage(e._emitter, e.language);
        }() : l(), S = "";
      }
      function u(e, t) {
        var n = 1;
        var i = t.length - 1;
        for (; n <= i;) {
          if (!e._emit[n]) {
            n++;
            continue;
          }
          var _i2 = y.classNameAliases[e[n]] || e[n],
            _r2 = t[n];
          _i2 ? M.addKeyword(_r2, _i2) : (S = _r2, l(), S = ""), n++;
        }
      }
      function h(e, t) {
        return e.scope && "string" == typeof e.scope && M.openNode(y.classNameAliases[e.scope] || e.scope), e.beginScope && (e.beginScope._wrap ? (M.addKeyword(S, y.classNameAliases[e.beginScope._wrap] || e.beginScope._wrap), S = "") : e.beginScope._multi && (u(e.beginScope, t), S = "")), N = Object.create(e, {
          parent: {
            value: N
          }
        }), N;
      }
      function p(e, t, i) {
        var r = function (e, t) {
          var n = e && e.exec(t);
          return n && 0 === n.index;
        }(e.endRe, i);
        if (r) {
          if (e["on:end"]) {
            var _i3 = new n(e);
            e["on:end"](t, _i3), _i3.isMatchIgnored && (r = !1);
          }
          if (r) {
            for (; e.endsParent && e.parent;) {
              e = e.parent;
            }
            return e;
          }
        }
        if (e.endsWithParent) return p(e.parent, t, i);
      }
      function f(e) {
        return 0 === N.matcher.regexIndex ? (S += e[0], 1) : (I = !0, 0);
      }
      function b(e) {
        var n = e[0],
          i = t.substring(e.index),
          r = p(N, e, i);
        if (!r) return ee;
        var s = N;
        N.endScope && N.endScope._wrap ? (d(), M.addKeyword(n, N.endScope._wrap)) : N.endScope && N.endScope._multi ? (d(), u(N.endScope, e)) : s.skip ? S += n : (s.returnEnd || s.excludeEnd || (S += n), d(), s.excludeEnd && (S = n));
        do {
          N.scope && M.closeNode(), N.skip || N.subLanguage || (R += N.relevance), N = N.parent;
        } while (N !== r.parent);
        return r.starts && h(r.starts, e), s.returnEnd ? 0 : n.length;
      }
      var m = {};
      function w(i, s) {
        var a = s && s[0];
        if (S += i, null == a) return d(), 0;
        if ("begin" === m.type && "end" === s.type && m.index === s.index && "" === a) {
          if (S += t.slice(s.index, s.index + 1), !o) {
            var _t4 = Error("0 width match regex (".concat(e, ")"));
            throw _t4.languageName = e, _t4.badRule = m.rule, _t4;
          }
          return 1;
        }
        if (m = s, "begin" === s.type) return function (e) {
          var t = e[0],
            i = e.rule,
            r = new n(i),
            s = [i.__beforeBegin, i["on:begin"]];
          for (var _i4 = 0, _s3 = s; _i4 < _s3.length; _i4++) {
            var _n4 = _s3[_i4];
            if (_n4 && (_n4(e, r), r.isMatchIgnored)) return f(t);
          }
          return i.skip ? S += t : (i.excludeBegin && (S += t), d(), i.returnBegin || i.excludeBegin || (S = t)), h(i, e), i.returnBegin ? 0 : t.length;
        }(s);
        if ("illegal" === s.type && !r) {
          var _e4 = Error('Illegal lexeme "' + a + '" for mode "' + (N.scope || "<unnamed>") + '"');
          throw _e4.mode = N, _e4;
        }
        if ("end" === s.type) {
          var _e5 = b(s);
          if (_e5 !== ee) return _e5;
        }
        if ("illegal" === s.type && "" === a) return 1;
        if (A > 1e5 && A > 3 * s.index) throw Error("potential infinite loop, way more iterations than matches");
        return S += a, a.length;
      }
      var y = O(e);
      if (!y) throw K(a.replace("{}", e)), Error('Unknown language: "' + e + '"');
      var _ = V(y);
      var v = "",
        N = s || _;
      var k = {},
        M = new g.__emitter(g);
      (function () {
        var e = [];
        for (var _t5 = N; _t5 !== y; _t5 = _t5.parent) {
          _t5.scope && e.unshift(_t5.scope);
        }
        e.forEach(function (e) {
          return M.openNode(e);
        });
      })();
      var S = "",
        R = 0,
        j = 0,
        A = 0,
        I = !1;
      try {
        for (N.matcher.considerAll();;) {
          A++, I ? I = !1 : N.matcher.considerAll(), N.matcher.lastIndex = j;
          var _e6 = N.matcher.exec(t);
          if (!_e6) break;
          var _n5 = w(t.substring(j, _e6.index), _e6);
          j = _e6.index + _n5;
        }
        return w(t.substring(j)), M.closeAllNodes(), M.finalize(), v = M.toHTML(), {
          language: e,
          value: v,
          relevance: R,
          illegal: !1,
          _emitter: M,
          _top: N
        };
      } catch (n) {
        if (n.message && n.message.includes("Illegal")) return {
          language: e,
          value: Y(t),
          illegal: !0,
          relevance: 0,
          _illegalBy: {
            message: n.message,
            index: j,
            context: t.slice(j - 100, j + 100),
            mode: n.mode,
            resultSoFar: v
          },
          _emitter: M
        };
        if (o) return {
          language: e,
          value: Y(t),
          illegal: !1,
          relevance: 0,
          errorRaised: n,
          _emitter: M,
          _top: N
        };
        throw n;
      }
    }
    function x(e, t) {
      t = t || g.languages || Object.keys(i);
      var n = function (e) {
          var t = {
            value: Y(e),
            illegal: !1,
            relevance: 0,
            _top: c,
            _emitter: new g.__emitter(g)
          };
          return t._emitter.addText(e), t;
        }(e),
        r = t.filter(O).filter(N).map(function (t) {
          return E(t, e, !1);
        });
      r.unshift(n);
      var s = r.sort(function (e, t) {
          if (e.relevance !== t.relevance) return t.relevance - e.relevance;
          if (e.language && t.language) {
            if (O(e.language).supersetOf === t.language) return 1;
            if (O(t.language).supersetOf === e.language) return -1;
          }
          return 0;
        }),
        _s4 = (0,_babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_1__["default"])(s, 2),
        o = _s4[0],
        a = _s4[1],
        l = o;
      return l.secondBest = a, l;
    }
    function w(e) {
      var t = null;
      var n = function (e) {
        var t = e.className + " ";
        t += e.parentNode ? e.parentNode.className : "";
        var n = g.languageDetectRe.exec(t);
        if (n) {
          var _t6 = O(n[1]);
          return _t6 || (W(a.replace("{}", n[1])), W("Falling back to no-highlight mode for this block.", e)), _t6 ? n[1] : "no-highlight";
        }
        return t.split(/\s+/).find(function (e) {
          return b(e) || O(e);
        });
      }(e);
      if (b(n)) return;
      if (k("before:highlightElement", {
        el: e,
        language: n
      }), e.children.length > 0 && (g.ignoreUnescapedHTML || (console.warn("One of your code blocks includes unescaped HTML. This is a potentially serious security risk."), console.warn("https://github.com/highlightjs/highlight.js/wiki/security"), console.warn("The element with unescaped HTML:"), console.warn(e)), g.throwUnescapedHTML)) throw new J("One of your code blocks includes unescaped HTML.", e.innerHTML);
      t = e;
      var i = t.textContent,
        s = n ? m(i, {
          language: n,
          ignoreIllegals: !0
        }) : x(i);
      e.innerHTML = s.value, function (e, t, n) {
        var i = t && r[t] || n;
        e.classList.add("hljs"), e.classList.add("language-" + i);
      }(e, n, s.language), e.result = {
        language: s.language,
        re: s.relevance,
        relevance: s.relevance
      }, s.secondBest && (e.secondBest = {
        language: s.secondBest.language,
        relevance: s.secondBest.relevance
      }), k("after:highlightElement", {
        el: e,
        result: s,
        text: i
      });
    }
    var y = !1;
    function _() {
      "loading" !== document.readyState ? document.querySelectorAll(g.cssSelector).forEach(w) : y = !0;
    }
    function O(e) {
      return e = (e || "").toLowerCase(), i[e] || i[r[e]];
    }
    function v(e, _ref7) {
      var t = _ref7.languageName;
      "string" == typeof e && (e = [e]), e.forEach(function (e) {
        r[e.toLowerCase()] = t;
      });
    }
    function N(e) {
      var t = O(e);
      return t && !t.disableAutodetect;
    }
    function k(e, t) {
      var n = e;
      s.forEach(function (e) {
        e[n] && e[n](t);
      });
    }
    "undefined" != typeof window && window.addEventListener && window.addEventListener("DOMContentLoaded", function () {
      y && _();
    }, !1), Object.assign(t, {
      highlight: m,
      highlightAuto: x,
      highlightAll: _,
      highlightElement: w,
      highlightBlock: function highlightBlock(e) {
        return X("10.7.0", "highlightBlock will be removed entirely in v12.0"), X("10.7.0", "Please use highlightElement now."), w(e);
      },
      configure: function configure(e) {
        g = Q(g, e);
      },
      initHighlighting: function initHighlighting() {
        _(), X("10.6.0", "initHighlighting() deprecated.  Use highlightAll() now.");
      },
      initHighlightingOnLoad: function initHighlightingOnLoad() {
        _(), X("10.6.0", "initHighlightingOnLoad() deprecated.  Use highlightAll() now.");
      },
      registerLanguage: function registerLanguage(e, n) {
        var r = null;
        try {
          r = n(t);
        } catch (t) {
          if (K("Language definition for '{}' could not be registered.".replace("{}", e)), !o) throw t;
          K(t), r = c;
        }
        r.name || (r.name = e), i[e] = r, r.rawDefinition = n.bind(null, t), r.aliases && v(r.aliases, {
          languageName: e
        });
      },
      unregisterLanguage: function unregisterLanguage(e) {
        delete i[e];
        for (var _i5 = 0, _Object$keys = Object.keys(r); _i5 < _Object$keys.length; _i5++) {
          var _t7 = _Object$keys[_i5];
          r[_t7] === e && delete r[_t7];
        }
      },
      listLanguages: function listLanguages() {
        return Object.keys(i);
      },
      getLanguage: O,
      registerAliases: v,
      autoDetection: N,
      inherit: Q,
      addPlugin: function addPlugin(e) {
        (function (e) {
          e["before:highlightBlock"] && !e["before:highlightElement"] && (e["before:highlightElement"] = function (t) {
            e["before:highlightBlock"](Object.assign({
              block: t.el
            }, t));
          }), e["after:highlightBlock"] && !e["after:highlightElement"] && (e["after:highlightElement"] = function (t) {
            e["after:highlightBlock"](Object.assign({
              block: t.el
            }, t));
          });
        })(e), s.push(e);
      }
    }), t.debugMode = function () {
      o = !1;
    }, t.safeMode = function () {
      o = !0;
    }, t.versionString = "11.7.0", t.regex = {
      concat: p,
      lookahead: d,
      either: f,
      optional: h,
      anyNumberOfTimes: u
    };
    for (var _t8 in A) {
      "object" == (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(A[_t8]) && e.exports(A[_t8]);
    }
    return Object.assign(t, A), t;
  }({});
  return te;
}();
"object" == (typeof exports === "undefined" ? "undefined" : (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(exports)) && "undefined" != "object" && (module.exports = hljs); /*! `xml` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var a = e.regex,
        n = a.concat(/(?:[A-Z_a-z\xAA\xB5\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0560-\u0588\u05D0-\u05EA\u05EF-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u0860-\u086A\u0870-\u0887\u0889-\u088E\u08A0-\u08C9\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u09FC\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C5D\u0C60\u0C61\u0C80\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D04-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D54-\u0D56\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E86-\u0E8A\u0E8C-\u0EA3\u0EA5\u0EA7-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16F1-\u16F8\u1700-\u1711\u171F-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1878\u1880-\u1884\u1887-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4C\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1C80-\u1C88\u1C90-\u1CBA\u1CBD-\u1CBF\u1CE9-\u1CEC\u1CEE-\u1CF3\u1CF5\u1CF6\u1CFA\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u212F-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2183\u2184\u2C00-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2E2F\u3005\u3006\u3031-\u3035\u303B\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312F\u3131-\u318E\u31A0-\u31BF\u31F0-\u31FF\u3400-\u4DBF\u4E00-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6E5\uA717-\uA71F\uA722-\uA788\uA78B-\uA7CA\uA7D0\uA7D1\uA7D3\uA7D5-\uA7D9\uA7F2-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA8FE\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB69\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDE80-\uDE9C\uDEA0-\uDED0\uDF00-\uDF1F\uDF2D-\uDF40\uDF42-\uDF49\uDF50-\uDF75\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF]|\uD801[\uDC00-\uDC9D\uDCB0-\uDCD3\uDCD8-\uDCFB\uDD00-\uDD27\uDD30-\uDD63\uDD70-\uDD7A\uDD7C-\uDD8A\uDD8C-\uDD92\uDD94\uDD95\uDD97-\uDDA1\uDDA3-\uDDB1\uDDB3-\uDDB9\uDDBB\uDDBC\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67\uDF80-\uDF85\uDF87-\uDFB0\uDFB2-\uDFBA]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00\uDE10-\uDE13\uDE15-\uDE17\uDE19-\uDE35\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE4\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2\uDD00-\uDD23\uDE80-\uDEA9\uDEB0\uDEB1\uDF00-\uDF1C\uDF27\uDF30-\uDF45\uDF70-\uDF81\uDFB0-\uDFC4\uDFE0-\uDFF6]|\uD804[\uDC03-\uDC37\uDC71\uDC72\uDC75\uDC83-\uDCAF\uDCD0-\uDCE8\uDD03-\uDD26\uDD44\uDD47\uDD50-\uDD72\uDD76\uDD83-\uDDB2\uDDC1-\uDDC4\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE2B\uDE3F\uDE40\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEDE\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3D\uDF50\uDF5D-\uDF61]|\uD805[\uDC00-\uDC34\uDC47-\uDC4A\uDC5F-\uDC61\uDC80-\uDCAF\uDCC4\uDCC5\uDCC7\uDD80-\uDDAE\uDDD8-\uDDDB\uDE00-\uDE2F\uDE44\uDE80-\uDEAA\uDEB8\uDF00-\uDF1A\uDF40-\uDF46]|\uD806[\uDC00-\uDC2B\uDCA0-\uDCDF\uDCFF-\uDD06\uDD09\uDD0C-\uDD13\uDD15\uDD16\uDD18-\uDD2F\uDD3F\uDD41\uDDA0-\uDDA7\uDDAA-\uDDD0\uDDE1\uDDE3\uDE00\uDE0B-\uDE32\uDE3A\uDE50\uDE5C-\uDE89\uDE9D\uDEB0-\uDEF8]|\uD807[\uDC00-\uDC08\uDC0A-\uDC2E\uDC40\uDC72-\uDC8F\uDD00-\uDD06\uDD08\uDD09\uDD0B-\uDD30\uDD46\uDD60-\uDD65\uDD67\uDD68\uDD6A-\uDD89\uDD98\uDEE0-\uDEF2\uDF02\uDF04-\uDF10\uDF12-\uDF33\uDFB0]|\uD808[\uDC00-\uDF99]|\uD809[\uDC80-\uDD43]|\uD80B[\uDF90-\uDFF0]|[\uD80C\uD81C-\uD820\uD822\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872\uD874-\uD879\uD880-\uD883\uD885-\uD887][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2F\uDC41-\uDC46]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDE70-\uDEBE\uDED0-\uDEED\uDF00-\uDF2F\uDF40-\uDF43\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDE40-\uDE7F\uDF00-\uDF4A\uDF50\uDF93-\uDF9F\uDFE0\uDFE1\uDFE3]|\uD821[\uDC00-\uDFF7]|\uD823[\uDC00-\uDCD5\uDD00-\uDD08]|\uD82B[\uDFF0-\uDFF3\uDFF5-\uDFFB\uDFFD\uDFFE]|\uD82C[\uDC00-\uDD22\uDD32\uDD50-\uDD52\uDD55\uDD64-\uDD67\uDD70-\uDEFB]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB]|\uD837[\uDF00-\uDF1E\uDF25-\uDF2A]|\uD838[\uDC30-\uDC6D\uDD00-\uDD2C\uDD37-\uDD3D\uDD4E\uDE90-\uDEAD\uDEC0-\uDEEB]|\uD839[\uDCD0-\uDCEB\uDFE0-\uDFE6\uDFE8-\uDFEB\uDFED\uDFEE\uDFF0-\uDFFE]|\uD83A[\uDC00-\uDCC4\uDD00-\uDD43\uDD4B]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD869[\uDC00-\uDEDF\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF39\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1\uDEB0-\uDFFF]|\uD87A[\uDC00-\uDFE0]|\uD87E[\uDC00-\uDE1D]|\uD884[\uDC00-\uDF4A\uDF50-\uDFFF]|\uD888[\uDC00-\uDFAF])/, a.optional(/(?:[\x2D\.0-9A-Z_a-z\xAA\xB5\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0560-\u0588\u05D0-\u05EA\u05EF-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u0860-\u086A\u0870-\u0887\u0889-\u088E\u08A0-\u08C9\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u09FC\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C5D\u0C60\u0C61\u0C80\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D04-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D54-\u0D56\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E86-\u0E8A\u0E8C-\u0EA3\u0EA5\u0EA7-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16F1-\u16F8\u1700-\u1711\u171F-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1878\u1880-\u1884\u1887-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4C\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1C80-\u1C88\u1C90-\u1CBA\u1CBD-\u1CBF\u1CE9-\u1CEC\u1CEE-\u1CF3\u1CF5\u1CF6\u1CFA\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u212F-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2183\u2184\u2C00-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2E2F\u3005\u3006\u3031-\u3035\u303B\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312F\u3131-\u318E\u31A0-\u31BF\u31F0-\u31FF\u3400-\u4DBF\u4E00-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6E5\uA717-\uA71F\uA722-\uA788\uA78B-\uA7CA\uA7D0\uA7D1\uA7D3\uA7D5-\uA7D9\uA7F2-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA8FE\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB69\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDE80-\uDE9C\uDEA0-\uDED0\uDF00-\uDF1F\uDF2D-\uDF40\uDF42-\uDF49\uDF50-\uDF75\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF]|\uD801[\uDC00-\uDC9D\uDCB0-\uDCD3\uDCD8-\uDCFB\uDD00-\uDD27\uDD30-\uDD63\uDD70-\uDD7A\uDD7C-\uDD8A\uDD8C-\uDD92\uDD94\uDD95\uDD97-\uDDA1\uDDA3-\uDDB1\uDDB3-\uDDB9\uDDBB\uDDBC\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67\uDF80-\uDF85\uDF87-\uDFB0\uDFB2-\uDFBA]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00\uDE10-\uDE13\uDE15-\uDE17\uDE19-\uDE35\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE4\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2\uDD00-\uDD23\uDE80-\uDEA9\uDEB0\uDEB1\uDF00-\uDF1C\uDF27\uDF30-\uDF45\uDF70-\uDF81\uDFB0-\uDFC4\uDFE0-\uDFF6]|\uD804[\uDC03-\uDC37\uDC71\uDC72\uDC75\uDC83-\uDCAF\uDCD0-\uDCE8\uDD03-\uDD26\uDD44\uDD47\uDD50-\uDD72\uDD76\uDD83-\uDDB2\uDDC1-\uDDC4\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE2B\uDE3F\uDE40\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEDE\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3D\uDF50\uDF5D-\uDF61]|\uD805[\uDC00-\uDC34\uDC47-\uDC4A\uDC5F-\uDC61\uDC80-\uDCAF\uDCC4\uDCC5\uDCC7\uDD80-\uDDAE\uDDD8-\uDDDB\uDE00-\uDE2F\uDE44\uDE80-\uDEAA\uDEB8\uDF00-\uDF1A\uDF40-\uDF46]|\uD806[\uDC00-\uDC2B\uDCA0-\uDCDF\uDCFF-\uDD06\uDD09\uDD0C-\uDD13\uDD15\uDD16\uDD18-\uDD2F\uDD3F\uDD41\uDDA0-\uDDA7\uDDAA-\uDDD0\uDDE1\uDDE3\uDE00\uDE0B-\uDE32\uDE3A\uDE50\uDE5C-\uDE89\uDE9D\uDEB0-\uDEF8]|\uD807[\uDC00-\uDC08\uDC0A-\uDC2E\uDC40\uDC72-\uDC8F\uDD00-\uDD06\uDD08\uDD09\uDD0B-\uDD30\uDD46\uDD60-\uDD65\uDD67\uDD68\uDD6A-\uDD89\uDD98\uDEE0-\uDEF2\uDF02\uDF04-\uDF10\uDF12-\uDF33\uDFB0]|\uD808[\uDC00-\uDF99]|\uD809[\uDC80-\uDD43]|\uD80B[\uDF90-\uDFF0]|[\uD80C\uD81C-\uD820\uD822\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872\uD874-\uD879\uD880-\uD883\uD885-\uD887][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2F\uDC41-\uDC46]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDE70-\uDEBE\uDED0-\uDEED\uDF00-\uDF2F\uDF40-\uDF43\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDE40-\uDE7F\uDF00-\uDF4A\uDF50\uDF93-\uDF9F\uDFE0\uDFE1\uDFE3]|\uD821[\uDC00-\uDFF7]|\uD823[\uDC00-\uDCD5\uDD00-\uDD08]|\uD82B[\uDFF0-\uDFF3\uDFF5-\uDFFB\uDFFD\uDFFE]|\uD82C[\uDC00-\uDD22\uDD32\uDD50-\uDD52\uDD55\uDD64-\uDD67\uDD70-\uDEFB]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB]|\uD837[\uDF00-\uDF1E\uDF25-\uDF2A]|\uD838[\uDC30-\uDC6D\uDD00-\uDD2C\uDD37-\uDD3D\uDD4E\uDE90-\uDEAD\uDEC0-\uDEEB]|\uD839[\uDCD0-\uDCEB\uDFE0-\uDFE6\uDFE8-\uDFEB\uDFED\uDFEE\uDFF0-\uDFFE]|\uD83A[\uDC00-\uDCC4\uDD00-\uDD43\uDD4B]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD869[\uDC00-\uDEDF\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF39\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1\uDEB0-\uDFFF]|\uD87A[\uDC00-\uDFE0]|\uD87E[\uDC00-\uDE1D]|\uD884[\uDC00-\uDF4A\uDF50-\uDFFF]|\uD888[\uDC00-\uDFAF])*:/), /(?:[\x2D\.0-9A-Z_a-z\xAA\xB5\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0560-\u0588\u05D0-\u05EA\u05EF-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u0860-\u086A\u0870-\u0887\u0889-\u088E\u08A0-\u08C9\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u09FC\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C5D\u0C60\u0C61\u0C80\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D04-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D54-\u0D56\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E86-\u0E8A\u0E8C-\u0EA3\u0EA5\u0EA7-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16F1-\u16F8\u1700-\u1711\u171F-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1878\u1880-\u1884\u1887-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4C\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1C80-\u1C88\u1C90-\u1CBA\u1CBD-\u1CBF\u1CE9-\u1CEC\u1CEE-\u1CF3\u1CF5\u1CF6\u1CFA\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u212F-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2183\u2184\u2C00-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2E2F\u3005\u3006\u3031-\u3035\u303B\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312F\u3131-\u318E\u31A0-\u31BF\u31F0-\u31FF\u3400-\u4DBF\u4E00-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6E5\uA717-\uA71F\uA722-\uA788\uA78B-\uA7CA\uA7D0\uA7D1\uA7D3\uA7D5-\uA7D9\uA7F2-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA8FE\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB69\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDE80-\uDE9C\uDEA0-\uDED0\uDF00-\uDF1F\uDF2D-\uDF40\uDF42-\uDF49\uDF50-\uDF75\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF]|\uD801[\uDC00-\uDC9D\uDCB0-\uDCD3\uDCD8-\uDCFB\uDD00-\uDD27\uDD30-\uDD63\uDD70-\uDD7A\uDD7C-\uDD8A\uDD8C-\uDD92\uDD94\uDD95\uDD97-\uDDA1\uDDA3-\uDDB1\uDDB3-\uDDB9\uDDBB\uDDBC\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67\uDF80-\uDF85\uDF87-\uDFB0\uDFB2-\uDFBA]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00\uDE10-\uDE13\uDE15-\uDE17\uDE19-\uDE35\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE4\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2\uDD00-\uDD23\uDE80-\uDEA9\uDEB0\uDEB1\uDF00-\uDF1C\uDF27\uDF30-\uDF45\uDF70-\uDF81\uDFB0-\uDFC4\uDFE0-\uDFF6]|\uD804[\uDC03-\uDC37\uDC71\uDC72\uDC75\uDC83-\uDCAF\uDCD0-\uDCE8\uDD03-\uDD26\uDD44\uDD47\uDD50-\uDD72\uDD76\uDD83-\uDDB2\uDDC1-\uDDC4\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE2B\uDE3F\uDE40\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEDE\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3D\uDF50\uDF5D-\uDF61]|\uD805[\uDC00-\uDC34\uDC47-\uDC4A\uDC5F-\uDC61\uDC80-\uDCAF\uDCC4\uDCC5\uDCC7\uDD80-\uDDAE\uDDD8-\uDDDB\uDE00-\uDE2F\uDE44\uDE80-\uDEAA\uDEB8\uDF00-\uDF1A\uDF40-\uDF46]|\uD806[\uDC00-\uDC2B\uDCA0-\uDCDF\uDCFF-\uDD06\uDD09\uDD0C-\uDD13\uDD15\uDD16\uDD18-\uDD2F\uDD3F\uDD41\uDDA0-\uDDA7\uDDAA-\uDDD0\uDDE1\uDDE3\uDE00\uDE0B-\uDE32\uDE3A\uDE50\uDE5C-\uDE89\uDE9D\uDEB0-\uDEF8]|\uD807[\uDC00-\uDC08\uDC0A-\uDC2E\uDC40\uDC72-\uDC8F\uDD00-\uDD06\uDD08\uDD09\uDD0B-\uDD30\uDD46\uDD60-\uDD65\uDD67\uDD68\uDD6A-\uDD89\uDD98\uDEE0-\uDEF2\uDF02\uDF04-\uDF10\uDF12-\uDF33\uDFB0]|\uD808[\uDC00-\uDF99]|\uD809[\uDC80-\uDD43]|\uD80B[\uDF90-\uDFF0]|[\uD80C\uD81C-\uD820\uD822\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872\uD874-\uD879\uD880-\uD883\uD885-\uD887][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2F\uDC41-\uDC46]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDE70-\uDEBE\uDED0-\uDEED\uDF00-\uDF2F\uDF40-\uDF43\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDE40-\uDE7F\uDF00-\uDF4A\uDF50\uDF93-\uDF9F\uDFE0\uDFE1\uDFE3]|\uD821[\uDC00-\uDFF7]|\uD823[\uDC00-\uDCD5\uDD00-\uDD08]|\uD82B[\uDFF0-\uDFF3\uDFF5-\uDFFB\uDFFD\uDFFE]|\uD82C[\uDC00-\uDD22\uDD32\uDD50-\uDD52\uDD55\uDD64-\uDD67\uDD70-\uDEFB]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB]|\uD837[\uDF00-\uDF1E\uDF25-\uDF2A]|\uD838[\uDC30-\uDC6D\uDD00-\uDD2C\uDD37-\uDD3D\uDD4E\uDE90-\uDEAD\uDEC0-\uDEEB]|\uD839[\uDCD0-\uDCEB\uDFE0-\uDFE6\uDFE8-\uDFEB\uDFED\uDFEE\uDFF0-\uDFFE]|\uD83A[\uDC00-\uDCC4\uDD00-\uDD43\uDD4B]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD869[\uDC00-\uDEDF\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF39\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1\uDEB0-\uDFFF]|\uD87A[\uDC00-\uDFE0]|\uD87E[\uDC00-\uDE1D]|\uD884[\uDC00-\uDF4A\uDF50-\uDFFF]|\uD888[\uDC00-\uDFAF])*/),
        s = {
          className: "symbol",
          begin: /&[a-z]+;|&#[0-9]+;|&#x[a-f0-9]+;/
        },
        t = {
          begin: /\s/,
          contains: [{
            className: "keyword",
            begin: /#?[a-z_][a-z1-9_-]+/,
            illegal: /\n/
          }]
        },
        i = e.inherit(t, {
          begin: /\(/,
          end: /\)/
        }),
        c = e.inherit(e.APOS_STRING_MODE, {
          className: "string"
        }),
        l = e.inherit(e.QUOTE_STRING_MODE, {
          className: "string"
        }),
        r = {
          endsWithParent: !0,
          illegal: /</,
          relevance: 0,
          contains: [{
            className: "attr",
            begin: /(?:[\x2D\.0-:A-Z_a-z\xAA\xB5\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0560-\u0588\u05D0-\u05EA\u05EF-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u0860-\u086A\u0870-\u0887\u0889-\u088E\u08A0-\u08C9\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u09FC\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C5D\u0C60\u0C61\u0C80\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D04-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D54-\u0D56\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E86-\u0E8A\u0E8C-\u0EA3\u0EA5\u0EA7-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16F1-\u16F8\u1700-\u1711\u171F-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1878\u1880-\u1884\u1887-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4C\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1C80-\u1C88\u1C90-\u1CBA\u1CBD-\u1CBF\u1CE9-\u1CEC\u1CEE-\u1CF3\u1CF5\u1CF6\u1CFA\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u212F-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2183\u2184\u2C00-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2E2F\u3005\u3006\u3031-\u3035\u303B\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312F\u3131-\u318E\u31A0-\u31BF\u31F0-\u31FF\u3400-\u4DBF\u4E00-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6E5\uA717-\uA71F\uA722-\uA788\uA78B-\uA7CA\uA7D0\uA7D1\uA7D3\uA7D5-\uA7D9\uA7F2-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA8FE\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB69\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDE80-\uDE9C\uDEA0-\uDED0\uDF00-\uDF1F\uDF2D-\uDF40\uDF42-\uDF49\uDF50-\uDF75\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF]|\uD801[\uDC00-\uDC9D\uDCB0-\uDCD3\uDCD8-\uDCFB\uDD00-\uDD27\uDD30-\uDD63\uDD70-\uDD7A\uDD7C-\uDD8A\uDD8C-\uDD92\uDD94\uDD95\uDD97-\uDDA1\uDDA3-\uDDB1\uDDB3-\uDDB9\uDDBB\uDDBC\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67\uDF80-\uDF85\uDF87-\uDFB0\uDFB2-\uDFBA]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00\uDE10-\uDE13\uDE15-\uDE17\uDE19-\uDE35\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE4\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2\uDD00-\uDD23\uDE80-\uDEA9\uDEB0\uDEB1\uDF00-\uDF1C\uDF27\uDF30-\uDF45\uDF70-\uDF81\uDFB0-\uDFC4\uDFE0-\uDFF6]|\uD804[\uDC03-\uDC37\uDC71\uDC72\uDC75\uDC83-\uDCAF\uDCD0-\uDCE8\uDD03-\uDD26\uDD44\uDD47\uDD50-\uDD72\uDD76\uDD83-\uDDB2\uDDC1-\uDDC4\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE2B\uDE3F\uDE40\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEDE\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3D\uDF50\uDF5D-\uDF61]|\uD805[\uDC00-\uDC34\uDC47-\uDC4A\uDC5F-\uDC61\uDC80-\uDCAF\uDCC4\uDCC5\uDCC7\uDD80-\uDDAE\uDDD8-\uDDDB\uDE00-\uDE2F\uDE44\uDE80-\uDEAA\uDEB8\uDF00-\uDF1A\uDF40-\uDF46]|\uD806[\uDC00-\uDC2B\uDCA0-\uDCDF\uDCFF-\uDD06\uDD09\uDD0C-\uDD13\uDD15\uDD16\uDD18-\uDD2F\uDD3F\uDD41\uDDA0-\uDDA7\uDDAA-\uDDD0\uDDE1\uDDE3\uDE00\uDE0B-\uDE32\uDE3A\uDE50\uDE5C-\uDE89\uDE9D\uDEB0-\uDEF8]|\uD807[\uDC00-\uDC08\uDC0A-\uDC2E\uDC40\uDC72-\uDC8F\uDD00-\uDD06\uDD08\uDD09\uDD0B-\uDD30\uDD46\uDD60-\uDD65\uDD67\uDD68\uDD6A-\uDD89\uDD98\uDEE0-\uDEF2\uDF02\uDF04-\uDF10\uDF12-\uDF33\uDFB0]|\uD808[\uDC00-\uDF99]|\uD809[\uDC80-\uDD43]|\uD80B[\uDF90-\uDFF0]|[\uD80C\uD81C-\uD820\uD822\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872\uD874-\uD879\uD880-\uD883\uD885-\uD887][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2F\uDC41-\uDC46]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDE70-\uDEBE\uDED0-\uDEED\uDF00-\uDF2F\uDF40-\uDF43\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDE40-\uDE7F\uDF00-\uDF4A\uDF50\uDF93-\uDF9F\uDFE0\uDFE1\uDFE3]|\uD821[\uDC00-\uDFF7]|\uD823[\uDC00-\uDCD5\uDD00-\uDD08]|\uD82B[\uDFF0-\uDFF3\uDFF5-\uDFFB\uDFFD\uDFFE]|\uD82C[\uDC00-\uDD22\uDD32\uDD50-\uDD52\uDD55\uDD64-\uDD67\uDD70-\uDEFB]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB]|\uD837[\uDF00-\uDF1E\uDF25-\uDF2A]|\uD838[\uDC30-\uDC6D\uDD00-\uDD2C\uDD37-\uDD3D\uDD4E\uDE90-\uDEAD\uDEC0-\uDEEB]|\uD839[\uDCD0-\uDCEB\uDFE0-\uDFE6\uDFE8-\uDFEB\uDFED\uDFEE\uDFF0-\uDFFE]|\uD83A[\uDC00-\uDCC4\uDD00-\uDD43\uDD4B]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD869[\uDC00-\uDEDF\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF39\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1\uDEB0-\uDFFF]|\uD87A[\uDC00-\uDFE0]|\uD87E[\uDC00-\uDE1D]|\uD884[\uDC00-\uDF4A\uDF50-\uDFFF]|\uD888[\uDC00-\uDFAF])+/,
            relevance: 0
          }, {
            begin: /=\s*/,
            relevance: 0,
            contains: [{
              className: "string",
              endsParent: !0,
              variants: [{
                begin: /"/,
                end: /"/,
                contains: [s]
              }, {
                begin: /'/,
                end: /'/,
                contains: [s]
              }, {
                begin: /[^\s"'=<>`]+/
              }]
            }]
          }]
        };
      return {
        name: "HTML, XML",
        aliases: ["html", "xhtml", "rss", "atom", "xjb", "xsd", "xsl", "plist", "wsf", "svg"],
        case_insensitive: !0,
        unicodeRegex: !0,
        contains: [{
          className: "meta",
          begin: /<![a-z]/,
          end: />/,
          relevance: 10,
          contains: [t, l, c, i, {
            begin: /\[/,
            end: /\]/,
            contains: [{
              className: "meta",
              begin: /<![a-z]/,
              end: />/,
              contains: [t, i, l, c]
            }]
          }]
        }, e.COMMENT(/<!--/, /-->/, {
          relevance: 10
        }), {
          begin: /<!\[CDATA\[/,
          end: /\]\]>/,
          relevance: 10
        }, s, {
          className: "meta",
          end: /\?>/,
          variants: [{
            begin: /<\?xml/,
            relevance: 10,
            contains: [l]
          }, {
            begin: /<\?[a-z][a-z0-9]+/
          }]
        }, {
          className: "tag",
          begin: /<style(?=\s|>)/,
          end: />/,
          keywords: {
            name: "style"
          },
          contains: [r],
          starts: {
            end: /<\/style>/,
            returnEnd: !0,
            subLanguage: ["css", "xml"]
          }
        }, {
          className: "tag",
          begin: /<script(?=\s|>)/,
          end: />/,
          keywords: {
            name: "script"
          },
          contains: [r],
          starts: {
            end: /<\/script>/,
            returnEnd: !0,
            subLanguage: ["javascript", "handlebars", "xml"]
          }
        }, {
          className: "tag",
          begin: /<>|<\/>/
        }, {
          className: "tag",
          begin: a.concat(/</, a.lookahead(a.concat(n, a.either(/\/>/, />/, /\s/)))),
          end: /\/?>/,
          contains: [{
            className: "name",
            begin: n,
            relevance: 0,
            starts: r
          }]
        }, {
          className: "tag",
          begin: a.concat(/<\//, a.lookahead(a.concat(n, />/))),
          contains: [{
            className: "name",
            begin: n,
            relevance: 0
          }, {
            begin: />/,
            relevance: 0,
            endsParent: !0
          }]
        }]
      };
    };
  }();
  hljs.registerLanguage("xml", e);
})(); /*! `csharp` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = {
          keyword: ["abstract", "as", "base", "break", "case", "catch", "class", "const", "continue", "do", "else", "event", "explicit", "extern", "finally", "fixed", "for", "foreach", "goto", "if", "implicit", "in", "interface", "internal", "is", "lock", "namespace", "new", "operator", "out", "override", "params", "private", "protected", "public", "readonly", "record", "ref", "return", "scoped", "sealed", "sizeof", "stackalloc", "static", "struct", "switch", "this", "throw", "try", "typeof", "unchecked", "unsafe", "using", "virtual", "void", "volatile", "while"].concat(["add", "alias", "and", "ascending", "async", "await", "by", "descending", "equals", "from", "get", "global", "group", "init", "into", "join", "let", "nameof", "not", "notnull", "on", "or", "orderby", "partial", "remove", "select", "set", "unmanaged", "value|0", "var", "when", "where", "with", "yield"]),
          built_in: ["bool", "byte", "char", "decimal", "delegate", "double", "dynamic", "enum", "float", "int", "long", "nint", "nuint", "object", "sbyte", "short", "string", "ulong", "uint", "ushort"],
          literal: ["default", "false", "null", "true"]
        },
        a = e.inherit(e.TITLE_MODE, {
          begin: "[a-zA-Z](\\.?\\w)*"
        }),
        i = {
          className: "number",
          variants: [{
            begin: "\\b(0b[01']+)"
          }, {
            begin: "(-?)\\b([\\d']+(\\.[\\d']*)?|\\.[\\d']+)(u|U|l|L|ul|UL|f|F|b|B)"
          }, {
            begin: "(-?)(\\b0[xX][a-fA-F0-9']+|(\\b[\\d']+(\\.[\\d']*)?|\\.[\\d']+)([eE][-+]?[\\d']+)?)"
          }],
          relevance: 0
        },
        s = {
          className: "string",
          begin: '@"',
          end: '"',
          contains: [{
            begin: '""'
          }]
        },
        t = e.inherit(s, {
          illegal: /\n/
        }),
        r = {
          className: "subst",
          begin: /\{/,
          end: /\}/,
          keywords: n
        },
        l = e.inherit(r, {
          illegal: /\n/
        }),
        c = {
          className: "string",
          begin: /\$"/,
          end: '"',
          illegal: /\n/,
          contains: [{
            begin: /\{\{/
          }, {
            begin: /\}\}/
          }, e.BACKSLASH_ESCAPE, l]
        },
        o = {
          className: "string",
          begin: /\$@"/,
          end: '"',
          contains: [{
            begin: /\{\{/
          }, {
            begin: /\}\}/
          }, {
            begin: '""'
          }, r]
        },
        d = e.inherit(o, {
          illegal: /\n/,
          contains: [{
            begin: /\{\{/
          }, {
            begin: /\}\}/
          }, {
            begin: '""'
          }, l]
        });
      r.contains = [o, c, s, e.APOS_STRING_MODE, e.QUOTE_STRING_MODE, i, e.C_BLOCK_COMMENT_MODE], l.contains = [d, c, t, e.APOS_STRING_MODE, e.QUOTE_STRING_MODE, i, e.inherit(e.C_BLOCK_COMMENT_MODE, {
        illegal: /\n/
      })];
      var g = {
          variants: [o, c, s, e.APOS_STRING_MODE, e.QUOTE_STRING_MODE]
        },
        E = {
          begin: "<",
          end: ">",
          contains: [{
            beginKeywords: "in out"
          }, a]
        },
        _ = e.IDENT_RE + "(<" + e.IDENT_RE + "(\\s*,\\s*" + e.IDENT_RE + ")*>)?(\\[\\])?",
        b = {
          begin: "@" + e.IDENT_RE,
          relevance: 0
        };
      return {
        name: "C#",
        aliases: ["cs", "c#"],
        keywords: n,
        illegal: /::/,
        contains: [e.COMMENT("///", "$", {
          returnBegin: !0,
          contains: [{
            className: "doctag",
            variants: [{
              begin: "///",
              relevance: 0
            }, {
              begin: "\x3c!--|--\x3e"
            }, {
              begin: "</?",
              end: ">"
            }]
          }]
        }), e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE, {
          className: "meta",
          begin: "#",
          end: "$",
          keywords: {
            keyword: "if else elif endif define undef warning error line region endregion pragma checksum"
          }
        }, g, i, {
          beginKeywords: "class interface",
          relevance: 0,
          end: /[{;=]/,
          illegal: /[^\s:,]/,
          contains: [{
            beginKeywords: "where class"
          }, a, E, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE]
        }, {
          beginKeywords: "namespace",
          relevance: 0,
          end: /[{;=]/,
          illegal: /[^\s:]/,
          contains: [a, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE]
        }, {
          beginKeywords: "record",
          relevance: 0,
          end: /[{;=]/,
          illegal: /[^\s:]/,
          contains: [a, E, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE]
        }, {
          className: "meta",
          begin: "^\\s*\\[(?=[\\w])",
          excludeBegin: !0,
          end: "\\]",
          excludeEnd: !0,
          contains: [{
            className: "string",
            begin: /"/,
            end: /"/
          }]
        }, {
          beginKeywords: "new return throw await else",
          relevance: 0
        }, {
          className: "function",
          begin: "(" + _ + "\\s+)+" + e.IDENT_RE + "\\s*(<[^=]+>\\s*)?\\(",
          returnBegin: !0,
          end: /\s*[{;=]/,
          excludeEnd: !0,
          keywords: n,
          contains: [{
            beginKeywords: "public private protected static internal protected abstract async extern override unsafe virtual new sealed partial",
            relevance: 0
          }, {
            begin: e.IDENT_RE + "\\s*(<[^=]+>\\s*)?\\(",
            returnBegin: !0,
            contains: [e.TITLE_MODE, E],
            relevance: 0
          }, {
            match: /\(\)/
          }, {
            className: "params",
            begin: /\(/,
            end: /\)/,
            excludeBegin: !0,
            excludeEnd: !0,
            keywords: n,
            relevance: 0,
            contains: [g, i, e.C_BLOCK_COMMENT_MODE]
          }, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE]
        }, b]
      };
    };
  }();
  hljs.registerLanguage("csharp", e);
})(); /*! `php` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var t = e.regex,
        a = /(?![A-Za-z0-9])(?![$])/,
        r = t.concat(/[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*/, a),
        n = t.concat(/(\\?[A-Z][a-z0-9_\x7f-\xff]+|\\?[A-Z]+(?=[A-Z][a-z0-9_\x7f-\xff])){1,}/, a),
        o = {
          scope: "variable",
          match: "\\$+" + r
        },
        c = {
          scope: "subst",
          variants: [{
            begin: /\$\w+/
          }, {
            begin: /\{\$/,
            end: /\}/
          }]
        },
        i = e.inherit(e.APOS_STRING_MODE, {
          illegal: null
        }),
        s = "[ \t\n]",
        l = {
          scope: "string",
          variants: [e.inherit(e.QUOTE_STRING_MODE, {
            illegal: null,
            contains: e.QUOTE_STRING_MODE.contains.concat(c)
          }), i, e.END_SAME_AS_BEGIN({
            begin: /<<<[ \t]*(\w+)\n/,
            end: /[ \t]*(\w+)\b/,
            contains: e.QUOTE_STRING_MODE.contains.concat(c)
          })]
        },
        _ = {
          scope: "number",
          variants: [{
            begin: "\\b0[bB][01]+(?:_[01]+)*\\b"
          }, {
            begin: "\\b0[oO][0-7]+(?:_[0-7]+)*\\b"
          }, {
            begin: "\\b0[xX][\\da-fA-F]+(?:_[\\da-fA-F]+)*\\b"
          }, {
            begin: "(?:\\b\\d+(?:_\\d+)*(\\.(?:\\d+(?:_\\d+)*))?|\\B\\.\\d+)(?:[eE][+-]?\\d+)?"
          }],
          relevance: 0
        },
        d = ["false", "null", "true"],
        p = ["__CLASS__", "__DIR__", "__FILE__", "__FUNCTION__", "__COMPILER_HALT_OFFSET__", "__LINE__", "__METHOD__", "__NAMESPACE__", "__TRAIT__", "die", "echo", "exit", "include", "include_once", "print", "require", "require_once", "array", "abstract", "and", "as", "binary", "bool", "boolean", "break", "callable", "case", "catch", "class", "clone", "const", "continue", "declare", "default", "do", "double", "else", "elseif", "empty", "enddeclare", "endfor", "endforeach", "endif", "endswitch", "endwhile", "enum", "eval", "extends", "final", "finally", "float", "for", "foreach", "from", "global", "goto", "if", "implements", "instanceof", "insteadof", "int", "integer", "interface", "isset", "iterable", "list", "match|0", "mixed", "new", "never", "object", "or", "private", "protected", "public", "readonly", "real", "return", "string", "switch", "throw", "trait", "try", "unset", "use", "var", "void", "while", "xor", "yield"],
        b = ["Error|0", "AppendIterator", "ArgumentCountError", "ArithmeticError", "ArrayIterator", "ArrayObject", "AssertionError", "BadFunctionCallException", "BadMethodCallException", "CachingIterator", "CallbackFilterIterator", "CompileError", "Countable", "DirectoryIterator", "DivisionByZeroError", "DomainException", "EmptyIterator", "ErrorException", "Exception", "FilesystemIterator", "FilterIterator", "GlobIterator", "InfiniteIterator", "InvalidArgumentException", "IteratorIterator", "LengthException", "LimitIterator", "LogicException", "MultipleIterator", "NoRewindIterator", "OutOfBoundsException", "OutOfRangeException", "OuterIterator", "OverflowException", "ParentIterator", "ParseError", "RangeException", "RecursiveArrayIterator", "RecursiveCachingIterator", "RecursiveCallbackFilterIterator", "RecursiveDirectoryIterator", "RecursiveFilterIterator", "RecursiveIterator", "RecursiveIteratorIterator", "RecursiveRegexIterator", "RecursiveTreeIterator", "RegexIterator", "RuntimeException", "SeekableIterator", "SplDoublyLinkedList", "SplFileInfo", "SplFileObject", "SplFixedArray", "SplHeap", "SplMaxHeap", "SplMinHeap", "SplObjectStorage", "SplObserver", "SplPriorityQueue", "SplQueue", "SplStack", "SplSubject", "SplTempFileObject", "TypeError", "UnderflowException", "UnexpectedValueException", "UnhandledMatchError", "ArrayAccess", "BackedEnum", "Closure", "Fiber", "Generator", "Iterator", "IteratorAggregate", "Serializable", "Stringable", "Throwable", "Traversable", "UnitEnum", "WeakReference", "WeakMap", "Directory", "__PHP_Incomplete_Class", "parent", "php_user_filter", "self", "static", "stdClass"],
        E = {
          keyword: p,
          literal: function (e) {
            var t = [];
            return e.forEach(function (e) {
              t.push(e), e.toLowerCase() === e ? t.push(e.toUpperCase()) : t.push(e.toLowerCase());
            }), t;
          }(d),
          built_in: b
        },
        u = function u(e) {
          return e.map(function (e) {
            return e.replace(/\|\d+$/, "");
          });
        },
        g = {
          variants: [{
            match: [/new/, t.concat(s, "+"), t.concat("(?!", u(b).join("\\b|"), "\\b)"), n],
            scope: {
              1: "keyword",
              4: "title.class"
            }
          }]
        },
        h = t.concat(r, "\\b(?!\\()"),
        m = {
          variants: [{
            match: [t.concat(/::/, t.lookahead(/(?!class\b)/)), h],
            scope: {
              2: "variable.constant"
            }
          }, {
            match: [/::/, /class/],
            scope: {
              2: "variable.language"
            }
          }, {
            match: [n, t.concat(/::/, t.lookahead(/(?!class\b)/)), h],
            scope: {
              1: "title.class",
              3: "variable.constant"
            }
          }, {
            match: [n, t.concat("::", t.lookahead(/(?!class\b)/))],
            scope: {
              1: "title.class"
            }
          }, {
            match: [n, /::/, /class/],
            scope: {
              1: "title.class",
              3: "variable.language"
            }
          }]
        },
        I = {
          scope: "attr",
          match: t.concat(r, t.lookahead(":"), t.lookahead(/(?!::)/))
        },
        f = {
          relevance: 0,
          begin: /\(/,
          end: /\)/,
          keywords: E,
          contains: [I, o, m, e.C_BLOCK_COMMENT_MODE, l, _, g]
        },
        O = {
          relevance: 0,
          match: [/\b/, t.concat("(?!fn\\b|function\\b|", u(p).join("\\b|"), "|", u(b).join("\\b|"), "\\b)"), r, t.concat(s, "*"), t.lookahead(/(?=\()/)],
          scope: {
            3: "title.function.invoke"
          },
          contains: [f]
        };
      f.contains.push(O);
      var v = [I, m, e.C_BLOCK_COMMENT_MODE, l, _, g];
      return {
        case_insensitive: !1,
        keywords: E,
        contains: [{
          begin: t.concat(/#\[\s*/, n),
          beginScope: "meta",
          end: /]/,
          endScope: "meta",
          keywords: {
            literal: d,
            keyword: ["new", "array"]
          },
          contains: [{
            begin: /\[/,
            end: /]/,
            keywords: {
              literal: d,
              keyword: ["new", "array"]
            },
            contains: ["self"].concat(v)
          }].concat(v, [{
            scope: "meta",
            match: n
          }])
        }, e.HASH_COMMENT_MODE, e.COMMENT("//", "$"), e.COMMENT("/\\*", "\\*/", {
          contains: [{
            scope: "doctag",
            match: "@[A-Za-z]+"
          }]
        }), {
          match: /__halt_compiler\(\);/,
          keywords: "__halt_compiler",
          starts: {
            scope: "comment",
            end: e.MATCH_NOTHING_RE,
            contains: [{
              match: /\?>/,
              scope: "meta",
              endsParent: !0
            }]
          }
        }, {
          scope: "meta",
          variants: [{
            begin: /<\?php/,
            relevance: 10
          }, {
            begin: /<\?=/
          }, {
            begin: /<\?/,
            relevance: .1
          }, {
            begin: /\?>/
          }]
        }, {
          scope: "variable.language",
          match: /\$this\b/
        }, o, O, m, {
          match: [/const/, /\s/, r],
          scope: {
            1: "keyword",
            3: "variable.constant"
          }
        }, g, {
          scope: "function",
          relevance: 0,
          beginKeywords: "fn function",
          end: /[;{]/,
          excludeEnd: !0,
          illegal: "[$%\\[]",
          contains: [{
            beginKeywords: "use"
          }, e.UNDERSCORE_TITLE_MODE, {
            begin: "=>",
            endsParent: !0
          }, {
            scope: "params",
            begin: "\\(",
            end: "\\)",
            excludeBegin: !0,
            excludeEnd: !0,
            keywords: E,
            contains: ["self", o, m, e.C_BLOCK_COMMENT_MODE, l, _]
          }]
        }, {
          scope: "class",
          variants: [{
            beginKeywords: "enum",
            illegal: /[($"]/
          }, {
            beginKeywords: "class interface trait",
            illegal: /[:($"]/
          }],
          relevance: 0,
          end: /\{/,
          excludeEnd: !0,
          contains: [{
            beginKeywords: "extends implements"
          }, e.UNDERSCORE_TITLE_MODE]
        }, {
          beginKeywords: "namespace",
          relevance: 0,
          end: ";",
          illegal: /[.']/,
          contains: [e.inherit(e.UNDERSCORE_TITLE_MODE, {
            scope: "title.class"
          })]
        }, {
          beginKeywords: "use",
          relevance: 0,
          end: ";",
          contains: [{
            match: /\b(as|const|function)\b/,
            scope: "keyword"
          }, e.UNDERSCORE_TITLE_MODE]
        }, l, _]
      };
    };
  }();
  hljs.registerLanguage("php", e);
})(); /*! `typescript` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    var e = "[A-Za-z$_][0-9A-Za-z$_]*",
      n = ["as", "in", "of", "if", "for", "while", "finally", "var", "new", "function", "do", "return", "void", "else", "break", "catch", "instanceof", "with", "throw", "case", "default", "try", "switch", "continue", "typeof", "delete", "let", "yield", "const", "class", "debugger", "async", "await", "static", "import", "from", "export", "extends"],
      a = ["true", "false", "null", "undefined", "NaN", "Infinity"],
      t = ["Object", "Function", "Boolean", "Symbol", "Math", "Date", "Number", "BigInt", "String", "RegExp", "Array", "Float32Array", "Float64Array", "Int8Array", "Uint8Array", "Uint8ClampedArray", "Int16Array", "Int32Array", "Uint16Array", "Uint32Array", "BigInt64Array", "BigUint64Array", "Set", "Map", "WeakSet", "WeakMap", "ArrayBuffer", "SharedArrayBuffer", "Atomics", "DataView", "JSON", "Promise", "Generator", "GeneratorFunction", "AsyncFunction", "Reflect", "Proxy", "Intl", "WebAssembly"],
      s = ["Error", "EvalError", "InternalError", "RangeError", "ReferenceError", "SyntaxError", "TypeError", "URIError"],
      c = ["setInterval", "setTimeout", "clearInterval", "clearTimeout", "require", "exports", "eval", "isFinite", "isNaN", "parseFloat", "parseInt", "decodeURI", "decodeURIComponent", "encodeURI", "encodeURIComponent", "escape", "unescape"],
      r = ["arguments", "this", "super", "console", "window", "document", "localStorage", "module", "global"],
      i = [].concat(c, t, s);
    function o(o) {
      var l = o.regex,
        d = e,
        b = {
          begin: /<[A-Za-z0-9\\._:-]+/,
          end: /\/[A-Za-z0-9\\._:-]+>|\/>/,
          isTrulyOpeningTag: function isTrulyOpeningTag(e, n) {
            var a = e[0].length + e.index,
              t = e.input[a];
            if ("<" === t || "," === t) return void n.ignoreMatch();
            var s;
            ">" === t && (function (e, _ref8) {
              var n = _ref8.after;
              var a = "</" + e[0].slice(1);
              return -1 !== e.input.indexOf(a, n);
            }(e, {
              after: a
            }) || n.ignoreMatch());
            var c = e.input.substring(a);
            ((s = c.match(/^\s*=/)) || (s = c.match(/^\s+extends\s+/)) && 0 === s.index) && n.ignoreMatch();
          }
        },
        g = {
          $pattern: e,
          keyword: n,
          literal: a,
          built_in: i,
          "variable.language": r
        },
        u = "\\.([0-9](_?[0-9])*)",
        m = "0|[1-9](_?[0-9])*|0[0-7]*[89][0-9]*",
        E = {
          className: "number",
          variants: [{
            begin: "(\\b(".concat(m, ")((").concat(u, ")|\\.)?|(").concat(u, "))[eE][+-]?([0-9](_?[0-9])*)\\b")
          }, {
            begin: "\\b(".concat(m, ")\\b((").concat(u, ")\\b|\\.)?|(").concat(u, ")\\b")
          }, {
            begin: "\\b(0|[1-9](_?[0-9])*)n\\b"
          }, {
            begin: "\\b0[xX][0-9a-fA-F](_?[0-9a-fA-F])*n?\\b"
          }, {
            begin: "\\b0[bB][0-1](_?[0-1])*n?\\b"
          }, {
            begin: "\\b0[oO][0-7](_?[0-7])*n?\\b"
          }, {
            begin: "\\b0[0-7]+n?\\b"
          }],
          relevance: 0
        },
        y = {
          className: "subst",
          begin: "\\$\\{",
          end: "\\}",
          keywords: g,
          contains: []
        },
        A = {
          begin: "html`",
          end: "",
          starts: {
            end: "`",
            returnEnd: !1,
            contains: [o.BACKSLASH_ESCAPE, y],
            subLanguage: "xml"
          }
        },
        p = {
          begin: "css`",
          end: "",
          starts: {
            end: "`",
            returnEnd: !1,
            contains: [o.BACKSLASH_ESCAPE, y],
            subLanguage: "css"
          }
        },
        _ = {
          className: "string",
          begin: "`",
          end: "`",
          contains: [o.BACKSLASH_ESCAPE, y]
        },
        N = {
          className: "comment",
          variants: [o.COMMENT(/\/\*\*(?!\/)/, "\\*/", {
            relevance: 0,
            contains: [{
              begin: "(?=@[A-Za-z]+)",
              relevance: 0,
              contains: [{
                className: "doctag",
                begin: "@[A-Za-z]+"
              }, {
                className: "type",
                begin: "\\{",
                end: "\\}",
                excludeEnd: !0,
                excludeBegin: !0,
                relevance: 0
              }, {
                className: "variable",
                begin: d + "(?=\\s*(-)|$)",
                endsParent: !0,
                relevance: 0
              }, {
                begin: /(?=[^\n])\s/,
                relevance: 0
              }]
            }]
          }), o.C_BLOCK_COMMENT_MODE, o.C_LINE_COMMENT_MODE]
        },
        f = [o.APOS_STRING_MODE, o.QUOTE_STRING_MODE, A, p, _, {
          match: /\$\d+/
        }, E];
      y.contains = f.concat({
        begin: /\{/,
        end: /\}/,
        keywords: g,
        contains: ["self"].concat(f)
      });
      var h = [].concat(N, y.contains),
        v = h.concat([{
          begin: /\(/,
          end: /\)/,
          keywords: g,
          contains: ["self"].concat(h)
        }]),
        S = {
          className: "params",
          begin: /\(/,
          end: /\)/,
          excludeBegin: !0,
          excludeEnd: !0,
          keywords: g,
          contains: v
        },
        w = {
          variants: [{
            match: [/class/, /\s+/, d, /\s+/, /extends/, /\s+/, l.concat(d, "(", l.concat(/\./, d), ")*")],
            scope: {
              1: "keyword",
              3: "title.class",
              5: "keyword",
              7: "title.class.inherited"
            }
          }, {
            match: [/class/, /\s+/, d],
            scope: {
              1: "keyword",
              3: "title.class"
            }
          }]
        },
        R = {
          relevance: 0,
          match: l.either(/\bJSON/, /\b[A-Z][a-z]+([A-Z][a-z]*|\d)*/, /\b[A-Z]{2,}([A-Z][a-z]+|\d)+([A-Z][a-z]*)*/, /\b[A-Z]{2,}[a-z]+([A-Z][a-z]+|\d)*([A-Z][a-z]*)*/),
          className: "title.class",
          keywords: {
            _: [].concat(t, s)
          }
        },
        x = {
          variants: [{
            match: [/function/, /\s+/, d, /(?=\s*\()/]
          }, {
            match: [/function/, /\s*(?=\()/]
          }],
          className: {
            1: "keyword",
            3: "title.function"
          },
          label: "func.def",
          contains: [S],
          illegal: /%/
        },
        k = {
          match: l.concat(/\b/, (O = [].concat(c, ["super", "import"]), l.concat("(?!", O.join("|"), ")")), d, l.lookahead(/\(/)),
          className: "title.function",
          relevance: 0
        };
      var O;
      var I = {
          begin: l.concat(/\./, l.lookahead(l.concat(d, /(?![0-9A-Za-z$_(])/))),
          end: d,
          excludeBegin: !0,
          keywords: "prototype",
          className: "property",
          relevance: 0
        },
        C = {
          match: [/get|set/, /\s+/, d, /(?=\()/],
          className: {
            1: "keyword",
            3: "title.function"
          },
          contains: [{
            begin: /\(\)/
          }, S]
        },
        T = "(\\([^()]*(\\([^()]*(\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)|" + o.UNDERSCORE_IDENT_RE + ")\\s*=>",
        M = {
          match: [/const|var|let/, /\s+/, d, /\s*/, /=\s*/, /(async\s*)?/, l.lookahead(T)],
          keywords: "async",
          className: {
            1: "keyword",
            3: "title.function"
          },
          contains: [S]
        };
      return {
        name: "Javascript",
        aliases: ["js", "jsx", "mjs", "cjs"],
        keywords: g,
        exports: {
          PARAMS_CONTAINS: v,
          CLASS_REFERENCE: R
        },
        illegal: /#(?![$_A-z])/,
        contains: [o.SHEBANG({
          label: "shebang",
          binary: "node",
          relevance: 5
        }), {
          label: "use_strict",
          className: "meta",
          relevance: 10,
          begin: /^\s*['"]use (strict|asm)['"]/
        }, o.APOS_STRING_MODE, o.QUOTE_STRING_MODE, A, p, _, N, {
          match: /\$\d+/
        }, E, R, {
          className: "attr",
          begin: d + l.lookahead(":"),
          relevance: 0
        }, M, {
          begin: "(" + o.RE_STARTERS_RE + "|\\b(case|return|throw)\\b)\\s*",
          keywords: "return throw case",
          relevance: 0,
          contains: [N, o.REGEXP_MODE, {
            className: "function",
            begin: T,
            returnBegin: !0,
            end: "\\s*=>",
            contains: [{
              className: "params",
              variants: [{
                begin: o.UNDERSCORE_IDENT_RE,
                relevance: 0
              }, {
                className: null,
                begin: /\(\s*\)/,
                skip: !0
              }, {
                begin: /\(/,
                end: /\)/,
                excludeBegin: !0,
                excludeEnd: !0,
                keywords: g,
                contains: v
              }]
            }]
          }, {
            begin: /,/,
            relevance: 0
          }, {
            match: /\s+/,
            relevance: 0
          }, {
            variants: [{
              begin: "<>",
              end: "</>"
            }, {
              match: /<[A-Za-z0-9\\._:-]+\s*\/>/
            }, {
              begin: b.begin,
              "on:begin": b.isTrulyOpeningTag,
              end: b.end
            }],
            subLanguage: "xml",
            contains: [{
              begin: b.begin,
              end: b.end,
              skip: !0,
              contains: ["self"]
            }]
          }]
        }, x, {
          beginKeywords: "while if switch catch for"
        }, {
          begin: "\\b(?!function)" + o.UNDERSCORE_IDENT_RE + "\\([^()]*(\\([^()]*(\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)\\s*\\{",
          returnBegin: !0,
          label: "func.def",
          contains: [S, o.inherit(o.TITLE_MODE, {
            begin: d,
            className: "title.function"
          })]
        }, {
          match: /\.\.\./,
          relevance: 0
        }, I, {
          match: "\\$" + d,
          relevance: 0
        }, {
          match: [/\bconstructor(?=\s*\()/],
          className: {
            1: "title.function"
          },
          contains: [S]
        }, k, {
          relevance: 0,
          match: /\b[A-Z][A-Z_0-9]+\b/,
          className: "variable.constant"
        }, w, C, {
          match: /\$[(.]/
        }]
      };
    }
    return function (t) {
      var s = o(t),
        c = ["any", "void", "number", "boolean", "string", "object", "never", "symbol", "bigint", "unknown"],
        l = {
          beginKeywords: "namespace",
          end: /\{/,
          excludeEnd: !0,
          contains: [s.exports.CLASS_REFERENCE]
        },
        d = {
          beginKeywords: "interface",
          end: /\{/,
          excludeEnd: !0,
          keywords: {
            keyword: "interface extends",
            built_in: c
          },
          contains: [s.exports.CLASS_REFERENCE]
        },
        b = {
          $pattern: e,
          keyword: n.concat(["type", "namespace", "interface", "public", "private", "protected", "implements", "declare", "abstract", "readonly", "enum", "override"]),
          literal: a,
          built_in: i.concat(c),
          "variable.language": r
        },
        g = {
          className: "meta",
          begin: "@[A-Za-z$_][0-9A-Za-z$_]*"
        },
        u = function u(e, n, a) {
          var t = e.contains.findIndex(function (e) {
            return e.label === n;
          });
          if (-1 === t) throw Error("can not find mode to replace");
          e.contains.splice(t, 1, a);
        };
      return Object.assign(s.keywords, b), s.exports.PARAMS_CONTAINS.push(g), s.contains = s.contains.concat([g, l, d]), u(s, "shebang", t.SHEBANG()), u(s, "use_strict", {
        className: "meta",
        relevance: 10,
        begin: /^\s*['"]use strict['"]/
      }), s.contains.find(function (e) {
        return "func.def" === e.label;
      }).relevance = 0, Object.assign(s, {
        name: "TypeScript",
        aliases: ["ts", "tsx"]
      }), s;
    };
  }();
  hljs.registerLanguage("typescript", e);
})(); /*! `kotlin` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    var e = "\\.([0-9](_*[0-9])*)",
      n = "[0-9a-fA-F](_*[0-9a-fA-F])*",
      a = {
        className: "number",
        variants: [{
          begin: "(\\b([0-9](_*[0-9])*)((".concat(e, ")|\\.)?|(").concat(e, "))[eE][+-]?([0-9](_*[0-9])*)[fFdD]?\\b")
        }, {
          begin: "\\b([0-9](_*[0-9])*)((".concat(e, ")[fFdD]?\\b|\\.([fFdD]\\b)?)")
        }, {
          begin: "(".concat(e, ")[fFdD]?\\b")
        }, {
          begin: "\\b([0-9](_*[0-9])*)[fFdD]\\b"
        }, {
          begin: "\\b0[xX]((".concat(n, ")\\.?|(").concat(n, ")?\\.(").concat(n, "))[pP][+-]?([0-9](_*[0-9])*)[fFdD]?\\b")
        }, {
          begin: "\\b(0|[1-9](_*[0-9])*)[lL]?\\b"
        }, {
          begin: "\\b0[xX](".concat(n, ")[lL]?\\b")
        }, {
          begin: "\\b0(_*[0-7])*[lL]?\\b"
        }, {
          begin: "\\b0[bB][01](_*[01])*[lL]?\\b"
        }],
        relevance: 0
      };
    return function (e) {
      var n = {
          keyword: "abstract as val var vararg get set class object open private protected public noinline crossinline dynamic final enum if else do while for when throw try catch finally import package is in fun override companion reified inline lateinit init interface annotation data sealed internal infix operator out by constructor super tailrec where const inner suspend typealias external expect actual",
          built_in: "Byte Short Char Int Long Boolean Float Double Void Unit Nothing",
          literal: "true false null"
        },
        i = {
          className: "symbol",
          begin: e.UNDERSCORE_IDENT_RE + "@"
        },
        s = {
          className: "subst",
          begin: /\$\{/,
          end: /\}/,
          contains: [e.C_NUMBER_MODE]
        },
        t = {
          className: "variable",
          begin: "\\$" + e.UNDERSCORE_IDENT_RE
        },
        r = {
          className: "string",
          variants: [{
            begin: '"""',
            end: '"""(?=[^"])',
            contains: [t, s]
          }, {
            begin: "'",
            end: "'",
            illegal: /\n/,
            contains: [e.BACKSLASH_ESCAPE]
          }, {
            begin: '"',
            end: '"',
            illegal: /\n/,
            contains: [e.BACKSLASH_ESCAPE, t, s]
          }]
        };
      s.contains.push(r);
      var l = {
          className: "meta",
          begin: "@(?:file|property|field|get|set|receiver|param|setparam|delegate)\\s*:(?:\\s*" + e.UNDERSCORE_IDENT_RE + ")?"
        },
        c = {
          className: "meta",
          begin: "@" + e.UNDERSCORE_IDENT_RE,
          contains: [{
            begin: /\(/,
            end: /\)/,
            contains: [e.inherit(r, {
              className: "string"
            }), "self"]
          }]
        },
        o = a,
        b = e.COMMENT("/\\*", "\\*/", {
          contains: [e.C_BLOCK_COMMENT_MODE]
        }),
        E = {
          variants: [{
            className: "type",
            begin: e.UNDERSCORE_IDENT_RE
          }, {
            begin: /\(/,
            end: /\)/,
            contains: []
          }]
        },
        d = E;
      return d.variants[1].contains = [E], E.variants[1].contains = [d], {
        name: "Kotlin",
        aliases: ["kt", "kts"],
        keywords: n,
        contains: [e.COMMENT("/\\*\\*", "\\*/", {
          relevance: 0,
          contains: [{
            className: "doctag",
            begin: "@[A-Za-z]+"
          }]
        }), e.C_LINE_COMMENT_MODE, b, {
          className: "keyword",
          begin: /\b(break|continue|return|this)\b/,
          starts: {
            contains: [{
              className: "symbol",
              begin: /@\w+/
            }]
          }
        }, i, l, c, {
          className: "function",
          beginKeywords: "fun",
          end: "[(]|$",
          returnBegin: !0,
          excludeEnd: !0,
          keywords: n,
          relevance: 5,
          contains: [{
            begin: e.UNDERSCORE_IDENT_RE + "\\s*\\(",
            returnBegin: !0,
            relevance: 0,
            contains: [e.UNDERSCORE_TITLE_MODE]
          }, {
            className: "type",
            begin: /</,
            end: />/,
            keywords: "reified",
            relevance: 0
          }, {
            className: "params",
            begin: /\(/,
            end: /\)/,
            endsParent: !0,
            keywords: n,
            relevance: 0,
            contains: [{
              begin: /:/,
              end: /[=,\/]/,
              endsWithParent: !0,
              contains: [E, e.C_LINE_COMMENT_MODE, b],
              relevance: 0
            }, e.C_LINE_COMMENT_MODE, b, l, c, r, e.C_NUMBER_MODE]
          }, b]
        }, {
          begin: [/class|interface|trait/, /\s+/, e.UNDERSCORE_IDENT_RE],
          beginScope: {
            3: "title.class"
          },
          keywords: "class interface trait",
          end: /[:\{(]|$/,
          excludeEnd: !0,
          illegal: "extends implements",
          contains: [{
            beginKeywords: "public protected internal private constructor"
          }, e.UNDERSCORE_TITLE_MODE, {
            className: "type",
            begin: /</,
            end: />/,
            excludeBegin: !0,
            excludeEnd: !0,
            relevance: 0
          }, {
            className: "type",
            begin: /[,:]\s*/,
            end: /[<\(,){\s]|$/,
            excludeBegin: !0,
            returnEnd: !0
          }, l, c]
        }, r, {
          className: "meta",
          begin: "^#!/usr/bin/env",
          end: "$",
          illegal: "\n"
        }, o]
      };
    };
  }();
  hljs.registerLanguage("kotlin", e);
})(); /*! `ruby` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = e.regex,
        a = "([a-zA-Z_]\\w*[!?=]?|[-+~]@|<<|>>|=~|===?|<=>|[<>]=?|\\*\\*|[-/+%^&*~`|]|\\[\\]=?)",
        s = n.either(/\b([A-Z]+[a-z0-9]+)+/, /\b([A-Z]+[a-z0-9]+)+[A-Z]+/),
        i = n.concat(s, /(::\w+)*/),
        t = {
          "variable.constant": ["__FILE__", "__LINE__", "__ENCODING__"],
          "variable.language": ["self", "super"],
          keyword: ["alias", "and", "begin", "BEGIN", "break", "case", "class", "defined", "do", "else", "elsif", "end", "END", "ensure", "for", "if", "in", "module", "next", "not", "or", "redo", "require", "rescue", "retry", "return", "then", "undef", "unless", "until", "when", "while", "yield", "include", "extend", "prepend", "public", "private", "protected", "raise", "throw"],
          built_in: ["proc", "lambda", "attr_accessor", "attr_reader", "attr_writer", "define_method", "private_constant", "module_function"],
          literal: ["true", "false", "nil"]
        },
        c = {
          className: "doctag",
          begin: "@[A-Za-z]+"
        },
        r = {
          begin: "#<",
          end: ">"
        },
        b = [e.COMMENT("#", "$", {
          contains: [c]
        }), e.COMMENT("^=begin", "^=end", {
          contains: [c],
          relevance: 10
        }), e.COMMENT("^__END__", e.MATCH_NOTHING_RE)],
        l = {
          className: "subst",
          begin: /#\{/,
          end: /\}/,
          keywords: t
        },
        d = {
          className: "string",
          contains: [e.BACKSLASH_ESCAPE, l],
          variants: [{
            begin: /'/,
            end: /'/
          }, {
            begin: /"/,
            end: /"/
          }, {
            begin: /`/,
            end: /`/
          }, {
            begin: /%[qQwWx]?\(/,
            end: /\)/
          }, {
            begin: /%[qQwWx]?\[/,
            end: /\]/
          }, {
            begin: /%[qQwWx]?\{/,
            end: /\}/
          }, {
            begin: /%[qQwWx]?</,
            end: />/
          }, {
            begin: /%[qQwWx]?\//,
            end: /\//
          }, {
            begin: /%[qQwWx]?%/,
            end: /%/
          }, {
            begin: /%[qQwWx]?-/,
            end: /-/
          }, {
            begin: /%[qQwWx]?\|/,
            end: /\|/
          }, {
            begin: /\B\?(\\\d{1,3})/
          }, {
            begin: /\B\?(\\x[A-Fa-f0-9]{1,2})/
          }, {
            begin: /\B\?(\\u\{?[A-Fa-f0-9]{1,6}\}?)/
          }, {
            begin: /\B\?(\\M-\\C-|\\M-\\c|\\c\\M-|\\M-|\\C-\\M-)[\x20-\x7e]/
          }, {
            begin: /\B\?\\(c|C-)[\x20-\x7e]/
          }, {
            begin: /\B\?\\?\S/
          }, {
            begin: n.concat(/<<[-~]?'?/, n.lookahead(/(\w+)(?=\W)[^\n]*\n(?:[^\n]*\n)*?\s*\1\b/)),
            contains: [e.END_SAME_AS_BEGIN({
              begin: /(\w+)/,
              end: /(\w+)/,
              contains: [e.BACKSLASH_ESCAPE, l]
            })]
          }]
        },
        o = "[0-9](_?[0-9])*",
        g = {
          className: "number",
          relevance: 0,
          variants: [{
            begin: "\\b([1-9](_?[0-9])*|0)(\\.(".concat(o, "))?([eE][+-]?(").concat(o, ")|r)?i?\\b")
          }, {
            begin: "\\b0[dD][0-9](_?[0-9])*r?i?\\b"
          }, {
            begin: "\\b0[bB][0-1](_?[0-1])*r?i?\\b"
          }, {
            begin: "\\b0[oO][0-7](_?[0-7])*r?i?\\b"
          }, {
            begin: "\\b0[xX][0-9a-fA-F](_?[0-9a-fA-F])*r?i?\\b"
          }, {
            begin: "\\b0(_?[0-7])+r?i?\\b"
          }]
        },
        _ = {
          variants: [{
            match: /\(\)/
          }, {
            className: "params",
            begin: /\(/,
            end: /(?=\))/,
            excludeBegin: !0,
            endsParent: !0,
            keywords: t
          }]
        },
        u = [d, {
          variants: [{
            match: [/class\s+/, i, /\s+<\s+/, i]
          }, {
            match: [/\b(class|module)\s+/, i]
          }],
          scope: {
            2: "title.class",
            4: "title.class.inherited"
          },
          keywords: t
        }, {
          match: [/(include|extend)\s+/, i],
          scope: {
            2: "title.class"
          },
          keywords: t
        }, {
          relevance: 0,
          match: [i, /\.new[. (]/],
          scope: {
            1: "title.class"
          }
        }, {
          relevance: 0,
          match: /\b[A-Z][A-Z_0-9]+\b/,
          className: "variable.constant"
        }, {
          relevance: 0,
          match: s,
          scope: "title.class"
        }, {
          match: [/def/, /\s+/, a],
          scope: {
            1: "keyword",
            3: "title.function"
          },
          contains: [_]
        }, {
          begin: e.IDENT_RE + "::"
        }, {
          className: "symbol",
          begin: e.UNDERSCORE_IDENT_RE + "(!|\\?)?:",
          relevance: 0
        }, {
          className: "symbol",
          begin: ":(?!\\s)",
          contains: [d, {
            begin: a
          }],
          relevance: 0
        }, g, {
          className: "variable",
          begin: "(\\$\\W)|((\\$|@@?)(\\w+))(?=[^@$?])(?![A-Za-z])(?![@$?'])"
        }, {
          className: "params",
          begin: /\|/,
          end: /\|/,
          excludeBegin: !0,
          excludeEnd: !0,
          relevance: 0,
          keywords: t
        }, {
          begin: "(" + e.RE_STARTERS_RE + "|unless)\\s*",
          keywords: "unless",
          contains: [{
            className: "regexp",
            contains: [e.BACKSLASH_ESCAPE, l],
            illegal: /\n/,
            variants: [{
              begin: "/",
              end: "/[a-z]*"
            }, {
              begin: /%r\{/,
              end: /\}[a-z]*/
            }, {
              begin: "%r\\(",
              end: "\\)[a-z]*"
            }, {
              begin: "%r!",
              end: "![a-z]*"
            }, {
              begin: "%r\\[",
              end: "\\][a-z]*"
            }]
          }].concat(r, b),
          relevance: 0
        }].concat(r, b);
      l.contains = u, _.contains = u;
      var m = [{
        begin: /^\s*=>/,
        starts: {
          end: "$",
          contains: u
        }
      }, {
        className: "meta.prompt",
        begin: "^([>?]>|[\\w#]+\\(\\w+\\):\\d+:\\d+[>*]|(\\w+-)?\\d+\\.\\d+\\.\\d+(p\\d+)?[^\\d][^>]+>)(?=[ ])",
        starts: {
          end: "$",
          keywords: t,
          contains: u
        }
      }];
      return b.unshift(r), {
        name: "Ruby",
        aliases: ["rb", "gemspec", "podspec", "thor", "irb"],
        keywords: t,
        illegal: /\/\*/,
        contains: [e.SHEBANG({
          binary: "ruby"
        })].concat(m).concat(b).concat(u)
      };
    };
  }();
  hljs.registerLanguage("ruby", e);
})(); /*! `yaml` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = "true false yes no null",
        a = "[\\w#;/?:@&=+$,.~*'()[\\]]+",
        s = {
          className: "string",
          relevance: 0,
          variants: [{
            begin: /'/,
            end: /'/
          }, {
            begin: /"/,
            end: /"/
          }, {
            begin: /\S+/
          }],
          contains: [e.BACKSLASH_ESCAPE, {
            className: "template-variable",
            variants: [{
              begin: /\{\{/,
              end: /\}\}/
            }, {
              begin: /%\{/,
              end: /\}/
            }]
          }]
        },
        i = e.inherit(s, {
          variants: [{
            begin: /'/,
            end: /'/
          }, {
            begin: /"/,
            end: /"/
          }, {
            begin: /[^\s,{}[\]]+/
          }]
        }),
        l = {
          end: ",",
          endsWithParent: !0,
          excludeEnd: !0,
          keywords: n,
          relevance: 0
        },
        t = {
          begin: /\{/,
          end: /\}/,
          contains: [l],
          illegal: "\\n",
          relevance: 0
        },
        g = {
          begin: "\\[",
          end: "\\]",
          contains: [l],
          illegal: "\\n",
          relevance: 0
        },
        b = [{
          className: "attr",
          variants: [{
            begin: "\\w[\\w :\\/.-]*:(?=[ \t]|$)"
          }, {
            begin: '"\\w[\\w :\\/.-]*":(?=[ \t]|$)'
          }, {
            begin: "'\\w[\\w :\\/.-]*':(?=[ \t]|$)"
          }]
        }, {
          className: "meta",
          begin: "^---\\s*$",
          relevance: 10
        }, {
          className: "string",
          begin: "[\\|>]([1-9]?[+-])?[ ]*\\n( +)[^ ][^\\n]*\\n(\\2[^\\n]+\\n?)*"
        }, {
          begin: "<%[%=-]?",
          end: "[%-]?%>",
          subLanguage: "ruby",
          excludeBegin: !0,
          excludeEnd: !0,
          relevance: 0
        }, {
          className: "type",
          begin: "!\\w+!" + a
        }, {
          className: "type",
          begin: "!<" + a + ">"
        }, {
          className: "type",
          begin: "!" + a
        }, {
          className: "type",
          begin: "!!" + a
        }, {
          className: "meta",
          begin: "&" + e.UNDERSCORE_IDENT_RE + "$"
        }, {
          className: "meta",
          begin: "\\*" + e.UNDERSCORE_IDENT_RE + "$"
        }, {
          className: "bullet",
          begin: "-(?=[ ]|$)",
          relevance: 0
        }, e.HASH_COMMENT_MODE, {
          beginKeywords: n,
          keywords: {
            literal: n
          }
        }, {
          className: "number",
          begin: "\\b[0-9]{4}(-[0-9][0-9]){0,2}([Tt \\t][0-9][0-9]?(:[0-9][0-9]){2})?(\\.[0-9]*)?([ \\t])*(Z|[-+][0-9][0-9]?(:[0-9][0-9])?)?\\b"
        }, {
          className: "number",
          begin: e.C_NUMBER_RE + "\\b",
          relevance: 0
        }, t, g, s],
        r = [].concat(b);
      return r.pop(), r.push(i), l.contains = r, {
        name: "YAML",
        case_insensitive: !0,
        aliases: ["yml"],
        contains: b
      };
    };
  }();
  hljs.registerLanguage("yaml", e);
})(); /*! `cpp` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var t = e.regex,
        a = e.COMMENT("//", "$", {
          contains: [{
            begin: /\\\n/
          }]
        }),
        n = "[a-zA-Z_]\\w*::",
        r = "(?!struct)(decltype\\(auto\\)|" + t.optional(n) + "[a-zA-Z_]\\w*" + t.optional("<[^<>]+>") + ")",
        i = {
          className: "type",
          begin: "\\b[a-z\\d_]*_t\\b"
        },
        s = {
          className: "string",
          variants: [{
            begin: '(u8?|U|L)?"',
            end: '"',
            illegal: "\\n",
            contains: [e.BACKSLASH_ESCAPE]
          }, {
            begin: "(u8?|U|L)?'(\\\\(x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4,8}|[0-7]{3}|\\S)|.)",
            end: "'",
            illegal: "."
          }, e.END_SAME_AS_BEGIN({
            begin: /(?:u8?|U|L)?R"([^()\\ ]{0,16})\(/,
            end: /\)([^()\\ ]{0,16})"/
          })]
        },
        c = {
          className: "number",
          variants: [{
            begin: "\\b(0b[01']+)"
          }, {
            begin: "(-?)\\b([\\d']+(\\.[\\d']*)?|\\.[\\d']+)((ll|LL|l|L)(u|U)?|(u|U)(ll|LL|l|L)?|f|F|b|B)"
          }, {
            begin: "(-?)(\\b0[xX][a-fA-F0-9']+|(\\b[\\d']+(\\.[\\d']*)?|\\.[\\d']+)([eE][-+]?[\\d']+)?)"
          }],
          relevance: 0
        },
        o = {
          className: "meta",
          begin: /#\s*[a-z]+\b/,
          end: /$/,
          keywords: {
            keyword: "if else elif endif define undef warning error line pragma _Pragma ifdef ifndef include"
          },
          contains: [{
            begin: /\\\n/,
            relevance: 0
          }, e.inherit(s, {
            className: "string"
          }), {
            className: "string",
            begin: /<.*?>/
          }, a, e.C_BLOCK_COMMENT_MODE]
        },
        l = {
          className: "title",
          begin: t.optional(n) + e.IDENT_RE,
          relevance: 0
        },
        d = t.optional(n) + e.IDENT_RE + "\\s*\\(",
        u = {
          type: ["bool", "char", "char16_t", "char32_t", "char8_t", "double", "float", "int", "long", "short", "void", "wchar_t", "unsigned", "signed", "const", "static"],
          keyword: ["alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit", "atomic_noexcept", "auto", "bitand", "bitor", "break", "case", "catch", "class", "co_await", "co_return", "co_yield", "compl", "concept", "const_cast|10", "consteval", "constexpr", "constinit", "continue", "decltype", "default", "delete", "do", "dynamic_cast|10", "else", "enum", "explicit", "export", "extern", "false", "final", "for", "friend", "goto", "if", "import", "inline", "module", "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "override", "private", "protected", "public", "reflexpr", "register", "reinterpret_cast|10", "requires", "return", "sizeof", "static_assert", "static_cast|10", "struct", "switch", "synchronized", "template", "this", "thread_local", "throw", "transaction_safe", "transaction_safe_dynamic", "true", "try", "typedef", "typeid", "typename", "union", "using", "virtual", "volatile", "while", "xor", "xor_eq"],
          literal: ["NULL", "false", "nullopt", "nullptr", "true"],
          built_in: ["_Pragma"],
          _type_hints: ["any", "auto_ptr", "barrier", "binary_semaphore", "bitset", "complex", "condition_variable", "condition_variable_any", "counting_semaphore", "deque", "false_type", "future", "imaginary", "initializer_list", "istringstream", "jthread", "latch", "lock_guard", "multimap", "multiset", "mutex", "optional", "ostringstream", "packaged_task", "pair", "promise", "priority_queue", "queue", "recursive_mutex", "recursive_timed_mutex", "scoped_lock", "set", "shared_future", "shared_lock", "shared_mutex", "shared_timed_mutex", "shared_ptr", "stack", "string_view", "stringstream", "timed_mutex", "thread", "true_type", "tuple", "unique_lock", "unique_ptr", "unordered_map", "unordered_multimap", "unordered_multiset", "unordered_set", "variant", "vector", "weak_ptr", "wstring", "wstring_view"]
        },
        p = {
          className: "function.dispatch",
          relevance: 0,
          keywords: {
            _hint: ["abort", "abs", "acos", "apply", "as_const", "asin", "atan", "atan2", "calloc", "ceil", "cerr", "cin", "clog", "cos", "cosh", "cout", "declval", "endl", "exchange", "exit", "exp", "fabs", "floor", "fmod", "forward", "fprintf", "fputs", "free", "frexp", "fscanf", "future", "invoke", "isalnum", "isalpha", "iscntrl", "isdigit", "isgraph", "islower", "isprint", "ispunct", "isspace", "isupper", "isxdigit", "labs", "launder", "ldexp", "log", "log10", "make_pair", "make_shared", "make_shared_for_overwrite", "make_tuple", "make_unique", "malloc", "memchr", "memcmp", "memcpy", "memset", "modf", "move", "pow", "printf", "putchar", "puts", "realloc", "scanf", "sin", "sinh", "snprintf", "sprintf", "sqrt", "sscanf", "std", "stderr", "stdin", "stdout", "strcat", "strchr", "strcmp", "strcpy", "strcspn", "strlen", "strncat", "strncmp", "strncpy", "strpbrk", "strrchr", "strspn", "strstr", "swap", "tan", "tanh", "terminate", "to_underlying", "tolower", "toupper", "vfprintf", "visit", "vprintf", "vsprintf"]
          },
          begin: t.concat(/\b/, /(?!decltype)/, /(?!if)/, /(?!for)/, /(?!switch)/, /(?!while)/, e.IDENT_RE, t.lookahead(/(<[^<>]+>|)\s*\(/))
        },
        _ = [p, o, i, a, e.C_BLOCK_COMMENT_MODE, c, s],
        m = {
          variants: [{
            begin: /=/,
            end: /;/
          }, {
            begin: /\(/,
            end: /\)/
          }, {
            beginKeywords: "new throw return else",
            end: /;/
          }],
          keywords: u,
          contains: _.concat([{
            begin: /\(/,
            end: /\)/,
            keywords: u,
            contains: _.concat(["self"]),
            relevance: 0
          }]),
          relevance: 0
        },
        g = {
          className: "function",
          begin: "(" + r + "[\\*&\\s]+)+" + d,
          returnBegin: !0,
          end: /[{;=]/,
          excludeEnd: !0,
          keywords: u,
          illegal: /[^\w\s\*&:<>.]/,
          contains: [{
            begin: "decltype\\(auto\\)",
            keywords: u,
            relevance: 0
          }, {
            begin: d,
            returnBegin: !0,
            contains: [l],
            relevance: 0
          }, {
            begin: /::/,
            relevance: 0
          }, {
            begin: /:/,
            endsWithParent: !0,
            contains: [s, c]
          }, {
            relevance: 0,
            match: /,/
          }, {
            className: "params",
            begin: /\(/,
            end: /\)/,
            keywords: u,
            relevance: 0,
            contains: [a, e.C_BLOCK_COMMENT_MODE, s, c, i, {
              begin: /\(/,
              end: /\)/,
              keywords: u,
              relevance: 0,
              contains: ["self", a, e.C_BLOCK_COMMENT_MODE, s, c, i]
            }]
          }, i, a, e.C_BLOCK_COMMENT_MODE, o]
        };
      return {
        name: "C++",
        aliases: ["cc", "c++", "h++", "hpp", "hh", "hxx", "cxx"],
        keywords: u,
        illegal: "</",
        classNameAliases: {
          "function.dispatch": "built_in"
        },
        contains: [].concat(m, g, p, _, [o, {
          begin: "\\b(deque|list|queue|priority_queue|pair|stack|vector|map|set|bitset|multiset|multimap|unordered_map|unordered_set|unordered_multiset|unordered_multimap|array|tuple|optional|variant|function)\\s*<(?!<)",
          end: ">",
          keywords: u,
          contains: ["self", i]
        }, {
          begin: e.IDENT_RE + "::",
          keywords: u
        }, {
          match: [/\b(?:enum(?:\s+(?:class|struct))?|class|struct|union)/, /\s+/, /\w+/],
          className: {
            1: "keyword",
            3: "title.class"
          }
        }])
      };
    };
  }();
  hljs.registerLanguage("cpp", e);
})(); /*! `less` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    var e = ["a", "abbr", "address", "article", "aside", "audio", "b", "blockquote", "body", "button", "canvas", "caption", "cite", "code", "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "mark", "menu", "nav", "object", "ol", "p", "q", "quote", "samp", "section", "span", "strong", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "tr", "ul", "var", "video"],
      t = ["any-hover", "any-pointer", "aspect-ratio", "color", "color-gamut", "color-index", "device-aspect-ratio", "device-height", "device-width", "display-mode", "forced-colors", "grid", "height", "hover", "inverted-colors", "monochrome", "orientation", "overflow-block", "overflow-inline", "pointer", "prefers-color-scheme", "prefers-contrast", "prefers-reduced-motion", "prefers-reduced-transparency", "resolution", "scan", "scripting", "update", "width", "min-width", "max-width", "min-height", "max-height"],
      r = ["active", "any-link", "blank", "checked", "current", "default", "defined", "dir", "disabled", "drop", "empty", "enabled", "first", "first-child", "first-of-type", "fullscreen", "future", "focus", "focus-visible", "focus-within", "has", "host", "host-context", "hover", "indeterminate", "in-range", "invalid", "is", "lang", "last-child", "last-of-type", "left", "link", "local-link", "not", "nth-child", "nth-col", "nth-last-child", "nth-last-col", "nth-last-of-type", "nth-of-type", "only-child", "only-of-type", "optional", "out-of-range", "past", "placeholder-shown", "read-only", "read-write", "required", "right", "root", "scope", "target", "target-within", "user-invalid", "valid", "visited", "where"],
      i = ["after", "backdrop", "before", "cue", "cue-region", "first-letter", "first-line", "grammar-error", "marker", "part", "placeholder", "selection", "slotted", "spelling-error"],
      o = ["align-content", "align-items", "align-self", "all", "animation", "animation-delay", "animation-direction", "animation-duration", "animation-fill-mode", "animation-iteration-count", "animation-name", "animation-play-state", "animation-timing-function", "backface-visibility", "background", "background-attachment", "background-blend-mode", "background-clip", "background-color", "background-image", "background-origin", "background-position", "background-repeat", "background-size", "block-size", "border", "border-block", "border-block-color", "border-block-end", "border-block-end-color", "border-block-end-style", "border-block-end-width", "border-block-start", "border-block-start-color", "border-block-start-style", "border-block-start-width", "border-block-style", "border-block-width", "border-bottom", "border-bottom-color", "border-bottom-left-radius", "border-bottom-right-radius", "border-bottom-style", "border-bottom-width", "border-collapse", "border-color", "border-image", "border-image-outset", "border-image-repeat", "border-image-slice", "border-image-source", "border-image-width", "border-inline", "border-inline-color", "border-inline-end", "border-inline-end-color", "border-inline-end-style", "border-inline-end-width", "border-inline-start", "border-inline-start-color", "border-inline-start-style", "border-inline-start-width", "border-inline-style", "border-inline-width", "border-left", "border-left-color", "border-left-style", "border-left-width", "border-radius", "border-right", "border-right-color", "border-right-style", "border-right-width", "border-spacing", "border-style", "border-top", "border-top-color", "border-top-left-radius", "border-top-right-radius", "border-top-style", "border-top-width", "border-width", "bottom", "box-decoration-break", "box-shadow", "box-sizing", "break-after", "break-before", "break-inside", "caption-side", "caret-color", "clear", "clip", "clip-path", "clip-rule", "color", "column-count", "column-fill", "column-gap", "column-rule", "column-rule-color", "column-rule-style", "column-rule-width", "column-span", "column-width", "columns", "contain", "content", "content-visibility", "counter-increment", "counter-reset", "cue", "cue-after", "cue-before", "cursor", "direction", "display", "empty-cells", "filter", "flex", "flex-basis", "flex-direction", "flex-flow", "flex-grow", "flex-shrink", "flex-wrap", "float", "flow", "font", "font-display", "font-family", "font-feature-settings", "font-kerning", "font-language-override", "font-size", "font-size-adjust", "font-smoothing", "font-stretch", "font-style", "font-synthesis", "font-variant", "font-variant-caps", "font-variant-east-asian", "font-variant-ligatures", "font-variant-numeric", "font-variant-position", "font-variation-settings", "font-weight", "gap", "glyph-orientation-vertical", "grid", "grid-area", "grid-auto-columns", "grid-auto-flow", "grid-auto-rows", "grid-column", "grid-column-end", "grid-column-start", "grid-gap", "grid-row", "grid-row-end", "grid-row-start", "grid-template", "grid-template-areas", "grid-template-columns", "grid-template-rows", "hanging-punctuation", "height", "hyphens", "icon", "image-orientation", "image-rendering", "image-resolution", "ime-mode", "inline-size", "isolation", "justify-content", "left", "letter-spacing", "line-break", "line-height", "list-style", "list-style-image", "list-style-position", "list-style-type", "margin", "margin-block", "margin-block-end", "margin-block-start", "margin-bottom", "margin-inline", "margin-inline-end", "margin-inline-start", "margin-left", "margin-right", "margin-top", "marks", "mask", "mask-border", "mask-border-mode", "mask-border-outset", "mask-border-repeat", "mask-border-slice", "mask-border-source", "mask-border-width", "mask-clip", "mask-composite", "mask-image", "mask-mode", "mask-origin", "mask-position", "mask-repeat", "mask-size", "mask-type", "max-block-size", "max-height", "max-inline-size", "max-width", "min-block-size", "min-height", "min-inline-size", "min-width", "mix-blend-mode", "nav-down", "nav-index", "nav-left", "nav-right", "nav-up", "none", "normal", "object-fit", "object-position", "opacity", "order", "orphans", "outline", "outline-color", "outline-offset", "outline-style", "outline-width", "overflow", "overflow-wrap", "overflow-x", "overflow-y", "padding", "padding-block", "padding-block-end", "padding-block-start", "padding-bottom", "padding-inline", "padding-inline-end", "padding-inline-start", "padding-left", "padding-right", "padding-top", "page-break-after", "page-break-before", "page-break-inside", "pause", "pause-after", "pause-before", "perspective", "perspective-origin", "pointer-events", "position", "quotes", "resize", "rest", "rest-after", "rest-before", "right", "row-gap", "scroll-margin", "scroll-margin-block", "scroll-margin-block-end", "scroll-margin-block-start", "scroll-margin-bottom", "scroll-margin-inline", "scroll-margin-inline-end", "scroll-margin-inline-start", "scroll-margin-left", "scroll-margin-right", "scroll-margin-top", "scroll-padding", "scroll-padding-block", "scroll-padding-block-end", "scroll-padding-block-start", "scroll-padding-bottom", "scroll-padding-inline", "scroll-padding-inline-end", "scroll-padding-inline-start", "scroll-padding-left", "scroll-padding-right", "scroll-padding-top", "scroll-snap-align", "scroll-snap-stop", "scroll-snap-type", "scrollbar-color", "scrollbar-gutter", "scrollbar-width", "shape-image-threshold", "shape-margin", "shape-outside", "speak", "speak-as", "src", "tab-size", "table-layout", "text-align", "text-align-all", "text-align-last", "text-combine-upright", "text-decoration", "text-decoration-color", "text-decoration-line", "text-decoration-style", "text-emphasis", "text-emphasis-color", "text-emphasis-position", "text-emphasis-style", "text-indent", "text-justify", "text-orientation", "text-overflow", "text-rendering", "text-shadow", "text-transform", "text-underline-position", "top", "transform", "transform-box", "transform-origin", "transform-style", "transition", "transition-delay", "transition-duration", "transition-property", "transition-timing-function", "unicode-bidi", "vertical-align", "visibility", "voice-balance", "voice-duration", "voice-family", "voice-pitch", "voice-range", "voice-rate", "voice-stress", "voice-volume", "white-space", "widows", "width", "will-change", "word-break", "word-spacing", "word-wrap", "writing-mode", "z-index"].reverse(),
      n = r.concat(i);
    return function (a) {
      var l = function (e) {
          return {
            IMPORTANT: {
              scope: "meta",
              begin: "!important"
            },
            BLOCK_COMMENT: e.C_BLOCK_COMMENT_MODE,
            HEXCOLOR: {
              scope: "number",
              begin: /#(([0-9a-fA-F]{3,4})|(([0-9a-fA-F]{2}){3,4}))\b/
            },
            FUNCTION_DISPATCH: {
              className: "built_in",
              begin: /[\w-]+(?=\()/
            },
            ATTRIBUTE_SELECTOR_MODE: {
              scope: "selector-attr",
              begin: /\[/,
              end: /\]/,
              illegal: "$",
              contains: [e.APOS_STRING_MODE, e.QUOTE_STRING_MODE]
            },
            CSS_NUMBER_MODE: {
              scope: "number",
              begin: e.NUMBER_RE + "(%|em|ex|ch|rem|vw|vh|vmin|vmax|cm|mm|in|pt|pc|px|deg|grad|rad|turn|s|ms|Hz|kHz|dpi|dpcm|dppx)?",
              relevance: 0
            },
            CSS_VARIABLE: {
              className: "attr",
              begin: /--[A-Za-z][A-Za-z0-9_-]*/
            }
          };
        }(a),
        s = n,
        d = "([\\w-]+|@\\{[\\w-]+\\})",
        c = [],
        g = [],
        b = function b(e) {
          return {
            className: "string",
            begin: "~?" + e + ".*?" + e
          };
        },
        m = function m(e, t, r) {
          return {
            className: e,
            begin: t,
            relevance: r
          };
        },
        p = {
          $pattern: /[a-z-]+/,
          keyword: "and or not only",
          attribute: t.join(" ")
        },
        u = {
          begin: "\\(",
          end: "\\)",
          contains: g,
          keywords: p,
          relevance: 0
        };
      g.push(a.C_LINE_COMMENT_MODE, a.C_BLOCK_COMMENT_MODE, b("'"), b('"'), l.CSS_NUMBER_MODE, {
        begin: "(url|data-uri)\\(",
        starts: {
          className: "string",
          end: "[\\)\\n]",
          excludeEnd: !0
        }
      }, l.HEXCOLOR, u, m("variable", "@@?[\\w-]+", 10), m("variable", "@\\{[\\w-]+\\}"), m("built_in", "~?`[^`]*?`"), {
        className: "attribute",
        begin: "[\\w-]+\\s*:",
        end: ":",
        returnBegin: !0,
        excludeEnd: !0
      }, l.IMPORTANT, {
        beginKeywords: "and not"
      }, l.FUNCTION_DISPATCH);
      var h = g.concat({
          begin: /\{/,
          end: /\}/,
          contains: c
        }),
        f = {
          beginKeywords: "when",
          endsWithParent: !0,
          contains: [{
            beginKeywords: "and not"
          }].concat(g)
        },
        k = {
          begin: d + "\\s*:",
          returnBegin: !0,
          end: /[;}]/,
          relevance: 0,
          contains: [{
            begin: /-(webkit|moz|ms|o)-/
          }, l.CSS_VARIABLE, {
            className: "attribute",
            begin: "\\b(" + o.join("|") + ")\\b",
            end: /(?=:)/,
            starts: {
              endsWithParent: !0,
              illegal: "[<=$]",
              relevance: 0,
              contains: g
            }
          }]
        },
        w = {
          className: "keyword",
          begin: "@(import|media|charset|font-face|(-[a-z]+-)?keyframes|supports|document|namespace|page|viewport|host)\\b",
          starts: {
            end: "[;{}]",
            keywords: p,
            returnEnd: !0,
            contains: g,
            relevance: 0
          }
        },
        v = {
          className: "variable",
          variants: [{
            begin: "@[\\w-]+\\s*:",
            relevance: 15
          }, {
            begin: "@[\\w-]+"
          }],
          starts: {
            end: "[;}]",
            returnEnd: !0,
            contains: h
          }
        },
        y = {
          variants: [{
            begin: "[\\.#:&\\[>]",
            end: "[;{}]"
          }, {
            begin: d,
            end: /\{/
          }],
          returnBegin: !0,
          returnEnd: !0,
          illegal: "[<='$\"]",
          relevance: 0,
          contains: [a.C_LINE_COMMENT_MODE, a.C_BLOCK_COMMENT_MODE, f, m("keyword", "all\\b"), m("variable", "@\\{[\\w-]+\\}"), {
            begin: "\\b(" + e.join("|") + ")\\b",
            className: "selector-tag"
          }, l.CSS_NUMBER_MODE, m("selector-tag", d, 0), m("selector-id", "#" + d), m("selector-class", "\\." + d, 0), m("selector-tag", "&", 0), l.ATTRIBUTE_SELECTOR_MODE, {
            className: "selector-pseudo",
            begin: ":(" + r.join("|") + ")"
          }, {
            className: "selector-pseudo",
            begin: ":(:)?(" + i.join("|") + ")"
          }, {
            begin: /\(/,
            end: /\)/,
            relevance: 0,
            contains: h
          }, {
            begin: "!important"
          }, l.FUNCTION_DISPATCH]
        },
        x = {
          begin: "[\\w-]+:(:)?(".concat(s.join("|"), ")"),
          returnBegin: !0,
          contains: [y]
        };
      return c.push(a.C_LINE_COMMENT_MODE, a.C_BLOCK_COMMENT_MODE, w, v, x, k, y, f, l.FUNCTION_DISPATCH), {
        name: "Less",
        case_insensitive: !0,
        illegal: "[=>'/<($\"]",
        contains: c
      };
    };
  }();
  hljs.registerLanguage("less", e);
})(); /*! `graphql` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var a = e.regex;
      return {
        name: "GraphQL",
        aliases: ["gql"],
        case_insensitive: !0,
        disableAutodetect: !1,
        keywords: {
          keyword: ["query", "mutation", "subscription", "type", "input", "schema", "directive", "interface", "union", "scalar", "fragment", "enum", "on"],
          literal: ["true", "false", "null"]
        },
        contains: [e.HASH_COMMENT_MODE, e.QUOTE_STRING_MODE, e.NUMBER_MODE, {
          scope: "punctuation",
          match: /[.]{3}/,
          relevance: 0
        }, {
          scope: "punctuation",
          begin: /[\!\(\)\:\=\[\]\{\|\}]{1}/,
          relevance: 0
        }, {
          scope: "variable",
          begin: /\$/,
          end: /\W/,
          excludeEnd: !0,
          relevance: 0
        }, {
          scope: "meta",
          match: /@\w+/,
          excludeEnd: !0
        }, {
          scope: "symbol",
          begin: a.concat(/[_A-Za-z][_0-9A-Za-z]*/, a.lookahead(/\s*:/)),
          relevance: 0
        }],
        illegal: [/[;<']/, /BEGIN/]
      };
    };
  }();
  hljs.registerLanguage("graphql", e);
})(); /*! `perl` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = e.regex,
        t = /[dualxmsipngr]{0,12}/,
        r = {
          $pattern: /[\w.]+/,
          keyword: "abs accept alarm and atan2 bind binmode bless break caller chdir chmod chomp chop chown chr chroot close closedir connect continue cos crypt dbmclose dbmopen defined delete die do dump each else elsif endgrent endhostent endnetent endprotoent endpwent endservent eof eval exec exists exit exp fcntl fileno flock for foreach fork format formline getc getgrent getgrgid getgrnam gethostbyaddr gethostbyname gethostent getlogin getnetbyaddr getnetbyname getnetent getpeername getpgrp getpriority getprotobyname getprotobynumber getprotoent getpwent getpwnam getpwuid getservbyname getservbyport getservent getsockname getsockopt given glob gmtime goto grep gt hex if index int ioctl join keys kill last lc lcfirst length link listen local localtime log lstat lt ma map mkdir msgctl msgget msgrcv msgsnd my ne next no not oct open opendir or ord our pack package pipe pop pos print printf prototype push q|0 qq quotemeta qw qx rand read readdir readline readlink readpipe recv redo ref rename require reset return reverse rewinddir rindex rmdir say scalar seek seekdir select semctl semget semop send setgrent sethostent setnetent setpgrp setpriority setprotoent setpwent setservent setsockopt shift shmctl shmget shmread shmwrite shutdown sin sleep socket socketpair sort splice split sprintf sqrt srand stat state study sub substr symlink syscall sysopen sysread sysseek system syswrite tell telldir tie tied time times tr truncate uc ucfirst umask undef unless unlink unpack unshift untie until use utime values vec wait waitpid wantarray warn when while write x|0 xor y|0"
        },
        s = {
          className: "subst",
          begin: "[$@]\\{",
          end: "\\}",
          keywords: r
        },
        i = {
          begin: /->\{/,
          end: /\}/
        },
        a = {
          variants: [{
            begin: /\$\d/
          }, {
            begin: n.concat(/[$%@](\^\w\b|#\w+(::\w+)*|\{\w+\}|\w+(::\w*)*)/, "(?![A-Za-z])(?![@$%])")
          }, {
            begin: /[$%@][^\s\w{]/,
            relevance: 0
          }]
        },
        c = [e.BACKSLASH_ESCAPE, s, a],
        o = [/!/, /\//, /\|/, /\?/, /'/, /"/, /#/],
        g = function g(e, r) {
          var s = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "\\1";
          var i = "\\1" === s ? s : n.concat(s, r);
          return n.concat(n.concat("(?:", e, ")"), r, /(?:\\.|[^\\\/])*?/, i, /(?:\\.|[^\\\/])*?/, s, t);
        },
        l = function l(e, r, s) {
          return n.concat(n.concat("(?:", e, ")"), r, /(?:\\.|[^\\\/])*?/, s, t);
        },
        d = [a, e.HASH_COMMENT_MODE, e.COMMENT(/^=\w/, /=cut/, {
          endsWithParent: !0
        }), i, {
          className: "string",
          contains: c,
          variants: [{
            begin: "q[qwxr]?\\s*\\(",
            end: "\\)",
            relevance: 5
          }, {
            begin: "q[qwxr]?\\s*\\[",
            end: "\\]",
            relevance: 5
          }, {
            begin: "q[qwxr]?\\s*\\{",
            end: "\\}",
            relevance: 5
          }, {
            begin: "q[qwxr]?\\s*\\|",
            end: "\\|",
            relevance: 5
          }, {
            begin: "q[qwxr]?\\s*<",
            end: ">",
            relevance: 5
          }, {
            begin: "qw\\s+q",
            end: "q",
            relevance: 5
          }, {
            begin: "'",
            end: "'",
            contains: [e.BACKSLASH_ESCAPE]
          }, {
            begin: '"',
            end: '"'
          }, {
            begin: "`",
            end: "`",
            contains: [e.BACKSLASH_ESCAPE]
          }, {
            begin: /\{\w+\}/,
            relevance: 0
          }, {
            begin: "-?\\w+\\s*=>",
            relevance: 0
          }]
        }, {
          className: "number",
          begin: "(\\b0[0-7_]+)|(\\b0x[0-9a-fA-F_]+)|(\\b[1-9][0-9_]*(\\.[0-9_]+)?)|[0_]\\b",
          relevance: 0
        }, {
          begin: "(\\/\\/|" + e.RE_STARTERS_RE + "|\\b(split|return|print|reverse|grep)\\b)\\s*",
          keywords: "split return print reverse grep",
          relevance: 0,
          contains: [e.HASH_COMMENT_MODE, {
            className: "regexp",
            variants: [{
              begin: g("s|tr|y", n.either.apply(n, o.concat([{
                capture: !0
              }])))
            }, {
              begin: g("s|tr|y", "\\(", "\\)")
            }, {
              begin: g("s|tr|y", "\\[", "\\]")
            }, {
              begin: g("s|tr|y", "\\{", "\\}")
            }],
            relevance: 2
          }, {
            className: "regexp",
            variants: [{
              begin: /(m|qr)\/\//,
              relevance: 0
            }, {
              begin: l("(?:m|qr)?", /\//, /\//)
            }, {
              begin: l("m|qr", n.either.apply(n, o.concat([{
                capture: !0
              }])), /\1/)
            }, {
              begin: l("m|qr", /\(/, /\)/)
            }, {
              begin: l("m|qr", /\[/, /\]/)
            }, {
              begin: l("m|qr", /\{/, /\}/)
            }]
          }]
        }, {
          className: "function",
          beginKeywords: "sub",
          end: "(\\s*\\(.*?\\))?[;{]",
          excludeEnd: !0,
          relevance: 5,
          contains: [e.TITLE_MODE]
        }, {
          begin: "-\\w\\b",
          relevance: 0
        }, {
          begin: "^__DATA__$",
          end: "^__END__$",
          subLanguage: "mojolicious",
          contains: [{
            begin: "^@@.*",
            end: "$",
            className: "comment"
          }]
        }];
      return s.contains = d, i.contains = d, {
        name: "Perl",
        aliases: ["pl", "pm"],
        keywords: r,
        contains: d
      };
    };
  }();
  hljs.registerLanguage("perl", e);
})(); /*! `sql` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var r = e.regex,
        t = e.COMMENT("--", "$"),
        n = ["true", "false", "unknown"],
        a = ["bigint", "binary", "blob", "boolean", "char", "character", "clob", "date", "dec", "decfloat", "decimal", "float", "int", "integer", "interval", "nchar", "nclob", "national", "numeric", "real", "row", "smallint", "time", "timestamp", "varchar", "varying", "varbinary"],
        i = ["abs", "acos", "array_agg", "asin", "atan", "avg", "cast", "ceil", "ceiling", "coalesce", "corr", "cos", "cosh", "count", "covar_pop", "covar_samp", "cume_dist", "dense_rank", "deref", "element", "exp", "extract", "first_value", "floor", "json_array", "json_arrayagg", "json_exists", "json_object", "json_objectagg", "json_query", "json_table", "json_table_primitive", "json_value", "lag", "last_value", "lead", "listagg", "ln", "log", "log10", "lower", "max", "min", "mod", "nth_value", "ntile", "nullif", "percent_rank", "percentile_cont", "percentile_disc", "position", "position_regex", "power", "rank", "regr_avgx", "regr_avgy", "regr_count", "regr_intercept", "regr_r2", "regr_slope", "regr_sxx", "regr_sxy", "regr_syy", "row_number", "sin", "sinh", "sqrt", "stddev_pop", "stddev_samp", "substring", "substring_regex", "sum", "tan", "tanh", "translate", "translate_regex", "treat", "trim", "trim_array", "unnest", "upper", "value_of", "var_pop", "var_samp", "width_bucket"],
        s = ["create table", "insert into", "primary key", "foreign key", "not null", "alter table", "add constraint", "grouping sets", "on overflow", "character set", "respect nulls", "ignore nulls", "nulls first", "nulls last", "depth first", "breadth first"],
        o = i,
        c = ["abs", "acos", "all", "allocate", "alter", "and", "any", "are", "array", "array_agg", "array_max_cardinality", "as", "asensitive", "asin", "asymmetric", "at", "atan", "atomic", "authorization", "avg", "begin", "begin_frame", "begin_partition", "between", "bigint", "binary", "blob", "boolean", "both", "by", "call", "called", "cardinality", "cascaded", "case", "cast", "ceil", "ceiling", "char", "char_length", "character", "character_length", "check", "classifier", "clob", "close", "coalesce", "collate", "collect", "column", "commit", "condition", "connect", "constraint", "contains", "convert", "copy", "corr", "corresponding", "cos", "cosh", "count", "covar_pop", "covar_samp", "create", "cross", "cube", "cume_dist", "current", "current_catalog", "current_date", "current_default_transform_group", "current_path", "current_role", "current_row", "current_schema", "current_time", "current_timestamp", "current_path", "current_role", "current_transform_group_for_type", "current_user", "cursor", "cycle", "date", "day", "deallocate", "dec", "decimal", "decfloat", "declare", "default", "define", "delete", "dense_rank", "deref", "describe", "deterministic", "disconnect", "distinct", "double", "drop", "dynamic", "each", "element", "else", "empty", "end", "end_frame", "end_partition", "end-exec", "equals", "escape", "every", "except", "exec", "execute", "exists", "exp", "external", "extract", "false", "fetch", "filter", "first_value", "float", "floor", "for", "foreign", "frame_row", "free", "from", "full", "function", "fusion", "get", "global", "grant", "group", "grouping", "groups", "having", "hold", "hour", "identity", "in", "indicator", "initial", "inner", "inout", "insensitive", "insert", "int", "integer", "intersect", "intersection", "interval", "into", "is", "join", "json_array", "json_arrayagg", "json_exists", "json_object", "json_objectagg", "json_query", "json_table", "json_table_primitive", "json_value", "lag", "language", "large", "last_value", "lateral", "lead", "leading", "left", "like", "like_regex", "listagg", "ln", "local", "localtime", "localtimestamp", "log", "log10", "lower", "match", "match_number", "match_recognize", "matches", "max", "member", "merge", "method", "min", "minute", "mod", "modifies", "module", "month", "multiset", "national", "natural", "nchar", "nclob", "new", "no", "none", "normalize", "not", "nth_value", "ntile", "null", "nullif", "numeric", "octet_length", "occurrences_regex", "of", "offset", "old", "omit", "on", "one", "only", "open", "or", "order", "out", "outer", "over", "overlaps", "overlay", "parameter", "partition", "pattern", "per", "percent", "percent_rank", "percentile_cont", "percentile_disc", "period", "portion", "position", "position_regex", "power", "precedes", "precision", "prepare", "primary", "procedure", "ptf", "range", "rank", "reads", "real", "recursive", "ref", "references", "referencing", "regr_avgx", "regr_avgy", "regr_count", "regr_intercept", "regr_r2", "regr_slope", "regr_sxx", "regr_sxy", "regr_syy", "release", "result", "return", "returns", "revoke", "right", "rollback", "rollup", "row", "row_number", "rows", "running", "savepoint", "scope", "scroll", "search", "second", "seek", "select", "sensitive", "session_user", "set", "show", "similar", "sin", "sinh", "skip", "smallint", "some", "specific", "specifictype", "sql", "sqlexception", "sqlstate", "sqlwarning", "sqrt", "start", "static", "stddev_pop", "stddev_samp", "submultiset", "subset", "substring", "substring_regex", "succeeds", "sum", "symmetric", "system", "system_time", "system_user", "table", "tablesample", "tan", "tanh", "then", "time", "timestamp", "timezone_hour", "timezone_minute", "to", "trailing", "translate", "translate_regex", "translation", "treat", "trigger", "trim", "trim_array", "true", "truncate", "uescape", "union", "unique", "unknown", "unnest", "update", "upper", "user", "using", "value", "values", "value_of", "var_pop", "var_samp", "varbinary", "varchar", "varying", "versioning", "when", "whenever", "where", "width_bucket", "window", "with", "within", "without", "year", "add", "asc", "collation", "desc", "final", "first", "last", "view"].filter(function (e) {
          return !i.includes(e);
        }),
        l = {
          begin: r.concat(/\b/, r.either.apply(r, o), /\s*\(/),
          relevance: 0,
          keywords: {
            built_in: o
          }
        };
      return {
        name: "SQL",
        case_insensitive: !0,
        illegal: /[{}]|<\//,
        keywords: {
          $pattern: /\b[\w\.]+/,
          keyword: function (e) {
            var _ref9 = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {},
              r = _ref9.exceptions,
              t = _ref9.when;
            var n = t;
            return r = r || [], e.map(function (e) {
              return e.match(/\|\d+$/) || r.includes(e) ? e : n(e) ? e + "|0" : e;
            });
          }(c, {
            when: function when(e) {
              return e.length < 3;
            }
          }),
          literal: n,
          type: a,
          built_in: ["current_catalog", "current_date", "current_default_transform_group", "current_path", "current_role", "current_schema", "current_transform_group_for_type", "current_user", "session_user", "system_time", "system_user", "current_time", "localtime", "current_timestamp", "localtimestamp"]
        },
        contains: [{
          begin: r.either.apply(r, s),
          relevance: 0,
          keywords: {
            $pattern: /[\w\.]+/,
            keyword: c.concat(s),
            literal: n,
            type: a
          }
        }, {
          className: "type",
          begin: r.either("double precision", "large object", "with timezone", "without timezone")
        }, l, {
          className: "variable",
          begin: /@[a-z0-9]+/
        }, {
          className: "string",
          variants: [{
            begin: /'/,
            end: /'/,
            contains: [{
              begin: /''/
            }]
          }]
        }, {
          begin: /"/,
          end: /"/,
          contains: [{
            begin: /""/
          }]
        }, e.C_NUMBER_MODE, e.C_BLOCK_COMMENT_MODE, t, {
          className: "operator",
          begin: /[-+*/=%^~]|&&?|\|\|?|!=?|<(?:=>?|<|>)?|>[>=]?/,
          relevance: 0
        }]
      };
    };
  }();
  hljs.registerLanguage("sql", e);
})(); /*! `makefile` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var i = {
          className: "variable",
          variants: [{
            begin: "\\$\\(" + e.UNDERSCORE_IDENT_RE + "\\)",
            contains: [e.BACKSLASH_ESCAPE]
          }, {
            begin: /\$[@%<?\^\+\*]/
          }]
        },
        a = {
          className: "string",
          begin: /"/,
          end: /"/,
          contains: [e.BACKSLASH_ESCAPE, i]
        },
        n = {
          className: "variable",
          begin: /\$\([\w-]+\s/,
          end: /\)/,
          keywords: {
            built_in: "subst patsubst strip findstring filter filter-out sort word wordlist firstword lastword dir notdir suffix basename addsuffix addprefix join wildcard realpath abspath error warning shell origin flavor foreach if or and call eval file value"
          },
          contains: [i]
        },
        s = {
          begin: "^" + e.UNDERSCORE_IDENT_RE + "\\s*(?=[:+?]?=)"
        },
        r = {
          className: "section",
          begin: /^[^\s]+:/,
          end: /$/,
          contains: [i]
        };
      return {
        name: "Makefile",
        aliases: ["mk", "mak", "make"],
        keywords: {
          $pattern: /[\w-]+/,
          keyword: "define endef undefine ifdef ifndef ifeq ifneq else endif include -include sinclude override export unexport private vpath"
        },
        contains: [e.HASH_COMMENT_MODE, i, a, n, s, {
          className: "meta",
          begin: /^\.PHONY:/,
          end: /$/,
          keywords: {
            $pattern: /[\.\w]+/,
            keyword: ".PHONY"
          }
        }, r]
      };
    };
  }();
  hljs.registerLanguage("makefile", e);
})(); /*! `javascript` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    var e = "[A-Za-z$_][0-9A-Za-z$_]*",
      n = ["as", "in", "of", "if", "for", "while", "finally", "var", "new", "function", "do", "return", "void", "else", "break", "catch", "instanceof", "with", "throw", "case", "default", "try", "switch", "continue", "typeof", "delete", "let", "yield", "const", "class", "debugger", "async", "await", "static", "import", "from", "export", "extends"],
      a = ["true", "false", "null", "undefined", "NaN", "Infinity"],
      t = ["Object", "Function", "Boolean", "Symbol", "Math", "Date", "Number", "BigInt", "String", "RegExp", "Array", "Float32Array", "Float64Array", "Int8Array", "Uint8Array", "Uint8ClampedArray", "Int16Array", "Int32Array", "Uint16Array", "Uint32Array", "BigInt64Array", "BigUint64Array", "Set", "Map", "WeakSet", "WeakMap", "ArrayBuffer", "SharedArrayBuffer", "Atomics", "DataView", "JSON", "Promise", "Generator", "GeneratorFunction", "AsyncFunction", "Reflect", "Proxy", "Intl", "WebAssembly"],
      s = ["Error", "EvalError", "InternalError", "RangeError", "ReferenceError", "SyntaxError", "TypeError", "URIError"],
      r = ["setInterval", "setTimeout", "clearInterval", "clearTimeout", "require", "exports", "eval", "isFinite", "isNaN", "parseFloat", "parseInt", "decodeURI", "decodeURIComponent", "encodeURI", "encodeURIComponent", "escape", "unescape"],
      c = ["arguments", "this", "super", "console", "window", "document", "localStorage", "module", "global"],
      i = [].concat(r, t, s);
    return function (o) {
      var l = o.regex,
        b = e,
        d = {
          begin: /<[A-Za-z0-9\\._:-]+/,
          end: /\/[A-Za-z0-9\\._:-]+>|\/>/,
          isTrulyOpeningTag: function isTrulyOpeningTag(e, n) {
            var a = e[0].length + e.index,
              t = e.input[a];
            if ("<" === t || "," === t) return void n.ignoreMatch();
            var s;
            ">" === t && (function (e, _ref10) {
              var n = _ref10.after;
              var a = "</" + e[0].slice(1);
              return -1 !== e.input.indexOf(a, n);
            }(e, {
              after: a
            }) || n.ignoreMatch());
            var r = e.input.substring(a);
            ((s = r.match(/^\s*=/)) || (s = r.match(/^\s+extends\s+/)) && 0 === s.index) && n.ignoreMatch();
          }
        },
        g = {
          $pattern: e,
          keyword: n,
          literal: a,
          built_in: i,
          "variable.language": c
        },
        u = "\\.([0-9](_?[0-9])*)",
        m = "0|[1-9](_?[0-9])*|0[0-7]*[89][0-9]*",
        E = {
          className: "number",
          variants: [{
            begin: "(\\b(".concat(m, ")((").concat(u, ")|\\.)?|(").concat(u, "))[eE][+-]?([0-9](_?[0-9])*)\\b")
          }, {
            begin: "\\b(".concat(m, ")\\b((").concat(u, ")\\b|\\.)?|(").concat(u, ")\\b")
          }, {
            begin: "\\b(0|[1-9](_?[0-9])*)n\\b"
          }, {
            begin: "\\b0[xX][0-9a-fA-F](_?[0-9a-fA-F])*n?\\b"
          }, {
            begin: "\\b0[bB][0-1](_?[0-1])*n?\\b"
          }, {
            begin: "\\b0[oO][0-7](_?[0-7])*n?\\b"
          }, {
            begin: "\\b0[0-7]+n?\\b"
          }],
          relevance: 0
        },
        A = {
          className: "subst",
          begin: "\\$\\{",
          end: "\\}",
          keywords: g,
          contains: []
        },
        y = {
          begin: "html`",
          end: "",
          starts: {
            end: "`",
            returnEnd: !1,
            contains: [o.BACKSLASH_ESCAPE, A],
            subLanguage: "xml"
          }
        },
        N = {
          begin: "css`",
          end: "",
          starts: {
            end: "`",
            returnEnd: !1,
            contains: [o.BACKSLASH_ESCAPE, A],
            subLanguage: "css"
          }
        },
        _ = {
          className: "string",
          begin: "`",
          end: "`",
          contains: [o.BACKSLASH_ESCAPE, A]
        },
        h = {
          className: "comment",
          variants: [o.COMMENT(/\/\*\*(?!\/)/, "\\*/", {
            relevance: 0,
            contains: [{
              begin: "(?=@[A-Za-z]+)",
              relevance: 0,
              contains: [{
                className: "doctag",
                begin: "@[A-Za-z]+"
              }, {
                className: "type",
                begin: "\\{",
                end: "\\}",
                excludeEnd: !0,
                excludeBegin: !0,
                relevance: 0
              }, {
                className: "variable",
                begin: b + "(?=\\s*(-)|$)",
                endsParent: !0,
                relevance: 0
              }, {
                begin: /(?=[^\n])\s/,
                relevance: 0
              }]
            }]
          }), o.C_BLOCK_COMMENT_MODE, o.C_LINE_COMMENT_MODE]
        },
        f = [o.APOS_STRING_MODE, o.QUOTE_STRING_MODE, y, N, _, {
          match: /\$\d+/
        }, E];
      A.contains = f.concat({
        begin: /\{/,
        end: /\}/,
        keywords: g,
        contains: ["self"].concat(f)
      });
      var v = [].concat(h, A.contains),
        p = v.concat([{
          begin: /\(/,
          end: /\)/,
          keywords: g,
          contains: ["self"].concat(v)
        }]),
        S = {
          className: "params",
          begin: /\(/,
          end: /\)/,
          excludeBegin: !0,
          excludeEnd: !0,
          keywords: g,
          contains: p
        },
        w = {
          variants: [{
            match: [/class/, /\s+/, b, /\s+/, /extends/, /\s+/, l.concat(b, "(", l.concat(/\./, b), ")*")],
            scope: {
              1: "keyword",
              3: "title.class",
              5: "keyword",
              7: "title.class.inherited"
            }
          }, {
            match: [/class/, /\s+/, b],
            scope: {
              1: "keyword",
              3: "title.class"
            }
          }]
        },
        R = {
          relevance: 0,
          match: l.either(/\bJSON/, /\b[A-Z][a-z]+([A-Z][a-z]*|\d)*/, /\b[A-Z]{2,}([A-Z][a-z]+|\d)+([A-Z][a-z]*)*/, /\b[A-Z]{2,}[a-z]+([A-Z][a-z]+|\d)*([A-Z][a-z]*)*/),
          className: "title.class",
          keywords: {
            _: [].concat(t, s)
          }
        },
        O = {
          variants: [{
            match: [/function/, /\s+/, b, /(?=\s*\()/]
          }, {
            match: [/function/, /\s*(?=\()/]
          }],
          className: {
            1: "keyword",
            3: "title.function"
          },
          label: "func.def",
          contains: [S],
          illegal: /%/
        },
        k = {
          match: l.concat(/\b/, (I = [].concat(r, ["super", "import"]), l.concat("(?!", I.join("|"), ")")), b, l.lookahead(/\(/)),
          className: "title.function",
          relevance: 0
        };
      var I;
      var x = {
          begin: l.concat(/\./, l.lookahead(l.concat(b, /(?![0-9A-Za-z$_(])/))),
          end: b,
          excludeBegin: !0,
          keywords: "prototype",
          className: "property",
          relevance: 0
        },
        T = {
          match: [/get|set/, /\s+/, b, /(?=\()/],
          className: {
            1: "keyword",
            3: "title.function"
          },
          contains: [{
            begin: /\(\)/
          }, S]
        },
        C = "(\\([^()]*(\\([^()]*(\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)|" + o.UNDERSCORE_IDENT_RE + ")\\s*=>",
        M = {
          match: [/const|var|let/, /\s+/, b, /\s*/, /=\s*/, /(async\s*)?/, l.lookahead(C)],
          keywords: "async",
          className: {
            1: "keyword",
            3: "title.function"
          },
          contains: [S]
        };
      return {
        name: "Javascript",
        aliases: ["js", "jsx", "mjs", "cjs"],
        keywords: g,
        exports: {
          PARAMS_CONTAINS: p,
          CLASS_REFERENCE: R
        },
        illegal: /#(?![$_A-z])/,
        contains: [o.SHEBANG({
          label: "shebang",
          binary: "node",
          relevance: 5
        }), {
          label: "use_strict",
          className: "meta",
          relevance: 10,
          begin: /^\s*['"]use (strict|asm)['"]/
        }, o.APOS_STRING_MODE, o.QUOTE_STRING_MODE, y, N, _, h, {
          match: /\$\d+/
        }, E, R, {
          className: "attr",
          begin: b + l.lookahead(":"),
          relevance: 0
        }, M, {
          begin: "(" + o.RE_STARTERS_RE + "|\\b(case|return|throw)\\b)\\s*",
          keywords: "return throw case",
          relevance: 0,
          contains: [h, o.REGEXP_MODE, {
            className: "function",
            begin: C,
            returnBegin: !0,
            end: "\\s*=>",
            contains: [{
              className: "params",
              variants: [{
                begin: o.UNDERSCORE_IDENT_RE,
                relevance: 0
              }, {
                className: null,
                begin: /\(\s*\)/,
                skip: !0
              }, {
                begin: /\(/,
                end: /\)/,
                excludeBegin: !0,
                excludeEnd: !0,
                keywords: g,
                contains: p
              }]
            }]
          }, {
            begin: /,/,
            relevance: 0
          }, {
            match: /\s+/,
            relevance: 0
          }, {
            variants: [{
              begin: "<>",
              end: "</>"
            }, {
              match: /<[A-Za-z0-9\\._:-]+\s*\/>/
            }, {
              begin: d.begin,
              "on:begin": d.isTrulyOpeningTag,
              end: d.end
            }],
            subLanguage: "xml",
            contains: [{
              begin: d.begin,
              end: d.end,
              skip: !0,
              contains: ["self"]
            }]
          }]
        }, O, {
          beginKeywords: "while if switch catch for"
        }, {
          begin: "\\b(?!function)" + o.UNDERSCORE_IDENT_RE + "\\([^()]*(\\([^()]*(\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)\\s*\\{",
          returnBegin: !0,
          label: "func.def",
          contains: [S, o.inherit(o.TITLE_MODE, {
            begin: b,
            className: "title.function"
          })]
        }, {
          match: /\.\.\./,
          relevance: 0
        }, x, {
          match: "\\$" + b,
          relevance: 0
        }, {
          match: [/\bconstructor(?=\s*\()/],
          className: {
            1: "title.function"
          },
          contains: [S]
        }, k, {
          relevance: 0,
          match: /\b[A-Z][A-Z_0-9]+\b/,
          className: "variable.constant"
        }, w, T, {
          match: /\$[(.]/
        }]
      };
    };
  }();
  hljs.registerLanguage("javascript", e);
})(); /*! `plaintext` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var t = function () {
    "use strict";

    return function (t) {
      return {
        name: "Plain text",
        aliases: ["text", "txt"],
        disableAutodetect: !0
      };
    };
  }();
  hljs.registerLanguage("plaintext", t);
})(); /*! `r` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var a = e.regex,
        n = /(?:(?:[a-zA-Z]|\.[._a-zA-Z])[._a-zA-Z0-9]*)|\.(?!\d)/,
        i = a.either(/0[xX][0-9a-fA-F]+\.[0-9a-fA-F]*[pP][+-]?\d+i?/, /0[xX][0-9a-fA-F]+(?:[pP][+-]?\d+)?[Li]?/, /(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?[Li]?/),
        s = /[=!<>:]=|\|\||&&|:::?|<-|<<-|->>|->|\|>|[-+*\/?!$&|:<=>@^~]|\*\*/,
        t = a.either(/[()]/, /[{}]/, /\[\[/, /[[\]]/, /\\/, /,/);
      return {
        name: "R",
        keywords: {
          $pattern: n,
          keyword: "function if in break next repeat else for while",
          literal: "NULL NA TRUE FALSE Inf NaN NA_integer_|10 NA_real_|10 NA_character_|10 NA_complex_|10",
          built_in: "LETTERS letters month.abb month.name pi T F abs acos acosh all any anyNA Arg as.call as.character as.complex as.double as.environment as.integer as.logical as.null.default as.numeric as.raw asin asinh atan atanh attr attributes baseenv browser c call ceiling class Conj cos cosh cospi cummax cummin cumprod cumsum digamma dim dimnames emptyenv exp expression floor forceAndCall gamma gc.time globalenv Im interactive invisible is.array is.atomic is.call is.character is.complex is.double is.environment is.expression is.finite is.function is.infinite is.integer is.language is.list is.logical is.matrix is.na is.name is.nan is.null is.numeric is.object is.pairlist is.raw is.recursive is.single is.symbol lazyLoadDBfetch length lgamma list log max min missing Mod names nargs nzchar oldClass on.exit pos.to.env proc.time prod quote range Re rep retracemem return round seq_along seq_len seq.int sign signif sin sinh sinpi sqrt standardGeneric substitute sum switch tan tanh tanpi tracemem trigamma trunc unclass untracemem UseMethod xtfrm"
        },
        contains: [e.COMMENT(/#'/, /$/, {
          contains: [{
            scope: "doctag",
            match: /@examples/,
            starts: {
              end: a.lookahead(a.either(/\n^#'\s*(?=@[a-zA-Z]+)/, /\n^(?!#')/)),
              endsParent: !0
            }
          }, {
            scope: "doctag",
            begin: "@param",
            end: /$/,
            contains: [{
              scope: "variable",
              variants: [{
                match: n
              }, {
                match: /`(?:\\.|[^`\\])+`/
              }],
              endsParent: !0
            }]
          }, {
            scope: "doctag",
            match: /@[a-zA-Z]+/
          }, {
            scope: "keyword",
            match: /\\[a-zA-Z]+/
          }]
        }), e.HASH_COMMENT_MODE, {
          scope: "string",
          contains: [e.BACKSLASH_ESCAPE],
          variants: [e.END_SAME_AS_BEGIN({
            begin: /[rR]"(-*)\(/,
            end: /\)(-*)"/
          }), e.END_SAME_AS_BEGIN({
            begin: /[rR]"(-*)\{/,
            end: /\}(-*)"/
          }), e.END_SAME_AS_BEGIN({
            begin: /[rR]"(-*)\[/,
            end: /\](-*)"/
          }), e.END_SAME_AS_BEGIN({
            begin: /[rR]'(-*)\(/,
            end: /\)(-*)'/
          }), e.END_SAME_AS_BEGIN({
            begin: /[rR]'(-*)\{/,
            end: /\}(-*)'/
          }), e.END_SAME_AS_BEGIN({
            begin: /[rR]'(-*)\[/,
            end: /\](-*)'/
          }), {
            begin: '"',
            end: '"',
            relevance: 0
          }, {
            begin: "'",
            end: "'",
            relevance: 0
          }]
        }, {
          relevance: 0,
          variants: [{
            scope: {
              1: "operator",
              2: "number"
            },
            match: [s, i]
          }, {
            scope: {
              1: "operator",
              2: "number"
            },
            match: [/%[^%]*%/, i]
          }, {
            scope: {
              1: "punctuation",
              2: "number"
            },
            match: [t, i]
          }, {
            scope: {
              2: "number"
            },
            match: [/[^a-zA-Z0-9._]|^/, i]
          }]
        }, {
          scope: {
            3: "operator"
          },
          match: [n, /\s+/, /<-/, /\s+/]
        }, {
          scope: "operator",
          relevance: 0,
          variants: [{
            match: s
          }, {
            match: /%[^%]*%/
          }]
        }, {
          scope: "punctuation",
          relevance: 0,
          match: t
        }, {
          begin: "`",
          end: "`",
          contains: [{
            begin: /\\./
          }]
        }]
      };
    };
  }();
  hljs.registerLanguage("r", e);
})(); /*! `scss` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    var e = ["a", "abbr", "address", "article", "aside", "audio", "b", "blockquote", "body", "button", "canvas", "caption", "cite", "code", "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "mark", "menu", "nav", "object", "ol", "p", "q", "quote", "samp", "section", "span", "strong", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "tr", "ul", "var", "video"],
      r = ["any-hover", "any-pointer", "aspect-ratio", "color", "color-gamut", "color-index", "device-aspect-ratio", "device-height", "device-width", "display-mode", "forced-colors", "grid", "height", "hover", "inverted-colors", "monochrome", "orientation", "overflow-block", "overflow-inline", "pointer", "prefers-color-scheme", "prefers-contrast", "prefers-reduced-motion", "prefers-reduced-transparency", "resolution", "scan", "scripting", "update", "width", "min-width", "max-width", "min-height", "max-height"],
      i = ["active", "any-link", "blank", "checked", "current", "default", "defined", "dir", "disabled", "drop", "empty", "enabled", "first", "first-child", "first-of-type", "fullscreen", "future", "focus", "focus-visible", "focus-within", "has", "host", "host-context", "hover", "indeterminate", "in-range", "invalid", "is", "lang", "last-child", "last-of-type", "left", "link", "local-link", "not", "nth-child", "nth-col", "nth-last-child", "nth-last-col", "nth-last-of-type", "nth-of-type", "only-child", "only-of-type", "optional", "out-of-range", "past", "placeholder-shown", "read-only", "read-write", "required", "right", "root", "scope", "target", "target-within", "user-invalid", "valid", "visited", "where"],
      t = ["after", "backdrop", "before", "cue", "cue-region", "first-letter", "first-line", "grammar-error", "marker", "part", "placeholder", "selection", "slotted", "spelling-error"],
      o = ["align-content", "align-items", "align-self", "all", "animation", "animation-delay", "animation-direction", "animation-duration", "animation-fill-mode", "animation-iteration-count", "animation-name", "animation-play-state", "animation-timing-function", "backface-visibility", "background", "background-attachment", "background-blend-mode", "background-clip", "background-color", "background-image", "background-origin", "background-position", "background-repeat", "background-size", "block-size", "border", "border-block", "border-block-color", "border-block-end", "border-block-end-color", "border-block-end-style", "border-block-end-width", "border-block-start", "border-block-start-color", "border-block-start-style", "border-block-start-width", "border-block-style", "border-block-width", "border-bottom", "border-bottom-color", "border-bottom-left-radius", "border-bottom-right-radius", "border-bottom-style", "border-bottom-width", "border-collapse", "border-color", "border-image", "border-image-outset", "border-image-repeat", "border-image-slice", "border-image-source", "border-image-width", "border-inline", "border-inline-color", "border-inline-end", "border-inline-end-color", "border-inline-end-style", "border-inline-end-width", "border-inline-start", "border-inline-start-color", "border-inline-start-style", "border-inline-start-width", "border-inline-style", "border-inline-width", "border-left", "border-left-color", "border-left-style", "border-left-width", "border-radius", "border-right", "border-right-color", "border-right-style", "border-right-width", "border-spacing", "border-style", "border-top", "border-top-color", "border-top-left-radius", "border-top-right-radius", "border-top-style", "border-top-width", "border-width", "bottom", "box-decoration-break", "box-shadow", "box-sizing", "break-after", "break-before", "break-inside", "caption-side", "caret-color", "clear", "clip", "clip-path", "clip-rule", "color", "column-count", "column-fill", "column-gap", "column-rule", "column-rule-color", "column-rule-style", "column-rule-width", "column-span", "column-width", "columns", "contain", "content", "content-visibility", "counter-increment", "counter-reset", "cue", "cue-after", "cue-before", "cursor", "direction", "display", "empty-cells", "filter", "flex", "flex-basis", "flex-direction", "flex-flow", "flex-grow", "flex-shrink", "flex-wrap", "float", "flow", "font", "font-display", "font-family", "font-feature-settings", "font-kerning", "font-language-override", "font-size", "font-size-adjust", "font-smoothing", "font-stretch", "font-style", "font-synthesis", "font-variant", "font-variant-caps", "font-variant-east-asian", "font-variant-ligatures", "font-variant-numeric", "font-variant-position", "font-variation-settings", "font-weight", "gap", "glyph-orientation-vertical", "grid", "grid-area", "grid-auto-columns", "grid-auto-flow", "grid-auto-rows", "grid-column", "grid-column-end", "grid-column-start", "grid-gap", "grid-row", "grid-row-end", "grid-row-start", "grid-template", "grid-template-areas", "grid-template-columns", "grid-template-rows", "hanging-punctuation", "height", "hyphens", "icon", "image-orientation", "image-rendering", "image-resolution", "ime-mode", "inline-size", "isolation", "justify-content", "left", "letter-spacing", "line-break", "line-height", "list-style", "list-style-image", "list-style-position", "list-style-type", "margin", "margin-block", "margin-block-end", "margin-block-start", "margin-bottom", "margin-inline", "margin-inline-end", "margin-inline-start", "margin-left", "margin-right", "margin-top", "marks", "mask", "mask-border", "mask-border-mode", "mask-border-outset", "mask-border-repeat", "mask-border-slice", "mask-border-source", "mask-border-width", "mask-clip", "mask-composite", "mask-image", "mask-mode", "mask-origin", "mask-position", "mask-repeat", "mask-size", "mask-type", "max-block-size", "max-height", "max-inline-size", "max-width", "min-block-size", "min-height", "min-inline-size", "min-width", "mix-blend-mode", "nav-down", "nav-index", "nav-left", "nav-right", "nav-up", "none", "normal", "object-fit", "object-position", "opacity", "order", "orphans", "outline", "outline-color", "outline-offset", "outline-style", "outline-width", "overflow", "overflow-wrap", "overflow-x", "overflow-y", "padding", "padding-block", "padding-block-end", "padding-block-start", "padding-bottom", "padding-inline", "padding-inline-end", "padding-inline-start", "padding-left", "padding-right", "padding-top", "page-break-after", "page-break-before", "page-break-inside", "pause", "pause-after", "pause-before", "perspective", "perspective-origin", "pointer-events", "position", "quotes", "resize", "rest", "rest-after", "rest-before", "right", "row-gap", "scroll-margin", "scroll-margin-block", "scroll-margin-block-end", "scroll-margin-block-start", "scroll-margin-bottom", "scroll-margin-inline", "scroll-margin-inline-end", "scroll-margin-inline-start", "scroll-margin-left", "scroll-margin-right", "scroll-margin-top", "scroll-padding", "scroll-padding-block", "scroll-padding-block-end", "scroll-padding-block-start", "scroll-padding-bottom", "scroll-padding-inline", "scroll-padding-inline-end", "scroll-padding-inline-start", "scroll-padding-left", "scroll-padding-right", "scroll-padding-top", "scroll-snap-align", "scroll-snap-stop", "scroll-snap-type", "scrollbar-color", "scrollbar-gutter", "scrollbar-width", "shape-image-threshold", "shape-margin", "shape-outside", "speak", "speak-as", "src", "tab-size", "table-layout", "text-align", "text-align-all", "text-align-last", "text-combine-upright", "text-decoration", "text-decoration-color", "text-decoration-line", "text-decoration-style", "text-emphasis", "text-emphasis-color", "text-emphasis-position", "text-emphasis-style", "text-indent", "text-justify", "text-orientation", "text-overflow", "text-rendering", "text-shadow", "text-transform", "text-underline-position", "top", "transform", "transform-box", "transform-origin", "transform-style", "transition", "transition-delay", "transition-duration", "transition-property", "transition-timing-function", "unicode-bidi", "vertical-align", "visibility", "voice-balance", "voice-duration", "voice-family", "voice-pitch", "voice-range", "voice-rate", "voice-stress", "voice-volume", "white-space", "widows", "width", "will-change", "word-break", "word-spacing", "word-wrap", "writing-mode", "z-index"].reverse();
    return function (n) {
      var a = function (e) {
          return {
            IMPORTANT: {
              scope: "meta",
              begin: "!important"
            },
            BLOCK_COMMENT: e.C_BLOCK_COMMENT_MODE,
            HEXCOLOR: {
              scope: "number",
              begin: /#(([0-9a-fA-F]{3,4})|(([0-9a-fA-F]{2}){3,4}))\b/
            },
            FUNCTION_DISPATCH: {
              className: "built_in",
              begin: /[\w-]+(?=\()/
            },
            ATTRIBUTE_SELECTOR_MODE: {
              scope: "selector-attr",
              begin: /\[/,
              end: /\]/,
              illegal: "$",
              contains: [e.APOS_STRING_MODE, e.QUOTE_STRING_MODE]
            },
            CSS_NUMBER_MODE: {
              scope: "number",
              begin: e.NUMBER_RE + "(%|em|ex|ch|rem|vw|vh|vmin|vmax|cm|mm|in|pt|pc|px|deg|grad|rad|turn|s|ms|Hz|kHz|dpi|dpcm|dppx)?",
              relevance: 0
            },
            CSS_VARIABLE: {
              className: "attr",
              begin: /--[A-Za-z][A-Za-z0-9_-]*/
            }
          };
        }(n),
        l = t,
        s = i,
        d = "@[a-z-]+",
        c = {
          className: "variable",
          begin: "(\\$[a-zA-Z-][a-zA-Z0-9_-]*)\\b",
          relevance: 0
        };
      return {
        name: "SCSS",
        case_insensitive: !0,
        illegal: "[=/|']",
        contains: [n.C_LINE_COMMENT_MODE, n.C_BLOCK_COMMENT_MODE, a.CSS_NUMBER_MODE, {
          className: "selector-id",
          begin: "#[A-Za-z0-9_-]+",
          relevance: 0
        }, {
          className: "selector-class",
          begin: "\\.[A-Za-z0-9_-]+",
          relevance: 0
        }, a.ATTRIBUTE_SELECTOR_MODE, {
          className: "selector-tag",
          begin: "\\b(" + e.join("|") + ")\\b",
          relevance: 0
        }, {
          className: "selector-pseudo",
          begin: ":(" + s.join("|") + ")"
        }, {
          className: "selector-pseudo",
          begin: ":(:)?(" + l.join("|") + ")"
        }, c, {
          begin: /\(/,
          end: /\)/,
          contains: [a.CSS_NUMBER_MODE]
        }, a.CSS_VARIABLE, {
          className: "attribute",
          begin: "\\b(" + o.join("|") + ")\\b"
        }, {
          begin: "\\b(whitespace|wait|w-resize|visible|vertical-text|vertical-ideographic|uppercase|upper-roman|upper-alpha|underline|transparent|top|thin|thick|text|text-top|text-bottom|tb-rl|table-header-group|table-footer-group|sw-resize|super|strict|static|square|solid|small-caps|separate|se-resize|scroll|s-resize|rtl|row-resize|ridge|right|repeat|repeat-y|repeat-x|relative|progress|pointer|overline|outside|outset|oblique|nowrap|not-allowed|normal|none|nw-resize|no-repeat|no-drop|newspaper|ne-resize|n-resize|move|middle|medium|ltr|lr-tb|lowercase|lower-roman|lower-alpha|loose|list-item|line|line-through|line-edge|lighter|left|keep-all|justify|italic|inter-word|inter-ideograph|inside|inset|inline|inline-block|inherit|inactive|ideograph-space|ideograph-parenthesis|ideograph-numeric|ideograph-alpha|horizontal|hidden|help|hand|groove|fixed|ellipsis|e-resize|double|dotted|distribute|distribute-space|distribute-letter|distribute-all-lines|disc|disabled|default|decimal|dashed|crosshair|collapse|col-resize|circle|char|center|capitalize|break-word|break-all|bottom|both|bolder|bold|block|bidi-override|below|baseline|auto|always|all-scroll|absolute|table|table-cell)\\b"
        }, {
          begin: /:/,
          end: /[;}{]/,
          relevance: 0,
          contains: [a.BLOCK_COMMENT, c, a.HEXCOLOR, a.CSS_NUMBER_MODE, n.QUOTE_STRING_MODE, n.APOS_STRING_MODE, a.IMPORTANT, a.FUNCTION_DISPATCH]
        }, {
          begin: "@(page|font-face)",
          keywords: {
            $pattern: d,
            keyword: "@page @font-face"
          }
        }, {
          begin: "@",
          end: "[{;]",
          returnBegin: !0,
          keywords: {
            $pattern: /[a-z-]+/,
            keyword: "and or not only",
            attribute: r.join(" ")
          },
          contains: [{
            begin: d,
            className: "keyword"
          }, {
            begin: /[a-z-]+(?=:)/,
            className: "attribute"
          }, c, n.QUOTE_STRING_MODE, n.APOS_STRING_MODE, a.HEXCOLOR, a.CSS_NUMBER_MODE]
        }, a.FUNCTION_DISPATCH]
      };
    };
  }();
  hljs.registerLanguage("scss", e);
})(); /*! `bash` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var s = e.regex,
        t = {},
        n = {
          begin: /\$\{/,
          end: /\}/,
          contains: ["self", {
            begin: /:-/,
            contains: [t]
          }]
        };
      Object.assign(t, {
        className: "variable",
        variants: [{
          begin: s.concat(/\$[\w\d#@][\w\d_]*/, "(?![\\w\\d])(?![$])")
        }, n]
      });
      var a = {
          className: "subst",
          begin: /\$\(/,
          end: /\)/,
          contains: [e.BACKSLASH_ESCAPE]
        },
        i = {
          begin: /<<-?\s*(?=\w+)/,
          starts: {
            contains: [e.END_SAME_AS_BEGIN({
              begin: /(\w+)/,
              end: /(\w+)/,
              className: "string"
            })]
          }
        },
        c = {
          className: "string",
          begin: /"/,
          end: /"/,
          contains: [e.BACKSLASH_ESCAPE, t, a]
        };
      a.contains.push(c);
      var o = {
          begin: /\$?\(\(/,
          end: /\)\)/,
          contains: [{
            begin: /\d+#[0-9a-f]+/,
            className: "number"
          }, e.NUMBER_MODE, t]
        },
        r = e.SHEBANG({
          binary: "(fish|bash|zsh|sh|csh|ksh|tcsh|dash|scsh)",
          relevance: 10
        }),
        l = {
          className: "function",
          begin: /\w[\w\d_]*\s*\(\s*\)\s*\{/,
          returnBegin: !0,
          contains: [e.inherit(e.TITLE_MODE, {
            begin: /\w[\w\d_]*/
          })],
          relevance: 0
        };
      return {
        name: "Bash",
        aliases: ["sh"],
        keywords: {
          $pattern: /\b[a-z][a-z0-9._-]+\b/,
          keyword: ["if", "then", "else", "elif", "fi", "for", "while", "in", "do", "done", "case", "esac", "function"],
          literal: ["true", "false"],
          built_in: ["break", "cd", "continue", "eval", "exec", "exit", "export", "getopts", "hash", "pwd", "readonly", "return", "shift", "test", "times", "trap", "umask", "unset", "alias", "bind", "builtin", "caller", "command", "declare", "echo", "enable", "help", "let", "local", "logout", "mapfile", "printf", "read", "readarray", "source", "type", "typeset", "ulimit", "unalias", "set", "shopt", "autoload", "bg", "bindkey", "bye", "cap", "chdir", "clone", "comparguments", "compcall", "compctl", "compdescribe", "compfiles", "compgroups", "compquote", "comptags", "comptry", "compvalues", "dirs", "disable", "disown", "echotc", "echoti", "emulate", "fc", "fg", "float", "functions", "getcap", "getln", "history", "integer", "jobs", "kill", "limit", "log", "noglob", "popd", "print", "pushd", "pushln", "rehash", "sched", "setcap", "setopt", "stat", "suspend", "ttyctl", "unfunction", "unhash", "unlimit", "unsetopt", "vared", "wait", "whence", "where", "which", "zcompile", "zformat", "zftp", "zle", "zmodload", "zparseopts", "zprof", "zpty", "zregexparse", "zsocket", "zstyle", "ztcp", "chcon", "chgrp", "chown", "chmod", "cp", "dd", "df", "dir", "dircolors", "ln", "ls", "mkdir", "mkfifo", "mknod", "mktemp", "mv", "realpath", "rm", "rmdir", "shred", "sync", "touch", "truncate", "vdir", "b2sum", "base32", "base64", "cat", "cksum", "comm", "csplit", "cut", "expand", "fmt", "fold", "head", "join", "md5sum", "nl", "numfmt", "od", "paste", "ptx", "pr", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum", "shuf", "sort", "split", "sum", "tac", "tail", "tr", "tsort", "unexpand", "uniq", "wc", "arch", "basename", "chroot", "date", "dirname", "du", "echo", "env", "expr", "factor", "groups", "hostid", "id", "link", "logname", "nice", "nohup", "nproc", "pathchk", "pinky", "printenv", "printf", "pwd", "readlink", "runcon", "seq", "sleep", "stat", "stdbuf", "stty", "tee", "test", "timeout", "tty", "uname", "unlink", "uptime", "users", "who", "whoami", "yes"]
        },
        contains: [r, e.SHEBANG(), l, o, e.HASH_COMMENT_MODE, i, {
          match: /(\/[a-z._-]+)+/
        }, c, {
          className: "",
          begin: /\\"/
        }, {
          className: "string",
          begin: /'/,
          end: /'/
        }, t]
      };
    };
  }();
  hljs.registerLanguage("bash", e);
})(); /*! `css` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    var e = ["a", "abbr", "address", "article", "aside", "audio", "b", "blockquote", "body", "button", "canvas", "caption", "cite", "code", "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "mark", "menu", "nav", "object", "ol", "p", "q", "quote", "samp", "section", "span", "strong", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "tr", "ul", "var", "video"],
      i = ["any-hover", "any-pointer", "aspect-ratio", "color", "color-gamut", "color-index", "device-aspect-ratio", "device-height", "device-width", "display-mode", "forced-colors", "grid", "height", "hover", "inverted-colors", "monochrome", "orientation", "overflow-block", "overflow-inline", "pointer", "prefers-color-scheme", "prefers-contrast", "prefers-reduced-motion", "prefers-reduced-transparency", "resolution", "scan", "scripting", "update", "width", "min-width", "max-width", "min-height", "max-height"],
      r = ["active", "any-link", "blank", "checked", "current", "default", "defined", "dir", "disabled", "drop", "empty", "enabled", "first", "first-child", "first-of-type", "fullscreen", "future", "focus", "focus-visible", "focus-within", "has", "host", "host-context", "hover", "indeterminate", "in-range", "invalid", "is", "lang", "last-child", "last-of-type", "left", "link", "local-link", "not", "nth-child", "nth-col", "nth-last-child", "nth-last-col", "nth-last-of-type", "nth-of-type", "only-child", "only-of-type", "optional", "out-of-range", "past", "placeholder-shown", "read-only", "read-write", "required", "right", "root", "scope", "target", "target-within", "user-invalid", "valid", "visited", "where"],
      t = ["after", "backdrop", "before", "cue", "cue-region", "first-letter", "first-line", "grammar-error", "marker", "part", "placeholder", "selection", "slotted", "spelling-error"],
      o = ["align-content", "align-items", "align-self", "all", "animation", "animation-delay", "animation-direction", "animation-duration", "animation-fill-mode", "animation-iteration-count", "animation-name", "animation-play-state", "animation-timing-function", "backface-visibility", "background", "background-attachment", "background-blend-mode", "background-clip", "background-color", "background-image", "background-origin", "background-position", "background-repeat", "background-size", "block-size", "border", "border-block", "border-block-color", "border-block-end", "border-block-end-color", "border-block-end-style", "border-block-end-width", "border-block-start", "border-block-start-color", "border-block-start-style", "border-block-start-width", "border-block-style", "border-block-width", "border-bottom", "border-bottom-color", "border-bottom-left-radius", "border-bottom-right-radius", "border-bottom-style", "border-bottom-width", "border-collapse", "border-color", "border-image", "border-image-outset", "border-image-repeat", "border-image-slice", "border-image-source", "border-image-width", "border-inline", "border-inline-color", "border-inline-end", "border-inline-end-color", "border-inline-end-style", "border-inline-end-width", "border-inline-start", "border-inline-start-color", "border-inline-start-style", "border-inline-start-width", "border-inline-style", "border-inline-width", "border-left", "border-left-color", "border-left-style", "border-left-width", "border-radius", "border-right", "border-right-color", "border-right-style", "border-right-width", "border-spacing", "border-style", "border-top", "border-top-color", "border-top-left-radius", "border-top-right-radius", "border-top-style", "border-top-width", "border-width", "bottom", "box-decoration-break", "box-shadow", "box-sizing", "break-after", "break-before", "break-inside", "caption-side", "caret-color", "clear", "clip", "clip-path", "clip-rule", "color", "column-count", "column-fill", "column-gap", "column-rule", "column-rule-color", "column-rule-style", "column-rule-width", "column-span", "column-width", "columns", "contain", "content", "content-visibility", "counter-increment", "counter-reset", "cue", "cue-after", "cue-before", "cursor", "direction", "display", "empty-cells", "filter", "flex", "flex-basis", "flex-direction", "flex-flow", "flex-grow", "flex-shrink", "flex-wrap", "float", "flow", "font", "font-display", "font-family", "font-feature-settings", "font-kerning", "font-language-override", "font-size", "font-size-adjust", "font-smoothing", "font-stretch", "font-style", "font-synthesis", "font-variant", "font-variant-caps", "font-variant-east-asian", "font-variant-ligatures", "font-variant-numeric", "font-variant-position", "font-variation-settings", "font-weight", "gap", "glyph-orientation-vertical", "grid", "grid-area", "grid-auto-columns", "grid-auto-flow", "grid-auto-rows", "grid-column", "grid-column-end", "grid-column-start", "grid-gap", "grid-row", "grid-row-end", "grid-row-start", "grid-template", "grid-template-areas", "grid-template-columns", "grid-template-rows", "hanging-punctuation", "height", "hyphens", "icon", "image-orientation", "image-rendering", "image-resolution", "ime-mode", "inline-size", "isolation", "justify-content", "left", "letter-spacing", "line-break", "line-height", "list-style", "list-style-image", "list-style-position", "list-style-type", "margin", "margin-block", "margin-block-end", "margin-block-start", "margin-bottom", "margin-inline", "margin-inline-end", "margin-inline-start", "margin-left", "margin-right", "margin-top", "marks", "mask", "mask-border", "mask-border-mode", "mask-border-outset", "mask-border-repeat", "mask-border-slice", "mask-border-source", "mask-border-width", "mask-clip", "mask-composite", "mask-image", "mask-mode", "mask-origin", "mask-position", "mask-repeat", "mask-size", "mask-type", "max-block-size", "max-height", "max-inline-size", "max-width", "min-block-size", "min-height", "min-inline-size", "min-width", "mix-blend-mode", "nav-down", "nav-index", "nav-left", "nav-right", "nav-up", "none", "normal", "object-fit", "object-position", "opacity", "order", "orphans", "outline", "outline-color", "outline-offset", "outline-style", "outline-width", "overflow", "overflow-wrap", "overflow-x", "overflow-y", "padding", "padding-block", "padding-block-end", "padding-block-start", "padding-bottom", "padding-inline", "padding-inline-end", "padding-inline-start", "padding-left", "padding-right", "padding-top", "page-break-after", "page-break-before", "page-break-inside", "pause", "pause-after", "pause-before", "perspective", "perspective-origin", "pointer-events", "position", "quotes", "resize", "rest", "rest-after", "rest-before", "right", "row-gap", "scroll-margin", "scroll-margin-block", "scroll-margin-block-end", "scroll-margin-block-start", "scroll-margin-bottom", "scroll-margin-inline", "scroll-margin-inline-end", "scroll-margin-inline-start", "scroll-margin-left", "scroll-margin-right", "scroll-margin-top", "scroll-padding", "scroll-padding-block", "scroll-padding-block-end", "scroll-padding-block-start", "scroll-padding-bottom", "scroll-padding-inline", "scroll-padding-inline-end", "scroll-padding-inline-start", "scroll-padding-left", "scroll-padding-right", "scroll-padding-top", "scroll-snap-align", "scroll-snap-stop", "scroll-snap-type", "scrollbar-color", "scrollbar-gutter", "scrollbar-width", "shape-image-threshold", "shape-margin", "shape-outside", "speak", "speak-as", "src", "tab-size", "table-layout", "text-align", "text-align-all", "text-align-last", "text-combine-upright", "text-decoration", "text-decoration-color", "text-decoration-line", "text-decoration-style", "text-emphasis", "text-emphasis-color", "text-emphasis-position", "text-emphasis-style", "text-indent", "text-justify", "text-orientation", "text-overflow", "text-rendering", "text-shadow", "text-transform", "text-underline-position", "top", "transform", "transform-box", "transform-origin", "transform-style", "transition", "transition-delay", "transition-duration", "transition-property", "transition-timing-function", "unicode-bidi", "vertical-align", "visibility", "voice-balance", "voice-duration", "voice-family", "voice-pitch", "voice-range", "voice-rate", "voice-stress", "voice-volume", "white-space", "widows", "width", "will-change", "word-break", "word-spacing", "word-wrap", "writing-mode", "z-index"].reverse();
    return function (n) {
      var a = n.regex,
        l = function (e) {
          return {
            IMPORTANT: {
              scope: "meta",
              begin: "!important"
            },
            BLOCK_COMMENT: e.C_BLOCK_COMMENT_MODE,
            HEXCOLOR: {
              scope: "number",
              begin: /#(([0-9a-fA-F]{3,4})|(([0-9a-fA-F]{2}){3,4}))\b/
            },
            FUNCTION_DISPATCH: {
              className: "built_in",
              begin: /[\w-]+(?=\()/
            },
            ATTRIBUTE_SELECTOR_MODE: {
              scope: "selector-attr",
              begin: /\[/,
              end: /\]/,
              illegal: "$",
              contains: [e.APOS_STRING_MODE, e.QUOTE_STRING_MODE]
            },
            CSS_NUMBER_MODE: {
              scope: "number",
              begin: e.NUMBER_RE + "(%|em|ex|ch|rem|vw|vh|vmin|vmax|cm|mm|in|pt|pc|px|deg|grad|rad|turn|s|ms|Hz|kHz|dpi|dpcm|dppx)?",
              relevance: 0
            },
            CSS_VARIABLE: {
              className: "attr",
              begin: /--[A-Za-z][A-Za-z0-9_-]*/
            }
          };
        }(n),
        s = [n.APOS_STRING_MODE, n.QUOTE_STRING_MODE];
      return {
        name: "CSS",
        case_insensitive: !0,
        illegal: /[=|'\$]/,
        keywords: {
          keyframePosition: "from to"
        },
        classNameAliases: {
          keyframePosition: "selector-tag"
        },
        contains: [l.BLOCK_COMMENT, {
          begin: /-(webkit|moz|ms|o)-(?=[a-z])/
        }, l.CSS_NUMBER_MODE, {
          className: "selector-id",
          begin: /#[A-Za-z0-9_-]+/,
          relevance: 0
        }, {
          className: "selector-class",
          begin: "\\.[a-zA-Z-][a-zA-Z0-9_-]*",
          relevance: 0
        }, l.ATTRIBUTE_SELECTOR_MODE, {
          className: "selector-pseudo",
          variants: [{
            begin: ":(" + r.join("|") + ")"
          }, {
            begin: ":(:)?(" + t.join("|") + ")"
          }]
        }, l.CSS_VARIABLE, {
          className: "attribute",
          begin: "\\b(" + o.join("|") + ")\\b"
        }, {
          begin: /:/,
          end: /[;}{]/,
          contains: [l.BLOCK_COMMENT, l.HEXCOLOR, l.IMPORTANT, l.CSS_NUMBER_MODE].concat(s, [{
            begin: /(url|data-uri)\(/,
            end: /\)/,
            relevance: 0,
            keywords: {
              built_in: "url data-uri"
            },
            contains: [].concat(s, [{
              className: "string",
              begin: /[^)]/,
              endsWithParent: !0,
              excludeEnd: !0
            }])
          }, l.FUNCTION_DISPATCH])
        }, {
          begin: a.lookahead(/@/),
          end: "[{;]",
          relevance: 0,
          illegal: /:/,
          contains: [{
            className: "keyword",
            begin: /@-?\w[\w]*(-\w+)*/
          }, {
            begin: /\s/,
            endsWithParent: !0,
            excludeEnd: !0,
            relevance: 0,
            keywords: {
              $pattern: /[a-z-]+/,
              keyword: "and or not only",
              attribute: i.join(" ")
            },
            contains: [{
              begin: /[a-z-]+(?=:)/,
              className: "attribute"
            }].concat(s, [l.CSS_NUMBER_MODE])
          }]
        }, {
          className: "selector-tag",
          begin: "\\b(" + e.join("|") + ")\\b"
        }]
      };
    };
  }();
  hljs.registerLanguage("css", e);
})(); /*! `swift` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    function e(e) {
      return e ? "string" == typeof e ? e : e.source : null;
    }
    function a(e) {
      return t("(?=", e, ")");
    }
    function t() {
      for (var _len5 = arguments.length, a = new Array(_len5), _key5 = 0; _key5 < _len5; _key5++) {
        a[_key5] = arguments[_key5];
      }
      return a.map(function (a) {
        return e(a);
      }).join("");
    }
    function n() {
      for (var _len6 = arguments.length, a = new Array(_len6), _key6 = 0; _key6 < _len6; _key6++) {
        a[_key6] = arguments[_key6];
      }
      var t = function (e) {
        var a = e[e.length - 1];
        return "object" == (0,_babel_runtime_helpers_typeof__WEBPACK_IMPORTED_MODULE_8__["default"])(a) && a.constructor === Object ? (e.splice(e.length - 1, 1), a) : {};
      }(a);
      return "(" + (t.capture ? "" : "?:") + a.map(function (a) {
        return e(a);
      }).join("|") + ")";
    }
    var i = function i(e) {
        return t(/\b/, e, /\w$/.test(e) ? /\b/ : /\B/);
      },
      s = ["Protocol", "Type"].map(i),
      u = ["init", "self"].map(i),
      c = ["Any", "Self"],
      r = ["actor", "any", "associatedtype", "async", "await", /as\?/, /as!/, "as", "break", "case", "catch", "class", "continue", "convenience", "default", "defer", "deinit", "didSet", "distributed", "do", "dynamic", "else", "enum", "extension", "fallthrough", /fileprivate\(set\)/, "fileprivate", "final", "for", "func", "get", "guard", "if", "import", "indirect", "infix", /init\?/, /init!/, "inout", /internal\(set\)/, "internal", "in", "is", "isolated", "nonisolated", "lazy", "let", "mutating", "nonmutating", /open\(set\)/, "open", "operator", "optional", "override", "postfix", "precedencegroup", "prefix", /private\(set\)/, "private", "protocol", /public\(set\)/, "public", "repeat", "required", "rethrows", "return", "set", "some", "static", "struct", "subscript", "super", "switch", "throws", "throw", /try\?/, /try!/, "try", "typealias", /unowned\(safe\)/, /unowned\(unsafe\)/, "unowned", "var", "weak", "where", "while", "willSet"],
      o = ["false", "nil", "true"],
      l = ["assignment", "associativity", "higherThan", "left", "lowerThan", "none", "right"],
      m = ["#colorLiteral", "#column", "#dsohandle", "#else", "#elseif", "#endif", "#error", "#file", "#fileID", "#fileLiteral", "#filePath", "#function", "#if", "#imageLiteral", "#keyPath", "#line", "#selector", "#sourceLocation", "#warn_unqualified_access", "#warning"],
      p = ["abs", "all", "any", "assert", "assertionFailure", "debugPrint", "dump", "fatalError", "getVaList", "isKnownUniquelyReferenced", "max", "min", "numericCast", "pointwiseMax", "pointwiseMin", "precondition", "preconditionFailure", "print", "readLine", "repeatElement", "sequence", "stride", "swap", "swift_unboxFromSwiftValueWithType", "transcode", "type", "unsafeBitCast", "unsafeDowncast", "withExtendedLifetime", "withUnsafeMutablePointer", "withUnsafePointer", "withVaList", "withoutActuallyEscaping", "zip"],
      d = n(/[/=\-+!*%<>&|^~?]/, /[\u00A1-\u00A7]/, /[\u00A9\u00AB]/, /[\u00AC\u00AE]/, /[\u00B0\u00B1]/, /[\u00B6\u00BB\u00BF\u00D7\u00F7]/, /[\u2016-\u2017]/, /[\u2020-\u2027]/, /[\u2030-\u203E]/, /[\u2041-\u2053]/, /[\u2055-\u205E]/, /[\u2190-\u23FF]/, /[\u2500-\u2775]/, /[\u2794-\u2BFF]/, /[\u2E00-\u2E7F]/, /[\u3001-\u3003]/, /[\u3008-\u3020]/, /[\u3030]/),
      F = n(d, /[\u0300-\u036F]/, /[\u1DC0-\u1DFF]/, /[\u20D0-\u20FF]/, /[\uFE00-\uFE0F]/, /[\uFE20-\uFE2F]/),
      b = t(d, F, "*"),
      h = n(/[a-zA-Z_]/, /[\u00A8\u00AA\u00AD\u00AF\u00B2-\u00B5\u00B7-\u00BA]/, /[\u00BC-\u00BE\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF]/, /[\u0100-\u02FF\u0370-\u167F\u1681-\u180D\u180F-\u1DBF]/, /[\u1E00-\u1FFF]/, /[\u200B-\u200D\u202A-\u202E\u203F-\u2040\u2054\u2060-\u206F]/, /[\u2070-\u20CF\u2100-\u218F\u2460-\u24FF\u2776-\u2793]/, /[\u2C00-\u2DFF\u2E80-\u2FFF]/, /[\u3004-\u3007\u3021-\u302F\u3031-\u303F\u3040-\uD7FF]/, /[\uF900-\uFD3D\uFD40-\uFDCF\uFDF0-\uFE1F\uFE30-\uFE44]/, /[\uFE47-\uFEFE\uFF00-\uFFFD]/),
      f = n(h, /\d/, /[\u0300-\u036F\u1DC0-\u1DFF\u20D0-\u20FF\uFE20-\uFE2F]/),
      w = t(h, f, "*"),
      y = t(/[A-Z]/, f, "*"),
      g = ["autoclosure", t(/convention\(/, n("swift", "block", "c"), /\)/), "discardableResult", "dynamicCallable", "dynamicMemberLookup", "escaping", "frozen", "GKInspectable", "IBAction", "IBDesignable", "IBInspectable", "IBOutlet", "IBSegueAction", "inlinable", "main", "nonobjc", "NSApplicationMain", "NSCopying", "NSManaged", t(/objc\(/, w, /\)/), "objc", "objcMembers", "propertyWrapper", "requires_stored_property_inits", "resultBuilder", "testable", "UIApplicationMain", "unknown", "usableFromInline"],
      E = ["iOS", "iOSApplicationExtension", "macOS", "macOSApplicationExtension", "macCatalyst", "macCatalystApplicationExtension", "watchOS", "watchOSApplicationExtension", "tvOS", "tvOSApplicationExtension", "swift"];
    return function (e) {
      var d = {
          match: /\s+/,
          relevance: 0
        },
        h = e.COMMENT("/\\*", "\\*/", {
          contains: ["self"]
        }),
        v = [e.C_LINE_COMMENT_MODE, h],
        A = {
          match: [/\./, n.apply(void 0, (0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(s).concat((0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(u)))],
          className: {
            2: "keyword"
          }
        },
        N = {
          match: t(/\./, n.apply(void 0, r)),
          relevance: 0
        },
        C = r.filter(function (e) {
          return "string" == typeof e;
        }).concat(["_|0"]),
        D = {
          variants: [{
            className: "keyword",
            match: n.apply(void 0, (0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(r.filter(function (e) {
              return "string" != typeof e;
            }).concat(c).map(i)).concat((0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(u)))
          }]
        },
        k = {
          $pattern: n(/\b\w+/, /#\w+/),
          keyword: C.concat(m),
          literal: o
        },
        B = [A, N, D],
        _ = [{
          match: t(/\./, n.apply(void 0, p)),
          relevance: 0
        }, {
          className: "built_in",
          match: t(/\b/, n.apply(void 0, p), /(?=\()/)
        }],
        S = {
          match: /->/,
          relevance: 0
        },
        M = [S, {
          className: "operator",
          relevance: 0,
          variants: [{
            match: b
          }, {
            match: "\\.(\\.|".concat(F, ")+")
          }]
        }],
        x = "([0-9a-fA-F]_*)+",
        I = {
          className: "number",
          relevance: 0,
          variants: [{
            match: "\\b(([0-9]_*)+)(\\.(([0-9]_*)+))?([eE][+-]?(([0-9]_*)+))?\\b"
          }, {
            match: "\\b0x(".concat(x, ")(\\.(").concat(x, "))?([pP][+-]?(([0-9]_*)+))?\\b")
          }, {
            match: /\b0o([0-7]_*)+\b/
          }, {
            match: /\b0b([01]_*)+\b/
          }]
        },
        L = function L() {
          var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
          return {
            className: "subst",
            variants: [{
              match: t(/\\/, e, /[0\\tnr"']/)
            }, {
              match: t(/\\/, e, /u\{[0-9a-fA-F]{1,8}\}/)
            }]
          };
        },
        O = function O() {
          var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
          return {
            className: "subst",
            match: t(/\\/, e, /[\t ]*(?:[\r\n]|\r\n)/)
          };
        },
        T = function T() {
          var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
          return {
            className: "subst",
            label: "interpol",
            begin: t(/\\/, e, /\(/),
            end: /\)/
          };
        },
        $ = function $() {
          var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
          return {
            begin: t(e, /"""/),
            end: t(/"""/, e),
            contains: [L(e), O(e), T(e)]
          };
        },
        j = function j() {
          var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
          return {
            begin: t(e, /"/),
            end: t(/"/, e),
            contains: [L(e), T(e)]
          };
        },
        P = {
          className: "string",
          variants: [$(), $("#"), $("##"), $("###"), j(), j("#"), j("##"), j("###")]
        },
        K = {
          match: t(/`/, w, /`/)
        },
        z = [K, {
          className: "variable",
          match: /\$\d+/
        }, {
          className: "variable",
          match: "\\$".concat(f, "+")
        }],
        q = [{
          match: /(@|#(un)?)available/,
          className: "keyword",
          starts: {
            contains: [{
              begin: /\(/,
              end: /\)/,
              keywords: E,
              contains: [].concat(M, [I, P])
            }]
          }
        }, {
          className: "keyword",
          match: t(/@/, n.apply(void 0, g))
        }, {
          className: "meta",
          match: t(/@/, w)
        }],
        U = {
          match: a(/\b[A-Z]/),
          relevance: 0,
          contains: [{
            className: "type",
            match: t(/(AV|CA|CF|CG|CI|CL|CM|CN|CT|MK|MP|MTK|MTL|NS|SCN|SK|UI|WK|XC)/, f, "+")
          }, {
            className: "type",
            match: y,
            relevance: 0
          }, {
            match: /[?!]+/,
            relevance: 0
          }, {
            match: /\.\.\./,
            relevance: 0
          }, {
            match: t(/\s+&\s+/, a(y)),
            relevance: 0
          }]
        },
        Z = {
          begin: /</,
          end: />/,
          keywords: k,
          contains: [].concat(v, B, q, [S, U])
        };
      U.contains.push(Z);
      var V = {
          begin: /\(/,
          end: /\)/,
          relevance: 0,
          keywords: k,
          contains: ["self", {
            match: t(w, /\s*:/),
            keywords: "_|0",
            relevance: 0
          }].concat(v, B, _, M, [I, P], z, q, [U])
        },
        W = {
          begin: /</,
          end: />/,
          contains: [].concat(v, [U])
        },
        G = {
          begin: /\(/,
          end: /\)/,
          keywords: k,
          contains: [{
            begin: n(a(t(w, /\s*:/)), a(t(w, /\s+/, w, /\s*:/))),
            end: /:/,
            relevance: 0,
            contains: [{
              className: "keyword",
              match: /\b_\b/
            }, {
              className: "params",
              match: w
            }]
          }].concat(v, B, M, [I, P], q, [U, V]),
          endsParent: !0,
          illegal: /["']/
        },
        R = {
          match: [/func/, /\s+/, n(K.match, w, b)],
          className: {
            1: "keyword",
            3: "title.function"
          },
          contains: [W, G, d],
          illegal: [/\[/, /%/]
        },
        X = {
          match: [/\b(?:subscript|init[?!]?)/, /\s*(?=[<(])/],
          className: {
            1: "keyword"
          },
          contains: [W, G, d],
          illegal: /\[|%/
        },
        H = {
          match: [/operator/, /\s+/, b],
          className: {
            1: "keyword",
            3: "title"
          }
        },
        J = {
          begin: [/precedencegroup/, /\s+/, y],
          className: {
            1: "keyword",
            3: "title"
          },
          contains: [U],
          keywords: [].concat(l, o),
          end: /}/
        };
      var _iterator = _createForOfIteratorHelper(P.variants),
        _step;
      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var _e7 = _step.value;
          var _a = _e7.contains.find(function (e) {
            return "interpol" === e.label;
          });
          _a.keywords = k;
          var _t9 = [].concat(B, _, M, [I, P], z);
          _a.contains = [].concat((0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(_t9), [{
            begin: /\(/,
            end: /\)/,
            contains: ["self"].concat((0,_babel_runtime_helpers_toConsumableArray__WEBPACK_IMPORTED_MODULE_5__["default"])(_t9))
          }]);
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
      return {
        name: "Swift",
        keywords: k,
        contains: [].concat(v, [R, X, {
          beginKeywords: "struct protocol class extension enum actor",
          end: "\\{",
          excludeEnd: !0,
          keywords: k,
          contains: [e.inherit(e.TITLE_MODE, {
            className: "title.class",
            begin: /[A-Za-z$_][\u00C0-\u02B80-9A-Za-z$_]*/
          })].concat(B)
        }, H, J, {
          beginKeywords: "import",
          end: /$/,
          contains: [].concat(v),
          relevance: 0
        }], B, _, M, [I, P], z, q, [U, V])
      };
    };
  }();
  hljs.registerLanguage("swift", e);
})(); /*! `wasm` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      e.regex;
      var a = e.COMMENT(/\(;/, /;\)/);
      return a.contains.push("self"), {
        name: "WebAssembly",
        keywords: {
          $pattern: /[\w.]+/,
          keyword: ["anyfunc", "block", "br", "br_if", "br_table", "call", "call_indirect", "data", "drop", "elem", "else", "end", "export", "func", "global.get", "global.set", "local.get", "local.set", "local.tee", "get_global", "get_local", "global", "if", "import", "local", "loop", "memory", "memory.grow", "memory.size", "module", "mut", "nop", "offset", "param", "result", "return", "select", "set_global", "set_local", "start", "table", "tee_local", "then", "type", "unreachable"]
        },
        contains: [e.COMMENT(/;;/, /$/), a, {
          match: [/(?:offset|align)/, /\s*/, /=/],
          className: {
            1: "keyword",
            3: "operator"
          }
        }, {
          className: "variable",
          begin: /\$[\w_]+/
        }, {
          match: /(\((?!;)|\))+/,
          className: "punctuation",
          relevance: 0
        }, {
          begin: [/(?:func|call|call_indirect)/, /\s+/, /\$[^\s)]+/],
          className: {
            1: "keyword",
            3: "title.function"
          }
        }, e.QUOTE_STRING_MODE, {
          match: /(i32|i64|f32|f64)(?!\.)/,
          className: "type"
        }, {
          className: "keyword",
          match: /\b(f32|f64|i32|i64)(?:\.(?:abs|add|and|ceil|clz|const|convert_[su]\/i(?:32|64)|copysign|ctz|demote\/f64|div(?:_[su])?|eqz?|extend_[su]\/i32|floor|ge(?:_[su])?|gt(?:_[su])?|le(?:_[su])?|load(?:(?:8|16|32)_[su])?|lt(?:_[su])?|max|min|mul|nearest|neg?|or|popcnt|promote\/f32|reinterpret\/[fi](?:32|64)|rem_[su]|rot[lr]|shl|shr_[su]|store(?:8|16|32)?|sqrt|sub|trunc(?:_[su]\/f(?:32|64))?|wrap\/i64|xor))\b/
        }, {
          className: "number",
          relevance: 0,
          match: /[+-]?\b(?:\d(?:_?\d)*(?:\.\d(?:_?\d)*)?(?:[eE][+-]?\d(?:_?\d)*)?|0x[\da-fA-F](?:_?[\da-fA-F])*(?:\.[\da-fA-F](?:_?[\da-fA-D])*)?(?:[pP][+-]?\d(?:_?\d)*)?)\b|\binf\b|\bnan(?::0x[\da-fA-F](?:_?[\da-fA-D])*)?\b/
        }]
      };
    };
  }();
  hljs.registerLanguage("wasm", e);
})(); /*! `vbnet` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = e.regex,
        t = /\d{1,2}\/\d{1,2}\/\d{4}/,
        a = /\d{4}-\d{1,2}-\d{1,2}/,
        i = /(\d|1[012])(:\d+){0,2} *(AM|PM)/,
        s = /\d{1,2}(:\d{1,2}){1,2}/,
        r = {
          className: "literal",
          variants: [{
            begin: n.concat(/# */, n.either(a, t), / *#/)
          }, {
            begin: n.concat(/# */, s, / *#/)
          }, {
            begin: n.concat(/# */, i, / *#/)
          }, {
            begin: n.concat(/# */, n.either(a, t), / +/, n.either(i, s), / *#/)
          }]
        },
        l = e.COMMENT(/'''/, /$/, {
          contains: [{
            className: "doctag",
            begin: /<\/?/,
            end: />/
          }]
        }),
        o = e.COMMENT(null, /$/, {
          variants: [{
            begin: /'/
          }, {
            begin: /([\t ]|^)REM(?=\s)/
          }]
        });
      return {
        name: "Visual Basic .NET",
        aliases: ["vb"],
        case_insensitive: !0,
        classNameAliases: {
          label: "symbol"
        },
        keywords: {
          keyword: "addhandler alias aggregate ansi as async assembly auto binary by byref byval call case catch class compare const continue custom declare default delegate dim distinct do each equals else elseif end enum erase error event exit explicit finally for friend from function get global goto group handles if implements imports in inherits interface into iterator join key let lib loop me mid module mustinherit mustoverride mybase myclass namespace narrowing new next notinheritable notoverridable of off on operator option optional order overloads overridable overrides paramarray partial preserve private property protected public raiseevent readonly redim removehandler resume return select set shadows shared skip static step stop structure strict sub synclock take text then throw to try unicode until using when where while widening with withevents writeonly yield",
          built_in: "addressof and andalso await directcast gettype getxmlnamespace is isfalse isnot istrue like mod nameof new not or orelse trycast typeof xor cbool cbyte cchar cdate cdbl cdec cint clng cobj csbyte cshort csng cstr cuint culng cushort",
          type: "boolean byte char date decimal double integer long object sbyte short single string uinteger ulong ushort",
          literal: "true false nothing"
        },
        illegal: "//|\\{|\\}|endif|gosub|variant|wend|^\\$ ",
        contains: [{
          className: "string",
          begin: /"(""|[^/n])"C\b/
        }, {
          className: "string",
          begin: /"/,
          end: /"/,
          illegal: /\n/,
          contains: [{
            begin: /""/
          }]
        }, r, {
          className: "number",
          relevance: 0,
          variants: [{
            begin: /\b\d[\d_]*((\.[\d_]+(E[+-]?[\d_]+)?)|(E[+-]?[\d_]+))[RFD@!#]?/
          }, {
            begin: /\b\d[\d_]*((U?[SIL])|[%&])?/
          }, {
            begin: /&H[\dA-F_]+((U?[SIL])|[%&])?/
          }, {
            begin: /&O[0-7_]+((U?[SIL])|[%&])?/
          }, {
            begin: /&B[01_]+((U?[SIL])|[%&])?/
          }]
        }, {
          className: "label",
          begin: /^\w+:/
        }, l, o, {
          className: "meta",
          begin: /[\t ]*#(const|disable|else|elseif|enable|end|externalsource|if|region)\b/,
          end: /$/,
          keywords: {
            keyword: "const disable else elseif enable end externalsource if region then"
          },
          contains: [o]
        }]
      };
    };
  }();
  hljs.registerLanguage("vbnet", e);
})(); /*! `markdown` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = {
          begin: /<\/?[A-Za-z_]/,
          end: ">",
          subLanguage: "xml",
          relevance: 0
        },
        a = {
          variants: [{
            begin: /\[.+?\]\[.*?\]/,
            relevance: 0
          }, {
            begin: /\[.+?\]\(((data|javascript|mailto):|(?:http|ftp)s?:\/\/).*?\)/,
            relevance: 2
          }, {
            begin: e.regex.concat(/\[.+?\]\(/, /[A-Za-z][A-Za-z0-9+.-]*/, /:\/\/.*?\)/),
            relevance: 2
          }, {
            begin: /\[.+?\]\([./?&#].*?\)/,
            relevance: 1
          }, {
            begin: /\[.*?\]\(.*?\)/,
            relevance: 0
          }],
          returnBegin: !0,
          contains: [{
            match: /\[(?=\])/
          }, {
            className: "string",
            relevance: 0,
            begin: "\\[",
            end: "\\]",
            excludeBegin: !0,
            returnEnd: !0
          }, {
            className: "link",
            relevance: 0,
            begin: "\\]\\(",
            end: "\\)",
            excludeBegin: !0,
            excludeEnd: !0
          }, {
            className: "symbol",
            relevance: 0,
            begin: "\\]\\[",
            end: "\\]",
            excludeBegin: !0,
            excludeEnd: !0
          }]
        },
        i = {
          className: "strong",
          contains: [],
          variants: [{
            begin: /_{2}(?!\s)/,
            end: /_{2}/
          }, {
            begin: /\*{2}(?!\s)/,
            end: /\*{2}/
          }]
        },
        s = {
          className: "emphasis",
          contains: [],
          variants: [{
            begin: /\*(?![*\s])/,
            end: /\*/
          }, {
            begin: /_(?![_\s])/,
            end: /_/,
            relevance: 0
          }]
        },
        c = e.inherit(i, {
          contains: []
        }),
        t = e.inherit(s, {
          contains: []
        });
      i.contains.push(t), s.contains.push(c);
      var g = [n, a];
      return [i, s, c, t].forEach(function (e) {
        e.contains = e.contains.concat(g);
      }), g = g.concat(i, s), {
        name: "Markdown",
        aliases: ["md", "mkdown", "mkd"],
        contains: [{
          className: "section",
          variants: [{
            begin: "^#{1,6}",
            end: "$",
            contains: g
          }, {
            begin: "(?=^.+?\\n[=-]{2,}$)",
            contains: [{
              begin: "^[=-]*$"
            }, {
              begin: "^",
              end: "\\n",
              contains: g
            }]
          }]
        }, n, {
          className: "bullet",
          begin: "^[ \t]*([*+-]|(\\d+\\.))(?=\\s+)",
          end: "\\s+",
          excludeEnd: !0
        }, i, s, {
          className: "quote",
          begin: "^>\\s+",
          contains: g,
          end: "$"
        }, {
          className: "code",
          variants: [{
            begin: "(`{3,})[^`](.|\\n)*?\\1`*[ ]*"
          }, {
            begin: "(~{3,})[^~](.|\\n)*?\\1~*[ ]*"
          }, {
            begin: "```",
            end: "```+[ ]*$"
          }, {
            begin: "~~~",
            end: "~~~+[ ]*$"
          }, {
            begin: "`.+?`"
          }, {
            begin: "(?=^( {4}|\\t))",
            contains: [{
              begin: "^( {4}|\\t)",
              end: "(\\n)$"
            }],
            relevance: 0
          }]
        }, {
          begin: "^[-\\*]{3,}",
          end: "$"
        }, a, {
          begin: /^\[[^\n]+\]:/,
          returnBegin: !0,
          contains: [{
            className: "symbol",
            begin: /\[/,
            end: /\]/,
            excludeBegin: !0,
            excludeEnd: !0
          }, {
            className: "link",
            begin: /:\s*/,
            end: /$/,
            excludeBegin: !0
          }]
        }]
      };
    };
  }();
  hljs.registerLanguage("markdown", e);
})(); /*! `java` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    var e = "\\.([0-9](_*[0-9])*)",
      a = "[0-9a-fA-F](_*[0-9a-fA-F])*",
      n = {
        className: "number",
        variants: [{
          begin: "(\\b([0-9](_*[0-9])*)((".concat(e, ")|\\.)?|(").concat(e, "))[eE][+-]?([0-9](_*[0-9])*)[fFdD]?\\b")
        }, {
          begin: "\\b([0-9](_*[0-9])*)((".concat(e, ")[fFdD]?\\b|\\.([fFdD]\\b)?)")
        }, {
          begin: "(".concat(e, ")[fFdD]?\\b")
        }, {
          begin: "\\b([0-9](_*[0-9])*)[fFdD]\\b"
        }, {
          begin: "\\b0[xX]((".concat(a, ")\\.?|(").concat(a, ")?\\.(").concat(a, "))[pP][+-]?([0-9](_*[0-9])*)[fFdD]?\\b")
        }, {
          begin: "\\b(0|[1-9](_*[0-9])*)[lL]?\\b"
        }, {
          begin: "\\b0[xX](".concat(a, ")[lL]?\\b")
        }, {
          begin: "\\b0(_*[0-7])*[lL]?\\b"
        }, {
          begin: "\\b0[bB][01](_*[01])*[lL]?\\b"
        }],
        relevance: 0
      };
    function s(e, a, n) {
      return -1 === n ? "" : e.replace(a, function (t) {
        return s(e, a, n - 1);
      });
    }
    return function (e) {
      var a = e.regex,
        t = "[\xC0-\u02B8a-zA-Z_$][\xC0-\u02B8a-zA-Z_$0-9]*",
        i = t + s("(?:<" + t + "~~~(?:\\s*,\\s*" + t + "~~~)*>)?", /~~~/g, 2),
        r = {
          keyword: ["synchronized", "abstract", "private", "var", "static", "if", "const ", "for", "while", "strictfp", "finally", "protected", "import", "native", "final", "void", "enum", "else", "break", "transient", "catch", "instanceof", "volatile", "case", "assert", "package", "default", "public", "try", "switch", "continue", "throws", "protected", "public", "private", "module", "requires", "exports", "do", "sealed", "yield", "permits"],
          literal: ["false", "true", "null"],
          type: ["char", "boolean", "long", "float", "int", "byte", "short", "double"],
          built_in: ["super", "this"]
        },
        l = {
          className: "meta",
          begin: "@" + t,
          contains: [{
            begin: /\(/,
            end: /\)/,
            contains: ["self"]
          }]
        },
        c = {
          className: "params",
          begin: /\(/,
          end: /\)/,
          keywords: r,
          relevance: 0,
          contains: [e.C_BLOCK_COMMENT_MODE],
          endsParent: !0
        };
      return {
        name: "Java",
        aliases: ["jsp"],
        keywords: r,
        illegal: /<\/|#/,
        contains: [e.COMMENT("/\\*\\*", "\\*/", {
          relevance: 0,
          contains: [{
            begin: /\w+@/,
            relevance: 0
          }, {
            className: "doctag",
            begin: "@[A-Za-z]+"
          }]
        }), {
          begin: /import java\.[a-z]+\./,
          keywords: "import",
          relevance: 2
        }, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE, {
          begin: /"""/,
          end: /"""/,
          className: "string",
          contains: [e.BACKSLASH_ESCAPE]
        }, e.APOS_STRING_MODE, e.QUOTE_STRING_MODE, {
          match: [/\b(?:class|interface|enum|extends|implements|new)/, /\s+/, t],
          className: {
            1: "keyword",
            3: "title.class"
          }
        }, {
          match: /non-sealed/,
          scope: "keyword"
        }, {
          begin: [a.concat(/(?!else)/, t), /\s+/, t, /\s+/, /=(?!=)/],
          className: {
            1: "type",
            3: "variable",
            5: "operator"
          }
        }, {
          begin: [/record/, /\s+/, t],
          className: {
            1: "keyword",
            3: "title.class"
          },
          contains: [c, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE]
        }, {
          beginKeywords: "new throw return else",
          relevance: 0
        }, {
          begin: ["(?:" + i + "\\s+)", e.UNDERSCORE_IDENT_RE, /\s*(?=\()/],
          className: {
            2: "title.function"
          },
          keywords: r,
          contains: [{
            className: "params",
            begin: /\(/,
            end: /\)/,
            keywords: r,
            relevance: 0,
            contains: [l, e.APOS_STRING_MODE, e.QUOTE_STRING_MODE, n, e.C_BLOCK_COMMENT_MODE]
          }, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE]
        }, n, l]
      };
    };
  }();
  hljs.registerLanguage("java", e);
})(); /*! `ini` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = e.regex,
        a = {
          className: "number",
          relevance: 0,
          variants: [{
            begin: /([+-]+)?[\d]+_[\d_]+/
          }, {
            begin: e.NUMBER_RE
          }]
        },
        s = e.COMMENT();
      s.variants = [{
        begin: /;/,
        end: /$/
      }, {
        begin: /#/,
        end: /$/
      }];
      var i = {
          className: "variable",
          variants: [{
            begin: /\$[\w\d"][\w\d_]*/
          }, {
            begin: /\$\{(.*?)\}/
          }]
        },
        t = {
          className: "literal",
          begin: /\bon|off|true|false|yes|no\b/
        },
        r = {
          className: "string",
          contains: [e.BACKSLASH_ESCAPE],
          variants: [{
            begin: "'''",
            end: "'''",
            relevance: 10
          }, {
            begin: '"""',
            end: '"""',
            relevance: 10
          }, {
            begin: '"',
            end: '"'
          }, {
            begin: "'",
            end: "'"
          }]
        },
        l = {
          begin: /\[/,
          end: /\]/,
          contains: [s, t, i, r, a, "self"],
          relevance: 0
        },
        c = n.either(/[A-Za-z0-9_-]+/, /"(\\"|[^"])*"/, /'[^']*'/);
      return {
        name: "TOML, also INI",
        aliases: ["toml"],
        case_insensitive: !0,
        illegal: /\S/,
        contains: [s, {
          className: "section",
          begin: /\[+/,
          end: /\]+/
        }, {
          begin: n.concat(c, "(\\s*\\.\\s*", c, ")*", n.lookahead(/\s*=\s*[^#\s]/)),
          className: "attr",
          starts: {
            end: /$/,
            contains: [s, l, t, i, r, a]
          }
        }]
      };
    };
  }();
  hljs.registerLanguage("ini", e);
})(); /*! `c` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = e.regex,
        t = e.COMMENT("//", "$", {
          contains: [{
            begin: /\\\n/
          }]
        }),
        s = "[a-zA-Z_]\\w*::",
        a = "(decltype\\(auto\\)|" + n.optional(s) + "[a-zA-Z_]\\w*" + n.optional("<[^<>]+>") + ")",
        r = {
          className: "type",
          variants: [{
            begin: "\\b[a-z\\d_]*_t\\b"
          }, {
            match: /\batomic_[a-z]{3,6}\b/
          }]
        },
        i = {
          className: "string",
          variants: [{
            begin: '(u8?|U|L)?"',
            end: '"',
            illegal: "\\n",
            contains: [e.BACKSLASH_ESCAPE]
          }, {
            begin: "(u8?|U|L)?'(\\\\(x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4,8}|[0-7]{3}|\\S)|.)",
            end: "'",
            illegal: "."
          }, e.END_SAME_AS_BEGIN({
            begin: /(?:u8?|U|L)?R"([^()\\ ]{0,16})\(/,
            end: /\)([^()\\ ]{0,16})"/
          })]
        },
        l = {
          className: "number",
          variants: [{
            begin: "\\b(0b[01']+)"
          }, {
            begin: "(-?)\\b([\\d']+(\\.[\\d']*)?|\\.[\\d']+)((ll|LL|l|L)(u|U)?|(u|U)(ll|LL|l|L)?|f|F|b|B)"
          }, {
            begin: "(-?)(\\b0[xX][a-fA-F0-9']+|(\\b[\\d']+(\\.[\\d']*)?|\\.[\\d']+)([eE][-+]?[\\d']+)?)"
          }],
          relevance: 0
        },
        o = {
          className: "meta",
          begin: /#\s*[a-z]+\b/,
          end: /$/,
          keywords: {
            keyword: "if else elif endif define undef warning error line pragma _Pragma ifdef ifndef include"
          },
          contains: [{
            begin: /\\\n/,
            relevance: 0
          }, e.inherit(i, {
            className: "string"
          }), {
            className: "string",
            begin: /<.*?>/
          }, t, e.C_BLOCK_COMMENT_MODE]
        },
        c = {
          className: "title",
          begin: n.optional(s) + e.IDENT_RE,
          relevance: 0
        },
        d = n.optional(s) + e.IDENT_RE + "\\s*\\(",
        u = {
          keyword: ["asm", "auto", "break", "case", "continue", "default", "do", "else", "enum", "extern", "for", "fortran", "goto", "if", "inline", "register", "restrict", "return", "sizeof", "struct", "switch", "typedef", "union", "volatile", "while", "_Alignas", "_Alignof", "_Atomic", "_Generic", "_Noreturn", "_Static_assert", "_Thread_local", "alignas", "alignof", "noreturn", "static_assert", "thread_local", "_Pragma"],
          type: ["float", "double", "signed", "unsigned", "int", "short", "long", "char", "void", "_Bool", "_Complex", "_Imaginary", "_Decimal32", "_Decimal64", "_Decimal128", "const", "static", "complex", "bool", "imaginary"],
          literal: "true false NULL",
          built_in: "std string wstring cin cout cerr clog stdin stdout stderr stringstream istringstream ostringstream auto_ptr deque list queue stack vector map set pair bitset multiset multimap unordered_set unordered_map unordered_multiset unordered_multimap priority_queue make_pair array shared_ptr abort terminate abs acos asin atan2 atan calloc ceil cosh cos exit exp fabs floor fmod fprintf fputs free frexp fscanf future isalnum isalpha iscntrl isdigit isgraph islower isprint ispunct isspace isupper isxdigit tolower toupper labs ldexp log10 log malloc realloc memchr memcmp memcpy memset modf pow printf putchar puts scanf sinh sin snprintf sprintf sqrt sscanf strcat strchr strcmp strcpy strcspn strlen strncat strncmp strncpy strpbrk strrchr strspn strstr tanh tan vfprintf vprintf vsprintf endl initializer_list unique_ptr"
        },
        g = [o, r, t, e.C_BLOCK_COMMENT_MODE, l, i],
        m = {
          variants: [{
            begin: /=/,
            end: /;/
          }, {
            begin: /\(/,
            end: /\)/
          }, {
            beginKeywords: "new throw return else",
            end: /;/
          }],
          keywords: u,
          contains: g.concat([{
            begin: /\(/,
            end: /\)/,
            keywords: u,
            contains: g.concat(["self"]),
            relevance: 0
          }]),
          relevance: 0
        },
        p = {
          begin: "(" + a + "[\\*&\\s]+)+" + d,
          returnBegin: !0,
          end: /[{;=]/,
          excludeEnd: !0,
          keywords: u,
          illegal: /[^\w\s\*&:<>.]/,
          contains: [{
            begin: "decltype\\(auto\\)",
            keywords: u,
            relevance: 0
          }, {
            begin: d,
            returnBegin: !0,
            contains: [e.inherit(c, {
              className: "title.function"
            })],
            relevance: 0
          }, {
            relevance: 0,
            match: /,/
          }, {
            className: "params",
            begin: /\(/,
            end: /\)/,
            keywords: u,
            relevance: 0,
            contains: [t, e.C_BLOCK_COMMENT_MODE, i, l, r, {
              begin: /\(/,
              end: /\)/,
              keywords: u,
              relevance: 0,
              contains: ["self", t, e.C_BLOCK_COMMENT_MODE, i, l, r]
            }]
          }, r, t, e.C_BLOCK_COMMENT_MODE, o]
        };
      return {
        name: "C",
        aliases: ["h"],
        keywords: u,
        disableAutodetect: !0,
        illegal: "</",
        contains: [].concat(m, p, g, [o, {
          begin: e.IDENT_RE + "::",
          keywords: u
        }, {
          className: "class",
          beginKeywords: "enum class struct union",
          end: /[{;:<>=]/,
          contains: [{
            beginKeywords: "final class struct"
          }, e.TITLE_MODE]
        }]),
        exports: {
          preprocessor: o,
          strings: i,
          keywords: u
        }
      };
    };
  }();
  hljs.registerLanguage("c", e);
})(); /*! `rust` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var t = e.regex,
        a = {
          className: "title.function.invoke",
          relevance: 0,
          begin: t.concat(/\b/, /(?!let\b)/, e.IDENT_RE, t.lookahead(/\s*\(/))
        },
        n = "([ui](8|16|32|64|128|size)|f(32|64))?",
        s = ["drop ", "Copy", "Send", "Sized", "Sync", "Drop", "Fn", "FnMut", "FnOnce", "ToOwned", "Clone", "Debug", "PartialEq", "PartialOrd", "Eq", "Ord", "AsRef", "AsMut", "Into", "From", "Default", "Iterator", "Extend", "IntoIterator", "DoubleEndedIterator", "ExactSizeIterator", "SliceConcatExt", "ToString", "assert!", "assert_eq!", "bitflags!", "bytes!", "cfg!", "col!", "concat!", "concat_idents!", "debug_assert!", "debug_assert_eq!", "env!", "panic!", "file!", "format!", "format_args!", "include_bytes!", "include_str!", "line!", "local_data_key!", "module_path!", "option_env!", "print!", "println!", "select!", "stringify!", "try!", "unimplemented!", "unreachable!", "vec!", "write!", "writeln!", "macro_rules!", "assert_ne!", "debug_assert_ne!"],
        r = ["i8", "i16", "i32", "i64", "i128", "isize", "u8", "u16", "u32", "u64", "u128", "usize", "f32", "f64", "str", "char", "bool", "Box", "Option", "Result", "String", "Vec"];
      return {
        name: "Rust",
        aliases: ["rs"],
        keywords: {
          $pattern: e.IDENT_RE + "!?",
          type: r,
          keyword: ["abstract", "as", "async", "await", "become", "box", "break", "const", "continue", "crate", "do", "dyn", "else", "enum", "extern", "false", "final", "fn", "for", "if", "impl", "in", "let", "loop", "macro", "match", "mod", "move", "mut", "override", "priv", "pub", "ref", "return", "self", "Self", "static", "struct", "super", "trait", "true", "try", "type", "typeof", "unsafe", "unsized", "use", "virtual", "where", "while", "yield"],
          literal: ["true", "false", "Some", "None", "Ok", "Err"],
          built_in: s
        },
        illegal: "</",
        contains: [e.C_LINE_COMMENT_MODE, e.COMMENT("/\\*", "\\*/", {
          contains: ["self"]
        }), e.inherit(e.QUOTE_STRING_MODE, {
          begin: /b?"/,
          illegal: null
        }), {
          className: "string",
          variants: [{
            begin: /b?r(#*)"(.|\n)*?"\1(?!#)/
          }, {
            begin: /b?'\\?(x\w{2}|u\w{4}|U\w{8}|.)'/
          }]
        }, {
          className: "symbol",
          begin: /'[a-zA-Z_][a-zA-Z0-9_]*/
        }, {
          className: "number",
          variants: [{
            begin: "\\b0b([01_]+)" + n
          }, {
            begin: "\\b0o([0-7_]+)" + n
          }, {
            begin: "\\b0x([A-Fa-f0-9_]+)" + n
          }, {
            begin: "\\b(\\d[\\d_]*(\\.[0-9_]+)?([eE][+-]?[0-9_]+)?)" + n
          }],
          relevance: 0
        }, {
          begin: [/fn/, /\s+/, e.UNDERSCORE_IDENT_RE],
          className: {
            1: "keyword",
            3: "title.function"
          }
        }, {
          className: "meta",
          begin: "#!?\\[",
          end: "\\]",
          contains: [{
            className: "string",
            begin: /"/,
            end: /"/
          }]
        }, {
          begin: [/let/, /\s+/, /(?:mut\s+)?/, e.UNDERSCORE_IDENT_RE],
          className: {
            1: "keyword",
            3: "keyword",
            4: "variable"
          }
        }, {
          begin: [/for/, /\s+/, e.UNDERSCORE_IDENT_RE, /\s+/, /in/],
          className: {
            1: "keyword",
            3: "variable",
            5: "keyword"
          }
        }, {
          begin: [/type/, /\s+/, e.UNDERSCORE_IDENT_RE],
          className: {
            1: "keyword",
            3: "title.class"
          }
        }, {
          begin: [/(?:trait|enum|struct|union|impl|for)/, /\s+/, e.UNDERSCORE_IDENT_RE],
          className: {
            1: "keyword",
            3: "title.class"
          }
        }, {
          begin: e.IDENT_RE + "::",
          keywords: {
            keyword: "Self",
            built_in: s,
            type: r
          }
        }, {
          className: "punctuation",
          begin: "->"
        }, a]
      };
    };
  }();
  hljs.registerLanguage("rust", e);
})(); /*! `go` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = {
        keyword: ["break", "case", "chan", "const", "continue", "default", "defer", "else", "fallthrough", "for", "func", "go", "goto", "if", "import", "interface", "map", "package", "range", "return", "select", "struct", "switch", "type", "var"],
        type: ["bool", "byte", "complex64", "complex128", "error", "float32", "float64", "int8", "int16", "int32", "int64", "string", "uint8", "uint16", "uint32", "uint64", "int", "uint", "uintptr", "rune"],
        literal: ["true", "false", "iota", "nil"],
        built_in: ["append", "cap", "close", "complex", "copy", "imag", "len", "make", "new", "panic", "print", "println", "real", "recover", "delete"]
      };
      return {
        name: "Go",
        aliases: ["golang"],
        keywords: n,
        illegal: "</",
        contains: [e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE, {
          className: "string",
          variants: [e.QUOTE_STRING_MODE, e.APOS_STRING_MODE, {
            begin: "`",
            end: "`"
          }]
        }, {
          className: "number",
          variants: [{
            begin: e.C_NUMBER_RE + "[i]",
            relevance: 1
          }, e.C_NUMBER_MODE]
        }, {
          begin: /:=/
        }, {
          className: "function",
          beginKeywords: "func",
          end: "\\s*(\\{|$)",
          excludeEnd: !0,
          contains: [e.TITLE_MODE, {
            className: "params",
            begin: /\(/,
            end: /\)/,
            endsParent: !0,
            keywords: n,
            illegal: /["']/
          }]
        }]
      };
    };
  }();
  hljs.registerLanguage("go", e);
})(); /*! `shell` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var s = function () {
    "use strict";

    return function (s) {
      return {
        name: "Shell Session",
        aliases: ["console", "shellsession"],
        contains: [{
          className: "meta.prompt",
          begin: /^\s{0,3}[/~\w\d[\]()@-]*[>%$#][ ]?/,
          starts: {
            end: /[^\\](?=\s*$)/,
            subLanguage: "bash"
          }
        }]
      };
    };
  }();
  hljs.registerLanguage("shell", s);
})(); /*! `objectivec` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = /[a-zA-Z@][a-zA-Z0-9_]*/,
        _ = {
          $pattern: n,
          keyword: ["@interface", "@class", "@protocol", "@implementation"]
        };
      return {
        name: "Objective-C",
        aliases: ["mm", "objc", "obj-c", "obj-c++", "objective-c++"],
        keywords: {
          "variable.language": ["this", "super"],
          $pattern: n,
          keyword: ["while", "export", "sizeof", "typedef", "const", "struct", "for", "union", "volatile", "static", "mutable", "if", "do", "return", "goto", "enum", "else", "break", "extern", "asm", "case", "default", "register", "explicit", "typename", "switch", "continue", "inline", "readonly", "assign", "readwrite", "self", "@synchronized", "id", "typeof", "nonatomic", "IBOutlet", "IBAction", "strong", "weak", "copy", "in", "out", "inout", "bycopy", "byref", "oneway", "__strong", "__weak", "__block", "__autoreleasing", "@private", "@protected", "@public", "@try", "@property", "@end", "@throw", "@catch", "@finally", "@autoreleasepool", "@synthesize", "@dynamic", "@selector", "@optional", "@required", "@encode", "@package", "@import", "@defs", "@compatibility_alias", "__bridge", "__bridge_transfer", "__bridge_retained", "__bridge_retain", "__covariant", "__contravariant", "__kindof", "_Nonnull", "_Nullable", "_Null_unspecified", "__FUNCTION__", "__PRETTY_FUNCTION__", "__attribute__", "getter", "setter", "retain", "unsafe_unretained", "nonnull", "nullable", "null_unspecified", "null_resettable", "class", "instancetype", "NS_DESIGNATED_INITIALIZER", "NS_UNAVAILABLE", "NS_REQUIRES_SUPER", "NS_RETURNS_INNER_POINTER", "NS_INLINE", "NS_AVAILABLE", "NS_DEPRECATED", "NS_ENUM", "NS_OPTIONS", "NS_SWIFT_UNAVAILABLE", "NS_ASSUME_NONNULL_BEGIN", "NS_ASSUME_NONNULL_END", "NS_REFINED_FOR_SWIFT", "NS_SWIFT_NAME", "NS_SWIFT_NOTHROW", "NS_DURING", "NS_HANDLER", "NS_ENDHANDLER", "NS_VALUERETURN", "NS_VOIDRETURN"],
          literal: ["false", "true", "FALSE", "TRUE", "nil", "YES", "NO", "NULL"],
          built_in: ["dispatch_once_t", "dispatch_queue_t", "dispatch_sync", "dispatch_async", "dispatch_once"],
          type: ["int", "float", "char", "unsigned", "signed", "short", "long", "double", "wchar_t", "unichar", "void", "bool", "BOOL", "id|0", "_Bool"]
        },
        illegal: "</",
        contains: [{
          className: "built_in",
          begin: "\\b(AV|CA|CF|CG|CI|CL|CM|CN|CT|MK|MP|MTK|MTL|NS|SCN|SK|UI|WK|XC)\\w+"
        }, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE, e.C_NUMBER_MODE, e.QUOTE_STRING_MODE, e.APOS_STRING_MODE, {
          className: "string",
          variants: [{
            begin: '@"',
            end: '"',
            illegal: "\\n",
            contains: [e.BACKSLASH_ESCAPE]
          }]
        }, {
          className: "meta",
          begin: /#\s*[a-z]+\b/,
          end: /$/,
          keywords: {
            keyword: "if else elif endif define undef warning error line pragma ifdef ifndef include"
          },
          contains: [{
            begin: /\\\n/,
            relevance: 0
          }, e.inherit(e.QUOTE_STRING_MODE, {
            className: "string"
          }), {
            className: "string",
            begin: /<.*?>/,
            end: /$/,
            illegal: "\\n"
          }, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE]
        }, {
          className: "class",
          begin: "(" + _.keyword.join("|") + ")\\b",
          end: /(\{|$)/,
          excludeEnd: !0,
          keywords: _,
          contains: [e.UNDERSCORE_TITLE_MODE]
        }, {
          begin: "\\." + e.UNDERSCORE_IDENT_RE,
          relevance: 0
        }]
      };
    };
  }();
  hljs.registerLanguage("objectivec", e);
})(); /*! `python` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var n = e.regex,
        a = /(?:[A-Z_a-z\xAA\xB5\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037B-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0560-\u0588\u05D0-\u05EA\u05EF-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u0860-\u086A\u0870-\u0887\u0889-\u088E\u08A0-\u08C9\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u09FC\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C5D\u0C60\u0C61\u0C80\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D04-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D54-\u0D56\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E86-\u0E8A\u0E8C-\u0EA3\u0EA5\u0EA7-\u0EB0\u0EB2\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16EE-\u16F8\u1700-\u1711\u171F-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1878\u1880-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4C\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1C80-\u1C88\u1C90-\u1CBA\u1CBD-\u1CBF\u1CE9-\u1CEC\u1CEE-\u1CF3\u1CF5\u1CF6\u1CFA\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2118-\u211D\u2124\u2126\u2128\u212A-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2160-\u2188\u2C00-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u3005-\u3007\u3021-\u3029\u3031-\u3035\u3038-\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312F\u3131-\u318E\u31A0-\u31BF\u31F0-\u31FF\u3400-\u4DBF\u4E00-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6EF\uA717-\uA71F\uA722-\uA788\uA78B-\uA7CA\uA7D0\uA7D1\uA7D3\uA7D5-\uA7D9\uA7F2-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA8FE\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB69\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFC5D\uFC64-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDF9\uFE71\uFE73\uFE77\uFE79\uFE7B\uFE7D\uFE7F-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFF9D\uFFA0-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDD40-\uDD74\uDE80-\uDE9C\uDEA0-\uDED0\uDF00-\uDF1F\uDF2D-\uDF4A\uDF50-\uDF75\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF\uDFD1-\uDFD5]|\uD801[\uDC00-\uDC9D\uDCB0-\uDCD3\uDCD8-\uDCFB\uDD00-\uDD27\uDD30-\uDD63\uDD70-\uDD7A\uDD7C-\uDD8A\uDD8C-\uDD92\uDD94\uDD95\uDD97-\uDDA1\uDDA3-\uDDB1\uDDB3-\uDDB9\uDDBB\uDDBC\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67\uDF80-\uDF85\uDF87-\uDFB0\uDFB2-\uDFBA]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00\uDE10-\uDE13\uDE15-\uDE17\uDE19-\uDE35\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE4\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2\uDD00-\uDD23\uDE80-\uDEA9\uDEB0\uDEB1\uDF00-\uDF1C\uDF27\uDF30-\uDF45\uDF70-\uDF81\uDFB0-\uDFC4\uDFE0-\uDFF6]|\uD804[\uDC03-\uDC37\uDC71\uDC72\uDC75\uDC83-\uDCAF\uDCD0-\uDCE8\uDD03-\uDD26\uDD44\uDD47\uDD50-\uDD72\uDD76\uDD83-\uDDB2\uDDC1-\uDDC4\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE2B\uDE3F\uDE40\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEDE\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3D\uDF50\uDF5D-\uDF61]|\uD805[\uDC00-\uDC34\uDC47-\uDC4A\uDC5F-\uDC61\uDC80-\uDCAF\uDCC4\uDCC5\uDCC7\uDD80-\uDDAE\uDDD8-\uDDDB\uDE00-\uDE2F\uDE44\uDE80-\uDEAA\uDEB8\uDF00-\uDF1A\uDF40-\uDF46]|\uD806[\uDC00-\uDC2B\uDCA0-\uDCDF\uDCFF-\uDD06\uDD09\uDD0C-\uDD13\uDD15\uDD16\uDD18-\uDD2F\uDD3F\uDD41\uDDA0-\uDDA7\uDDAA-\uDDD0\uDDE1\uDDE3\uDE00\uDE0B-\uDE32\uDE3A\uDE50\uDE5C-\uDE89\uDE9D\uDEB0-\uDEF8]|\uD807[\uDC00-\uDC08\uDC0A-\uDC2E\uDC40\uDC72-\uDC8F\uDD00-\uDD06\uDD08\uDD09\uDD0B-\uDD30\uDD46\uDD60-\uDD65\uDD67\uDD68\uDD6A-\uDD89\uDD98\uDEE0-\uDEF2\uDF02\uDF04-\uDF10\uDF12-\uDF33\uDFB0]|\uD808[\uDC00-\uDF99]|\uD809[\uDC00-\uDC6E\uDC80-\uDD43]|\uD80B[\uDF90-\uDFF0]|[\uD80C\uD81C-\uD820\uD822\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872\uD874-\uD879\uD880-\uD883\uD885-\uD887][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2F\uDC41-\uDC46]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDE70-\uDEBE\uDED0-\uDEED\uDF00-\uDF2F\uDF40-\uDF43\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDE40-\uDE7F\uDF00-\uDF4A\uDF50\uDF93-\uDF9F\uDFE0\uDFE1\uDFE3]|\uD821[\uDC00-\uDFF7]|\uD823[\uDC00-\uDCD5\uDD00-\uDD08]|\uD82B[\uDFF0-\uDFF3\uDFF5-\uDFFB\uDFFD\uDFFE]|\uD82C[\uDC00-\uDD22\uDD32\uDD50-\uDD52\uDD55\uDD64-\uDD67\uDD70-\uDEFB]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB]|\uD837[\uDF00-\uDF1E\uDF25-\uDF2A]|\uD838[\uDC30-\uDC6D\uDD00-\uDD2C\uDD37-\uDD3D\uDD4E\uDE90-\uDEAD\uDEC0-\uDEEB]|\uD839[\uDCD0-\uDCEB\uDFE0-\uDFE6\uDFE8-\uDFEB\uDFED\uDFEE\uDFF0-\uDFFE]|\uD83A[\uDC00-\uDCC4\uDD00-\uDD43\uDD4B]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD869[\uDC00-\uDEDF\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF39\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1\uDEB0-\uDFFF]|\uD87A[\uDC00-\uDFE0]|\uD87E[\uDC00-\uDE1D]|\uD884[\uDC00-\uDF4A\uDF50-\uDFFF]|\uD888[\uDC00-\uDFAF])(?:[0-9A-Z_a-z\xAA\xB5\xB7\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0300-\u0374\u0376\u0377\u037B-\u037D\u037F\u0386-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u0483-\u0487\u048A-\u052F\u0531-\u0556\u0559\u0560-\u0588\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7\u05D0-\u05EA\u05EF-\u05F2\u0610-\u061A\u0620-\u0669\u066E-\u06D3\u06D5-\u06DC\u06DF-\u06E8\u06EA-\u06FC\u06FF\u0710-\u074A\u074D-\u07B1\u07C0-\u07F5\u07FA\u07FD\u0800-\u082D\u0840-\u085B\u0860-\u086A\u0870-\u0887\u0889-\u088E\u0898-\u08E1\u08E3-\u0963\u0966-\u096F\u0971-\u0983\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7\u09C8\u09CB-\u09CE\u09D7\u09DC\u09DD\u09DF-\u09E3\u09E6-\u09F1\u09FC\u09FE\u0A01-\u0A03\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A3C\u0A3E-\u0A42\u0A47\u0A48\u0A4B-\u0A4D\u0A51\u0A59-\u0A5C\u0A5E\u0A66-\u0A75\u0A81-\u0A83\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABC-\u0AC5\u0AC7-\u0AC9\u0ACB-\u0ACD\u0AD0\u0AE0-\u0AE3\u0AE6-\u0AEF\u0AF9-\u0AFF\u0B01-\u0B03\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3C-\u0B44\u0B47\u0B48\u0B4B-\u0B4D\u0B55-\u0B57\u0B5C\u0B5D\u0B5F-\u0B63\u0B66-\u0B6F\u0B71\u0B82\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BBE-\u0BC2\u0BC6-\u0BC8\u0BCA-\u0BCD\u0BD0\u0BD7\u0BE6-\u0BEF\u0C00-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3C-\u0C44\u0C46-\u0C48\u0C4A-\u0C4D\u0C55\u0C56\u0C58-\u0C5A\u0C5D\u0C60-\u0C63\u0C66-\u0C6F\u0C80-\u0C83\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBC-\u0CC4\u0CC6-\u0CC8\u0CCA-\u0CCD\u0CD5\u0CD6\u0CDD\u0CDE\u0CE0-\u0CE3\u0CE6-\u0CEF\u0CF1-\u0CF3\u0D00-\u0D0C\u0D0E-\u0D10\u0D12-\u0D44\u0D46-\u0D48\u0D4A-\u0D4E\u0D54-\u0D57\u0D5F-\u0D63\u0D66-\u0D6F\u0D7A-\u0D7F\u0D81-\u0D83\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0DCA\u0DCF-\u0DD4\u0DD6\u0DD8-\u0DDF\u0DE6-\u0DEF\u0DF2\u0DF3\u0E01-\u0E3A\u0E40-\u0E4E\u0E50-\u0E59\u0E81\u0E82\u0E84\u0E86-\u0E8A\u0E8C-\u0EA3\u0EA5\u0EA7-\u0EBD\u0EC0-\u0EC4\u0EC6\u0EC8-\u0ECE\u0ED0-\u0ED9\u0EDC-\u0EDF\u0F00\u0F18\u0F19\u0F20-\u0F29\u0F35\u0F37\u0F39\u0F3E-\u0F47\u0F49-\u0F6C\u0F71-\u0F84\u0F86-\u0F97\u0F99-\u0FBC\u0FC6\u1000-\u1049\u1050-\u109D\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u135D-\u135F\u1369-\u1371\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16EE-\u16F8\u1700-\u1715\u171F-\u1734\u1740-\u1753\u1760-\u176C\u176E-\u1770\u1772\u1773\u1780-\u17D3\u17D7\u17DC\u17DD\u17E0-\u17E9\u180B-\u180D\u180F-\u1819\u1820-\u1878\u1880-\u18AA\u18B0-\u18F5\u1900-\u191E\u1920-\u192B\u1930-\u193B\u1946-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u19D0-\u19DA\u1A00-\u1A1B\u1A20-\u1A5E\u1A60-\u1A7C\u1A7F-\u1A89\u1A90-\u1A99\u1AA7\u1AB0-\u1ABD\u1ABF-\u1ACE\u1B00-\u1B4C\u1B50-\u1B59\u1B6B-\u1B73\u1B80-\u1BF3\u1C00-\u1C37\u1C40-\u1C49\u1C4D-\u1C7D\u1C80-\u1C88\u1C90-\u1CBA\u1CBD-\u1CBF\u1CD0-\u1CD2\u1CD4-\u1CFA\u1D00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u203F\u2040\u2054\u2071\u207F\u2090-\u209C\u20D0-\u20DC\u20E1\u20E5-\u20F0\u2102\u2107\u210A-\u2113\u2115\u2118-\u211D\u2124\u2126\u2128\u212A-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2160-\u2188\u2C00-\u2CE4\u2CEB-\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D7F-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2DE0-\u2DFF\u3005-\u3007\u3021-\u302F\u3031-\u3035\u3038-\u303C\u3041-\u3096\u3099\u309A\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312F\u3131-\u318E\u31A0-\u31BF\u31F0-\u31FF\u3400-\u4DBF\u4E00-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA62B\uA640-\uA66F\uA674-\uA67D\uA67F-\uA6F1\uA717-\uA71F\uA722-\uA788\uA78B-\uA7CA\uA7D0\uA7D1\uA7D3\uA7D5-\uA7D9\uA7F2-\uA827\uA82C\uA840-\uA873\uA880-\uA8C5\uA8D0-\uA8D9\uA8E0-\uA8F7\uA8FB\uA8FD-\uA92D\uA930-\uA953\uA960-\uA97C\uA980-\uA9C0\uA9CF-\uA9D9\uA9E0-\uA9FE\uAA00-\uAA36\uAA40-\uAA4D\uAA50-\uAA59\uAA60-\uAA76\uAA7A-\uAAC2\uAADB-\uAADD\uAAE0-\uAAEF\uAAF2-\uAAF6\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB69\uAB70-\uABEA\uABEC\uABED\uABF0-\uABF9\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFC5D\uFC64-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDF9\uFE00-\uFE0F\uFE20-\uFE2F\uFE33\uFE34\uFE4D-\uFE4F\uFE71\uFE73\uFE77\uFE79\uFE7B\uFE7D\uFE7F-\uFEFC\uFF10-\uFF19\uFF21-\uFF3A\uFF3F\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDD40-\uDD74\uDDFD\uDE80-\uDE9C\uDEA0-\uDED0\uDEE0\uDF00-\uDF1F\uDF2D-\uDF4A\uDF50-\uDF7A\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF\uDFD1-\uDFD5]|\uD801[\uDC00-\uDC9D\uDCA0-\uDCA9\uDCB0-\uDCD3\uDCD8-\uDCFB\uDD00-\uDD27\uDD30-\uDD63\uDD70-\uDD7A\uDD7C-\uDD8A\uDD8C-\uDD92\uDD94\uDD95\uDD97-\uDDA1\uDDA3-\uDDB1\uDDB3-\uDDB9\uDDBB\uDDBC\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67\uDF80-\uDF85\uDF87-\uDFB0\uDFB2-\uDFBA]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00-\uDE03\uDE05\uDE06\uDE0C-\uDE13\uDE15-\uDE17\uDE19-\uDE35\uDE38-\uDE3A\uDE3F\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE6\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2\uDD00-\uDD27\uDD30-\uDD39\uDE80-\uDEA9\uDEAB\uDEAC\uDEB0\uDEB1\uDEFD-\uDF1C\uDF27\uDF30-\uDF50\uDF70-\uDF85\uDFB0-\uDFC4\uDFE0-\uDFF6]|\uD804[\uDC00-\uDC46\uDC66-\uDC75\uDC7F-\uDCBA\uDCC2\uDCD0-\uDCE8\uDCF0-\uDCF9\uDD00-\uDD34\uDD36-\uDD3F\uDD44-\uDD47\uDD50-\uDD73\uDD76\uDD80-\uDDC4\uDDC9-\uDDCC\uDDCE-\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE37\uDE3E-\uDE41\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEEA\uDEF0-\uDEF9\uDF00-\uDF03\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3B-\uDF44\uDF47\uDF48\uDF4B-\uDF4D\uDF50\uDF57\uDF5D-\uDF63\uDF66-\uDF6C\uDF70-\uDF74]|\uD805[\uDC00-\uDC4A\uDC50-\uDC59\uDC5E-\uDC61\uDC80-\uDCC5\uDCC7\uDCD0-\uDCD9\uDD80-\uDDB5\uDDB8-\uDDC0\uDDD8-\uDDDD\uDE00-\uDE40\uDE44\uDE50-\uDE59\uDE80-\uDEB8\uDEC0-\uDEC9\uDF00-\uDF1A\uDF1D-\uDF2B\uDF30-\uDF39\uDF40-\uDF46]|\uD806[\uDC00-\uDC3A\uDCA0-\uDCE9\uDCFF-\uDD06\uDD09\uDD0C-\uDD13\uDD15\uDD16\uDD18-\uDD35\uDD37\uDD38\uDD3B-\uDD43\uDD50-\uDD59\uDDA0-\uDDA7\uDDAA-\uDDD7\uDDDA-\uDDE1\uDDE3\uDDE4\uDE00-\uDE3E\uDE47\uDE50-\uDE99\uDE9D\uDEB0-\uDEF8]|\uD807[\uDC00-\uDC08\uDC0A-\uDC36\uDC38-\uDC40\uDC50-\uDC59\uDC72-\uDC8F\uDC92-\uDCA7\uDCA9-\uDCB6\uDD00-\uDD06\uDD08\uDD09\uDD0B-\uDD36\uDD3A\uDD3C\uDD3D\uDD3F-\uDD47\uDD50-\uDD59\uDD60-\uDD65\uDD67\uDD68\uDD6A-\uDD8E\uDD90\uDD91\uDD93-\uDD98\uDDA0-\uDDA9\uDEE0-\uDEF6\uDF00-\uDF10\uDF12-\uDF3A\uDF3E-\uDF42\uDF50-\uDF59\uDFB0]|\uD808[\uDC00-\uDF99]|\uD809[\uDC00-\uDC6E\uDC80-\uDD43]|\uD80B[\uDF90-\uDFF0]|[\uD80C\uD81C-\uD820\uD822\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872\uD874-\uD879\uD880-\uD883\uD885-\uD887][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2F\uDC40-\uDC55]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDE60-\uDE69\uDE70-\uDEBE\uDEC0-\uDEC9\uDED0-\uDEED\uDEF0-\uDEF4\uDF00-\uDF36\uDF40-\uDF43\uDF50-\uDF59\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDE40-\uDE7F\uDF00-\uDF4A\uDF4F-\uDF87\uDF8F-\uDF9F\uDFE0\uDFE1\uDFE3\uDFE4\uDFF0\uDFF1]|\uD821[\uDC00-\uDFF7]|\uD823[\uDC00-\uDCD5\uDD00-\uDD08]|\uD82B[\uDFF0-\uDFF3\uDFF5-\uDFFB\uDFFD\uDFFE]|\uD82C[\uDC00-\uDD22\uDD32\uDD50-\uDD52\uDD55\uDD64-\uDD67\uDD70-\uDEFB]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99\uDC9D\uDC9E]|\uD833[\uDF00-\uDF2D\uDF30-\uDF46]|\uD834[\uDD65-\uDD69\uDD6D-\uDD72\uDD7B-\uDD82\uDD85-\uDD8B\uDDAA-\uDDAD\uDE42-\uDE44]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB\uDFCE-\uDFFF]|\uD836[\uDE00-\uDE36\uDE3B-\uDE6C\uDE75\uDE84\uDE9B-\uDE9F\uDEA1-\uDEAF]|\uD837[\uDF00-\uDF1E\uDF25-\uDF2A]|\uD838[\uDC00-\uDC06\uDC08-\uDC18\uDC1B-\uDC21\uDC23\uDC24\uDC26-\uDC2A\uDC30-\uDC6D\uDC8F\uDD00-\uDD2C\uDD30-\uDD3D\uDD40-\uDD49\uDD4E\uDE90-\uDEAE\uDEC0-\uDEF9]|\uD839[\uDCD0-\uDCF9\uDFE0-\uDFE6\uDFE8-\uDFEB\uDFED\uDFEE\uDFF0-\uDFFE]|\uD83A[\uDC00-\uDCC4\uDCD0-\uDCD6\uDD00-\uDD4B\uDD50-\uDD59]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD83E[\uDFF0-\uDFF9]|\uD869[\uDC00-\uDEDF\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF39\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1\uDEB0-\uDFFF]|\uD87A[\uDC00-\uDFE0]|\uD87E[\uDC00-\uDE1D]|\uD884[\uDC00-\uDF4A\uDF50-\uDFFF]|\uD888[\uDC00-\uDFAF]|\uDB40[\uDD00-\uDDEF])*/,
        i = ["and", "as", "assert", "async", "await", "break", "case", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "match", "nonlocal|10", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"],
        s = {
          $pattern: /[A-Za-z]\w+|__\w+__/,
          keyword: i,
          built_in: ["__import__", "abs", "all", "any", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip"],
          literal: ["__debug__", "Ellipsis", "False", "None", "NotImplemented", "True"],
          type: ["Any", "Callable", "Coroutine", "Dict", "List", "Literal", "Generic", "Optional", "Sequence", "Set", "Tuple", "Type", "Union"]
        },
        t = {
          className: "meta",
          begin: /^(>>>|\.\.\.) /
        },
        r = {
          className: "subst",
          begin: /\{/,
          end: /\}/,
          keywords: s,
          illegal: /#/
        },
        l = {
          begin: /\{\{/,
          relevance: 0
        },
        b = {
          className: "string",
          contains: [e.BACKSLASH_ESCAPE],
          variants: [{
            begin: /([uU]|[bB]|[rR]|[bB][rR]|[rR][bB])?'''/,
            end: /'''/,
            contains: [e.BACKSLASH_ESCAPE, t],
            relevance: 10
          }, {
            begin: /([uU]|[bB]|[rR]|[bB][rR]|[rR][bB])?"""/,
            end: /"""/,
            contains: [e.BACKSLASH_ESCAPE, t],
            relevance: 10
          }, {
            begin: /([fF][rR]|[rR][fF]|[fF])'''/,
            end: /'''/,
            contains: [e.BACKSLASH_ESCAPE, t, l, r]
          }, {
            begin: /([fF][rR]|[rR][fF]|[fF])"""/,
            end: /"""/,
            contains: [e.BACKSLASH_ESCAPE, t, l, r]
          }, {
            begin: /([uU]|[rR])'/,
            end: /'/,
            relevance: 10
          }, {
            begin: /([uU]|[rR])"/,
            end: /"/,
            relevance: 10
          }, {
            begin: /([bB]|[bB][rR]|[rR][bB])'/,
            end: /'/
          }, {
            begin: /([bB]|[bB][rR]|[rR][bB])"/,
            end: /"/
          }, {
            begin: /([fF][rR]|[rR][fF]|[fF])'/,
            end: /'/,
            contains: [e.BACKSLASH_ESCAPE, l, r]
          }, {
            begin: /([fF][rR]|[rR][fF]|[fF])"/,
            end: /"/,
            contains: [e.BACKSLASH_ESCAPE, l, r]
          }, e.APOS_STRING_MODE, e.QUOTE_STRING_MODE]
        },
        o = "[0-9](_?[0-9])*",
        c = "(\\b(".concat(o, "))?\\.(").concat(o, ")|\\b(").concat(o, ")\\."),
        d = "\\b|" + i.join("|"),
        g = {
          className: "number",
          relevance: 0,
          variants: [{
            begin: "(\\b(".concat(o, ")|(").concat(c, "))[eE][+-]?(").concat(o, ")[jJ]?(?=").concat(d, ")")
          }, {
            begin: "(".concat(c, ")[jJ]?")
          }, {
            begin: "\\b([1-9](_?[0-9])*|0+(_?0)*)[lLjJ]?(?=".concat(d, ")")
          }, {
            begin: "\\b0[bB](_?[01])+[lL]?(?=".concat(d, ")")
          }, {
            begin: "\\b0[oO](_?[0-7])+[lL]?(?=".concat(d, ")")
          }, {
            begin: "\\b0[xX](_?[0-9a-fA-F])+[lL]?(?=".concat(d, ")")
          }, {
            begin: "\\b(".concat(o, ")[jJ](?=").concat(d, ")")
          }]
        },
        p = {
          className: "comment",
          begin: n.lookahead(/# type:/),
          end: /$/,
          keywords: s,
          contains: [{
            begin: /# type:/
          }, {
            begin: /#/,
            end: /\b\B/,
            endsWithParent: !0
          }]
        },
        m = {
          className: "params",
          variants: [{
            className: "",
            begin: /\(\s*\)/,
            skip: !0
          }, {
            begin: /\(/,
            end: /\)/,
            excludeBegin: !0,
            excludeEnd: !0,
            keywords: s,
            contains: ["self", t, g, b, e.HASH_COMMENT_MODE]
          }]
        };
      return r.contains = [b, g, t], {
        name: "Python",
        aliases: ["py", "gyp", "ipython"],
        unicodeRegex: !0,
        keywords: s,
        illegal: /(<\/|->|\?)|=>/,
        contains: [t, g, {
          begin: /\bself\b/
        }, {
          beginKeywords: "if",
          relevance: 0
        }, b, p, e.HASH_COMMENT_MODE, {
          match: [/\bdef/, /\s+/, a],
          scope: {
            1: "keyword",
            3: "title.function"
          },
          contains: [m]
        }, {
          variants: [{
            match: [/\bclass/, /\s+/, a, /\s*/, /\(\s*/, a, /\s*\)/]
          }, {
            match: [/\bclass/, /\s+/, a]
          }],
          scope: {
            1: "keyword",
            3: "title.class",
            6: "title.class.inherited"
          }
        }, {
          className: "meta",
          begin: /^[\t ]*@/,
          end: /(?=#)|$/,
          contains: [g, m, b]
        }]
      };
    };
  }();
  hljs.registerLanguage("python", e);
})(); /*! `lua` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var t = "\\[=*\\[",
        a = "\\]=*\\]",
        n = {
          begin: t,
          end: a,
          contains: ["self"]
        },
        o = [e.COMMENT("--(?!\\[=*\\[)", "$"), e.COMMENT("--\\[=*\\[", a, {
          contains: [n],
          relevance: 10
        })];
      return {
        name: "Lua",
        keywords: {
          $pattern: e.UNDERSCORE_IDENT_RE,
          literal: "true false nil",
          keyword: "and break do else elseif end for goto if in local not or repeat return then until while",
          built_in: "_G _ENV _VERSION __index __newindex __mode __call __metatable __tostring __len __gc __add __sub __mul __div __mod __pow __concat __unm __eq __lt __le assert collectgarbage dofile error getfenv getmetatable ipairs load loadfile loadstring module next pairs pcall print rawequal rawget rawset require select setfenv setmetatable tonumber tostring type unpack xpcall arg self coroutine resume yield status wrap create running debug getupvalue debug sethook getmetatable gethook setmetatable setlocal traceback setfenv getinfo setupvalue getlocal getregistry getfenv io lines write close flush open output type read stderr stdin input stdout popen tmpfile math log max acos huge ldexp pi cos tanh pow deg tan cosh sinh random randomseed frexp ceil floor rad abs sqrt modf asin min mod fmod log10 atan2 exp sin atan os exit setlocale date getenv difftime remove time clock tmpname rename execute package preload loadlib loaded loaders cpath config path seeall string sub upper len gfind rep find match char dump gmatch reverse byte format gsub lower table setn insert getn foreachi maxn foreach concat sort remove"
        },
        contains: o.concat([{
          className: "function",
          beginKeywords: "function",
          end: "\\)",
          contains: [e.inherit(e.TITLE_MODE, {
            begin: "([_a-zA-Z]\\w*\\.)*([_a-zA-Z]\\w*:)?[_a-zA-Z]\\w*"
          }), {
            className: "params",
            begin: "\\(",
            endsWithParent: !0,
            contains: o
          }].concat(o)
        }, e.C_NUMBER_MODE, e.APOS_STRING_MODE, e.QUOTE_STRING_MODE, {
          className: "string",
          begin: t,
          end: a,
          contains: [n],
          relevance: 5
        }])
      };
    };
  }();
  hljs.registerLanguage("lua", e);
})(); /*! `json` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var a = ["true", "false", "null"],
        n = {
          scope: "literal",
          beginKeywords: a.join(" ")
        };
      return {
        name: "JSON",
        keywords: {
          literal: a
        },
        contains: [{
          className: "attr",
          begin: /"(\\.|[^\\"\r\n])*"(?=\s*:)/,
          relevance: 1.01
        }, {
          match: /[{}[\],:]/,
          className: "punctuation",
          relevance: 0
        }, e.QUOTE_STRING_MODE, n, e.C_NUMBER_MODE, e.C_LINE_COMMENT_MODE, e.C_BLOCK_COMMENT_MODE],
        illegal: "\\S"
      };
    };
  }();
  hljs.registerLanguage("json", e);
})(); /*! `diff` grammar compiled for Highlight.js 11.7.0 */
(function () {
  var e = function () {
    "use strict";

    return function (e) {
      var a = e.regex;
      return {
        name: "Diff",
        aliases: ["patch"],
        contains: [{
          className: "meta",
          relevance: 10,
          match: a.either(/^@@ +-\d+,\d+ +\+\d+,\d+ +@@/, /^\*\*\* +\d+,\d+ +\*\*\*\*$/, /^--- +\d+,\d+ +----$/)
        }, {
          className: "comment",
          variants: [{
            begin: a.either(/Index: /, /^index/, /={3,}/, /^-{3}/, /^\*{3} /, /^\+{3}/, /^diff --git/),
            end: /$/
          }, {
            match: /^\*{15}$/
          }]
        }, {
          className: "addition",
          begin: /^\+/,
          end: /$/
        }, {
          className: "deletion",
          begin: /^-/,
          end: /$/
        }, {
          className: "addition",
          begin: /^!/,
          end: /$/
        }]
      };
    };
  }();
  hljs.registerLanguage("diff", e);
})();
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (hljs);

/***/ })

}]);
//# sourceMappingURL=hljs.js.map