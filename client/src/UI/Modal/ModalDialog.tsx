import classNames from "classnames"
import React from "react"
import { ModalSize } from "./Modal.types"

interface IModalDialogProps {
  centered?: boolean
  children: React.ReactNode
  className?: string
  size: ModalSize
}

const ModalDialog: React.FC<IModalDialogProps> = ({ centered, children, className, size }) => (
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
    onClick={e => e.stopPropagation()}
  >
    <div className="modal-content">{children}</div>
  </div>
)

export default ModalDialog
