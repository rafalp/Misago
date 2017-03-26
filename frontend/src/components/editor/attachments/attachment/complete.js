// jshint ignore:start
import React from 'react';
import misago from 'misago';
import escapeHtml from 'misago/utils/escape-html';
import formatFilesize from 'misago/utils/file-size';

const DATE_ABBR = '<abbr title="%(absolute)s">%(relative)s</abbr>';
const USER_SPAN = '<span class="item-title">%(user)s</span>';
const USER_URL = '<a href="%(url)s" class="item-title">%(user)s</a>';

export default class extends React.Component {
  onInsert = () => {
    this.props.replaceSelection(this.insertAttachment);
  };

  insertAttachment = (selection, replace) => {
    const item = this.props.item;

    if (item.is_image) {
      if (item.url.thumb) {
        replace('[![' + item.filename + '](' + item.url.thumb + ')](' + item.url.index + ')');
      } else {
        replace('[![' + item.filename + '](' + item.url.index + ')](' + item.url.index + ')');
      }
    } else {
      replace('[' + item.filename + '](' + item.url.index + ')');
    }
  };

  onRemove = () => {
    this.updateItem({
      isRemoved: true
    });
  };

  onUndo = () => {
    this.updateItem({
      isRemoved: false
    });
  };

  updateItem = (newState) => {
    const updatedAttachments = this.props.attachments.map((item) => {
      if (item.id === this.props.item.id) {
        return Object.assign({}, item, newState);
      } else {
        return item;
      }
    });
    this.props.onAttachmentsChange(updatedAttachments);
  };

  render() {
    return (
      <li className="editor-attachment-complete">
        <div className="row">
          <div className="col-xs-12 col-sm-8 col-md-9">
            <Preview {...this.props} />
            <div className="editor-attachment-details">
              <Filename {...this.props} />
              <Details {...this.props} />
            </div>
          </div>
          <div className="col-xs-12 col-sm-4 col-md-3 xs-margin-top-half">
            <Actions
              onInsert={this.onInsert}
              onRemove={this.onRemove}
              onUndo={this.onUndo}
              {...this.props}
            />
          </div>
        </div>
      </li>
    );
  }
};

export function Preview(props) {
  if (props.item.is_image) {
    return (
      <Image {...props} />
    );
  } else {
    return (
      <Icon {...props} />
    );
  }
}

export function Image(props) {
  const thumbnailUrl = props.item.url.thumb || props.item.url.index;

  return (
    <div className="editor-attachment-image">
      <a
        href={props.item.url.index + '?shva=1'}
        style={{backgroundImage: "url('" + thumbnailUrl + "?shva=1')"}}
        target="_blank"
      />
    </div>
  );
};

export function Icon(props) {
  return (
    <div className="editor-attachment-icon">
      <span className="material-icon">
        insert_drive_file
      </span>
    </div>
  );
}

export function Filename(props) {
  return (
    <h4>
      <a
        className="item-title"
        href={props.item.url.index + '?shva=1'}
        target="_blank"
      >
        {props.item.filename}
      </a>
    </h4>
  );
}

export function Details(props) {
  let user = null;
  if (props.item.url.uploader) {
    user = interpolate(USER_URL, {
      url: escapeHtml(props.item.url.uploader),
      user: escapeHtml(props.item.uploader_name)
    }, true);
  } else {
    user = interpolate(USER_SPAN, {
      user: escapeHtml(props.item.uploader_name)
    }, true);
  }

  const date = interpolate(DATE_ABBR, {
    absolute: escapeHtml(props.item.uploaded_on.format('LLL')),
    relative: escapeHtml(props.item.uploaded_on.fromNow())
  }, true);

  const message = interpolate(escapeHtml(gettext("%(filetype)s, %(size)s, uploaded by %(uploader)s %(uploaded_on)s.")), {
    filetype: props.item.filetype,
    size: formatFilesize(props.item.size),
    uploader: user,
    uploaded_on: date
  }, true);

  return (
    <p dangerouslySetInnerHTML={{__html: message}} />
  );
}

export function Actions(props) {
  return (
    <div className="editor-attachment-actions">
      <div className="row">
        <Insert {...props} />
        <Remove {...props} />
        <Undo {...props} />
      </div>
    </div>
  );
}

export function Insert(props) {
  if (!!props.item.isRemoved) {
    return null;
  }

  return (
    <div className="col-xs-6">
      <button
        className="btn btn-default btn-sm btn-block"
        onClick={props.onInsert}
        type="button"
      >
        {gettext("Insert")}
      </button>
    </div>
  );
}

export function Remove(props) {
  if (!!props.item.isRemoved && props.item.acl.can_delete) {
    return null;
  }

  return (
    <div className="col-xs-6">
      <button
        className="btn btn-default btn-sm btn-block"
        onClick={props.onRemove}
        type="button"
      >
        {gettext("Remove")}
      </button>
    </div>
  );
}

export function Undo(props) {
  if (!props.item.isRemoved) {
    return null;
  }

  return (
    <div className="col-xs-12">
      <button
        className="btn btn-default btn-sm btn-block"
        onClick={props.onUndo}
        type="button"
      >
        {gettext("Undo removal")}
      </button>
    </div>
  );
}
