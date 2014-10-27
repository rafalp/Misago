$(function() {

  YouTubeOnebox = function(href, movie_id, startfrom) {

    var _this = this;

    if (startfrom !== undefined) {
      player_url = '//www.youtube.com/embed/' + movie_id + '?start=' + startfrom + '&amp;autoplay=1';
    } else {
      player_url = '//www.youtube.com/embed/' + movie_id + '?autoplay=1';
    }

    this.$element = $('<div class="post-media"><div class="media-border youtube-player" data-movieid="' + movie_id + '"><div class="media-thumbnail" style="background-image: url(\'//img.youtube.com/vi/' + movie_id + '/0.jpg\');"><a href="' + href + '" class="play-link" data-playerurl="' + player_url + '"><i class="fa fa-youtube-play"></i><strong>' + lang_play_media + '</strong></a></div></div></div>');
    this.$element.find('.play-link').click(function() {
      $(this).parent().replaceWith('<iframe width="853" height="480" src="' + $(this).data('playerurl') + '" frameborder="0" allowfullscreen></iframe>');
      return false;
    });

    // Fetch title, author name and thumbnail
    $.getJSON("//gdata.youtube.com/feeds/api/videos/" + movie_id + "?v=2&alt=json",
      function(data, textStatus, jqXHR) {

        // Movie details
        var movie_title = data.entry.title.$t;
        var movie_author = data.entry.author['0'].name.$t
        _this.$element.find('.play-link').addClass('movie-title');
        _this.$element.find('.play-link strong').text(movie_title);
        _this.$element.find('.play-link').append(lang_media_author.replace('{author}', movie_author));

        // Movie thumbnail
        var thumb = {height: 90, url: '//img.youtube.com/vi/' + movie_id + '/0.jpg'};
        $(data.entry['media$group']['media$thumbnail']).each(function(key, yt_image) {
          if (thumb.height < yt_image.height) {
            thumb = yt_image;
          }
        });

        _this.$element.find('.media-thumbnail').css('background-image', "url('" + thumb.url + "')");

    });

    this.activate = function($element) {
      $element.replaceWith(this.$element.clone());
    }

  }

  MisagoOnebox = function() {

    this.boxes = {};

    var _this = this;

    this.youtube = function(href) {

      // Youtube link
      var re = /watch\?v=((\w|-)+)/;
      if (re.test(href)) {
        var media_url = href.match(re);
        return new YouTubeOnebox(href, media_url[1]);
      }

      // Youtube feature=embed
      var re = /watch\?feature=player_embedded&v=((\w|-)+)/;
      if (re.test(href)) {
        var media_url = href.match(re);
        return new YouTubeOnebox(href, media_url[1]);
      }

      // Youtube embed with start time
      var re = /youtu.be\/((\w|-)+)\?t=([A-Za-z0-9]+)/;
      if (re.test(href)) {
        var media_url = href.match(re);
        var media_minutes = media_url[2].match(/([0-9]+)m/);
        var media_seconds = media_url[2].match(/([0-9]+)s/);
        media_url[2] = 0;
        if (media_minutes) { media_url[2] += (media_minutes[1] - 0) * 60; }
        if (media_seconds) { media_url[2] += (media_seconds[1] - 0); }
        return new YouTubeOnebox(href, media_url[1], media_url[2]);
      }

      // Youtube embed
      var re = /youtu.be\/(([A-Za-z0-9]|_|-)+)/;
      if (re.test(href)) {
        var media_url = href.match(re);
        return new YouTubeOnebox(href, media_url[1]);
      }

      return false;
    }

    this.oneboxes = [this.youtube];

    this.activate = function($element) {

      $element.find('a').each(function() {

        var href = $.trim($(this).text());
        if (_this.boxes[href] === undefined) {
          $.each(_this.oneboxes, function(i, onebox) {
            _this.boxes[href] = _this.youtube(href);
            if (_this.boxes[href] != false) {
              return true;
            }
          })
        }

        if (_this.boxes[href] !== false) {
          _this.boxes[href].activate($(this));
        }

      });
    }

  };

  Misago.Onebox = new MisagoOnebox();

});
