var gulp = require('gulp');
var sass = require('gulp-sass');
var browserSync = require('browser-sync');
var useref = require('gulp-useref');
var uglify = require('gulp-uglify');
var gulpIf = require('gulp-if');
var imagemin = require('gulp-imagemin');
var cache = require('gulp-cache');
var del = require('del');
var runSequence = require('run-sequence');


gulp.task('hello', function () {
  console.log('Hello Zell!');
});

// Development Tasks 
// -----------------

// Start browserSync server
gulp.task('browserSync', function() {
  browserSync({
    server: {
      baseDir: 'app'
    }
  });
});


gulp.task('sass', function() {
  return gulp.src('site/scss/*.scss') // Gets all files ending with .scss in app/scss and children dirs
    .pipe(sass().on('error', sass.logError)) // Passes it through a gulp-sass, log errors to console
    .pipe(sass({outputStyle: 'compressed'}))
    .pipe(gulp.dest('site/css')) // Outputs it in the css folder
    .pipe(browserSync.reload({ // Reloading with Browser Sync
      stream: true
    }));
})



// Watchers
gulp.task('watch', function() {
  gulp.watch('site/scss/*.scss', ['sass']);
  gulp.watch('*.php', browserSync.reload);
  gulp.watch('site/js/*.js', browserSync.reload);
});

// Optimization Tasks 
// ------------------

// Optimizing CSS and JavaScript 
gulp.task('useref', function() {

  return gulp.src('*.html')
    .pipe(useref())
    .pipe(gulpIf('site/*.js', uglify()))
    .pipe(gulp.dest('dist'));
});



// Optimizing Images 
gulp.task('images', function() {
  return gulp.src('site/img/*.+(png|jpg|jpeg|gif|svg)')
    // Caching images that ran through imagemin
    .pipe(cache(imagemin({
      interlaced: true,
    })))
    .pipe(gulp.dest('site/img'));
});

// Copying fonts 
gulp.task('fonts', function() {
  return gulp.src('site/fonts/*')
    .pipe(gulp.dest('site/fonts'))
});

// Cleaning 
gulp.task('clean', function() {
  return del.sync('dist').then(function(cb) {
    return cache.clearAll(cb);
  });
});

gulp.task('clean:dist', function() {
  return del.sync(['site/**/*', '!site/img', '!site/img/**/*']);
});

// Build Sequences
// ---------------

gulp.task('default', function(callback) {
  runSequence(['sass', 'browserSync'], 'watch',
    callback
  );
});

gulp.task('build', function(callback) {
  runSequence(
    'clean:dist',
    'sass',
    ['useref', 'images', 'fonts'],
    callback
  );
});