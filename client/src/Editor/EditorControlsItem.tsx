import React from "react"
import EditorControlButton from "./EditorControl/EditorControlButton"
import { EditorContext } from "./EditorContext"
import { EditorControl } from "./EditorControl"

interface EditorControlsItemProps extends EditorControl {
  disabled?: boolean
}

const EditorControlsItem: React.FC<EditorControlsItemProps> = ({
  component: Component,
  disabled,
  icon,
  title,
  name,
  onClick,
}) => (
  <EditorContext.Consumer>
    {(context) =>
      Component ? (
        <Component context={context} name={name} icon={icon} title={title} />
      ) : (
        <EditorControlButton
          disabled={disabled}
          name={name}
          icon={icon}
          title={title}
          onClick={() => {
            if (onClick && !context.disabled) onClick(context)
          }}
        />
      )
    }
  </EditorContext.Consumer>
)

export default EditorControlsItem
