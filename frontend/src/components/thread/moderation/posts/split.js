/* jshint ignore:start */
import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import CategorySelect from 'misago/components/category-select'; // jshint ignore:line
import ModalLoader from 'misago/components/modal-loader'; // jshint ignore:line
import Select from 'misago/components/select'; // jshint ignore:line
import * as post from 'misago/reducers/post';
import ajax from 'misago/services/ajax'; // jshint ignore:line
import modal from 'misago/services/modal'; // jshint ignore:line
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store'; // jshint ignore:line
import * as validators from 'misago/utils/validators';

export default function(props) {
  return (
    <PostingConfig {...props} Form={ModerationForm} />
  );
}

export class PostingConfig extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoaded: false,
      isError: false,

      categories: []
    };
  }

  componentDidMount() {
    ajax.get(misago.get('THREAD_EDITOR_URL')).then((data) => {
      // hydrate categories, extract posting options
      const categories = data.map((item) => {
        return Object.assign(item, {
          disabled: item.post === false,
          label: item.name,
          value: item.id,
          post: item.post
        });
      });

      this.setState({
        isLoaded: true,
        categories
      })
    }, (rejection) => {
      this.setState({
        isError: rejection.detail
      });
    });
  }

  render() {
    if (this.state.isError) {
      return (
        <Error message={this.state.isError} />
      );
    } else if (this.state.isLoaded) {
      return (
        <ModerationForm {...this.props} categories={this.state.categories} />
      );
    } else {
      return (
        <Loader />
      );
    }
  }
}

