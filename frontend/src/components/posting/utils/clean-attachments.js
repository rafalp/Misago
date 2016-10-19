export default function(attachments) {
  const completedAttachments = attachments.filter((attachment) => {
    return attachment.id && !!attachment.isRemoved;
  });

  return completedAttachments.map((a) => { return a.id; });
}