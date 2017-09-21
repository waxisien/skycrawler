// requirements
var gulp = require('gulp');
var gulpBrowser = require("gulp-browser");
var reactify = require('reactify');
var del = require('del');
var size = require('gulp-size');
var mainBowerFiles = require('gulp-main-bower-files');
var inject = require('gulp-inject');

// tasks
gulp.task('transform', function () {
  var stream = gulp.src('./skycrawler/static/scripts/jsx/*.js')
    .pipe(gulpBrowser.browserify({transform: ['reactify']}))
    .pipe(gulp.dest('./skycrawler/static/scripts/js/'))
    .pipe(size());
  return stream;
});

gulp.task('del', function () {
    return del(['./skycrawler/static/scripts/js', './skycrawler/static/scripts/vendor']);
});

gulp.task('default', ['del'], function() {
  gulp.start('transform');
  gulp.start('build');
});

gulp.task('build', function () {
  // copy vendor files from /bower_compontents to /assets/vendors
  var bowerStreamJS = gulp.src('./bower.json')
        .pipe(mainBowerFiles('**/*.js'))
        .pipe(gulp.dest('./skycrawler/static/scripts/vendor'));

  // send bower bower scripts
  gulp.src('./skycrawler/templates/map.html')
  .pipe(
    inject(bowerStreamJS, {relative: true, name: 'bower'})
  )
  // save the file
  .pipe(
    gulp.dest('./skycrawler/templates')
  );
});


gulp.task('watch', function () {
  gulp.watch('./skycrawler/static/scripts/jsx/*.js', ['transform']);
});
