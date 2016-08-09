import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom';
import PostingComponent from 'misago/components/posting'; // jshint ignore:line
import mount from 'misago/utils/mount-component'; // jshint ignore:line

export class Posting {
  init(ajax, snackbar, placeholder) {
    this._ajax = ajax;
    this._snackbar = snackbar;
    this._placeholder = $(placeholder);

    this._isOpen = false;
    this._isClosing = false;
  }

  open(options) {
    if (!this._isOpen) {
      this._isOpen = true;
      this._realOpen(options);
    }
  }

  // jshint ignore:start
  _realOpen(options) {
    mount(
      <PostingComponent options={options} />,
      'posting-mount'
    );

    this._placeholder.addClass('in');
  }
  // jshint ignore:end

  close() {
    if (this._isOpen && !this._isClosing) {
      this._isClosing = true;
      this._placeholder.removeClass('in');

      window.setTimeout(() => {
        ReactDOM.render(null, document.getElementById('posting-mount'));
        this._isClosing = false;
        this._isOpen = false;
      }, 300);
    }
  }
}

export default new Posting();
