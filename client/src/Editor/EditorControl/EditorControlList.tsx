import React from "react"
import Icon from "../../UI/Icon"
import { IEditorControlProps } from "./EditorControl.types"
import EditorButton from "../EditorButton"
import EditorControlListModal from "./EditorControlListModal"

const EditorControlList: React.FC<IEditorControlProps> = ({
  title,
  icon,
  context,
}) => {
  const { disabled } = context
  const [isOpen, setOpen] = React.useState(false)

  return (
    <>
      <EditorButton
        className="btn-editor-list"
        disabled={disabled}
        title={title}
        icon
        onClick={() => setOpen(true)}
      >
        <Icon icon={icon} fixedWidth />
      </EditorButton>
      <EditorControlListModal
        context={context}
        isOpen={isOpen}
        close={() => setOpen(false)}
      />
    </>
  )
}

export default EditorControlList
