import React from "react"
import misago from "misago"
import escapeHtml from "misago/utils/escape-html"

const AGREEMENT_URL = '<a href="%(url)s" target="_blank">%(agreement)s</a>'

const RegisterLegalFootnote = (props) => {
  const {
    errors,
    privacyPolicy,
    termsOfService,
    onPrivacyPolicyChange,
    onTermsOfServiceChange,
  } = props

  const termsOfServiceId = misago.get("TERMS_OF_SERVICE_ID")
  const termsOfServiceUrl = misago.get("TERMS_OF_SERVICE_URL")

  const privacyPolicyId = misago.get("PRIVACY_POLICY_ID")
  const privacyPolicyUrl = misago.get("PRIVACY_POLICY_URL")

  if (!termsOfServiceId && !privacyPolicyId) return null

  return (
    <div>
      <LegalAgreement
        agreement={pgettext(
          "register form agreement prompt",
          "the terms of service"
        )}
        checked={termsOfService !== null}
        errors={errors.termsOfService}
        url={termsOfServiceUrl}
        value={termsOfServiceId}
        onChange={onTermsOfServiceChange}
      />
      <LegalAgreement
        agreement={pgettext(
          "register form agreement prompt",
          "the privacy policy"
        )}
        checked={privacyPolicy !== null}
        errors={errors.privacyPolicy}
        url={privacyPolicyUrl}
        value={privacyPolicyId}
        onChange={onPrivacyPolicyChange}
      />
    </div>
  )
}

const LegalAgreement = (props) => {
  const { agreement, checked, errors, url, value, onChange } = props

  if (!url) return null

  const agreementHtml = interpolate(
    AGREEMENT_URL,
    { agreement: escapeHtml(agreement), url: escapeHtml(url) },
    true
  )
  const label = interpolate(
    pgettext(
      "register form agreement prompt",
      "I have read and accept %(agreement)s."
    ),
    { agreement: agreementHtml },
    true
  )

  return (
    <div className="checkbox legal-footnote">
      <label>
        <input
          checked={checked}
          type="checkbox"
          value={value}
          onChange={onChange}
        />
        <span dangerouslySetInnerHTML={{ __html: label }} />
      </label>
      {errors &&
        errors.map((error, i) => (
          <div className="help-block errors" key={i}>
            {error}
          </div>
        ))}
    </div>
  )
}

export default RegisterLegalFootnote
