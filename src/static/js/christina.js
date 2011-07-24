var NRI = NRI || {};

/* Create a closure to maintain scope of the '$',
   ensure that our global variables haven't been messed with,
   and remain compatible with other frameworks.  */
(function(window, document, $, undefined) {

    // It's rare that we'd ever want to cache AJAX responses on the browser
    // side as opposed to a server-side memcached setup for example.
    $.ajaxSetup({
        cache: false
    });

    NRI.global = this;

    NRI.status = null;

    NRI.settings = {
        debug: false,
        ssl: false,
        static_url: '',
        media_url: '',
        search_autocomplete_url: '',

        setup: function() {
            var self = this;

            if (self.debug) {
                self.static_url = '/static/';
            } else {
                self.static_url = '//static.nrishirts.dotcloud.com/';
            }

            self.media_url = '/uploads/';
        }
    };

    NRI.security = {
        shield_len: 8,
        shield_str: 'for(;;);',
        
        disarm_json: function(response) {
            var self = this;

            if (response.substring(0, self.shield_len) !== self.shield_str) {
                return response;
            }

            if (response.length > self.shield_len) {
                response = response.substring(self.shield_len);
            }

            return response;
        }
    };

    NRI.ready = {
        common: {
            // This function will fire on every page first
            init: function() {
                NRI.settings.setup();
            }
        },

        search: {
            main: function() {
                $('#id_q').autocomplete({
                    source: function(request, response) {
                        $.get(NRI.settings.search_autocomplete_url, {
                            q: request.term
                        }, function(data) {
                            response($.map(data.results, function(item) {
                                return {
                                    label: item.name,
                                    value: item.name
                                };
                            }));
                        });
                    },
                    minLength: 2
                });
            }
        }
    };

    /* DOM Ready */
	$(function() {
        Site.init(NRI);
	});

    /* Window Ready */
	$(window).bind("load", function() {
	});

})(this, this.document, jQuery);
