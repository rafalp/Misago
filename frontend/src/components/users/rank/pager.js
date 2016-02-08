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

  getProgessBar() {
    /* jshint ignore:start */
    return <ul className="pager-progress-bar">
      {this.props.page_range.map((page) => {
        let className = page === this.props.page ? 'active' : null;
        let url = this.props.baseUrl;

        if (page > 1) {
          url += page + '/';
        }

        return <li key={page} className={className}>
          <Link to={url} onClick={resetScroll}>
            {page}
          </Link>
        </li>;
      })}
    </ul>;
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return <div className="pager-undercontent">
      <nav>
        <ul className="pager">
          {this.getPreviousPage()}
          {this.getNextPage()}
        </ul>
        {this.getProgessBar()}
      </nav>
    </div>;
    /* jshint ignore:end */
  }
}