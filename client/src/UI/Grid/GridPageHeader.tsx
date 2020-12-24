import React from "react"
import PageTitle from "../PageTitle"

interface GridPageHeaderProps {
  actions?: Array<React.ReactNode>
  title: React.ReactNode
  tidbits?: React.ReactNode
}

const GridPageHeader: React.FC<GridPageHeaderProps> = ({
  actions,
  title,
  tidbits,
}) => (
  <div className="row align-items-center row-page-header">
    <div className="col-12 col-lg col-page-title">
      <PageTitle text={title} />
    </div>
    {tidbits && (
      <div className="col-12 col-lg-auto col-tidbits">{tidbits}</div>
    )}
    {actions &&
      actions.map((action, i) =>
        action ? (
          <div className="col-auto col-action" key={i}>
            {action}
          </div>
        ) : null
      )}
  </div>
)

export default GridPageHeader
