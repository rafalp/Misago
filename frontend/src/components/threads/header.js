import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import { TabsNav } from 'misago/components/threads/navs'; // jshint ignore:line
import { read } from 'misago/reducers/threads'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isBusy: false
    };
  }

  /* jshint ignore:start */
  markAsRead = () => {
    this.setState({
      isBusy: true
    });

    ajax.post(this.props.route.category.api_url.read).then(() => {
      store.dispatch(read());

      this.setState({
        isBusy: false
      });

      snackbar.success(gettext("Threads have been marked as read."));
    }, (rejection) => {
      this.setState({
        isBusy: false
      });

      snackbar.apiError(rejection);
    });
  };

  startThread = () => {
    console.log('TODO: Start thread form!');
  };
  /* jshint ignore:end */

  getGoBackButton() {
    if (this.props.route.category.parent) {
      /* jshint ignore:start */
      const parent = this.props.categories[this.props.route.category.parent];

      return <Link className="btn btn-default btn-aligned btn-icon btn-go-back pull-left"
                   to={parent.absolute_url + this.props.route.list.path}>
        <span className="material-icon">
          keyboard_arrow_left
        </span>
      </Link>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getStartThreadButton() {
    if (this.props.user.id) {
      /* jshint ignore:start */
      return <Button className="btn btn-success btn-aligned hidden-xs hidden-sm"
                     onClick={this.startThread}
                     disabled={this.props.disabled}>
        <span className="material-icon">
          chat
        </span>
        {gettext("Start thread")}
      </Button>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getMarkAsReadButton() {
    if (this.props.user.id) {
      /* jshint ignore:start */
      return <Button className="btn btn-default btn-aligned hidden-xs hidden-sm"
                     onClick={this.markAsRead}
                     loading={this.state.isBusy}
                     disabled={this.props.disabled}>
        <span className="material-icon">
          playlist_add_check
        </span>
        {gettext("Mark as read")}
      </Button>;
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

  getClassName() {
    if (this.props.route.lists.length > 1) {
      return 'page-header tabbed';
    } else {
      return 'page-header';
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className="container">
        {this.getGoBackButton()}
        <h1 className="pull-left">{this.props.title}</h1>

        {this.getStartThreadButton()}
        {this.getMarkAsReadButton()}
        {this.getCompactNavToggle()}
      </div>

      {this.getTabsNav()}

    </div>;
    /* jshint ignore:end */
  }
}