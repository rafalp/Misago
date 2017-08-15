// jshint ignore:start
import React from 'react';
import Autosuggest from 'react-autosuggest';
import ajax from 'misago/services/ajax';
import misago from 'misago';
import renderSuggestion from './render-suggestion';
import THEME from './theme';
import { getSuggestions } from './utils';
import { getSectionSuggestions } from './utils';
import { renderSectionTitle } from './utils';

const getSuggestionValue = suggestion => suggestion.name;

export default class extends React.Component {
  constructor() {
    super();

    this.state = {
      value: '',
      suggestions: []
    };
  }

  onChange = (event, { newValue }) => {
    this.setState({
      value: newValue
    });
  };

  onSuggestionsFetchRequested = ({ value }) => {
    ajax.get(misago.get('SEARCH_API'), {'q': value.trim()}).then(
      (data) => {
        this.setState({
          suggestions: getSuggestions(data)
        });
      },
      (rejection) => {
        console.log('ERROR!')
      }
    );
  };

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });
  };

  render() {
    const { value, suggestions } = this.state;

    const inputProps = {
      value,

      className: 'form-control',
      onChange: this.onChange,
      placeholder: gettext("Search")
    };

    return (
      <div className="navbar-form">
        <div className="form-group">
          <Autosuggest
            alwaysRenderSuggestions={false}
            getSuggestionValue={getSuggestionValue}
            getSectionSuggestions={getSectionSuggestions}
            inputProps={inputProps}
            multiSection={true}
            onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
            onSuggestionsClearRequested={this.onSuggestionsClearRequested}
            renderSectionTitle={renderSectionTitle}
            renderSuggestion={renderSuggestion}
            suggestions={suggestions}
            theme={THEME}
          />
        </div>
      </div>
    );
  }
}