import React from 'react'; // jshint ignore:line
import { Link } from 'react-router'; // jshint ignore:line
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import { TabsNav, CompactNav } from 'misago/components/threads/navs'; // jshint ignore:line
import { getPageTitle, getTitle } from 'misago/components/threads/title-utils';
import ThreadsList from 'misago/components/threads-list/root'; // jshint ignore:line
import WithDropdown from 'misago/components/with-dropdown';
import title from 'misago/services/page-title';

export default class extends WithDropdown {
  componentDidMount() {
    title.set(getPageTitle(this.props.route));
  }

  getTitle() {
    return getTitle(this.props.route);
  }

  getClassName() {
    let className = 'page page-threads';
    className += ' page-threads-' + this.props.route.list;
    if (this.props.route.category.css_class) {
      className += ' page-' + this.props.route.category.css_class;
    }
    return className;
  }

  getHeaderClassName() {
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

  getTabsNav() {
    if (this.props.route.lists.length > 1) {
      /* jshint ignore:start */
      return <TabsNav baseUrl={this.props.route.category.absolute_url}
                      list={this.props.route.list}
                      lists={this.props.route.lists}
                      hideNav={this.hideNav} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getCompactNavToggle() {
    if (this.props.route.lists.length > 1) {
      /* jshint ignore:start */
      return <DropdownToggle toggleNav={this.toggleNav}
                             dropdown={this.state.dropdown} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getCompactNav() {
    if (this.props.route.lists.length > 1) {
      /* jshint ignore:start */
      return <CompactNav baseUrl={this.props.route.category.absolute_url}
                         list={this.props.route.list}
                         lists={this.props.route.lists}
                         hideNav={this.hideNav} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className={this.getHeaderClassName()}>
        <div className="container">
          {this.getGoBackButton()}
          <h1 className="pull-left">{this.getTitle()}</h1>
          {this.getCompactNavToggle()}
        </div>

        {this.getTabsNav()}

      </div>
      <div className={this.getCompactNavClassName()}>
        {this.getCompactNav()}
      </div>
      <div className="container">

        <ThreadsList />

      </div>
    </div>;
    /* jshint ignore:end */
  }
}