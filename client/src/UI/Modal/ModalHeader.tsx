import { I18n } from "@lingui/react"
import { t } from "@lingui/macro"
import classNames from "classnames"
import React from "react"

interface IModalHeaderProps {
  children?: React.ReactNode
  className?: string
  close?: () => void
}

const ModalHeader: React.FC<IModalHeaderProps> = ({ children, className, close }) => (
  <I18n>
    {({ i18n }) => (
      <div className={classNames("modal-header", className)}>
        {children}
        {close && (
          <button
            className="close"
            data-dismiss="modal"
            type="button"
            aria-label={i18n._(t("modal.close")`Close`)}
            onClick={close}
          >
            <span aria-hidden="true">&times;</span>
          </button>
        )}
      </div>
    )}
  </I18n>
)

export default ModalHeader
