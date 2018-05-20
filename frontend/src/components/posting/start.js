import React from 'react'; //jshint ignore:line
import CategorySelect from 'misago/components/category-select'; //jshint ignore:line
import Editor from 'misago/components/editor'; //jshint ignore:line
import Form from 'misago/components/form';
import Container from './utils/container'; //jshint ignore:line
import Loader from './utils/loader'; //jshint ignore:line
import Message from './utils/message'; //jshint ignore:line
import Options from './utils/options'; //jshint ignore:line
import * as attachments from './utils/attachments'; //jshint ignore:line
import { getPostValidators, getTitleValidators } from './utils/validators';
import ajax from 'misago/services/ajax';
import posting from 'misago/services/posting'; //jshint ignore:line
import snackbar from 'misago/services/snackbar';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isReady: false,
      isLoading: false,
      isErrored: false,

      showOptions: false,
      categoryOptions: null,

      title: '',
      category: props.category || null,
      categories: [],
      post: '',
      attachments: [],
      close: false,
      hide: false,
      pin: 0,

      validators: {
        title: getTitleValidators(),
        post: getPostValidators()
      },
      errors: {}
    };
  }

  componentDidMount() {
    ajax.get(this.props.config).then(this.loadSuccess, this.loadError);
  }

  /* jshint ignore:start */
  loadSuccess = (data) => {
    let category = null;
    let showOptions = false;
    let categoryOptions = null;

    // hydrate categories, extract posting options
    const categories = data.map((item) => {
      // pick first category that allows posting and if it may, override it with initial one
      if (item.post !== false && (!category || item.id == this.state.category)) {
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

  onCancel = () => {
    const cancel = confirm(gettext("Are you sure you want to discard thread?"));
    if (cancel) {
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

    // if selected pin is greater than allowed, reduce it
    let pin = this.state.pin;
    if (category.post.pin && category.post.pin < pin) {
      pin = category.post.pin;
    }

    this.setState({
      category: category.id,
      categoryOptions: category.post,

      pin
    });
  };

  onPostChange = (event) => {
    this.changeValue('post', event.target.value);
  };

  onAttachmentsChange = (attachments) => {
    this.setState({
      attachments
    });
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
    this.changeValue('hide', true);
  };

  onUnhide = () => {
    this.changeValue('hide', false);
  };
  /* jshint ignore:end */

  clean() {
    if (!this.state.title.trim().length) {
      snackbar.error(gettext("You have to enter thread title."));
      return false;
    }

    if (!this.state.post.trim().length) {
      snackbar.error(gettext("You have to enter a message."));
      return false;
    }

    const errors = this.validate();

    if (errors.title) {
      snackbar.error(errors.title[0]);
      return false;
    }

    if (errors.post) {
      snackbar.error(errors.post[0]);
      return false;
    }

    return true;
  }

  send() {
    return ajax.post(this.props.submit, {
      title: this.state.title,
      category: this.state.category,
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
      close: this.state.close,
      hide: this.state.hide,
      pin: this.state.pin
    });
  }

  handleSuccess(success) {
    snackbar.success(gettext("Your thread has been posted."));
    window.location = success.url;

    // keep form loading
    this.setState({
      'isLoading': true
    });
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      const errors = [].concat(
        rejection.non_field_errors || [],
        rejection.category || [],
        rejection.title || [],
        rejection.post || [],
        rejection.attachments || []
      );

      snackbar.error(errors[0]);
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    /* jshint ignore:start */
    if (this.state.isErrored) {
      return (
        <Message message={this.state.isErrored} />
      );
    }

    if (!this.state.isReady) {
      return (
        <Loader />
      );
    }

    let columns = 0;
    if (this.state.categoryOptions.close) columns += 1;
    if (this.state.categoryOptions.hide) columns += 1;
    if (this.state.categoryOptions.pin) columns += 1;

    let titleStyle = null;

    if (columns === 1) {
      titleStyle = 'col-sm-6';
    } else {
      titleStyle = 'col-sm-8';
    }

    if (columns === 3) {
      titleStyle += ' col-md-6'
    } else if (columns) {
      titleStyle += ' col-md-7'
    } else {
      titleStyle += ' col-md-9'
    }

    return (
      <Container className="posting-form" withFirstRow={true}>
        <form onSubmit={this.handleSubmit}>
          <div className="row first-row">
            <div className={titleStyle}>
              <input
                className="form-control"
                disabled={this.state.isLoading}
                onChange={this.onTitleChange}
                placeholder={gettext("Thread title")}
                type="text"
                value={this.state.title}
              />
            </div>
            <div className='col-xs-12 col-sm-4 col-md-3 xs-margin-top'>
              <CategorySelect
                choices={this.state.categories}
                disabled={this.state.isLoading}
                onChange={this.onCategoryChange}
                value={this.state.category}
              />
            </div>
            <Options
              close={this.state.close}
              columns={columns}
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
                attachments={this.state.attachments}
                loading={this.state.isLoading}
                onAttachmentsChange={this.onAttachmentsChange}
                onCancel={this.onCancel}
                onChange={this.onPostChange}
                submitLabel={gettext("Post thread")}
                value={this.state.post}
              />

            </div>
          </div>
        </form>
      </Container>
    );
    /* jshint ignore:end */
  }
}
