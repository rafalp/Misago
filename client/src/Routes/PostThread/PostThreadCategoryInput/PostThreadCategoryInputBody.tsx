import React from "react"

interface IPostThreadCategoryInputBodyProps {
  children: React.ReactNode
}

const PostThreadCategoryInputBody: React.FC<IPostThreadCategoryInputBodyProps> = ({
  children,
}) => <div className="form-control-select-category">{children}</div>

export default PostThreadCategoryInputBody
