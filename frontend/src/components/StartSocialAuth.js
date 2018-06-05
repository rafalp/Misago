/* jshint ignore:start */
import React from 'react'
import misago from 'misago'

const StartSocialAuth = (props) => {
  const {
    buttonClassName,
    buttonLabel,
    formLabel,
    header,
    labelClassName,
  } = props;
  const socialAuth = misago.get('SETTINGS').SOCIAL_AUTH;

  if (socialAuth.length === 0) return null;

  return (
    <div className="form-group form-social-auth">
      <FormHeader className={labelClassName} text={header} />
      <div className="row">
        {socialAuth.map(({ id, name, url }) => {
          const className = 'btn btn-block btn-default btn-social-' + id;
          const finalButtonLabel = interpolate(buttonLabel, { site: name }, true);

          return (
            <div className={buttonClassName || 'col-xs-12'} key={id}>
              <a className={className} href={url}>
                {finalButtonLabel}
              </a>
            </div>
          );
        })}
      </div>
      <hr />
      <FormHeader className={labelClassName} text={formLabel} />
    </div>
  )
}

const FormHeader = ({ className, text }) => {
  if (!text) return null;
  return (
    <h5 className={className || ""}>{text}</h5>
  );
}

export default StartSocialAuth