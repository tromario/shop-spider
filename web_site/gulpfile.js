'use strict';

var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('bundle-vendor', function() {
    gulp.src([
        // todo: очень важен порядок!
        './node_modules/jquery/dist/jquery.js',
        './node_modules/bootstrap/dist/js/bootstrap.js',
        './node_modules/angular/angular.js',
        './node_modules/angular-resource/angular-resource.js',
        './node_modules/angular-route/angular-route.js',
        './node_modules/angular-ui-bootstrap/dist/ui-bootstrap-tpls.js',
        './node_modules/ramda/dist/ramda.min.js',
        './node_modules/bluebird/js/browser/bluebird.min.js'
    ])
        .pipe(concat('vendor.js', { newLine: '\r\n;\r\n' }))
        .pipe(gulp.dest('./app/static/lib/vendor'));

    gulp
        .src(['./node_modules/requirejs/require.js'])
        .pipe(gulp.dest('./app/static/lib/vendor'))
});
