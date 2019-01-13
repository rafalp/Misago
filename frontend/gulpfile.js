'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');

var babelify = require('babelify');
var browserify = require('browserify');
var buffer = require('vinyl-buffer');
var eslint = require('gulp-eslint');
var image = require('gulp-image');
var less = require('gulp-less');
var minify = require('gulp-minify-css');
var rename = require('gulp-rename');
var source = require('vinyl-source-stream');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var watchify = require('watchify');

var fs = require('fs');
var glob = require('glob');
var del = require('del');

var misago = '../misago/static/misago/';

// Entry points

gulp.task('watch', ['watchifybuild'], function() {
  gulp.watch('style/**/*.less', ['faststyle']);
});

gulp.task('watchstyle', ['faststyle', 'faststatic'], function() {
  gulp.watch('style/**/*.less', ['faststyle']);
});

// Builds

gulp.task('fastbuild', [
  'fastsource',
  'faststyle',
  'faststatic',
  'fastvendorsources',
  'copypolyfill',
  'copyzxcvbn'
]);

gulp.task('build', [
  'source',
  'style',
  'static',
  'vendorsources',
  'copypolyfill',
  'copyzxcvbn'
]);

// Source tasks

function getSources() {
  var sources = ['src/index.js'];

  function include(pattern) {
    var paths = glob.sync(pattern);
    paths.forEach(function(path) {
      sources.push(path);
    });
  };

  include('src/initializers/*.js');
  include('src/initializers/**/*.js');

  return sources.map(function(path) {
    return path;
  });
};

gulp.task('lintsource', function() {
  return gulp.src('src/**/*.js')
    .pipe(eslint({
        'parser': 'babel-eslint',
        'parserOptions': {
            'ecmaVersion': 7,
            'sourceType': 'module',
            'ecmaFeatures': {
                'jsx': true
            }
        },
        rules: {
          "semi": ["error", "never"],
          "no-undef": "error",
          "strict": 2
        },
        globals: [
          "gettext",
          "ngettext",
          "interpolate",
          "misago",
          "hljs"
        ],
        envs: [
            "browser",
            "jquery",
            "node",
            "es6"
        ]
    }))
    .pipe(eslint.format());
});

gulp.task('fastsource', ['lintsource'], function() {
  process.env.NODE_ENV = 'development';

  return browserify({
      entries: getSources(),
      debug: true,
    })
    .external('moment')
    .external('cropit')
    .external('react')
    .external('react-dom')
    .external('react-router')
    .external('redux')
    .external('react-redux')
    .transform(babelify)
    .bundle()
    .pipe(source('misago.js'))
    .pipe(buffer())
    .pipe(gulp.dest(misago + 'js'));
});

gulp.task('watchifybuild', ['fastbuild'], function() {
  process.env.NODE_ENV = 'development';

  var b = browserify({
      entries: getSources(),
      debug: true,
      cache: {},
      packageCache: {}
    })
    .plugin(watchify, {
      delay: 100,
      poll: true
    })
    .external('moment')
    .external('cropit')
    .external('react')
    .external('react-dom')
    .external('react-router')
    .external('redux')
    .external('react-redux')
    .transform(babelify)
    .on('error', function(err) {
      gutil.log(gutil.colors.red(err.toString() + '\n' + err.codeFrame));
      this.emit('end');
    });

    function bundle() {
      b.bundle()
        .on('error', function(err) {
          gutil.log(gutil.colors.red(err.toString() + '\n' + err.codeFrame));
          this.emit('end');
        })
        .pipe(fs.createWriteStream(misago + 'js/misago.js'));
    }

    b.on('update', bundle);
    bundle();

    b.on('log', function (msg) {
      gutil.log(gutil.colors.cyan('watchify:'), msg);
    });
})

gulp.task('source', ['lintsource'], function() {
  process.env.NODE_ENV = 'production';

  return browserify({
      entries: getSources(),
      debug: false
    })
    .external('moment')
    .external('cropit')
    .external('react')
    .external('react-dom')
    .external('react-router')
    .external('redux')
    .external('react-redux')
    .transform(babelify)
    .bundle()
    .pipe(source('misago.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init())
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(misago + 'js'));
});

// Styles tasks

gulp.task('cleanstyle', function(cb) {
  del(misago + 'css', cb);
});

gulp.task('faststyle', function() {
  return gulp.src('style/index.less')
    .pipe(less().on('error', function(err) {
        gutil.log(gutil.colors.red(err.toString()));
        this.emit('end');
      }))
    .pipe(rename('misago.css'))
    .pipe(gulp.dest(misago + 'css'));
});

gulp.task('style', function() {
  return gulp.src('style/index.less')
    .pipe(less())
    .pipe(minify())
    .pipe(rename('misago.css'))
    .pipe(gulp.dest(misago + 'css'));
});

// Static tasks

gulp.task('copyfonts', function(cb) {
  return gulp.src('static/fonts/**/*')
    .pipe(gulp.dest(misago + 'fonts'));
});

gulp.task('fastcopyimages', function() {
  return gulp.src('static/img/**/*')
    .pipe(gulp.dest(misago + 'img'));
});

gulp.task('copyimages', function() {
  return gulp.src('static/img/**/*')
    .pipe(image())
    .pipe(gulp.dest(misago + 'img'));
});

gulp.task('faststatic', ['copyfonts', 'fastcopyimages']);

gulp.task('static', ['copyfonts', 'copyimages']);

// Vendor tasks

gulp.task('fastvendorsources', function() {
  process.env.NODE_ENV = 'development';

  return browserify({
      entries: 'src/vendor.js',
      debug: true
    })
    .transform('browserify-shim')
    .require('moment')
    .require('cropit')
    .require('react')
    .require('react-dom')
    .require('react-router')
    .require('redux')
    .require('react-redux')
    .bundle()
    .pipe(source('vendor.js'))
    .pipe(buffer())
    .pipe(gulp.dest(misago + 'js'));
});

gulp.task('vendorsources', function() {
  process.env.NODE_ENV = 'production';

  return browserify({
      entries: 'src/vendor.js',
      debug: false
    })
    .transform('browserify-shim')
    .require('moment')
    .require('cropit')
    .require('react')
    .require('react-dom')
    .require('react-router')
    .require('redux')
    .require('react-redux')
    .transform(babelify)
    .bundle()
    .pipe(source('vendor.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init())
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(misago + 'js'));
});

gulp.task('copyzxcvbn', function() {
  return gulp.src('node_modules/zxcvbn/dist/*')
    .pipe(gulp.dest(misago + 'js'));
});

gulp.task('copypolyfill', function() {
  return gulp.src('node_modules/babel-polyfill/dist/polyfill.js')
    .pipe(rename('es2015.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init())
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(misago + 'js'));
});
