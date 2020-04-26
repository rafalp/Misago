import classNames from "classnames"
import React from "react"
import { ModalSize } from "./Modal.types"
import ModalHeader from "./ModalHeader"
import ModalTitle from "./ModalTitle"

interface IModalDialogProps {
  centered?: boolean
  children: React.ReactNode
  className?: string
  size?: ModalSize
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
        "modal-sm": size === ModalSize.SMALL,
        "modal-lg": size === ModalSize.LARGE,
        "modal-xl": size === ModalSize.EXTRA_LARGE,
      },
      className
    )}
    role="document"
    onClick={(e) => e.stopPropagation()}
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
