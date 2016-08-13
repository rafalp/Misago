import React from 'react'; //jshint ignore:line
import CategorySelect from 'misago/components/category-select'; //jshint ignore:line
import Editor from 'misago/components/editor'; //jshint ignore:line
import Form from 'misago/components/form';
import Container from './container'; //jshint ignore:line
import Loader from './loader'; //jshint ignore:line
import Message from './message'; //jshint ignore:line
import Options from './options'; //jshint ignore:line
import misago from 'misago';
import ajax from 'misago/services/ajax';
import posting from 'misago/services/posting'; //jshint ignore:line
import snackbar from 'misago/services/snackbar';
import * as validators from 'misago/utils/validators'; //jshint ignore:line

export default class extends Form {
    constructor(props) {
    super(props);

    const initial = props.options.initial || {};
    const validators = {post: getPostValidators()};

    if (props.options.mode === 'START_THREAD') {
      validators.title = getThreadTitleValidators();
    }

    this.state = {
      isReady: false,
      isLoading: false,
      isErrored: false,

      showOptions: false,
      categoryOptions: null,

      title: initial.title || '',
      category: initial.category || null,
      categories: [],
      post: initial.post || '',
      close: initial.close || false,
      hide: initial.hide || false,
      pin: initial.pin || 0,

      validators: validators,
      errors: {}
    };
  }

  componentDidMount() {
    ajax.get(this.props.options.url).then(this.loadSuccess, this.loadError);
  }

  /* jshint ignore:start */
  loadSuccess = (data) => {
    let category = null;
    let showOptions = false;
    let categoryOptions = null;

    // hydrate categories, extract posting options
    const categories = data.map((item) => {
      if (!category && item.post !== false) {
        category = item.id;
        categoryOptions = item.post;
      }

      if (item.post && (item.post.close || item.post.hide || item.post.pin)) {
        showOptions = true;
      }

      return Object.assign(item, {
        disabled: item.post === false,
        label: item.name,
        value: item.id
      });
    });

    this.setState({
      isReady: true,
      showOptions,

      categories,
      category,
      categoryOptions
    });
  };

  loadError = (rejection) => {
    this.setState({
      isErrored: rejection.detail
    });
  };

  onClose = () => {
    const close = confirm(gettext("Are you sure you want to discard your message?"));
    if (close) {
      posting.close();
    }
  };

  onTitleChange = (event) => {
    this.changeValue('title', event.target.value);
  };

  onCategoryChange = (event) => {
    const category = this.state.categories.find((item) => {
      return event.target.value == item.value;
    });

    this.setState({
      category,
      categoryOptions: category.post
    });
  };

  onPostchange = (event) => {
    this.changeValue('post', event.target.value);
  };

  onClose = () => {
    this.changeValue('close', true);
  };

  onOpen = () => {
    this.changeValue('close', false);
  };

  onPinGlobally = () => {
    this.changeValue('pin', 2);
  };

  onPinLocally = () => {
    this.changeValue('pin', 1);
  };

  onUnpin = () => {
    this.changeValue('pin', 0);
  };

  onHide = () => {
    this.changeValue('hide', 1);
  };

  onUnhide = () => {
    this.changeValue('hide', 0);
  };
  /* jshint ignore:end */

  clean() {
    if (this.props.options.mode === 'START_THREAD' && !this.state.title.trim().length) {
      snackbar.error(gettext("You have to enter thread title."));
      return false;
    }

    if (!this.state.post.trim().length) {
      snackbar.error(gettext("You have to enter a message."));
      return false;
    }

    const errors = this.validate();

    if (errors.post) {
      snackbar.error(errors.post[0]);
      return false;
    }

    if (errors.title) {
      snackbar.error(errors.title[0]);
      return false;
    }

    return true;
  }

  send() {
    return ajax.post(misago.get('THREADS_API'), {
      title: this.state.title,
      category: this.state.category,
      post: this.state.post,
      close: this.state.close,
      hide: this.state.hide,
      pin: this.state.pin
    });
  }

  handleSuccess(success) {
    window.location = success.url.index;
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      if (rejection.category) {
        snackbar.error(rejection.category[0]);
      } else if (rejection.title) {
        snackbar.error(rejection.title[0]);
      } else if (rejection.post) {
        snackbar.error(rejection.post[0]);
      }
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    /* jshint ignore:start */
    if (this.state.isReady) {
      return (
        <Container className="posting-form">
          <form onSubmit={this.handleSubmit} method="POST">
            <div className="row first-row">
              <div className={this.state.showOptions ? 'col-md-6' : 'col-md-8'}>
                <input
                  className="form-control"
                  disabled={this.state.isLoading}
                  onChange={this.onTitleChange}
                  placeholder={gettext("Thread title")}
                  type="text"
                  value={this.state.title}
                />
              </div>
              <div className={'col-md-4'}>
                <CategorySelect
                  choices={this.state.categories}
                  disabled={this.state.isLoading}
                  onChange={this.onCategoryChange}
                  value={this.state.category}
                />
              </div>
              <Options
                close={this.state.close}
                disabled={this.state.isLoading}
                hide={this.state.hide}
                onClose={this.onClose}
                onHide={this.onHide}
                onOpen={this.onOpen}
                onPinGlobally={this.onPinGlobally}
                onPinLocally={this.onPinLocally}
                onUnhide={this.onUnhide}
                onUnpin={this.onUnpin}
                options={this.state.categoryOptions}
                pin={this.state.pin}
                showOptions={this.state.showOptions}
              />
            </div>
            <div className="row">
              <div className="col-md-12">

                <Editor
                  loading={this.state.isLoading}
                  onChange={this.onPostchange}
                  onClose={this.onClose}
                  submitLabel={gettext("Post thread")}
                  value={this.state.post}
                />

              </div>
            </div>
          </form>
        </Container>
      );
    } else if (this.state.isErrored) {
      return (
        <Message message={this.state.isErrored} />
      );
    } else {
      return (
        <Loader />
      );
    }
    /* jshint ignore:end */
  }
}

export function getThreadTitleValidators() {
  return [
    validators.minLength(misago.get('SETTINGS').thread_title_length_min, (limitValue, length) => {
      const message = ngettext(
        "Thread title cannot be shorter than %(limit_value)s character (it has %(show_value)s).",
        "Thread title cannot be shorter than %(limit_value)s characters (it has %(show_value)s).",
        limitValue);

      return interpolate(message, {
        limit_value: limitValue,
        show_value: length
      }, true);
    }),
    validators.maxLength(misago.get('SETTINGS').thread_title_length_max, (limitValue, length) => {
      const message = ngettext(
        "Thread title cannot be longer than %(limit_value)s character (it has %(show_value)s).",
        "Thread title cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
        limitValue);

      return interpolate(message, {
        limit_value: limitValue,
        show_value: length
      }, true);
    })
  ];
}

export function getPostValidators() {
  return [
    validators.minLength(misago.get('SETTINGS').post_length_min, (limitValue, length) => {
      const message = ngettext(
        "Post content cannot be shorter than %(limit_value)s character (it has %(show_value)s).",
        "Post content cannot be shorter than %(limit_value)s characters (it has %(show_value)s).",
        limitValue);

      return interpolate(message, {
        limit_value: limitValue,
        show_value: length
      }, true);
    }),
    validators.maxLength(misago.get('SETTINGS').post_length_max, (limitValue, length) => {
      const message = ngettext(
        "Post content cannot be longer than %(limit_value)s character (it has %(show_value)s).",
        "Post content cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
        limitValue);

      return interpolate(message, {
        limit_value: limitValue,
        show_value: length
      }, true);
    })
  ];
}