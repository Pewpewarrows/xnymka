/*
 * Utility objects and functions, jQuery additions, and Javascript prototype extensions.
 */

/*
 * Scope reference:
 *
 * var foo; // Global
 * bar; // Global
 *
 * function () {
 *     var baz; // Local
 *     waldo; // Global
 * }
 *
 */

/*
 * JSDoc reference:
 *
 * This is a generic description, with a link to a class: {@link ClassName},
 * and a link to a method: {@link ClassName#methodName}.
 *
 * @author name
 * @version number
 * @deprecated
 * @requires OtherClassName description
 * @throws ExceptionType description
 * @see #methodName
 * @see ClassName
 * @see ClassName#methodName
 * @this ObjectTypeThisIs
 * @constructor
 * @addon
 * @member ClassName
 * @base ParentClassName
 * @param {Type} param_name description
 * @returns description_of_returned_value
 * @type ReturnType
 */

/*
 * Extensions to default Javascript prototypes, objects, and types
 */


/*
 * Utility functions and objects
 *
 * I would wrap these in an anonymous function to utilize jQuery,
 * but I'd rather keep them library-agnostic as much as possible.
 */

/* Simple JavaScript Inheritance
 * By John Resig http://ejohn.org/
 * MIT Licensed.
 */
// Inspired by base2 and Prototype
(function(){
    var initializing = false,
    fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;
    // The base Class implementation (does nothing)
    this.Class = function(){};

    // Create a new Class that inherits from this class
    Class.extend = function(prop) {
        var _super = this.prototype;

        // Instantiate a base class (but only create the instance,
        // don't run the init constructor)
        initializing = true;
        var prototype = new this();
        initializing = false;

        // Copy the properties over onto the new prototype
        for (var name in prop) {
            // Check if we're overwriting an existing function
            if (typeof prop[name] == "function" && typeof _super[name] == "function" && fnTest.test(prop[name])) {
                prototype[name] = (function(name, fn){
                    return function() {
                        var tmp = this._super;

                        // Add a new ._super() method that is the same method
                        // but on the super-class
                        this._super = _super[name];

                        // The method only need to be bound temporarily, so we
                        // remove it when we're done executing
                        var ret = fn.apply(this, arguments);
                        this._super = tmp;

                        return ret;
                    };
                })(name, prop[name]);
            } else {
                prototype[name] = prop[name];
            }
        }

        // The dummy class constructor
        function Class() {
            // All construction is actually done in the init method
            if (!initializing && this.init) {
                this.init.apply(this, arguments);
            }
        }

        // Populate our constructed prototype object
        Class.prototype = prototype;

        // Enforce the constructor to be what we expect
        Class.constructor = Class;

        // And make this class extendable
        Class.extend = arguments.callee;

        return Class;
    };
})();

/*
 * http://www.viget.com/inspire/extending-paul-irishs-comprehensive-dom-ready-execution/
 *
 * Essentially, just add 'data-controller' and 'data-action' attributes to the 'body' tag
 * and define those as functions within objects here to get page-specific 'document.ready'
 * code to fire. Big thanks to Paul Irish and Jason Garber.
 *
 * Modified to accept the namespace as an init argument and to place all DOM
 * ready functions in their own inner namespace: 'ready'.
 */
var Site = {
    ns: null,

    exec: function(controller, action) {
        action = (action === undefined) ? 'init' : action;

        if ((controller !== '') && this.ns.ready[controller] && (typeof this.ns.ready[controller][action] === 'function')) {
            this.ns.ready[controller][action]();
        }
    },

    init: function(ns) {
        var body = document.body,
        controller = body.getAttribute('data-controller'),
        action = body.getAttribute('data-action');

        this.ns = ns;

        this.exec('common');
        this.exec(controller);
        this.exec(controller, action);
        this.exec('common', 'finalize');
    }
};

function str_pad (input, pad_length, pad_string, pad_type) {
    // Returns input string padded on the left or right to specified length with pad_string
    //
    // version: 1101.3117
    // discuss at: http://phpjs.org/functions/str_pad
    // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // + namespaced by: Michael White (http://getsprink.com)
    // +      input by: Marco van Oort
    // +   bugfixed by: Brett Zamir (http://brett-zamir.me)
    // *     example 1: str_pad('Kevin van Zonneveld', 30, '-=', 'STR_PAD_LEFT');
    // *     returns 1: '-=-=-=-=-=-Kevin van Zonneveld'
    // *     example 2: str_pad('Kevin van Zonneveld', 30, '-', 'STR_PAD_BOTH');
    // *     returns 2: '------Kevin van Zonneveld-----'
    var half = '', pad_to_go;

    var str_pad_repeater = function (s, len) {
        var collect = '', i;

        while (collect.length < len) {collect += s;}
        collect = collect.substr(0,len);

        return collect;
    };

    input += '';
    pad_string = pad_string !== undefined ? pad_string : ' ';

    if (pad_type != 'STR_PAD_LEFT' && pad_type != 'STR_PAD_RIGHT' && pad_type != 'STR_PAD_BOTH') { pad_type = 'STR_PAD_RIGHT'; }
    if ((pad_to_go = pad_length - input.length) > 0) {
        if (pad_type == 'STR_PAD_LEFT') { input = str_pad_repeater(pad_string, pad_to_go) + input; }
        else if (pad_type == 'STR_PAD_RIGHT') { input = input + str_pad_repeater(pad_string, pad_to_go); }
        else if (pad_type == 'STR_PAD_BOTH') {
            half = str_pad_repeater(pad_string, Math.ceil(pad_to_go/2));
            input = half + input + half;
            input = input.substr(0, pad_length);
        }
    }

    return input;
}

window.isInt = function(x) {
	var y = parseInt(x, 10);

	if (isNaN(y)) {
        return false;
    }

	return (x == y) && (x.toString() == y.toString());
};

// usage: log('inside coolFunc',this,arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function() {
	log.history = log.history || [];   // store logs to an array for reference
	log.history.push(arguments);
    arguments.callee = arguments.callee.caller;

	if (this.console) {
		console.log(Array.prototype.slice.call(arguments));
	}
};


/*
 * jQuery mini-plugins and existing plugin extensions
 */

/*
 * Quick .data() wrapper
 *
 * http://yehudakatz.com/2009/04/20/evented-programming-with-jquery/
 */
var $$ = function(param) {
	var node = $(param)[0];
	var id = $.data(node);
	$.cache[id] = $.cache[id] || {};
	$.cache[id].node = node;
	return $.cache[id];
};

/*
 * http://chris-barr.com/entry/disable_text_selection_with_jquery/
 * modified to be "$" safe by Dakkar Daemor [www.imaginific.com]
 */
(function($) {
	$.fn.disableTextSelect = function() {
		return this.each(function() {
			if ($.browser.mozilla) { // Firefox
					$(this).css('MozUserSelect', 'none');
				} else if ($.browser.msie) { // IE
					$(this).bind('selectstart', function() {
						return false;
					});
				} else { // Opera, etc.
					$(this).mousedown(function() {
						return false;
					});
				}
			});
	};
	$(function($) {
		// No text selection on elements with a class of 'noSelect'
		$('.noSelect').disableTextSelect();
	});
})(jQuery);
