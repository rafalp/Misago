import React from "react"
import misago from "misago"

const StartSocialAuth = (props) => {
  const { buttonClassName, buttonLabel, formLabel, header, labelClassName } =
    props
  const socialAuth = misago.get("SOCIAL_AUTH")

  if (socialAuth.length === 0) return null

  return (
    <div className="form-group form-social-auth">
      <FormHeader className={labelClassName} text={header} />
      <div className="row">
        {socialAuth.map(({ pk, name, button_text, button_color, url }) => {
          const className = "btn btn-block btn-default btn-social-" + pk
          const style = button_color ? { color: button_color } : null
          const finalButtonLabel =
            button_text || interpolate(buttonLabel, { site: name }, true)

          return (
            <div className={buttonClassName || "col-xs-12"} key={pk}>
              <a className={className} style={style} href={url}>
                {finalButtonLabel}
              </a>
            </div>
          )
        })}
      </div>
      <hr />
      <FormHeader className={labelClassName} text={formLabel} />
    </div>
  )
}

const FormHeader = ({ className, text }) => {
  if (!text) return null
  return <h5 className={className || ""}>{text}</h5>
}

export default StartSocialAuth
