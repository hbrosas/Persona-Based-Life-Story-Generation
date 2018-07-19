(function ($) {
    $.fn.ColorPanel = function (options) {
        var settings = $.extend({
            styleSheet: '#cpswitch'
            , colors: {
                '#14a2d2': 'css/color/blue.css',
                '#d2141d': 'css/color/red.css',
                '#cc005f': 'css/color/pink.css',
                '#14d283': 'css/color/green.css',
                '#d2ac14': 'css/color/orange.css'
            }
            , linkClass: 'linka'
            , animateContainer: false
        }, options);
        var panelDiv = this;
		
		$('#cp_toggle').on('click', function(e){
			e.preventDefault();
			 $('ul',panelDiv).slideToggle();
		});
		
        var colors = settings.colors || null;
        if (colors) {
            $.each(colors, function (key, value) {
                var li = $("<li/>");
                var e = $("<a />", {
                    href: value
                    , "class": settings.linkClass, // you need to quote "class" since it's a reserved keyword
                }).css('background-color', key);
                li.append(e);
                $(panelDiv).find('ul').append(li);
            });
            $('ul',panelDiv).on('click', 'a', function (e) {
                e.preventDefault();
                var CssFile = $(this).attr('href') || 'default.css';
                if (settings.animateContainer) {
                    $(settings.animateContainer).fadeOut(function () {
                        $(settings.styleSheet).attr('href', CssFile);
                        // And then:
                        $(this).fadeIn();
                    });
                }
                else {
                    $(settings.styleSheet).attr('href', CssFile);
                }
            });
        }
    };
}(jQuery));