export class ModerationForm extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,

      title: '',
      category: null,
      categories: props.categories,
      weight: 0,
      is_hidden: 0,
      is_closed: false,

      validators: {
        title: [
          validators.required()
        ]
      },

      errors: {}
    };

    this.isHiddenChoices = [
      {
        'value': 0,
        'icon': 'visibility',
        'label': gettext("No")
      },
      {
        'value': 1,
        'icon': 'visibility_off',
        'label': gettext("Yes")
      },
    ];

    this.isClosedChoices = [
      {
        'value': false,
        'icon': 'lock_outline',
        'label': gettext("No")
      },
      {
        'value': true,
        'icon': 'lock',
        'label': gettext("Yes")
      },
    ];

    this.acl = {};
    this.props.categories.forEach((category) => {
      if (category.post) {
        if (!this.state.category) {
          this.state.category = category.id;
        }

        this.acl[category.id] = {
          can_pin_threads: category.post.pin,
          can_close_threads: category.post.close,
          can_hide_threads: category.post.hide,
        };
      }
    });
  }

  clean() {
    if (this.isValid()) {
      return true;
    } else {
      snackbar.error(gettext("Form contains errors."));
      this.setState({
        errors: this.validate()
      });
      return false;
    }
  }

  send() {
    return ajax.post(this.props.thread.api.posts.split, {
      title: this.state.title,
      category: this.state.category,
      weight: this.state.weight,
      is_hidden: this.state.is_hidden,
      is_closed: this.state.is_closed,
      posts: this.props.selection.map((post) => post.id)
    });
  }

  handleSuccess(apiResponse) {
    this.props.selection.forEach((selection) => {
      store.dispatch(post.patch(selection, {
        isDeleted: true
      }));
    });

    modal.hide();

    snackbar.success(gettext("Selected posts were split into new thread."));
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      this.setState({
        'errors': Object.assign({}, this.state.errors, rejection)
      });
      snackbar.error(gettext("Form contains errors."));
    } else if (rejection.status === 403 && Array.isArray(rejection)) {
      modal.show(<ErrorsModal errors={rejection} />);
    } else {
      snackbar.apiError(rejection);
    }
  }

  onCategoryChange = (ev) => {
    const categoryId = ev.target.value;
    const newState = {
      category: categoryId
    };

    if (this.acl[categoryId].can_pin_threads < newState.weight) {
      newState.weight = 0;
    }

    if (!this.acl[categoryId].can_hide_threads) {
      newState.is_hidden = 0;
    }

    if (!this.acl[categoryId].can_close_threads) {
      newState.is_closed = false;
    }

    this.setState(newState);
  };

  getWeightChoices() {
    const choices = [
      {
        'value': 0,
        'icon': 'remove',
        'label': gettext("Not pinned"),
      },
      {
        'value': 1,
        'icon': 'bookmark_border',
        'label': gettext("Pinned locally"),
      }
    ];

    if (this.acl[this.state.category].can_pin_threads == 2) {
      choices.push({
        'value': 2,
        'icon': 'bookmark',
        'label': gettext("Pinned globally"),
      });
    }

    return choices;
  }

  renderWeightField() {
    if (this.acl[this.state.category].can_pin_threads) {
      return <FormGroup label={gettext("Thread weight")}
                        for="id_weight"
                        labelClass="col-sm-4" controlClass="col-sm-8">
        <Select id="id_weight"
                onChange={this.bindInput('weight')}
                value={this.state.weight}
                choices={this.getWeightChoices()} />
      </FormGroup>;
    } else {
      return null;
    }
  }

  renderHiddenField() {
    if (this.acl[this.state.category].can_hide_threads) {
      return <FormGroup label={gettext("Hide thread")}
                        for="id_is_hidden"
                        labelClass="col-sm-4" controlClass="col-sm-8">
        <Select id="id_is_closed"
                onChange={this.bindInput('is_hidden')}
                value={this.state.is_hidden}
                choices={this.isHiddenChoices} />
      </FormGroup>;
    } else {
      return null;
    }
  }

  renderClosedField() {
    if (this.acl[this.state.category].can_close_threads) {
      return <FormGroup label={gettext("Close thread")}
                        for="id_is_closed"
                        labelClass="col-sm-4" controlClass="col-sm-8">
        <Select id="id_is_closed"
                onChange={this.bindInput('is_closed')}
                value={this.state.is_closed}
                choices={this.isClosedChoices} />
      </FormGroup>;
    } else {
      return null;
    }
  }

  render() {
    return (
      <Modal className="modal-dialog">
        <form onSubmit={this.handleSubmit}>
          <div className="modal-body">

            <FormGroup label={gettext("Thread title")}
                       for="id_title"
                       labelClass="col-sm-4" controlClass="col-sm-8"
                       validation={this.state.errors.title}>
              <input id="id_title"
                     className="form-control"
                     type="text"
                     onChange={this.bindInput('title')}
                     value={this.state.title} />
            </FormGroup>
            <div className="clearfix"></div>

            <FormGroup label={gettext("Category")}
                       for="id_category"
                       labelClass="col-sm-4" controlClass="col-sm-8"
                       validation={this.state.errors.category}>
              <CategorySelect id="id_category"
                              onChange={this.onCategoryChange}
                              value={this.state.category}
                              choices={this.state.categories} />
            </FormGroup>
            <div className="clearfix"></div>

            {this.renderWeightField()}
            {this.renderHiddenField()}
            {this.renderClosedField()}

          </div>
          <div className="modal-footer">
            <Button className="btn-primary" loading={this.state.isLoading}>
              {gettext("Split posts")}
            </Button>
          </div>
        </form>
      </Modal>
    );
  }
}

export function Loader() {
  return (
    <Modal className="modal-dialog">
      <ModalLoader />
    </Modal>
  );
}

export function Error(props) {
  return (
    <Modal className="modal-dialog modal-message">
      <div className="message-icon">
        <span className="material-icon">
          info_outline
        </span>
      </div>
      <div className="message-body">
        <p className="lead">
          {gettext("You can't move selected posts at the moment.")}
        </p>
        <p>
          {props.message}
        </p>
      </div>
    </Modal>
  );
}

export function Modal(props) {
  return (
    <div className={props.className} role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button
            aria-label={gettext("Close")}
            className="close"
            data-dismiss="modal"
            type="button"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Split posts into new thread")}</h4>
        </div>
        {props.children}
      </div>
    </div>
  );
}