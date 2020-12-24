import { t } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import ModalTitle from "./ModalTitle"

interface ModalHeaderProps {
  children?: React.ReactNode
  className?: string
  title?: React.ReactNode
  close?: () => void
}

const ModalHeader: React.FC<ModalHeaderProps> = ({
  children,
  className,
  close,
  title,
}) => (
  <div className={classnames("modal-header", className)}>
    {title && <ModalTitle text={title} />}
    {children}
    {close && (
      <button
        className="close"
        data-dismiss="modal"
        type="button"
        aria-label={t({ id: "close", message: "Close" })}
        onClick={close}
      >
        <span aria-hidden="true">&times;</span>
      </button>
    )}
  </div>
)

export default ModalHeader
