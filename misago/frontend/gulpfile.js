var static_path = '../static/misago/';

var packageJSON  = require('./package');

var gulp = require('gulp');

var concat = require('gulp-concat');
var connect = require('gulp-connect');
var jshint = require('gulp-jshint');
var less = require('gulp-less');
var minify = require('gulp-minify-css');
var open = require('gulp-open');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');

var del = require('del');

var vendors = [
  'bower_components/jquery/dist/jquery.js',
  'bower_components/mithril/mithril.js',

  'bower_components/bootstrap/js/transition.js',
  'bower_components/bootstrap/js/affix.js',
  'bower_components/bootstrap/js/modal.js'
];

var ace = [
  'bower_components/ace-builds/src/ace.js',
  'bower_components/ace-builds/src/mode-markdown.js'
];

gulp.task('lint', function() {
  return gulp.src(['misago/*.js', 'misago/**/*.js'])
    .pipe(jshint(packageJSON.jshintConfig))
    .pipe(jshint.reporter('default'));
});

gulp.task('misagojs', ['lint'], function() {
  return gulp.src([
      'misago/app.js',
      'misago/components/**/*.js',
      'misago/models/*.js',
      'misago/services/*.js',
      'misago/templates/**/*.js',
      'misago/utils/**/*.js',
    ])
    .pipe(concat('misago.js'))
    .pipe(gulp.dest('dist'));
});

gulp.task('vendorjs', function() {
  return gulp.src(vendors)
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest('dist'));
});

gulp.task('acejs', function() {
  return gulp.src(ace)
    .pipe(concat('ace.js'))
    .pipe(gulp.dest('dist'));
});

gulp.task('collectjs', ['vendorjs', 'misagojs', 'acejs'], function() {
  return gulp.src('dist/*.js')
    .pipe(gulp.dest('dist/js'));
});

gulp.task('compressjs', ['collectjs'], function() {
  return gulp.src('dist/js/*.js')
    .pipe(sourcemaps.init())
      .pipe(uglify())
    .pipe(sourcemaps.write('/'))
    .pipe(gulp.dest('dist/js'));
});

gulp.task('compileless', function() {
  return gulp.src('misago/style/misago.less')
    .pipe(less())
    .pipe(gulp.dest('dist'));
});

gulp.task('collectcss', ['compileless'], function() {
  return gulp.src('dist/*.css')
    .pipe(gulp.dest('dist/css'));
});

gulp.task('compresscss', ['collectcss'], function() {
  return gulp.src('dist/css/*.css')
    .pipe(minify())
    .pipe(gulp.dest('dist/css'));
});

gulp.task('copyfonts', function() {
  return gulp.src('static/fonts/**/*')
    .pipe(gulp.dest('dist/fonts'));
});

gulp.task('copyimg', function() {
  return gulp.src('static/img/**/*')
    .pipe(gulp.dest('dist/img'));
});

gulp.task('cleanprod', function(cb) {
  del([
    static_path + 'css',
    static_path + 'js',
    static_path + 'fonts',
    static_path + 'img'
  ], {force: true}, cb);
});

gulp.task('prepareprod', ['cleanprod', 'compressjs', 'compresscss', 'copyfonts', 'copyimg']);

gulp.task('deployjs', ['prepareprod'], function() {
  return gulp.src('dist/js/**/*')
    .pipe(gulp.dest(static_path + 'js'));
})

gulp.task('deploycss', ['prepareprod'], function() {
  return gulp.src('dist/css/**/*')
    .pipe(gulp.dest(static_path + 'css'));
})

gulp.task('deployfonts', ['prepareprod'], function() {
  return gulp.src('dist/fonts/**/*')
    .pipe(gulp.dest(static_path + 'fonts'));
})

gulp.task('deployimg', ['prepareprod'], function() {
  return gulp.src('dist/img/**/*')
    .pipe(gulp.dest(static_path + 'img'));
})

gulp.task('default', ['deployjs', 'deploycss', 'deployfonts', 'deployimg']);


gulp.task('quickdeployjs', ['collectjs'], function() {
  return gulp.src('dist/js/**/*')
    .pipe(gulp.dest(static_path + 'js'));

});

gulp.task('quickdeploycss', ['collectcss'], function() {
  return gulp.src('dist/css/**/*')
    .pipe(gulp.dest(static_path + 'css'));
});

gulp.task('watch', ['default'], function() {
   gulp.watch('misago/**/*.js', ['quickdeployjs']);
   gulp.watch('misago/**/*.less', ['quickdeploycss']);
});

gulp.task('cleantest', function(cb) {
  del('test/dist', cb);
});

gulp.task('collecttestjs', ['cleantest', 'collectjs'], function() {
  return gulp.src('dist/js/**/*')
    .pipe(gulp.dest('test/dist/js'));
});

gulp.task('collecttestcss', ['cleantest', 'collectcss'], function() {
  return gulp.src('dist/css/**/*')
    .pipe(gulp.dest('test/dist/css'));
});

gulp.task('collecttestfonts', ['cleantest', 'copyfonts'], function() {
  return gulp.src('dist/fonts/**/*')
    .pipe(gulp.dest('test/dist/fonts'));
});

gulp.task('collecttestimg', ['cleantest', 'copyimg'], function() {
  return gulp.src('dist/img/**/*')
    .pipe(gulp.dest('test/dist/img'));
});

gulp.task('collecttestsutils', ['cleantest'], function() {
  return gulp.src('test/utils/**/*.js')
    .pipe(jshint(packageJSON.jshintConfig))
    .pipe(jshint.reporter('default'))
    .pipe(jshint.reporter('fail'))
    .pipe(concat('utils.js'))
    .pipe(gulp.dest('test/dist'));
});

gulp.task('collecttests', ['cleantest'], function() {
  return gulp.src('test/tests/**/*.js')
    .pipe(jshint(packageJSON.jshintConfig))
    .pipe(jshint.reporter('default'))
    .pipe(jshint.reporter('fail'))
    .pipe(concat('tests.js'))
    .pipe(gulp.dest('test/dist'));
});

gulp.task('starttestserver', ['collecttests', 'collecttestsutils', 'collecttestjs', 'collecttestcss', 'collecttestfonts', 'collecttestimg'], function() {
  connect.server({
    port: 8080,
    root: 'test'
  });

  gulp.src(__filename)
    .pipe(open({ uri: 'http://127.0.0.1:8080/' }));
});

gulp.task('test', ['starttestserver'], function() {
  gulp.watch([
    'test/tests/**/*.js', 'misago/**/*.js', 'misago/**/*.less'
  ], [
    'collecttests', 'collecttestjs', 'collecttestcss'
  ]);
});
