import React from "react"
import PostingFormHeaderButton from "./PostingFormHeaderButton"

interface IPostingFormHeaderProps {
  children: React.ReactNode
  fullscreen?: boolean
  minimized?: boolean
  setFullscreen: (state: boolean) => void
  setMinimized: (state: boolean) => void
}

const PostingFormHeader: React.FC<IPostingFormHeaderProps> = ({
  children,
  fullscreen,
  minimized,
  setFullscreen,
  setMinimized,
}) => (
  <div className="posting-form-header">
    <h5 className="posting-form-title">{children}</h5>
    <PostingFormHeaderButton
      className="btn-posting-form-minimize"
      icon={minimized ? "far fa-window-maximize" : "fas fa-window-minimize"}
      onClick={() => {
        setFullscreen(false)
        setMinimized(!minimized)
      }}
    />
    <PostingFormHeaderButton
      className="btn-posting-form-maximize"
      icon={fullscreen && !minimized ? "fas fa-compress" : "fas fa-expand"}
      onClick={() => {
        setMinimized(false)
        if (minimized) {
          setFullscreen(true)
        } else {
          setFullscreen(!fullscreen)
        }
      }}
    />
  </div>
)

export default PostingFormHeader
