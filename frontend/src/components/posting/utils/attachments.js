import moment from 'moment';

export function clean(attachments) {
  const completedAttachments = attachments.filter((attachment) => {
    return attachment.id && !attachment.isRemoved;
  });

  return completedAttachments.map((a) => { return a.id; });
}

export function hydrate(attachments) {
  return attachments.map((attachment) => {
    return Object.assign({}, attachment, {
      uploaded_on: moment(attachment.uploaded_on)
    });
  });
}