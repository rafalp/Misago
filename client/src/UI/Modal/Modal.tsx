import classNames from "classnames"
import React from "react"
import ModalBacktrop from "./ModalBacktrop"
import ModalDialog from "./ModalDialog"
import ModalHeader from "./ModalHeader"
import { ModalSize } from "./Modal.types"
import ModalTitle from "./ModalTitle"
import useTransition from "./useTransition"

interface IModalProps {
  centered?: boolean
  className?: string
  children: React.ReactNode
  isOpen: boolean
  resistant?: boolean
  size?: ModalSize
  title?: React.ReactNode
  close: () => void
}

const Modal: React.FC<IModalProps> = ({
  centered,
  children,
  className,
  isOpen,
  resistant = false,
  size = ModalSize.DEFAULT,
  title,
  close,
}) => {
  const { display, fade } = useTransition(isOpen)
  if (!display) return null

  return (
    <div onClick={resistant ? undefined : close}>
      <div
        className={classNames("modal", "d-block", "fade", { show: fade })}
        tabIndex={-1}
        role="dialog"
        aria-hidden={fade ? "false" : "true"}
        onKeyDown={({ keyCode }) => {
          if (keyCode === 27) close()
        }}
      >
        <ModalDialog className={className} centered={centered} size={size}>
          {title && (
            <ModalHeader close={close}>
              <ModalTitle text={title} />
            </ModalHeader>
          )}
          {children}
        </ModalDialog>
      </div>
      <ModalBacktrop fade={fade} onClick={resistant ? undefined : close} />
    </div>
  )
}

export default Modal
