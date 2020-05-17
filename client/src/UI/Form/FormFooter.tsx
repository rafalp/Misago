import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonPrimary, ButtonSecondary } from "../Button"
import Spinner from "../Spinner"

interface IFormFooterProps {
  submitText: React.ReactNode
  disabled?: boolean
  loading?: boolean
  onCancel?: () => void
}

const FormFooter: React.FC<IFormFooterProps> = ({
  submitText,
  disabled,
  loading,
  onCancel,
}) => (
  <div className="form-footer">
    {loading && <Spinner small />}
    {onCancel && (
      <ButtonSecondary
        text={<Trans id="cancel">Cancel</Trans>}
        disabled={disabled || loading}
        responsive
        onClick={onCancel}
      />
    )}
    <ButtonPrimary
      text={submitText}
      disabled={disabled || loading}
      responsive
    />
  </div>
)

export default FormFooter
