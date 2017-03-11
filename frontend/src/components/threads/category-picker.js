import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line

export class Subcategory extends React.Component {
  getUrl() {
    if (this.props.listPath) {
      return this.props.category.absolute_url + this.props.listPath;
    } else {
      return this.props.category.absolute_url;
    }
  }

  render() {
    /* jshint ignore:start */
    return <li>
      <Link to={this.getUrl()} className="btn btn-link">
        {this.props.category.name}
      </Link>
    </li>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="dropdown category-picker">
      <button type="button"
              className="btn btn-default btn-icon dropdown-toggle btn-block"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false">
        <span className="material-icon">
          expand_more
        </span>
        <span className="hidden-xs">{' ' + gettext("Go to")}</span>
      </button>
      <ul className="dropdown-menu categories-menu">
        {this.props.choices.map((id) => {
          if (this.props.categories[id]) {
            return <Subcategory category={this.props.categories[id]}
                                listPath={this.props.list.path}
                                key={id} />;
          } else {
            return null;
          }
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}