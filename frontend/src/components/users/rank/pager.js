import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import resetScroll from 'misago/utils/reset-scroll'; // jshint ignore:line

export default class extends React.Component {
  getPreviousPage() {
    if (this.props.previous || this.props.first) {
      /* jshint ignore:start */
      let url = this.props.baseUrl;
      if (this.props.previous) {
        url += this.props.previous + '/';
      }

      return <li className="previous">
        <Link to={url} onClick={resetScroll}>
          <span aria-hidden="true" className="material-icon">
            arrow_back
          </span>
        </Link>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getNextPage() {
    if (this.props.next) {
      /* jshint ignore:start */
      let url = this.props.baseUrl + this.props.next + '/';
      return <li className="next">
        <Link to={url} onClick={resetScroll}>
          <span aria-hidden="true" className="material-icon">
            arrow_forward
          </span>
        </Link>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="pager-undercontent">
      <nav>
        <ul className="pager">
          {this.getPreviousPage()}
          {this.getNextPage()}
        </ul>
      </nav>
    </div>;
    /* jshint ignore:end */
  }
}