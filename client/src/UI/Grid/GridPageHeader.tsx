import React from "react"
import PageTitle from "../PageTitle"

interface IGridPageHeaderProps {
  title: React.ReactNode
  sideTidbits?: React.ReactNode | null
}

const GridPageHeader: React.FC<IGridPageHeaderProps> = ({
  title,
  sideTidbits,
}) => (
  <div className="row align-items-center row-page-header">
    <div className="col-12 col-lg col-page-title">
      <PageTitle text={title} />
    </div>
    {sideTidbits && (
      <div className="col-12 col-lg-auto col-side-tidbits">{sideTidbits}</div>
    )}
  </div>
)

export default GridPageHeader
