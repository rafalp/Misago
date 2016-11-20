// jshint ignore:start
import React from 'react';
import Button from 'misago/components/button';
import escapeHtml from 'misago/utils/escape-html';

const DATE_ABBR = '<abbr title="%(absolute)s">%(relative)s</abbr>';
const USER_SPAN = '<span class="item-title">%(user)s</span>';
const USER_URL = '<a href="%(url)s" class="item-title">%(user)s</a>';

export default class extends React.Component {
  goLast = () => {
    this.props.goToEdit();
  };

  goForward = () => {
    this.props.goToEdit(this.props.edit.next);
  };

  goBack = () => {
    this.props.goToEdit(this.props.edit.previous);
  };

  revertEdit = () => {
    this.props.revertEdit(this.props.edit.id);
  }

  render() {
    return (
      <div className="modal-toolbar">
        <GoBackBtn
          disabled={this.props.disabled}
          edit={this.props.edit}
          onClick={this.goBack}
        />
        <GoForwardBtn
          disabled={this.props.disabled}
          edit={this.props.edit}
          onClick={this.goForward}
        />
        <GoLastBtn
          disabled={this.props.disabled}
          edit={this.props.edit}
          onClick={this.goLast}
        />
        <Label edit={this.props.edit} />
        <RevertBtn
          canRevert={this.props.canRevert}
          disabled={this.props.disabled}
          onClick={this.revertEdit}
        />
      </div>
    );
  }
}

export function GoBackBtn(props) {
  return (
    <Button
      className="btn-default btn-icon btn-sm pull-left"
      disabled={props.disabled || !props.edit.previous}
      onClick={props.onClick}
      title={gettext("See previous change")}
    >
      <span className="material-icon">
        chevron_left
      </span>
    </Button>
  )
}

export function GoForwardBtn(props) {
  return (
    <Button
      className="btn-default btn-icon btn-sm pull-left"
      disabled={props.disabled || !props.edit.next}
      onClick={props.onClick}
      title={gettext("See previous change")}
    >
      <span className="material-icon">
        chevron_right
      </span>
    </Button>
  )
}

export function GoLastBtn(props) {
  return (
    <Button
      className="btn-default btn-icon btn-sm pull-left"
      disabled={props.disabled || !props.edit.next}
      onClick={props.onClick}
      title={gettext("See previous change")}
    >
      <span className="material-icon">
        last_page
      </span>
    </Button>
  )
}

export function RevertBtn(props) {
  if (!props.canRevert) return null;

  return (
    <Button
      className="btn-default btn-sm pull-right"
      disabled={props.disabled}
      onClick={props.onClick}
      title={gettext("Revert post to state from before this edit.")}
    >
      {gettext("Revert")}
    </Button>
  )
}

export function Label(props) {
  let user = null;
  if (props.edit.url.editor) {
    user = interpolate(USER_URL, {
      url: escapeHtml(props.edit.url.editor),
      user: escapeHtml(props.edit.editor_name)
    }, true);
  } else {
    user = interpolate(USER_SPAN, {
      user: escapeHtml(props.edit.editor_name)
    }, true);
  }

  const date = interpolate(DATE_ABBR, {
    absolute: escapeHtml(props.edit.edited_on.format('LLL')),
    relative: escapeHtml(props.edit.edited_on.fromNow())
  }, true);

  const message = interpolate(escapeHtml(gettext("By %(edited_by)s %(edited_on)s.")), {
    edited_by: user,
    edited_on: date
  }, true);

  return (
    <p
      className="pull-left"
      dangerouslySetInnerHTML={{__html: message}}
    />
  );
}