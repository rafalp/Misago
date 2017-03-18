import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import { CompactNav, TabsNav } from 'misago/components/threads/navs'; // jshint ignore:line
import { read } from 'misago/reducers/threads'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import posting from 'misago/services/posting'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line
import misago from 'misago'; // jshint ignore:line

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
      store.dispatch(read(this.props.route.categoriesMap, this.props.route.category));

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
    posting.open(this.props.startThread || {
      mode: 'START',

      config: misago.get('THREAD_EDITOR_API'),
      submit: misago.get('THREADS_API'),

      category: this.props.route.category.id
    });
  };
  /* jshint ignore:end */

  hasGoBackButton() {
    return !!this.props.route.category.parent;
  }

  getGoBackButton() {
    if (!this.props.route.category.parent) return null;

    /* jshint ignore:start */
    const parent = this.props.categories[this.props.route.category.parent];

    return (
      <div className="hidden-xs col-sm-2 col-lg-1">
        <Link
          className="btn btn-default btn-icon btn-aligned btn-go-back btn-block"
          to={parent.absolute_url + this.props.route.list.path}
        >
          <span className="material-icon">
            keyboard_arrow_left
          </span>
        </Link>
      </div>
    );
    /* jshint ignore:end */
  }

  getStartThreadButton() {
    if (!this.props.user.id) return null;

    /* jshint ignore:start */
    return (
      <div className="col-xs-6 col-sm-4 col-md-6">
        <Button
          className="btn-success btn-block"
          onClick={this.startThread}
          disabled={this.props.disabled}
        >
          <span className="material-icon">
            chat
          </span>
          {gettext("Start thread")}
        </Button>
      </div>
    );
    /* jshint ignore:end */
  }

  getMarkAsReadButton() {
    if (!this.props.user.id) return null;

    /* jshint ignore:start */
    return (
      <div className="col-xs-6 col-sm-4 col-md-6">
        <Button
          className="btn-default btn-block"
          onClick={this.markAsRead}
          loading={this.state.isBusy}
          disabled={this.props.disabled}
        >
          <span className="material-icon">
            playlist_add_check
          </span>
          {gettext("Mark as read")}
        </Button>
      </div>
    );
    /* jshint ignore:end */
  }

  getTabsNav() {
    if (this.props.route.lists.length > 1) {
      /* jshint ignore:start */
      return (
        <TabsNav
          baseUrl={this.props.route.category.absolute_url}
          list={this.props.route.list}
          lists={this.props.route.lists}
        />
      );
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getCompactNav() {
    if (this.props.route.lists.length > 1) {
      /* jshint ignore:start */
      return (
        <CompactNav
          baseUrl={this.props.route.category.absolute_url}
          list={this.props.route.list}
          lists={this.props.route.lists}
        />
      );
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
    let headerClassName = 'col-xs-12';
    if (this.hasGoBackButton()) {
      headerClassName += ' col-sm-10 col-lg-11';
    }

    const isAuthenticated = !!this.props.user.id;

    return (
      <div className={this.getClassName()}>
        <div className="container">
          <div className="row">
            <div className={isAuthenticated ? "col-md-8" : "col-xs-12"}>
              <div className="row">
                {this.getGoBackButton()}
                <div className={headerClassName}>
                  <ParentCategory
                    categories={this.props.categories}
                    category={this.props.route.category.parent}
                  />
                  <h1>{this.props.title}</h1>
                </div>
              </div>
            </div>
            {isAuthenticated && (
              <div className="col-md-4">
                <div className="row xs-margin-top-half sm-margin-top-half">
                  <div className="col-sm-4 visible-sm-block">
                    {this.getCompactNav()}
                  </div>
                  {this.getMarkAsReadButton()}
                  {this.getStartThreadButton()}
                </div>
              </div>
            )}
          </div>
        </div>

        {this.getTabsNav()}

        {isAuthenticated && (
          <div className="container xs-margin-top hidden-sm hidden-md hidden-lg">
            {this.getCompactNav()}
          </div>
        )}

      </div>
    );
    /* jshint ignore:end */
  }
}

/* jshint ignore:start */
export function ParentCategory(props) {
  const { categories, category } = props;
  if (!category) return null;

  const parent = categories[category];

  return (
    <Link
      className="go-back-sm visible-xs-block"
      to={parent.absolute_url}
    >
      <span className="material-icon">
        chevron_left
      </span>
      {parent.parent ? parent.name : gettext("Threads")}
    </Link>
  );
}
/* jshint ignore:end */