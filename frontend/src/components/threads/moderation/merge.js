import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import CategorySelect from 'misago/components/category-select'; // jshint ignore:line
import Select from 'misago/components/select'; // jshint ignore:line
import misago from 'misago/index';
import { filterThreads } from 'misago/reducers/threads'; // jshint ignore:line
import * as select from 'misago/reducers/selection'; // jshint ignore:line
import ErrorsModal from 'misago/components/threads/moderation/errors-list'; // jshint ignore:line
import MergePolls from 'misago/components/merge-polls'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import modal from 'misago/services/modal'; // jshint ignore:line
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store'; // jshint ignore:line
import * as validators from 'misago/utils/validators';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,

      title: '',
      category: null,
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

    this.acl = {};
    for (const i in props.user.acl.categories) {
      if (!props.user.acl.categories.hasOwnProperty(i)) {
        continue;
      }

      const acl = props.user.acl.categories[i];
      this.acl[acl.id] = acl;
    }

    this.categoryChoices = [];
    props.categories.forEach((category) => {
      if (category.level > 0) {
        const acl = this.acl[category.id];
        const disabled = !acl.can_start_threads || (category.is_closed && !acl.can_close_threads);

        this.categoryChoices.push({
          value: category.id,
          disabled: disabled,
          level: category.level - 1,
          label: category.name
        });

        if (!disabled && !this.state.category) {
          this.state.category = category.id;
        }
      }
    });

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
    return ajax.post(misago.get('MERGE_THREADS_API'), this.getFormdata());
  }

  /* jshint ignore:start */
  getFormdata = () => {
    return {
      threads: this.props.threads.map((thread) => thread.id),
      title: this.state.title,
      category: this.state.category,
      weight: this.state.weight,
      is_hidden: this.state.is_hidden,
      is_closed: this.state.is_closed
    };
  };

  handleSuccess = (apiResponse) => {
    // unfreeze and remove merged threads
    this.props.threads.forEach((thread) => {
      this.props.freezeThread(thread.id);
      this.props.deleteThread(thread);
    });

    // deselect all threads
    store.dispatch(select.none());

    // append merged thread, filter threads
    this.props.addThreads([apiResponse]);
    store.dispatch(filterThreads(this.props.route.category, this.props.categoriesMap));

    // hide modal
    modal.hide();
  };

  handleError = (rejection) => {
    if (rejection.status === 400) {
      if (rejection.polls) {
        modal.show(
          <MergePolls
            api={misago.get('MERGE_THREADS_API')}
            data={this.getFormdata()}
            polls={rejection.polls}
            onError={this.handleError}
            onSuccess={this.handleSuccess}
          />
        );
      } else {
        this.setState({
          'errors': Object.assign({}, this.state.errors, rejection)
        });
        snackbar.error(gettext("Form contains errors."));
      }
    } else if (rejection.status === 403 && Array.isArray(rejection)) {
      modal.show(<ErrorsModal errors={rejection} />);
    } else {
      snackbar.apiError(rejection);
    }
  };

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
  /* jshint ignore:end */

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
      /* jshint ignore:start */
      return <FormGroup label={gettext("Thread weight")}
                        for="id_weight"
                        labelClass="col-sm-4" controlClass="col-sm-8">
        <Select id="id_weight"
                onChange={this.bindInput('weight')}
                value={this.state.weight}
                choices={this.getWeightChoices()} />
      </FormGroup>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  renderHiddenField() {
    if (this.acl[this.state.category].can_hide_threads) {
      /* jshint ignore:start */
      return <FormGroup label={gettext("Hide thread")}
                        for="id_is_hidden"
                        labelClass="col-sm-4" controlClass="col-sm-8">
        <Select id="id_is_closed"
                onChange={this.bindInput('is_hidden')}
                value={this.state.is_hidden}
                choices={this.isHiddenChoices} />
      </FormGroup>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  renderClosedField() {
    if (this.acl[this.state.category].can_close_threads) {
      /* jshint ignore:start */
      return <FormGroup label={gettext("Close thread")}
                        for="id_is_closed"
                        labelClass="col-sm-4" controlClass="col-sm-8">
        <Select id="id_is_closed"
                onChange={this.bindInput('is_closed')}
                value={this.state.is_closed}
                choices={this.isClosedChoices} />
      </FormGroup>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  renderForm() {
    /* jshint ignore:start */
    return <form onSubmit={this.handleSubmit}>
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
                          choices={this.categoryChoices} />
        </FormGroup>
        <div className="clearfix"></div>

        {this.renderWeightField()}
        {this.renderHiddenField()}
        {this.renderClosedField()}

      </div>
      <div className="modal-footer">
        <Button className="btn-primary" loading={this.state.isLoading}>
          {gettext("Merge threads")}
        </Button>
      </div>
    </form>;
    /* jshint ignore:end */
  }

  renderCantMergeMessage() {
    /* jshint ignore:start */
    return <div className="modal-body">
      <div className="message-icon">
        <span className="material-icon">
          info_outline
        </span>
      </div>
      <div className="message-body">
        <p className="lead">
          {gettext("You can't move threads because there are no categories you are allowed to move them to.")}
        </p>
        <p>
          {gettext("You need permission to start threads in category to be able to merge threads to it.")}
        </p>
      </div>
    </div>;
    /* jshint ignore:end */
  }

  getClassName() {
    if (!this.state.category) {
      return 'modal-dialog modal-message';
    } else {
      return 'modal-dialog';
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()} role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal"
                  aria-label={gettext("Close")}>
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Merge threads")}</h4>
        </div>
        {this.state.category ? this.renderForm() : this.renderCantMergeMessage()}
      </div>
    </div>;
    /* jshint ignore:end */
  }
}
