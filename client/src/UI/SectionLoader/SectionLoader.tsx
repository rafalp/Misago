import classnames from "classnames"
import React from "react"
import Spinner from "../Spinner"

interface ISectionLoaderProps {
  loading?: boolean
  children: React.ReactNode
}

const SectionLoader: React.FC<ISectionLoaderProps> = ({
  children,
  loading,
}) => (
  <div className={classnames("section-loader", { active: loading })}>
    <div className="section-loader-content">{children}</div>
    <div className="section-loader-backtrop">
      <div className="section-loader-overlay">
        <div className="section-loader-spinner-body">
          <div className="section-loader-spinner">
            <Spinner />
          </div>
        </div>
      </div>
    </div>
  </div>
)

export default SectionLoader
