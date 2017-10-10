(function() {
    var djangoJQuery;
    if (typeof jQuery == 'undefined' && typeof django == 'undefined') {
        console.error('ERROR django-simditor missing jQuery. Set SIMDITOR_JQUERY_URL or provide jQuery in the template.');
    } else if (typeof django != 'undefined') {
        djangoJQuery = django.jQuery;
    }

    var $ = jQuery || djangoJQuery;
    $(function() {

        initialiseSimditor();
        function initialiseSimditor() {
            $('textarea[data-type=simditortype]').each(function() {

                if($(this).data('processed') == "0" && $(this).attr('data-id').indexOf('__prefix__') == -1){
                    $(this).data('processed', "1");
                    var dataConfig = $(this).data('config');
                    new Simditor({
                        textarea: $(this),
                        upload: dataConfig.upload,
                        cleanPaste: dataConfig.cleanPaste,
                        tabIndent: dataConfig.tabIndent,
                        pasteImage: dataConfig.pasteImage,
                        toolbar: dataConfig.toolbar,
                        emoji: dataConfig.emoji
                    });
                }
            });
        }

    });
})();
