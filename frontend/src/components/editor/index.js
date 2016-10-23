// jshint ignore:start
import React from 'react';
import Code from './actions/code';
import Emphasis from './actions/emphasis';
import Hr from './actions/hr';
import Image from './actions/image';
import Link from './actions/link';
import Striketrough from './actions/striketrough';
import Strong from './actions/strong';
import Quote from './actions/quote';
import AttachmentsEditor from './attachments';
import Upload from './attachments/upload-button/';
import MarkupPreview from './markup-preview';
import * as textUtils from './textUtils';
import Button from 'misago/components/button';
import misago from 'misago';
import ajax from 'misago/services/ajax';
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isPreviewLoading: false
    };
  }

  onPreviewClick = () => {
    if (this.state.isPreviewLoading) {
      return;
    }

    this.setState({
      isPreviewLoading: true
    });

    ajax.post(misago.get('PARSE_MARKUP_API'), {post: this.props.value}).then((data) => {
      modal.show(
        <MarkupPreview markup={data.parsed} />
      );

      this.setState({
        isPreviewLoading: false
      });
    }, (rejection) => {
      if (rejection.status === 400) {
        snackbar.error(rejection.detail);
      } else {
        snackbar.apiError(rejection);
      }

      this.setState({
        isPreviewLoading: false
      });
    });
  };

  replaceSelection = (operation) => {
    operation(textUtils.getSelectionText(), this._replaceSelection);
  };

  _replaceSelection = (newValue) => {
    this.props.onChange({
      target: {
        value: textUtils.replace(newValue)
      }
    });
  };

  render() {
    return (
      <div className="editor-border">
        <textarea
          className="form-control"
          defaultValue={this.props.value}
          disabled={this.props.loading}
          id="editor-textarea"
          onChange={this.props.onChange}
          rows="9"
        ></textarea>
        <div className="editor-footer">
          <Strong
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Emphasis
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Striketrough
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Hr
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Link
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Image
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Quote
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Code
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            replaceSelection={this.replaceSelection}
          />
          <Upload
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
          />
          <Button
            className="btn-default btn-sm pull-left"
            disabled={this.props.loading || this.state.isPreviewLoading}
            onClick={this.onPreviewClick}
            type="button"
          >
            {gettext("Preview")}
          </Button>
          <Button
            className="btn-primary btn-sm pull-right"
            loading={this.props.loading}
          >
            {this.props.submitLabel || gettext("Post")}
          </Button>
          <button
            className="btn btn-default btn-sm pull-right"
            disabled={this.props.loading}
            onClick={this.props.onCancel}
            type="button"
          >
            {gettext("Cancel")}
          </button>
          <Protect
            canProtect={this.props.canProtect}
            disabled={this.props.loading}
            onProtect={this.props.onProtect}
            onUnprotect={this.props.onUnprotect}
            protect={this.props.protect}
          />
        </div>
        <AttachmentsEditor
          attachments={this.props.attachments}
          onAttachmentsChange={this.props.onAttachmentsChange}
          placeholder={this.props.placeholder}
          replaceSelection={this.replaceSelection}
        />
      </div>
    );
  }
}

export function Protect(props) {
  if (props.canProtect) {
    return (
      <button
        className="btn btn-default btn-sm pull-right"
        disabled={props.disabled}
        onClick={props.protect ? props.onUnprotect : props.onProtect}
        title={props.protect ? gettext('Protected') : gettext('Protect')}
        type="button"
      >
        <span className="material-icon">
          {props.protect ? 'lock' : 'lock_outline'}
        </span>
      </button>
    );
  } else {
    return null;
  }
}
