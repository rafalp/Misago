// jshint ignore:start
import React from 'react';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import misago from 'misago';
import cleanResults from './clean-results';
import Input from './input';
import Dropdown from './dropdown';

export default class extends React.Component {
  constructor() {
    super();

    this.state = {
      isLoading: false,
      isOpen: false,
      query: '',
      results: []
    };

    this.intervalId = null;
  }

  componentDidMount() {
    document.addEventListener('mousedown', this.onDocumentMouseDown);
    document.addEventListener('keydown', this.onEscape);
  }

  componentWillUnmount() {
    document.removeEventListener('mousedown', this.onDocumentMouseDown);
    document.removeEventListener('keydown', this.onEscape);
  }

  onFocus = (ev) => {
    this.setState({ isOpen: true });
  };

  onDocumentMouseDown = (ev) => {
    let closeResults = true;
    let node = ev.target;

    while (node !== null && node !== document) {
      if (node === this.container) {
        closeResults = false;
        return;
      }

      node = node.parentNode;
    }

    if (closeResults) {
      this.setState({ isOpen: false });
    }
  };

  onEscape = (ev) => {
    if (ev.key === 'Escape') {
      this.setState({ isOpen: false });
    }
  };

  onChange = (ev) => {
    const query = ev.target.value;

    this.setState({ query });
    this.loadResults(query.trim());
  };

  loadResults(query) {
    if (!query.length) return;

    const delay = 300 + (Math.random() * 300);

    if (this.intervalId) {
      window.clearTimeout(this.intervalId);
    }

    this.setState({ isLoading: true });

    this.intervalId = window.setTimeout(
      () => {
        ajax.get(misago.get('SEARCH_API'), {q: query}).then(
          (data) => {
            this.setState({
              intervalId: null,
              isLoading: false,
              results: cleanResults(data)
            });
          },
          (rejection) => {
            snackbar.apiError(rejection);

            this.setState({
              intervalId: null,
              isLoading: false,
              results: []
            });
          }
        );
      },
      delay
    );
  }

  render() {
    let className = "navbar-right navbar-search dropdown";
    if (this.state.isOpen) className += " open";

    return (
      <div className="navbar-form" ref={(container) => this.container = container}>
        <div className={className}>
          <div className="form-group">
            <Input
              value={this.state.query}
              onChange={this.onChange}
              onFocus={this.onFocus}
            />
          </div>
          <Dropdown
            isLoading={this.state.isLoading}
            results={this.state.results}
            query={this.state.query}
          />
        </div>
      </div>
    );
  }
}