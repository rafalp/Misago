import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import Nav from 'misago/components/threads/nav'; // jshint ignore:line
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
          className="btn btn-default btn-icon btn-aligned btn-go-back btn-block btn-outline"
          to={parent.url.index + this.props.route.list.path}
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
      <Button
        className="btn-primary btn-block btn-outline"
        onClick={this.startThread}
        disabled={this.props.disabled}
      >
        <span className="material-icon">
          chat
        </span>
        {gettext("Start thread")}
      </Button>
    );
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    let headerClassName = 'col-xs-12';
    if (this.hasGoBackButton()) {
      headerClassName += ' col-sm-10 col-lg-11 sm-align-row-buttons';
    }

    const isAuthenticated = !!this.props.user.id;

    return (
      <div className="page-header-bg">
        <div className="page-header">
          <div className="container">
            <div className="row">
              <div className={isAuthenticated ? "col-sm-9 col-md-10" : "col-xs-12"}>
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
                <div className="col-sm-3 col-md-2 xs-margin-top">
                  {this.getStartThreadButton()}
                </div>
              )}
            </div>
          </div>

          <Nav
            baseUrl={this.props.route.category.url.index}
            list={this.props.route.list}
            lists={this.props.route.lists}
          />

        </div>
      </div>
    );
    /* jshint ignore:end */
  }
}

/* jshint ignore:start */
export function ParentCategory({ categories, category }) {
  if (!category) return null;

  const parent = categories[category];

  return (
    <Link
      className="go-back-sm visible-xs-block"
      to={parent.url.index}
    >
      <span className="material-icon">
        chevron_left
      </span>
      {parent.parent ? parent.name : gettext("Threads")}
    </Link>
  );
}
/* jshint ignore:end */