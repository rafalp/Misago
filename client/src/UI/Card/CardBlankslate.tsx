import React from "react"

interface CardBlankslateProps {
  header: React.ReactNode
  message?: React.ReactNode
  actions?: React.ReactNode
}

const CardBlankslate: React.FC<CardBlankslateProps> = ({
  actions,
  header,
  message,
}) => (
  <div className="card-body card-blank-slate">
    <div className="card-blank-slate-body">
      <div className="card-blank-slate-icon" />
      <div className="card-blank-slate-message">
        <p className="lead">{header}</p>
        {message && <p>{message}</p>}
        {actions && <div className="card-blank-slate-actions">{actions}</div>}
      </div>
    </div>
  </div>
)

export default CardBlankslate
