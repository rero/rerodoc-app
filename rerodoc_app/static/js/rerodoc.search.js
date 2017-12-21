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
    // When the DOM is ready bootstrap the `invenio-search-js`
    angular.element(document).ready(function() {

      angular.bootstrap(
        document.getElementById("invenio-search"), [
          'invenioSearch', 'angular-loading-bar', 'rerodocTranslations', 'rerodocHighlights'
        ]
      );
    });
});