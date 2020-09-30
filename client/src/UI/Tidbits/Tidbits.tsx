import classnames from "classnames"
import React from "react"

interface ITidbitsProps {
  children?: React.ReactNode
  vertical?: boolean
}

const Tidbits: React.FC<ITidbitsProps> = ({ children, vertical }) => (
  <ul
    className={classnames(
      "tidbits",
      vertical ? "list-unstyled" : "list-inline"
    )}
  >
    {children}
  </ul>
)

export default Tidbits
