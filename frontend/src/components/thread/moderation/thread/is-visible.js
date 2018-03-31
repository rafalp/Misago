export default function(thread) {
  return !!(
    (thread.acl.can_approve && thread.is_unapproved) ||
    thread.acl.can_close ||
    thread.acl.can_delete ||
    thread.acl.can_hide ||
    thread.acl.can_move ||
    thread.acl.can_merge ||
    thread.acl.can_pin ||
    (thread.acl.can_pin_globally && thread.weight !== 2) ||
    thread.acl.can_unhide
  );
}