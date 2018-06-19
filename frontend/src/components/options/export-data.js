/* jshint ignore:start */
import React from 'react';
import moment from 'moment';
import Button from 'misago/components/button';
import ajax from 'misago/services/ajax';
import title from 'misago/services/page-title';
import snackbar from 'misago/services/snackbar';

export default class ExportData extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
      isSubmiting: false,
      exports: []
    }
  }

  componentDidMount() {
    title.set({
      title: gettext("Download your data"),
      parent: gettext("Change your options")
    });

    this.handleLoadExports();
  }

  handleLoadExports = () => {
    ajax.get(this.props.user.api.data_export).then((data) => {
      this.setState({
        isLoading: false,
        exports: data
      });
    });
  };

  handleStartDataExport = () => {
    this.setState({ isSubmiting: true });
    ajax.post(this.props.user.api.start_data_export).then(
      (data) => {
        this.handleLoadExports();
        snackbar.success(rejection);
        this.setState({ isSubmiting: false });
      },
      (rejection) => {
        snackbar.apiError(rejection);
        this.setState({ isSubmiting: false });
      }
    );
  }

  render() {
    return (
      <div>
        <div className="panel panel-default panel-form">
          <div className="panel-heading">
            <h3 className="panel-title">{gettext("Download your data")}</h3>
          </div>
          <div className="panel-body lead">

            To download your data from the site, click the "Request data download" button.

          </div>
          <table className="table">
            <thead>
              <tr>
                <th>{gettext("Requested on")}</th>
                <th className="col-md-3">{gettext("Download")}</th>
              </tr>
            </thead>
            <tbody>
              {this.state.exports.map((item) => {
                return (
                  <tr key={item.id}>
                    <td style={rowStyle}>{moment(item.requested_on).fromNow()}</td>
                    <td>
                      <DownloadButton
                        exportFile={item.export_file}
                        status={item.status}
                      />
                    </td>
                  </tr>
                )
              })}
              {this.state.exports.length == 0 ?
                <tr>
                  <td colSpan="2">{gettext("You have no data exports history.")}</td>
                </tr> : null}
            </tbody>
          </table>
          <div className="panel-footer text-right">
            <Button
              className="btn-primary"
              loading={this.state.isSubmiting}
              type="button"
              onClick={this.handleStartDataExport}
            >
              {gettext("Request data download")}
            </Button>
          </div>
        </div>
      </div>
    );
  }
}

const rowStyle = {
  verticalAlign: 'middle'
};

const STATUS_PENDING = 0;
const STATUS_PROCESSING = 1;

const DownloadButton = ({ exportFile, status }) => {
  if (status === STATUS_PENDING) {
    return (
      <Button
        className="btn-info btn-sm btn-block"
        disabled={true}
        type="button"
      >
        {gettext("Export is started")}
      </Button>
    );
  }

  if (status === STATUS_PROCESSING) {
    return (
      <Button
        className="btn-success btn-sm btn-block"
        disabled={true}
        type="button"
      >
        {gettext("Export in progress")}
      </Button>
    );
  }

  if (exportFile) {
    return (
      <a
        className="btn btn-success btn-sm btn-block"
        href={exportFile}
      >
        {gettext("Download your data")}
      </a>
    );
  }

  return (
    <Button
      className="btn-default btn-sm btn-block"
      disabled={true}
      type="button"
    >
      {gettext("Download has expired")}
    </Button>
  );
}