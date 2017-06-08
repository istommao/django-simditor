(function() {
    var djangoJQuery;
    if (typeof jQuery == 'undefined' && typeof django == 'undefined') {
        console.error('ERROR django-simditor missing jQuery. Set SIMDITOR_JQUERY_URL or provide jQuery in the template.');
    } else if (typeof django != 'undefined') {
        djangoJQuery = django.jQuery;
    }

    var $ = jQuery || djangoJQuery;
    $(function() {

    });
});
