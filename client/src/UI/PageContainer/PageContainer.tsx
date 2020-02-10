import classNames from "classnames"
import React from "react"

interface IPageContainerProps {
  children: React.ReactNode
  className?: string | null
}

const PageContainer: React.FC<IPageContainerProps> = ({
  children,
  className,
}) => (
  <div className={classNames("page-container", className)}>
    <div className="container-fluid">{children}</div>
  </div>
)

export default PageContainer
