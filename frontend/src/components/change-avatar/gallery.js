import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import misago from 'misago/index'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import batch from 'misago/utils/batch'; // jshint ignore:line

export class GalleryItem extends React.Component {
  /* jshint ignore:start */
  select = () => {
    this.props.select(this.props.id);
  };
  /* jshint ignore:end */

  getClassName() {
    if (this.props.selection === this.props.id) {
      if (this.props.disabled) {
        return 'btn btn-avatar btn-disabled avatar-selected';
      } else {
        return 'btn btn-avatar avatar-selected';
      }
    } else if (this.props.disabled) {
      return 'btn btn-avatar btn-disabled';
    } else {
      return 'btn btn-avatar';
    }
  }

  render() {
    /* jshint ignore:start */
    return <button type="button"
                   className={this.getClassName()}
                   disabled={this.props.disabled}
                   onClick={this.select}>
      <img src={this.props.url} />
    </button>
    /* jshint ignore:end */
  }
}

export class Gallery extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="avatars-gallery">
      <h3>{this.props.name}</h3>

      <div className="avatars-gallery-images">
        {batch(this.props.images, 4, null).map((row, i) => {
          return <div className="row" key={i}>
            {row.map((item, i) => {
              return <div className="col-xs-3" key={i}>
                {item ? <GalleryItem
                          disabled={this.props.disabled}
                          select={this.props.select}
                          selection={this.props.selection}
                          {...item}
                        />
                      : <div className="blank-avatar" />}
              </div>
            })}
          </div>
        })}
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      'selection': null,
      'isLoading': false
    };
  }

  /* jshint ignore:start */
  select = (image) => {
    this.setState({
      selection: image
    });
  };

  save = () => {
    if (this.state.isLoading) {
      return false;
    }

    this.setState({
      'isLoading': true
    });

    ajax.post(this.props.user.api_url.avatar, {
      avatar: 'galleries',
      image: this.state.selection
    }).then((response) => {
      this.setState({
        'isLoading': false
      });

      snackbar.success(response.detail);
      this.props.onComplete(response);
      this.props.showIndex();
    }, (rejection) => {
      if (rejection.status === 400) {
        snackbar.error(rejection.detail);
        this.setState({
          'isLoading': false
        });
      } else {
        this.props.showError(rejection);
      }
    });
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    return <div>
      <div className="modal-body modal-avatar-gallery">

        {this.props.options.galleries.map((item, i) => {
          return <Gallery name={item.name}
                          images={item.images}
                          selection={this.state.selection}
                          disabled={this.state.isLoading}
                          select={this.select}
                          key={i} />;
        })}

      </div>
      <div className="modal-footer">
        <div className="row">
          <div className="col-md-6 col-md-offset-3">

            <Button onClick={this.save}
                    loading={this.state.isLoading}
                    disabled={!this.state.selection}
                    className="btn-primary btn-block">
              {this.state.selection ? gettext("Save choice")
                                    : gettext("Select avatar")}
            </Button>

            <Button onClick={this.props.showIndex}
                    disabled={this.state.isLoading}
                    className="btn-default btn-block">
              {gettext("Cancel")}
            </Button>

          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}