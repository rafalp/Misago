import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import CategoryPicker from 'misago/components/threads/category-picker'; // jshint ignore:line
import Header from 'misago/components/threads/header'; // jshint ignore:line
import ThreadsListEmpty from 'misago/components/threads/list-empty'; // jshint ignore:line
import { CompactNav } from 'misago/components/threads/navs'; // jshint ignore:line
import { getPageTitle, getTitle } from 'misago/components/threads/title-utils';
import ThreadsList from 'misago/components/threads-list/root'; // jshint ignore:line
import WithDropdown from 'misago/components/with-dropdown';
import misago from 'misago/index';
import { append, hydrate } from 'misago/reducers/threads'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import title from 'misago/services/page-title';

export default class extends WithDropdown {
  constructor(props) {
    super(props);

    if (misago.has('THREADS')) {
      this.initWithPreloadedData(misago.get('THREADS'));
    } else {
      this.initWithoutPreloadedData();
    }
  }

  initWithPreloadedData(data) {
    this.state = {
      isLoaded: false,
      isBusy: false,

      dropdown: false,
      subcategories: data.subcategories,

      count: data.count,
      more: data.more,

      page: data.page,
      pages: data.pages
    };
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false,
      isBusy: false,

      dropdown: false,
      subcategories: [],

      count: 0,
      more: 0,

      page: 1,
      pages: 1
    };

    this.loadThreads();
  }

  loadThreads(page=1) {
    let category = null;
    if (!this.props.route.category.special_role) {
      category = this.props.route.category.id;
    }

    ajax.get(misago.get('THREADS_API'), {
      category: category,
      list: this.props.route.list.type,
      page: page || 1
    }, 'threads').then((data) => {
      if (page === 1) {
        store.dispatch(hydrate(data.results));
      } else {
        store.dispatch(append(data.results));
      }

      this.setState({
        isLoaded: true,
        isBusy: false,

        subcategories: data.subcategories,

        count: data.count,
        more: data.more,

        page: data.page,
        pages: data.pages
      });
    }, (rejection) => {
      snackbar.apiError(rejection);
    });
  }

  componentDidMount() {
    title.set(getPageTitle(this.props.route));

    if (misago.has('THREADS')) {
      // unlike in other components, routes are root components for threads
      // so we can't dispatch store action from constructor
      store.dispatch(hydrate(misago.pop('THREADS').results));

      this.setState({
        isLoaded: true
      });
    }
  }

  getTitle() {
    return getTitle(this.props.route);
  }

  /* jshint ignore:start */
  loadMore = () => {
    this.setState({
      isBusy: true
    });

    this.loadThreads(this.state.page + 1);
  };
  /* jshint ignore:end */

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

  getCategoryDescription() {
    if (this.props.route.category.description) {
      /* jshint ignore:start */
      return <div className="category-description">
        <div className="lead" dangerouslySetInnerHTML={{
          __html: this.props.route.category.description.html
        }} />
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getToolbar() {
    if (this.state.subcategories.length) {
      /* jshint ignore:start */
      return <div className="toolbar">
        <CategoryPicker choices={this.state.subcategories}
                        categories={this.props.route.categoriesMap}
                        list={this.props.route.list} />
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getMoreButton() {
    if (this.state.more) {
      /* jshint ignore:start */
      return <div className="pager-more">
        <Button loading={this.state.isBusy}
                onClick={this.loadMore}>
          {gettext("Show more")}
        </Button>
      </div>;
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

        {this.getCategoryDescription()}
        {this.getToolbar()}

        <ThreadsList threads={this.props.threads}
                     categories={this.props.route.categoriesMap}
                     isLoaded={this.state.isLoaded}
                     isBusy={this.state.isBusy}>
          <ThreadsListEmpty category={this.props.route.category}
                            list={this.props.route.list} />
        </ThreadsList>

        {this.getMoreButton()}

      </div>
    </div>;
    /* jshint ignore:end */
  }
}