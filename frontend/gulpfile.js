var gulp = require("gulp");
var sass = require("gulp-sass");
var changed = require('gulp-changed');
var autoprefixer = require('gulp-autoprefixer');
var browserSync  = require('browser-sync').create();
var rename = require('gulp-rename');
var cssnano = require('gulp-cssnano');
var concat = require('gulp-concat');
var uglify = require('gulp-uglifyjs');

const { series, parallel } = gulp;

function style(cb) {
    // Theme
    gulp.src('./assets/scss/**/*.scss')
    .pipe(changed('./assets/css/'))
    .pipe(sass({ outputStyle: 'expanded' }))
    .on('error', sass.logError)
    .pipe(autoprefixer([
        "last 1 major version",
        ">= 1%",
        "Chrome >= 45",
        "Firefox >= 38",
        "Edge >= 12",
        "Explorer >= 10",
        "iOS >= 9",
        "Safari >= 9",
        "Android >= 4.4",
        "Opera >= 30"], { cascade: true }))
    .pipe(gulp.dest('./assets/css/'))
    .pipe(browserSync.stream());
    cb();
}

function minCss(cb) {
    return gulp.src([
        './assets/css/theme.css',
    ])
    .pipe(cssnano())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('./assets/css/'));
    cb();
}

exports.style = series(style, minCss);
