import { t } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import classnames from "classnames"
import React from "react"
import ModalTitle from "./ModalTitle"

interface IModalHeaderProps {
  children?: React.ReactNode
  className?: string
  title?: React.ReactNode
  close?: () => void
}

const ModalHeader: React.FC<IModalHeaderProps> = ({
  children,
  className,
  close,
  title,
}) => {
  const { i18n } = useLingui()

  return (
    <div className={classnames("modal-header", className)}>
      {title && <ModalTitle text={title} />}
      {children}
      {close && (
        <button
          className="close"
          data-dismiss="modal"
          type="button"
          aria-label={i18n._("close", t`Close`)}
          onClick={close}
        >
          <span aria-hidden="true">&times;</span>
        </button>
      )}
    </div>
  )
}

export default ModalHeader
