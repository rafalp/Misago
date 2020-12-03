import { EmojiButton } from "@joeattardi/emoji-button"
import React from "react"
import Icon from "../../UI/Icon"
import { IEditorControlProps } from "./EditorControl.types"
import EditorButton from "../EditorButton"

const EditorControlEmoji: React.FC<IEditorControlProps> = ({
  title,
  icon,
  context,
}) => {
  const picker = React.useRef<EmojiButton | null>(null)
  const { textarea, disabled, replaceSelection } = context

  React.useEffect(() => {
    if (!textarea || disabled) return

    picker.current = new EmojiButton()
    picker.current.on("emoji", ({ emoji }) =>
      replaceSelection({ replace: emoji })
    )

    return () => {
      if (picker.current) picker.current.destroyPicker()
    }
  }, [picker, textarea, disabled])

  return (
    <EditorButton
      className="btn-editor-emoji"
      disabled={disabled}
      title={title}
      icon
      onClick={(event) => {
        if (picker.current) {
          picker.current.togglePicker(event.currentTarget)
        }
      }}
    >
      <Icon icon={icon} fixedWidth />
    </EditorButton>
  )
}

export default EditorControlEmoji
