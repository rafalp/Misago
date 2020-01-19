import classNames from "classnames"
import React from "react"
import ModalHeader from "./ModalHeader"
import ModalTitle from "./ModalTitle"

interface IModalDialogProps {
  centered?: boolean
  children: React.ReactNode
  className?: string
  size?: "default" | "small" | "large" | "extra_large" | null
  title?: React.ReactNode
  close?: () => void
}

const ModalDialog: React.FC<IModalDialogProps> = ({
  centered,
  children,
  className,
  size,
  title,
  close,
}) => (
  <div
    className={classNames(
      "modal-dialog",
      {
        "modal-dialog-centered": centered,
        "modal-sm": size === "small",
        "modal-lg": size === "large",
        "modal-xl": size === "extra_large",
      },
      className
    )}
    role="document"
    onClick={e => e.stopPropagation()}
  >
    <div className="modal-content">
      {title && (
        <ModalHeader close={close}>
          <ModalTitle text={title} />
        </ModalHeader>
      )}
      {children}
    </div>
  </div>
)

export default ModalDialog
