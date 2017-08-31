// jshint ignore:start
import React from 'react';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import misago from 'misago';
import cleanResults from './clean-results';
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

  onToggle = (ev) => {
    this.setState((prevState, props) => {
      return { isOpen: !prevState.isOpen };
    });
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
          <a
            aria-haspopup="true"
            aria-expanded="false"
            className="btn navbar-btn dropdown-toggle"
            data-toggle="dropdown"
            href={misago.get('SEARCH_URL')}
            onClick={this.onToggle}
          >
            <i className="material-icon">
              search
            </i>
          </a>
          <Dropdown
            isLoading={this.state.isLoading}
            onChange={this.onChange}
            results={this.state.results}
            query={this.state.query}
          />
        </div>
      </div>
    );
  }
}