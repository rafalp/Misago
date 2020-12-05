import React from "react"
import Icon from "../../UI/Icon"
import { IEditorControlProps } from "./EditorControl.types"
import EditorButton from "../EditorButton"
import EditorControlImageModal from "./EditorControlImageModal"

const EditorControlImage: React.FC<IEditorControlProps> = ({
  title,
  icon,
  context,
}) => {
  const { disabled } = context
  const [isOpen, setOpen] = React.useState(false)

  return (
    <>
      <EditorButton
        className="btn-editor-image"
        disabled={disabled}
        title={title}
        icon
        onClick={() => setOpen(true)}
      >
        <Icon icon={icon} fixedWidth />
      </EditorButton>
      <EditorControlImageModal
        context={context}
        isOpen={isOpen}
        close={() => setOpen(false)}
      />
    </>
  )
}

export default EditorControlImage
