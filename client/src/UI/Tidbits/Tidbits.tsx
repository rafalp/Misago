import classNames from "classnames"
import React from "react"

interface ITidbitsProps {
  children?: React.ReactNode
  small?: boolean
  vertical?: boolean
}

const Tidbits: React.FC<ITidbitsProps> = ({ children, small, vertical }) => (
  <ul
    className={classNames("list-tidbits", {
      "list-inline": !vertical,
      "list-unstyled": vertical,
      "tidbits-small": small,
    })}
  >
    {children}
  </ul>
)

export default Tidbits
