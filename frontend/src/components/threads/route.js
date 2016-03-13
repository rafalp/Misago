import React from 'react'; // jshint ignore:line
import Header from 'misago/components/threads/header'; // jshint ignore:line
import { CompactNav } from 'misago/components/threads/navs'; // jshint ignore:line
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
      <Header title={this.getTitle()}
              route={this.props.route}
              dropdown={this.state.dropdown}
              toggleNav={this.toggleNav}
              hideNav={this.hideNav} />
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