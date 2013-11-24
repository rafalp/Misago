// Basic editor functions
<<<<<<< HEAD
function storeCaret(ftext) {
=======
function storeCaret(ftext) {    
>>>>>>> master
  if (ftext.createTextRange) {
    ftext.caretPos = document.selection.createRange().duplicate();
  }
}

function SelectionRange(start, end) {
  this.start = start;
  this.end = end;
}

function getSelection(textId) {
  ctrl = document.getElementById(textId);
  if (document.selection) {
    ctrl.focus();
    var range = document.selection.createRange();
    var length = range.text.length;
    range.moveStart('character', -ctrl.value.length);
    return new SelectionRange(range.text.length - length, range.text.length);
  } else if (ctrl.selectionStart || ctrl.selectionStart == '0') {
    return new SelectionRange(ctrl.selectionStart, ctrl.selectionEnd);
  }
}

function getSelectionText(textId) {
  var ctrl = document.getElementById(textId);
  var text = ctrl.value;
  myRange = getSelection(textId);
  return $.trim(text.substring(myRange.start, myRange.end));
}

function setSelection(textId, SelectionRange) {
  ctrl = document.getElementById(textId);
  if (ctrl.setSelectionRange) {
    ctrl.focus();
    ctrl.setSelectionRange(SelectionRange.start, SelectionRange.end);
  } else if (ctrl.createTextRange) {
    var range = ctrl.createTextRange();
    range.collapse(true);
    range.moveStart('character', SelectionRange.start);
    range.moveEnd('character', SelectionRange.end);
    range.select();
  }
}

function _makeWrap(textId, myRange, wrap_start, wrap_end) {
  var ctrl = document.getElementById(textId);
  var text = ctrl.value;
  var startText = text.substring(0, myRange.start) + wrap_start;
  var middleText = text.substring(myRange.start, myRange.end);
  var endText = wrap_end + text.substring(myRange.end);
  ctrl.value = startText + middleText + endText;
  setSelection(textId, new SelectionRange(startText.length, startText.length + middleText.length));
}

function makeWrap(textId, wrap_start, wrap_end) {
  _makeWrap(textId, getSelection(textId), wrap_start, wrap_end);
}

function _makeReplace(textId, myRange, replacement) {
  var ctrl = document.getElementById(textId);
  var text = ctrl.value;
  var startText = text.substring(0, myRange.start);
  var middleText = text.substring(myRange.start, myRange.end);
  var endText = text.substring(myRange.end);
  ctrl.value = text.substring(0, myRange.start) + replacement + text.substring(myRange.end);
  setSelection(textId, new SelectionRange(startText.length + middleText.length, startText.length + middleText.length));
}

function makeReplace(textId, replacement) {
  _makeReplace(textId, getSelection(textId), replacement);
}

var url_pattern = new RegExp('^(https?:\\/\\/)?((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|((\\d{1,3}\\.){3}\\d{1,3}))(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*(\\?[;&a-z\\d%_.~+=-]*)?(\\#[-a-z\\d_]*)?$','i');
function is_url(str) {
  return url_pattern.test($.trim(str));
}

function extractor(query) {
    var result = /([^\s]+)$/.exec(query);
    if(result && result[1])
        return result[1].trim();
    return '';
}

// Small and nice editor functionality
$(function() {
<<<<<<< HEAD
  function textarea(ev) {
    return $(ev).parents('.editor-editable').find('textarea');
  }

  function textareaId(ev) {
    return textarea(ev).attr('id');
  }

  $('.editor-tools').fadeIn(600);
  $('.editor-zen-on').css('display', 'block');
  $('.editor-editable').each(function() {
    // Do we have emojis?
    if (ed_emojis.length > 1) {
      $(this).find('textarea').atwho({
        at: ":",
        tpl: ed_emoji_tpl,
        data: ed_emojis_list
      });
    }
  });

  // Handle buttons
  $('.editor-zen-on a').click(function() {
    var overlay = $('.zen-overlay');
    var overlay_textarea = overlay.find('textarea');
    overlay_textarea.val(textarea(this).val());
    overlay_textarea.data('org', '#' + textareaId(this));
    overlay_textarea.data('pos', $('body').scrollTop());
    overlay.show();
    $('#wrap').hide();
    return false;
  });

  $('.editor-bold').click(function() {
    makeWrap(textareaId(this), '**', '**');
    return false;
  });

  $('.editor-emphasis').click(function() {
    makeWrap(textareaId(this), '*', '*');
    return false;
  });

  $('.editor-link').click(function() {
    var selection = $.trim(getSelectionText(textareaId(this)));
    if (is_url(selection)) {
      var link_url = $.trim(prompt(ed_lang_enter_link_url, selection));
      selection = false;
    } else {
      var link_url = $.trim(prompt(ed_lang_enter_link_url));
    }

    if (is_url(link_url)) {
      if (selection) {
        var link_label = $.trim(prompt(ed_lang_enter_link_label, selection));
      } else {
        var link_label = $.trim(prompt(ed_lang_enter_link_label));
      }

      if (link_label.length > 0) {
        makeReplace(textareaId(this), '[' + link_label + '](' + link_url + ')');
      } else {
        makeReplace(textareaId(this), '<' + link_url + '>');
      }
    }

    return false;
  });

  $('.editor-image').click(function() {
    var selection = $.trim(getSelectionText(textareaId(this)));
    if (is_url(selection)) {
      var image_url = $.trim(prompt(ed_lang_enter_image_url, selection));
      selection = false;
    } else {
      var image_url = $.trim(prompt(ed_lang_enter_image_url));
    }

    if (is_url(image_url)) {
      if (selection) {
        var image_label = $.trim(prompt(ed_lang_enter_image_label, selection));
      } else {
        var image_label = $.trim(prompt(ed_lang_enter_image_label));
      }

      if (image_label.length > 0) {
        makeReplace(textareaId(this), '![' + image_label + '](' + image_url + ')');
      } else {
        makeReplace(textareaId(this), '!(' + image_url + ')');
      }
    }

    return false;
  });

  $('.editor-hr').click(function() {
    makeReplace(textareaId(this), '\r\n\r\n- - - - -\r\n\r\n');
    return false;
  });

  $('.editor-zen-off a').click(function() {
    var overlay = $('.zen-overlay');
    var overlay_textarea = overlay.find('textarea');
    var scrooltop = overlay.find('textarea').data('pos');

    $(overlay.find('textarea').data('org')).val(overlay.find('textarea').val());
    $('#wrap').show();
    $('html, body').scrollTop(scrooltop);
    overlay.hide();
    return false;
  });

  $('.editor-insert-attachment').click(function() {
    var insertion_code = $(this).data('attachment-md');
    makeReplace(textareaId(this), insertion_code);
=======
  $('.editor-tools').fadeIn(600);
  $('.editor').each(function() {
    // Get textarea stuff
    var textarea = $(this).find('textarea');
    var textarea_id = $(textarea).attr('id');
    
    // Do we have emojis?
    if (1==2 && ed_emojis.length > 1) {
      var mode = 0;
      var open = -1;

      $(textarea).focusout(function() {
        mode = 0;
        open = -1;
      });

      $(textarea).keyup(function() {
        text = $(textarea).val();
        cursor = getSelection(textarea_id).start;
        if (cursor > 0) {
          // Read typed character and previous character
          input = text.substring(cursor - 1, cursor);
          if (cursor > 1) {
            pre = text.substring(cursor - 2, cursor - 1);
          } else {
            pre = '';
          }

          // Act accordingly to current mode
          if (mode == 0) {
            if (input == ':' && !pre.match(/^[A-Za-z0-9]+$/i)) {
              // Test passed, mode 1 engaged!
              mode = 1;
              open = cursor;
            }
          } else if (mode == 1) {
            // Inside emoji mode, we are helping user enter emoji input
            if (cursor > open && !input.match(/^(\+|\-|[_A-Za-z0-9])+$/i)) {
              // Emoji fail
              mode = 0;
            }
          }
        }
      });
    }

    // Handle buttons
    $('.editor-bold').click(function() {
      makeWrap(textarea_id, '**', '**');
      return false;
    });
    
    $('.editor-emphasis').click(function() {
      makeWrap(textarea_id, '*', '*');
      return false;
    });
    
    $('.editor-link').click(function() {
      var selection = $.trim(getSelectionText(textarea_id));
      if (is_url(selection)) {
        var link_url = $.trim(prompt(ed_lang_enter_link_url, selection));
        selection = false;
      } else {
        var link_url = $.trim(prompt(ed_lang_enter_link_url));
      }

      if (is_url(link_url)) {
        if (selection) {
          var link_label = $.trim(prompt(ed_lang_enter_link_label, selection));
        } else {
          var link_label = $.trim(prompt(ed_lang_enter_link_label));
        }

        if (link_label.length > 0) {
          makeReplace(textarea_id, '[' + link_label + '](' + link_url + ')');
        } else {
          makeReplace(textarea_id, '<' + link_url + '>');
        }
      }

      return false;
    });
    
    $('.editor-image').click(function() {
      var selection = $.trim(getSelectionText(textarea_id));
      if (is_url(selection)) {
        var image_url = $.trim(prompt(ed_lang_enter_image_url, selection));
        selection = false;
      } else {
        var image_url = $.trim(prompt(ed_lang_enter_image_url));
      }

      if (is_url(image_url)) {
        if (selection) {
          var image_label = $.trim(prompt(ed_lang_enter_image_label, selection));
        } else {
          var image_label = $.trim(prompt(ed_lang_enter_image_label));
        }

        if (image_label.length > 0) {
          makeReplace(textarea_id, '![' + image_label + '](' + image_url + ')');
        } else {
          makeReplace(textarea_id, '!(' + image_url + ')');
        }
      }

      return false;
    });
    
    $('.editor-hr').click(function() {
      makeReplace(textarea_id, '\r\n\r\n- - - - -\r\n\r\n');
      return false;
    });
>>>>>>> master
  });
});