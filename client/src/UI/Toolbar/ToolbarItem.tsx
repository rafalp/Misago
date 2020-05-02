import React from "react"

interface IToolbarItemProps {
  children: React.ReactNode
  fill?: boolean
}

const ToolbarItem: React.FC<IToolbarItemProps> = ({ children, fill }) => (
  <div className={fill ? "col toolbar-item" : "col-auto toolbar-item"}>
    {children}
  </div>
)

export default ToolbarItem
