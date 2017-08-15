// jshint ignore:start
import React from 'react';
import ajax from 'misago/services/ajax';
import misago from 'misago';
import cleanResults from './clean-results';
import Input from './input';

export default class extends React.Component {
  constructor() {
    super();

    this.state = {
      isLoading: false,
      isOpen: false,
      query: '',
      results: []
    };
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

    ajax.get(misago.get('SEARCH_API'), {q: query}).then(
      (data) => {
        this.setState({
          isLoading: false,
          results: cleanResults(data)
        });
      },
      (rejection) => {
        this.setState({ isLoading: false });
        console.log(rejection);
      }
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
          <ul className="dropdown-menu dropdown-search-results" role="menu">
            <li>
              <a href="/">
                HELLO!
              </a>
            </li>
          </ul>
        </div>
      </div>
    );
  }
}