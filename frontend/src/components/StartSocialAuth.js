import React from 'react'
import misago from 'misago'

const StartSocialAuth = ({ buttonLabel, formLabel, header }) => {
  const socialAuth = misago.get('SETTINGS').SOCIAL_AUTH;

  if (socialAuth.length === 0) return;

  return (
    <div className="form-group">
      <FormHeader text={header} />
      {socialAuth.map(({ id, name, url }) => {
        const className = 'btn btn-block btn-default btn-social-' + id;
        const finalButtonLabel = interpolate(buttonLabel, { site: name }, true);

        return (
          <a
            className={className}
            href={url}
            key={id}
          >
            {finalButtonLabel}
          </a>
        );
      })}
      <hr />
      <FormHeader text={formLabel} />
    </div>
  )
}

const FormHeader = ({ text }) => {
  if (!text) return null;
  return (
    <h5 className="text-center">{text}</h5>
  );
}

export default StartSocialAuth