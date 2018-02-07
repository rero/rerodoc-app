require([
    'node_modules/d3/d3',
    'node_modules/angular/angular',
    'node_modules/angular-gettext/dist/angular-gettext',
    'node_modules/angular-sanitize/angular-sanitize.js',
    'node_modules/angular-loading-bar/build/loading-bar',
    'node_modules/invenio-search-js/dist/invenio-search-js'
  ], function() {
    var app = angular.module('rerodocTranslations');
    app.run(['gettextCatalog', function (gettextCatalog) {
       gettextCatalog.setCurrentLanguage(document.documentElement.lang);
    }]);
    angular.module('rerodocHighlights', ['ngSanitize']);
    angular.module('rerodocBriefView', [])
    .filter('summary', function() {
        return function(summaries) {
            var summary = undefined;
            angular.forEach(summaries, function(value) {
              var lang = document.documentElement.lang;
              if(lang === value.language) {
                summary = value.value;
              }
            });
            if (summary && summary.length > 400){
              summary = summary.substring(0, 400).replace(/\s\S+$/, '') + '...';
            }
            return summary
        };
    })
    .filter('roles', function() {
        return function(contributors, roles) {
            var to_return = [];
            angular.forEach(contributors, function(value) {
              if(roles.indexOf(value.role) > -1) {
                to_return.push(value);
              }
            });
            return to_return;
        };
    });
    // When the DOM is ready bootstrap the `invenio-search-js`
    angular.element(document).ready(function() {

      angular.bootstrap(
        document.getElementById("invenio-search"), [
          'invenioSearch', 'angular-loading-bar',
          'rerodocTranslations', 'rerodocHighlights',
          'rerodocBriefView'
        ]
      );
    });
});
