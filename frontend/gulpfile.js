'use strict';

var gulp = require('gulp');

var babelify = require('babelify');
var browserify = require('browserify');
var buffer = require('vinyl-buffer');
var imageop = require('gulp-image-optimization');
var jshint = require('gulp-jshint');
var less = require('gulp-less');
var minify = require('gulp-minify-css');
var rename = require('gulp-rename');
var source = require('vinyl-source-stream');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');

var glob = require('glob');
var del = require('del');

var misago = '../misago/static/misago/';

// Entry points

gulp.task('watch', ['fastbuild'], function() {
  gulp.watch('src/**/*.js', ['fastsource']);
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
  'copyzxcvbn'
]);

gulp.task('build', [
  'source',
  'style',
  'static',
  'vendorsources',
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
    .pipe(jshint())
    .pipe(jshint.reporter('default'));
});

gulp.task('fastsource', ['lintsource'], function() {
  return browserify({
      entries: getSources(),
      debug: true
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
    .pipe(less())
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
    .pipe(imageop({
      optimizationLevel: 9
    }))
    .pipe(gulp.dest(misago + 'img'));
});

gulp.task('faststatic', ['copyfonts', 'fastcopyimages']);

gulp.task('static', ['copyfonts', 'copyimages']);

// Vendor tasks

gulp.task('fastvendorsources', function() {
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

// Test task

var tests = (function() {
  var flag = process.argv.indexOf('--limit');
  var value = process.argv[flag + 1];

  var tests = ['src/test-setup.js'];
  if (flag !== -1 && value) {
    var pattern = value.trim();
    glob.sync('tests/**/*.js').map(function(path) {
      if (path.indexOf(pattern) !== -1) {
        tests.push(path);
      }
    });
  } else {
    tests.push('tests/**/*.js');
  }

  return tests;
})();

gulp.task('linttests', function() {
  return gulp.src(tests)
    .pipe(jshint())
    .pipe(jshint.reporter('default'));
});

gulp.task('test', ['linttests', 'lintsource'], function() {
  var mochify = require('mochify');

  mochify(tests.join(" "), {
      reporter: 'spec'
    })
    .transform(babelify)
    .bundle();
});
