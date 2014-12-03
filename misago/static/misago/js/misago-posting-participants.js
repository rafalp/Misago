Misago.participants = function($e) {

  this.$users = $e.find('.users-list');
  this.$input = $e.find('.user-input');
  this.$value = $e.find('input[type=hidden]');

  this.api_url = this.$input.data('api-url');
  this.csrf_token = $e.parents('form').find("input[name=csrfmiddlewaretoken]").val()

  var _this = this;

  this.add_user = function(user) {

    if (!this.$users.find('.user-' + user.username).length) {
      var $user = $('<li class="user-' + user.username + '" data-username="' + user.username + '">' + user.username + '</li>');
      var $cancel = $('<button type="button" class="btn btn-sm"><span class="fa fa-times"></span></button>')

      $cancel.click(function() {
        $cancel.parent().remove();
        _this.update_val();
      });

      var $avatar = $('<img src="' + user.avatar[Object.keys(user.avatar)[0]] + '" alt="">');

      $user.prepend($avatar);
      $user.append($cancel);

      this.$users.append($user);
      this.update_val();
    }

  }

  this.update_val = function() {

    var usernames = [];

    this.$users.find('li').each(function(index, el) {
      usernames.push($(el).data('username'));
    });

    this.$value.val(usernames.join(',', usernames));

  }

  this.$input.typeahead({
      minLength: 2,
      hint: false,
    },
    {
      name: 'profiles',
      displayKey: 'username',
      source: function(query, cb) {
        var POST = {'username': query, 'csrfmiddlewaretoken': _this.csrf_token};
        return $.post(_this.api_url, POST, function (data) {
          return cb(data.profiles);
        });
      },
      templates: {
        suggestion: function(data) {
          return '<img src="' + data.avatar[Object.keys(data.avatar)[0]] + '" alt=""> ' + data.username;
        }
      }
    });

  this.$input.on('typeahead:selected', function(e, suggestion, dataset) {

    _this.$input.typeahead('val', '');
    _this.add_user(suggestion);

  });
}
