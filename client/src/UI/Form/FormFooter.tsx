import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonPrimary, ButtonDanger, ButtonSecondary } from "../Button"
import Spinner from "../Spinner"

interface IFormFooterProps {
  children?: React.ReactNode
  danger?: boolean
  submitText?: React.ReactNode
  disabled?: boolean
  loading?: boolean
  onCancel?: () => void
}

const FormFooter: React.FC<IFormFooterProps> = ({
  children,
  danger,
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
    {children}
    {submitText && (
      <>
        {danger ? (
          <ButtonDanger
            text={submitText}
            disabled={disabled || loading}
            responsive
          />
        ) : (
          <ButtonPrimary
            text={submitText}
            disabled={disabled || loading}
            responsive
          />
        )}
      </>
    )}
  </div>
)

export default FormFooter
