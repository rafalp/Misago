import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import { TabsNav } from 'misago/components/threads/navs'; // jshint ignore:line

export default class extends React.Component {
  getClassName() {
    if (this.props.route.lists.length > 1) {
      return 'page-header tabbed';
    } else {
      return 'page-header';
    }
  }

  getGoBackButton() {
    if (this.props.route.category.parent) {
      /* jshint ignore:start */
      return <Link className="btn btn-default btn-aligned btn-icon btn-go-back pull-left"
                   to={this.props.route.category.parent.absolute_url + this.props.route.list.path}>
        <span className="material-icon">
          keyboard_arrow_left
        </span>
      </Link>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getCompactNavToggle() {
    if (this.props.route.lists.length > 1) {
      /* jshint ignore:start */
      return <DropdownToggle toggleNav={this.props.toggleNav}
                             dropdown={this.props.dropdown} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getTabsNav() {
    if (this.props.route.lists.length > 1) {
      /* jshint ignore:start */
      return <TabsNav baseUrl={this.props.route.category.absolute_url}
                      list={this.props.route.list}
                      lists={this.props.route.lists} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className="container">
        {this.getGoBackButton()}
        <h1 className="pull-left">{this.props.title}</h1>
        {this.getCompactNavToggle()}
      </div>

      {this.getTabsNav()}

    </div>;
    /* jshint ignore:end */
  }
}